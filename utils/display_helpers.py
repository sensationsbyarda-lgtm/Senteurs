"""
Helpers pour l'affichage amélioré des produits - VERSION CORRIGÉE
Sensations by Arda J
"""

import streamlit as st
from utils.formatters import format_price

def display_product_card(product, image_url, product_id):
    """
    Affiche une carte produit avec PRIX FCFA ULTRA VISIBLE
    
    Args:
        product: Dict avec les données du produit
        image_url: URL de l'image principale
        product_id: ID du produit pour les clés uniques
    """
    
    # Image du produit
    st.image(image_url, use_container_width=True)
    
    # Nom du produit (en gras et bien visible)
    st.markdown(f"**{product['name']}**")
    
    # Type de produit
    st.caption(f"🏷️ {product['type']}")
    
    # Description tronquée
    if product.get('description'):
        desc = product['description'][:65] + "..." if len(product['description']) > 65 else product['description']
        st.caption(desc)
    
    # FIX: Prix ULTRA VISIBLE avec FCFA en gros
    st.markdown(
        f"""
        <div class="price-container">
            <span class="price-value">{format_price(product['price'])} FCFA</span>
        </div>
        """, 
        unsafe_allow_html=True
    )
    
    # FIX: Badges de stock plus visibles avec émojis
    if product['stock'] <= 0:
        st.markdown('<span class="out-of-stock">❌ Rupture de stock</span>', unsafe_allow_html=True)
    elif product['stock'] <= 5:
        st.markdown(f'<span class="low-stock">⚠️ Stock faible ({product["stock"]})</span>', unsafe_allow_html=True)
    else:
        st.markdown(f'<span class="in-stock">✅ En stock ({product["stock"]})</span>', unsafe_allow_html=True)
    
    st.write("")  # Espacement
    
    # FIX: Boutons bien alignés et espacés
    col_btn1, col_btn2 = st.columns([1, 1])
    
    with col_btn1:
        if st.button("👁️ Détails", key=f"details_{product_id}", use_container_width=True):
            return 'details', product_id
    
    with col_btn2:
        if product['stock'] > 0:
            if st.button("🛒 Ajouter", key=f"add_{product_id}", use_container_width=True, type="primary"):
                return 'add', product_id
        else:
            st.button("Épuisé", key=f"add_{product_id}", use_container_width=True, disabled=True)
    
    return None, None


def display_product_modal(product, images):
    """
    Affiche le modal de détails produit avec PRIX ENCORE PLUS GRAND
    
    Args:
        product: Dict avec les données du produit
        images: Liste des images du produit
    """
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        # Galerie d'images
        st.markdown("### 📸 Photos")
        if images:
            for img in images:
                st.image(img['url'], use_container_width=True)
        else:
            st.image('https://via.placeholder.com/500x375?text=Aucune+Image')
    
    with col2:
        # En-tête du produit
        st.markdown(f"### {product['name']}")
        
        # Type avec badge stylisé
        st.markdown(f"""
        <div style="
            display: inline-block;
            background: linear-gradient(135deg, rgba(212, 175, 55, 0.25) 0%, rgba(255, 215, 0, 0.25) 100%);
            border: 3px solid rgba(212, 175, 55, 0.6);
            border-radius: 25px;
            padding: 0.6rem 1.4rem;
            margin: 0.5rem 0 1.5rem 0;
            font-weight: 700;
            color: #FFD700;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 1);
            font-size: 1rem;
        ">
            🏷️ {product['type']}
        </div>
        """, unsafe_allow_html=True)
        
        st.divider()
        
        # FIX: Prix ÉNORME dans le modal avec animation
        st.markdown(
            f"""
            <div class="price-container" style="margin: 1.5rem 0 !important;">
                <span class="price-value" style="font-size: 2.5rem !important;">{format_price(product['price'])} FCFA</span>
            </div>
            """, 
            unsafe_allow_html=True
        )
        
        # FIX: Stock avec badges plus grands
        if product['stock'] <= 0:
            st.markdown(
                '<div style="text-align: center; margin: 1rem 0;">'
                '<span class="out-of-stock" style="padding: 0.8rem 1.5rem; font-size: 1rem;">❌ Rupture de stock</span>'
                '</div>', 
                unsafe_allow_html=True
            )
        elif product['stock'] <= 5:
            st.markdown(
                f'<div style="text-align: center; margin: 1rem 0;">'
                f'<span class="low-stock" style="padding: 0.8rem 1.5rem; font-size: 1rem;">⚠️ Plus que {product["stock"]} disponible(s)</span>'
                f'</div>', 
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                f'<div style="text-align: center; margin: 1rem 0;">'
                f'<span class="in-stock" style="padding: 0.8rem 1.5rem; font-size: 1rem;">✅ {product["stock"]} disponible(s)</span>'
                f'</div>', 
                unsafe_allow_html=True
            )
        
        st.divider()
        
        # Description complète
        if product.get('description'):
            st.markdown("**📝 Description**")
            st.write(product['description'])
        
        st.divider()
        
        # Section d'ajout au panier
        if product['stock'] > 0:
            st.markdown("**🛒 Quantité**")
            quantity = st.number_input(
                "Quantité", 
                min_value=1, 
                max_value=product['stock'], 
                value=1, 
                key="modal_qty",
                help=f"Maximum disponible: {product['stock']}",
                label_visibility="collapsed"
            )
            
            return quantity
        else:
            st.error("😢 Cette senteur est actuellement en rupture de stock")
            return 0
    
    return 0


