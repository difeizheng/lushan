"""
全局搜索页面
"""
import streamlit as st
from utils.search import show_search_modal, load_all_data, search_spots, search_poems, search_celebrities

st.set_page_config(
    page_title="搜索",
    page_icon="🔍",
    layout="wide"
)

show_search_modal()
