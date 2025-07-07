import streamlit as st
import pandas as pd
import os
import random
import time

# --- CSS 스타일 정의 ---
custom_css = """
<style>
/* Streamlit 앱의 메인 컨테이너에 배경 이미지 적용 */
/* JavaScript에서 동적으로 설정할 변수를 선언 */
:root {
    --bg-image: none;
}

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
    /* 원래 위치를 유지 */
    position: absolute; bottom: 8vh; left: 50%; transform: translateX(-50%);
    width: 90%; max-width: 500px; background: rgba(255, 255, 255, 0.1);
    padding: 20px 25px; border-radius: 25px; box-shadow: 0 4px 15px rgba(0, 0, 0, 0.4);
    text-align: center; z-index: 100; /* 배경 이미지보다 위에 오도록 z-index를 높게 설정 */
    backdrop-filter: blur(8px); /* 블러 효과로 배경 가독성 향상 */
    -webkit-backdrop-filter: blur(8px); /* Safari 지원 */
}
.speech-title { font-size: 1.4rem; font-weight: bold; color: #ffffff; }
.speech-sub { margin-top: 10px; font-size: 1rem; color: #f0f0f0; }

/* Streamlit 위젯 스타일 오버라이드 (가독성 향상) */
/* 모든 라벨 텍스트 기본 색상 흰색으로 설정 */
label {
    color: #ffffff !important;
}
p {
    color: #ffffff !important; /* 일반 텍스트도 흰색으로 */
}

/* selectbox 드롭다운 배경색 */
div[data-baseweb="select"] > div { /* selectbox 컨테이너 */
    background-color: rgba(0, 0, 0, 0.6) !important; /* 반투명 검정 */
    border-radius: 5px;
    border: 1px solid rgba(255, 255, 255, 0.3); /* 연한 테두리 */
}
div[data-baseweb="select"] > div > div > div { /* 선택된 값 텍스트 색상 */
    color: #ffffff !important;
}
/* 드롭다운 메뉴 (옵션 목록) */
div[data-baseweb="popover"] > div > div {
    background-color: rgba(0, 0, 0, 0.8) !important; /* 드롭다운 메뉴 배경 */
    color: #ffffff !important;
    border: 1px solid rgba(255, 255, 255, 0.3);
    border-radius: 5px;
}
div[data-baseweb="popover"] > div > div * { /* 드롭다운 메뉴 내부 텍스트 */
    color: #ffffff !important;
}
div[data-baseweb="popover"] li:hover { /* 드롭다운 메뉴 호버 시 */
    background-color: rgba(255, 255, 255, 0.2) !important;
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
div.stRadio > label > div > input:checked + div { /* 선택된 라디오 버튼 원 안의 색 */
    background-color: #6c5ce7 !important;
    border-color: #6c5ce7 !important;
}

/* 텍스트 입력창 배경색 및 텍스트 색상 */
div.stTextInput > div > div { /* 바깥쪽 컨테이너 */
    background-color: rgba(0, 0, 0, 0.6) !important; /* 반투명 검정 */
    border-radius: 5px;
    border: 1px solid rgba(255, 255, 255, 0.3);
}
div.stTextInput input { /* 실제 입력 필드 */
    color: #ffffff !important; /* 입력 텍스트 흰색 */
    background-color: transparent !important; /* 내부 입력 필드 투명 */
}

/* 버튼 스타일 */
/* Streamlit 1.x 버전에서는 button 클래스가 동적으로 변경될 수 있으므로,
   가장 바깥쪽 div에 있는 button 태그를 선택하는 것이 가장 안전합니다. */
button[data-testid*="stButton"] > div > p {
    color: #ffffff !important; /* 버튼 텍스트 색상 */
    font-weight: bold;
}
button[data-testid*="stButton"] { /* 버튼 실제 요소 */
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
button[data-testid*="stButton"]:hover {
    background-color: #5a4ac3; /* 호버 시 색상 변경 */
}

/* 에러 메시지 텍스트 색상 */
.st-emotion-cache-1f06x3d p { /* Streamlit error 메시지 클래스 */
    color: red !important;
}

</style>
"""

# Streamlit 앱 시작 시 CSS 적용
st.markdown(custom_css, unsafe_allow_html=True)

# --- JavaScript를 사용하여 동적으로 배경 이미지 설정 ---
# 이 함수는 .stApp의 --bg-image CSS 변수를 변경하여 배경 이미지를 설정합니다.
def set_background_image(image_url):
    js_code = f"""
    <script>
        document.documentElement.style.setProperty('--bg-image', 'url("{image_url}")');
    </script>
    """
    st.markdown(js_code, unsafe_allow_html=True)

# ✅ 세션 상태 초기화 함수
def initialize_session_state():
    """Streamlit 세션 상태를 초기화하거나 재설정합니다."""
    defaults = {
        "step": 0,
        "industry": "",
        "industry_confirmed": False,
        "company_name": "",
        "situation": "",
        "options": [],
        "selected_strategy_feedback": "",
        "score": 0,
        "crisis_situation": "",
        "crisis_options": [],
        "effective_strategies_map": {},
        "best_crisis_strategies_map": {},
        "random_events_data": {},
        "step3_score_earned": 0,
        "step5_score_earned": 0,
        "step7_score_earned": 0,  # 기존 Step 6 (내부 문제 해결)
        "step8_score_earned": 0,  # 기존 Step 7 (돌발 변수)
        "step9_score_earned": 0,  # 기존 Step 8 (마케팅/확장)
        "step3_strategy_selected": "",
        "step5_strategy_selected": "",
        "step7_strategy_selected": "",  # 기존 Step 6
        "step8_strategy_selected": "",  # 기존 Step 7
        "step9_strategy_selected": "",  # 기존 Step 8
        "current_event_name": None,
        "current_event_options": [],
        "current_event_best_strategy": "",
        "step7_state": "pending",  # Step 7 (내부 문제 해결) 진행 상태 관리
        "step8_state": "pending",  # Step 8 (돌발 변수) 진행 상태 관리
        "step9_state": "pending",  # Step 9 (마케팅/확장) 진행 상태 관리
    }

    if st.session_state.get("reset_game", False):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.session_state.reset_game = False

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

