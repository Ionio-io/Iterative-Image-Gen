import streamlit as st
import requests
from requests_toolbelt.multipart.encoder import MultipartEncoder
import base64
import os
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
    improvement_question = f"Based on the original intent to depict '{original_prompt}', suggest a concise prompt for refining this image:"
    data = {
        "model": "gpt-4-vision-preview",
        "messages": [
            {"role": "system", "content": "You are a helpful assistant that generates specific improvement prompts based on image analysis."},
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
        feedback = response.json()['choices'][0]['message']['content']
        return feedback.split('.')[0]  # Example to just return the first sentence
    else:
        return f"Failed to analyze image: {response.text}"
    
st.title('Iteratively Enhanced Images Demo')
user_prompt = st.text_area('Enter a description for the image:', height=200, key='user_prompt')

if 'iterations' not in st.session_state:
    st.session_state.iterations = []

if st.button('Generate Image'):
    if 'iterations' not in st.session_state:
        st.session_state.iterations = []
    params = {
        "prompt": user_prompt,
        "mode": "text-to-image",
        "output_format": "png",
        "size": "1024x1024"
    }
    image_b64 = send_generation_request(host, params, os.getenv('api_key_stability'))
    if image_b64:
        st.session_state.iterations.append({'prompt': user_prompt, 'image': image_b64})
        feedback_prompt = analyze_image_with_gpt4(image_b64, os.getenv('api_key_openai'), user_prompt)
        st.session_state.iterations[-1]['feedback'] = feedback_prompt
        feedback_edit = st.text_area("Edit the improvements before regenerating the image:", feedback_prompt, height=150)
        st.session_state.iterations[-1]['feedback_edit'] = feedback_edit

if 'iterations' in st.session_state and st.button('Regenerate Image with Suggestions'):
    last_iteration = st.session_state.iterations[-1]
    new_params = {
        "prompt": last_iteration['feedback_edit'],
        "mode": "text-to-image",
        "output_format": "png",
        "size": "1024x1024"
    }
    new_image_b64 = send_generation_request(host, new_params, os.getenv('api_key_stability'))
    if new_image_b64:
        st.session_state.iterations.append({'prompt': last_iteration['feedback_edit'], 'image': new_image_b64})
        feedback_prompt = analyze_image_with_gpt4(new_image_b64, os.getenv('api_key_openai'), last_iteration['feedback_edit'])
        st.session_state.iterations[-1]['feedback'] = feedback_prompt
        feedback_edit = st.text_area("Edit improvements for further refinement:", feedback_prompt, height=150)
        st.session_state.iterations[-1]['feedback_edit'] = feedback_edit

for i, iteration in enumerate(st.session_state.iterations):
    st.image(iteration['image'], caption=f'Iteration {i+1}: Image')
    st.write(f"Iteration {i+1}: Prompt - ", iteration['prompt'])
    if 'feedback' in iteration:
        st.write(f"Iteration {i+1}: Feedback - ", iteration['feedback'])
