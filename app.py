import streamlit as st
import streamlit.components.v1 as components
from parser import get_triples
from visualize import draw_ann

st.set_page_config(layout="wide", page_title="Neuro-Notes Web")

# 1. Initialize Session State so we don't lose data on rerun
if 'width' not in st.session_state: 
    st.session_state.width = 1200
if 'processed_data' not in st.session_state:
    st.session_state.processed_data = None

st.sidebar.title("📐 Design Controls")
if st.sidebar.button("➕ Make Wider (Fix Graphics)"):
    st.session_state.width += 400
    st.rerun()

if st.sidebar.button("🔄 Reset App"):
    st.session_state.processed_data = None
    st.rerun()

st.title("🧠 Neuro-Notes: Public Knowledge Webpage")

# 2. File Uploader
file = st.file_uploader("Upload your Data Structures PDF", type="pdf")

if file:
    # Only process the PDF if we haven't already
    if st.session_state.processed_data is None:
        with st.spinner("Mapping 123 neurons..."):
            st.session_state.processed_data = get_triples(file)

# 3. Display Logic
if st.session_state.processed_data:
    try:
        html = draw_ann(st.session_state.processed_data, st.session_state.width)
        # Use a container to keep the graph stable
        with st.container():
            components.html(html, height=850)
    except Exception as e:
        st.error(f"Visualization Error: {e}")
else:
    st.info("Upload a PDF to see your Neural Architecture.")