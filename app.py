import streamlit as st

# --- CSS 스타일 정의 ---
# 배경 이미지를 전체 화면에 꽉 채우고, Streamlit 위젯의 가독성을 높이는 CSS
custom_css = """
<style>
/* Streamlit 앱의 메인 컨테이너에 배경 이미지 적용 */
.stApp {
    background-image: var(--bg-image); /* JavaScript에서 동적으로 설정될 배경 이미지 URL */
    background-size: cover; /* 이미지를 화면에 꽉 채우도록 크기 조절 */
    background-position: center; /* 이미지를 중앙에 배치 */
    background-repeat: no-repeat; /* 이미지 반복 없음 */
    min-height: 100vh; /* 앱의 최소 높이를 뷰포트 높이와 같게 설정 */
    display: flex; /* Flexbox 레이아웃 사용 */
    flex-direction: column; /* 아이템들을 세로로 정렬 */
    justify-content: flex-start; /* 아이템들을 상단에 배치 */
    align-items: center; /* 아이템들을 가로 중앙에 배치 (전역적으로, 필요시 오버라이드) */
    padding-top: 20px; /* 상단 여백 */
    position: relative; /* 자식 요소의 absolute 위치 기준점 */
    overflow-y: auto; /* 내용이 넘칠 경우 스크롤 허용 */
}

/* Streamlit 메인 콘텐츠 블록에 투명한 배경과 패딩 추가 */
/* 배경 이미지를 덮지 않고 투명하게 유지하면서 내부 콘텐츠를 감쌈 */
.main .block-container {
    background-color: rgba(0, 0, 0, 0); /* 완전 투명 */
    padding-top: 0rem;
    padding-right: 1rem;
    padding-left: 1rem;
    padding-bottom: 1rem;
    width: 100%; /* 너비를 꽉 채우도록 설정 */
    max-width: 100%; /* 최대 너비도 100% */
}

/* Streamlit 헤더와 푸터 숨기기 */
header {
    visibility: hidden;
    height: 0px !important;
}
footer {
    visibility: hidden;
    height: 0px !important;
}
.st-emotion-cache-cio0dv { /* "Made with Streamlit" 워터마크 숨김 */
    visibility: hidden;
}

/* 말풍선 스타일 */
.speech-bubble {
    position: relative; /* Streamlit 콘텐츠 흐름에 따라 배치 */
    margin-bottom: 20px; /* 아래 위젯들과 간격 */
    width: 80%; /* 폭 조정 */
    max-width: 600px; /* 최대 폭 */
    background-color: rgba(255, 255, 255, 0.85); /* 흰색 배경, 반투명 */
    border-radius: 20px;
    padding: 20px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
    text-align: center;
    font-size: 1.2em;
    color: #333;
    display: flex; /* Flexbox를 사용하여 내부 정렬 */
    align-items: center; /* 세로 중앙 정렬 */
    justify-content: center; /* 가로 중앙 정렬 */
    flex-direction: column; /* 내부 요소 세로 정렬 */
    z-index: 10; /* 다른 요소 위에 오도록 z-index 설정 */
}

.speech-bubble .character-img {
    width: 80px; /* 캐릭터 이미지 크기 */
    height: 80px;
    border-radius: 50%; /* 원형으로 만듬 */
    object-fit: cover;
    margin-bottom: 10px;
    border: 3px solid #6c5ce7; /* 테두리 추가 */
}

.speech-bubble p {
    margin: 0; /* 단락 마진 제거 */
    line-height: 1.5;
}

/* Streamlit 위젯 스타일 오버라이드 (가독성 향상) */
/* selectbox 드롭다운 배경색 */
div.stSelectbox > div {
    background-color: rgba(0, 0, 0, 0.6) !important; /* 반투명 검정 */
    border-radius: 5px;
    border: 1px solid rgba(255, 255, 255, 0.3); /* 연한 테두리 */
}
div.stSelectbox > div > div > div { /* 선택된 값 텍스트 색상 */
    color: #ffffff !important;
}
.st-cg, .st-ci, .st-ch, .st-ck { /* 드롭다운 옵션 텍스트 색상 (Streamlit 클래스) */
    color: #ffffff !important;
}
.st-cd, .st-ce { /* 드롭다운 옵션 배경색 (Streamlit 클래스) */
    background-color: rgba(0, 0, 0, 0.7) !important; /* 드롭다운 메뉴 배경 */
    color: #ffffff !important;
}

/* 라디오 버튼 텍스트 색상 */
div.stRadio > label {
    background-color: rgba(0, 0, 0, 0.6) !important; /* 반투명 검정 */
    color: #ffffff !important; /* 텍스트 흰색 */
    border-radius: 5px;
    padding: 5px 10px;
    margin-bottom: 5px;
    border: 1px solid rgba(255, 255, 255, 0.3);
}
div.stRadio > label:hover {
    background-color: rgba(0, 0, 0, 0.7) !important;
}
div.stRadio > label > div > p {
    color: #ffffff !important;
}

/* 텍스트 입력창 배경색 및 텍스트 색상 */
div.stTextInput > div > div {
    background-color: rgba(0, 0, 0, 0.6) !important; /* 반투명 검정 */
    border-radius: 5px;
    border: 1px solid rgba(255, 255, 255, 0.3);
}
div.stTextInput input {
    color: #ffffff !important; /* 입력 텍스트 흰색 */
    background-color: transparent !important; /* 내부 입력 필드 투명 */
}

/* 버튼 스타일 */
button.st-emotion-cache-gh2jli { /* Streamlit 버튼 기본 클래스 (변경될 수 있음) */
    background-color: #6c5ce7; /* 보라색 계열 */
    color: white;
    border-radius: 8px;
    padding: 10px 20px;
    font-size: 1.1em;
    border: none;
    cursor: pointer;
    transition: background-color 0.3s ease;
    margin-top: 10px;
}
button.st-emotion-cache-gh2jli:hover {
    background-color: #5a4ac3; /* 호버 시 색상 변경 */
}

/* 다음/이전 버튼 그룹 정렬을 위한 컨테이너 */
.button-container {
    display: flex;
    justify-content: center; /* 버튼을 중앙으로 정렬 */
    gap: 20px; /* 버튼 간 간격 */
    margin-top: 20px;
    width: 100%;
}

</style>
"""

