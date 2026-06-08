import streamlit as st
from PIL import Image
import os

# --- 페이지 기본 설정 ---
st.set_page_config(page_title="ADHD 설문", layout="centered")

# --- CSS 스타일링 (핵심: 이미지 높이 제한 & 간격 삭제) ---
st.markdown("""
    <style>
    /* 1. 배경 및 기본 여백 제거 */
    .stApp { background-color: #FDFBF7; padding: 0px !important; }
    
    /* 2. 전체 컨테이너를 화면 꽉 차게 설정 */
    .block-container {
        padding: 10px !important;
        max-width: 400px !important; 
        margin: 0 auto !important; 
        height: 100vh !important;
        display: flex;
        flex-direction: column;
        justify-content: center;
        overflow: hidden;
    }

    /* 3. 🔥 사진 크기 강제 조절: 화면의 35%까지만 차지하도록 설정 */
    div[data-testid="stImage"] {
        display: flex;
        justify-content: center;
        margin: 0px !important;
    }
    div[data-testid="stImage"] img {
        max-height: 35vh !important; /* 사진이 너무 커지지 않게 제한 */
        object-fit: contain !important;
        border-radius: 15px;
    }

    /* 4. 질문 텍스트 크기 및 간격 */
    h4 {
        margin: 5px 0 !important;
        padding: 0 !important;
        font-size: 16px !important;
        text-align: center;
        color: #333 !important;
    }

    /* 5. 버튼 4등분 및 간격 밀착 */
    div[data-testid="stHorizontalBlock"] {
        gap: 4px !important; 
        margin-top: 5px !important;
    }
    div[data-testid="column"] {
        padding: 0 !important;
    }

    /* 6. 동그란 알약 버튼 */
    div.stButton > button {
        border-radius: 50px !important;
        height: 50px !important;
        width: 100% !important;
        font-size: 13px !important;
        font-weight: bold;
        background-color: white !important;
        border: 1px solid #ddd !important;
    }
    
    /* 진행도 바 높이 축소 */
    div[data-testid="stProgress"] { height: 4px !important; margin-bottom: 5px !important; }
    </style>
""", unsafe_allow_html=True)

# --- 세션 상태 ---
if 'page' not in st.session_state: st.session_state.page = 'start'
if 'score' not in st.session_state: st.session_state.score = 0
if 'current_q' not in st.session_state: st.session_state.current_q = 1

# --- 질문 데이터 ---
questions = [
    {"num": 1, "text": "1. 당신은 제출보다 사소한 수정에 집착한 적이 얼마나 자주 있나요?", "img": "q1.jpg"},
    {"num": 2, "text": "2. 해야 할 일의 우선순위 정리가 어려웠던 적이 얼마나 자주 있나요?", "img": "q2.jpg"},
    {"num": 3, "text": "3. 리포트 작성, 시험 공부처럼 많은 집중과 노력이 필요한 일을 시작하기 전에 자꾸 미루게 되는 일이 얼마나 자주 있나요?", "img": "q3.jpg"},
    {"num": 4, "text": "4. 수업을 들으면서 가만히 있기 힘든 적이 얼마나 자주 있나요?", "img": "q4.jpg"},
    {"num": 5, "text": "5. 지루한 일을 하며 집중이 끊긴 적이 얼마나 자주 있나요?", "img": "q5.jpg"},
    {"num": 6, "text": "6. 친구나 교수님이 중요한 이야기를 하고 있는데, 듣고 있는 중에도 갑자기 다른 생각이 떠올라 내용 일부를 놓친 적이 얼마나 자주 있나요?", "img": "q6.jpg"},
    {"num": 7, "text": "7. 학생증, 이어폰, 충전기, 필기구 등 필요한 물건을 자주 잃어버리거나 어디에 두었는지 찾기 어려운 적이 한 주에 몇 번 있나요?", "img": "q7.jpg"},
    {"num": 8, "text": "8. 회의나 수업처럼 계속 앉아 있어야 하는 상황에서 자리를 벗어나고 싶거나 몸이 답답하게 느껴진 적이 얼마나 자주 있나요?", "img": "q8.jpg"},
    {"num": 9, "text": "9. 대화 중에 스스로 '내가 지금 말을 너무 많이 하고 있나?'라고 느낀 적이 얼마나 자주 있나요?", "img": "q9.jpg"},
    {"num": 10, "text": "10. 상대방의 설명이 끝나기 전에 먼저 결론을 말하거나 끼어든 적이 얼마나 자주 있나요?", "img": "q10.jpg"}
]

# --- 로직 ---
def go_next(points):
    st.session_state.score += points
    st.session_state.current_q += 1
    if st.session_state.current_q > 10: st.session_state.page = 'result'
    st.rerun()

# --- 화면 ---
if st.session_state.page == 'start':
    if os.path.exists("start.png"): st.image("start.png", use_container_width=True)
    if st.button("🌱 시작하기"):
        st.session_state.page = 'question'
        st.rerun()

elif st.session_state.page == 'question':
    q = questions[st.session_state.current_q - 1]
    st.progress(st.session_state.current_q / 10)
    if os.path.exists(q["img"]): st.image(q["img"], use_container_width=True)
    st.markdown(f"<h4>{q['text']}</h4>", unsafe_allow_html=True)
    
    cols = st.columns(4)
    if q["num"] == 7: labels, points = ["0~1", "2~3", "4~5", "6+"], [0, 1, 2, 3]
    elif q["num"] in [2, 5, 8]: labels, points = ["드물다", "보통", "자주", "매우 자주"], [0, 1, 2, 3]
    else: labels, points = ["매우 자주", "자주", "보통", "드물다"], [3, 2, 1, 0]
    
    for i, col in enumerate(cols):
        with col:
            if st.button(labels[i]): go_next(points[i])

elif st.session_state.page == 'result':
    total = st.session_state.score
    st.markdown(f"### 총 점수: {total}점")
    res = "final4.png" if total >= 22 else "final3.jpg" if total >= 17 else "final2.jpg" if total >= 12 else "final1.jpg"
    if os.path.exists(res): st.image(res, use_container_width=True)
    if st.button("🔄 다시 하기"): 
        st.session_state.score = 0
        st.session_state.current_q = 1
        st.session_state.page = 'start'
        st.rerun()
