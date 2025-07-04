import streamlit as st
import urllib.parse

st.set_page_config(
    page_title="Clicker",
    page_icon="🦾",
    layout="centered",
)

st.markdown("""
<style>
@keyframes click-animation {
    0% { transform: scale(1); opacity: 1; }
    100% { transform: scale(3); opacity: 0; }
}  
    
.click-animation {
    position: absolute;
    animation: click-animation 0.8s ease-out;
    color: #4CAF50;
    font-weight: bold;
    pointer-events: none;
}

/* Стили для основной кнопки */
div[data-testid="stButton"]:has(button:contains("Кликнуть")) button {
    font-size: 24px !important;
    padding: 25px 35px !important;
    border-radius: 15px !important;
    background: linear-gradient(45deg, #4CAF50, #45a049) !important;
    transition: all 0.2s ease !important;
}

div[data-testid="st Button"]:has(button:contains("Кликнуть")) button:hover {
    transform: scale(1.05);
    box-shadow: 0 5px 15px rgba(76,175,80,0.4);
}
            
/* Стили для кнопки сброса */
div[data-testid="stButton"]:has(button:contains("Сбросить")) button {
    background: linear-gradient(45deg, #ff4444, #cc0000) !important;
}
</style>
""", unsafe_allow_html=True)

def get_telegram_user():
    params = st.query_params
    try:
        name = urllib.parse.unquote(params.get("name", ["Anonymous"])[0]) # Декодируем имя
        user_id = params.get("user_id", [None])[0]
        auth_date = params.get("auth_date", [None])[0]
        return {
            'name': name,
            'user_id': user_id,
            'auth_date': auth_date
        }
    except (KeyError, IndexError): # Обработка отсутствующих параметров
        st.error("Ошибка получения данных пользователя. Проверьте URL.")
        return {'name': 'Anonymous', 'user_id': 12345, 'auth_date': None}


if 'clicks' not in st.session_state:
    st.session_state.update({
        'clicks': 0,
        'animations': [],
        'last_click': None
    })

def handle_click():
    st.session_state.clicks += 1
    st.session_state.animations.append(f'click-{st.session_state.clicks}')
    st.session_state.last_click = st.session_state.clicks

def reset_clicks():
    st.session_state.clicks = 0
    st.session_state.animations = []

user_data = get_telegram_user()

st.title("Clicker")
with st.expander("Профиль пользователя", expanded=True):
    col_info = st.columns([1, 4])
    with col_info[0]:
        st.image("https://ecolak.ru/images/smaili/harakteristiki_i_sertifikaty_antiseptika_dlya_drevesiny.jpg")
    with col_info[1]:
        st.write(f"Имя: {user_data['name']}")
        if user_data['user_id']:
            st.write(f"ID: {user_data['user_id']}")

if st.session_state.animations:
    with st.empty().container():
        for anim_id in st.session_state.animations:
            st.markdown(
                f'<div class="click-animation" id="{anim_id}">+1</div>',
                unsafe_allow_html=True
            )
    st.session_state.animations = []

col_stats, _, _ = st.columns([2, 1, 1])
with col_stats:
    st.metric("Всeго кликов", st.session_state.clicks)

col_buttons = st.columns([3, 1])
with col_buttons[0]:
    st.button("Кликнуть!", use_container_width=True, on_click=handle_click)

with col_buttons[1]:
    st.button("Сбросить", use_container_width=True, on_click=reset_clicks, type="secondary")