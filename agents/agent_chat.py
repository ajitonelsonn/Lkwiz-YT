import streamlit as st
from langchain_openai import ChatOpenAI
from langchain.prompts.chat import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate

AI71_BASE_URL = "https://api.ai71.ai/v1/"

def get_ai71_chat(api_key):
    #print(f"Using API Key: {api_key}")  # Debugging statement
    return ChatOpenAI(
        model="tiiuae/falcon-180B-chat",
        api_key=api_key,
        base_url=AI71_BASE_URL,
        streaming=True,
    )

def ask_question(transcription, question, api_key):
    template = """
    You are a helpful assistant. Given the following transcription of a YouTube video, answer the user's question based on the content:
    {transcription}

    Instructions:
    - If the user's question is a greeting (like "Hi" or "Hello"), respond with "Hi, I'm Lkwiz-YT, your YouTube video link assistant. How can I help you?"
    - If the user's question is not relevant to the content of the transcription, respond with "Your question is not relevant to the YouTube video. Please ask about the YouTube video link that you provide."
    - Ensure your answer is no more than 50 words.

    Question: {question}
    """
    try:
        system_message_prompt = SystemMessagePromptTemplate.from_template(template)
        human_message_prompt = HumanMessagePromptTemplate.from_template("{question}")
        chat_prompt = ChatPromptTemplate.from_messages(
            [system_message_prompt, human_message_prompt]
        )
        formatted_messages = chat_prompt.format_messages(
            transcription=transcription, question=question
        )
        ai71_chat = get_ai71_chat(api_key)
        return ai71_chat.invoke(formatted_messages)
    except Exception as e:
        if "AuthenticationError" in str(e):
            st.error("Incorrect API key provided. Please check and update your API key.")
            st.stop()
        else:
            st.error(f"An error occurred: {str(e)}")
            st.stop()