import streamlit as st
import streamlit.components.v1 as components
from parser import get_triples
from visualize import draw_ann

st.set_page_config(layout="wide", page_title="Neuro-Notes Web")

# Width setting is critical to see all 123 neurons
if 'width' not in st.session_state: 
    st.session_state.width = 1200 # Starting even wider to ensure visibility

st.sidebar.title("📐 Design Controls")
if st.sidebar.button("➕ Make Wider (Fix Graphics)"):
    st.session_state.width += 300
    st.rerun()

st.title("🧠 Neuro-Notes: Public Knowledge Webpage")
file = st.file_uploader("Upload your Data Structures PDF", type="pdf")

if file:
    with st.spinner("Mapping 123 neurons..."):
        data = get_triples(file)
        if data:
            html = draw_ann(data, st.session_state.width)
            # FIXED: Removed 'key' argument which caused the TypeError
            components.html(html, height=850)
        else:
            st.error("No neurons found in PDF.")
else:
    st.info("Upload a PDF to see your Neural Architecture.")