# Streamlit 앱 시작 시 CSS 적용
st.markdown(custom_css, unsafe_allow_html=True)

# --- JavaScript를 사용하여 동적으로 배경 이미지 설정 ---
# Streamlit은 직접 CSS 변수를 파이썬에서 변경하기 어려우므로, JavaScript를 사용
def set_background_image_style(image_url):
    js_code = f"""
    <script>
        document.documentElement.style.setProperty('--bg-image', 'url("{image_url}")');
    </script>
    """
    st.markdown(js_code, unsafe_allow_html=True)

# --- 말풍선 표시 함수 ---
def display_speech_bubble(character_image_path, text):
    st.markdown(
        f"""
        <div class="speech-bubble">
            <img class="character-img" src="{character_image_path}" alt="Character Image">
            <p>{text}</p>
        </div>
        """,
        unsafe_allow_html=True
    )

# --- Streamlit 상태 초기화 ---
if 'current_step' not in st.session_state:
    st.session_state.current_step = 0
if 'user_name' not in st.session_state:
    st.session_state.user_name = ""

# --- 게임/스토리 단계 정의 ---
steps = [
    {
        "bg_image": "assets/background_images/background_main.png",
        "character_img": "assets/character_images/character_1.png",
        "text": "안녕? 난 인공지능 비서야. 널 도와주기 위해 있어.",
        "input": None,
        "options": None,
        "buttons": ["다음"]
    },
    {
        "bg_image": "assets/background_images/background_main.png",
        "character_img": "assets/character_images/character_1.png",
        "text": "나는 네가 어떤 상태인지 파악해서 너에게 딱 맞는 정보를 추천해 줄 거야. 네 이름을 알려줄 수 있니?",
        "input": "user_name",
        "options": None,
        "buttons": ["다음"]
    },
    {
        "bg_image": "assets/background_images/background_second.png",
        "character_img": "assets/character_images/character_1.png",
        "text": lambda name: f"만나서 반가워, {name}!\n이제 너의 현재 상태를 알려줘. 어떤 도움이 필요해?",
        "input": None,
        "options": {
            "type": "radio",
            "key": "user_state",
            "choices": ["업무", "학습", "취미", "스트레스 해소", "기타"]
        },
        "buttons": ["이전", "다음"]
    },
    {
        "bg_image": "assets/background_images/background_main.png",
        "character_img": "assets/character_images/character_1.png",
        "text": lambda state: f"네가 선택한 것은 '{state}'이구나. 좋아, 이제 더 자세한 내용을 알려줘.",
        "input": "detail_input",
        "options": None,
        "buttons": ["이전", "다음"]
    },
    {
        "bg_image": "assets/background_images/background_second.png",
        "character_img": "assets/character_images/character_1.png",
        "text": lambda name, detail: f"{name}의 '{st.session_state.user_state}' 관련 요청 '{detail}'을 잘 알겠어! 이제 최적의 솔루션을 찾아볼게!",
        "input": None,
        "options": None,
        "buttons": ["다시 시작"]
    }
]

