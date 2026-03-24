"""
AI 智能导游页面
"""
import streamlit as st
from utils.ai_guide import render_chat_interface

st.set_page_config(
    page_title="AI 导游",
    page_icon="🤖",
    layout="wide"
)

render_chat_interface()
