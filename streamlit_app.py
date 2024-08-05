import streamlit as st
import base64  # Ensure this import is present
from modules.variables import initialize_session_state
from helpers.youtube_utils import extract_video_id_from_url, get_transcript_text
from modules.quiz import create_quiz, display_quiz, display_quiz_results
from modules.chat import display_chat, get_base64_image

st.set_page_config(
    page_title="YTLafaekQuiz",
    page_icon="imagen/logo.png",
    layout="centered",
    initial_sidebar_state="auto"
)

initialize_session_state()

user_img_base64 = get_base64_image("imagen/user.png")
bot_img_base64 = get_base64_image("imagen/bot.png")

with st.sidebar:
    img_path = "imagen/slidebar_avatar1.png"
    img_base64 = get_base64_image(img_path)
    if img_base64:
        st.sidebar.markdown(
            '<img src="data:image/png;base64,{}" class="cover-glow">'.format(img_base64),
            unsafe_allow_html=True,
        )

    st.sidebar.markdown("---")
    st.header("👨‍💻 About the Author")
    st.write("""
    Hello! I'm **Ajito Nelson**, a native Tetum 🇹🇱 speaker with a keen interest in Machine Learning and Artificial Intelligence.
    """)

    st.divider()
    st.subheader("🔗 Connect with Me", anchor=False)
    st.markdown(
        """
        - [🧸 Source Code](https://github.com/ajitonelsonn/Lkwiz-YT)
        - [🎞️ YouTube Channel](https://www.youtube.com/@anotilkharu59)
        - [👔 LinkedIn](https://www.linkedin.com/in/ajitonelson/)
        """
    )

    st.divider()
    st.subheader("Welcome to Lafaek Quiz YouTube!", anchor=False)
    st.write("Test your knowledge with fun and challenging questions on various topics. Join us for a learning adventure and see how much you know. Let's learn and grow together!")

    st.divider()
    st.write("From **Timor-Leste** 🇹🇱.")

st.title(":green[Lkwiz-YT] — Watch. Ask. Quiz. 🐊", anchor=False)
st.write("""
Ever watched a YouTube video and wondered how well you understood its content? With **Lkwiz-YT**, you can challenge yourself and test your comprehension with engaging quizzes. Dive deeper by asking questions about the video's content, ensuring your inquiries are relevant. Join us for a fun, educational experience and see how much you really know!

**How does it work?** 🤔

1. Paste the YouTube video URL of your recently watched video.
2. Enter your [AI71 API Key](https://lablab.ai/t/ai71-platform-guide).

⚠️ Important: The video **must** have English captions for the tool to work.

Once you've input the details! Dive deep into questions crafted just for you, ensuring you've truly grasped the content of the video. Let's put your knowledge to the test!
""")

with st.form("user_input"):
    YOUTUBE_URL = st.text_input("Enter the YouTube video link:", value="https://www.youtube.com/watch?v=9MArp9H2YCM")
    AI71_API_KEY = st.text_input("Enter your AI71 API Key:", placeholder="ai71-api-XXXX", type='password')
    submitted = st.form_submit_button("Submit")

centered_text_1 = """
<div style="display: flex; justify-content: center; align-items: center; height: 50px;">
    <p>Select the button <b style="color: red;">OPEN CHAT PANEL</b> for Chat <b>or</b> <b style="color: green;">CREATE A QUIZ</b> for quiz.</p>
</div>
"""

if submitted or ('video_id' in st.session_state and st.session_state.video_id):
    if not YOUTUBE_URL:
        st.info("Please provide a valid YouTube video link.")
        st.stop()
    elif not AI71_API_KEY:
        st.info("Please fill out the AI71 API Key to proceed.")
        st.stop()

    with st.expander("🎬 Click Here To Watch The Video Again"):
        st.video(YOUTUBE_URL)

    if submitted:
        # Extract video ID and fetch transcript only if not done previously
        if 'video_transcription' not in st.session_state or not st.session_state.video_transcription:
            with st.spinner("Fetching video transcription..."):
                st.session_state.video_id = extract_video_id_from_url(YOUTUBE_URL)
                st.session_state.video_transcription = get_transcript_text(st.session_state.video_id)

    st.markdown(centered_text_1, unsafe_allow_html=True)
    empty_col1, col1, col2, empty_col2 = st.columns([1, 1, 1, 1])
    st.write("-----")
    with col1:
        if st.button("Open Chat Panel"):
            st.session_state.show_chat = True
            st.session_state.quiz_started = False

    with col2:
        if st.button("Create a Quiz"):
            st.session_state.show_chat = False
            st.session_state.quiz_started = True
            create_quiz(st.session_state.video_transcription, AI71_API_KEY)

if st.session_state.show_chat:
    display_chat(AI71_API_KEY)  # Pass the AI71_API_KEY here

if st.session_state.quiz_started:
    display_quiz()

display_quiz_results()