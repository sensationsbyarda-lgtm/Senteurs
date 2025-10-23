"""
Page Gestion des Commandes Admin
"""

import streamlit as st
import pandas as pd
from config.supabase_client import init_supabase
from models.order import Order
from utils.session import init_session_state, require_auth, display_flash_message, set_flash_message
from utils.formatters import format_price, format_date, format_order_status, format_phone
from models.analytics import Analytics

# Configuration
st.set_page_config(page_title="Commandes Admin - Sensations Arda", page_icon="📋", layout="wide")

# Initialisation
init_supabase()
init_session_state()

# Protection de la page
@require_auth
def main():
    st.title("📋 Gestion des Commandes")
    
    # Afficher les messages flash
    display_flash_message()
    
    # Filtres
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        search = st.text_input("🔍 Rechercher", placeholder="Numéro de commande ou nom client...")
    
    with col2:
        status_filter = st.selectbox("Statut", ["Tous", "en_cours", "livree", "annulee"])
    
    with col3:
        show_only_new = st.checkbox("Nouvelles uniquement")
    
    # Récupérer les commandes
    if show_only_new:
        orders = Order.get_new_orders()
    elif status_filter != "Tous":
        orders = Order.get_orders_by_status(status_filter)
    else:
        orders = Order.get_all()
    
    # Filtrer par recherche
    if search:
        orders = [
            o for o in orders
            if search.lower() in str(o['id']) or
               search.lower() in f"{o.get('clients', {}).get('first_name', '')} {o.get('clients', {}).get('last_name', '')}".lower()
        ]
    
    st.markdown(f"**{len(orders)} commande(s) trouvée(s)**")
    
    # Bouton export CSV
    if orders:
        csv_data = Analytics.export_orders_to_csv(orders)
        st.download_button(
            label="📥 Exporter en CSV",
            data=csv_data,
            file_name=f"commandes_{pd.Timestamp.now().strftime('%Y%m%d')}.csv",
            mime="text/csv"
        )
    
    st.divider()
    
    # Afficher les commandes
    if not orders:
        st.info("Aucune commande trouvée")
    else:
        for order in orders:
            client = order.get('clients', {})
            items = order.get('order_items', [])
            
            # Card commande avec style conditionnel
            card_class = "new-order" if not order['viewed'] else ""
            
            with st.container(border=True):
                # En-tête
                col1, col2, col3, col4 = st.columns([2, 2, 2, 1])
                
                with col1:
                    icon = "🆕" if not order['viewed'] else "📦"
                    st.markdown(f"### {icon} Commande #{order['id']}")
                    st.caption(format_date(order['created_at']))
                
                with col2:
                    st.markdown("**Client**")
                    st.write(f"{client.get('first_name', '')} {client.get('last_name', '')}")
                    st.caption(f"📧 {client.get('email', '')}")
                
                with col3:
                    st.markdown("**Statut**")
                    st.markdown(format_order_status(order['status']), unsafe_allow_html=True)
                
                with col4:
                    st.markdown("**Total**")
                    st.markdown(f"<p style='font-size: 1.5rem; font-weight: 700; color: #3b82f6; margin: 0;'>{format_price(order['total'])}</p>", unsafe_allow_html=True)
                
                # Expandable details
                with st.expander("📄 Voir les détails", expanded=not order['viewed']):
                    col_info, col_items = st.columns([1, 2])
                    
                    with col_info:
                        st.markdown("#### 📍 Informations Client")
                        st.markdown(f"""
                        **Nom:** {client.get('first_name', '')} {client.get('last_name', '')}  
                        **Email:** {client.get('email', '')}  
                        **Téléphone:** {format_phone(client.get('phone', ''))}  
                        **Adresse:**  
                        {client.get('address', '')}
                        """)
                    
                    with col_items:
                        st.markdown("#### 🛒 Articles Commandés")
                        
                        for item in items:
                            product = item.get('products', {})
                            col_a, col_b, col_c = st.columns([3, 1, 2])
                            
                            with col_a:
                                st.write(f"**{product.get('name', 'Produit')}**")
                            
                            with col_b:
                                st.write(f"x{item.get('quantity', 0)}")
                            
                            with col_c:
                                st.write(f"{format_price(item.get('price', 0) * item.get('quantity', 0))}")
                            
                            st.divider()
                        
                        # Total
                        st.markdown(f"**TOTAL:** {format_price(order['total'])}")
                    
                    st.divider()
                    
                    # Actions
                    col_act1, col_act2, col_act3 = st.columns(3)
                    
                    with col_act1:
                        # Changer le statut
                        status_options = ["en_cours", "livree", "annulee"]
                        current_index = status_options.index(order['status'])
                        
                        new_status = st.selectbox(
                            "Changer le statut",
                            options=status_options,
                            index=current_index,
                            key=f"status_{order['id']}",
                            format_func=lambda x: {"en_cours": "En cours", "livree": "Livrée", "annulee": "Annulée"}[x]
                        )
                        
                        if new_status != order['status']:
                            if st.button("💾 Sauvegarder le statut", key=f"save_status_{order['id']}", use_container_width=True):
                                if Order.update_status(order['id'], new_status):
                                    set_flash_message(f"✅ Statut mis à jour", "success")
                                    st.rerun()
                    
                    with col_act2:
                        # Marquer comme vue
                        if not order['viewed']:
                            if st.button("👁️ Marquer comme vue", key=f"mark_viewed_{order['id']}", use_container_width=True):
                                if Order.mark_as_viewed(order['id']):
                                    set_flash_message(f"✅ Commande marquée comme vue", "success")
                                    st.rerun()
                    
                    with col_act3:
                        # Export PDF (placeholder - nécessiterait une lib comme reportlab)
                        st.button("📄 Exporter PDF", key=f"pdf_{order['id']}", use_container_width=True, disabled=True, help="Fonctionnalité à venir")

# Exécuter
main()