import streamlit as st
import json
import os
from datetime import datetime

if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'user_data' not in st.session_state:
    st.session_state.user_data = {}

v_int = 75
v_str = "Assessment"
v_float = 1.0
v_list = ["Posture", "Study", "Comfort"]
v_tuple = (0, 5)
v_range = range(0, 20)
v_bool = True
v_dict = {"Status": "Active"}
v_set = {1, 2, 3}
v_frozenset = frozenset([0, 100])

def load_survey_data(file_path):
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            return json.load(f)
    return []

def get_interpretation(score):
    if score <= 20:
        return "Excellent Posture awareness & High Comfort: Exemplary, vigilant, disciplined, comfortable, effortless, sustainable"
    elif 21 <= score <= 40:
        return "Good Habits & Occasional Stretching: Solid, consistent, reliable, stable, comfortable, manageable."
    elif 41 <= score <= 60:
        return "Fair Awareness & Improvement of the Workstation Setup: Fair, developing, transitional, noticeable, strained, inconsistent"
    elif 61 <= score <= 80:
        return "Moderate Discomfort & Need for Ergonomic Adjustments: Troubled, strained, problematic, painful, fatigued, disruptive"
    else:
        return "High Discomfort & Urgent Posture Workshop: Critical, severe, alarming, chronic, debilitating, unsustainable"

if not st.session_state.authenticated:
    st.title("User Login")
    st.subheader("Please enter your details to unlock the survey")
    
    in_name = st.text_input("First Name")
    in_surname = st.text_input("Surname")
    in_dob = st.text_input("Date of Birth (YYYY-MM-DD)")
    in_id = st.text_input("ID (5 digits)")

    if st.button("Start the Survey"):
        valid_login = True
        
        if not in_name.isalpha():
            st.error("Invalid Name: Please use letters only.")
            valid_login = False
        if not in_surname.isalpha():
            st.error("Invalid Surname: Please use letters only.")
            valid_login = False
        try:
            datetime.strptime(in_dob, '%Y-%m-%d')
        except ValueError:
            st.error("Invalid Date: Please use YYYY-MM-DD format.")
            valid_login = False
        if not (in_id.isdigit() and len(in_id) == 5):
            st.error("Invalid ID: Must be exactly 5 digits.")
            valid_login = False
            
        if valid_login:
            st.session_state.authenticated = True
            st.session_state.user_data = {
                "name": in_name,
                "surname": in_surname,
                "dob": in_dob,
                "id": in_id
            }
            st.rerun()

if st.session_state.authenticated:
    st.title("Program Evaluation Survey")
    st.write(f"User: {st.session_state.user_data['name']} {st.session_state.user_data['surname']} | ID: {st.session_state.user_data['id']}")

    questions = load_survey_data('questions.json')

    if not questions:
        st.error("Error: questions.json not found!")
    else:
        options_map = {
            "Never / Strongly Disagree (0)": 0,
            "Rarely / Disagree (1)": 1,
            "Sometimes / Neutral (2)": 2,
            "Often / Agree (3)": 3,
            "Very Often / Strongly Agree (4)": 4,
            "Always / Completely Agree (5)": 5
        }
        
        responses = []
        
        u_name = st.session_state.user_data['name']
        u_surname = st.session_state.user_data['surname']
        u_dob = st.session_state.user_data['dob']
        u_id = st.session_state.user_data['id']

        with st.form("survey_form"):
            st.write("Confirm your details above and complete the questions below.")
            
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

                output_dict = {
                    "user_info": {
                        "name": u_name,
                        "surname": u_surname,
                        "dob": u_dob,
                        "id": u_id
                    },
                    "total_score": total_score, 
                    "interpretation": result_text
                }
                json_string = json.dumps(output_dict, indent=2)
                
                with open("results.json", "w") as f:
                    f.write(json_string)
                
                st.download_button(
                    label="Download Results as JSON",
                    data=json_string,
                    file_name=f"results_{u_id}.json",
                    mime="application/json"
                )
    
    if st.button("Logout"):
        st.session_state.authenticated = False
        st.rerun()
