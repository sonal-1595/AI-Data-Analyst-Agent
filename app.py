import streamlit as st
import pandas as pd
import plotly.express as px
import requests
from fpdf import FPDF

st.set_page_config(page_title="AI Data Dashboard", layout="wide")

# -----------------------------
# PDF Generator
# -----------------------------
def create_pdf(text):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=10)
    clean_text = text.encode('latin-1', 'replace').decode('latin-1')
    pdf.multi_cell(0, 10, txt=clean_text)
    return pdf.output(dest='S').encode('latin-1')

# -----------------------------
# HEADER
# -----------------------------
st.title("🚀 AI Advanced Data Analyst")

# -----------------------------
# SIDEBAR
# -----------------------------
with st.sidebar:
    st.header("⚙️ Settings")
    api_key = st.text_input("OpenAI API Key", type="password")
    backend_url = st.text_input("Backend URL", value="http://localhost:8000/analyze")

# -----------------------------
# FILE UPLOAD
# -----------------------------
uploaded_files = st.file_uploader(
    "📂 Upload CSV / Excel Files",
    type=['csv', 'xlsx'],
    accept_multiple_files=True
)

all_dfs = []

# -----------------------------
# LOAD FILE FUNCTION (FIXED)
# -----------------------------
def load_file(file):
    
    skip = 0
    if "Inventory" in file.name or "Call-Center" in file.name:
        skip = 6

    if file.name.endswith('.csv'):
        df = pd.read_csv(file, skiprows=skip)
    else:
        df = pd.read_excel(file, skiprows=skip)

    df = df.dropna(how='all')
    df.columns = [str(c).replace('\n', ' ').strip() for c in df.columns]
    df = df.loc[:, ~df.columns.str.contains('Unnamed|nan|^$')]

    return df

# -----------------------------
# SMART CHART SUGGESTION
# -----------------------------
def suggest_chart(df):
    num_cols = df.select_dtypes(include=['number']).columns
    cat_cols = df.select_dtypes(include=['object']).columns
    if len(num_cols) >= 2: return "Scatter"
    elif len(cat_cols) >= 1: return "Bar"
    else: return "Histogram"

# -----------------------------
# PROCESS FILES
# -----------------------------
if uploaded_files:
    for file in uploaded_files:
        try:
            df = load_file(file)
            all_dfs.append(df)

            st.subheader(f"📄 {file.name}")

            with st.expander("👀 Preview Data"):
                st.dataframe(df.head())

            col1, col2 = st.columns(2)
            col1.metric("Rows", df.shape[0])
            col2.metric("Columns", df.shape[1])

            num_cols = df.select_dtypes(include=['number']).columns

            if len(num_cols) > 0:
                st.markdown("### 📊 KPI Overview")
                k1, k2, k3 = st.columns(3)
                k1.metric("Mean", round(df[num_cols[0]].mean(), 2))
                k2.metric("Max", round(df[num_cols[0]].max(), 2))
                k3.metric("Min", round(df[num_cols[0]].min(), 2))

            st.markdown("### 📈 Visualization")
            default_chart = suggest_chart(df)
            chart_options = ["Bar", "Line", "Scatter", "Histogram", "Box"]

            chart_type = st.selectbox(
                f"📊 Select Chart Type ({file.name})",
                chart_options,
                index=chart_options.index(default_chart) if default_chart in chart_options else 0
            )

            x_col = st.selectbox(f"X-axis ({file.name})", df.columns)
            y_col = st.selectbox(f"Y-axis ({file.name})", num_cols if len(num_cols)>0 else df.columns)

            if chart_type == "Bar": fig = px.bar(df, x=x_col, y=y_col)
            elif chart_type == "Line": fig = px.line(df, x=x_col, y=y_col)
            elif chart_type == "Scatter": fig = px.scatter(df, x=x_col, y=y_col)
            elif chart_type == "Histogram": fig = px.histogram(df, x=y_col)
            elif chart_type == "Box": fig = px.box(df, y=y_col)

            st.plotly_chart(fig, use_container_width=True)
            st.divider()

        except Exception as e:
            st.error(f"Error in {file.name}: {e}")

# -----------------------------
# AI QUERY
# -----------------------------
st.subheader("💬 Ask AI")
query = st.text_input("Ask anything about your data")

if st.button("Analyze Data"):
    if not api_key:
        st.warning("Enter API Key")
    elif not uploaded_files:
        st.warning("Upload files first")
    else:
        with st.spinner("🤖 AI analyzing..."):
            files_payload = []
            for f in uploaded_files:
                f.seek(0)
                files_payload.append(("files", (f.name, f.read())))

            res = requests.post(
                backend_url,
                files=files_payload,
                data={"query": query, "api_key": api_key}
            )

            data = res.json()
            if data.get("status") == "success":
                answer = data["answer"]
                st.markdown("### 📊 AI Report")
                st.markdown(answer)
                col1, col2 = st.columns(2)
                col1.download_button("📥 PDF", create_pdf(answer), "report.pdf")
                col2.download_button("📥 TXT", answer, "report.txt")
            else:
                st.error(data.get("error"))