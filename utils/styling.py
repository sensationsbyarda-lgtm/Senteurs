"""
Module de Styling Premium pour Sensations by Arda J
Version avec inputs fond blanc et texte noir
(Header : Accueil (sombre) + Menu déroulant (clair) avec Panier à l'intérieur)
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
    'text': "#FFFCFC",
    'text_secondary': "#EAE2E2",
    'text_muted': "#E7D7D7",
    'accent': '#FFD700',
    'hover': '#F0C040',
    'success': '#10B981',
    'error': '#EF4444',
    'warning': '#F59E0B',
    'info': '#60A5FA',
    'card_bg': 'rgba(20, 20, 20, 0.95)',
    'card_border': 'rgba(212, 175, 55, 0.5)',
    'shadow_gold': 'rgba(212, 175, 55, 0.6)',
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
            background: rgba(0, 0, 0, 0.75);
            backdrop-filter: blur(2px);
        "></div>
        """, unsafe_allow_html=True)
        return True
    else:
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
            background: rgba(0, 0, 0, 0.4);
        "></div>
        """, unsafe_allow_html=True)
        return False

def load_custom_styling():
    """Charge le CSS premium corrigé"""
    
    custom_css = f"""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700;900&family=Montserrat:wght@300;400;600;700;800;900&display=swap');
        
        /* RÉDUCTION DES BARRES NOIRES */
        .main .block-container {{
            padding-top: 0.5rem !important;
            padding-bottom: 0.5rem !important;
            padding-left: 1.5rem !important;
            padding-right: 1.5rem !important;
            max-width: 100% !important;
        }}
        
        section[data-testid="stAppViewContainer"] > .main {{
            padding-top: 0 !important;
        }}
        
        /* ANIMATIONS */
        @keyframes fadeIn {{
            from {{ opacity: 0; transform: translateY(20px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}
        
        @keyframes slideDown {{
            from {{ transform: translateY(-50px); opacity: 0; }}
            to {{ transform: translateY(0); opacity: 1; }}
        }}
        
        @keyframes pulse {{
            0%, 100% {{ transform: scale(1); }}
            50% {{ transform: scale(1.05); }}
        }}
        
        @keyframes shimmer {{
            0% {{ background-position: -1000px 0; }}
            100% {{ background-position: 1000px 0; }}
        }}
        
        @keyframes glow {{
            0%, 100% {{ box-shadow: 0 0 20px {COLORS['shadow_gold']}, 0 0 40px {COLORS['shadow_gold']}; }}
            50% {{ box-shadow: 0 0 30px {COLORS['shadow_gold']}, 0 0 60px {COLORS['shadow_gold']}; }}
        }}

        /* CONFIGURATION GÉNÉRALE */
        * {{
            font-family: 'Montserrat', sans-serif;
        }}
        
        [data-testid="stHeader"] {{
            display: none !important;
        }}
        
        footer {{
            visibility: hidden;
        }}
        
        html, body, #root,
        [data-testid="stApp"],
        [data-testid="stAppViewContainer"],
        [data-testid="stAppViewContainer"] > section,
        .main,
        [data-testid="stVerticalBlock"],
        [data-testid="stVerticalBlock"] > div,
        section[data-testid="stSidebar"],
        .element-container {{
            background: transparent !important;
            background-color: transparent !important;
        }}
        
        .main, .main > div {{
            position: relative;
            z-index: 1;
        }}
        
        [data-testid="stVerticalBlock"] > div {{
            animation: fadeIn 0.6s ease-out;
        }}

        /* TYPOGRAPHIE */
        h1 {{
            font-family: 'Playfair Display', serif !important;
            color: {COLORS['primary']} !important;
            font-weight: 900 !important;
            font-size: 2.5rem !important;
            text-shadow: 3px 3px 6px rgba(0, 0, 0, 1), 0 0 30px {COLORS['shadow_gold']}, 0 0 50px rgba(0, 0, 0, 0.9);
            letter-spacing: 2px;
            margin-bottom: 0.8rem !important;
        }}
        
        h2 {{
            font-family: 'Playfair Display', serif !important;
            color: {COLORS['primary']} !important;
            font-weight: 700 !important;
            font-size: 1.8rem !important;
            text-shadow: 2px 2px 5px rgba(0, 0, 0, 1), 0 0 20px rgba(212, 175, 55, 0.5);
            letter-spacing: 1px;
        }}
        
        h3 {{
            font-family: 'Playfair Display', serif !important;
            color: {COLORS['accent']} !important;
            font-weight: 700 !important;
            font-size: 1.3rem !important;
            text-shadow: 2px 2px 5px rgba(0, 0, 0, 1);
        }}
        
        p, li, span {{
            color: {COLORS['text_secondary']} !important;
            text-shadow: 1px 1px 3px rgba(0, 0, 0, 0.9);
            line-height: 1.7;
        }}
        
        strong {{
            color: {COLORS['accent']} !important;
            font-weight: 800 !important;
        }}

        /* HEADER COMPACT ET ALIGNÉ */
        .custom-header {{
            background: linear-gradient(135deg, rgba(15, 15, 15, 0.98) 0%, rgba(5, 5, 5, 0.99) 100%);
            border: 2px solid {COLORS['card_border']};
            border-radius: 18px;
            padding: 1rem 1.5rem !important;
            margin-bottom: 1rem !important;
            margin-top: 0 !important;
            box-shadow: 0 10px 50px rgba(0, 0, 0, 0.9), 0 0 100px {COLORS['shadow_gold']};
            backdrop-filter: blur(20px);
            animation: slideDown 0.6s ease-out;
        }}
        
        .logo-section {{
            display: flex;
            align-items: center;
            gap: 1rem;
        }}
        
        .logo-section img {{
            height: 55px;
            width: 55px;
            border-radius: 50%;
            border: 3px solid {COLORS['primary']};
            box-shadow: 0 0 40px {COLORS['shadow_gold']};
            object-fit: cover;
            transition: all 0.3s ease;
        }}
        
        .logo-section img:hover {{
            transform: rotate(360deg) scale(1.15);
            box-shadow: 0 0 60px {COLORS['accent']};
        }}
        
        .logo-section h1 {{
            margin: 0 !important;
            font-size: 1.8rem !important;
            background: linear-gradient(135deg, {COLORS['primary']} 0%, {COLORS['accent']} 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            text-shadow: none !important;
            filter: drop-shadow(2px 2px 4px rgba(0, 0, 0, 1));
        }}
        
        .nav-buttons {{
            display: flex;
            gap: 0.6rem;
            align-items: center;
            justify-content: flex-end;
            flex-wrap: nowrap;
        }}

        /* ========================================
           BOUTONS PREMIUM (Version Améliorée)
        ======================================== */
        
        /* Style par défaut (pour "Accueil" et autres boutons) */
        .stButton button {{
            /* -- Fond et Bordure -- */
            background: linear-gradient(135deg, rgba(25, 25, 25, 0.98) 0%, rgba(10, 10, 10, 1) 100%) !important;
            border: 2px solid {COLORS['card_border']} !important;
            border-radius: 12px !important;
            
            /* -- Typographie et Espacement -- */
            color: {COLORS['text']} !important;
            padding: 0.7rem 1.3rem !important; 
            font-weight: 700 !important;
            font-size: 0.9rem !important;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 1) !important;
            letter-spacing: 0.5px !important;

            /* -- Effets et Positionnement -- */
            box-shadow: 0 5px 20px rgba(0, 0, 0, 0.6), inset 0 1px 0 rgba(255, 255, 255, 0.1) !important;
            cursor: pointer !important;
            position: relative !important;
            overflow: hidden !important;
            
            /* -- Transition LISSE -- */
            transition: 
                transform 0.3s cubic-bezier(0.4, 0, 0.2, 1),
                box-shadow 0.3s cubic-bezier(0.4, 0, 0.2, 1),
                border-color 0.3s ease,
                background 0.3s ease !important;
            
            width: 100%; 
        }}
        
        .stButton button::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: linear-gradient(110deg, transparent 30%, rgba(212, 175, 55, 0.4) 50%, transparent 70%);
            transform: translateX(-100%); 
            transition: transform 0.6s cubic-bezier(0.23, 1, 0.32, 1); 
        }}
        
        .stButton button:hover::before {{
            transform: translateX(100%); 
        }}
        
        .stButton button:hover {{
            transform: translateY(-3px) !important;
            border-color: {COLORS['primary']} !important; 
            box-shadow: 0 7px 25px {COLORS['shadow_gold']}, 0 0 30px rgba(212, 175, 55, 0.3), inset 0 1px 0 rgba(255, 255, 255, 0.15) !important;
            background: linear-gradient(135deg, rgba(35, 35, 35, 1) 0%, rgba(20, 20, 20, 1) 100%) !important;
        }}
        
        .stButton button:active {{
            transform: translateY(-1px) scale(0.98) !important;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.5), inset 0 1px 1px rgba(0, 0, 0, 0.2) !important;
        }}
        
        /* --- Style pour le bouton Popover "Menu" (style clair) --- */
        /* Cible le bouton qui ouvre le popover, mais UNIQUEMENT dans le .nav-buttons */
        .nav-buttons [data-testid="stPopover"] > button {{
            background: linear-gradient(135deg, #FFFFFF 0%, #F0F0F0 100%) !important;
            color: #1a1a1a !important; /* Texte noir */
            border: 2px solid #FFFFFF !important;
            text-shadow: none !important;
            box-shadow: 0 4px 15px rgba(255, 255, 255, 0.2), inset 0 -1px 0 rgba(0, 0, 0, 0.1) !important;
        }}
        
        .nav-buttons [data-testid="stPopover"] > button:hover {{
            background: linear-gradient(135deg, #F0F0F0 0%, #FFFFFF 100%) !important;
            border-color: #FFFFFF !important;
            color: #000000 !important;
            box-shadow: 0 6px 20px rgba(255, 255, 255, 0.3), inset 0 -1px 0 rgba(0, 0, 0, 0.1) !important;
            transform: translateY(-2px) !important;
        }}
        
        /* Enlève l'effet shimmer du bouton popover */
        .nav-buttons [data-testid="stPopover"] > button::before {{
            background: none !important;
        }}
        /* --- FIN DU STYLE POPOVER --- */
        
        
        /* ========================================
           BOUTON PRIMAIRE (ex: "Ajouter")
        ======================================== */
        
        @keyframes pulse-green {{
            0% {{ box-shadow: 0 6px 25px rgba(16, 185, 129, 0.5), inset 0 1px 0 rgba(255, 255, 255, 0.2); }}
            50% {{ box-shadow: 0 8px 35px rgba(16, 185, 129, 0.8), inset 0 1px 0 rgba(255, 255, 255, 0.2); }}
            100% {{ box-shadow: 0 6px 25px rgba(16, 185, 129, 0.5), inset 0 1px 0 rgba(255, 255, 255, 0.2); }}
        }}

        .stButton button[kind="primary"] {{
            background: linear-gradient(135deg, {COLORS['success']} 0%, #059669 100%) !important;
            border-color: {COLORS['success']} !important;
            color: white !important;
            font-weight: 800 !important;
            text-shadow: 1px 1px 3px rgba(0, 0, 0, 0.5) !important;
            box-shadow: 0 6px 25px rgba(16, 185, 129, 0.5), inset 0 1px 0 rgba(255, 255, 255, 0.2) !important;
            animation: pulse-green 2.5s infinite cubic-bezier(0.4, 0, 0.2, 1);
        }}
        
        .stButton button[kind="primary"]:hover {{
            background: linear-gradient(135deg, #059669 0%, #047857 100%) !important;
            box-shadow: 0 10px 40px rgba(16, 185, 129, 0.7), 0 0 60px rgba(16, 185, 129, 0.4) !important;
            transform: translateY(-4px) scale(1.02) !important;
            animation-play-state: paused; 
        }}
        
        /* ========================================
           BOUTON DÉSACTIVÉ
        ======================================== */

        .stButton button:disabled {{
            opacity: 0.4 !important;
            cursor: not-allowed !important;
            transform: none !important;
            background: rgba(50, 50, 50, 0.5) !important;
            border-color: rgba(100, 100, 100, 0.5) !important;
            box-shadow: none !important;
            animation: none !important; 
        }}

        .stButton button:disabled:hover {{
            transform: none !important;
            box-shadow: none !important;
        }}
        
        /* BADGE PANIER (NON UTILISÉ SUR LE HEADER, MAIS CONSERVÉ) */
        .cart-badge-wrapper {{
            position: relative;
            display: inline-block;
        }}
        
        .cart-badge {{
            position: absolute;
            top: -10px;
            right: -10px;
            background: linear-gradient(135deg, {COLORS['error']} 0%, #DC2626 100%);
            color: white !important;
            border-radius: 50%;
            width: 26px;
            height: 26px;
            display: flex;
            justify-content: center;
            align-items: center;
            font-size: 0.75rem;
            font-weight: 900;
            box-shadow: 0 4px 15px rgba(239, 68, 68, 0.7), 0 0 30px rgba(239, 68, 68, 0.4);
            animation: pulse 2s infinite;
            border: 2px solid {COLORS['background']};
            z-index: 10;
            text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.8);
        }}

        /* CARTES PRODUIT */
        [data-testid="column"] {{
            background: transparent !important;
            padding: 0.5rem !important;
        }}
        
        [data-testid="column"] > div {{
            background: {COLORS['card_bg']} !important;
            border: 2px solid {COLORS['card_border']};
            border-radius: 20px;
            padding: 1.2rem;
            transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
            box-shadow: 0 8px 35px rgba(0, 0, 0, 0.8);
            backdrop-filter: blur(15px);
            position: relative;
            overflow: hidden;
            height: 100%;
            display: flex;
            flex-direction: column;
        }}
        
        [data-testid="column"] > div:hover {{
            transform: translateY(-8px);
            border-color: {COLORS['primary']};
            box-shadow: 0 15px 50px rgba(0, 0, 0, 0.9), 0 0 70px {COLORS['shadow_gold']}, inset 0 0 35px rgba(212, 175, 55, 0.1);
        }}
        
        [data-testid="stImage"] {{
            margin-bottom: 1rem !important;
            border-radius: 16px;
            overflow: hidden;
            position: relative;
            aspect-ratio: 4/3;
            background: linear-gradient(135deg, rgba(0, 0, 0, 0.5), rgba(0, 0, 0, 0.3));
        }}
        
        [data-testid="stImage"] img {{
            border-radius: 16px;
            transition: all 0.45s ease;
            box-shadow: 0 5px 20px rgba(0, 0, 0, 0.8);
            object-fit: cover;
            width: 100%;
            height: 100%;
        }}
        
        [data-testid="stImage"]:hover img {{
            transform: scale(1.08);
            box-shadow: 0 10px 40px {COLORS['shadow_gold']};
        }}
        
        [data-testid="column"] strong {{
            display: block;
            color: {COLORS['accent']} !important;
            font-size: 1.05rem !important;
            font-weight: 800 !important;
            margin: 0.6rem 0 0.4rem 0;
            text-shadow: 2px 2px 5px rgba(0, 0, 0, 1), 0 0 15px rgba(255, 215, 0, 0.3);
            line-height: 1.3;
        }}
        
        /* PRIX RÉDUIT */
        .price-container {{
            background: linear-gradient(135deg, rgba(212, 175, 55, 0.2) 0%, rgba(255, 215, 0, 0.2) 100%);
            border: 2px solid {COLORS['card_border']};
            border-radius: 14px;
            padding: 0.6rem 0.9rem;
            margin: 0.6rem 0;
            text-align: center;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3), inset 0 0 20px rgba(212, 175, 55, 0.1);
        }}
        
        .price-value {{
            font-size: 1.1rem !important;
            font-weight: 800 !important;
            color: {COLORS['primary']} !important;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 1), 0 0 20px {COLORS['shadow_gold']} !important;
            letter-spacing: 0.5px;
            display: block;
            font-family: 'Montserrat', sans-serif !important;
        }}
        
        [data-testid="stDialog"] .price-value {{
            font-size: 1.8rem !important;
        }}

        /* BADGES STOCK */
        .out-of-stock {{
            background: linear-gradient(135deg, {COLORS['error']} 0%, #DC2626 100%);
            color: white !important;
            padding: 0.5rem 1rem;
            border-radius: 20px;
            font-size: 0.85rem;
            font-weight: 800;
            display: inline-block;
            box-shadow: 0 3px 12px rgba(239, 68, 68, 0.5);
            text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.6);
            letter-spacing: 0.3px;
            border: 2px solid rgba(239, 68, 68, 0.3);
        }}
        
        .low-stock {{
            background: linear-gradient(135deg, {COLORS['warning']} 0%, #F97316 100%);
            color: white !important;
            padding: 0.5rem 1rem;
            border-radius: 20px;
            font-size: 0.85rem;
            font-weight: 800;
            display: inline-block;
            box-shadow: 0 3px 12px rgba(245, 158, 11, 0.5);
            text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.6);
            letter-spacing: 0.3px;
            border: 2px solid rgba(245, 158, 11, 0.3);
            animation: pulse 2s infinite;
        }}
        
        .in-stock {{
            background: linear-gradient(135deg, {COLORS['success']} 0%, #059669 100%);
            color: white !important;
            padding: 0.5rem 1rem;
            border-radius: 20px;
            font-size: 0.85rem;
            font-weight: 800;
            display: inline-block;
            box-shadow: 0 3px 12px rgba(16, 185, 129, 0.5);
            text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.6);
            letter-spacing: 0.3px;
            border: 2px solid rgba(16, 185, 129, 0.3);
        }}

        /* INPUTS - FOND BLANC ET TEXTE NOIR FONCÉ */
        .stTextInput input, .stTextArea textarea, 
        .stNumberInput input, .stSelectbox select {{
            background: rgba(255, 255, 255, 0.95) !important;
            border: 2px solid {COLORS['card_border']} !important;
            border-radius: 12px !important;
            color: #1a1a1a !important;
            padding: 0.8rem 1rem !important;
            transition: all 0.3s ease !important;
            font-size: 0.95rem !important;
            font-weight: 600 !important;
            text-shadow: none !important;
        }}
        
        .stTextInput input:focus, .stTextArea textarea:focus,
        .stNumberInput input:focus, .stSelectbox select:focus {{
            border-color: {COLORS['primary']} !important;
            box-shadow: 0 0 0 3px rgba(212, 175, 55, 0.3), 0 0 25px {COLORS['shadow_gold']} !important;
            background: rgba(255, 255, 255, 1) !important;
            outline: none !important;
        }}
        
        .stTextInput input::placeholder, .stTextArea textarea::placeholder {{
            color: rgba(26, 26, 26, 0.5) !important;
            text-shadow: none !important;
        }}
        
        label {{
            color: {COLORS['accent']} !important;
            font-weight: 700 !important;
            font-size: 0.95rem !important;
            margin-bottom: 0.6rem !important;
            text-shadow: 1px 1px 3px rgba(0, 0, 0, 1);
        }}

        /* ALERTES */
        [data-testid="stAlert"] {{
            background: rgba(0, 0, 0, 0.85) !important;
            border-left: 5px solid;
            border-radius: 12px;
            padding: 1rem 1.5rem;
            backdrop-filter: blur(15px);
            box-shadow: 0 5px 25px rgba(0, 0, 0, 0.6);
        }}
        
        [data-testid="stAlert"] p {{
            color: {COLORS['text']} !important;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 1);
            font-weight: 600;
        }}

        /* DIVIDERS */
        hr {{
            border: none;
            height: 1px;
            background: linear-gradient(90deg, transparent 0%, {COLORS['primary']} 50%, transparent 100%);
            margin: 1.5rem 0;
            box-shadow: 0 0 10px {COLORS['shadow_gold']};
        }}

        /* SCROLLBAR */
        ::-webkit-scrollbar {{
            width: 12px;
            height: 12px;
        }}
        
        ::-webkit-scrollbar-track {{
            background: rgba(0, 0, 0, 0.5);
            border-radius: 10px;
        }}
        
        ::-webkit-scrollbar-thumb {{
            background: linear-gradient(180deg, {COLORS['primary']} 0%, {COLORS['accent']} 100%);
            border-radius: 10px;
            border: 2px solid rgba(0, 0, 0, 0.5);
        }}
        
        ::-webkit-scrollbar-thumb:hover {{
            background: linear-gradient(180deg, {COLORS['accent']} 0%, {COLORS['hover']} 100%);
        }}

        /* CONTENEURS */
        [data-testid="stExpander"] {{
            background: {COLORS['card_bg']} !important;
            border: 2px solid {COLORS['card_border']} !important;
            border-radius: 14px !important;
            backdrop-filter: blur(15px);
        }}
        
        [data-testid="stExpander"] summary {{
            color: {COLORS['accent']} !important;
            font-weight: 700 !important;
        }}
        
        .stCaption, [data-testid="stCaptionContainer"] {{
            color: rgba(255, 255, 255, 0.85) !important;
            font-size: 0.85rem !important;
            text-shadow: 1px 1px 3px rgba(0, 0, 0, 0.8);
            font-weight: 500 !important;
        }}

        /* --- STYLE POUR LE MENU DÉROULANT (POPOVER) --- */
        [data-testid="stPopoverContent"] {{
            background: {COLORS['card_bg']} !important;
            border: 2px solid {COLORS['card_border']} !important;
            border-radius: 14px !important;
            backdrop-filter: blur(15px);
            box-shadow: 0 8px 35px rgba(0, 0, 0, 0.8);
        }}
        
        /* Boutons à l'intérieur du popover (style "menu item") */
        [data-testid="stPopoverContent"] .stButton button {{
            background: transparent !important;
            border: none !important;
            box-shadow: none !important;
            text-align: left;
            color: {COLORS['text_secondary']} !important;
            font-weight: 600 !important;
        }}
        
        [data-testid="stPopoverContent"] .stButton button:hover {{
            background: rgba(212, 175, 55, 0.2) !important; /* Léger fond or au survol */
            color: {COLORS['primary']} !important;
            transform: none !important;
            box-shadow: none !important;
        }}
        /* --- FIN DU STYLE POPOVER --- */

        /* RESPONSIVE */
        @media (max-width: 768px) {{
            .custom-header {{
                padding: 0.8rem !important;
            }}
            
            .logo-section {{
                flex-direction: column;
                text-align: center;
                gap: 0.6rem;
            }}
            
            .logo-section h1 {{
                font-size: 1.4rem !important;
            }}
            
            .logo-section img {{
                height: 50px;
                width: 50px;
            }}
            
            .nav-buttons {{
                justify-content: center;
                gap: 0.4rem;
                flex-wrap: wrap;
            }}
            
            h1 {{
                font-size: 1.8rem !important;
            }}
            
            h2 {{
                font-size: 1.4rem !important;
            }}
            
            .stButton button {{
                padding: 0.6rem 1rem !important;
                font-size: 0.85rem !important;
            }}
            
            [data-testid="column"] {{
                padding: 0.3rem !important;
            }}
            
            .price-value {{
                font-size: 1rem !important;
            }}
        }}
        
    </style>
    """
    
    st.markdown(custom_css, unsafe_allow_html=True)

def build_header():
    """Construit le header compact (Accueil + Menu déroulant)"""
    inject_background_layer()
    logo_b64, logo_ext = get_img_as_base64(f"assets/{LOGO_FILENAME}")
    cart_count = sum(item['quantity'] for item in st.session_state.cart.values())

    with st.container():
        st.markdown('<div class="custom-header">', unsafe_allow_html=True)
        
        col1, col2 = st.columns([1.5, 1])
        
        with col1:
            logo_html = f'<img src="data:image/{logo_ext};base64,{logo_b64}" alt="Logo">' if logo_b64 else '<div style="width:55px;height:55px;background:linear-gradient(135deg,#D4AF37,#FFD700);border-radius:50%;"></div>'
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
            
            # --- MODIFIÉ: Layout pour Accueil + Menu ---
            cols_nav = st.columns([1, 1]) 
            
            with cols_nav[0]:
                # Bouton Accueil (style sombre par défaut)
                if st.button("🏠 Accueil", key="nav_home", use_container_width=True):
                    st.switch_page("app.py")

            with cols_nav[1]:
                # Libellé du menu avec badge panier
                menu_label = "☰ Menu"
                if cart_count > 0:
                    menu_label = f"☰ Menu ({cart_count}) 🛒" # Ajoute le compte au bouton menu

                # Menu déroulant Popover (style clair)
                with st.popover(menu_label, use_container_width=True):
                    
                    # --- Bouton Panier (MAINTENANT A L'INTERIEUR) ---
                    if st.button(f"🛒 Panier ({cart_count})", key="popover_cart", use_container_width=True):
                        st.switch_page("pages/2_Panier.py")
                    
                    if st.button("📦 Commander", key="popover_checkout", use_container_width=True):
                        st.switch_page("pages/3_Checkout.py")
                    
                    # Séparateur visuel dans le menu
                    st.markdown("---") 
                    
                    if st.session_state.get('authenticated', False):
                        if st.button("📊 Admin", key="popover_admin", use_container_width=True):
                            st.switch_page("pages/admin_4_Dashboard.py")
                    else:
                        if st.button("🔐 Connexion", key="popover_login", use_container_width=True):
                            st.switch_page("pages/admin_login.py")
            # --- FIN DE LA MODIFICATION ---

            st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)