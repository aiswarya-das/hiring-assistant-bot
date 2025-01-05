# TalentScout Hiring Assistant

## Project Overview
The **TalentScout Hiring Assistant** is an AI-powered chatbot designed to streamline the hiring process. It collects key user information, such as personal details and tech stack, and generates tailored technical questions. Based on the responses, it evaluates if the user is suitable for the job role, providing valuable insights for the hiring process.

## Installation Instructions
1. **Clone the repository**:
   ```
   git clone <repository-url>
   cd <repository-folder>
2. **Create a virtual environment**:
   ```
   python -m venv venv
3. **Activate the virtual environment**:
   ```
   source venv/bin/activate
4. **Install dependencies**:
    ``` 
    pip install streamlit openai
5. **Run the application**:
    ```
    streamlit run main.py
## Usage Guide

- Enter the OpenAI API key in the input field in the sidebar to start interacting with the assistant.
- The assistant will ask for details like **name**, **email**, **phone number**, and **tech stack**.
- Once the information is gathered, the assistant will generate **technical questions** based on the provided tech stack.
- User responses are evaluated, and feedback is given regarding their suitability for the job position.

## Technical Details

- **Libraries**: `streamlit`, `openai`
- **Model**: **GPT-4o-mini** by OpenAI for generating responses and technical questions.
- **State Management**: Utilizes `st.session_state` to track user inputs and manage conversation history.

## Prompt Design

Prompts are designed to:

- Collect personal details such as **name**, **email**, and **phone number**.
- Generate **technical questions** based on the user’s tech stack.
- Evaluate user responses and provide feedback on **job suitability**.

## Challenges & Solutions

- **Dynamic Question Generation**: The assistant generates technical questions based on the user's tech stack using OpenAI's GPT model.
- **API Key Input**: Instead of using a `.env` file, the user provides the OpenAI API key directly through a text input field in the sidebar.
- **Input Validation**: Although not fully implemented, potential improvements include adding regex validation for email and phone number inputs.

