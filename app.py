import streamlit as st
import pandas as pd
import os
import random
import time

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
# ✅ 공통 CSS 스타일 (한 번만 정의)
st.markdown("""
<style>
body { background-color: #1a1a1a; color: #ffffff; }
h1, h2, h3, h4, h5, h6, label, p, span, div { color: inherit; }
div[data-baseweb="select"] { background-color: #ffffff; color: #000000; }
div[data-baseweb="select"] * { color: #000000; fill: #000000; }
button p { color: #000000; font-weight: bold; }

/* Streamlit 앱 전체에 배경 이미지 적용 */
.stApp {
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
    min-height: 100vh; /* 화면 전체 높이 사용 */
    display: flex;
    flex-direction: column;
    justify-content: flex-start; /* 콘텐츠가 위에서부터 쌓이도록 */
    align-items: center; /* 가로 중앙 정렬 (필요시) */
    padding-top: 20px; /* 상단 여백 추가 (배경 이미지와 겹치지 않도록) */
    position: relative; /* 자식 absolute 요소의 기준점 */
}

.speech-bubble {
    /* 이 말풍선은 Streamlit 콘텐츠 흐름 내에 배치되며, 위치는 relative */
    position: relative;
    margin-bottom: 20px; /* 아래 위젯과의 간격 */
    width: 90%; max-width: 500px; background: rgba(255, 255, 255, 0.1);
    padding: 20px 25px; border-radius: 25px; box-shadow: 0 4px 15px rgba(0, 0, 0, 0.4);
    text-align: center; z-index: 1; backdrop-filter: blur(8px);
    color: #ffffff; /* 텍스트 색상 명시 */
}
.speech-title { font-size: 1.4rem; font-weight: bold; color: #ffffff; }
.speech-sub { margin-top: 10px; font-size: 1rem; color: #f0f0f0; }

/* Streamlit 기본 위젯 배경색 투명화 (배경 이미지가 보이도록) */
div.stSelectbox > div, div.stRadio > label, div.stTextInput > div > div {
    background-color: rgba(0, 0, 0, 0.5) !important; /* 위젯 배경을 반투명 검정으로 */
    border-radius: 10px;
    padding: 5px 10px;
}

/* 라디오 버튼 텍스트 색상 */
div.stRadio > label > div[data-testid="stMarkdownContainer"] p {
    color: #ffffff !important;
}

/* 텍스트 입력창 텍스트 색상 */
div.stTextInput input {
    color: #ffffff !important;
}

/* 버튼 스타일 */
.stButton>button {
    background-color: #4CAF50; /* 버튼 배경색 */
    color: white; /* 버튼 텍스트 색상 */
    padding: 10px 20px;
    border: none;
    border-radius: 5px;
    cursor: pointer;
    font-weight: bold;
    margin-top: 15px; /* 버튼 상단 여백 */
    transition: background-color 0.3s ease;
}

.stButton>button:hover {
    background-color: #45a049;
}
</style>
""", unsafe_allow_html=True)


# ✅ 배경 이미지를 설정하는 함수 (show_speech 대체)
def set_background_image_style(image_url: str):
    st.markdown(f"""
    <style>
    .stApp {{
        background-image: url("{image_url}");
    }}
    </style>
    """, unsafe_allow_html=True)

# ✅ 말풍선 내용을 표시하는 함수
def display_speech_bubble(title: str, subtitle: str):
    st.markdown(f"""
    <div class="speech-bubble">
        <div class="speech-title">{title}</div>
        <div class="speech-sub">{subtitle}</div>
    </div>
    """, unsafe_allow_html=True)


# ---
## Step 0: 시작 안내
if st.session_state.step == 0:
    set_background_image_style("https://raw.githubusercontent.com/dddowobbb/16-1/main/talking%20ceo.png")
    display_speech_bubble("“환영합니다!”", "마지막에 전체 순위가 집계되니, 집중해서 신중하게 플레이해 주세요.")
    st.markdown("### 경영 시뮬레이션 게임에 오신 것을 환영합니다!")
    st.markdown("이 게임에서는 회사를 창업하고 성장시키는 과정에서 다양한 결정을 내려야 합니다. 회사를 성공적으로 운영해보세요!")
    if st.button("게임 시작 ▶️"):
        st.session_state.step = 1
        st.rerun()

