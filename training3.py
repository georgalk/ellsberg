import streamlit as st
import pandas as pd
import plotly.graph_objects as go


def create_figure(red_indices, total_balls=9):
    """Creates a 3x3 (or smaller) box with colored balls at certain positions."""
    fig = go.Figure()
    fig.add_shape(
        type="rect",
        x0=0, y0=0,
        x1=3, y1=3,
        line=dict(color="black", width=5)
    )

    ball_positions = [(x, y) for x in [0.5, 1.5, 2.5] for y in [0.5, 1.5, 2.5]][:total_balls]
    ball_colors = ["red" if i in red_indices else "lightgray" for i in range(len(ball_positions))]

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

def matching_probability(optionA, optionB, probability_strings, probability_floats):
    """
    Displays a risk preference elicitation task where users choose between two lotteries.
    """

    if len(probability_strings) != len(probability_floats):
        st.error("Error: Probability string and float lists must be the same length!")
        return

    lottery_A = [optionA] * len(probability_strings)
    lottery_B = [f"£{optionB} with probability {p_str}" for p_str in probability_strings]

    st.subheader("Which option do you prefer?")

    # ✅ Ensure `choices` is initialized with correct length
    if "choices" not in st.session_state or len(st.session_state["choices"]) != len(probability_strings):
        st.session_state["choices"] = [None] * len(probability_strings)

    df = pd.DataFrame({
        "Probability (p)": probability_strings,
        "Lottery A": lottery_A,
        "Lottery B": lottery_B
    })

    def enforce_monotonic(index, choice):
        """Enforces a single switch from A to B in the choice selection."""
        if choice == 'B':
            for i in range(len(st.session_state.choices)):
                st.session_state.choices[i] = 'B' if i >= index else 'A'
        else:
            st.session_state.choices[index] = 'A'
            for i in range(index):
                if st.session_state.choices[i] == 'B':
                    st.session_state.choices[i] = 'A'
            for i in range(index + 1, len(probability_strings)):
                if st.session_state.choices[i] == 'B':
                    st.session_state.choices[i] = None

    def on_select_A(index):
        enforce_monotonic(index, 'A')

    def on_select_B(index):
        enforce_monotonic(index, 'B')

    for i in range(len(df)):
        c_A_text, c_A_check, c_B_check, c_B_text = st.columns([3, 1, 1, 3])

        c_A_text.write(df.loc[i, 'Lottery A'])
        c_A_check.checkbox(
            "A",
            value=(st.session_state.choices[i] == 'A'),
            key=f"a_check_{i}",
            on_change=on_select_A,
            args=(i,)
        )

        c_B_text.write(df.loc[i, 'Lottery B'])
        c_B_check.checkbox(
            "B",
            value=(st.session_state.choices[i] == 'B'),
            key=f"b_check_{i}",
            on_change=on_select_B,
            args=(i,)
        )

    if st.button("Submit", key="submit_button"):
        if None not in st.session_state.choices:  # Ensure all selections are made
            if st.session_state["stage"] == 1:
                st.session_state["stage"] = 2  # Move to Stage 2 (Betting on Black)
                st.session_state["choices"] = [None] * len(probability_strings)  # Reset selections
                st.rerun()
            else:
                st.success("You have completed both betting rounds!")
                st.session_state["page"] += 1  # ✅ Move to the next page after both rounds
                st.rerun()  # ✅ Refresh the app to display the next page
        else:
            st.error("Please make a selection for all probabilities before proceeding.")

def training3():
    # Initialize session state variables
    if "stage" not in st.session_state:
        st.session_state["stage"] = 1  # Start at Stage 1 (betting on Red)
    if "choices" not in st.session_state or not isinstance(st.session_state["choices"], list):
        st.session_state["choices"] = []  # Ensure choices is an empty list

    st.header("Question Training 3")
    st.markdown("""
    Suppose now you are faced with a situation in which you have no information about the relative proportions of the three colors in the urn.

    In other words, you only know that there are 9 balls inside the urn with red, black, and yellow colors.

    You will be presented with three scenarios—hypotheses that specify different possible numbers of red balls in the urn, each of which can be either true or false. 
    For each scenario, what do you believe is the probability of drawing a red ball, P(R), and the probability of drawing a black ball, P(B)?
    """)

    st.subheader(f"Scenario 1: There are 3 Red balls and 6 Black and Yellow balls - Stage {st.session_state['stage']}")

    col1, col2 = st.columns(2)

    with col1:
        st.plotly_chart(
            create_figure([0, 3, 6], total_balls=9),
            config={"displayModeBar": False, "staticPlot": True}
        )

    with col2:
        color_bet = "Red" if st.session_state["stage"] == 1 else "Black"
        st.markdown(f"""
        With **Option A**, you win £10 if a **{color_bet}** ball is drawn from the urn, otherwise nothing.

        With **Option B**, you win £10 with some probability, otherwise nothing.  
        """)

    probability_strings = ["0 out of 9", "1 out of 9", "2 out of 9", "3 out of 9", "4 out of 9",
                           "5 out of 9", "6 out of 9", "7 out of 9", "8 out of 9", "9 out of 9"]
    probability_floats = [0, 1 / 9, 2 / 9, 3 / 9, 4 / 9, 5 / 9, 6 / 9, 7 / 9, 8 / 9, 9 / 9]

    optionA_label = "Red ball from the urn" if st.session_state["stage"] == 1 else "Black ball from the urn"

    # Run Matching Probability Function
    matching_probability(optionA_label, "20", probability_strings, probability_floats)


