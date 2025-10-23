"""
Module de Styling Premium pour Sensations by Arda J
Solution ultra-fixe avec injection de fond prioritaire
"""

import streamlit as st
import base64
from pathlib import Path

# =============================================================================
# CONSTANTES
# =============================================================================

COLORS = {
    'primary': '#D4AF37',
    'secondary': '#000000',
    'background': '#0A0A0A',
    'text': '#FFFFFF',
    'text_secondary': '#E5E5E5',
    'text_muted': '#D1D1D1',
    'accent': '#FFD700',
    'hover': '#F0C040',
    'success': '#10B981',
    'error': '#EF4444',
    'warning': '#F59E0B',
    'info': '#60A5FA',
    'card_bg': 'rgba(20, 20, 20, 0.90)',
    'card_border': 'rgba(212, 175, 55, 0.4)',
    'shadow_gold': 'rgba(212, 175, 55, 0.5)',
}

LOGO_FILENAME = "logo.jpg"
BACKGROUND_FILENAME = "background.jpg"

# =============================================================================
# FONCTIONS
# =============================================================================

@st.cache_data
def get_img_as_base64(file_path: str) -> tuple:
    """Charge une image et la convertit en base64"""
    try:
        path = Path(file_path)
        if not path.exists():
            path = Path(__file__).parent.parent / file_path
        
        if path.exists():
            with open(path, "rb") as f:
                data = f.read()
            
            ext = path.suffix.replace('.', '')
            if ext == 'jpg':
                ext = 'jpeg'
                
            return base64.b64encode(data).decode(), ext
    except:
        pass
    
    return None, None

def inject_background_layer():
    """Injecte le fond en premier avant tout le reste"""
    bg_b64, bg_ext = get_img_as_base64(f"assets/{BACKGROUND_FILENAME}")
    
    if bg_b64:
        st.markdown(f"""
        <div id="background-layer" style="
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            z-index: -1000;
            background-image: url('data:image/{bg_ext};base64,{bg_b64}');
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;
        "></div>
        <div id="overlay-layer" style="
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            z-index: -999;
            background: rgba(0, 0, 0, 0.65);
            backdrop-filter: blur(1px);
        "></div>
        """, unsafe_allow_html=True)
        return True
    else:
        # Fond de secours en dégradé
        st.markdown(f"""
        <div id="background-layer" style="
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            z-index: -1000;
            background: linear-gradient(135deg, #0a0a0a 0%, #1a1410 50%, #0a0a0a 100%);
        "></div>
        <div id="overlay-layer" style="
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            z-index: -999;
            background: rgba(0, 0, 0, 0.3);
        "></div>
        """, unsafe_allow_html=True)
        return False

