import streamlit as st
import base64
from agents.agent_chat import ask_question

def get_base64_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode()

def display_chat(AI71_API_KEY):
    st.subheader("Chat about this video")
    with st.expander("💬 **Some Tips for Chat:**"):
        st.markdown(
        """
        - What is this video talking about?
        - 🇨🇳    Explain in Chinese language
        - 🇦🇪    Explain in Arabic language
        """
    )
    user_img_base64 = get_base64_image("imagen/user.png")
    bot_img_base64 = get_base64_image("imagen/bot.png")

    for user_q, bot_a in st.session_state.chat_history:
        st.markdown("""
        <div style="display: flex; align-items: center; margin-bottom: 8px; background-color: #f0f0f5; padding: 8px; border-radius: 10px;">
            <img src="data:image/png;base64,{}" style="width: 32px; height: 32px; border-radius: 50%; margin-right: 8px;">
            <div>{}</div>
        </div>
        """.format(user_img_base64, user_q), unsafe_allow_html=True)
        st.markdown("""
        <div style="display: flex; align-items: center; margin-bottom: 8px; background-color: #e8f4f8; padding: 8px; border-radius: 10px;">
            <img src="data:image/png;base64,{}" style="width: 32px; height: 32px; border-radius: 50%; margin-right: 8px;">
            <div>{}</div>
        </div>
        """.format(bot_img_base64, bot_a), unsafe_allow_html=True)

    def ask_question_callback():
        user_question = st.session_state.chat_input
        if user_question.strip() != "":
            with st.spinner("Getting the answer..."):
                answer = ask_question(st.session_state.video_transcription, user_question, AI71_API_KEY)
                st.session_state.chat_history.append((user_question, answer.content))
                st.session_state.chat_input = ''  
                st.session_state.update() 

    with st.form(key="chat_form"):
        user_question = st.text_input("Ask a question about the video:", key="chat_input", value=st.session_state.chat_input)
        ask_submitted = st.form_submit_button("Ask", on_click=ask_question_callback)