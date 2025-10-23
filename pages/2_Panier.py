"""
Page Panier - Gestion du panier d'achat
Sensations by Arda J - Parfums & Essences
"""

import streamlit as st
from dotenv import load_dotenv # <-- AJOUTER
load_dotenv() # <-- AJOUTER
from config.supabase_client import init_supabase
from utils.session import (init_session_state, get_cart_total, get_cart_count, 
                           update_cart_quantity, remove_from_cart, display_flash_message,
                           set_flash_message)
from utils.formatters import format_price
from utils.styling import load_custom_styling, build_header

# Configuration
st.set_page_config(
    page_title="Panier - Sensations by Arda J", 
    page_icon="🛒", 
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Initialisation
init_supabase()
init_session_state()

# Charger le style et construire le header
load_custom_styling()
build_header()

# Titre
st.markdown("""
<h1 style="
    text-align: center;
    color: #D4AF37 !important;
    font-family: 'Playfair Display', serif !important;
    margin-bottom: 2rem;
">🛒 Mon Panier</h1>
""", unsafe_allow_html=True)

# Afficher les messages flash
display_flash_message()

# Vérifier si le panier est vide
if not st.session_state.cart or len(st.session_state.cart) == 0:
    st.markdown("""
    <div style="
        background: rgba(20, 20, 20, 0.9);
        border: 1px solid rgba(212, 175, 55, 0.4);
        border-radius: 20px;
        padding: 3rem;
        text-align: center;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4);
        margin: 2rem 0;
    ">
        <div style="font-size: 5rem; margin-bottom: 1rem;">🛒</div>
        <h2 style="color: #D4AF37 !important; margin-bottom: 1rem;">Votre panier est vide</h2>
        <p style="color: #E5E5E5 !important; font-size: 1.1rem; text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.9);">
            Découvrez notre collection exclusive de parfums & essences d'exception
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🌸 Découvrir nos senteurs", use_container_width=True, type="primary"):
            st.switch_page("app.py")
else:
    # Afficher les articles du panier
    st.markdown(f"""
    <div style="
        color: #D4AF37;
        font-size: 1.2rem;
        font-weight: 600;
        margin-bottom: 1.5rem;
        text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.9);
    ">
        ✨ {get_cart_count()} senteur(s) dans votre panier
    </div>
    """, unsafe_allow_html=True)
    
    st.divider()
    
    # Liste des articles
    for product_id, item in st.session_state.cart.items():
        col1, col2, col3, col4, col5 = st.columns([1, 3, 2, 2, 1])
        
        with col1:
            # Image du produit
            if item.get('image'):
                st.image(item['image'], use_container_width=True)
            else:
                st.image("https://via.placeholder.com/100x100?text=No+Image")
        
        with col2:
            # Nom du produit
            st.markdown(f"**{item['name']}**")
            st.caption(f"Prix unitaire: {format_price(item['price'])} FCFA")
        
        with col3:
            # Quantité
            new_quantity = st.number_input(
                "Quantité",
                min_value=0,
                max_value=item['stock'],
                value=item['quantity'],
                key=f"qty_{product_id}",
                label_visibility="collapsed"
            )
            
            # Mettre à jour si changement
            if new_quantity != item['quantity']:
                if new_quantity == 0:
                    remove_from_cart(product_id)
                    set_flash_message(f"🗑️ {item['name']} retiré du panier", "info")
                    st.rerun()
                else:
                    if update_cart_quantity(product_id, new_quantity):
                        st.rerun()
                    else:
                        st.error("Stock insuffisant")
        
        with col4:
            # Sous-total
            subtotal = item['price'] * item['quantity']
            st.markdown(
                f"<p style='font-weight: 700; color: #D4AF37; font-size: 1.1rem; text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.9);'>{format_price(subtotal)} FCFA</p>", 
                unsafe_allow_html=True
            )
        
        with col5:
            # Bouton supprimer
            if st.button("🗑️", key=f"remove_{product_id}", help="Retirer du panier"):
                remove_from_cart(product_id)
                set_flash_message(f"🗑️ {item['name']} retiré du panier", "info")
                st.rerun()
        
        st.divider()
    
    # Récapitulatif
    st.markdown("### 💰 Récapitulatif")
    
    col1, col2 = st.columns([2, 1])
    
    with col2:
        # Conteneur pour le récapitulatif
        st.markdown("""
        <div style="
            background: rgba(20, 20, 20, 0.9);
            border: 1px solid rgba(212, 175, 55, 0.4);
            border-radius: 15px;
            padding: 1.5rem;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4);
        ">
        """, unsafe_allow_html=True)
        
        total = get_cart_total()
        
        # Sous-total
        st.markdown(f"**Sous-total:** {format_price(total)} FCFA")
        
        # Frais de livraison
        shipping = 0  # Livraison gratuite
        st.markdown(f"**Livraison:** Gratuite ✨")
        
        st.divider()
        
        # Total
        st.markdown(
            f"<p style='font-size: 1.5rem; font-weight: 700; color: #D4AF37; text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.9);'>TOTAL: {format_price(total)} FCFA</p>", 
            unsafe_allow_html=True
        )
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        st.write("")  # Espacement
        
        # Boutons d'action
        if st.button("📦 Passer la commande", use_container_width=True, type="primary"):
            st.switch_page("pages/3_Checkout.py")
        
        if st.button("🌸 Continuer mes achats", use_container_width=True):
            st.switch_page("app.py")
        
        if st.button("🗑️ Vider le panier", use_container_width=True):
            st.session_state.cart = {}
            set_flash_message("🗑️ Panier vidé", "info")
            st.rerun()

# Footer informatif
st.divider()
st.markdown("""
<div style="
    text-align: center;
    background: rgba(10, 10, 10, 0.9);
    border: 1px solid rgba(212, 175, 55, 0.3);
    border-radius: 15px;
    padding: 1.5rem;
    margin-top: 2rem;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4);
">
    <p style="color: #D4AF37 !important; font-size: 1rem; font-weight: 600; margin-bottom: 0.5rem;">
        ✨ Sensations by Arda J ✨
    </p>
    <p style="color: #CCCCCC !important; font-size: 0.9rem; margin: 0;">
        🔒 Paiement sécurisé | 🚚 Livraison gratuite | 📞 Support client disponible
    </p>
</div>
""", unsafe_allow_html=True)