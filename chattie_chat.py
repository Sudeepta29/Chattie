import openai
import pdfplumber
import streamlit as st
import difflib

open_ai_key = st.secrets["open_ai_key"]
# Set the API key directly on the openai module
openai.api_key = open_ai_key

# Assign the openai module to a client instance for consistency
client_instance = openai
pdf_path = "Training_Chattie_responses.pdf"

# Function to extract text from PDF
def extract_text_from_pdf(pdf_path):
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page_num, page in enumerate(pdf.pages, start=1):
            page_text = page.extract_text()
            if page_text:
                text += f"--- Page {page_num} ---\n{page_text}\n"
            else:
                text += f"--- Page {page_num} ---\n[No text found]\n"
    return text

# Function to check if a line is a question
def is_question(line):
    question_words = ["what", "how", "why", "when", "who", "where", "is", "are", "can", "should", "do", "does", "if"]
    return line.strip().lower().split()[0] in question_words if line.strip() else False

# Function to extract 10-15 lines after finding a partial match in the PDF
def extract_relevant_text(user_input, pdf_text, lines_to_extract=15):
    user_input_lower = user_input.lower()
    pdf_text_lines = pdf_text.splitlines()

    # Find the best partial match using difflib
    best_match = difflib.get_close_matches(user_input_lower, pdf_text_lines, n=1, cutoff=0.7)  # Adjust cutoff for partial match sensitivity

    if best_match:
        # Find the index of the best match in the pdf_text_lines
        idx = pdf_text_lines.index(best_match[0])
        # Extract the next 10-15 lines after the match
        start_idx = idx + 1
        extracted_text = []
        for i in range(start_idx, len(pdf_text_lines)):
            current_line = pdf_text_lines[i].strip()
            if current_line == "" or is_question(current_line):  # Stop at blank line or next question
                break
            extracted_text.append(current_line)
            if len(extracted_text) >= lines_to_extract:
                break
        return "\n".join(extracted_text) if extracted_text else "No answer found."

    return None  # Return None if no partial match is found

# Function to get a response from OpenAI if PDF search fails
def get_chattie_response(user_input, system_prompt, client_instance):
    # Base system prompt
    system_prompt = (
         f"The user is named {st.session_state.context.get('address', 'there')}, is in the age range {st.session_state.context.get('age_range', 'unknown')}, "
        f"and has a professional background in {st.session_state.context.get('background', 'an unspecified field')}."
    )
   # Refined prompt logic based on user's intentions
    background = st.session_state.context.get('background')
    looking_to_start = st.session_state.context.get('looking_to_start')
    risk_tolerance = st.session_state.context.get('risk_tolerance')
    
     if background == "Working for a startup or small company" and looking_to_start == "Yes":
        if risk_tolerance in ["Low", "Medium"]:
            interest_type = st.session_state.context.get('interest_type', 'angel investing or a side hustle')
            system_prompt += (
                f" They have a low to medium risk tolerance and are interested in exploring {interest_type} as a way to start up without full commitment."
            )
        elif risk_tolerance == "High":
            startup_area = st.session_state.context.get('startup_area', 'an unspecified area')
            startup_phase = st.session_state.context.get('startup_phase', 'an unspecified phase')
            system_prompt += (
                f" They are highly interested in starting up with a high risk tolerance, focusing on {startup_area} and currently in the {startup_phase} phase."
            )

    elif background == "Working for a mid or large size company" and looking_to_start == "Yes":
        if risk_tolerance in ["Low", "Medium"]:
            interest_type = st.session_state.context.get('interest_type', 'angel investing or a side hustle')
            system_prompt += (
                f" They have a low to medium risk tolerance and are interested in exploring {interest_type} before a full startup commitment."
            )
        elif risk_tolerance == "High":
            startup_area = st.session_state.context.get('startup_area', 'an unspecified area')
            startup_phase = st.session_state.context.get('startup_phase', 'an unspecified phase')
            system_prompt += (
                f" With a high risk tolerance, they are focused on starting up in {startup_area} and are in the {startup_phase} phase."
            )

    elif background == "Tinkering with ideas or on a break/exploration phase":
        tinkering_idea = st.session_state.context.get('tinkering_idea', 'an unspecified concept')
        startup_phase = st.session_state.context.get('startup_phase', 'an unspecified phase')
        system_prompt += (
            f" They are exploring ideas with an interest in {tinkering_idea}, currently in the {startup_phase} phase of development."
        )
    try:
        response = client_instance.chat.completions.create(
            model="gpt-4",  # You can use "gpt-3.5-turbo" if required
            messages=[
                {"role": "system", "content": system_prompt},  # Provide user context
                {"role": "user", "content": user_input},       # The user's query
            ]
        )
        return response.choices[0].message.content
        
    except Exception as e:  # Correct error handling
        # Catch OpenAI-specific errors and display a detailed message
        print(f"OpenAI Error: {str(e)}")
        return f"Error: {e}"
        
# Main Chat Section
def chat_with_chattie(pdf_text):
    
    user_input = st.text_input("Ask Chattie here..")
    col1, col2, col3 = st.columns(3)

    with col1:
        send_button_clicked = st.button("Send", key="send_button")
    with col2:
        continue_button_clicked = st.button("Continue", key="continue_button")
    with col3:
        reset_button_clicked = st.button("Reset Chat", key="reset_button")

    if send_button_clicked and user_input:
        st.session_state.chat_history.append({"user": user_input})

        # First, search the PDF for a response
        pdf_response = extract_relevant_text(user_input, pdf_text)
        if pdf_response:
            # If a PDF response is found, use it and **do not** call OpenAI
            response = pdf_response
        else:
            # Pass the user context (st.session_state.context) to get a personalized response from OpenAI
            response = get_chattie_response(user_input, st.session_state.context, client_instance)

        st.session_state.chat_history.append({"chattie": response})


    # Display chat history
    for chat in st.session_state.chat_history:
        if "user" in chat:
            st.markdown(f"**You:** {chat['user']}")
        if "chattie" in chat:
            st.markdown(f"**Chattie:** {chat['chattie']}")

    # Reset session
    if reset_button_clicked:
        st.session_state.chat_history = []
        st.session_state.user_input = ""
