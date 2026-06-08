import streamlit as st
from PIL import Image
import os

# --- 페이지 기본 설정 ---
st.set_page_config(page_title="ADHD 성향 설문", page_icon="🌱", layout="centered")

# --- CSS 스타일링 (밝기 증가 & 한 화면 고정 스크롤 방지) ---
st.markdown("""
    <style>
    /* 1. 기본 앱 배경색 */
    .stApp {
        background-color: #FDFBF7;
    }

    /* 2. Streamlit 기본 상단바/하단바 숨기기 (공간 확보) */
    header {visibility: hidden;}
    footer {visibility: hidden;}

    /* 3. 화면을 한 페이지(100vh)에 고정하고 내용물을 중앙 정렬 */
    .block-container {
        padding-top: 1rem !important;
        padding-bottom: 0rem !important;
        padding-left: 1.5rem !important;
        padding-right: 1.5rem !important;
        max-width: 450px !important; 
        margin: 0 auto !important; 
        height: 100vh !important; /* 스마트폰 전체 높이로 고정 */
        display: flex;
        flex-direction: column;
        justify-content: center; /* 위아래 중앙 정렬 */
        overflow: hidden; /* 스크롤바 강제 숨김 */
    }

    /* 4. 🔥 사진 설정: 밝기를 15% 올리고, 높이를 화면의 45% 이내로 제한하여 스크롤 방지 */
    div[data-testid="stImage"] img {
        filter: brightness(1.15) !important; /* 사진 밝기 증가 (1.0이 원본, 1.15는 15% 밝게) */
        max-height: 45vh !important; /* 화면 높이의 45%까지만 커지도록 제한 */
        object-fit: contain !important; /* 비율 깨짐 방지 */
        width: 100% !important;
    }
    
    div[data-testid="stImage"] {
        margin-bottom: 5px;
    }

    /* 5. 텍스트 위아래 여백 최소화 */
    h3, h4 {
        margin-top: 0px !important;
        margin-bottom: 10px !important;
        padding: 0 !important;
        color: #2C2C2C !important;
    }

    /* 6. 버튼 4개 간격 및 마진 없애기 (사진 폭에 딱 맞춤) */
    div[data-testid="stHorizontalBlock"] {
        margin-left: 0 !important;
        margin-right: 0 !important;
        width: 100% !important;
        gap: 4px !important; 
    }
    div[data-testid="column"] {
        padding: 0 !important; 
        margin: 0 !important;
    }

    /* 7. 모바일 화면에서 무조건 1줄로 4등분 고정 */
    @media (max-width: 600px) {
        div[data-testid="stHorizontalBlock"] {
            flex-direction: row !important;
            flex-wrap: nowrap !important;
        }
        div[data-testid="column"] {
            width: 25% !important; 
            flex: 1 1 0% !important; 
            min-width: 0 !important; 
        }
    }

    /* 8. 버튼 디자인 (글자 잘림 방지 및 둥근 디자인) */
    div.stButton > button:first-child {
        border-radius: 20px;
        width: 100%;
        height: 45px;
        font-weight: bold;
        font-size: 13px !important; 
        letter-spacing: -0.5px; 
        padding: 0 2px !important; 
        word-break: keep-all; 
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
    {"num": 7, "text": "7. 학생증, 이어폰, 충전기, 필기구 등 필요한 물건을 자주 잃어버리거나 어디에 두었는지 찾기 어려운 적이 한 주에 몇 번 있나요?", "img": "q7.jpg"},
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
        st.warning("start.png 파일이 없습니다.")
    
    if st.button("🌱 시작하려면 클릭하세요!", key="start_btn", use_container_width=True):
        st.session_state.page = 'question'
        st.rerun()

# 2. 질문 화면
elif st.session_state.page == 'question':
    q_index = st.session_state.current_q - 1
    current_question = questions[q_index]
    
    st.markdown(f"<h4 style='text-align: center; font-size: 16px;'>{current_question['text']}</h4>", unsafe_allow_html=True)
    
    img_path = current_question["img"]
    if os.path.exists(img_path):
        image = Image.open(img_path)
        st.image(image, use_container_width=True)
    else:
        st.info(f"[{img_path}] 이미지를 준비 중입니다.")
    
    col1, col2, col3, col4 = st.columns(4)
    q_num = current_question["num"]
    
    if q_num == 7:
        btn_labels = ["0~1", "2~3", "4~5", "6+"]
        btn_points = [0, 1, 2, 3]
    elif q_num in [2, 5, 8]:
        btn_labels = ["드물다", "보통", "자주", "매우 자주"]
        btn_points = [0, 1, 2, 3]
    else:
        btn_labels = ["매우 자주", "자주", "보통", "드물다"]
        btn_points = [3, 2, 1, 0]
    
    with col1:
        if st.button(btn_labels[0], key=f"btn_col1_{q_index}"):
            go_to_next_question(btn_points[0])
            st.rerun()
    with col2:
        if st.button(btn_labels[1], key=f"btn_col2_{q_index}"):
            go_to_next_question(btn_points[1])
            st.rerun()
    with col3:
        if st.button(btn_labels[2], key=f"btn_col3_{q_index}"):
            go_to_next_question(btn_points[2])
            st.rerun()
    with col4:
        if st.button(btn_labels[3], key=f"btn_col4_{q_index}"):
            go_to_next_question(btn_points[3])
            st.rerun()
            
    st.write("")
    st.progress(st.session_state.current_q / 10)

# 3. 결과 화면
elif st.session_state.page == 'result':
    total_score = st.session_state.score
    
    st.markdown(f"<h3 style='text-align: center;'>당신의 총 점수는 {total_score}점 입니다.</h3>", unsafe_allow_html=True)

    result_img_path = ""
    if total_score >= 22:
        result_img_path = "final4.png"
    elif total_score >= 17:
        result_img_path = "final3.jpg"
    elif total_score >= 12:
        result_img_path = "final2.jpg"
    else:
        result_img_path = "final1.jpg"

    if os.path.exists(result_img_path):
        res_image = Image.open(result_img_path)
        st.image(res_image, use_container_width=True)
    else:
        st.error(f"결과 이미지({result_img_path})를 찾을 수 없습니다.")
        
    if st.button("🔄 다시 검사하기", use_container_width=True):
        restart_survey()
        st.rerun()