def display_welcome_banner():
    """Affiche la bannière de bienvenue SANS barre noire"""
    st.markdown("""
    <div style="
        text-align: center; 
        background: linear-gradient(135deg, rgba(212, 175, 55, 0.2) 0%, rgba(255, 215, 0, 0.2) 100%);
        border: 3px solid rgba(212, 175, 55, 0.6);
        border-radius: 25px;
        padding: 2.5rem 2rem;
        margin-bottom: 2rem;
        backdrop-filter: blur(20px);
        box-shadow: 0 12px 50px rgba(0, 0, 0, 0.6), inset 0 0 60px rgba(212, 175, 55, 0.15);
    ">
        <h2 style="
            color: #D4AF37 !important;
            margin: 0 0 1rem 0 !important;
            font-size: 2.2rem !important;
            font-family: 'Playfair Display', serif !important;
            text-shadow: 3px 3px 6px rgba(0, 0, 0, 1), 0 0 40px rgba(212, 175, 55, 0.6);
        ">🌟 Bienvenue chez Sensations by Arda J 🌟</h2>
        <p style="
            color: #E5E5E5 !important;
            margin: 0 !important;
            font-size: 1.2rem;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 1);
            font-style: italic;
            line-height: 1.6;
        ">Découvrez notre collection exclusive de parfums & essences d'exception</p>
    </div>
    """, unsafe_allow_html=True)


def display_collections_section():
    """Affiche la section des collections"""
    st.markdown("### ✨ Nos Collections")
    
    col1, col2, col3 = st.columns(3)
    
    collections = [
        {
            'icon': '👨',
            'title': 'Pour Homme',
            'description': 'Des fragrances boisées et épicées qui évoquent la force et l\'élégance masculine.',
            'col': col1
        },
        {
            'icon': '👩',
            'title': 'Pour Femme',
            'description': 'Des senteurs florales et délicates qui révèlent la féminité et la sensualité.',
            'col': col2
        },
        {
            'icon': '🤝',
            'title': 'Mixte',
            'description': 'Des compositions unisexes audacieuses pour tous les amoureux de senteurs d\'exception.',
            'col': col3
        }
    ]
    
    for collection in collections:
        with collection['col']:
            st.markdown(f"""
            <div style="
                background: rgba(15, 15, 15, 0.98);
                border: 3px solid rgba(212, 175, 55, 0.5);
                border-radius: 22px;
                padding: 2.5rem 1.8rem;
                text-align: center;
                box-shadow: 0 10px 40px rgba(0, 0, 0, 0.6);
                transition: all 0.4s ease;
                height: 100%;
                cursor: pointer;
            " onmouseover="
                this.style.transform='translateY(-8px)'; 
                this.style.boxShadow='0 15px 50px rgba(212, 175, 55, 0.4)';
                this.style.borderColor='#D4AF37';
            " onmouseout="
                this.style.transform='translateY(0)'; 
                this.style.boxShadow='0 10px 40px rgba(0, 0, 0, 0.6)';
                this.style.borderColor='rgba(212, 175, 55, 0.5)';
            ">
                <div style="font-size: 4rem; margin-bottom: 1.2rem;">{collection['icon']}</div>
                <h3 style="
                    color: #D4AF37 !important; 
                    margin-bottom: 1rem;
                    font-size: 1.5rem !important;
                    text-shadow: 2px 2px 5px rgba(0, 0, 0, 1);
                ">{collection['title']}</h3>
                <p style="
                    color: #E5E5E5 !important; 
                    text-shadow: 1px 1px 3px rgba(0, 0, 0, 0.9);
                    line-height: 1.7;
                    font-size: 0.98rem;
                ">{collection['description']}</p>
            </div>
            """, unsafe_allow_html=True)