initialize_session_state()

# ---
# ✅ 로컬 파일 기반 순위 시스템 함수
RANK_FILE = "rankings.csv"

def save_to_ranking(company_name, final_score):
    """회사명과 점수를 rankings.csv에 저장"""
    new_entry = pd.DataFrame([{"company_name": company_name, "score": final_score}])

    if os.path.exists(RANK_FILE):
        existing = pd.read_csv(RANK_FILE)
        updated = pd.concat([existing, new_entry], ignore_index=True)
    else:
        updated = new_entry

    updated.to_csv(RANK_FILE, index=False)
    st.success(f"점수가 성공적으로 기록되었습니다: {company_name}, {final_score}점")


def show_full_rankings():
    """전체 순위 출력 (내림차순 정렬)"""
    if os.path.exists(RANK_FILE):
        df = pd.read_csv(RANK_FILE)
        df_sorted = df.sort_values(by="score", ascending=False).reset_index(drop=True)
        df_sorted.index = df_sorted.index + 1  # 1부터 시작하는 순위
        st.markdown("### 🏁 전체 플레이어 순위표")
        st.dataframe(df_sorted, use_container_width=True)
    else:
        st.info("아직 저장된 기록이 없습니다.")

# ---
# ✅ 말풍선 출력 함수 (배경 이미지는 set_background_image로 분리)
def show_speech(title: str, subtitle: str):
    """말풍선 UI만 렌더링합니다. 배경 이미지는 별도로 set_background_image 함수로 설정됩니다."""
    st.markdown(f"""
    <div class="speech-bubble">
        <div class="speech-title">{title}</div>
        <div class="speech-sub">{subtitle}</div>
    </div>
    """, unsafe_allow_html=True)

# ---
# --- 게임/스토리 단계 정의 (기존 스토리 유지) ---
# Step 정보들을 딕셔너리로 미리 정의하여 관리 용이하게
game_steps_info = {
    0: {
        "bg_image": "https://raw.githubusercontent.com/dddowobbb/16-1/main/talking%20ceo.png",
        "speech_title": "“환영합니다!”",
        "speech_subtitle": "게임 플레이에 앞서 다크모드를 적용중이시라면 라이트모드로 전환해주시길 바랍니다."
    },
    1: {
        "bg_image": "https://raw.githubusercontent.com/dddowobbb/16-1/main/talking%20ceo.png",
        "speech_title_pending": "“좋아, 이제 우리가 어떤 산업에 뛰어들지 결정할 시간이군.”",
        "speech_subtitle_pending": "어떤 분야에서 승부할지, 네 선택을 보여줘.",
        "speech_title_confirmed": lambda industry: f"“{industry}... 흥미로운 선택이군.”",
        "speech_subtitle_confirmed": "다음 단계로 가볼까?"
    },
    2: {
        "bg_image": "https://raw.githubusercontent.com/dddowobbb/16-1/main/talking%20ceo.png",
        "speech_title_pending": "“이제 회사를 설립할 시간이야.”",
        "speech_subtitle_pending": "멋진 회사 이름을 지어보자!",
        "speech_title_confirmed": lambda name: f"“{name}... 멋진 이름이군!”",
        "speech_subtitle_confirmed": "이제 다음 단계로 넘어가자."
    },
    3: {
        "bg_image": "https://raw.githubusercontent.com/dddowobbb/simulator1/main/badevent.png",
        "speech_title": "“예기치 못한 사건 발생!”",
        "speech_subtitle": "상황에 적절한 전략을 선택해 회사를 지켜내자."
    },
    4: {
        "bg_image": "https://raw.githubusercontent.com/dddowobbb/16-1/main/talking%20ceo.png",
        "speech_title_good": "“훌륭한 판단이었어!”",
        "speech_title_bad": "“음... 더 나은 전략도 있었을 거야.”",
        "speech_subtitle": lambda feedback: feedback # feedback은 selected_strategy_feedback
    },
    5: {
        "bg_image": "https://raw.githubusercontent.com/dlwlgh726/16-/main/badevent.png",
        "speech_title": "“국가적 위기 발생!”",
        "speech_subtitle": "경제, 정치, 국제 환경이 급변하고 있어. 대응 전략이 필요해."
    },
    6: {
        "bg_image": "https://raw.githubusercontent.com/dddowobbb/16-1/main/talking%20ceo.png",
        "speech_title_good": "“최고의 경영자군!”",
        "speech_title_bad": "“괜찮은 성과지만 아직 성장 가능성이 보여.”",
        "speech_subtitle": lambda feedback, score: f"{feedback} 총 점수: {score}점"
    },
    7: {
        "bg_image_pending": "https://raw.githubusercontent.com/dlwlgh726/16-/main/KakaoTalk_Photo_2025-07-03-16-19-06 005.png",
        "bg_image_done": "https://raw.githubusercontent.com/dddowobbb/16-1/main/talking%20ceo.png",
        "speech_title_pending": "“요즘 직원들 분위기가 심상치 않아...”",
        "speech_subtitle_pending": "사기 저하, 인사 갈등, 생산성 저하 문제가 보고됐어. 어떻게 대응할까?",
        "speech_title_done": lambda prefix: prefix,
        "speech_subtitle_done": lambda feedback, score: f"{feedback} (누적 점수: {score}점)"
    },
    8: {
        "bg_image_pending": "https://raw.githubusercontent.com/dlwlgh726/16-/main/badevent.png",
        "bg_image_done": "https://raw.githubusercontent.com/dddowobbb/16-1/main/talking%20ceo.png",
        "speech_title_pending": "“뜻밖의 일이 벌어졌어!”",
        "speech_subtitle_pending": "외부 변수로 인해 경영환경이 크게 흔들리고 있어.",
        "speech_title_done": lambda prefix: prefix,
        "speech_subtitle_done": lambda feedback, score: f"{feedback} (총 점수: {score}점)"
    },
    9: {
        "bg_image_pending": "https://raw.githubusercontent.com/dlwlgh726/16-/main/goodevent.png",
        "bg_image_done": "https://raw.githubusercontent.com/dddowobbb/16-1/main/talking%20ceo.png",
        "speech_title_pending": "“제품이 시장에서 인기를 얻기 시작했어!”",
        "speech_subtitle_pending": "이제 어떻게 회사를 더욱 성장시킬지 결정해야 해.",
        "speech_title_done": lambda prefix: prefix,
        "speech_subtitle_done": lambda feedback, score: f"{feedback} (누적 점수: {score}점)"
    },
    10: {
        "bg_image": "https://raw.githubusercontent.com/dddowobbb/16-1/main/talking%20ceo.png",
        "speech_title": lambda company_name: f"“{company_name}의 3년간 경영 리포트”",
        "speech_subtitle": "당신의 선택이 회사를 이렇게 변화시켰습니다."
    },
    11: {
        "bg_image_good": "https://raw.githubusercontent.com/dlwlgh726/16-/main/applause.png",
        "bg_image_bad": "https://raw.githubusercontent.com/dlwlgh726/16-/main/badevent.png",
        "speech_title_unicorn": "“글로벌 유니콘 기업 달성!”",
        "speech_title_growth": "“안정적 성장!”",
        "speech_title_reorg": "“재정비의 기회!”",
        "speech_title_failure": "“혹독한 실패...”",
        "speech_subtitle": lambda msg: msg
    }
}


