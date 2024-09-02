import streamlit as st
import random
import json

WIPjson = open("psalmdict.json")
psalm_dict = json.load(WIPjson)

vocab_dict = json.load(open("vocab.json"))

st.set_page_config(layout="wide")

col1, col2, col3, col4= st.columns(4)

def get_question():

    verses = len(psalm_dict)
    random_verse = random.randint(1,verses)

    divisions = len(psalm_dict[str(random_verse)]['division'])
    random_division = random.randint(1,divisions)
    words = len(psalm_dict[str(random_verse)]['division'][str(random_division)]['word'])
    random_word = random.randint(1,words)
    question_word = psalm_dict[str(random_verse)]['division'][str(random_division)]['word'][str(random_word)]['text']
    question_division = psalm_dict[str(random_verse)]['division'][str(random_division)]['text']
    question = f'What is the general meaning of the word "{question_word}", as in "{question_division}"?'
    root = psalm_dict[str(random_verse)]['division'][str(random_division)]['word'][str(random_word)]['root']
    answer = vocab_dict[root]['meaning']


    if 'unacceptable answers' in psalm_dict[str(random_verse)]['division'][str(random_division)]['word'][str(random_word)]:
        unacceptable_answers = psalm_dict[str(random_verse)]['division'][str(random_division)]['word'][str(random_word)]['unacceptable answers']
    else:
        unacceptable_answers = []

    data = {
        'question': question,
        'correct_answer': answer,
        'acceptable_answers': vocab_dict[root]['acceptable answers'],
        'root': root,
        'unacceptable_answers': unacceptable_answers,
        'explanation': f'the correct answer is "{answer}"',
        'translations': psalm_dict[str(random_verse)]['division'][str(random_division)]['word'][str(random_word)]['translation'],
        'contexts': psalm_dict[str(random_verse)]['division'][str(random_division)]['translation'],
        'line': question_division,
        'derivative': vocab_dict[root]['derivatives'],
        'etymology': vocab_dict[root]['etymology']
    }
    return data

def initialize_session_state():
    session_state = st.session_state
    session_state.form_count = 0
    session_state.quiz_data = get_question()

if 'something' not in st.session_state:
    st.session_state.something = ''

def submit():
    st.session_state.something = st.session_state.widget
    st.session_state.widget = ''



def main():
    if 'form_count' not in st.session_state:
        initialize_session_state()
    if not st.session_state.quiz_data:
        st.session_state.quiz_data = get_question()

    quiz_data = st.session_state.quiz_data
    with col1:
        st.page_link("https://ko-fi.com/williamofdallas", label="Support this site & projects like it", icon="☕")
        st.title('Psalm 134')

        for verse in psalm_dict:
            psalm_line_count = 0
            for line in psalm_dict[verse]['division']:
                if psalm_line_count==0:
                    if psalm_dict[verse]['division'][line]['text'] == quiz_data['line']:
                        st.markdown(f"->***{psalm_dict[verse]['division'][line]['text']}***")
                    else:
                        st.markdown(f"{psalm_dict[verse]['division'][line]['text']}")
                else:
                    if psalm_dict[verse]['division'][line]['text'] == quiz_data['line']:
                        st.markdown(f"&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;->***{psalm_dict[verse]['division'][line]['text']}***")
                    else:
                        st.markdown(f"&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;{psalm_dict[verse]['division'][line]['text']}")
                psalm_line_count += 1

    with col2:
        st.markdown("")
        st.markdown("")
        st.markdown("")
        st.title('Quiz')
        st.markdown(f"{quiz_data['question']}")
        st.text_input('Answer', key='widget', on_change=submit)

        if st.session_state.something:
            st.write(f'Your answer: {st.session_state.something}')
            user_choice = st.session_state.something
            st.session_state.something = ''

            another_question = st.button("Another question")

            if user_choice.lower() == quiz_data['correct_answer'].lower() or user_choice.lower() in quiz_data['acceptable_answers']:
                st.success(f'Correct: "{quiz_data["correct_answer"]}"')

            else:
                st.error("Incorrect")
                for bad_guess in quiz_data['unacceptable_answers']:
                    if user_choice == bad_guess:
                        st.markdown(f'This is not a good answer. {quiz_data["unacceptable_answers"][bad_guess]} A better answer is really "{quiz_data["correct_answer"]}."')

            with col3:
                st.markdown("")
                st.markdown("")
                st.markdown("")

                st.title(quiz_data['root'].capitalize())
                answer_display = quiz_data['correct_answer'].capitalize()

                if quiz_data['acceptable_answers']:
                    for answer in quiz_data['acceptable_answers']:
                        answer_display = answer_display + ", " + answer
                st.markdown(answer_display)


                if quiz_data["etymology"]:
                    st.markdown('#### Etymology')
                    st.markdown(quiz_data['etymology'])
                if quiz_data["derivative"]:
                    st.markdown('#### Derivatives')
                    for derivative in quiz_data["derivative"]:
                        st.markdown(f'**{derivative}**: {quiz_data["derivative"][derivative]}')

            with col4:
                st.markdown("")
                st.markdown("")
                st.markdown("")
                st.title('Translations')

                for translation in quiz_data['translations']:
                    st.markdown(f'**{translation}**: *{quiz_data["translations"][translation]}*, as in "{dict(quiz_data["contexts"])[translation]}"')

            with st.spinner("Calling the model for the next question"):
                session_state = st.session_state
                session_state.quiz_data = get_question()

            if another_question:
                st.session_state.form_count += 1
            else:
                st.stop()

if __name__ == '__main__':
    main()
