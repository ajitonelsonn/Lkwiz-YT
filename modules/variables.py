import streamlit as st
from helpers.toast_messages import get_random_toast

# Initialize session state variables
def initialize_session_state():
    if 'first_time' not in st.session_state:
        st.session_state.first_time = True
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    if 'chat_input' not in st.session_state:
        st.session_state.chat_input = ''
    if 'quiz_data_list' not in st.session_state:
        st.session_state.quiz_data_list = []
    if 'user_answers' not in st.session_state:
        st.session_state.user_answers = []
    if 'correct_answers' not in st.session_state:
        st.session_state.correct_answers = []
    if 'randomized_options' not in st.session_state:
        st.session_state.randomized_options = []
    if 'show_chat' not in st.session_state:
        st.session_state.show_chat = False
    if 'score_submitted' not in st.session_state:
        st.session_state.score_submitted = False
    if 'quiz_started' not in st.session_state:
        st.session_state.quiz_started = False
    if 'video_id' not in st.session_state:
        st.session_state.video_id = ''
    if 'video_transcription' not in st.session_state:
        st.session_state.video_transcription = ''

    # Check if user is new or returning using session state.
    if st.session_state.first_time:
        message, icon = get_random_toast()
        st.toast(message, icon=icon)
        st.session_state.first_time = False