## Step 0: 시작 안내
if st.session_state.step == 0:
    set_background_image(game_steps_info[0]["bg_image"])
    show_speech(game_steps_info[0]["speech_title"], game_steps_info[0]["speech_subtitle"])
    st.markdown("### 경영 시뮬레이션 게임에 오신 것을 환영합니다!")
    st.markdown("이 게임에서는 회사를 창업하고 성장시키는 과정에서 다양한 결정을 내려야 합니다. 회사를 성공적으로 운영해보세요!")
    if st.button("게임 시작 ▶️"):
        st.session_state.step = 1
        st.rerun()

# ---
## Step 1: 업종 선택
elif st.session_state.step == 1:
    set_background_image(game_steps_info[1]["bg_image"]) # Step 1의 배경 이미지 설정

    if not st.session_state.industry_confirmed:
        show_speech(game_steps_info[1]["speech_title_pending"], game_steps_info[1]["speech_subtitle_pending"])
    else:
        # 이미 확정된 경우, 람다 함수 호출
        show_speech(game_steps_info[1]["speech_title_confirmed"](st.session_state.industry), game_steps_info[1]["speech_subtitle_confirmed"])

    st.markdown("### Step 1: 회사 분야 선택")
    industries = ["💻 IT 스타트업", "🌱 친환경 제품", "🎮 게임 개발사", "👗 패션 브랜드", "🍔 푸드테크", "🛒 글로벌 전자상거래"]

    if not st.session_state.industry_confirmed:
        selected = st.selectbox("회사 업종을 선택해주세요", industries)
        if st.button("업종 확정"):
            st.session_state.industry = selected
            st.session_state.industry_confirmed = True
            st.session_state.step = 2 # 다음 스텝으로 바로 이동
            st.rerun()
    else:
        st.success(f"✅ 선택된 업종: **{st.session_state.industry}**")
        if st.button("다음 ▶️"):
            st.session_state.step = 2
            st.rerun()

# ---
## Step 2: 회사 이름 입력
elif st.session_state.step == 2:
    set_background_image(game_steps_info[2]["bg_image"]) # Step 2의 배경 이미지 설정

    if not st.session_state.company_name:
        show_speech(game_steps_info[2]["speech_title_pending"], game_steps_info[2]["speech_subtitle_pending"])
    else:
        show_speech(game_steps_info[2]["speech_title_confirmed"](st.session_state.company_name), game_steps_info[2]["speech_subtitle_confirmed"])

    st.markdown("### Step 2: 회사 이름 입력")
    name_input = st.text_input("당신의 회사 이름은?", max_chars=20)

    if st.button("회사 이름 확정"):
        if name_input.strip():
            st.session_state.company_name = name_input.strip()
            st.success("✅ 회사 이름이 등록되었습니다!")
        else:
            st.warning("⚠️ 회사 이름을 입력해주세요.")

    if st.session_state.company_name and st.button("다음 ▶️"):
        st.session_state.step = 3
        st.rerun()

