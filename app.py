
import streamlit as st
from chattie_chat import chat_with_chattie, extract_text_from_pdf


# Inject custom CSS to reduce the title font size
st.markdown(
    """
   <style>
    .custom-title {
        font-size: 30px;  /* Adjust the font size as needed */
        font-weight: bold;
        color: #1F618D !important;  /* Change this hex code to the desired color */
        text-align: center;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Display the title
st.markdown(
    '<h1 class="custom-title">Chattie: Your guide to all things startup & entrepreneurship</h1>',
    unsafe_allow_html=True
)


# Add custom CSS to center the image
st.markdown(
    """
    <style>
    .centered-image {
        display: block;
        margin-left: auto;
        margin-right: auto;
    }
    </style>
    """,
    unsafe_allow_html=True
)
# Display the image using st.image() wrapped in a div for centering
st.markdown('<div class="centered">', unsafe_allow_html=True)
st.image("Chattie image.png", width=70)  # Adjust the path and width as needed
st.markdown('</div>', unsafe_allow_html=True)


# Inject custom CSS to style buttons
st.markdown(
    """
    <style>
    div.stButton > button {
        font-size: 8px !important;  /* Adjust the font size as needed */
        padding: 5px 7px !important;  /* Adjust padding for the button */
    }
    </style>
    """,
    unsafe_allow_html=True
)

pdf_path = "Training_Chattie_responses.pdf"

pdf_text = extract_text_from_pdf(pdf_path)

# Initialize session state to store user inputs and step counter
if 'context' not in st.session_state:
    st.session_state.context = {}
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'step' not in st.session_state:
    st.session_state.step = 0  # Start with the first question

# Step-by-step questions

st.markdown(
    """
    <h3 style="text-align: left; color: #1F618D; font-size:20px;">
        Whether you are thinking of starting up OR generally wondering about nuances of entrepreneurship/startup space, Chattie can guide!
    </h3>
    """, 
    unsafe_allow_html=True
)

def user_context_questions():
    if st.session_state.step == 0:
        # Step 1: Ask the user's preferred name
        st.session_state.context['address'] = st.text_input("How would you like to be addressed by Chattie?", key="user_address")
        if st.button("Next", key="next_1"):
            if st.session_state.context['address']:
                st.session_state.step += 1

    elif st.session_state.step == 1:
        # Step 2: Ask the user's age range
        st.session_state.context['age_range'] = st.selectbox("Your age range:", ["20-30", "31-40", "41-50", "Above 50"], key="age_range")
        if st.button("Next", key="next_2"):
            st.session_state.step += 1

    elif st.session_state.step == 2:
        # Step 3: Ask the user's professional background
        st.session_state.context['background'] = st.selectbox(
            "What's your current professional background?", 
            ["Working for a startup or small company", "Working for a mid or large size company", "Tinkering with ideas or on a break/exploration phase"],
            key="professional_background"
        )
        if st.button("Next", key="next_3"):
            st.session_state.step += 1

    elif st.session_state.step == 3:
        # Step 4: Follow-up questions based on user background
        background = st.session_state.context['background']
        
        if background == "Working for a startup or small company" or background == "Working for a mid or large size company":
            # Logic for users working in a company based on size
            st.session_state.context['looking_to_start'] = st.selectbox(
                "Are you looking to start up?",
                ["Yes", "No"],
                key="looking_to_start"
            )

            if st.session_state.context.get('looking_to_start') == "Yes":
                # Define risk tolerance levels with descriptions
                risk_tolerance_options = {
                    "Low": "Prefers minimal risk, low investment, not willing to spend too much time or resources.",
                    "Medium": "Willing to take some risks, can invest time, money, and resources.",
                    "High": "Comfortable with high risk, willing to invest heavily and explore it full time."
                }

                st.session_state.context['risk_tolerance'] = st.selectbox(
                    "What's your risk tolerance in starting up?",
                    options=list(risk_tolerance_options.keys()),
                    format_func=lambda x: f"{x}: {risk_tolerance_options[x]}",
                    key=f"risk_tolerance_{st.session_state.step}"
                )

                # Follow-up based on risk tolerance level
                if st.session_state.context['risk_tolerance'] in ["Low", "Medium"]:
                    st.write("Since you have indicated your risk tolerance as low/medium, would you like to know more about aspects such as angel investing or exploring an idea on the side before plunging into starting up full time?")
                
                elif st.session_state.context['risk_tolerance'] == "High":
                    st.write("Since you have indicated a high risk tolerance, which area are you keen on starting up?")
                    startup_area = st.text_input("Please type in the area you are interested in:")
                    
                    if startup_area:
                        st.session_state.context['startup_area'] = startup_area
                        startup_phase = st.selectbox(
                            "Which phase of starting up are you in?", 
                            ["Have a solid idea", "Have an MVP", "Setting up a company", "Looking for co-founders"]
                        )
                        st.session_state.context['startup_phase'] = startup_phase

            elif st.session_state.context.get('looking_to_start') == "No":
                st.session_state.context['reason'] = st.text_input("What brings you here?", key="reason_1")

        elif background == "Tinkering with ideas or on a break/exploration phase":
            st.write("What are you thinking about? Do you have an idea or a concept or specific area you would like to work upon?")
            tinkering_idea = st.text_input("Please describe your idea or concept:")
            
            if tinkering_idea:
                st.session_state.context['tinkering_idea'] = tinkering_idea

        if st.button("Next", key="next_4"):
            st.session_state.step += 1

     # Final Step: Display summary before starting chat
    elif st.session_state.step == 4:
        address = st.session_state.context.get('address', 'there')
        age_range = st.session_state.context.get('age_range', 'unknown')
        background = st.session_state.context.get('background', 'unspecified')

        # Construct summary message
        summary_message = f"Hey {address}, you mentioned that you're in the age range {age_range} and your background is {background}."
        
        if background in ["Working for a startup or small company", "Working for a mid or large size company"]:
            looking_to_start = st.session_state.context.get('looking_to_start', 'unspecified')
            if looking_to_start == "Yes":
                risk_tolerance = st.session_state.context.get('risk_tolerance', 'unspecified')
                summary_message += f" You are looking to start up, with a risk tolerance of {risk_tolerance.lower()}."
            else:
                reason = st.session_state.context.get('reason', 'unspecified')
                summary_message += f" You're here because: {reason.lower()}."

        elif background == "Tinkering with ideas or on a break/exploration phase":
            tinkering_idea = st.session_state.context.get('tinkering_idea', 'an unspecified concept')
            summary_message += f" You're exploring ideas and described your concept as: {tinkering_idea}."

        # Display the summary
        st.markdown(summary_message)

        # Button to start chat
        if st.button("Start chatting with Chattie"):
            st.session_state.step += 1

col1, col2 = st.columns([1, 1])

# Display Next button in Column 1
with col1:
    if st.button("Next", key=f"next_{st.session_state.step}"):
        st.session_state.step += 1

# Display Back button in Column 2 (only if not on the first step)
with col2:
    if st.session_state.step > 0:
        if st.button("Back", key=f"back_{st.session_state.step}"):
            st.session_state.step -= 1
# Display the initial context questions if not completed
if st.session_state.step < 5:
    user_context_questions()

# Only show the main chat once the user context questions and summary are completed
if st.session_state.step >= 5:
    chat_with_chattie(pdf_text)        
          