def display_footer():
    """Affiche le footer professionnel"""
    st.markdown("""
    <div style="
        text-align: center; 
        background: rgba(8, 8, 8, 0.98);
        border: 2px solid rgba(212, 175, 55, 0.5);
        border-radius: 22px;
        padding: 3rem 2rem;
        margin-top: 3rem;
        box-shadow: 0 10px 40px rgba(0, 0, 0, 0.6);
    ">
        <p style="
            color: #D4AF37 !important; 
            font-size: 1.4rem; 
            font-weight: 800; 
            margin-bottom: 1.2rem;
            text-shadow: 2px 2px 5px rgba(0, 0, 0, 1);
        ">
            ✨ Sensations by Arda J - Parfums & Essences d'Exception ✨
        </p>
        <p style="color: #CCCCCC !important; font-size: 0.95rem; margin: 0.7rem 0;">
            © 2024 Sensations by Arda J - Tous droits réservés
        </p>
        <p style="color: #CCCCCC !important; font-size: 0.95rem; line-height: 2.2;">
            <a href="mailto:contact@sensations-arda.com" style="
                color: #D4AF37; 
                text-decoration: none; 
                transition: all 0.3s;
                font-weight: 600;
            " onmouseover="this.style.color='#FFD700'; this.style.textShadow='0 0 10px rgba(255,215,0,0.5)';" 
               onmouseout="this.style.color='#D4AF37'; this.style.textShadow='none';">📧 Contact</a> | 
            <a href="#" style="
                color: #D4AF37; 
                text-decoration: none; 
                transition: all 0.3s;
                font-weight: 600;
            " onmouseover="this.style.color='#FFD700'; this.style.textShadow='0 0 10px rgba(255,215,0,0.5)';" 
               onmouseout="this.style.color='#D4AF37'; this.style.textShadow='none';">📜 Mentions légales</a> | 
            <a href="#" style="
                color: #D4AF37; 
                text-decoration: none; 
                transition: all 0.3s;
                font-weight: 600;
            " onmouseover="this.style.color='#FFD700'; this.style.textShadow='0 0 10px rgba(255,215,0,0.5)';" 
               onmouseout="this.style.color='#D4AF37'; this.style.textShadow='none';">🔒 Confidentialité</a>
        </p>
    </div>
    """, unsafe_allow_html=True)


def display_product_count(count):
    """Affiche le nombre de produits trouvés de manière élégante"""
    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, rgba(212, 175, 55, 0.2) 0%, rgba(255, 215, 0, 0.2) 100%);
        border: 3px solid rgba(212, 175, 55, 0.5);
        border-radius: 18px;
        padding: 1.2rem 1.8rem;
        margin-bottom: 2rem;
        text-align: center;
        box-shadow: 0 5px 25px rgba(0, 0, 0, 0.4), inset 0 0 30px rgba(212, 175, 55, 0.1);
    ">
        <span style="
            color: #D4AF37;
            font-size: 1.3rem;
            font-weight: 800;
            text-shadow: 2px 2px 5px rgba(0, 0, 0, 1), 0 0 25px rgba(212, 175, 55, 0.5);
            letter-spacing: 0.5px;
        ">
            ✨ {count} senteur{'s' if count > 1 else ''} d'exception
        </span>
    </div>
    """, unsafe_allow_html=True)


def display_no_products_message():
    """Affiche un message quand aucun produit n'est trouvé"""
    st.markdown("""
    <div style="
        background: rgba(96, 165, 250, 0.15);
        border: 3px solid rgba(96, 165, 250, 0.5);
        border-radius: 25px;
        padding: 4rem 3rem;
        text-align: center;
        margin: 3rem 0;
        box-shadow: 0 10px 40px rgba(0, 0, 0, 0.5);
    ">
        <div style="font-size: 5rem; margin-bottom: 1.5rem;">😢</div>
        <h3 style="
            color: #60A5FA !important; 
            margin-bottom: 1.2rem; 
            font-size: 2rem !important;
            text-shadow: 2px 2px 5px rgba(0, 0, 0, 1);
        ">
            Aucune senteur trouvée
        </h3>
        <p style="
            color: #E5E5E5 !important; 
            font-size: 1.15rem; 
            text-shadow: 1px 1px 3px rgba(0, 0, 0, 0.9);
            line-height: 1.6;
        ">
            Essayez d'autres critères de recherche ou parcourez toute notre collection
        </p>
    </div>
    """, unsafe_allow_html=True)