# ---
## Step 3: 전략 선택 (예기치 못한 사건)
elif st.session_state.step == 3:
    set_background_image(game_steps_info[3]["bg_image"]) # Step 3의 배경 이미지 설정
    show_speech(game_steps_info[3]["speech_title"], game_steps_info[3]["speech_subtitle"])

    situations = {
        "⚠️ 대규모 고객 데이터 유출 발생": ["보안 시스템 전면 재구축", "PR 대응", "사과문 발표", "외부 컨설턴트 투입", "서비스 일시 중단"],
        "📈 갑작스러운 수요 폭증": ["생산 라인 확장", "기술 투자", "임시 고용 확대", "외주 활용", "품질 단가 조정"],
        "💸 원자재 가격 급등": ["공급처 다변화", "대체 소재 도입", "장기 계약", "수입 조정", "원가 절감"],
        "🔥 경쟁사 파산": ["인재 채용 강화", "기술 인수", "시장 확대", "기술 유출 방지", "법적 검토"],
        "📉 주요 제품 매출 급감": ["제품 리뉴얼", "광고 캠페인", "신제품 출시", "할인 행사", "시장 조사"],
        "🏆 대기업으로부터 투자 제안": ["지분 일부 매각", "전략적 제휴", "거절", "조건 재협상", "지분 공동 소유"],
        "🌍 글로벌 시장 진출 기회": ["현지화 전략", "글로벌 광고 캠페인", "온라인 직판", "외국 파트너와 제휴", "해외 공장 설립"]
    }
    effective_strategies_map_data = {
        "⚠️ 대규모 고객 데이터 유출 발생": "보안 시스템 전면 재구축",
        "📈 갑작스러운 수요 폭증": "생산 라인 확장",
        "💸 원자재 가격 급등": "공급처 다변화",
        "🔥 경쟁사 파산": "인재 채용 강화",
        "📉 주요 제품 매출 급감": "제품 리뉴얼",
        "🏆 대기업으로부터 투자 제안": "지분 일부 매각",
        "🌍 글로벌 시장 진출 기회": "현지화 전략"
    }
    st.session_state.effective_strategies_map = effective_strategies_map_data

    if not st.session_state.situation:
        st.session_state.situation, st.session_state.options = random.choice(list(situations.items()))

    st.markdown("### Step 3: 전략 선택")
    st.markdown(f"📍 **상황:** {st.session_state.situation}")
    strategy = st.radio("🧠 당신의 전략은?", st.session_state.options)

    if st.button("전략 확정"):
        st.session_state.step3_strategy_selected = strategy

        if strategy == st.session_state.effective_strategies_map.get(st.session_state.situation):
            st.session_state.score += 10
            st.session_state.step3_score_earned = 10
            st.session_state.selected_strategy_feedback = f"선택한 전략: **{strategy}** (획득 점수: 10점)"
        else:
            st.session_state.score += 5
            st.session_state.step3_score_earned = 5
            st.session_state.selected_strategy_feedback = f"선택한 전략: **{strategy}** (획득 점수: 5점)"

        st.session_state.step = 4
        st.rerun()

# ---
## Step 4: 결과 분석 및 피드백 (Step 3에 대한)
elif st.session_state.step == 4:
    set_background_image(game_steps_info[4]["bg_image"]) # Step 4의 배경 이미지 설정

    score_earned_this_step = st.session_state.get("step3_score_earned", 0)
    selected_strategy_for_feedback = st.session_state.get("step3_strategy_selected", "선택 없음")

    if score_earned_this_step == 10:
        title = game_steps_info[4]["speech_title_good"]
    else:
        title = game_steps_info[4]["speech_title_bad"]

    # 람다 함수에 필요한 인자 전달
    subtitle = game_steps_info[4]["speech_subtitle"](st.session_state.selected_strategy_feedback)
    show_speech(title, subtitle)

    st.markdown("### Step 4: 결과 분석")
    st.success(f"당신의 전략: **{selected_strategy_for_feedback}**")
    st.info(f"현재 점수: **{st.session_state.score}점**")

    # 세션 상태 정리
    if "step3_score_earned" in st.session_state:
        del st.session_state.step3_score_earned
    if "step3_strategy_selected" in st.session_state:
        del st.session_state.step3_strategy_selected
    st.session_state.situation = ""
    st.session_state.options = []
    st.session_state.selected_strategy_feedback = ""

    if st.button("다음 이벤트 ▶️"):
        st.session_state.step = 5
        st.rerun()

