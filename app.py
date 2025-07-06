# ✅ 경영 시뮬레이션 게임 전체 리팩토링 코드 (점수 다양화 제외)
import streamlit as st
import random

# ✅ 세션 상태 초기화 함수

def initialize_session_state():
    defaults = {
        "step": 0,
        "industry": "",
        "industry_confirmed": False,
        "company_name": "",
        "situation": "",
        "options": [],
        "selected_strategy": "",
        "score": 0,
        "crisis_situation": "",
        "crisis_options": [],
        "best_crisis_strategies": {},
        "event_8": None,
        "event_8_options": [],
        "event_8_best": "",
        "event8_score": 0,
        "step7_done": False,
        "step8_done": False,
        "step3_score_earned": 0,
        "step5_score_earned": 0,
        "step7_score": 0,
        "step3_strategy": "",
        "step5_strategy": "",
        "step7_strategy": "",
        "step8_strategy": ""
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

initialize_session_state()

# ✅ 공통 스타일 적용
st.markdown("""
<style>
body {
    background-color: #1a1a1a;
    color: #ffffff;
}
h1, h2, h3, h4, h5, h6, label, p, span, div {
    color: inherit;
}
div[data-baseweb="select"] {
    background-color: #ffffff;
    color: #000000;
}
div[data-baseweb="select"] * {
    color: #000000;
    fill: #000000;
}
button p {
    color: #000000;
    font-weight: bold;
}
.container {
    position: relative;
    width: 100%;
    height: 100vh;
    overflow: hidden;
    margin: 0;
    padding: 0;
    background-color: #1a1a1a;
}
.bg-image {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100vh;
    object-fit: cover;
    z-index: 0;
}
.speech-bubble {
    position: absolute;
    bottom: 8vh;
    left: 50%;
    transform: translateX(-50%);
    width: 90%;
    max-width: 500px;
    background: rgba(255, 255, 255, 0.1);
    padding: 20px 25px;
    border-radius: 25px;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.4);
    text-align: center;
    z-index: 1;
    backdrop-filter: blur(8px);
}
.speech-title {
    font-size: 1.4rem;
    font-weight: bold;
    color: #ffffff;
}
.speech-sub {
    margin-top: 10px;
    font-size: 1rem;
    color: #f0f0f0;
}
</style>
""", unsafe_allow_html=True)

# ✅ 말풍선 렌더링 함수
def show_speech(title: str, subtitle: str, image_url: str):
    st.markdown(f"""
    <div class=\"container\">
        <img src=\"{image_url}\" class=\"bg-image\">
        <div class=\"speech-bubble\">
            <div class=\"speech-title\">{title}</div>
            <div class=\"speech-sub\">{subtitle}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ✅ 단계별 로직
if st.session_state.step == 0:
    show_speech("“환영합니다!”", "게임을 시작해봅시다.", "https://raw.githubusercontent.com/dddowobbb/16-1/main/talking%20ceo.png")
    if st.button("게임 시작 ▶️"):
        st.session_state.step = 1
        st.rerun()

elif st.session_state.step == 1:
    st.markdown("## 업종 선택")
    options = ["IT", "푸드", "패션", "게임"]
    industry = st.selectbox("업종을 선택하세요", options)
    if st.button("업종 확정"):
        st.session_state.industry = industry
        st.session_state.industry_confirmed = True
        st.session_state.step = 2
        st.rerun()

elif st.session_state.step == 2:
    name = st.text_input("회사 이름을 지어보세요")
    if st.button("확정"):
        st.session_state.company_name = name
        st.session_state.step = 3
        st.rerun()

elif st.session_state.step == 3:
    situation = "📉 주요 제품 매출 급감"
    strategies = ["제품 리뉴얼", "광고 캠페인", "시장 조사"]
    best = "제품 리뉴얼"
    st.session_state.situation = situation
    strategy = st.radio("전략 선택:", strategies)
    if st.button("확정"):
        st.session_state.step3_strategy = strategy
        score = 10 if strategy == best else 5
        st.session_state.step3_score_earned = score
        st.session_state.score += score
        st.session_state.step = 4
        st.rerun()

elif st.session_state.step == 4:
    st.success(f"전략 결과: {st.session_state.step3_strategy} → {st.session_state.step3_score_earned}점")
    if st.button("다음 ▶️"):
        st.session_state.step = 5
        st.rerun()

elif st.session_state.step == 5:
    show_speech("“국가적 위기 발생!”", "경제, 정치, 국제 환경이 급변하고 있어. 대응 전략이 필요해.", "https://raw.githubusercontent.com/dddowobbb/16-1/main/talking%20ceo.png")

    crisis_situations = {
        "📉 한국 외환시장 급변 (원화 가치 급락)": ["환 헤지 강화", "수출 확대", "정부와 협력", "외환 보유 확대", "위기 커뮤니케이션"],
        "🇺🇸 미 연준의 기준금리 인상": ["대출 축소", "내수 집중 전략", "고금리 대비 자산 조정", "비용 구조 개선", "긴축 경영"],
        "🗳️ 정치적 불확실성 증가": ["리스크 분산 경영", "정치 모니터링 강화", "내부 의사결정 체계 정비", "단기 전략 전환", "위기 대비 태스크포스 운영"],
        "🇺🇸 트럼프 대통령 재취임": ["미국 중심 전략 강화", "공급망 재편", "관세 대비 물류 최적화", "현지 생산 강화", "미국 투자 확대"],
        "🛃 주요 국가의 관세 인상 정책": ["무역 파트너 다변화", "현지 생산 확대", "비관세 수출 전략", "신시장 개척", "가격 재설정"]
    }

    if not st.session_state.crisis_situation:
        st.session_state.crisis_situation, st.session_state.crisis_options = random.choice(list(crisis_situations.items()))

    st.markdown("### Step 5: 국가적 위기 대응")
    st.markdown(f"**상황:** {st.session_state.crisis_situation}")
    strategy = st.radio("🧠 대응 전략을 선택하세요:", st.session_state.crisis_options)

    best_strategies = {
        "📉 한국 외환시장 급변 (원화 가치 급락)": "환 헤지 강화",
        "🇺🇸 미 연준의 기준금리 인상": "고금리 대비 자산 조정",
        "🗳️ 정치적 불확실성 증가": "리스크 분산 경영",
        "🇺🇸 트럼프 대통령 재취임": "공급망 재편",
        "🛃 주요 국가의 관세 인상 정책": "무역 파트너 다변화"
    }

    if st.button("전략 확정"):
        st.session_state.step5_strategy = strategy
        score = 10 if strategy == best_strategies.get(st.session_state.crisis_situation) else 5
        st.session_state.step5_score_earned = score
        st.session_state.score += score
        st.session_state.crisis_situation = ""
        st.session_state.crisis_options = []
        st.session_state.step = 6
        st.rerun()

elif st.session_state.step == 6:
    st.success(f"위기 대응: {st.session_state.step5_strategy} → {st.session_state.step5_score_earned}점")
    if st.button("다음 ▶️"):
        st.session_state.step = 7
        st.rerun()

elif st.session_state.step == 7:
    options = {"조직문화 혁신": 10, "복지 강화": 7, "기다린다": 2}
    strategy = st.radio("내부 문제 대응:", list(options.keys()))
    if st.button("확정"):
        st.session_state.step7_strategy = strategy
        score = options[strategy]
        st.session_state.step7_score = score
        st.session_state.score += score
        st.session_state.step = 8
        st.rerun()

elif st.session_state.step == 8:
    event = "🚀 경쟁사 혁신 제품 발표"
    options = ["기술 개발 가속", "마케팅 강화", "가격 인하"]
    best = "기술 개발 가속"
    strategy = st.radio("돌발 이벤트 대응:", options)
    if st.button("확정"):
        st.session_state.step8_strategy = strategy
        score = 10 if strategy == best else 5
        st.session_state.event8_score = score
        st.session_state.score += score
        st.session_state.step = 9
        st.rerun()

elif st.session_state.step == 9:
    score = st.session_state.score
    if score >= 40:
        msg = "최고의 경영자입니다!"
    elif score >= 25:
        msg = "좋은 성과입니다."
    else:
        msg = "다음엔 더 잘할 수 있어요."
    st.success(f"총 점수: {score}점 — {msg}")
    if st.button("다시 시작"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()
