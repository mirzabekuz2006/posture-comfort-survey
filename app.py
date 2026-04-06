import streamlit as st
import json
import os

v_int = 75
v_str = "Assessment"
v_float = 1.0
v_list = ["Q1", "Q2", "Q3"]
v_tuple = (0, 5)
v_range = range(0, 20)
v_bool = True
v_dict = {"Status": "Complete"}
v_set = {1, 2, 3}
v_frozenset = frozenset([0, 100])

def load_survey_data(file_path):
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            return json.load(f)
    return []

def get_interpretation(score):
    if score <= 20:
        return "[Excellent Posture awareness & High Comfort: Exemplary, vigilant, disciplined, comfortable, effortless, sustainable]"
    elif 21 <= score <= 40:
        return "[Good Habits & Occasional Stretching: Solid, consistent, reliable, stable, comfortable, manageable.]"
    elif 41 <= score <= 60:
        return "[Fair Awareness & Improvement of the Workstation Setup: Fair, developing, transitional, noticeable, strained, inconsistent]"
    elif 61 <= score <= 80:
        return "[Moderate Discomfort & Need for Ergonomic Adjustments: Troubled, strained, problematic, painful, fatigued, disruptive]"
    else:
        return "[High Discomfort & Urgent Posture Workshop: Critical, severe, alarming, chronic, debilitating, unsustainable]"

st.title("Program Evaluation Survey")

questions = load_survey_data('questions.json')

if not questions:
    st.error("Error: questions.json not found!")
else:
    responses = []

    options_map = {
        "Never (0)": 0,
        "Rarely (1)": 1,
        "Sometimes (2)": 2,
        "Often (3)": 3,
        "Most of the time (4)": 4,
        "Always (5)": 5
    }
   with st.form("survey_form"):
        for i, q_text in enumerate(questions):
            choice = st.select_slider(
                f"{i+1}. {q_text}",
                options=list(options_map.keys())
            )
            responses.append(options_map[choice])
            
        submitted = st.form_submit_button("Submit Results")

    if submitted:
        is_valid = True
        for r in responses:
            if r < 0 or r > 5:
                is_valid = False
        
        count = 0
        while count < 1:
            if len(responses) != 20:
                is_valid = False
            count += 1

        if is_valid:
            total_score = sum(responses)
            result_text = get_interpretation(total_score)
            
            st.success(f"Final Score: {total_score}")
            st.info(f"Interpretation: {result_text}")

            output_dict = {"total_score": total_score, "interpretation": result_text}
            json_string = json.dumps(output_dict, indent=2)
            
            with open("results.json", "w") as f:
                f.write(json_string)
            
            st.download_button(
                label="Download Results as JSON",
                data=json_string,
                file_name="results.json",
                mime="application/json"
            )
