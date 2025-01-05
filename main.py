import streamlit as st
# from dotenv import load_dotenv
from openai import OpenAI
import os
import re

# Initialize session state variables
if "conversation" not in st.session_state:
    st.session_state.conversation = []  # Store the conversation history
if "question_index" not in st.session_state:
    st.session_state.question_index = 0  # Track the current question
if "responses" not in st.session_state:
    st.session_state.responses = {}  # Store user responses
if "tech_questions" not in st.session_state:
    st.session_state.tech_questions = []  # Store generated technical questions
if "tech_evaluations" not in st.session_state:
    st.session_state.tech_evaluations = []  # Store technical evaluations

# load_dotenv()
# client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

api_key = st.sidebar.text_input("Enter your OpenAI API key", type="password")
client = OpenAI(api_key=api_key)

if api_key:
    if st.sidebar.button("Generate Response"):
        try:
            result = client.chat.completions.create(
                model="gpt-4o-mini",
                store=True,
                messages=[{"role": "user", "content": "hi"}],
            )
            st.sidebar.write("Api key working")
        except Exception as e:
            st.sidebar.error("Invalid OpenAI API key. Please enter a valid key.")
else:
    st.sidebar.warning("Please enter your OpenAI API key.")


# Define the questions
questions = [
    "What's your full name?",
    "whats your email address?",
    "What's your phone number?",
    "What's your years of experience?",
    "What's your desired position?",
    "What's your location?",
    "What's your tech stack? (include programming languages, frameworks, databases, and tools)",
]