# ---
## Step 5: 국가적 위기 대응
elif st.session_state.step == 5:
    set_background_image(game_steps_info[5]["bg_image"]) # Step 5의 배경 이미지 설정
    show_speech(game_steps_info[5]["speech_title"], game_steps_info[5]["speech_subtitle"])

    crisis_situations = {
        "📉 한국 외환시장 급변 (원화 가치 급락)": ["환 헤지 강화", "수출 확대", "정부와 협력", "외환 보유 확대", "위기 커뮤니케이션"],
        "🇺🇸 미 연준의 기준금리 인상": ["대출 축소", "내수 집중 전략", "고금리 대비 자산 조정", "비용 구조 개선", "긴축 경영"],
        "🗳️ 정치적 불확실성 증가": ["리스크 분산 경영", "정치 모니터링 강화", "내부 의사결정 체계 정비", "단기 전략 전환", "위기 대비 태스크포스 운영"],
        "🇺🇸 트럼프 대통령 재취임": ["미국 중심 전략 강화", "공급망 재편", "관세 대비 물류 최적화", "현지 생산 강화", "미국 투자 확대"],
        "🛃 주요 국가의 관세 인상 정책": ["무역 파트너 다변화", "현지 생산 확대", "비관세 수출 전략", "신시장 개척", "가격 재설정"]
    }

    if "best_crisis_strategies_map" not in st.session_state or not st.session_state.best_crisis_strategies_map:
        best_strategies_map_data = {
            "📉 한국 외환시장 급변 (원화 가치 급락)": "환 헤지 강화",
            "🇺🇸 미 연준의 기준금리 인상": "고금리 대비 자산 조정",
            "🗳️ 정치적 불확실성 증가": "리스크 분산 경영",
            "🇺🇸 트럼프 대통령 재취임": "공급망 재편",
            "🛃 주요 국가의 관세 인상 정책": "무역 파트너 다변화"
        }
        st.session_state.best_crisis_strategies_map = best_strategies_map_data

    if not st.session_state.crisis_situation:
        st.session_state.crisis_situation, st.session_state.crisis_options = random.choice(list(crisis_situations.items()))

    st.markdown("### Step 5: 국가적 위기 대응")
    st.markdown(f"**상황:** {st.session_state.crisis_situation}")
    crisis_strategy = st.radio("🧠 대응 전략을 선택하세요:", st.session_state.crisis_options)

    if st.button("전략 확정"):
        st.session_state.step5_strategy_selected = crisis_strategy

        if crisis_strategy == st.session_state.best_crisis_strategies_map.get(st.session_state.crisis_situation):
            st.session_state.score += 10
            st.session_state.step5_score_earned = 10
            st.session_state.selected_strategy_feedback = f"국가적 위기 속 **{crisis_strategy}** 전략은 뛰어난 선택이었어. (획득 점수: 10점)"
        else:
            st.session_state.score += 5
            st.session_state.step5_score_earned = 5
            st.session_state.selected_strategy_feedback = f"국가적 위기 속 **{crisis_strategy}** 전략도 나쁘지 않았어. (획득 점수: 5점)"

        st.session_state.step = 6 # 다음 스텝으로 이동 (새로운 피드백 스텝)
        st.rerun()

# ---
## Step 6: 중간 평가 (국가적 위기 대응에 대한 피드백)
elif st.session_state.step == 6:
    set_background_image(game_steps_info[6]["bg_image"]) # Step 6의 배경 이미지 설정

    score_earned_this_step = st.session_state.get("step5_score_earned", 0)
    selected_strategy_for_feedback = st.session_state.get("step5_strategy_selected", "선택 없음")

    if score_earned_this_step == 10:
        title = game_steps_info[6]["speech_title_good"]
    else:
        title = game_steps_info[6]["speech_title_bad"]

    subtitle = game_steps_info[6]["speech_subtitle"](st.session_state.selected_strategy_feedback, st.session_state.score)
    show_speech(title, subtitle)

    st.markdown("### Step 6: 국가적 위기 대응 결과")
    st.success(f"당신의 전략: **{selected_strategy_for_feedback}**")
    st.info(f"현재 점수: **{st.session_state.score}점**")

    if "step5_score_earned" in st.session_state:
        del st.session_state.step5_score_earned
    if "step5_strategy_selected" in st.session_state:
        del st.session_state.step5_strategy_selected
    st.session_state.selected_strategy_feedback = ""

    if st.button("다음 이벤트 ▶️"):
        st.session_state.step = 7 # 다음 스텝으로 이동 (기존 Step 6)
        st.rerun()

# ---
## Step 7: 내부 문제 해결 (이전 Step 6)
elif st.session_state.step == 7:
    org_issues = {
        "🧠 조직문화 혁신": 10,
        "💰 복지 강화": 8,
        "🔁 리더십 교체": 6,
        "📚 교육 강화": 7,
        "🧘 그냥 기다린다": 2
    }

    if st.session_state.step7_state == "pending":
        set_background_image(game_steps_info[7]["bg_image_pending"])
        show_speech(game_steps_info[7]["speech_title_pending"], game_steps_info[7]["speech_subtitle_pending"])
        st.markdown("### Step 7: 내부 문제 해결 전략 선택")

        selected_org_strategy = st.radio("내부 문제를 해결할 전략을 선택하세요:", list(org_issues.keys()))

        if st.button("전략 확정"):
            st.session_state.step7_strategy_selected = selected_org_strategy
            st.session_state.score += org_issues[selected_org_strategy]
            st.session_state.step7_score_earned = org_issues[selected_org_strategy]

            if st.session_state.step7_score_earned >= 8:
                title_prefix = "탁월한 내부 결정이었어!"
            elif st.session_state.step7_score_earned >= 5:
                title_prefix = "무난한 선택이었군."
            else:
                title_prefix = "기다리는 건 항상 좋은 선택은 아니지..."

            st.session_state.selected_strategy_feedback = (
                f"{title_prefix}\n\n" # 말풍선 제목으로 사용될 부분
                f"{selected_org_strategy} 전략에 따른 점수: {st.session_state.step7_score_earned}점"
            )

            st.session_state.step7_state = "done"
            st.rerun()

    elif st.session_state.step7_state == "done":
        set_background_image(game_steps_info[7]["bg_image_done"])

        # 피드백 메시지 파싱
        feedback_parts = st.session_state.selected_strategy_feedback.split('\n\n', 1)
        title_bubble = game_steps_info[7]["speech_title_done"](feedback_parts[0]) # 첫 번째 라인을 제목으로 사용
        subtitle_bubble = game_steps_info[7]["speech_subtitle_done"](feedback_parts[1] if len(feedback_parts) > 1 else "", st.session_state.score)

        show_speech(title_bubble, subtitle_bubble)

        st.markdown("### Step 7: 내부 문제 해결 결과")
        st.success(f"당신의 전략: **{st.session_state.step7_strategy_selected}**")
        st.info(f"누적 점수: **{st.session_state.score}점**")

        # Step 7 관련 세션 상태 정리
        if "step7_score_earned" in st.session_state:
            del st.session_state.step7_score_earned
        if "step7_strategy_selected" in st.session_state:
            del st.session_state.step7_strategy_selected
        st.session_state.selected_strategy_feedback = ""

        if st.button("다음 이벤트 ▶️"):
            st.session_state.step = 8 # 다음 스텝으로 이동 (기존 Step 7)
            st.session_state.step7_state = "pending"
            st.rerun()

