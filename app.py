"""
Sensations by Arda J - Application E-commerce Streamlit
Page d'accueil avec catalogue intégré - Prix en Franc CFA
VERSION CORRIGÉE
"""

import streamlit as st
from dotenv import load_dotenv # <-- AJOUTER
load_dotenv() # <-- AJOUTER
from config.supabase_client import init_supabase
from models.product import Product
from utils.session import (init_session_state, add_to_cart, set_flash_message, 
                           display_flash_message)
from utils.formatters import format_price, format_stock_badge
from utils.styling import load_custom_styling, build_header

# Configuration de la page
st.set_page_config(
    page_title="Sensations by Arda J - Parfums & Essences",
    page_icon="assets/logo.jpg", 
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Initialisation
def main():
    """Page d'accueil avec catalogue de senteurs"""
    
    # Initialiser Supabase
    init_supabase()
    
    # Initialiser la session
    init_session_state()
    
    # Charger le style et construire le header
    load_custom_styling()
    build_header()
    
    # Message de bienvenue
    st.markdown("""
    <div style="
        text-align: center; 
        background: linear-gradient(135deg, rgba(212, 175, 55, 0.15) 0%, rgba(255, 215, 0, 0.15) 100%);
        border: 1px solid rgba(212, 175, 55, 0.4);
        border-radius: 15px;
        padding: 1.2rem;
        margin-bottom: 1.5rem;
        backdrop-filter: blur(10px);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4);
    ">
        <h2 style="
            color: #D4AF37 !important;
            margin: 0 0 0.4rem 0 !important;
            font-size: 1.6rem !important;
            font-family: 'Playfair Display', serif !important;
        ">🌟 Bienvenue chez Sensations by Arda J 🌟</h2>
        <p style="
            color: #E5E5E5 !important;
            margin: 0 !important;
            font-size: 1rem;
            text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.9);
            font-style: italic;
        ">Découvrez notre collection exclusive de parfums, essences & senteurs d'exception</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Afficher les messages flash
    display_flash_message()
    
    # Barre de recherche et filtres
    st.markdown("### 🔍 Trouvez votre senteur idéale")
    
    col_search, col_filter = st.columns([3, 1])
    
    with col_search:
        search_query = st.text_input(
            "Rechercher une senteur", 
            placeholder="Nom, description, notes olfactives...", 
            label_visibility="collapsed",
            key="search_input"
        )
    
    with col_filter:
        filter_type = st.selectbox(
            "Type", 
            ["Tous", "Homme", "Femme", "Mixte"], 
            label_visibility="collapsed",
            key="type_filter"
        )
    
    st.divider()
    
    # Récupérer les produits
    products = Product.get_all(search=search_query, filter_type=filter_type)
    
    if not products:
        st.info("😢 Aucune senteur trouvée. Essayez d'autres critères de recherche.")
    else:
        # Nombre de produits trouvés
        st.markdown(f"""
        <div style="
            color: #D4AF37;
            font-size: 1.1rem;
            font-weight: 600;
            margin-bottom: 1.2rem;
            text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.9);
        ">
            ✨ {len(products)} senteur(s) d'exception
        </div>
        """, unsafe_allow_html=True)
        
        # Afficher les produits en grille
        cols_per_row = 4
        for i in range(0, len(products), cols_per_row):
            cols = st.columns(cols_per_row)
            
            for j, col in enumerate(cols):
                idx = i + j
                if idx < len(products):
                    product = products[idx]
                    
                    with col:
                        # Carte produit
                        with st.container():
                            # Image principale
                            images = product.get('product_images', [])
                            image_url = images[0]['url'] if images else 'https://via.placeholder.com/300x200?text=No+Image'
                            
                            st.image(image_url, use_container_width=True)
                            
                            # Nom et type
                            st.markdown(f"**{product['name']}**")
                            st.caption(f"🏷️ {product['type']}")
                            
                            # Description tronquée
                            if product.get('description'):
                                desc = product['description'][:80] + "..." if len(product['description']) > 80 else product['description']
                                st.caption(desc)
                            
                            # Prix
                            st.markdown(
                                f"<p style='font-size: 1.1rem; font-weight: 700; color: #D4AF37; margin: 0.4rem 0; text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.9);'>{format_price(product['price'])}</p>", 
                                unsafe_allow_html=True
                            )
                            
                            # Stock
                            st.markdown(format_stock_badge(product['stock']), unsafe_allow_html=True)
                            
                            st.write("")  # Espacement
                            
                            # Boutons
                            col_btn1, col_btn2 = st.columns(2)
                            
                            with col_btn1:
                                if st.button("👁️ Détails", key=f"details_{product['id']}", use_container_width=True):
                                    st.session_state['selected_product'] = product['id']
                                    st.rerun()
                            
                            with col_btn2:
                                if product['stock'] > 0:
                                    if st.button("🛒 Ajouter", key=f"add_{product['id']}", use_container_width=True, type="primary"):
                                        product_data = {
                                            'name': product['name'],
                                            'price': product['price'],
                                            'stock': product['stock'],
                                            'image': image_url
                                        }
                                        if add_to_cart(product['id'], product_data, 1):
                                            set_flash_message(f"✅ {product['name']} ajouté au panier !", "success")
                                            st.rerun()
                                        else:
                                            set_flash_message("❌ Stock insuffisant", "error")
                                            st.rerun()
                                else:
                                    st.button("Épuisé", key=f"add_{product['id']}", use_container_width=True, disabled=True)
    
    # Modal détail produit
    if 'selected_product' in st.session_state and st.session_state['selected_product']:
        product = Product.get_by_id(st.session_state['selected_product'])
        
        if product:
            @st.dialog(f"🌸 {product['name']}", width="large")
            def show_product_details():
                col1, col2 = st.columns([1, 1])
                
                with col1:
                    # Galerie d'images
                    images = product.get('product_images', [])
                    if images:
                        for img in images:
                            st.image(img['url'], use_container_width=True)
                    else:
                        st.image('https://via.placeholder.com/400x300?text=No+Image')
                
                with col2:
                    st.markdown(f"### {product['name']}")
                    st.markdown(f"**Type:** {product['type']}")
                    
                    st.divider()
                    
                    # Prix
                    st.markdown(
                        f"<p style='font-size: 1.5rem; font-weight: 700; color: #D4AF37; text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.9);'>{format_price(product['price'])}</p>", 
                        unsafe_allow_html=True
                    )
                    
                    # Stock
                    st.markdown(format_stock_badge(product['stock']), unsafe_allow_html=True)
                    
                    st.divider()
                    
                    # Description
                    if product.get('description'):
                        st.markdown("**Description**")
                        st.write(product['description'])
                    
                    st.divider()
                    
                    # Quantité et ajout au panier
                    if product['stock'] > 0:
                        quantity = st.number_input("Quantité", min_value=1, max_value=product['stock'], value=1, key="modal_qty")
                        
                        col_a, col_b = st.columns(2)
                        
                        with col_a:
                            if st.button("Ajouter au panier", use_container_width=True, type="primary"):
                                product_data = {
                                    'name': product['name'],
                                    'price': product['price'],
                                    'stock': product['stock'],
                                    'image': images[0]['url'] if images else ''
                                }
                                if add_to_cart(product['id'], product_data, quantity):
                                    set_flash_message(f"✅ {quantity}x {product['name']} ajouté(s) au panier !", "success")
                                    st.session_state['selected_product'] = None
                                    st.rerun()
                                else:
                                    st.error("❌ Stock insuffisant")
                        
                        with col_b:
                            if st.button("Fermer", use_container_width=True):
                                st.session_state['selected_product'] = None
                                st.rerun()
                    else:
                        st.error("😢 Cette senteur est actuellement en rupture de stock")
                        if st.button("Fermer", use_container_width=True):
                            st.session_state['selected_product'] = None
                            st.rerun()
            
            show_product_details()
    
    # Section des collections - PLUS DE CATÉGORIES
    #A faire

    # BOUTON COMMANDER EN BAS
    st.divider()
    col_empty1, col_button, col_empty2 = st.columns([1, 2, 1])
    with col_button:
        if st.button("📦 PASSER COMMANDE", use_container_width=True, type="primary"):
            st.switch_page("pages/3_Checkout.py")
    
    # Footer avec bon email
    st.divider()
    st.markdown("""
    <div style="
        text-align: center; 
        background: rgba(10, 10, 10, 0.95);
        border: 1px solid rgba(212, 175, 55, 0.3);
        border-radius: 15px;
        padding: 1.5rem;
        margin-top: 2rem;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4);
    ">
        <p style="color: #D4AF37 !important; font-size: 1.1rem; font-weight: 600; margin-bottom: 0.8rem;">
            ✨ Sensations by Arda J - Parfums, Essences & Senteurs d'Exception ✨
        </p>
        <p style="color: #CCCCCC !important; font-size: 0.9rem; margin: 0.4rem 0;">
            © 2025 Sensations by Arda J - Tous droits réservés
        </p>
        <p style="color: #CCCCCC !important; font-size: 0.9rem;">
            <a href="mailto:sensationsbyarda@gmail.com" style="color: #D4AF37; text-decoration: none;">📧 sensationsbyarda@gmail.com</a> | 
        </p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()