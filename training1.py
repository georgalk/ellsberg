import streamlit as st
import plotly.graph_objects as go
import time
def training1():
    # Ensure session state exists for responses and text input
    if "selected_answer" not in st.session_state:
        st.session_state["selected_answer"] = ""

    if "free_text_reason" not in st.session_state:
        st.session_state["free_text_reason"] = ""

    if "show_free_text" not in st.session_state:
        st.session_state["show_free_text"] = False  # Controls visibility of free-text box


    # Function to create the 3x3 figure
    def create_figure(red_indices, total_balls=9):
        """Creates a 3x3 (or smaller) box with colored balls at certain positions."""
        fig = go.Figure()

        # Draw the outer box (3x3 grid)
        fig.add_shape(
            type="rect",
            x0=0, y0=0,
            x1=3, y1=3,
            line=dict(color="black", width=5)
        )

        # Positions for up to 9 balls (3 across x, 3 across y)
        ball_positions = [(x, y) for x in [0.5, 1.5, 2.5] for y in [0.5, 1.5, 2.5]][:total_balls]

        # Decide ball color (red vs gray) by index
        ball_colors = ["red" if i in red_indices else "lightgray" for i in range(len(ball_positions))]

        # Add scatter traces for each ball
        for (x, y), color in zip(ball_positions, ball_colors):
            fig.add_trace(
                go.Scatter(
                    x=[x],
                    y=[y],
                    mode="markers+text",
                    marker=dict(size=60, color=color),
                    text="?" if color == "lightgray" else "",
                    textfont=dict(size=30, color="black"),
                    textposition="middle center",
                    hoverinfo="skip",
                    showlegend=False
                )
            )

        fig.update_layout(
            xaxis=dict(range=[-0.2, 3.2], zeroline=False, showgrid=False, showticklabels=False),
            yaxis=dict(range=[-0.2, 3.2], zeroline=False, showgrid=False, showticklabels=False),
            height=300,
            width=300,
            plot_bgcolor="white",
            margin=dict(l=0, r=0, t=10, b=10),
            hovermode=False
        )

        return fig


    # UI Elements
    st.header("Question Training 1")
    st.markdown("""
    Continuing from the box example, given that the outcomes for all bets are exactly the same, your choice is based solely on the probability of each event occurring. 
    
    Obviously, given that we know that there are 3 red balls in the urn, the probability of drawing a red ball is 3/9 (or 1/3). What do you believe is the probability of drawing a black ball?
    """)

    col1, col2 = st.columns(2)

    with col1:
        st.plotly_chart(
            create_figure([0, 3, 6], total_balls=9),
            config={"displayModeBar": False, "staticPlot": True}
        )

    with col2:
        st.write("### The two options:")
        st.write("Win £10 if the ball is 🔴 Red, otherwise £0")
        st.write("Win £10 if the ball is ⚫ Black, otherwise £0")

        # Dropdown options
        choices = ["", "Lower than 3/9", "Equal to 3/9", "Higher than 3/9", "Cannot be determined"]

        # Selectbox for user's answer
        selected_answer = st.selectbox(
            "What do you believe is the probability of drawing a ⚫ Black ball?",
            choices,
            index=choices.index(st.session_state["selected_answer"]) if st.session_state[
                                                                            "selected_answer"] in choices else 0
        )

        # Button to validate answer
        if st.button("Submit"):
            if selected_answer and selected_answer != "":
                st.session_state["selected_answer"] = selected_answer  # Store selection

                if selected_answer != "Equal to 3/9":
                    st.session_state["show_free_text"] = True  # Show free-text input if wrong answer
                else:
                    st.session_state["show_free_text"] = False  # Hide if correct
                    st.session_state["page"] += 1

                st.rerun()  # Refresh UI to update changes
            else:
                st.warning("⚠️ Please select an option before submitting.")

    # Show free-text input **only if the answer is NOT "Equal to 3/9"**
    if st.session_state["show_free_text"]:
        st.write(
            f"###  Why do you think the probability of drawing a black ball is '{st.session_state['selected_answer']}' given that the only information you have is that the number of black balls is between 0 and 6?")

        # Ensure the session state variable exists before using it
        if "free_text_reason" not in st.session_state:
            st.session_state["free_text_reason"] = ""

        # Text area for explanation
        free_text_input = st.text_area(
            "Please provide your reasoning:",
            value=st.session_state["free_text_reason"],  # ✅ Maintain session state
            key="free_text_reason_input"  # ✅ Change the key to avoid conflict
        )

        # Submit explanation button
        if st.button("Submit Explanation"):
            if free_text_input.strip():  # ✅ Ensure user provided input
                st.session_state["free_text_reason"] = free_text_input  # ✅ Save response
                st.session_state["page"] += 1
                st.rerun()
            else:
                st.warning("⚠️ Please provide an explanation before submitting.")