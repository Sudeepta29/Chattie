
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
    # Step 1: Ask for the user's name
    if st.session_state.step == 0:
        st.session_state.context['address'] = st.text_input("How would you like to be addressed by Chattie?", key="user_address")
        
        # Display Next button only if name is provided
        if st.session_state.context['address']:
            if st.button("Next", key="next_0"):
                st.session_state.step += 1
            
    # Step 2: Ask for the user's age range
    elif st.session_state.step == 1:
        st.session_state.context['age_range'] = st.selectbox("Your age range:", ["20-30", "31-40", "41-50", "Above 50"], key="age_range")
        if st.button("Next", key="next_1"):
            st.session_state.step += 1

    # Step 3: Ask for professional background
    elif st.session_state.step == 2:
        st.session_state.context['background'] = st.selectbox(
            "What's your current professional background?", 
            ["Working for a startup or small company", "Working for a mid or large size company", "Tinkering with ideas or on a break/exploration phase"],
            key="professional_background"
        )
        if st.button("Next", key="next_2"):
            st.session_state.step += 1

    # Step 4: Follow-up questions based on professional background
    elif st.session_state.step == 3:
        background = st.session_state.context.get('background', None)
        
        if background in ["Working for a startup or small company", "Working for a mid or large size company"]:
            st.session_state.context['looking_to_start'] = st.selectbox(
                "Are you looking to start up?",
                ["Yes", "No"],
                key="looking_to_start"
            )

            if st.session_state.context['looking_to_start'] == "Yes":
                risk_tolerance_options = {
                    "Low": "Prefers minimal risk, low investment.",
                    "Medium": "Willing to take some risks, can invest time and resources.",
                    "High": "Comfortable with high risk, willing to invest heavily."
                }
                st.session_state.context['risk_tolerance'] = st.selectbox(
                    "What's your risk tolerance in starting up?",
                    options=list(risk_tolerance_options.keys()),
                    format_func=lambda x: f"{x}: {risk_tolerance_options[x]}",
                    key=f"risk_tolerance_{st.session_state.step}"
                )
                 # Actions based on risk tolerance level
                if st.session_state.context['risk_tolerance'] in ["Low", "Medium"]:
                    st.write("Since you have indicated your risk tolerance as low/medium, you might benefit from learning about angel investing or exploring an idea on the side before committing fully.")
                    if st.button("Start chatting with Chattie"):
                        st.session_state.step += 1

                elif st.session_state.context['risk_tolerance'] == "High":
                    st.write("Since you have indicated that you are willing to take a high risk, which area are you keen on starting up?")
                    startup_area = st.text_input("Please type in the area you are interested in:", key="startup_area")
                    
                    if startup_area:
                        st.session_state.context['startup_area'] = startup_area
                        startup_phase = st.selectbox(
                            "Which phase of starting up are you in?", 
                            ["Have a solid idea", "Have an MVP", "Setting up a company", "Looking for co-founders"],
                            key="startup_phase"
                        )
                        st.session_state.context['startup_phase'] = startup_phase

                        st.session_state.context['summary'] = (
                            f"Hey {st.session_state.context['address']}, you mentioned that you're working in a {background} and are keen on starting up "
                            f"with a high risk tolerance. You are interested in the area of {startup_area} and are currently in the {startup_phase} phase."
                        )
                        if st.button("Display Summary"):
                            st.session_state.step += 1

            else:
                st.session_state.context['reason'] = st.text_input("What brings you here?", key="reason")
                st.session_state.context['summary'] = f"Hey {st.session_state.context['address']}, you mentioned that you're here because: {st.session_state.context['reason']}."
                if st.button("Display Summary"):
                    st.session_state.step += 1

        elif background == "Tinkering with ideas or on a break/exploration phase":
            st.write("What are you thinking about? Do you have an idea or specific area you'd like to work upon?")
            tinkering_idea = st.text_input("Please describe your idea or concept:", key="tinkering_idea")
            st.session_state.context['tinkering_idea'] = tinkering_idea
            st.session_state.context['summary'] = f"You're exploring ideas and described your concept as: {tinkering_idea}."
            
            if st.button("Display Summary"):
                st.session_state.step += 1

# Chat function
def chat_with_chattie(pdf_text):
    user_input = st.text_input("Ask Chattie here...")
    if st.button("Send"):
        st.session_state.chat_history.append({"user": user_input})
        pdf_response = extract_text_from_pdf(pdf_text)
        if pdf_response:
            response = pdf_response
        else:
            system_prompt = st.session_state.context['summary']
            response = get_chattie_response(user_input, system_prompt)
        st.session_state.chat_history.append({"chattie": response})

    for chat in st.session_state.chat_history:
        if "user" in chat:
            st.markdown(f"**You:** {chat['user']}")
        if "chattie" in chat:
            st.markdown(f"**Chattie:** {chat['chattie']}")

# Display initial context questions or chat
if st.session_state.step < 5:
    user_context_questions()
elif st.session_state.step >= 5:
    chat_with_chattie(pdf_text)
