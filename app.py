import streamlit as st
import pandas as pd
import json
from pipeline import financial_insight_pipeline

# ---------- PAGE CONFIG ----------
st.set_page_config(
    page_title="Financial Insight App",
    page_icon="📊",
    layout="wide"
)

# ---------- CUSTOM CSS ----------
st.markdown("""
<style>

/* ---- MAIN BACKGROUND ---- */
.stApp {
    background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
    color: white;
}

/* ---- CONTAINER SPACING ---- */
.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
}

/* ---- HEADINGS ---- */
h1, h2, h3 {
    color: #f1f5f9;
    font-weight: 600;
}

/* ---- CARD STYLE ---- */
.card {
    background: rgba(255, 255, 255, 0.08);
    border-radius: 14px;
    padding: 20px;
    margin-bottom: 20px;
    box-shadow: 0 8px 24px rgba(0,0,0,0.25);
}

/* ---- BUTTON ---- */
.stButton>button {
    background: linear-gradient(90deg, #00c6ff, #0072ff);
    color: white;
    border-radius: 10px;
    padding: 0.6rem 1.2rem;
    font-weight: 600;
    border: none;
}

.stButton>button:hover {
    transform: scale(1.03);
    transition: 0.2s ease-in-out;
}

/* ---- DATAFRAME ---- */
[data-testid="stDataFrame"] {
    background-color: rgba(255,255,255,0.95);
    border-radius: 10px;
}

/* ---- FILE UPLOADER ---- */
[data-testid="stFileUploader"] {
    background-color: rgba(255,255,255,0.08);
    border-radius: 10px;
    padding: 10px;
}

</style>
""", unsafe_allow_html=True)

# ---------- SESSION STATE ----------
if "output" not in st.session_state:
    st.session_state.output = None

# ---------- HEADER ----------
st.markdown("""
<div class="card">
<h1>📊 Financial Insight Extraction System</h1>
<p>Extract structured financial insights from long financial documents using NLP.</p>
</div>
""", unsafe_allow_html=True)

# ---------- UPLOAD ----------
st.markdown('<div class="card">', unsafe_allow_html=True)
st.subheader("📄 Upload Financial Document")

uploaded_file = st.file_uploader(
    "Upload a financial PDF (Annual Report / 10-K)",
    type=["pdf"]
)

st.markdown('</div>', unsafe_allow_html=True)

# ---------- RUN ----------
st.markdown('<div class="card">', unsafe_allow_html=True)
st.subheader("⚙️ Run Analysis")
run = st.button("🚀 Extract Financial Insights")
st.markdown('</div>', unsafe_allow_html=True)

if run and uploaded_file:
    with st.spinner("Analyzing document..."):
        st.session_state.output = financial_insight_pipeline(uploaded_file)

    st.success("✅ Extraction completed successfully!")

# ---------- OUTPUT ----------
if st.session_state.output:
    output = st.session_state.output

    # SUMMARY
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("📊 Insight Summary")

    total = len(output["metrics"])
    quant = sum(1 for m in output["metrics"] if m["type"] == "quantitative")
    qual = total - quant

    c1, c2, c3 = st.columns(3)
    c1.metric("Total Insights", total)
    c2.metric("Quantitative", quant)
    c3.metric("Qualitative", qual)

    st.markdown('</div>', unsafe_allow_html=True)

    # TABLE
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("📈 Extracted Financial Insights")

    df = pd.DataFrame(output["metrics"])

    filter_type = st.selectbox(
        "Filter by Insight Type",
        ["All", "quantitative", "qualitative"]
    )

    if filter_type != "All":
        df = df[df["type"] == filter_type]

    st.dataframe(df, use_container_width=True, height=400)
    st.markdown('</div>', unsafe_allow_html=True)

    # DOWNLOAD + JSON
    st.markdown('<div class="card">', unsafe_allow_html=True)

    st.download_button(
        "⬇ Download JSON Output",
        data=json.dumps(output, indent=2),
        file_name="financial_insights.json",
        mime="application/json"
    )

    with st.expander("🔍 View Raw JSON Output"):
        st.json(output)

    st.markdown('</div>', unsafe_allow_html=True)
