import streamlit as st
from query_class import extract_intent_entity_field_groq
from api_call import get_users_by_search_query
from extract_data import extract_fields
from reponse import generate_natural_response

# Hardcoded token and companyID (replace 'your_token_here' with actual token)
token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbiI6eyJ1c2VybWFzdGVyaWQiOjMyOTMsInVzZXJUeXBlIjoiMCJ9LCJpYXQiOjE3NDc2MzM3NjMsImV4cCI6MTc0NzcyMDE2M30.VaiqLrGlzjMORYomZ3BQP6STl7cQhb2Y9HenoE_XX1A'
companyID = 68

# Initialize session state
if 'history' not in st.session_state:
    st.session_state.history = []
if 'selected_user' not in st.session_state:
    st.session_state.selected_user = None
if 'employees_to_select' not in st.session_state:
    st.session_state.employees_to_select = None
if 'pending_query' not in st.session_state:
    st.session_state.pending_query = None

# App title and instructions
st.title("HR Assistant")
st.write("Ask questions about employees, such as 'What is Ajay's email?' or 'When did he join?'")

# Display conversation history
for message in st.session_state.history:
    with st.chat_message(message['role']):
        st.write(message['content'])

# Chat input for user queries
query = st.chat_input("Enter your query:")

if query:
    st.session_state.history.append({'role': 'user', 'content': query})
    intent, entity, field = extract_intent_entity_field_groq(query)
    if entity is not None:
        api_res = get_users_by_search_query(token, companyID, intent, entity)
        if api_res and api_res.get('data'):
            employees = api_res['data']
            if len(employees) == 1:
                st.session_state.selected_user = employees[0]
                result = extract_fields({'data': employees}, field)
                response = generate_natural_response(intent, entity, result)
                st.session_state.history.append({'role': 'assistant', 'content': response})
            else:
                st.session_state.employees_to_select = employees
                st.session_state.pending_query = query
                response = "There are multiple employees with that name. Please select one from the options below."
                st.session_state.history.append({'role': 'assistant', 'content': response})
        else:
            response = "No employees found with that name."
            st.session_state.history.append({'role': 'assistant', 'content': response})
    else:
        if st.session_state.selected_user is not None:
            result = extract_fields({'data': [st.session_state.selected_user]}, field)
            employee_name = st.session_state.selected_user['displayName']
            response = generate_natural_response(intent, employee_name, result)
            st.session_state.history.append({'role': 'assistant', 'content': response})
        else:
            response = "Please specify an employee name."
            st.session_state.history.append({'role': 'assistant', 'content': response})

# Display employee selection if multiple employees are found
if st.session_state.employees_to_select:
    options = [f"{user['displayName']} (ID: {user['userMasterID']})" for user in st.session_state.employees_to_select]
    selected_option = st.selectbox("Select an employee", options)
    if st.button("Confirm Selection"):
        index = options.index(selected_option)
        st.session_state.selected_user = st.session_state.employees_to_select[index]
        st.session_state.employees_to_select = None
        # Generate response for the pending query
        pending_query = st.session_state.pending_query
        intent, entity, field = extract_intent_entity_field_groq(pending_query)
        result = extract_fields({'data': [st.session_state.selected_user]}, field)
        employee_name = st.session_state.selected_user['displayName']
        response = generate_natural_response(intent, employee_name, result)
        st.session_state.history.append({'role': 'assistant', 'content': response})
        st.session_state.pending_query = None

# Button to start a new query and clear session
if st.button("Start new query"):
    st.session_state.selected_user = None
    st.session_state.employees_to_select = None
    st.session_state.history = []
    st.session_state.pending_query = None