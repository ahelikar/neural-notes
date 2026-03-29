import streamlit as st
import streamlit.components.v1 as components
from parser import extract_neurons
from visualize import build_ann_graph

st.set_page_config(page_title="Neuro-Notes Web", layout="wide")

# Session State for Reset and Scaling
if 'n_size' not in st.session_state: st.session_state.n_size = 40
if 'l_gap' not in st.session_state: st.session_state.l_gap = 600
if 'data' not in st.session_state: st.session_state.data = [("Start", "to", "End")]

# Sidebar
st.sidebar.header("📐 Controls")
if st.sidebar.button("➕ Bigger"):
    st.session_state.n_size += 10
    st.session_state.l_gap += 100
if st.sidebar.button("➖ Smaller"):
    st.session_state.n_size -= 10
    st.session_state.l_gap -= 100
if st.sidebar.button("🔄 Reset"):
    st.session_state.n_size, st.session_state.l_gap = 40, 600
    st.session_state.data = [("Start", "to", "End")]
    st.rerun()

# Main
st.title("🧠 Neuro-Notes: Modular ANN Web-App")
file = st.file_uploader("Upload CSE PDF", type="pdf")

if file:
    st.session_state.data = extract_neurons(file)

graph_html = build_ann_graph(st.session_state.data, st.session_state.n_size, st.session_state.l_gap)
components.html(graph_html, height=750)
