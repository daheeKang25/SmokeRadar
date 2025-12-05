import streamlit as st
import pandas as pd
import time
import folium
from streamlit_folium import st_folium

# 설정
st.set_page_config(page_title="스모크레이더",page_icon='😮‍💨', layout="wide")
st.title("Smoke Radar")
st.caption("데이터과학 미니프로젝트 프로토타입")

# 데이터 불러오기
if 'df' not in st.session_state:
    try:
        st.session_state.df = pd.read_csv("pages/dataset.csv")
    except FileNotFoundError:
        st.error("데이터 파일을 찾을 수 없습니다.")
        st.stop()
df = st.session_state.df

# 사이드바 설정
st.sidebar.header("현재 위치 설정")
selected_gu = st.sidebar.selectbox("지역 선택", ["성동구", "용산구", "서초구","성북구", "강남구", "중구", "종로구"])

# 지도 중심 좌표 설정
if selected_gu == "성동구":
    map_center = [37.555, 127.045]
    zoom_level = 14
    filtered_df = df[(df['id'] >= 1) & (df['id'] <= 80)]
elif selected_gu == "용산구":
    map_center = [37.532, 126.990]
    zoom_level = 14
    filtered_df = df[(df['id'] >= 81) & (df['id'] <= 156)]
else:
    st.sidebar.warning("현재는 성동구와 용산구만 선택가능합니다.")


# 메인 화면 구성
col1, col2 = st.columns([3, 1])

with col1:
    st.subheader(f"{selected_gu} 흡연구역 지도")
    
    # 지도 생성
    m = folium.Map(location=map_center, zoom_start=zoom_level)

    # 마커 표시
    for idx, row in filtered_df.iterrows():
        # 상태에 따른 색상 결정
        if row['status'] == 1:
            marker_color = 'red'    # 금연구역
            status_text = "금연구역"
            icon_type = 'ban'
        elif row['reliability'] < 70:
            marker_color = 'orange' # 보류
            status_text = "확인필요(보류)"
            icon_type = 'question'
        else:
            marker_color = 'green'  # 정상 운영
            status_text = "이용가능"
            icon_type = 'check'

        # 팝업
        popup_html = f"""
        <div style="width:200px">
            <b>{row['name']}</b><br>
            상태: {status_text}<br>
            신뢰도: {row['reliability']}점<br>
            <hr>
            <small>{row['description']}</small>
            {f'<br><b style="color:red">과태료: {row["penalty"]:,}원</b>' if row['penalty'] > 0 else ''}
        </div>
        """

        # 지도에 마커 추가
        folium.Marker(
            location=[row['latitude'], row['longitude']],
            popup=folium.Popup(popup_html, max_width=300),
            tooltip=row['name'],
            icon=folium.Icon(color=marker_color, icon=icon_type, prefix='fa')
        ).add_to(m)

    # 지도 표시
    st_folium(m, width="100%", height=500)

with col2:
    st.subheader("신뢰도 점수 피드백")
    st.write("폐쇄가 의심되는 경우 제보해주세요.")
    
    # 제보할 장소 선택
    target_place = st.selectbox("장소 선택", filtered_df['name'])
    
    # 선택된 장소의 현재 정보 가져오기
    target_index = df[df['name'] == target_place].index[0]
    current_score = df.loc[target_index, 'reliability']
    
    st.metric(label="현재 신뢰도 점수", value=f"{current_score}점")

    # 신고 버튼 처리
    if st.button("폐쇄/없음 신고 (-10점)"):
        # 점수 차감
        st.session_state.df.loc[target_index, 'reliability'] -= 10
        new_score = st.session_state.df.loc[target_index, 'reliability']

        # 파일 저장
        st.session_state.df.to_csv("dataset.csv", index=False)
        
        # 알림 메시지
        st.toast(f"※반영 완료! {target_place}의 현재 신뢰도 점수: {new_score}점※")
        
        if new_score < 70 and current_score >= 70:
            st.toast("※신뢰도 하락으로 상태가 **'보류'**로 변경됩니다.※")
        
        time.sleep(1.5)
        st.rerun()

    st.info("""
    신뢰도 점수란?
            
    사용자들이 폐쇄 의심 제보를 하면, 신뢰도 점수가 실시간으로 차감됩니다.
            
    점수가 **70점 미만**으로 떨어지면, 해당 구역은 **보류** 상태가 됩니다.
    """)
