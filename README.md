# 🚀 Iteratively Enhanced Image Generation

Build an iterative image enhancement process using the capabilities of Stable Diffusion and GPT-4 Vision. Allowing the users to generate images based on textual descriptions and iteratively refine these images based on GPT-4Vision's feedback.

### [Read the blog!](https://www.ionio.ai/blog/iteratively-improving-product-images-using-gpt-v-and-stable-diffusion)

### Architecture
![image](https://github.com/Ionio-io/Iterative-Image-Gen/assets/87160848/d11b5ecc-48dc-44b1-adcd-afbbbfe9f20b)

## Features

- Generate initial images based on user-provided textual descriptions.
- Utilize GPT-4 Vision to analyze generated images and suggest improvements.
- Allow users to refine the image iteratively based on AI suggestions.
- Support multiple rounds of feedback and image regeneration to refine the outcome.

## 🤖 Setup

1. **Clone the Repository**: Clone this repository to your local machine.
2. **Install Dependencies**:
   ```bash
   pip install streamlit requests python-dotenv
   ```
### Setup Environment Variables:
Add your OpenAI API key and Stability AI key to the .env file.
```
OPENAI_API_KEY = <key_here>
STABILITYAI_API_KEY = <key_here>
```

### ⚙️ Running the App
To run the application, navigate to the directory containing the app and run:
```
streamlit run demo.py
```


## 🤔 How It Works
- **Input Description:** Start by entering a description for the image you want to generate.
- **Generate Image:** Click 'Generate Image' to create the initial image.
- **Feedback and Refinement:** The AI analyzes the image and provides feedback. Edit this feedback if necessary and use it to regenerate a refined image.
- **Iterative Process:** Continue refining the image through multiple iterations.
Technology
- **Stable Diffusion:** Used for generating images based on textual descriptions.
- **GPT-4 Vision:** Provides AI-driven feedback for image refinement.
Feel free to explore the code and adapt it for your own projects!


## Example Prompt
Imagine a young Indian man showcasing his casual fashion sense. He wears a dark pant paired with a subtle, geometric printed full-sleeve shirt. His accessories include a simple wrist watch, and shoes with brown leather. He stands against the backdrop of a an aesthetic grey color.

![image](https://github.com/Ionio-io/Iterative-Image-Gen/assets/87160848/352a1fa2-1df2-4065-af2d-d01727550a68)
![image](https://github.com/Ionio-io/Iterative-Image-Gen/assets/87160848/b04933bc-9047-4756-9dd0-d1117a8719d3)
![image](https://github.com/Ionio-io/Iterative-Image-Gen/assets/87160848/d9ea58cd-964d-4138-8713-696948fcf994)
![image](https://github.com/Ionio-io/Iterative-Image-Gen/assets/87160848/4d5adbcb-a9b1-4d12-864f-cef02bfee37c)
![image](https://github.com/Ionio-io/Iterative-Image-Gen/assets/87160848/afc0cdf0-017a-4f91-afe7-0fcf9e498f16)
![image](https://github.com/Ionio-io/Iterative-Image-Gen/assets/87160848/2044a7af-2882-4290-9c52-b13e164c9cda)
![image](https://github.com/Ionio-io/Iterative-Image-Gen/assets/87160848/d455b3a8-997d-457e-ab4d-65a34008cc82)






