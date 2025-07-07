import streamlit as st
import pandas as pd
import os
import random
import time

# ---
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
        "step7_score_earned": 0,
        "step8_score_earned": 0,
        "step9_score_earned": 0,
        "step3_strategy_selected": "",
        "step5_strategy_selected": "",
        "step7_strategy_selected": "",
        "step8_strategy_selected": "",
        "step9_strategy_selected": "",
        "current_event_name": None,
        "current_event_options": [],
        "current_event_best_strategy": "",
        "step7_state": "pending",
        "step8_state": "pending",
        "step9_state": "pending",
        "background_image_url": "https://images.unsplash.com/photo-1552664730-d307ca884978?q=80&w=2070&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D" # 기본 배경 이미지 URL
    }

    if st.session_state.get("reset_game", False):
        for key in list(st.session_state.keys()):
            del st.session_state.key = value

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
    # st.success(f"점수가 성공적으로 기록되었습니다: {company_name}, {final_score}점") # 최종 단계에서만 표시

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
# ✅ 공통 CSS 스타일 (전체 화면 배경 및 말풍선 UI 고정)
st.markdown(f"""
<style>
/* 기본 앱 컨테이너 설정 */
html, body, [data-testid="stApp"] {
    margin: 0;
    padding: 0;
    height: 100%;
    width: 100%;
    overflow: hidden; /* 전체 앱 스크롤 방지 */
    background-image: url('{st.session_state.background_image_url}'); /* 배경 이미지 설정 */
    background-size: cover; /* 화면에 꽉 채우도록 */
    background-repeat: no-repeat; /* 반복 방지 */
    color: #ffffff; /* 기본 텍스트 색상 */
}

/* Streamlit 메인 콘텐츠 컨테이너 설정 */
.main .block-container {
    padding-top: 0.5rem; /* 여백 최소화 */
    padding-bottom: 0.5rem; /* 여백 최소화 */
    height: 100vh; /* 전체 뷰포트 높이 사용, 스크롤 방지 */
    overflow-y: auto; /* 필요 시 내부 콘텐츠 스크롤 허용 (배경은 고정) */
    overflow-x: hidden;
    display: flex; /* 내부 요소 중앙 정렬을 위해 flexbox 사용 */
    flex-direction: column; /* 세로 정렬 */
    justify-content: center; /* 세로 중앙 정렬 */
    align-items: center; /* 가로 중앙 정렬 */
    width: 100%; /* 전체 너비 사용 */
    background-color: rgba(0, 0, 0, 0.3); /* 배경 이미지 위에 약간 어두운 투명 배경 추가 (선택 사항) */
}

/* 텍스트 중앙 정렬 */
.stMarkdown, .stText, .stAlert, .stSuccess, .stInfo, .stWarning, .stError,
h1, h2, h3, h4, h5, h6, label, p, .stRadio > label > div, .stCheckbox > label > div,
div
