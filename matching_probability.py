import streamlit as st
import pandas as pd

def matching_probability(optionA, optionB, probability_strings, probability_floats):
    """
    Displays a risk preference elicitation task where users choose between two lotteries.
    The function now takes in two lists: one with formatted probability strings and another with float values.
    """

    # Ensure both lists have the same length
    if len(probability_strings) != len(probability_floats):
        st.error("Error: Probability string and float lists must be the same length!")
        return

    lottery_A = [optionA] * len(probability_strings)
    lottery_B = ["£" f"{optionB} with probability {p_str}" for p_str in probability_strings]


    st.subheader("Which option do you prefer?")

    if 'choices' not in st.session_state:
        st.session_state.choices = [None] * len(probability_strings)

    df = pd.DataFrame({
        "Probability (p)": probability_strings,  # Display formatted probability
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
        c_A_text, c_A_check,  c_B_check, c_B_text = st.columns([ 3, 1,1, 3])

        #c_p.write(df.loc[i, "Probability (p)"])  # Display formatted probability

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
        results = [f"p={df.loc[i, 'Probability (p)']}: {('No choice made' if choice is None else choice)}"
                   for i, choice in enumerate(st.session_state['choices'])]

        st.write("Results:")
        st.write(", ".join(results))
        count_A = sum(1 for choice in st.session_state['choices'] if choice == 'A')
        count_B = sum(1 for choice in st.session_state['choices'] if choice == 'B')
        st.write(f"Total 'A' choices: {count_A}")
        st.write(f"Total 'B' choices: {count_B}")

        if None not in st.session_state.choices:  # If all choices are made
            st.session_state["page"] += 1
        else:
            st.error("Please make a selection for all choices before proceeding.")

# Example Usage:
# probability_strings = ["1 out of 9", "2 out of 9", "3 out of 9", "4 out of 9", "5 out of 9"]
# probability_floats = [1/9, 2/9, 3/9, 4/9, 5/9]
# matching_probability("Win £10 if black", "Win £10", probability_strings, probability_floats)
