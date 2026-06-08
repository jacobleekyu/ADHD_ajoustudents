import streamlit as st
from PIL import Image
import os

# --- 페이지 기본 설정 ---
st.set_page_config(page_title="ADHD 성향 설문", page_icon="🌱", layout="centered")

# --- CSS 스타일링 (배경색, 여백 최소화 및 버튼 디자인) ---
st.markdown("""
    <style>
    /* 1. 앱 전체 배경색을 자연스러운 연한 아이보리 톤으로 변경 */
    .stApp {
        background-color: #FDFBF7;
    }

    /* 2. 상하좌우 흰색 여백을 대폭 줄여 화면을 꽉 차게 만듦 */
    .block-container {
        padding-top: 2rem !important;
        padding-bottom: 1rem !important;
        padding-left: 0.5rem !important;
        padding-right: 0.5rem !important;
        max-width: 600px; /* 이미지가 한눈에 예쁘게 들어오는 너비 */
    }

    /* 3. 버튼을 둥글게 만들고 텍스트를 가운데 정렬 + 약간의 그림자 */
    div.stButton > button:first-child {
        border-radius: 30px;
        width: 100%;
        height: 50px;
        font-weight: bold;
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

    /* 4. 이미지 주변의 미세한 기본 여백 제거 */
    div[data-testid="stImage"] {
        margin-bottom: -10px;
    }
    
    /* 텍스트 요소들 색상을 배경과 어울리게 약간 부드럽게 조정 */
    h1, h2, h3, p {
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

# --- 질문 데이터 리스트 ---
questions = [
    {"num": 1, "text": "1. 당신은 제출보다 사소한 수정에 집착한 적이 얼마나 자주 있나요?", "img": "q1.jpg"},
    {"num": 2, "text": "2. 해야 할 일의 우선순위 정리가 어려웠던 적이 얼마나 자주 있나요?", "img": "q2.jpg"},
    {"num": 3, "text": "3. 리포트 작성, 시험 공부처럼 많은 집중과 노력이 필요한 일을 시작하기 전에 자꾸 미루게 되는 일이 얼마나 자주 있나요?", "img": "q3.jpg"},
    {"num": 4, "text": "4. 수업을 들으면서 가만히 있기 힘든 적이 얼마나 자주 있나요?", "img": "q4.jpg"},
    {"num": 5, "text": "5. 지루한 일을 하며 집중이 끊긴 적이 얼마나 자주 있나요?", "img": "q5.jpg"},
    {"num": 6, "text": "6. 친구나 교수님이 중요한 이야기를 하고 있는데, 듣고 있는 중에도 갑자기 다른 생각이 떠올라 내용 일부를 놓친 적이 얼마나 자주 있나요?", "img": "q6.jpg"},
    {"num": 7, "text": "7. 학생증, 이어폰, 충전기, 필기구 등 필요한 물건을 자주 잃어버리거나 어디에 두었는지 찾기 어려운 적이 얼마나 자주 있나요?", "img": "q7.jpg"},
    {"num": 8, "text": "8. 회의나 수업처럼 계속 앉아 있어야 하는 상황에서 자리를 벗어나고 싶거나 몸이 답답하게 느껴진 적이 얼마나 자주 있나요?", "img": "q8.jpg"},
    {"num": 9, "text": "9. 대화 중에 스스로 '내가 지금 말을 너무 많이 하고 있나?'라고 느낀 적이 얼마나 자주 있나요?", "img": "q9.jpg"},
    {"num": 10, "text": "10. 상대방의 설명이 끝나기 전에 먼저 결론을 말하거나 끼어든 적이 얼마나 자주 있나요?", "img": "q10.jpg"}
]

# --- 함수 모음 ---
def go_to_next_question(points):
    st.session_state.score += points
    st.session_state.current_q += 1
    if st.session_state.current_q > 10:
        st.session_state.page = 'result'

def restart_survey():
    st.session_state.page = 'start'
    st.session_state.score = 0
    st.session_state.current_q = 1

# --- 화면 렌더링 로직 ---

# 1. 시작 화면
if st.session_state.page == 'start':
    if os.path.exists("start.png"):
        image = Image.open("start.png")
        st.image(image, use_container_width=True)
    else:
        st.warning("start.jpg 파일이 없습니다. 이미지를 추가해주세요.")
    
    st.write("") 
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🌱 시작하려면 클릭하세요!", key="start_btn"):
            st.session_state.page = 'question'
            st.rerun()

# 2. 질문 화면
elif st.session_state.page == 'question':
    q_index = st.session_state.current_q - 1
    current_question = questions[q_index]
    
    st.markdown(f"<h4 style='text-align: center;'>{current_question['text']}</h4>", unsafe_allow_html=True)
    
    img_path = current_question["img"]
    if os.path.exists(img_path):
        image = Image.open(img_path)
        st.image(image, use_container_width=True)
    else:
        st.info(f"[{img_path}] 이미지를 준비 중입니다.")
    
    st.write("") 
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("매우 자주", key=f"btn3_{q_index}"):
            go_to_next_question(3)
            st.rerun()
    with col2:
        if st.button("자주", key=f"btn2_{q_index}"):
            go_to_next_question(2)
            st.rerun()
    with col3:
        if st.button("보통", key=f"btn1_{q_index}"):
            go_to_next_question(1)
            st.rerun()
    with col4:
        if st.button("드물다", key=f"btn0_{q_index}"):
            go_to_next_question(0)
            st.rerun()
            
    st.progress(st.session_state.current_q / 10)

# 3. 결과 화면
elif st.session_state.page == 'result':
    total_score = st.session_state.score
    
    # 점수 기준별 결과 이미지 매칭
    result_img_path = ""
    if total_score >= 22:
        result_img_path = "final4.png"  # 상담 권장 단계
    elif total_score >= 17:
        result_img_path = "final3.jpg"  # 주의 단계
    elif total_score >= 12:
        result_img_path = "final2.jpg"  # 관심 단계
    else:
        result_img_path = "final1.jpg"  # 안정 단계

    # 결과 이미지 출력
    if os.path.exists(result_img_path):
        res_image = Image.open(result_img_path)
        st.image(res_image, use_container_width=True)
    else:
        st.error(f"결과 이미지({result_img_path})를 찾을 수 없습니다. 폴더에 이미지가 있는지 확인해주세요.")
        
    st.write("")
    
    # 다시하기 버튼
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🔄 다시 검사하기"):
            restart_survey()
            st.rerun()
