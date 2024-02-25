import streamlit as st
import json

st.set_page_config(page_title="Synthesify")

from model import get_output


def load_templates():
    try:
        with open("templates.json", "r") as f:
            templates = json.load(f)
    except FileNotFoundError:
        templates = {}
    return templates


def save_templates(templates):
    with open("templates.json", "w") as f:
        json.dump(templates, f)


def generate_prompt(num_mcq, num_3_marks, num_5_marks, difficulty_level, subject, topics=None):
    
    prompt = f"Generate a Question Paper of {subject} having "
    
    if num_mcq > 0:
        prompt += f'{num_mcq} MCQs with weightage of 1 mark each, '
    if num_3_marks > 0:
        prompt += f'{num_3_marks} Questions with weightage of 3 marks each, '
    if num_5_marks > 0:
        prompt += f'{num_5_marks} Questions with weightage of 5 marks each. '

    prompt += f'Difficulty level should be {difficulty_level}. '
    if topics is not None:
        prompt += f'Pick questions only from following topics: {topics}'

    return prompt


def main():
    st.title("Question Paper Generator")

    # Load templates
    templates = load_templates()
    selected_template = st.selectbox("Select Template", ["Custom"] + list(templates.keys()), index=0)
    select_difficulty = ["Easy", "Medium", "Hard"]
    subjects = {
        'Data Structures and Algorithms': ['Data Strucutre', 'Searching & Sorting', 'Tree Traversal'],
        'Operating Systems': ['Scheduling', 'Memory Management', 'Process & Threads'],
        'Database Management System': ['Transaction & Concurrency Control', 'Normalization', 'File Organization']
    }
    
    subject = st.selectbox('Subjects', list(subjects.keys()))

    if selected_template == "Custom":
        # Sidebar options for custom template
        st.header("Question Type")  # Making the title smaller

        option = st.selectbox('Option', ['Full-syllabus', 'Topic-wise'])
        if option == 'Topic-wise':
            topics = st.multiselect(f'Select Topics for {subject}', subjects[subject])

        question_types = {
            "MCQ": st.checkbox("MCQ"),
            "Descriptive": st.checkbox("Descriptive")}
        if question_types["MCQ"]:
                num_mcq = st.slider("Number of MCQ", min_value=0, max_value=20, value=0)
        else:   
                num_mcq = 0
        num_3_marks = st.slider("Number of 3-marks Questions", min_value=0, max_value=20, value=0)
        num_5_marks = st.slider("Number of 5-marks Questions", min_value=0, max_value=20, value=0)
        total_marks = num_mcq + (num_3_marks * 3) + (num_5_marks * 5)
        st.text(f"Total Marks {total_marks}")
        selected_option = st.selectbox('Difficulty level', select_difficulty)

        # Validate if at least one checkbox is checked for question type
        if not any(question_types.values()):
            st.error("Please select at least one question type.")
            return
      
    else:
        template = templates[selected_template]
        question_types = template["question_types"]
        num_mcq = template["num_mcq"]
        num_3_marks = template["num_3_marks"]
        num_5_marks = template["num_5_marks"]
        total_marks = template["total_marks"]
        selected_option = template["selected_option"]
        option = 'Full-syllabus'
    
    if st.button("Generate Question Paper"):
        topics = None if option is None or option == 'Full-syllabus' else topics
        question = generate_prompt(num_mcq, num_3_marks, num_5_marks, selected_option, subject, topics)
        output = get_output(question)
        st.text(output)


if __name__ == "__main__":
    main()
