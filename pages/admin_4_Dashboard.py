"""
Page Dashboard Admin - Vue d'ensemble
"""

import streamlit as st
from typing import Dict
# --- MODIFIÉ ---
from config.supabase_client import init_supabase, load_supabase_session, clear_supabase_session
from models.analytics import Analytics
from models.order import Order
from models.product import Product
from utils.session import init_session_state, require_auth, display_flash_message
# --- FIN MODIFIÉ ---
from utils.formatters import format_price, format_date, format_relative_time

# Configuration
st.set_page_config(page_title="Dashboard Admin - Sensations Arda", page_icon="📊", layout="wide")

# Initialisation
init_supabase()
init_session_state()

# Protection de la page
@require_auth
def main():
    # --- AJOUTÉ ---
    # S'assure que le client Supabase a bien le token d'authentification
    load_supabase_session()
    
    # En-tête avec déconnexion
    col1, col2 = st.columns([4, 1])
    
    with col1:
        st.title("📊 Dashboard Administrateur")
        # --- CORRIGÉ ---
        # Utiliser la donnée stockée par set_supabase_session
        st.markdown(f"Bienvenue, **{st.session_state.get('user', {}).get('email', 'Admin')}**")
    
    with col2:
        if st.button("🚪 Déconnexion", use_container_width=True):
            # --- CORRIGÉ ---
            # Appeler la nouvelle fonction de déconnexion
            clear_supabase_session()
            # La page est rechargée par clear_supabase_session,
            # mais on garde un switch_page au cas où.
            st.switch_page("app.py")
    
    # Afficher les messages flash
    display_flash_message()
    
    st.divider()
    
    # Récupérer les métriques
    metrics = Analytics.get_dashboard_metrics()
    
    # ... (le reste du fichier est identique) ...
    
    # Métriques principales
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="📦 Total Commandes",
            value=metrics['total_orders'],
            help="Nombre total de commandes"
        )
    
    with col2:
        st.metric(
            label="🆕 Nouvelles Commandes",
            value=metrics['new_orders'],
            delta=f"+{metrics['new_orders']}" if metrics['new_orders'] > 0 else None,
            delta_color="normal",
            help="Commandes non encore consultées"
        )
    
    with col3:
        st.metric(
            label="⏱️ Commandes 24h",
            value=metrics['orders_24h'],
            help="Commandes des dernières 24 heures"
        )
    
    with col4:
        st.metric(
            label="📦 Produits",
            value=metrics['total_products'],
            help="Nombre total de produits"
        )
    
    st.divider()
    
    # Deux colonnes pour le contenu
    col_left, col_right = st.columns([2, 1])
    
    with col_left:
        # Nouvelles commandes
        st.subheader("🆕 Nouvelles Commandes")
        
        new_orders = Order.get_new_orders()
        
        if new_orders:
            for order in new_orders[:5]:  # Afficher les 5 dernières
                client = order.get('clients', {})
                
                # Card avec background vert pour nouvelles commandes
                st.markdown(f"""
                <div class="new-order">
                    <strong>Commande #{order['id']}</strong> - {format_relative_time(order['created_at'])}<br>
                    👤 {client.get('first_name', '')} {client.get('last_name', '')}<br>
                    💰 {format_price(order['total'])}
                </div>
                """, unsafe_allow_html=True)
                
                col_a, col_b = st.columns([1, 1])
                
                with col_a:
                    if st.button("👁️ Voir détails", key=f"view_{order['id']}", use_container_width=True):
                        st.switch_page("pages/admin_6_Commandes.py")
                
                with col_b:
                    if st.button("✅ Marquer comme vue", key=f"mark_{order['id']}", use_container_width=True):
                        if Order.mark_as_viewed(order['id']):
                            st.rerun()
        else:
            st.info("✨ Aucune nouvelle commande")
        
        st.divider()
        
        # Activité récente
        st.subheader("📋 Activité Récente")
        
        activities = Analytics.get_recent_activity(limit=5)
        
        for activity in activities:
            icon = "🆕" if not activity['viewed'] else "✅"
            st.markdown(f"""
            {icon} **Commande #{activity['order_id']}** - {activity['client_name']}  
            💰 {format_price(activity['total'])} • {format_relative_time(activity['created_at'])}
            """)
            st.divider()
    
    with col_right:
        # Alertes stock
        st.subheader("⚠️ Alertes Stock")
        
        # Produits en rupture
        out_of_stock = Product.get_out_of_stock_products()
        if out_of_stock:
            st.markdown('<div class="alert-danger">', unsafe_allow_html=True)
            st.markdown(f"**🚫 {len(out_of_stock)} produit(s) en rupture de stock**")
            for product in out_of_stock[:3]:
                st.markdown(f"• {product['name']}")
            if len(out_of_stock) > 3:
                st.markdown(f"*... et {len(out_of_stock) - 3} autre(s)*")
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Produits en stock faible
        low_stock = Product.get_low_stock_products(threshold=5)
        low_stock = [p for p in low_stock if p['stock'] > 0]  # Exclure ruptures
        
        if low_stock:
            st.markdown('<div class="alert-warning">', unsafe_allow_html=True)
            st.markdown(f"**⚠️ {len(low_stock)} produit(s) en stock faible**")
            for product in low_stock[:3]:
                st.markdown(f"• {product['name']} ({product['stock']} restants)")
            if len(low_stock) > 3:
                st.markdown(f"*... et {len(low_stock) - 3} autre(s)*")
            st.markdown('</div>', unsafe_allow_html=True)
        
        if not out_of_stock and not low_stock:
            st.success("✅ Tous les stocks sont OK")
        
        st.divider()
        
        # Navigation rapide
        st.subheader("🧭 Navigation Rapide")
        
        if st.button("📦 Gérer les produits", use_container_width=True):
            st.switch_page("pages/admin_5_Produits.py")
        
        if st.button("📋 Voir les commandes", use_container_width=True):
            st.switch_page("pages/admin_6_Commandes.py")
        
        if st.button("📈 Analytics", use_container_width=True):
            st.switch_page("pages/admin_7_Analyses.py")
        
        if st.button("🏠 Retour au site", use_container_width=True):
            st.switch_page("app.py")

# Exécuter la fonction principale
main()