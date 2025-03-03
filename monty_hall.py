import streamlit as st
import matplotlib.pyplot as plt

def draw_question_marked_rectangle(ax):
    """Draws a rectangle with a centered question mark."""
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.add_patch(plt.Rectangle((0.1, 0.1), 0.8, 0.8, fill=False, edgecolor="black", linewidth=2))
    ax.text(0.5, 0.5, "?", fontsize=30, ha="center", va="center", fontweight="bold")
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_frame_on(False)

def three_doors():
    """Displays three rectangles with dropdowns underneath each."""
    st.write("Suppose you're on a game show, and you're given the choice of three doors:\n\n"
             "Behind one door is a car; behind the others, goats. "
             "What is the probability the car is behind door 1, 2, or 3?")

    # Ensure session state variables exist
    if "submitted_choices" not in st.session_state:
        st.session_state["submitted_choices"] = False
    if "submitted_explanation" not in st.session_state:
        st.session_state["submitted_explanation"] = False

    # Create three columns for side-by-side layout
    col1, col2, col3 = st.columns(3)

    # Draw the rectangles with question marks
    fig1, ax1 = plt.subplots(figsize=(2, 2))
    draw_question_marked_rectangle(ax1)
    col1.pyplot(fig1)

    fig2, ax2 = plt.subplots(figsize=(2, 2))
    draw_question_marked_rectangle(ax2)
    col2.pyplot(fig2)

    fig3, ax3 = plt.subplots(figsize=(2, 2))
    draw_question_marked_rectangle(ax3)
    col3.pyplot(fig3)

    # Dropdown options
    choices = ["", "0", "1/2", "1/3", "Cannot be determined"]

    # Create dropdowns below each rectangle
    choice1 = col1.selectbox("Door 1", choices, key="dropdown1")
    choice2 = col2.selectbox("Door 2", choices, key="dropdown2")
    choice3 = col3.selectbox("Door 3", choices, key="dropdown3")

    # Button to check answers
    if st.button("Submit Choices", key="submit_choices") and not st.session_state["submitted_choices"]:
        if choice1 == "1/3" and choice2 == "1/3" and choice3 == "1/3":
            st.session_state["page"] += 1
            st.rerun()
        else:
            st.session_state["submitted_choices"] = True
            st.rerun()

    # Show follow-up question only if incorrect answers were provided
    if st.session_state["submitted_choices"]:
        st.write("### Would you agree with the following statement?")
        st.write("'Given that my only knowledge is that there is one car behind one of the three doors, "
                 "I believe the car is equally likely to be behind any door, i.e., the probability is 1/3 for any door.'")

        # Dropdown menu with Yes/No
        agree_choice = st.selectbox("Select your answer:", ["", "Yes, Probably yes", "No, Probably no"], key="agree_dropdown")

        # Submit button for the explanation
        if st.button("Submit", key="submit_explanation") and not st.session_state["submitted_explanation"]:
            if agree_choice:
                st.session_state["submitted_explanation"] = True
                st.session_state["page"] += 1
                st.rerun()
            else:
                st.warning("⚠️ Please provide an answer before submitting.")

# Call the function to display the new page
if "page" not in st.session_state:
    st.session_state["page"] = 0


