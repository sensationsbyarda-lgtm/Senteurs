"""
Page Checkout - Validation et finalisation de la commande
Sensations by Arda J - Parfums & Essences - Gabon
"""

import streamlit as st
from config.supabase_client import init_supabase
from models.order import Order
from models.client import Client
from utils.session import (init_session_state, get_cart_total, clear_cart, 
                           set_flash_message, display_flash_message)
from utils.validators import validate_checkout_form
from utils.formatters import format_price
from config.email_config import send_admin_notification
from utils.styling import load_custom_styling, build_header

# Configuration
st.set_page_config(
    page_title="Commande - Sensations by Arda J", 
    page_icon="📦", 
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
">📦 Finaliser ma commande</h1>
""", unsafe_allow_html=True)

# Afficher les messages flash
display_flash_message()

# Vérifier si le panier est vide
if not st.session_state.cart or len(st.session_state.cart) == 0:
    st.markdown("""
    <div style="
        background: rgba(239, 68, 68, 0.15);
        border: 1px solid rgba(239, 68, 68, 0.4);
        border-radius: 15px;
        padding: 2rem;
        text-align: center;
        margin: 2rem 0;
    ">
        <div style="font-size: 3rem; margin-bottom: 1rem;">⚠️</div>
        <h3 style="color: #EF4444 !important; margin-bottom: 1rem;">Votre panier est vide</h3>
        <p style="color: #E5E5E5 !important; text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.9);">
            Ajoutez des senteurs avant de commander
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("🌸 Découvrir nos senteurs", use_container_width=True, type="primary"):
        st.switch_page("app.py")
    st.stop()

# Layout en deux colonnes
col_form, col_recap = st.columns([2, 1])

with col_recap:
    st.markdown("""
    <div style="
        background: rgba(20, 20, 20, 0.9);
        border: 1px solid rgba(212, 175, 55, 0.4);
        border-radius: 15px;
        padding: 1.5rem;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4);
        position: sticky;
        top: 2rem;
    ">
    """, unsafe_allow_html=True)
    
    st.markdown("### 📋 Récapitulatif")
    
    # Afficher les produits
    for product_id, item in st.session_state.cart.items():
        st.markdown(f"**{item['name']}**")
        st.caption(f"{item['quantity']} × {format_price(item['price'])} FCFA = {format_price(item['price'] * item['quantity'])} FCFA")
        st.divider()
    
    # Total
    total = get_cart_total()
    st.markdown(
        f"<p style='font-size: 1.5rem; font-weight: 700; color: #D4AF37; text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.9);'>TOTAL: {format_price(total)} FCFA</p>", 
        unsafe_allow_html=True
    )
    
    st.markdown("</div>", unsafe_allow_html=True)

with col_form:
    st.markdown("""
    <div style="
        background: rgba(20, 20, 20, 0.9);
        border: 1px solid rgba(212, 175, 55, 0.4);
        border-radius: 15px;
        padding: 2rem;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4);
    ">
    """, unsafe_allow_html=True)
    
    st.markdown("### 👤 Vos informations")
    
    # Formulaire de commande
    with st.form("checkout_form", clear_on_submit=False):
        col1, col2 = st.columns(2)
        
        with col1:
            first_name = st.text_input("Prénom *", placeholder="Jean")
        
        with col2:
            last_name = st.text_input("Nom *", placeholder="Dupont")
        
        email = st.text_input("Email *", placeholder="jean.dupont@email.com")
        phone = st.text_input("Téléphone *", placeholder="+241 XX XX XX XX")
        address = st.text_area("Adresse complète *", placeholder="Libreville, Gabon", height=100)
        
        st.caption("* Champs obligatoires")
        
        st.divider()
        
        # Conditions générales
        accept_terms = st.checkbox("J'accepte les conditions générales de vente")
        
        # Bouton de validation
        submit = st.form_submit_button("✅ Valider ma commande", use_container_width=True, type="primary")
        
        if submit:
            # Valider les CGV
            if not accept_terms:
                st.error("❌ Vous devez accepter les conditions générales de vente")
            else:
                # Valider le formulaire
                validation = validate_checkout_form(first_name, last_name, email, phone, address)
                
                if not validation['is_valid']:
                    st.error("❌ Veuillez corriger les erreurs suivantes:")
                    for field, error in validation['errors'].items():
                        st.error(f"• {error}")
                else:
                    # Vérifier les stocks une dernière fois
                    stock_check = Order.validate_cart_stock(st.session_state.cart)
                    
                    if not all(stock_check.values()):
                        st.error("❌ Certaines senteurs ne sont plus disponibles en quantité suffisante. Veuillez modifier votre panier.")
                    else:
                        # Créer ou récupérer le client
                        existing_client = Client.get_by_email(email)
                        
                        if existing_client:
                            client = existing_client
                        else:
                            client = Client.create(first_name, last_name, email, phone, address)
                        
                        if not client:
                            st.error("❌ Erreur lors de la création du profil client")
                        else:
                            # Créer la commande
                            order = Order.create(
                                client_id=client['id'],
                                cart_items=st.session_state.cart,
                                total=total
                            )
                            
                            if not order:
                                st.error("❌ Erreur lors de la création de la commande")
                            else:
                                # Préparer les données pour l'email
                                order_items = []
                                for product_id, item in st.session_state.cart.items():
                                    order_items.append({
                                        'product_name': item['name'],
                                        'quantity': item['quantity'],
                                        'price': item['price']
                                    })
                                
                                order_data = {
                                    'id': order['id'],
                                    'total': total,
                                    'items': order_items
                                }
                                
                                client_data = {
                                    'first_name': first_name,
                                    'last_name': last_name,
                                    'email': email,
                                    'phone': phone,
                                    'address': address
                                }
                                
                                # Envoyer les emails
                                try:
                                    send_admin_notification(order_data, client_data)
                                except Exception as e:
                                    # Ne pas bloquer la commande si l'email échoue
                                    print(f"Erreur envoi email: {str(e)}")
                                
                                # Vider le panier
                                clear_cart()
                                
                                # Afficher le succès
                                st.success("✅ Commande validée avec succès !")
                                st.balloons()
                                
                                # Message de confirmation stylisé
                                st.markdown(f"""
                                <div style="
                                    background: linear-gradient(135deg, rgba(16, 185, 129, 0.15) 0%, rgba(5, 150, 105, 0.15) 100%);
                                    border: 1px solid rgba(16, 185, 129, 0.4);
                                    border-radius: 15px;
                                    padding: 2rem;
                                    margin: 2rem 0;
                                    text-align: center;
                                ">
                                    <div style="font-size: 4rem; margin-bottom: 1rem;">🎉</div>
                                    <h2 style="color: #10B981 !important; margin-bottom: 1rem;">Merci pour votre commande !</h2>
                                    <p style="color: #E5E5E5 !important; font-size: 1.1rem; margin-bottom: 1rem; text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.9);">
                                        <strong>Numéro de commande:</strong> <span style="color: #D4AF37;">#{order['id']}</span>
                                    </p>
                                    <p style="color: #E5E5E5 !important; font-size: 1.3rem; font-weight: 700; margin-bottom: 1rem; text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.9);">
                                        <strong>Montant total:</strong> <span style="color: #D4AF37;">{format_price(total)} FCFA</span>
                                    </p>
                                    <p style="color: #CCCCCC !important; margin-top: 1rem; font-size: 0.95rem; text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.9);">
                                        Nous préparons votre commande de parfums & essences avec soin.<br>
                                        Vous serez tenu informé de son expédition.
                                    </p>
                                </div>
                                """, unsafe_allow_html=True)
                                
                                if st.button("🏠 Retour à l'accueil", use_container_width=True):
                                    st.switch_page("app.py")
    
    st.markdown("</div>", unsafe_allow_html=True)

# Informations supplémentaires
st.divider()

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div style="
        background: rgba(20, 20, 20, 0.9);
        border: 1px solid rgba(212, 175, 55, 0.3);
        border-radius: 15px;
        padding: 1.5rem;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4);
    ">
        <h3 style="color: #D4AF37 !important; text-align: center; margin-bottom: 1rem;">🚚 Livraison</h3>
        <ul style="color: #E5E5E5 !important; line-height: 1.8; text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.9);">
            <li>Livraison à la charge du client</li>
            <li>Délai: 3-5 jours ouvrés</li>
            <li>Emballage soigné</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div style="
        background: rgba(20, 20, 20, 0.9);
        border: 1px solid rgba(212, 175, 55, 0.3);
        border-radius: 15px;
        padding: 1.5rem;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4);
    ">
        <h3 style="color: #D4AF37 !important; text-align: center; margin-bottom: 1rem;">💳 Paiement</h3>
        <ul style="color: #E5E5E5 !important; line-height: 1.8; text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.9);">
            <li>Paiement sécurisé</li>
            <li>Mobile Money accepté</li>
            <li>Airtel Money / Moov</li>
            <li>Garantie satisfaction</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div style="
        background: rgba(20, 20, 20, 0.9);
        border: 1px solid rgba(212, 175, 55, 0.3);
        border-radius: 15px;
        padding: 1.5rem;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4);
    ">
        <h3 style="color: #D4AF37 !important; text-align: center; margin-bottom: 1rem;">📞 Support</h3>
        <ul style="color: #E5E5E5 !important; line-height: 1.8; text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.9);">
            <li>📧 sensationsbyarda@gmail.com</li>
            <li>📱 +241 XX XX XX XX</li>
            <li>🕐 Lun-Sam, 9h-19h</li>
            <li>💬 Assistance dédiée</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)