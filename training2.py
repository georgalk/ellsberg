import streamlit as st
import plotly.graph_objects as go
import time


def training2():
    # UI Elements

    st.header("Question Training 2")
    st.markdown("""
     On the one hand, you know that the probability of drawing a red ball is 3/9, whereas on the other you have some hypothesis about the probability of drawing a black ball. 
     
     Assuming for a moment that your hypothesis about the probability of drawing a black ball is also 3/9. 
     
     Would you consider the 3/9 probability of drawing a red ball (which you know) to be more reliable than the same 3/9 probability for a black ball (which you assume), given that you’re less certain about the latter probability? In other words, do you feel a bit more uncertain about “black” than “red”, and is this uncertainty why you’re less willing to bet on “black”?
    """)

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
    col1, col2 = st.columns(2)

    with col1:
        st.plotly_chart(
            create_figure([0, 3, 6], total_balls=9),
            config={"displayModeBar": False, "staticPlot": True}
        )

    with col2:

        if "agree_choice" not in st.session_state:
            st.session_state["agree_choice"] = ""
        # Selectbox for user's answer
        agree_choice = st.selectbox("Select your answer:", ["","Yes, Probably yes", "No, Probably no"], key="agree_dropdown")
        # Submit button for the explanation
        if st.button("Submit"):
            if agree_choice and agree_choice != "":
                st.session_state["agree_choice"] = agree_choice # Store selection
                st.session_state["page"] += 1
                st.rerun()  # Refresh UI to update changes
            else:
                st.warning("⚠️ Please select an option before submitting.")
