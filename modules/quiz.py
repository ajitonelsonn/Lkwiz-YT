import streamlit as st
from agents.agent_quiz import get_quiz_data
from helpers.quiz_utils import get_randomized_options

def create_quiz(video_transcription, AI71_API_KEY):
    with st.spinner("Crafting your quiz...🤓"):
        quiz_data = get_quiz_data(video_transcription, AI71_API_KEY)
        if quiz_data:
            st.session_state.quiz_data_list = quiz_data
            st.session_state.user_answers = [None] * len(quiz_data)
            st.session_state.correct_answers = []
            st.session_state.randomized_options = []
            for q in quiz_data:
                options, correct_answer = get_randomized_options(q[1:])
                st.session_state.randomized_options.append(options)
                st.session_state.correct_answers.append(correct_answer)
        else:
            st.error("Please try again.👩‍🎤")
            st.session_state.quiz_started = False

def display_quiz():
    st.subheader("👨‍🎤 Quiz Time: Test Your Knowledge!", anchor=False)
    with st.form(key='quiz_form'):
        for i, q in enumerate(st.session_state.quiz_data_list):
            options = st.session_state.randomized_options[i]
            default_index = options.index(st.session_state.user_answers[i]) if st.session_state.user_answers[i] is not None else 0
            response = st.radio(q[0], options, index=default_index, key=f"q{i}")
            st.session_state.user_answers[i] = response  

        results_submitted = st.form_submit_button(label='Unveil My Score!')

        if results_submitted:
            st.session_state.score_submitted = True

def display_quiz_results(AI71_API_KEY):
    if st.session_state.score_submitted:
        score = sum([ua == ca for ua, ca in zip(st.session_state.user_answers, st.session_state.correct_answers)])
        st.success(f"Your score: {score}/{len(st.session_state.quiz_data_list)}")

        if score == len(st.session_state.quiz_data_list): 
            st.balloons()
        else:
            incorrect_count = len(st.session_state.quiz_data_list) - score
            if incorrect_count == 1:
                st.warning("Almost perfect! You got 1 question wrong. Let's review it:")
            else:
                st.warning("Almost there! You got {} questions wrong. Let's review them:".format(incorrect_count))

        for i, (ua, ca, q, ro) in enumerate(zip(st.session_state.user_answers, st.session_state.correct_answers, st.session_state.quiz_data_list, st.session_state.randomized_options)):
            with st.expander("Question {}".format(i + 1), expanded=False):
                if ua != ca:
                    st.info("Question: {}".format(q[0]))
                    st.error("Your answer: {}".format(ua))
                    st.success("Correct answer: {}".format(ca))