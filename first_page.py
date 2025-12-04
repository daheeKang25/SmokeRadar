import streamlit as st

# 페이지 설정
st.set_page_config(page_title="스모크레이더 - Smoke Radar",page_icon='😮‍💨', layout="wide")

# style
st.markdown("""
<style>
    .stApp {
        background-image: url('https://velog.velcdn.com/images/ljs7463/post/c6c7dae4-ec27-4213-9b28-d538a59162aa/image.png');
        background-size: cover;
        background-position: center;
        font-family: 'Noto-Sans', sans-serif;
    }

    /* 타이틀 디자인 */
    .main-title-container {
        text-align: center;
        padding-top: 80px;
        padding-bottom: 40px;
    }
    
    .sub-title {
        color: #00a9b0;
        font-size: 2rem;
        font-weight: 700;
        text-shadow: -1px 0px #0e2a47, 0px 1px #0e2a47, 1px 0px #0e2a47, 0px -1px #0e2a47;
        margin-bottom: 10px;
    }
    
    .main-title {
        color: #0e2a47;
        font-size: 3.5rem;
        font-weight: 800;
        text-shadow: -1px 0px #00a9b0, 0px 1px #00a9b0, 1px 0px #00a9b0, 0px -1px #00a9b0;
        margin: 0;
    }

    .description {
        margin-top: 20px;
        font-size: 1.5rem;
        color: #333;
        font-weight: 700;
        background-color: rgba(255, 255, 255, 0.6);
        display: inline-block;
        padding: 10px 20px;
        border-radius: 20px;
        box-shadow: 0px 0px 5px #444
    }
            
    .maintext {
        font-size: 1rem;
        color: green;
        text-align: center;
        text-shadow: -0.2px 0px green, 0px 0.2px green, 0.2px 0px green, 0px -0.2px green;
        margin-top: 50px;
        }

    .caption {
        font-size: 1rem;
        color: blue;
        text-align: center;
        margin-top: 10px;
        }
            
    div[data-testid="stVerticalBlockBorderWrapper"] {
        background-color: white;
        padding: 10px;
        border-radius: 15px;
        max-width: 1200px;
        height: 100px;
        margin: 0 auto;
        border: none;
    }
            
    div.stButton > button {
        background-color: #00a9b0;
        color: white;
        border: none;
        border-radius: 8px;
        height: 100%;
        width: 200px;
        font-size: 3rem;
        box-shadow: 0px 0px 5px #444
        transition: background 0.3s;
    }

    div.stButton > button:hover {
        background-color: #008c93;
        color: white;
        border: none;
    }
    
    header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# 3. 화면 구성
st.markdown("""
    <div class="main-title-container">
        <div class="sub-title">데이터 기반 실시간 흡연구역 정보 제공 서비스</div>
        <div class="main-title">Smoke Radar</div>
        <div class="description">
            아래 지역 중 원하시는 지역을 선택하면<br>
            해당 지역의 흡연구역 정보를 볼 수 있습니다.
        </div>
        <div class="caption">※서울시 성동구를 선택해주세요!
        </div>
        <div class="maintext">
            한양여대 빅데이터과<br>
            데이터과학 미니 프로젝트<br>
            비흡연자 팀
        </div>
    </div>
""", unsafe_allow_html=True)

# 기능구현 - 중앙정렬하기위해 컬럼을 사용함
col_space_1, col_main, col_space_2 = st.columns([2, 2.5, 2])

with col_main:
    with st.container(border=True):
        # 하얀색 박스 안에 들어갈 내용
        c1, c2, c3 = st.columns([1, 1, 1], gap="medium")
        
        with c1:
            si_do = st.selectbox("시/도 선택", ["서울시", "경기도"], label_visibility="collapsed")
            
        with c2:
            gu_gun = st.selectbox("구/군 선택", ["성동구", "성북구", "서초구","용산구", "강남구", "중구", "종로구"], label_visibility="collapsed")
            
        with c3:
            # 검색 버튼
            search_click = st.button("검색")

# 검색 결과
if search_click:
    st.success(f"'{si_do} {gu_gun}' 지역의 흡연구역을 검색합니다!")
    st.switch_page("pages/app.py")