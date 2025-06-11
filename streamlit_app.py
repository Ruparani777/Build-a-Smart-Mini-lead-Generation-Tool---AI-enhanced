import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder
import base64

st.set_page_config(
    page_title="Smart AI Lead Generator",
    layout="wide",
    page_icon="🚀"
)

st.markdown(
    "<h1 style='text-align: center; color: white;'>🤖 Build a Smart Mini Lead Generation Tool</h1>",
    unsafe_allow_html=True
)

st.markdown("---")

# Sidebar Instructions
with st.sidebar:
    st.header("📂 Upload Scored Leads CSV")
    uploaded_file = st.file_uploader("Upload your scored_leads_100.csv", type=["csv"])
    st.markdown("**Minimum AI Score Filter**")

    min_score = st.slider("Minimum AI Score", 1, 10, 5)
    st.markdown("---")
    st.markdown("Made with ❤️ by Ruparani")

# Load and filter data
if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file)
        if 'ai_score' not in df.columns:
            st.error("❌ 'ai_score' column not found in the uploaded file.")
        else:
            st.success("✅ File uploaded and loaded successfully!")

            filtered_df = df[df["ai_score"] >= min_score]

            st.subheader(f"🔎 Showing {len(filtered_df)} leads with AI score ≥ {min_score}")
            st.caption("Use the slider to filter high-quality leads based on their AI readiness score.")

            # Display using AgGrid
            gb = GridOptionsBuilder.from_dataframe(filtered_df)
            gb.configure_pagination(enabled=True)
            gb.configure_side_bar()
            gb.configure_default_column(groupable=True, value=True, enableRowGroup=True, editable=False)
            gridOptions = gb.build()

            AgGrid(filtered_df, gridOptions=gridOptions, theme='streamlit', height=400, fit_columns_on_grid_load=True)

            # Download filtered leads
            csv = filtered_df.to_csv(index=False)
            b64 = base64.b64encode(csv.encode()).decode()
            href = f'<a href="data:file/csv;base64,{b64}" download="filtered_leads.csv">📥 Download Filtered Leads CSV</a>'
            st.markdown(href, unsafe_allow_html=True)

    except Exception as e:
        st.error(f"⚠️ Error loading file: {e}")
else:
    st.info("👈 Upload your scored_leads_100.csv file to get started.")
    
