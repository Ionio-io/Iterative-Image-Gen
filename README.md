# Iteratively Enhanced Images Demo

This Streamlit application demonstrates an iterative image enhancement process using the capabilities of Stable Diffusion and GPT-4 Vision. It allows users to generate images based on textual descriptions and iteratively refine these images based on AI-generated feedback.

## Features

- **Image Generation**: Generate initial images based on user-provided textual descriptions.
- **Automated Feedback**: Utilize GPT-4 Vision to analyze generated images and suggest improvements.
- **Iterative Enhancement**: Allow users to refine the image iteratively based on AI suggestions.
- **Multiple Iterations**: Support multiple rounds of feedback and image regeneration to refine the outcome.

## Setup

1. **Clone the Repository**: Clone this repository to your local machine.
2. **Install Dependencies**:
   ```bash
   pip install streamlit requests python-dotenv
   ```
### Setup Environment Variables:
Rename .env.example to .env.
Add your OpenAI API key and Stability AI key to the .env file.
### Running the App
To run the application, navigate to the directory containing the app and run:
```
streamlit run demo.py
```

## How It Works
- **Input Description:** Start by entering a description for the image you want to generate.
- **Generate Image:** Click 'Generate Image' to create the initial image.
- **Feedback and Refinement:** The AI analyzes the image and provides feedback. Edit this feedback if necessary and use it to regenerate a refined image.
- **Iterative Process:** Continue refining the image through multiple iterations.
Technology
- **Stable Diffusion:** Used for generating images based on textual descriptions.
- **GPT-4 Vision:** Provides AI-driven feedback for image refinement.
Feel free to explore the code and adapt it for your own projects!

