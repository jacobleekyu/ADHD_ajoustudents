import streamlit as st
from PIL import Image
import os

# --- 페이지 기본 설정 ---
st.set_page_config(page_title="ADHD 성향 설문", page_icon="🌱", layout="centered")

# --- CSS 스타일링 (사진 폭에 버튼 맞춤 & 중앙 정렬) ---
st.markdown("""
    <style>
    .stApp {
        background-color: #FDFBF7;
    }

    /* 1. 화면 최대 너비를 스마트폰/사진 너비로 딱 맞춤 */
    .block-container {
        padding-top: 1.5rem !important;
        padding-bottom: 1rem !important;
        padding-left: 1rem !important;
        padding-right: 1rem !important;
        max-width: 450px !important; /* 사진과 버튼이 맞춰질 기준 선 */
        margin: 0 auto !important; /* 화면을 화면 정중앙에 고정 */
    }

    /* 2. 4가지 선택지 간격을 최소화하여 튀어나가지 않게 함 */
    div[data-testid="stHorizontalBlock"] {
        gap: 0.3rem !important;
    }

    /* 3. 모바일에서 4가지 버튼이 무조건 1줄에 딱 맞게 들어가도록 강제 */
    @media (max-width: 600px) {
        div[data-testid="stHorizontalBlock"] {
            flex-direction: row !important;
            flex-wrap: nowrap !important;
        }
        div[data-testid="column"] {
            width: auto !important;
            flex: 1 1 0% !important; /* 4등분하여 공간을 공평하게 나눠 가짐 */
            min-width: 0 !important; /* 버튼이 사진 폭 밖으로 밀려나는 것 완벽 차단 */
            padding: 0 !important;
        }
    }

    /* 4. 선택 버튼 디자인 (좁은 공간에서도 글씨가 예쁘게 보이도록 조정) */
    div.stButton > button:first-child {
        border-radius: 3
