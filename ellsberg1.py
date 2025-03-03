import streamlit as st
import plotly.graph_objects as go
import time

# Time delay for transitions
time_sleep = 1

# Define different scenarios with unique questions and options
scenarios = [
    {"red_indices": [0, 3, 6],
     "question": "Which one do you prefer?", "options": [
        "Win £10 if the ball is 🔴 Red, otherwise £0",
        "Win £10 if the ball is ⚫ Black, otherwise £0"
    ]},
    {"red_indices": [0, 3, 6],
     "question": "Which one do you prefer?", "options": [
        "Win £10 if the ball is 🔴 Red OR ⚫ Black, otherwise £0",
        "Win £10 if the ball is ⚫ Black OR 🟡 Yellow, otherwise £0"
    ]}
]


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


def ellsberg_task():
    """Encapsulates the ellsberg experiment to be called from `main.py`"""

    # Initialize session state for tracking progress within the task
    if "ellsberg_stage" not in st.session_state:
        st.session_state["ellsberg_stage"] = 0  # 0 = First option, 1 = Second option
        st.session_state["ellsberg_responses"] = []  # Stores user choices

    scenario = scenarios[st.session_state["ellsberg_stage"]]

    st.header(f"Question {st.session_state['ellsberg_stage'] + 1}")
    st.markdown("""
    Consider a box with 9 balls. Three of them are red, and the remaining six are either yellow or black in unknown proportions. 
    Since you don’t know how many are yellow or black, they’re shown in the figure as gray. 

    The computer will simulate a draw of a ball from this box, and you are asked to bet on the color of this ball. 
    """)

    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(
            create_figure(scenario["red_indices"], total_balls=9),
            config={"displayModeBar": False, "staticPlot": True}
        )

    with col2:
        st.write("Which option do you prefer?")
        choice = st.radio(
            "",
            scenario["options"],
            index=None,
            key=f"ellsberg_choice_{st.session_state['ellsberg_stage']}"
        )

    # Show only one button at a time
    if st.button("Submit"):
        if choice is not None:
            st.session_state["ellsberg_responses"].append(
                {"scenario": st.session_state["ellsberg_stage"], "choice": choice})
            with st.spinner("Loading next question..."):
                time.sleep(time_sleep)

            # Move to next stage or return to main app
            if st.session_state["ellsberg_stage"] == 0:
                st.session_state["ellsberg_stage"] = 1  # Move to second option
            else:
                st.session_state["page"] += 1  # Move to next page in main app

            st.rerun()
        else:
            st.warning("Please select an option before submitting.")