def load_custom_styling():
    """Charge le CSS premium - SANS gérer le fond (déjà fait par inject_background_layer)"""
    
    custom_css = f"""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700;900&family=Montserrat:wght@300;400;600;700&display=swap');
        
        /* ========================================
           ANIMATIONS
        ======================================== */
        
        @keyframes fadeIn {{
            from {{ opacity: 0; transform: translateY(20px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}
        
        @keyframes slideDown {{
            from {{ transform: translateY(-100px); opacity: 0; }}
            to {{ transform: translateY(0); opacity: 1; }}
        }}
        
        @keyframes pulse {{
            0%, 100% {{ transform: scale(1); }}
            50% {{ transform: scale(1.08); }}
        }}
        
        @keyframes shimmer {{
            0% {{ background-position: -1000px 0; }}
            100% {{ background-position: 1000px 0; }}
        }}
        
        @keyframes glow {{
            0%, 100% {{ box-shadow: 0 0 20px {COLORS['shadow_gold']}, 0 0 40px {COLORS['shadow_gold']}; }}
            50% {{ box-shadow: 0 0 30px {COLORS['shadow_gold']}, 0 0 60px {COLORS['shadow_gold']}; }}
        }}

        /* ========================================
           CONFIGURATION GÉNÉRALE - TRANSPARENCE TOTALE
        ======================================== */
        
        * {{
            font-family: 'Montserrat', sans-serif;
        }}
        
        [data-testid="stHeader"] {{
            display: none !important;
        }}
        
        footer {{
            visibility: hidden;
        }}
        
        /* CRITICAL - Force tous les conteneurs à être transparents */
        html, body, #root,
        [data-testid="stApp"],
        [data-testid="stAppViewContainer"],
        [data-testid="stAppViewContainer"] > section,
        .main,
        .block-container,
        [data-testid="stVerticalBlock"],
        [data-testid="stVerticalBlock"] > div,
        section[data-testid="stSidebar"],
        .element-container {{
            background: transparent !important;
            background-color: transparent !important;
        }}
        
        /* Assurer que le contenu est au-dessus du fond */
        .main, .main > div {{
            position: relative;
            z-index: 1;
        }}
        
        [data-testid="stVerticalBlock"] > div {{
            animation: fadeIn 0.6s ease-out;
        }}

        /* ========================================
           TYPOGRAPHIE - CONTRASTE MAXIMUM
        ======================================== */
        
        h1 {{
            font-family: 'Playfair Display', serif !important;
            color: {COLORS['primary']} !important;
            font-weight: 900 !important;
            font-size: 3rem !important;
            text-shadow: 
                2px 2px 4px rgba(0, 0, 0, 1), 
                0 0 20px {COLORS['shadow_gold']},
                0 0 40px rgba(0, 0, 0, 0.9);
            letter-spacing: 2px;
            margin-bottom: 1rem !important;
        }}
        
        h2 {{
            font-family: 'Playfair Display', serif !important;
            color: {COLORS['primary']} !important;
            font-weight: 700 !important;
            font-size: 2rem !important;
            text-shadow: 
                2px 2px 4px rgba(0, 0, 0, 1),
                0 0 15px rgba(212, 175, 55, 0.4);
            letter-spacing: 1px;
        }}
        
        h3 {{
            font-family: 'Playfair Display', serif !important;
            color: {COLORS['accent']} !important;
            font-weight: 700 !important;
            font-size: 1.5rem !important;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 1);
        }}
        
        h4, h5, h6 {{
            color: {COLORS['accent']} !important;
            font-weight: 600 !important;
            text-shadow: 1px 1px 3px rgba(0, 0, 0, 1);
        }}
        
        /* Force le blanc pur sur TOUT le texte */
        p, span, div, li, label,
        .st-emotion-cache-16txtl3,
        .st-emotion-cache-q8sbsg, 
        .st-emotion-cache-ax1dkn,
        [data-testid="stMarkdown"],
        [data-testid="stMarkdown"] *,
        [data-testid="stMarkdownContainer"],
        [data-testid="stMarkdownContainer"] *,
        [data-testid="stText"],
        [data-testid="stCaption"] {{
            color: {COLORS['text']} !important;
            text-shadow: 1px 1px 3px rgba(0, 0, 0, 1);
        }}

        /* ========================================
           HEADER PREMIUM
        ======================================== */
        
        .custom-header {{
            background: linear-gradient(135deg, 
                rgba(10, 10, 10, 0.95) 0%, 
                rgba(26, 20, 16, 0.95) 50%,
                rgba(10, 10, 10, 0.95) 100%) !important;
            border: 2px solid {COLORS['primary']};
            border-radius: 20px;
            padding: 1.5rem 2rem;
            margin-bottom: 2rem;
            box-shadow: 
                0 10px 40px rgba(0, 0, 0, 0.9),
                0 0 80px {COLORS['shadow_gold']},
                inset 0 1px 0 rgba(255, 255, 255, 0.1);
            animation: slideDown 0.7s cubic-bezier(0.68, -0.55, 0.265, 1.55);
            position: relative;
            overflow: hidden;
            z-index: 100;
        }}
        
        .custom-header::before {{
            content: '';
            position: absolute;
            top: -50%;
            left: -50%;
            width: 200%;
            height: 200%;
            background: linear-gradient(
                45deg,
                transparent 30%,
                rgba(212, 175, 55, 0.1) 50%,
                transparent 70%
            );
            animation: shimmer 3s infinite;
        }}
        
        .logo-section {{
            display: flex;
            align-items: center;
            gap: 20px;
            position: relative;
            z-index: 1;
        }}
        
        .logo-section img {{
            height: 70px;
            width: 70px;
            border-radius: 50%;
            border: 3px solid {COLORS['primary']};
            box-shadow: 
                0 0 20px {COLORS['shadow_gold']},
                0 0 40px {COLORS['shadow_gold']},
                0 8px 20px rgba(0, 0, 0, 0.9);
            transition: all 0.3s ease;
        }}
        
        .logo-section img:hover {{
            transform: scale(1.05);
            box-shadow: 
                0 0 30px {COLORS['accent']},
                0 0 60px {COLORS['accent']},
                0 10px 30px rgba(0, 0, 0, 1);
        }}
        
        .logo-section h1 {{
            font-size: 2.5rem !important;
            background: linear-gradient(135deg, {COLORS['primary']} 0%, {COLORS['accent']} 50%, {COLORS['primary']} 100%);
            background-size: 200% 200%;
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            animation: shimmer 4s infinite;
            margin: 0 !important;
            letter-spacing: 3px;
            filter: drop-shadow(2px 2px 4px rgba(0, 0, 0, 1));
        }}
        
        .nav-buttons {{
            display: flex;
            justify-content: flex-end;
            gap: 12px;
            position: relative;
            z-index: 1;
        }}

        /* ========================================
           BOUTONS PREMIUM
        ======================================== */
        
        .stButton button {{
            background: linear-gradient(135deg, {COLORS['primary']} 0%, {COLORS['accent']} 100%) !important;
            color: {COLORS['secondary']} !important;
            border: none !important;
            border-radius: 12px;
            font-weight: 700;
            font-size: 0.95rem;
            padding: 0.7rem 1.5rem;
            transition: all 0.4s cubic-bezier(0.68, -0.55, 0.265, 1.55);
            box-shadow: 0 4px 15px rgba(212, 175, 55, 0.4);
            text-transform: uppercase;
            letter-spacing: 1.5px;
            position: relative;
            overflow: hidden;
        }}
        
        .stButton button::before {{
            content: '';
            position: absolute;
            top: 50%;
            left: 50%;
            width: 0;
            height: 0;
            border-radius: 50%;
            background: rgba(255, 255, 255, 0.3);
            transform: translate(-50%, -50%);
            transition: width 0.6s, height 0.6s;
        }}
        
        .stButton button:hover {{
            transform: translateY(-3px) scale(1.05);
            box-shadow: 0 8px 25px rgba(212, 175, 55, 0.6);
            background: linear-gradient(135deg, {COLORS['accent']} 0%, {COLORS['primary']} 100%) !important;
        }}
        
        .stButton button:hover::before {{
            width: 300px;
            height: 300px;
        }}
        
        .nav-buttons .stButton button {{
            padding: 0.6rem 1rem;
            font-size: 0.85rem;
        }}
        
        .stButton button[kind="primary"] {{
            background: linear-gradient(135deg, {COLORS['success']} 0%, #059669 100%) !important;
            animation: glow 2s infinite;
        }}

        /* ========================================
           BADGE PANIER
        ======================================== */
        
        .cart-badge-wrapper {{
            position: relative;
            display: inline-block;
        }}
        
        .cart-badge {{
            position: absolute;
            top: -12px;
            right: -12px;
            background: linear-gradient(135deg, {COLORS['error']} 0%, #DC2626 100%);
            color: white !important;
            border-radius: 50%;
            width: 28px;
            height: 28px;
            display: flex;
            justify-content: center;
            align-items: center;
            font-size: 0.75rem;
            font-weight: 900;
            box-shadow: 0 3px 10px rgba(239, 68, 68, 0.5);
            animation: pulse 2s infinite;
            border: 2px solid {COLORS['background']};
            z-index: 10;
        }}

        /* ========================================
           CARTES PRODUIT
        ======================================== */
        
        [data-testid="column"] {{
            background: transparent !important;
        }}
        
        [data-testid="column"] > div {{
            background: {COLORS['card_bg']} !important;
            border: 1px solid {COLORS['card_border']};
            border-radius: 20px;
            padding: 1.5rem;
            transition: all 0.4s ease;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.7);
            backdrop-filter: blur(10px);
            position: relative;
            overflow: hidden;
        }}
        
        [data-testid="column"] > div:hover {{
            transform: translateY(-10px) scale(1.02);
            border-color: {COLORS['primary']};
            box-shadow: 0 15px 50px rgba(0, 0, 0, 0.9), 0 0 60px {COLORS['shadow_gold']};
        }}
        
        [data-testid="stImage"] img {{
            border-radius: 15px;
            transition: all 0.4s ease;
            box-shadow: 0 5px 20px rgba(0, 0, 0, 0.7);
        }}
        
        [data-testid="stImage"]:hover img {{
            transform: scale(1.05);
            box-shadow: 0 10px 40px {COLORS['shadow_gold']};
        }}

        /* ========================================
           INPUTS
        ======================================== */
        
        .stTextInput input, .stTextArea textarea, 
        .stNumberInput input, .stSelectbox select {{
            background: rgba(255, 255, 255, 0.08) !important;
            border: 2px solid {COLORS['card_border']} !important;
            border-radius: 12px !important;
            color: {COLORS['text']} !important;
            padding: 0.8rem 1rem !important;
            transition: all 0.3s ease !important;
        }}
        
        .stTextInput input:focus, .stTextArea textarea:focus {{
            border-color: {COLORS['primary']} !important;
            box-shadow: 0 0 20px {COLORS['shadow_gold']} !important;
            background: rgba(255, 255, 255, 0.12) !important;
        }}

        /* ========================================
           ALERTES
        ======================================== */
        
        [data-testid="stAlert"] {{
            background: rgba(0, 0, 0, 0.7) !important;
            border-left: 4px solid;
            border-radius: 12px;
            padding: 1rem 1.5rem;
            backdrop-filter: blur(10px);
        }}
        
        [data-testid="stAlert"] p {{
            color: {COLORS['text']} !important;
            text-shadow: 1px 1px 3px rgba(0, 0, 0, 1);
            font-weight: 500;
        }}

        /* ========================================
           DIVIDERS
        ======================================== */
        
        hr {{
            border: none;
            height: 2px;
            background: linear-gradient(90deg, transparent 0%, {COLORS['primary']} 50%, transparent 100%);
            margin: 2rem 0;
            box-shadow: 0 0 10px {COLORS['shadow_gold']};
        }}

        /* ========================================
           SCROLLBAR
        ======================================== */
        
        ::-webkit-scrollbar {{
            width: 12px;
        }}
        
        ::-webkit-scrollbar-track {{
            background: rgba(0, 0, 0, 0.3);
        }}
        
        ::-webkit-scrollbar-thumb {{
            background: linear-gradient(180deg, {COLORS['primary']} 0%, {COLORS['accent']} 100%);
            border-radius: 10px;
        }}

        /* ========================================
           RESPONSIVE
        ======================================== */
        
        @media (max-width: 768px) {{
            .custom-header {{
                padding: 1rem;
            }}
            
            .logo-section h1 {{
                font-size: 1.8rem !important;
            }}
            
            .logo-section img {{
                height: 50px;
                width: 50px;
            }}
            
            h1 {{
                font-size: 2rem !important;
            }}
        }}
        
    </style>
    """
    
    st.markdown(custom_css, unsafe_allow_html=True)

