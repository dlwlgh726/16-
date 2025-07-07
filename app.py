import streamlit as st
import pandas as pd
import os

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

# ✅ Step 10 최종 평가
elif st.session_state.step == 10:
    final_score = st.session_state.score
    company_name = st.session_state.company_name

    if final_score >= 60:
        title_bubble = "“글로벌 유니콘 기업 달성!”"
        final_message = f"축하합니다, {company_name}는 당신의 뛰어난 리더십 아래 **글로벌 유니콘 기업**으로 등극했습니다! 당신은 진정한 비즈니스 영웅입니다."
        image_url = "https://raw.githubusercontent.com/dddowobbb/16-1/main/talking%20ceo.png"
    elif final_score >= 40:
        title_bubble = "“안정적 성장!”"
        final_message = f"잘하셨습니다, {company_name}는 꾸준하고 **안정적인 성장**을 이루었습니다. 시장에서 견고한 입지를 다졌습니다."
        image_url = "https://raw.githubusercontent.com/dddowobbb/16-1/main/talking%20ceo.png"
    elif final_score >= 20:
        title_bubble = "“재정비의 기회!”"
        final_message = f"아쉽게도, {company_name}는 **존폐 위기**에 처해 있습니다. 중요한 순간에 더 나은 결정을 내렸더라면 좋았을 것입니다."
        image_url = "https://raw.githubusercontent.com/dddowobbb/16-1/main/sad_ceo.png"
    else:
        title_bubble = "“혹독한 실패...”"
        final_message = f"{company_name}는 당신의 경영 판단으로 인해 **회생 불능** 상태에 이르렀습니다. 다음 도전에는 더 큰 준비가 필요합니다."
        image_url = "https://raw.githubusercontent.com/dddowobbb/16-1/main/sad_ceo.png"

    show_speech(title_bubble, final_message, image_url)

    st.markdown("### Step 10: 최종 평가")
    st.success(f"당신의 최종 점수: **{final_score}점**")
    st.markdown(f"**{final_message}**")

    # ✅ 점수 저장 후 전체 순위 출력
    save_to_ranking(company_name, final_score)
    show_full_rankings()

    if st.button("다시 시작하기"):
        st.session_state.reset_game = True
        st.rerun()
