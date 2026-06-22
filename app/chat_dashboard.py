import sys
from pathlib import Path

project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

import streamlit as st

from src.agents.stock_graph import graph


# ---------------------------------
# Page Config
# ---------------------------------

st.set_page_config(
    page_title="StockIQ",
    page_icon="📈",
    layout="wide"
)

# ---------------------------------
# Header
# ---------------------------------

st.title("📈 StockIQ")
st.subheader("AI Quantitative Stock Intelligence Platform")

st.markdown(
    """
    ### Example Questions

    - What is the latest Infosys news?
    - Should I buy TCS for long term investment?
    - Predict Reliance stock performance.
    - What are the key risks in HDFC Bank?
    - What are the growth drivers of Infosys?
"""
)

st.divider()

# ---------------------------------
# Chat History
# ---------------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ---------------------------------
# User Input
# ---------------------------------

query = st.chat_input("Ask StockIQ...")

if query:

    st.session_state.messages.append({"role": "user", "content": query})

    with st.chat_message("user"):
        st.markdown(query)

    with st.chat_message("assistant"):
        with st.spinner("Analyzing..."):
            result = graph.invoke({"user_query": query})

            route = result["agents"]
            symbol = result["symbol"]
            response = result["response"]

            # -------------------------
            # NEWS RESPONSE
            # -------------------------

            if route == "news":
                answer = f"""
                ### 📰 News Analysis
                **Stock:** {symbol}
                {response["summary"]}
            **Sentiment Score:** {response["sentiment_score"]}
            """     

            # -------------------------
            # PREDICTION RESPONSE
            # -------------------------

            elif route == "prediction":
                answer = f""" ### 📊 Prediction
                **Stock:** {symbol}
                **Prediction:** {response["prediction"]}
                **Probability Up:** {response["probability_up"]:.2%}
                **Probability Down:** {response["probability_down"]:.2%}
                **Confidence:** {response["confidence"]:.2%}
                """

            # -------------------------
            # ANALYSIS RESPONSE
            # -------------------------

            else:
                answer = f"""### 📈 Stock Analysis
            **Stock:** {symbol}
            **Prediction:** {response["prediction"]}
            **Confidence:** {response["confidence"]}%
            **Sentiment:** {response["sentiment"]}
            ### Growth Drivers
            """ + "\n".join([f"- {item}"
                        for item in response["growth_drivers"]
                    ]
                )

                answer += "\n\n### Risks\n\n"
                answer += "\n".join([f"- {item}" for item in response["risks"]])

                answer += "\n\n### Outlook\n\n"
                answer += "\n".join( [f"- {item}" for item in response["outlook"]])

            st.markdown(answer)

    st.session_state.messages.append({"role": "assistant", "content": answer})