# ---
## Step 8: 돌발 변수 등장 (이전 Step 7)
elif st.session_state.step == 8:
    if not st.session_state.random_events_data:
        st.session_state.random_events_data = {
            "📉 글로벌 경제 불황": {
                "options": ["비용 절감", "내수 시장 집중", "긴축 재정 운영", "신사업 보류", "시장 철수"],
                "best": "내수 시장 집중"
            },
            "🚀 경쟁사의 혁신 제품 발표": {
                "options": ["기술 개발 가속", "브랜드 리뉴얼", "마케팅 강화", "가격 인하", "특허 소송"],
                "best": "기술 개발 가속"
            },
            "📜 정부 규제 강화": {
                "options": ["법무팀 확대", "규제 준수 시스템 강화", "비즈니스 모델 전환", "로비 활동 강화", "해외 진출 모색"],
                "best": "규제 준수 시스템 강화"
            }
        }

    if st.session_state.step8_state == "pending":
        set_background_image(game_steps_info[8]["bg_image_pending"])
        show_speech(game_steps_info[8]["speech_title_pending"], game_steps_info[8]["speech_subtitle_pending"])
        st.markdown("### Step 8: 돌발 변수 등장")

        if st.session_state.current_event_name is None:
            event_name, event_info = random.choice(list(st.session_state.random_events_data.items()))
            st.session_state.current_event_name = event_name
            st.session_state.current_event_options = event_info["options"]
            st.session_state.current_event_best_strategy = event_info["best"]

        st.markdown(f"**🌀 이벤트:** {st.session_state.current_event_name}")
        selected_event_strategy = st.radio("✅ 어떤 전략으로 대응할까요?", st.session_state.current_event_options)

        if st.button("전략 확정"):
            st.session_state.step8_strategy_selected = selected_event_strategy

            if selected_event_strategy == st.session_state.current_event_best_strategy:
                st.session_state.score += 10
                st.session_state.step8_score_earned = 10
                title_prefix = "이번에도 잘 대처했군."
            else:
                st.session_state.score += 5
                st.session_state.step8_score_earned = 5
                title_prefix = "나쁘지 않은 대응이었어."

            st.session_state.selected_strategy_feedback = (
                f"{title_prefix}\n\n"
                f"{selected_event_strategy} 전략으로 {st.session_state.step8_score_earned}점 획득!"
            )

            st.session_state.step8_state = "done"
            st.rerun()

    elif st.session_state.step8_state == "done":
        set_background_image(game_steps_info[8]["bg_image_done"])
        feedback_parts = st.session_state.selected_strategy_feedback.split('\n\n', 1)
        title_bubble = game_steps_info[8]["speech_title_done"](feedback_parts[0])
        subtitle_bubble = game_steps_info[8]["speech_subtitle_done"](feedback_parts[1] if len(feedback_parts) > 1 else "", st.session_state.score)

        show_speech(title_bubble, subtitle_bubble)
        st.markdown("### Step 8: 돌발 변수 결과")
        st.success(f"전략: **{st.session_state.step8_strategy_selected}**")
        st.info(f"총 점수: **{st.session_state.score}점**")

        # Step 8 관련 세션 상태 정리
        if "step8_score_earned" in st.session_state:
            del st.session_state.step8_score_earned
        if "step8_strategy_selected" in st.session_state:
            del st.session_state.step8_strategy_selected
        st.session_state.current_event_name = None
        st.session_state.current_event_options = []
        st.session_state.current_event_best_strategy = ""
        st.session_state.selected_strategy_feedback = ""

        if st.button("다음 이벤트 ▶️"):
            st.session_state.step = 9 # 다음 스텝으로 이동 (기존 Step 8)
            st.session_state.step8_state = "pending"
            st.rerun()

