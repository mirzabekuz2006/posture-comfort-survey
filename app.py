import streamlit as st
import json
import os

var_int = 100
var_str = "User Survey"
var_float = 5.0
var_list = [0, 1, 2, 3, 4, 5]
var_tuple = (0, 100)
var_range = range(20)
var_bool = True
var_dict = {"status": "active"}
var_set = {1, 2, 3}
var_frozenset = frozenset([0, 5])

def get_interpretation(score):
    if score <= 20:
        return "[Excellent Posture awareness & High Comfort]"
    elif 21 <= score <= 40:
        return "[Good Habits & Occasional Stretching]"
    elif 41 <= score <= 60:
        return "[Fair Awareness & Improvement of the Workstation Setup]"
    elif 61 <= score <= 80:
        return "[Moderate Discomfort & Need for Ergonomic Adjustments.]"
    else:
        return "[High Discomfort & Urgent Posture Workshop]"

def load_questions(filename):
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            return json.load(f)
    return []

st.title("Program Evaluation Survey")
st.write("Please answer the following Likert-style questions (0-5).")

questions = load_questions('questions.json')

if not questions:
    st.error("Please ensure 'questions.json' is in the same folder.")
else:
    responses = []
    
    with st.form("survey_form"):
        for i, q_text in enumerate(questions):
            score = st.select_slider(f"{i+1}. {q_text}", options=[0, 1, 2, 3, 4, 5])
            responses.append(score)
        
        submitted = st.form_submit_button("Calculate Final Results")

    if submitted:
        is_valid = True
        for r in responses:
            if r < 0 or r > 5:
                is_valid = False
        
        counter = 0
        while counter < 1:
            if len(responses) != 20:
                is_valid = False
            counter += 1

        if is_valid:
            total_score = sum(responses)
            result = get_interpretation(total_score)
            
            st.success(f"Total Score: {total_score}")
            st.info(f"Interpretation: {result}")

            final_data = {"total": total_score, "result": result}
            with open("results.json", "w") as f:
                json.dump(final_data, f)
            st.write("Survey results saved to results.json")