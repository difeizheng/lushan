"""
游览足迹页面
"""
import streamlit as st
from utils.footprints import render_footprint_ui

st.set_page_config(
    page_title="我的足迹",
    page_icon="👣",
    layout="wide"
)

render_footprint_ui()