# ---
## Step 9: 마케팅 또는 확장 전략 선택 (이전 Step 8)
elif st.session_state.step == 9:
    # 업종별 적합 전략 정의
    growth_strategies = {
        "💻 IT 스타트업": {
            "options": ["광고 집중 (온라인/SNS)", "글로벌 시장 진출 (초기)", "유사 기업 M&A", "가격 인하 (시장 점유율 확대)", "프리미엄 서비스 전략"],
            "best": {
                "광고 집중 (온라인/SNS)": 8,
                "글로벌 시장 진출 (초기)": 10,
                "유사 기업 M&A": 7,
                "가격 인하 (시장 점유율 확대)": 5,
                "프리미엄 서비스 전략": 6
            }
        },
        "🌱 친환경 제품": {
            "options": ["광고 집중 (환경 캠페인)", "친환경 기술 특허 확보", "대기업과 전략적 제휴", "제품 라인업 확장", "ESG 경영 강화"],
            "best": {
                "광고 집중 (환경 캠페인)": 7,
                "친환경 기술 특허 확보": 10,
                "대기업과 전략적 제휴": 8,
                "제품 라인업 확장": 6,
                "ESG 경영 강화": 9
            }
        },
        "🎮 게임 개발사": {
            "options": ["글로벌 퍼블리싱 계약", "신규 게임 장르 개발", "기존 게임 대규모 업데이트", "e스포츠 리그 개최", "유저 커뮤니티 활성화"],
            "best": {
                "글로벌 퍼블리싱 계약": 10,
                "신규 게임 장르 개발": 8,
                "기존 게임 대규모 업데이트": 7,
                "e스포츠 리그 개최": 6,
                "유저 커뮤니티 활성화": 5
            }
        },
        "👗 패션 브랜드": {
            "options": ["해외 유명 디자이너 협업", "온라인 스토어 글로벌 확장", "지속 가능한 소재 도입", "고급 라인 런칭", "가성비 중심 대중화 전략"],
            "best": {
                "해외 유명 디자이너 협업": 8,
                "온라인 스토어 글로벌 확장": 10,
                "지속 가능한 소재 도입": 7,
                "고급 라인 런칭": 9,
                "가성비 중심 대중화 전략": 5
            }
        },
        "🍔 푸드테크": {
            "options": ["신규 시장 (배달/케이터링) 확장", "R&D 투자 (대체육 등)", "물류 시스템 혁신", "프랜차이즈 확대", "건강식/맞춤형 푸드 서비스"],
            "best": {
                "신규 시장 (배달/케이터링) 확장": 8,
                "R&D 투자 (대체육 등)": 10,
                "물류 시스템 혁신": 7,
                "프랜차이즈 확대": 6,
                "건강식/맞춤형 푸드 서비스": 9
            }
        },
        "🛒 글로벌 전자상거래": {
            "options": ["신규 국가 진출", "물류 인프라 강화", "AI 기반 추천 시스템 도입", "파트너십 확장", "초개인화 쇼핑 경험 제공"],
            "best": {
                "신규 국가 진출": 10,
                "물류 인프라 강화": 8,
                "AI 기반 추천 시스템 도입": 9,
                "파트너십 확장": 7,
                "초개인화 쇼핑 경험 제공": 8
            }
        }
    }

    current_industry = st.session_state.industry
    current_growth_data = growth_strategies.get(current_industry, {"options": [], "best": {}}) # 이름을 current_growth_options에서 current_growth_data로 변경하여 혼동 방지

    if st.session_state.step9_state == "pending":
        set_background_image(game_steps_info[9]["bg_image_pending"])
        show_speech(game_steps_info[9]["speech_title_pending"], game_steps_info[9]["speech_subtitle_pending"])

        st.markdown("### Step 9: 마케팅 또는 확장 전략 선택")
        st.markdown(f"📍 **회사 업종:** {current_industry}")

        if not current_growth_data["options"]:
            st.warning("⚠️ 선택된 업종에 대한 성장 전략 데이터가 없습니다. 게임을 다시 시작해주세요.")
            if st.button("게임 다시 시작"):
                st.session_state.reset_game = True
                st.rerun()
        else:
            selected_marketing_strategy = st.radio("📈 어떤 전략으로 회사를 성장시킬까요?", current_growth_data["options"])

            if st.button("전략 확정"):
                st.session_state.step9_strategy_selected = selected_marketing_strategy
                score_to_add = current_growth_data["best"].get(selected_marketing_strategy, 5) # 기본 5점
                st.session_state.score += score_to_add
                st.session_state.step9_score_earned = score_to_add

                # 피드백 메시지 생성
                if score_to_add >= 8:
                    title_prefix = "현명한 성장 전략이었어!"
                else:
                    title_prefix = "성장을 위한 좋은 시도였어."

                st.session_state.selected_strategy_feedback = (
                    f"{title_prefix}\n\n"
                    f"{selected_marketing_strategy} 전략으로 {st.session_state.step9_score_earned}점 획득!"
                )
                
                st.session_state.step9_state = "done"
                st.rerun()

    elif st.session_state.step9_state == "done":
        set_background_image(game_steps_info[9]["bg_image_done"])
        feedback_parts = st.session_state.selected_strategy_feedback.split('\n\n', 1)
        title_bubble = game_steps_info[9]["speech_title_done"](feedback_parts[0])
        subtitle_bubble = game_steps_info[9]["speech_subtitle_done"](feedback_parts[1] if len(feedback_parts) > 1 else "", st.session_state.score)

        show_speech(title_bubble, subtitle_bubble)
        st.markdown("### Step 9: 마케팅 또는 확장 전략 결과")
        st.success(f"당신의 전략: **{st.session_state.step9_strategy_selected}**")
        st.info(f"누적 점수: **{st.session_state.score}점**")

        # Step 9 관련 세션 상태 정리
        if "step9_score_earned" in st.session_state:
            del st.session_state.step9_score_earned
        if "step9_strategy_selected" in st.session_state:
            del st.session_state.step9_strategy_selected
        st.session_state.selected_strategy_feedback = "" # 피드백 메시지 초기화

        if st.button("다음 이벤트 ▶️"):
            st.session_state.step = 10 # 다음 스텝 (리포트)으로 이동
            st.session_state.step9_state = "pending" # 다음 게임을 위해 상태 초기화
            st.rerun()

