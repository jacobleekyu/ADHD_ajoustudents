import streamlit as st
from PIL import Image
import os

# --- 페이지 기본 설정 ---
st.set_page_config(page_title="ADHD 성향 설문", page_icon="🌱", layout="centered")

# --- CSS 스타일링 (여백 최소화 및 모바일 4등분 강제) ---
st.markdown("""
    <style>
    .stApp {
        background-color: #FDFBF7;
    }

    /* 1. 화면 최대 너비와 기본 여백 설정 */
    .block-container {
        padding-top: 1.5rem !important;
        padding-bottom: 1rem !important;
        padding-left: 1rem !important;
        padding-right: 1rem !important;
        max-width: 450px !important; 
        margin: 0 auto !important; 
    }

    /* 2. 버튼 4개가 들어가는 가로 블록의 간격을 완전히 없앰 */
    div[data-testid="stHorizontalBlock"] {
        gap: 0px !important; /* 버튼 사이 간격 0으로 밀착 */
    }

    /* 3. 모바일에서 4가지 버튼이 1줄에 딱 붙어서 나오도록 강제 */
    @media (max-width: 600px) {
        div[data-testid="stHorizontalBlock"] {
            flex-direction: row !important;
            flex-wrap: nowrap !important;
        }
        div[data-testid="column"] {
            width: 25% !important; /* 정확히 4등분 */
            flex: 1 1 25% !important; 
            min-width: 0 !important; 
            padding: 0 2px !important; /* 버튼 좌우 여백을 최소화하여 서로 밀착 */
        }
    }

    /* 4. 선택 버튼 디자인 (좁은 공간에 쏙 들어가도록) */
    div.stButton > button:first-child {
        border-radius: 30px;
        width: 100%;
        height: 45px;
        font-weight: bold;
        font-size: 12px !important; /* 글씨 크기를 살짝 줄여서 잘림 방지 */
        padding: 0 !important; 
        white-space: nowrap; 
        border: 2px solid #E0E0E0;
        background-color: white;
        color: #333333;
        transition: all 0.3s ease;
        box-shadow: 0px 2px 4px rgba(0,0,0,0.05);
    }
    div.stButton > button:first-child:hover {
        border-color: #8BC34A;
        color: #8BC34A;
        background-color: #F1F8E9;
    }

    /* 5. 사진 하단 여백 제거 */
    div[data-testid="stImage"] {
        margin-bottom: 0px;
    }
    
    h1, h2, h3, h4, p {
        color: #2C2C2C !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- 세션 상태(Session State) 초기화 ---
if 'page' not in st.session_state:
    st.session_state.page = 'start'
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'current_q' not in st.session_state:
    st.session_state.current_q = 1
