import streamlit as st
import json
import csv
import os
import io
from datetime import datetime

if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'user_data' not in st.session_state:
    st.session_state.user_data = {}
if 'survey_submitted' not in st.session_state:
    st.session_state.survey_submitted = False
if 'final_results' not in st.session_state:
    st.session_state.final_results = {}

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
        if file_path.endswith('.json'):
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

st.sidebar.title("Navigation")
app_mode = st.sidebar.radio("Choose Action", ["Start New Questionnaire", "Load Existing Results"])

if app_mode == "Load Existing Results":
    st.title("Load Previous Results")
    uploaded_file = st.file_uploader("Upload result file", type=['json', 'csv', 'txt'])
    if uploaded_file:
        if uploaded_file.name.endswith('.json'):
            st.json(json.load(uploaded_file))
        elif uploaded_file.name.endswith('.csv'):
            st.text(uploaded_file.read().decode("utf-8"))
        else:
            st.text(uploaded_file.read().decode("utf-8"))

elif app_mode == "Start New Questionnaire":
    if not st.session_state.authenticated:
        st.title("User Login")
        in_name = st.text_input("First Name")
        in_surname = st.text_input("Surname")
        in_dob = st.text_input("Date of Birth (YYYY-MM-DD)")
        in_id = st.text_input("ID (5 digits)")

        if st.button("Start the Survey"):
            valid_login = True
            if not in_name.isalpha() or not in_surname.isalpha():
                st.error("Invalid Name/Surname: Use letters only.")
                valid_login = False
            try:
                datetime.strptime(in_dob, '%Y-%m-%d')
            except:
                st.error("Invalid Date format.")
                valid_login = False
            if not (in_id.isdigit() and len(in_id) == 5):
                st.error("ID must be 5 digits.")
                valid_login = False
            
            if valid_login:
                st.session_state.authenticated = True
                st.session_state.user_data = {"name": in_name, "surname": in_surname, "dob": in_dob, "id": in_id}
                st.rerun()

    if st.session_state.authenticated:
        # Display Results at the top if they have already submitted
        if st.session_state.survey_submitted:
            st.success(f"Final Score: {st.session_state.final_results['total_score']}")
            st.info(f"Interpretation: {st.session_state.final_results['interpretation']}")
            
            # Download section remains visible at top after submission
            res = st.session_state.final_results
            st.download_button(
                label=f"Download {res['format']}",
                data=res['data_str'],
                file_name=f"results_{st.session_state.user_data['id']}.{res['ext']}",
                mime=res['mime']
            )
            if st.button("Take Survey Again"):
                st.session_state.survey_submitted = False
                st.rerun()
        else:
            st.title("Program Evaluation Survey")
            questions = load_survey_data('questions.json')

            if not questions:
                st.error("questions.json not found!")
            else:
                options_map = {
                    "Never (0)": 0, "Rarely (1)": 1, "Sometimes (2)": 2,
                    "Often (3)": 3, "Most of the time (4)": 4, "Always (5)": 5
                }
                responses = []
                with st.form("survey_form"):
                    for i, q_text in enumerate(questions):
                        choice = st.select_slider(f"{i+1}. {q_text}", options=list(options_map.keys()))
                        responses.append(options_map[choice])
                    
                    export_format = st.selectbox("Select Save Format", ["JSON", "CSV", "TXT"])
                    submitted = st.form_submit_button("Submit Results")

                if submitted:
                    if len(responses) == 20:
                        total_score = sum(responses)
                        result_text = get_interpretation(total_score)
                        
                        # Prepare data for download
                        u_info = st.session_state.user_data
                        if export_format == "JSON":
                            data_str = json.dumps({"user": u_info, "score": total_score, "result": result_text}, indent=2)
                            ext, mime = "json", "application/json"
                        elif export_format == "CSV":
                            si = io.StringIO()
                            cw = csv.writer(si); cw.writerow(["Name", "ID", "Score", "Result"])
                            cw.writerow([u_info['name'], u_info['id'], total_score, result_text])
                            data_str = si.getvalue(); ext, mime = "csv", "text/csv"
                        else:
                            data_str = f"Score: {total_score}\nResult: {result_text}"; ext, mime = "txt", "text/plain"

                        # Store in session state and flip the flag
                        st.session_state.final_results = {
                            "total_score": total_score,
                            "interpretation": result_text,
                            "data_str": data_str,
                            "ext": ext,
                            "mime": mime,
                            "format": export_format
                        }
                        st.session_state.survey_submitted = True
                        st.rerun()
                    else:
                        st.error("Please answer all questions.")

        if st.button("Logout"):
            st.session_state.authenticated = False
            st.session_state.survey_submitted = False
            st.rerun()