# ---
## Step 1: 업종 선택
elif st.session_state.step == 1:
    set_background_image_style("https://raw.githubusercontent.com/dddowobbb/16-1/main/talking%20ceo.png")
    if not st.session_state.industry_confirmed:
        display_speech_bubble("“좋아, 이제 우리가 어떤 산업에 뛰어들지 결정할 시간이군.”", "어떤 분야에서 승부할지, 네 선택을 보여줘.")
    else:
        display_speech_bubble(f"“{st.session_state.industry}... 흥미로운 선택이군.”", "다음 단계로 가볼까?")

    st.markdown("### Step 1: 회사 분야 선택")
    industries = ["💻 IT 스타트업", "🌱 친환경 제품", "🎮 게임 개발사", "👗 패션 브랜드", "🍔 푸드테크", "🛒 글로벌 전자상거래"]

    if not st.session_state.industry_confirmed:
        selected = st.selectbox("회사 업종을 선택해주세요", industries)
        if st.button("업종 확정"):
            st.session_state.industry = selected
            st.session_state.industry_confirmed = True
            st.session_state.step = 2
            st.rerun()
    else:
        st.success(f"✅ 선택된 업종: **{st.session_state.industry}**")
        if st.button("다음 ▶️"):
            st.session_state.step = 2
            st.rerun()

# ---
## Step 2: 회사 이름 입력
elif st.session_state.step == 2:
    set_background_image_style("https://raw.githubusercontent.com/dddowobbb/16-1/main/talking%20ceo.png")
    if not st.session_state.company_name:
        display_speech_bubble("“이제 회사를 설립할 시간이야.”", "멋진 회사 이름을 지어보자!")
    else:
        display_speech_bubble(f"“{st.session_state.company_name}... 멋진 이름이군!”", "이제 다음 단계로 넘어가자.")

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
    set_background_image_style("https://raw.githubusercontent.com/dlwlgh726/16-/main/badevent.png")
    display_speech_bubble("“예기치 못한 사건 발생!”", "상황에 적절한 전략을 선택해 회사를 지켜내자.")

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
    score_earned_this_step = st.session_state.get("step3_score_earned", 0)
    selected_strategy_for_feedback = st.session_state.get("step3_strategy_selected", "선택 없음")

    if score_earned_this_step == 10:
        title = "“훌륭한 판단이었어!”"
        subtitle = st.session_state.selected_strategy_feedback
    else:
        title = "“음... 더 나은 전략도 있었을 거야.”"
        subtitle = st.session_state.selected_strategy_feedback

    set_background_image_style("https://raw.githubusercontent.com/dddowobbb/16-1/main/talking%20ceo.png")
    display_speech_bubble(title, subtitle)

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
    set_background_image_style("https://raw.githubusercontent.com/dlwlgh726/16-/main/badevent.png")
    display_speech_bubble("“국가적 위기 발생!”", "경제, 정치, 국제 환경이 급변하고 있어. 대응 전략이 필요해.")

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
    score_earned_this_step = st.session_state.get("step5_score_earned", 0)
    selected_strategy_for_feedback = st.session_state.get("step5_strategy_selected", "선택 없음")

    if score_earned_this_step == 10:
        title = "“최고의 경영자군!”"
        subtitle = st.session_state.selected_strategy_feedback + f" 총 점수: {st.session_state.score}점"
    else:
        title = "“괜찮은 성과지만 아직 성장 가능성이 보여.”"
        subtitle = st.session_state.selected_strategy_feedback + f" 총 점수: {st.session_state.score}점"

    set_background_image_style("https://raw.githubusercontent.com/dddowobbb/16-1/main/talking%20ceo.png")
    display_speech_bubble(title, subtitle)
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
        set_background_image_style("https://raw.githubusercontent.com/dlwlgh726/16-/main/KakaoTalk_Photo_2025-07-03-16-19-06 005.png")
        display_speech_bubble("“요즘 직원들 분위기가 심상치 않아...”", "사기 저하, 인사 갈등, 생산성 저하 문제가 보고됐어. 어떻게 대응할까?")
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
                f"“{title_prefix}”\n\n"
                f"{selected_org_strategy} 전략에 따른 점수: {st.session_state.step7_score_earned}점"
            )

            st.session_state.step7_state = "done"
            st.rerun()

    elif st.session_state.step7_state == "done":
        # 피드백 화면
        feedback_parts = st.session_state.selected_strategy_feedback.split('\n\n', 1)
        title_bubble = feedback_parts[0] if len(feedback_parts) > 0 else "결과"
        subtitle_bubble = feedback_parts[1] if len(feedback_parts) > 1 else ""
        subtitle_bubble += f" (누적 점수: {st.session_state.score}점)"

        set_background_image_style("https://raw.githubusercontent.com/dddowobbb/16-1/main/talking%20ceo.png")
        display_speech_bubble(title_bubble, subtitle_bubble)

        st.markdown("### Step 7: 내부 문제 해결 결과")
        st.success(f"당신의 전략: **{st.session_state.step7_strategy_selected}**")
        st.info(f"누적 점수: **{st.session_state.score}점**")

        # Step 7 관련 세션 상태 정리
        if "step7_score_earned" in st.session_state:
            del st.session_state.step7_score_earned
        if "step7_strategy_selected" in st.session_state:
