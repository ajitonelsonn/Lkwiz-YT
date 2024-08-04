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
        - If this is the user's first question, respond with "Hi, I'm Lkwiz-YT, your YouTube video link assistant." and answer the question if there is one.
            - Example Question: Can you use Tetum language?
            - Example Answer: Hi, I'm Lkwiz-YT, your YouTube video link assistant. Yes, I can use Tetum language.
        - If the user asks to use Tetum language or any other specific language, respond in that language and continue to use that language until the user requests to switch to another language.
        - If the user's question is not relevant to the content of the transcription, respond with "Your question is not relevant to the YouTube video. Please ask about the YouTube video link that you provide." or answer in the language that the user provided.
        - Ensure your answer is no more than 50 words.

        Example Conversation:
            What is this video talking about?
            This video is about the new language model called "Falcon 180b" developed by Tii. It is currently the most powerful large language model in the world with 180 billion parameters, trained on 3.5 trillion tokens, and is open access for both researchers and commercial users. Tii is striving to create a more inclusive AI world with this new technology.
            Explain with Tetum language
            Video ne'e hakerek kona ba modelu lian foun naran "Falcon 180b" ne'ebé desenvolve husi Tii. Modelu ida ne'e mak modelu lian bo'ot liu iha mundu ne'ebé iha 180 bilyon parametru sira, treinadu iha liña 3.5 trilhaun token, no atu mai maka'ak horik-kria ai-hanoin komersial nian hodi peskizadór sira bele uza. Tii buka atu kria mundu AI ida ne'ebé liu ho teknoloji foun ne'e.


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