# --- 네비게이션 함수 ---
def go_next():
    # 현재 단계가 텍스트 입력 단계이고, 입력값이 비어있으면 진행하지 않음
    if 'input' in steps[st.session_state.current_step] and steps[st.session_state.current_step]['input']:
        input_key = steps[st.session_state.current_step]['input']
        if not st.session_state.get(input_key):
            st.error("입력값을 채워주세요!")
            return

    if st.session_state.current_step < len(steps) - 1:
        st.session_state.current_step += 1
    else:
        # 마지막 단계에서 '다시 시작' 버튼 누르면 첫 단계로
        st.session_state.current_step = 0
        st.session_state.user_name = "" # 사용자 이름 초기화
        if 'user_state' in st.session_state:
            del st.session_state.user_state # 사용자 상태 초기화
        if 'detail_input' in st.session_state:
            del st.session_state.detail_input # 상세 입력 초기화

def go_prev():
    if st.session_state.current_step > 0:
        st.session_state.current_step -= 1

# --- 현재 단계 로직 실행 ---
current_step_data = steps[st.session_state.current_step]

# 1. 배경 이미지 설정 (가장 먼저)
set_background_image_style(current_step_data["bg_image"])

# 2. 말풍선 표시
speech_text = current_step_data["text"]
if callable(speech_text):
    if st.session_state.current_step == 2: # 이름 사용
        speech_text = speech_text(st.session_state.user_name)
    elif st.session_state.current_step == 3: # 상태 사용
        speech_text = speech_text(st.session_state.user_state)
    elif st.session_state.current_step == 4: # 이름과 상세 내용 사용
        speech_text = speech_text(st.session_state.user_name, st.session_state.detail_input)

display_speech_bubble(current_step_data["character_img"], speech_text)

# 3. 사용자 입력 위젯 표시 (말풍선 아래에 배치)
if current_step_data["input"]:
    st.text_input("여기에 입력하세요:", key=current_step_data["input"], label_visibility="collapsed")

if current_step_data["options"]:
    if current_step_data["options"]["type"] == "radio":
        st.radio("선택하세요:", current_step_data["options"]["choices"], key=current_step_data["options"]["key"], label_visibility="collapsed")
    elif current_step_data["options"]["type"] == "selectbox":
        st.selectbox("선택하세요:", current_step_data["options"]["choices"], key=current_step_data["options"]["key"], label_visibility="collapsed")


# 4. 네비게이션 버튼 표시 (가장 하단에 배치)
# 버튼을 감싸는 컨테이너를 사용하여 중앙 정렬
st.markdown('<div class="button-container">', unsafe_allow_html=True)
cols = st.columns(len(current_step_data["buttons"])) # 버튼 수에 따라 컬럼 생성

for i, button_label in enumerate(current_step_data["buttons"]):
    with cols[i]:
        if button_label == "다음":
            st.button(button_label, on_click=go_next, use_container_width=True)
        elif button_label == "이전":
            st.button(button_label, on_click=go_prev, use_container_width=True)
        elif button_label == "다시 시작":
            st.button(button_label, on_click=go_next, use_container_width=True) # 다시 시작은 next 함수와 동일하게 동작

st.markdown('</div>', unsafe_allow_html=True) # 컨테이너 닫기
