import streamlit as st
import pandas as pd

# 페이지 설정
st.set_page_config(
    page_title="서울 연평균 기온 변화",
    page_icon="🌡️",
    layout="wide"
)

# 제목
st.title("🌡️ 서울의 연평균 기온 변화")
st.write("서울의 일별 기온 데이터를 이용해 연평균 기온이 어떻게 변해 왔는지 살펴봅니다.")

# 데이터 주소
DATA_URL = "https://raw.githubusercontent.com/greatsong/modudata/main/data/seoul.csv"

# 데이터 불러오기
@st.cache_data
def load_data():
    df = pd.read_csv(DATA_URL, encoding="utf-8-sig")

    # 날짜를 날짜 형식으로 변환
    df["날짜"] = pd.to_datetime(df["날짜"], errors="coerce")

    # 평균기온을 숫자 형식으로 변환
    df["평균기온"] = pd.to_numeric(df["평균기온"], errors="coerce")

    # 결측값 제거
    df = df.dropna(subset=["날짜", "평균기온"])

    # 연도 추출
    df["연도"] = df["날짜"].dt.year

    return df


try:
    df = load_data()

    # 연도별 평균기온 계산
    yearly_temp = (
        df.groupby("연도")["평균기온"]
        .mean()
        .reset_index()
    )

    yearly_temp.columns = ["연도", "연평균기온"]

    # 그래프
    st.subheader("📈 연도별 연평균 기온")

    st.line_chart(
        yearly_temp.set_index("연도"),
        y="연평균기온",
        x_label="연도",
        y_label="평균기온 (℃)"
    )

    # 간단한 정보
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "관측 시작 연도",
            f"{yearly_temp['연도'].min()}년"
        )

    with col2:
        st.metric(
            "최근 연도",
            f"{yearly_temp['연도'].max()}년"
        )

    with col3:
        first_temp = yearly_temp.iloc[0]["연평균기온"]
        last_temp = yearly_temp.iloc[-1]["연평균기온"]
        change = last_temp - first_temp

        st.metric(
            "처음과 최근의 차이",
            f"{change:+.1f} ℃"
        )

    st.info(
        "💡 그래프의 가로축은 연도, 세로축은 해당 연도의 평균기온입니다. "
        "해마다 변동은 있지만 장기간의 흐름을 통해 기온 변화를 확인할 수 있습니다."
    )

    # 데이터 보기
    with st.expander("📋 연평균 기온 데이터 보기"):
        display_df = yearly_temp.copy()
        display_df["연평균기온"] = display_df["연평균기온"].round(1)
        st.dataframe(
            display_df,
            use_container_width=True,
            hide_index=True
        )

except Exception as e:
    st.error("데이터를 불러오는 중 문제가 발생했습니다.")
    st.write(f"오류 내용: {e}")
