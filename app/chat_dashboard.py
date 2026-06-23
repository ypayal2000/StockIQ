import sys
from pathlib import Path

project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

import streamlit as st

from src.agents.stock_graph import graph
from src.upload.upload_service import UploadService

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
# Upload Annual Report
# ---------------------------------

upload_service = UploadService()

st.subheader("📄 Upload Annual Report")

selected_symbol = st.selectbox(
    "Select Company",
    [
        "TCS.NS",
        "INFY.NS",
        "RELIANCE.NS",
        "ITC.NS",
        "HDFCBANK.NS",
        "HINDUNILVR.NS"
    ]
)

uploaded_file = st.file_uploader(
    "Choose PDF",
    type=["pdf"]
)

if st.button("Upload Report"):

    if uploaded_file is not None:
        result = upload_service.upload_document(uploaded_file, selected_symbol)
        

        if result["status"] == "uploaded":
            st.success(f"Uploaded Successfully: {result['key']}")
        else:
            st.warning(f"Document already exists: {result['key']}")

    else:
        st.warning("Please select a PDF file.")

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
            response = result["response"]

            # ------------------------
            # Investment Recommendation
            # ------------------------

            if "recommendation" in response:

                answer = f"""
                # 📈 Investment Recommendation
                **Stock:** {response["symbol"]}
                {response["recommendation"]}
                """

            # ------------------------
            # News Response
            # ------------------------

            elif "summary" in response:

                answer = f"""
                # 📰 News Analysis
                **Stock:** {response["symbol"]}
                {response["summary"]}
                ### Sentiment Score
                {response["sentiment_score"]}
                """

            # ------------------------
            # Prediction Response
            # ------------------------

            elif "probability_up" in response:

                answer = f"""
                # 📊 Prediction
                **Stock:** {response["symbol"]}
                **Prediction:** {response["prediction"]}
                **Probability Up:** {response["probability_up"]:.2%}
                **Probability Down:** {response["probability_down"]:.2%}
                **Confidence:** {response["confidence"]:.2%}
                """

            # ------------------------
            # Analysis Response
            # ------------------------

            else:

                answer = f"""
                # 📋 Company Analysis

                **Stock:** {response["symbol"]}
                **Prediction:** {response["prediction"]}
                **Confidence:** {response["confidence"]}%
                **Risk Level:** {response["risk_level"]}
                **Sentiment:** {response["sentiment"]}
                ## Growth Drivers

                """ + "\n".join([f"- {item}" for item in response["growth_drivers"]])

                answer += "\n\n## Risks\n\n"
                answer += "\n".join([f"- {item}" for item in response["risks"]])

                answer += "\n\n## Outlook\n\n"
                answer += "\n".join([f"- {item}" for item in response["outlook"]])

            st.markdown(answer)

    st.session_state.messages.append({"role": "assistant", "content": answer})