# ---
## Step 10: 연도별 리포트 + 사용자 피드백 (이전 Step 9)
elif st.session_state.step == 10:
    set_background_image(game_steps_info[10]["bg_image"]) # Step 10의 배경 이미지 설정

    final_score = st.session_state.score
    company_name = st.session_state.company_name

    # 지표 변화 계산 (간단한 예시)
    market_share = 20 + (final_score / 10) * 2 # 점수에 따라 시장 점유율 변화
    brand_reputation = 60 + (final_score / 10) * 1.5 # 점수에 따라 브랜드 평판 변화
    employee_satisfaction = 70 + (final_score / 10) # 점수에 따라 직원 만족도 변화
    revenue_growth = 10 + (final_score / 10) * 3 # 점수에 따라 매출 증가율 변화

    report_title = game_steps_info[10]["speech_title"](company_name)
    report_subtitle = game_steps_info[10]["speech_subtitle"]
    show_speech(report_title, report_subtitle)

    st.markdown(f"### Step 10: {company_name}의 3년간 리포트")
    st.write(f"CEO **{company_name}**님, 지난 3년간 당신의 경영 활동을 분석한 결과입니다.")

    st.markdown("---")
    st.markdown("#### 📊 주요 경영 지표 변화")
    st.markdown(f"- **시장 점유율**: 현재 **{market_share:.1f}%** ({'상승📈' if market_share > 20 else '하락📉' if market_share < 20 else '유지📊'})")
    st.markdown(f"- **브랜드 평판**: **{brand_reputation:.1f}점** (100점 만점, {'매우 좋음👍' if brand_reputation > 80 else '좋음😊' if brand_reputation > 60 else '보통😐' if brand_reputation > 40 else '개선 필요😟'})")
    st.markdown(f"- **직원 만족도**: **{employee_satisfaction:.1f}점** (100점 만점, {'높음😃' if employee_satisfaction > 80 else '보통🙂' if employee_satisfaction > 60 else '낮음🙁'})")
    st.markdown(f"- **매출 증가율**: 연평균 **{revenue_growth:.1f}%** (목표 대비 {'초과 달성💰' if revenue_growth > 15 else '달성💸' if revenue_growth > 10 else '미달성🔻'})")
    st.markdown("---")

    st.markdown("#### 📝 CEO의 피드백")
    if final_score >= 60:
        st.success("“정말 탁월한 경영 능력을 보여주셨습니다! 당신의 리더십 덕분에 회사는 눈부신 성장을 이루었습니다. 시장을 선도하는 기업으로 자리매김했습니다.”")
    elif final_score >= 40:
        st.info("“안정적인 성장세를 유지하며 중요한 고비들을 잘 넘겼습니다. 앞으로 더 큰 도약을 위한 발판을 마련했습니다.”")
    elif final_score >= 20:
        st.warning("“몇몇 전략에서 아쉬운 점이 있었지만, 그래도 회사를 잘 이끌어 오셨습니다. 다음 기회에는 더 신중한 판단이 필요할 것 같습니다.”")
    else:
        st.error("“경영 환경의 어려움을 극복하는 데는 한계가 있었습니다. 회사의 재정비와 새로운 전략 수립이 시급해 보입니다.”")

    if st.button("최종 평가 확인 ▶️"):
        st.session_state.step = 11 # 다음 스텝으로 이동 (최종 평가)
        st.rerun()

# ---
## Step 11: 최종 평가 및 엔딩 분기 (이전 Step 10)
elif st.session_state.step == 11:
    final_score = st.session_state.score
    company_name = st.session_state.company_name
    final_message = ""
    title_bubble = ""
    image_url = ""

    if final_score >= 60:
        title_bubble = game_steps_info[11]["speech_title_unicorn"]
        final_message = f"축하합니다, {company_name}는 당신의 뛰어난 리더십 아래 **글로벌 유니콘 기업**으로 등극했습니다! 당신은 진정한 비즈니스 영웅입니다."
        image_url = game_steps_info[11]["bg_image_good"] # 성공 이미지
    elif final_score >= 40:
        title_bubble = game_steps_info[11]["speech_title_growth"]
        final_message = f"잘하셨습니다, {company_name}는 꾸준하고 **안정적인 성장**을 이루었습니다. 시장에서 견고한 입지를 다졌습니다."
        image_url = game_steps_info[11]["bg_image_good"] # 성공 이미지
    elif final_score >= 20:
        title_bubble = game_steps_info[11]["speech_title_reorg"]
        final_message = f"아쉽게도, {company_name}는 **존폐 위기**에 처해 있습니다. 중요한 순간에 더 나은 결정을 내렸더라면 좋았을 것입니다."
        image_url = game_steps_info[11]["bg_image_bad"] # 슬픈 CEO 이미지
    else:
        title_bubble = game_steps_info[11]["speech_title_failure"]
        final_message = f"{company_name}는 당신의 경영 판단으로 인해 **회생 불능** 상태에 이르렀습니다. 다음 도전에는 더 큰 준비가 필요합니다."
        image_url = game_steps_info[11]["bg_image_bad"] # 슬픈 CEO 이미지
    
    set_background_image(image_url) # 최종 결과에 따라 배경 이미지 설정
    show_speech(title_bubble, game_steps_info[11]["speech_subtitle"](final_message)) # final_message를 subtitle로 전달

    st.markdown("### Step 11: 최종 평가")
    st.success(f"당신의 최종 점수: **{final_score}점**")
    st.markdown(f"**{final_message}**")

    st.write("---")
    st.markdown("#### 🏆 전체 플레이어 순위")
    # 점수 저장
    save_to_ranking(company_name, final_score)
    # 순위 표시
    show_full_rankings()

    if st.button("다시 시작하기"):
        st.session_state.reset_game = True
        st.rerun()
