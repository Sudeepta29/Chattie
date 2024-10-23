
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
        col1, col2 = st.columns([1, 1])
        with col2:  # 'Next' in the second column
            if st.button("Next", key="next_1"):
                if st.session_state.context['address']:
                    st.session_state.step += 1
        # No "Back" button for step 0 as it's the first step

    elif st.session_state.step == 1:
        # Step 2: Ask the user's age range
        st.session_state.context['age_range'] = st.selectbox("Your age range:", ["20-30", "31-40", "41-50", "Above 50"], key="age_range")
        col1, col2 = st.columns([1, 1])
        with col2:  # 'Back' in the second column
            if st.button("Back", key="back_1"):
                st.session_state.step -= 1
        with col1:  # 'Next' in the first column
            if st.button("Next", key="next_2"):
                st.session_state.step += 1

    elif st.session_state.step == 2:
        # Step 3: Ask the user's professional background
        st.session_state.context['background'] = st.selectbox(
            "What's your current professional background?", 
            ["Working for a startup or small company", "Working for a mid or large size company", "Running own startup or business", "Tinkering with ideas Or on a break/ exploration phase"],
            key="professional_background"
        )
        col1, col2 = st.columns([1, 1])
        with col2:  # 'Back' in the second column
            if st.button("Back", key="back_2"):
                st.session_state.step -= 1
        with col1:  # 'Next' in the first column
            if st.button("Next", key="next_3"):
                st.session_state.step += 1

    elif st.session_state.step == 3:
        # Step 4: Handle different paths based on user background and age range
        background = st.session_state.context['background']
        age_range = st.session_state.context['age_range']
        
        if background == "Running own startup or business":
            # Logic for startup founders (bootstrapped or funded)
            st.session_state.context['funding_status'] = st.selectbox("Is your startup bootstrapped or funded?", ["Bootstrapped", "Funded"], key="funding_status")
            
            if st.session_state.context['funding_status'] == "Funded":
                st.session_state.context['funded_advice'] = st.selectbox(
                    "What advice are you looking for from Chattie?",
                    ["Raising your next round", "Not achieved product market fit", "People challenges", "General"],
                    key="funded_advice"
                )
            else:
                st.session_state.context['advice'] = st.selectbox(
                    "What advice are you looking for from Chattie?",
                    ["Cashflow management", "How to raise funds", "Pitch decks", "People management"],
                    key="specific_advice"
                )

        elif background == "Working for a startup or small company" or background == "Working for a mid or large size company":
            # Logic for users working in a company based on size
            st.session_state.context['looking_to_start'] = st.selectbox(
                "Are you looking to start up?",
                ["Yes", "No"],
                key="looking_to_start"
            )

            if st.session_state.context.get('looking_to_start') == "Yes":
                # Define risk appetite levels with descriptions
                risk_tolerance_options = {
                    "Low": "Prefers minimal risk, low investment, not willing to spend too much time or resources.",
                    "Medium": "Willing to take some risks, can invest time, money, and resources.",
                    "High": "Comfortable with high risk, willing to invest heavily and explore it full time."
                }

                # Ensure the key for risk appetite is unique by appending the step number
                st.session_state.context['risk_tolerance'] = st.selectbox(
                    "What's your risk tolerance in starting up?",
                    options=list(risk_tolerance_options.keys()),
                    format_func=lambda x: f"{x}: {risk_tolerance_options[x]}",
                    key=f"risk_appetite_{st.session_state.step}"  # Unique key for the widget
                )

            elif st.session_state.context.get('looking_to_start') == "No":
                st.session_state.context['reason'] = st.text_input("What brings you here?", key="reason_1")
        
        elif background == "Tinkering with ideas Or on a break/ exploration phase":
            st.session_state.context['beginner_questions'] = st.selectbox(
                "Are you curious about:",
                ["How to get started", "Building a network", "Finding investors", "Learning from failure"],
                key="beginner_interests"
            )

        col1, col2 = st.columns([1, 1])
        with col2:  # 'Back' in the second column
            if st.button("Back", key="back_3"):
                st.session_state.step -= 1
        with col1:  # 'Next' in the first column
            if st.button("Next", key="next_4"):
                st.session_state.step += 1

    elif st.session_state.step == 4:
        # Final step: Confirm all information before starting the chat
        address = st.session_state.context.get('address', 'there')
        age_range = st.session_state.context.get('age_range', 'unknown')
        background = st.session_state.context.get('background', 'unspecified')

        summary_message = f"Hey {address}, you mentioned that you're currently {background}, in the age range {age_range}."

        if background == "Running own startup or business":
            funding_status = st.session_state.context.get('funding_status', 'unspecified')
            if funding_status == "Funded":
                funded_advice = st.session_state.context.get('funded_advice', 'general advice')
                summary_message += f" Your startup is funded, and you're seeking advice on {funded_advice.lower()}."
            else:
                advice = st.session_state.context.get('advice', 'general advice')
                summary_message += f" Your startup is bootstrapped, and you're seeking advice on {advice.lower()}."

        elif background == "Working for a startup or small company" or background == "Working for a mid or large size company":
            looking_to_start = st.session_state.context.get('looking_to_start', 'unspecified')
            if looking_to_start == "Yes":
                risk_appetite = st.session_state.context.get('risk_appetite', 'unspecified')
                summary_message += f" You are looking to start up, and your risk appetite is {risk_appetite.lower()}."
            else:
                reason = st.session_state.context.get('reason', 'unspecified')
                summary_message += f" You're not looking to start up, and you're here because: {reason.lower()}."

        elif background == "Tinkering with ideas Or on a break/ exploration phase":
            beginner_questions = st.session_state.context.get('beginner_questions', 'unspecified')
            summary_message += f" You're curious about {beginner_questions.lower()}."

        # Display the summary
        st.markdown(summary_message)

        col1, col2 = st.columns([1, 1])
        with col2:  # 'Back' in the second column
            if st.button("Back", key="back_4"):
                st.session_state.step -= 1
        with col1:  # 'Start Chatting' in the first column
            if st.button("Start chatting with Chattie"):
                st.session_state.step += 1

# Display the initial context questions if not completed
if st.session_state.step < 5:
    user_context_questions()

# Only show the main chat once the user context questions and summary are completed
if st.session_state.step >= 5:
    chat_with_chattie(pdf_text)        
          
