import streamlit as st
import plotly.graph_objects as go

def display_lotteries(A1, A2, p, B1, B2, q):
    st.title("Lottery Comparison")
    st.markdown(
        f"Consider the following two lotteries:\n\n"
        f"Lottery A pays **£{A1}** with probability **{p}** and **£{A2}** with probability **{1 - p}**.\n\n"
        f"Lottery B pays **£{B1}** with probability **{q}** and **£{B2}** with probability **{1 - q}**."
    )

    # Labels & values for Lottery A
    labels_A = [f"£{A1} with", f"£{A2} with"]
    values_A = [p, 1 - p]

    # Labels & values for Lottery B
    labels_B = [f"£{B1} with", f"£{B2} with"]
    values_B = [q, 1 - q]

    # Create pie charts for lotteries
    fig_A = go.Figure(data=[go.Pie(labels=labels_A, values=values_A, hole=0, hoverinfo="none", textinfo="label+percent", textfont=dict(size=18))])
    fig_B = go.Figure(data=[go.Pie(labels=labels_B, values=values_B, hole=0, hoverinfo="none", textinfo="label+percent", textfont=dict(size=18))])

    # Remove legend
    fig_A.update_layout(showlegend=False)
    fig_B.update_layout(showlegend=False)

    # Display lotteries in two columns
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("<h3 style='text-align: center;'>Lottery A</h3>", unsafe_allow_html=True)
        st.plotly_chart(fig_A, use_container_width=True, config={"displayModeBar": False})

    with col2:
        st.markdown("<h3 style='text-align: center;'>Lottery B</h3>", unsafe_allow_html=True)
        st.plotly_chart(fig_B, use_container_width=True, config={"displayModeBar": False})

    # Initialize session state variables
    if "lottery_choice" not in st.session_state:
        st.session_state["lottery_choice"] = None
    if "multiple_choice" not in st.session_state:
        st.session_state["multiple_choice"] = []
    if "free_text_reason" not in st.session_state:
        st.session_state["free_text_reason"] = ""
    if "ask_reason" not in st.session_state:
        st.session_state["ask_reason"] = False
    if "page" not in st.session_state:
        st.session_state["page"] = 0

    # Lottery selection
    if st.session_state["lottery_choice"] is None:
        st.write("Which lottery do you prefer?")
        choice = st.radio("", ["Lottery A", "Lottery B"], index=None)

        if st.button("Submit Choice", key="submit_choice"):
            if choice is not None:
                st.session_state["lottery_choice"] = choice
                st.rerun()
            else:
                st.warning("Please select a lottery before submitting.")
    else:
        st.success(f"You selected: {st.session_state['lottery_choice']}")

    # Multiple-choice question after selecting a lottery
    if st.session_state["lottery_choice"]:
        st.write("### When comparing choices and deciding on an action, which of the following factors do you consider most important? (Select up to 2)")
        options = [
            "How likely the outcome is to happen.",
            "How much you value the outcome.",
            "How familiar or comfortable you are with the choice.",
            "How risky the choice feels, regardless of the actual probability of success."
        ]

        selected_options = []
        for option in options:
            if st.checkbox(option, key=f"checkbox_{option}", value=option in st.session_state["multiple_choice"]):
                selected_options.append(option)

        # Submit multiple-choice selection
        if st.button("Submit Explanation", key="submit_explanation"):
            if 1 <= len(selected_options) <= 2:
                st.session_state["multiple_choice"] = selected_options
                st.success(f"You selected: {', '.join(st.session_state['multiple_choice'])}")

                # Check if both first two options were selected
                first_two_selected = all(opt in selected_options for opt in options[:2])

                if first_two_selected:
                    st.session_state["page"] += 1  # Move forward
                    st.rerun()
                else:
                    st.session_state["ask_reason"] = True  # Show text input if needed
                    st.rerun()
            else:
                st.warning("⚠️ Please select at least 1 and at most 2 factors before submitting.")

        # Show free-text input only if at least one of the first two options is NOT selected
        if st.session_state["ask_reason"]:
            st.write("### Please explain why 'how likely the outcome is to happen' or 'how much you value the outcome' were not selected.")

            # JavaScript to auto-scroll when text input appears
            st.components.v1.html(
                """
                <script>
                    window.scrollTo({top: document.body.scrollHeight, behavior: 'smooth'});
                </script>
                """,
                height=0
            )

            free_text_input = st.text_area(
                "Provide your reason:",
                value=st.session_state.get("free_text_reason", ""),
                key="free_text_input"
            )

            # Submit free-text explanation
            if st.button("Submit Reason", key="submit_reason"):
                if free_text_input.strip():
                    st.session_state["free_text_reason"] = free_text_input
                    st.session_state["page"] += 1  # Move forward
                    st.session_state["ask_reason"] = False  # Hide text box on next load
                    st.rerun()
                else:
                    st.warning("⚠️ Please provide a reason before submitting.")

