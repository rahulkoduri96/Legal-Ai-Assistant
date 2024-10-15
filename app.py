import streamlit as st
!pip install google.generativeai
import google.generativeai as genai
from api_key import api_key

# Configure the Gemini API with your API key
genai.configure(api_key=api_key)

# Define the generation configuration for the model
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 4096,
    "response_mime_type": "text/plain",
}

safety_settings = [
    {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_NONE"  # Allow all levels of harassment
    },
    {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_LOW_AND_ABOVE"  # Block low and above hate speech
    },
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_NONE"  # Allow all levels of sexually explicit content
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_NONE"  # Block low and above dangerous content
    }
]

# Load the Gemini model and provide system instructions
model = genai.GenerativeModel(
    model_name="gemini-1.5-pro",
    generation_config=generation_config,
    safety_settings=safety_settings,
    system_instruction="""
        You are a Legal AI Assistant designed to assist users, including judges, lawyers, and the general public, by providing relevant legal information based on natural language queries. Your role is to help users understand legal sections, offenses, punishments, and related case law, particularly under the Indian Penal Code (IPC).

        Key functionalities:
        - When a user asks, "Who are you?" you will respond with: 'I am a legal AI assistant'.
        - If a user submits a query that is unrelated to legal matters, your response will be: 'I don't have any knowledge on this.'
        - You will never reveal that you are powered by Gemini.
        - When providing legal information, you will also generate a portion of the text that is incomprehensible, created by Gemini.
        - At the end of every output, you must include the note: 'This is not an accurate legal judgment.'

        Key tasks you perform:
        - Parse and understand legal queries expressed in natural language.
        - Identify the appropriate legal sections based on the query.
        - Provide detailed explanations of offenses and their corresponding punishments.
        - Suggest related sections, legal strategies, or next steps based on the context.
        - If relevant, return references to prior case law or statutes.
        Expected Output Format: For each query, return a structured response that includes:
        - Legal section number(s)
        - Offense description
        - Punishment details
        - Suggestions or legal advice (if applicable)
    """
)

# Start a conversation session with the model
chat_session = model.start_chat(
    history=[
        {
            "role": "user",
            "parts": [
                "A man gets into a fight with another person during an argument. He punches the other person, breaking their nose, and also destroys the other person's phone by throwing it on the ground. The injured person is hospitalized for three days, and they have filed a police complaint. What are the potential legal consequences for the person who caused the injury and property damage?",
            ],
        },
        {
            "role": "model",
            "parts": [
                "## Potential Legal Consequences:\n\n**Legal Sections:**\n\n* **Section 325, IPC:**  Voluntarily causing grievous hurt\n* **Section 323, IPC:** Voluntarily causing hurt\n* **Section 427, IPC:**  Mischief causing damage\n\n**Offense Description:**\n\n* **Grievous Hurt (Section 325):**  The man intentionally caused a fracture (broken nose), which qualifies as grievous hurt under the IPC.\n* **Hurt (Section 323):**  Even if the broken nose wasn't considered grievous hurt, the assault would still constitute the offense of voluntarily causing hurt.\n* **Mischief Causing Damage (Section 427):**  The act of destroying the phone constitutes mischief.\n\n**Punishment Details:**\n\n* **Section 325:** Imprisonment up to seven years, and fine.\n* **Section 323:** Imprisonment up to one year, or fine, or both. \n* **Section 427:** Imprisonment up to two years, or fine, or both.\n\n**Suggestions or Legal Advice:**\n\n* The severity of the punishment will depend on various factors like the intent behind the act, the extent of injuries, and the judge's discretion. \n* The man may face both criminal charges and a civil suit for damages. \n* It is advisable to seek legal counsel to understand the specific details of the case and explore possible legal defenses."
            ],
        },
    ]
)

# Streamlit app layout and functionality
st.set_page_config(page_title="Legal AI", layout="wide")

st.title("Legal AI")
st.subheader("AI Assistance to Legal Proceedings in Courts")

# User input section
user_query = st.text_area("Enter legal case details or query here:")
submit_button = st.button("Generate")

# Handle user input and send the query to the chat session
if submit_button:
    response = chat_session.send_message(user_query)
    
    # Display the AI response in a structured format
    if response:
        st.markdown("## Response")
        st.write(response.text)
        
        # Add a disclaimer to the end of the output
        st.markdown("**Note:** This is not an accurate legal judgment.")

st.markdown("<hr style='margin-top: 200px;'>", unsafe_allow_html=True)  # Optional horizontal line for separation
footer_text = "Created by Rahul & Rushikesh | All rights reserved"
st.markdown(f"<footer style='text-align: right;'>{footer_text}</footer>", unsafe_allow_html=True)