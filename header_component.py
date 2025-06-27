import streamlit as st
import base64

def get_base64_of_bin_file(filepath):
    with open(filepath, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

def logout():
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.rerun()

def render_header():
    logo_base64 = get_base64_of_bin_file("LOGO_RDV_AZUL.png")

    st.markdown("""
        <style>
        .header-container {
            background-color: #0F2A4D;
            padding: 10px 20px;
            border-radius: 8px;
            margin-bottom: 20px;
        }
        .header-img {
            display: flex;
            align-items: center;
            justify-content: center;
        }
        .logout-button button {
            background-color: white !important;
            color: #0F2A4D !important;
            font-weight: bold;
            border-radius: 8px;
            padding: 6px 18px;
            border: none;
            cursor: pointer;
        }
        .logout-button button:hover {
            background-color: #e0e0e0 !important;
        }
        </style>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([5, 1])
    with col1:
        st.markdown(f"""
            <div class="header-container header-img">
                <img src="data:image/png;base64,{logo_base64}" alt="Logo RDV" style="height: 60px;" />
            </div>
        """, unsafe_allow_html=True)

    with col2:
        with st.container():
            st.markdown('<div class="logout-button">', unsafe_allow_html=True)
            if st.button("🚪 Sair"):
                logout()
            st.markdown('</div>', unsafe_allow_html=True)
