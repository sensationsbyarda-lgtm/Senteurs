"""
Page Analytics Admin - Statistiques et rapports
"""

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from config.supabase_client import init_supabase
from models.analytics import Analytics
from utils.session import init_session_state, require_auth, display_flash_message
from utils.formatters import format_price

# Configuration
st.set_page_config(page_title="Analytics Admin - Sensations Arda", page_icon="📈", layout="wide")

# Initialisation
init_supabase()
init_session_state()

# NOTE (Refactoring): La fonction get_period_comparison qui se trouvait ici a été supprimée.
# Elle n'était pas utilisée, car l'appel à la ligne 123 
# (maintenant ligne 65) utilise Analytics.get_period_comparison (depuis le modèle).
# C'était du code mort qui prêtait à confusion.

# Protection de la page
@require_auth
def main():
    st.title("📈 Analytics & Rapports")
    
    # Afficher les messages flash
    display_flash_message()
    
    # Sélecteur de période
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.markdown("Analysez les performances de votre boutique sur différentes périodes")
    
    with col2:
        period = st.selectbox(
            "Période",
            options=[7, 30, 90, 365],
            format_func=lambda x: {7: "7 derniers jours", 30: "30 derniers jours", 90: "90 derniers jours", 365: "Année"}[x]
        )
    
    st.divider()
    
    # Métriques principales avec comparaison
    st.subheader("📊 Métriques Clés")
    
    # NOTE: L'erreur TypeError se produit à l'intérieur de cette fonction,
    # qui se trouve dans votre fichier models/analytics.py.
    # C'est LÀ-BAS que la correction pd.to_datetime(..., utc=True) doit être appliquée.
    comparison = Analytics.get_period_comparison(period)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="💰 Chiffre d'Affaires",
            value=format_price(comparison['revenue']['current']),
            delta=f"{comparison['revenue']['delta']:.1f}%",
            delta_color="normal"
        )
    
    with col2:
        st.metric(
            label="📦 Nombre de Commandes",
            value=int(comparison['count']['current']),
            delta=f"{comparison['count']['delta']:.1f}%",
            delta_color="normal"
        )
    
    with col3:
        st.metric(
            label="🛒 Panier Moyen",
            value=format_price(comparison['average_cart']['current']),
            delta=f"{comparison['average_cart']['delta']:.1f}%",
            delta_color="normal"
        )
    
    with col4:
        # Taux de conversion (exemple fictif)
        conversion_rate = 3.5  # Placeholder
        st.metric(
            label="📈 Taux de Conversion",
            value=f"{conversion_rate}%",
            help="Pourcentage de visiteurs qui passent commande"
        )
    
    st.divider()
    
    # Graphiques
    col_left, col_right = st.columns([2, 1])
    
    with col_left:
        # Graphique d'évolution des ventes
        st.subheader("📈 Évolution des Ventes")
        
        sales_data = Analytics.get_sales_evolution(period)
        
        if not sales_data.empty:
            fig = go.Figure()
            
            # Ligne du chiffre d'affaires
            fig.add_trace(go.Scatter(
                x=sales_data['date'],
                y=sales_data['chiffre_affaires'],
                mode='lines+markers',
                name='Chiffre d\'affaires (€)',
                line=dict(color='#3b82f6', width=3),
                marker=dict(size=8)
            ))
            
            # Ligne du nombre de commandes (axe secondaire)
            fig.add_trace(go.Scatter(
                x=sales_data['date'],
                y=sales_data['nb_commandes'],
                mode='lines+markers',
                name='Nombre de commandes',
                line=dict(color='#10b981', width=3),
                marker=dict(size=8),
                yaxis='y2'
            ))
            
            fig.update_layout(
                xaxis_title="Date",
                yaxis_title="Chiffre d'affaires (€)",
                yaxis2=dict(
                    title="Nombre de commandes",
                    overlaying='y',
                    side='right'
                ),
                hovermode='x unified',
                height=400,
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=1.02,
                    xanchor="right",
                    x=1
                )
            )
            
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Pas de données pour cette période")
    
    with col_right:
        # Graphique donut des statuts de commandes
        st.subheader("📊 Répartition des Commandes")
        
        status_stats = Analytics.get_orders_by_status_stats()
        
        labels = []
        values = []
        colors = []
        
        status_config = {
            'en_cours': {'label': 'En cours', 'color': '#3b82f6'},
            'livree': {'label': 'Livrées', 'color': '#10b981'},
            'annulee': {'label': 'Annulées', 'color': '#ef4444'}
        }
        
        for status, count in status_stats.items():
            if count > 0:
                labels.append(status_config[status]['label'])
                values.append(count)
                colors.append(status_config[status]['color'])
        
        if values:
            fig_donut = go.Figure(data=[go.Pie(
                labels=labels,
                values=values,
                hole=0.5,
                marker=dict(colors=colors)
            )])
            
            fig_donut.update_layout(
                height=400,
                showlegend=True,
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=-0.1,
                    xanchor="center",
                    x=0.5
                )
            )
            
            st.plotly_chart(fig_donut, use_container_width=True)
        else:
            st.info("Aucune commande")
    
    st.divider()
    
    # Top produits
    st.subheader("🏆 Top 10 Produits Vendus")
    
    # NOTE (Refactoring): Appel déplacé vers Analytics pour une meilleure séparation des préoccupations.
    # La logique Order.get_top_products() doit être dans models/analytics.py
    top_products = Analytics.get_top_products(limit=10, days=period)
    
    if top_products:
        # Créer un DataFrame pour l'affichage
        df_top = pd.DataFrame(top_products)
        df_top = df_top.rename(columns={
            'product_name': 'Produit',
            'total_quantity': 'Quantité Vendue'
        })
        df_top.index = df_top.index + 1  # Commencer à 1
        
        # Graphique en barres
        fig_bar = px.bar(
            df_top,
            x='Quantité Vendue',
            y='Produit',
            orientation='h',
            text='Quantité Vendue',
            color='Quantité Vendue',
            color_continuous_scale='Blues'
        )
        
        fig_bar.update_layout(
            height=400,
            showlegend=False,
            yaxis={'categoryorder': 'total ascending'}
        )
        
        fig_bar.update_traces(textposition='outside')
        
        st.plotly_chart(fig_bar, use_container_width=True)
        
        # Tableau détaillé
        with st.expander("📋 Voir le tableau détaillé"):
            st.dataframe(df_top, use_container_width=True, hide_index=False)
    else:
        st.info("Aucune vente sur cette période")
    
    st.divider()
    
    # Alertes stock
    st.subheader("⚠️ Alertes Stock")
    
    # NOTE (Refactoring): Les appels à Product.get... ont été
    # regroupés en une seule méthode dans Analytics pour une meilleure abstraction.
    # Vous devez créer Analytics.get_stock_alerts() dans votre modèle.
    # Elle doit renvoyer (list_out_of_stock, list_low_stock)
    out_of_stock, low_stock = Analytics.get_stock_alerts(threshold=5)
    
    col_alert1, col_alert2 = st.columns(2)
    
    with col_alert1:
        # Ruptures de stock
        st.markdown("#### 🚫 Ruptures de Stock")
        
        if out_of_stock:
            st.error(f"{len(out_of_stock)} produit(s) en rupture")
            
            df_out = pd.DataFrame(out_of_stock)
            df_out = df_out[['name', 'type', 'price']]
            df_out = df_out.rename(columns={
                'name': 'Produit',
                'type': 'Type',
                'price': 'Prix'
            })
            df_out['Prix'] = df_out['Prix'].apply(lambda x: format_price(x))
            
            st.dataframe(df_out, use_container_width=True, hide_index=True)
        else:
            st.success("✅ Aucune rupture de stock")
    
    with col_alert2:
        # Stock faible
        st.markdown("#### ⚠️ Stock Faible (≤ 5)")
        
        if low_stock:
            st.warning(f"{len(low_stock)} produit(s) à réapprovisionner")
            
            df_low = pd.DataFrame(low_stock)
            df_low = df_low[['name', 'type', 'stock', 'price']]
            df_low = df_low.rename(columns={
                'name': 'Produit',
                'type': 'Type',
                'stock': 'Stock',
                'price': 'Prix'
            })
            df_low['Prix'] = df_low['Prix'].apply(lambda x: format_price(x))
            
            st.dataframe(df_low, use_container_width=True, hide_index=True)
        else:
            st.success("✅ Tous les stocks sont suffisants")
    
    st.divider()
    
    # Export des données
    st.subheader("📥 Export des Données")
    
    # NOTE (Refactoring): Les données pour l'export sont maintenant 
    # aussi récupérées via le modèle Analytics.
    orders_for_export = Analytics.get_orders_for_export(days=period)
    products_for_export = Analytics.get_products_for_export()
    
    col_exp1, col_exp2 = st.columns(2)
    
    with col_exp1:
        # Export commandes
        if orders_for_export:
            csv_orders = Analytics.export_orders_to_csv(orders_for_export)
            st.download_button(
                label=f"📦 Exporter les commandes ({len(orders_for_export)})",
                data=csv_orders,
                file_name=f"commandes_{period}j_{pd.Timestamp.now().strftime('%Y%m%d')}.csv",
                mime="text/csv",
                use_container_width=True
            )
        else:
            st.button(f"📦 Exporter les commandes (0)", disabled=True, use_container_width=True)
    
    with col_exp2:
        # Export produits
        if products_for_export:
            csv_products = Analytics.export_products_to_csv(products_for_export)
            st.download_button(
                label=f"📦 Exporter les produits ({len(products_for_export)})",
                data=csv_products,
                file_name=f"produits_{pd.Timestamp.now().strftime('%Y%m%d')}.csv",
                mime="text/csv",
                use_container_width=True
            )
        else:
            st.button(f"📦 Exporter les produits (0)", disabled=True, use_container_width=True)

# Exécuter
main()