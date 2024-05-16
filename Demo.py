import streamlit as st
import requests
from requests_toolbelt.multipart.encoder import MultipartEncoder
import base64
import os
import re
from dotenv import load_dotenv
load_dotenv()

host = 'https://api.stability.ai/v2beta/stable-image/generate/sd3'

def send_generation_request(host, params, api_key):
    fields = {key: (None, value) for key, value in params.items()}
    m = MultipartEncoder(fields=fields)
    headers = {
        "Accept": "image/*",
        "Authorization": f"Bearer {os.getenv('api_key_stability')}",
        "Content-Type": m.content_type
    }
    response = requests.post(host, headers=headers, data=m)
    if response.ok:
        return f"data:image/png;base64,{base64.b64encode(response.content).decode()}"
    else:
        raise Exception(f"HTTP {response.status_code}: {response.text}")

def analyze_image_with_gpt4(image_b64, api_key, original_prompt):
    improvement_question = f"Here is the prompt which was used to generate the given image {original_prompt}"
    data = {
        "model": "gpt-4-vision-preview",
        "messages": [
            {"role": "system", "content": """
             You are a helpful assistant that generates specific improvements for a specific object in an image. You will be given an older prompt to an image and you will be given an image which was generated using that prompt. Your job is to find the focused object from the prompt and provide a feedback and a new prompt to improve the given object in an image and your focus should be only to improve the given object in an image and your new prompt will be more focused on that object specifically.

             Your final response must be like this
             <feedback>
             Your feedback here
             </feedback>

             <prompt>
             New prompt here
             </prompt>
             """},
            {"role": "user", "content": [
                {"type": "image_url", "image_url": image_b64},
                {"type": "text", "text": improvement_question}
            ]}
        ]
    }
    headers = {
        "Authorization": f"Bearer {os.getenv('api_key_openai')}",
        "Content-Type": "application/json"
    }
    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=data)
    if response.status_code == 200:
        res = response.json()['choices'][0]['message']['content']
        # Define the regular expression pattern
        pattern = r"<feedback>(.*?)</feedback>.*?<prompt>(.*?)</prompt>"

        matches = re.findall(pattern, res, re.DOTALL)
        # Use re.findall() to find all matches of the pattern in the input string
        if matches:
            feedback, prompt = matches[0]
            return feedback,prompt  # Example to just return the first sentence
        else:
            return None, None
    else:
        return f"Failed to analyze image: {response.text}",None
    
st.title('Iteratively Enhanced Images Demo')
user_prompt = st.text_area('Enter a description for the image:', height=200, key='user_prompt')

if 'iterations' not in st.session_state:
    st.session_state.iterations = []

def start_iteration(user_prompt):
    if 'iterations' not in st.session_state:
        st.session_state.iterations = []

    st.session_state.iterations.append({'prompt': user_prompt})
    iterations = 0
    while(iterations != 4):
        print("Iteration", iterations + 1)
        st.session_state.iterations[iterations]['expanded'] = True
        with st.expander(f"Iteration {iterations+1}",expanded=st.session_state.iterations[iterations]['expanded']):
            
            print("Generating an image")
            params = {
                "prompt": st.session_state.iterations[-1]["prompt"],
                "mode": "text-to-image",
                "output_format": "png",
                "size": "1024x1024"
            }
            image_b64 = send_generation_request(host, params, os.getenv('api_key_stability'))
            if image_b64:
                st.session_state.iterations[-1]['image'] = image_b64
                user_prompt = st.session_state.iterations[-1]['prompt']
                st.image(image_b64, caption=f'Iteration {iterations+1}: Image')
                st.write(f"Original Prompt - ", user_prompt)
                feedback,prompt = analyze_image_with_gpt4(image_b64, os.getenv('api_key_openai'), user_prompt)
                print("Feedback:",feedback)
                print("New Prompt:",prompt)
                if prompt != None:
                    st.write(f"Feedback - ", feedback)
                    st.write(f"New Prompt - ", prompt)
                    st.session_state.iterations[iterations]['feedback'] = feedback
                    st.session_state.iterations.append({'prompt': prompt})
                else:
                    st.write(f"Failed to generate feedback for given image!")
        st.session_state.iterations[iterations]['expanded'] = False  
        iterations += 1

if st.button('Generate Image'):
    start_iteration(user_prompt=user_prompt)