st.markdown(
    """
    <style>
        /* Import Poppins font from Google Fonts */
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600&display=swap');

        /* Main container for the chat messages */
        .assistant, .user {
            margin: 15px 0;
            padding: 15px 20px;
            padding-left: 50px; /* Added padding for assistant to make room for the icon */
            padding-right: 50px; /* Added padding for user to make room for the icon */
            border-radius: 20px;
            font-family: 'Poppins', sans-serif;
            font-size: 16px;
            max-width: 75%;
            display: inline-block;
            line-height: 1.5;
            position: relative;
            transition: transform 0.3s, box-shadow 0.3s;
            word-wrap: break-word;
        }

        /* Assistant chat bubble */
        .assistant {
            background-color: #1c3d63; /* Soft blue-gray */
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
            color: #f0f4f8; /* Light gray text */
            text-align: left;
            margin-right: auto;
            display: flex;
            align-items: center;
        }

        /* User chat bubble */
        .user {
            background-color: #4c9e9b; /* Soft teal */
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
            color: #f0f4f8; /* Light gray text */
            text-align: right;
            margin-left: auto;
            display: flex;
            align-items: center;
        }

        /* Assistant icon */
        .assistant::before {
            content: "🤖";
            font-size: 25px; /* Adjust the size of the icon */
            position: absolute;
            left: -35px; /* Position it outside the bubble */
            top: 50%;
            transform: translateY(-50%);
        }

        /* User icon */
        .user::before {
            content: "👤";
            font-size: 25px; /* Adjust the size of the icon */
            position: absolute;
            right: -35px; /* Position it outside the bubble */
            top: 50%;
            transform: translateY(-50%);
        }

        /* Hover effect for chat bubbles */
        .assistant:hover, .user:hover {
            transform: scale(1.05);
            box-shadow: 0 6px 12px rgba(0, 0, 0, 0.25);
        }

        /* Chat container styling */
        .chat-container {
            padding: 20px;
            margin: auto;
            background: #121212; /* Very dark background */
            border: 2px solid #333333; /* Dark border for contrast */
            border-radius: 15px;
            max-width: 800px;
            box-shadow: 0 8px 16px rgba(0, 0, 0, 0.3);
            overflow-y: auto;
            max-height: 400px;
        }

        /* Style for the input field */
        .stTextInput input {
            padding: 12px;
            border: 2px solid #555555;
            border-radius: 8px;
            font-size: 16px;
            color: #ffffff;
            background-color: #2a2a2a; /* Dark background for input */
            transition: border-color 0.3s, box-shadow 0.3s;
            font-family: 'Poppins', sans-serif;
        }

        .stTextInput input:focus {
            border-color: #4c9e9b;
            box-shadow: 0 0 8px rgba(76, 158, 155, 0.4);
        }

        /* Style for the button */
        .stButton button {
            background-color: #1c3d63;
            color: white;
            font-size: 16px;
            padding: 10px 20px;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            transition: all 0.3s;
            font-family: 'Poppins', sans-serif;
        }

        .stButton button:hover {
            background-color: #155b7a;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    "<h1 class='main-title'>TalentScout Hiring Assistant</h1>", unsafe_allow_html=True
)

st.chat_message("assistant").markdown(
    "Hello! I'm your Hiring Assistant at TalentScout. I'll help you with your job application process. "
    "Let's start by gathering some information from you. If you want to end the conversation at any time, just type 'exit'."
)

# Validation functions
# def validate_phone_number(phone_number):
#     pattern = r'^\+?\d{1,4}?[-.\s]?\(?\d{1,3}?\)?[-.\s]?\d{1,4}[-.\s]?\d{1,4}[-.\s]?\d{1,9}$'
#     if not re.match(pattern, phone_number):
#         return False, "Please enter a valid phone number (including optional country code and dashes)."
#     return True, ""

# def validate_non_empty_input(input_text):
#     if not input_text.strip():
#         return False, "This field cannot be empty. Please provide a valid response."
#     return True, ""

# def validate_email(email):
#     pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$'
#     if not re.match(pattern, email):
#         return False, "Please enter a valid email address."
#     return True, ""


# Function to display all chat messages in session state
def display_conversation():
    for message in st.session_state.conversation:
        if message["role"] == "assistant":
            st.markdown(
                f'<div class="assistant">{message["content"]}</div>',
                unsafe_allow_html=True,
            )
        elif message["role"] == "user":
            st.markdown(
                f'<div class="user">{message["content"]}</div>', unsafe_allow_html=True
            )


# Display the chat history
display_conversation()


def generate_tech_questions(tech_stack):
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        store=True,
        messages=[
            {
                "role": "user",
                "content": "Generate 3-5 technical questions based on the tech stack (if the user-given tech stack is unexpected or not meaningful, provide meaningful responses to the user): "
                + tech_stack,
            }
        ],
    )
    msgcontent = completion.choices[0].message.content
    questions = [line.strip() for line in msgcontent.split("\n") if line.strip()]

    st.session_state.tech_questions.extend(questions)
    for question in questions:
        st.session_state.conversation.append({"role": "assistant", "content": question})
        st.markdown(f'<div class="assistant">{question}</div>', unsafe_allow_html=True)

    # print(msgcontent)  # For debugging purposes
    # print(questions, "questions")  # For debugging purposes


def evaluate_user_answers(tech_stack, user_answers, position):
    # Constructing the prompt to evaluate the answers
    prompt = f"""
    Evaluate the following:

    Tech Stack provided by user: {tech_stack}
    Answers to tech questions: {user_answers}
    Job position: {position}

    Check if the user's answers are correct for the tech questions provided by the assistant. 
    If the answers are suitable, say that they are fit for the position and provide next steps. 
    If not, provide feedback on how they can improve. Most importantly,  inform them about the next steps.
    """

    completion = client.chat.completions.create(
        model="gpt-4o-mini", store=True, messages=[{"role": "user", "content": prompt}]
    )

    evaluation = completion.choices[0].message.content
    return evaluation


if st.session_state.question_index < len(questions):
    current_question = questions[st.session_state.question_index]

    if (
        not st.session_state.conversation
        or st.session_state.conversation[-1]["content"] != current_question
    ):
        st.session_state.conversation.append(
            {"role": "assistant", "content": current_question}
        )
        st.markdown(
            f'<div class="assistant">{current_question}</div>', unsafe_allow_html=True
        )

    user_input = st.chat_input("Your answer:")
    if user_input == "exit":
        st.markdown(f'<div class="assistant">Goodbye!</div>', unsafe_allow_html=True)
        st.session_state.question_index = len(questions)  # End the conversation
        st.session_state.tech_questions = []  # Clear tech questions for the next user
        st.session_state.responses = {}  # Clear user responses
        st.session_state.evaluation = []  # Clear evaluation history
        st.stop()

    if user_input:
        # Save the user response
        st.session_state.conversation.append({"role": "user", "content": user_input})
        st.session_state.responses[current_question] = user_input

        if current_question == questions[-1]:
            st.markdown(
                f'<div class="assistant">Going to generate some technical questions based on your tech stack.</div>',
                unsafe_allow_html=True,
            )
            generate_tech_questions(user_input)

        # Move to the next question
        st.session_state.question_index += 1

        # Rerun the script to update the conversation dynamically
        st.rerun()

# Handle tech answers after gathering user info
if st.session_state.question_index >= len(questions):
    # Check if tech questions exist
       if st.session_state.tech_questions:
        # Ask user for answers to the technical questions
        tech_answer = st.chat_input("Answer the technical questions here:")
        answers = [line.strip() for line in tech_answer.split("\n") if line.strip()]
        for answer in answers:
            print(answer, "answer")
            st.sidebar.write(answer)
            st.markdown(f'<div class="user">{answer}</div>', unsafe_allow_html=True)
            st.session_state.conversation.append({"role": "user", "content": answer})

            position = st.session_state.responses.get("What's your desired position?")
            tech_stack = st.session_state.responses.get("What's your tech stack?")

            evaluation = evaluate_user_answers(tech_stack, tech_answer, position)

            # print("evaluation", evaluation)

            evals = [line.strip() for line in evaluation.split("\n") if line.strip()]

            st.session_state.tech_evaluations.extend(evals)
            for eva in evals:
                st.session_state.conversation.append(
                    {"role": "assistant", "content": eva}
                )
                st.markdown(
                    f'<div class="assistant">{eva}</div>', unsafe_allow_html=True
                )

            # End the conversation
            st.markdown(
                f'<div class="assistant">Thank you for your time! The hiring process is complete. We will get back to you with the next steps.</div>',
                unsafe_allow_html=True,
            )

            st.session_state.question_index = len(questions)  # End the conversation
            st.session_state.tech_questions = []  # Clear tech questions for the next user
            st.session_state.responses = {}  # Clear user responses
            st.session_state.evaluation = []  # Clear evaluation history
            st.stop()