# =============================================================================
# HEADER
# =============================================================================

def build_header():
    """Construit le header - INJECTE LE FOND EN PREMIER"""
    
    # ÉTAPE 1: Injecter le fond AVANT tout
    inject_background_layer()
    
    # ÉTAPE 2: Charger le logo
    logo_b64, logo_ext = get_img_as_base64(f"assets/{LOGO_FILENAME}")
    cart_count = sum(item['quantity'] for item in st.session_state.cart.values())

    # ÉTAPE 3: Construire le header
    with st.container():
        st.markdown('<div class="custom-header">', unsafe_allow_html=True)
        
        col1, col2 = st.columns([1.5, 1])
        
        with col1:
            logo_html = f'<img src="data:image/{logo_ext};base64,{logo_b64}" alt="Logo">' if logo_b64 else '<div style="width:70px;height:70px;background:linear-gradient(135deg,#D4AF37,#FFD700);border-radius:50%;"></div>'
            st.markdown(
                f"""
                <div class="logo-section">
                    {logo_html}
                    <h1>✨ Sensations by Arda J</h1>
                </div>
                """,
                unsafe_allow_html=True
            )
        
        with col2:
            st.markdown('<div class="nav-buttons">', unsafe_allow_html=True)
            cols_nav = st.columns(4)
            
            with cols_nav[0]:
                if st.button("🏠 Accueil", key="nav_home", use_container_width=True):
                    st.switch_page("app.py")
            
            with cols_nav[1]:
                st.markdown('<div class="cart-badge-wrapper">', unsafe_allow_html=True)
                if st.button("🛒 Panier", key="nav_cart", use_container_width=True):
                    st.switch_page("pages/2_Panier.py")
                if cart_count > 0:
                    st.markdown(f'<span class="cart-badge">{cart_count}</span>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)

            with cols_nav[2]:
                if st.button("📦 Commander", key="nav_checkout", use_container_width=True):
                    st.switch_page("pages/3_Checkout.py")
            
            with cols_nav[3]:
                if st.session_state.get('authenticated', False):
                    if st.button("📊 Admin", key="nav_admin", use_container_width=True):
                        st.switch_page("pages/admin_4_Dashboard.py")
                else:
                    if st.button("🔐 Connexion", key="nav_login", use_container_width=True):
                        st.switch_page("pages/admin_login.py")

            st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)