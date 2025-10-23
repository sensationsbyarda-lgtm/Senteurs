"""
Modèle Analytics pour les statistiques et rapports
"""

from typing import List, Dict
from datetime import datetime, timedelta, timezone  # <-- 1. IMPORT AJOUTÉ
from models.order import Order
from models.product import Product
import pandas as pd

class Analytics:
    """Classe pour gérer les analytics et statistiques"""
    
    @staticmethod
    def get_dashboard_metrics() -> Dict:
        """
        Récupère les métriques principales du dashboard
        
        Returns:
            Dict avec les métriques clés
        """
        all_orders = Order.get_all()
        new_orders = Order.get_new_orders()
        orders_24h = Order.get_orders_last_24h()
        all_products = Product.get_all()
        
        return {
            'total_orders': len(all_orders),
            'new_orders': len(new_orders),
            'orders_24h': len(orders_24h),
            'total_products': len(all_products)
        }
    
    @staticmethod
    def get_sales_evolution(days: int = 30) -> pd.DataFrame:
        """
        Génère les données d'évolution des ventes
        
        Args:
            days: Période en jours
        
        Returns:
            DataFrame avec date, nb_commandes, chiffre_affaires
        """
        orders = Order.get_orders_by_period(days)
        
        # Créer un DataFrame avec toutes les dates
        end_date = datetime.now(timezone.utc) # <-- 2. CORRIGÉ
        start_date = end_date - timedelta(days=days)
        # Assurer que le range est en UTC et normalisé
        date_range = pd.date_range(start=start_date.date(), end=end_date.date(), freq='D', tz='UTC')
        
        df = pd.DataFrame({'date': date_range})
        df['nb_commandes'] = 0
        df['chiffre_affaires'] = 0.0
        
        # Agréger les commandes par jour
        for order in orders:
            # 3. CORRIGÉ : Assurer la conversion en UTC avant de normaliser
            order_date = pd.to_datetime(order['created_at'], utc=True).normalize()
            mask = df['date'] == order_date
            if mask.any():
                df.loc[mask, 'nb_commandes'] += 1
                df.loc[mask, 'chiffre_affaires'] += order['total']
        
        # Formatter en 'jour/mois' pour l'affichage
        df['date'] = df['date'].dt.strftime('%d/%m')
        
        return df
    
    @staticmethod
    def get_orders_by_status_stats() -> Dict:
        """
        Récupère les statistiques des commandes par statut
        
        Returns:
            Dict {status: count}
        """
        all_orders = Order.get_all()
        
        stats = {
            'en_cours': 0,
            'livree': 0,
            'annulee': 0
        }
        
        for order in all_orders:
            status = order.get('status', 'en_cours')
            if status in stats:
                stats[status] += 1
        
        return stats
    
    @staticmethod
    def get_period_comparison(current_days: int) -> Dict:
        """
        Compare les métriques entre la période actuelle et la période précédente
        
        Args:
            current_days: Nombre de jours de la période actuelle
        
        Returns:
            Dict avec current, previous et delta pour chaque métrique
        """
        # Période actuelle
        current_orders = Order.get_orders_by_period(current_days)
        current_revenue = sum(o['total'] for o in current_orders)
        current_count = len(current_orders)
        
        # Période précédente
        # 2. CORRIGÉ : Utiliser timezone.utc
        end_previous = datetime.now(timezone.utc) - timedelta(days=current_days)
        start_previous = end_previous - timedelta(days=current_days)
        
        # Récupérer toutes les commandes et filtrer manuellement
        all_orders = Order.get_all()
        previous_orders = [
            o for o in all_orders
            # 3. CORRIGÉ : Utiliser utc=True pour rendre le datetime "aware"
            if start_previous <= pd.to_datetime(o['created_at'], utc=True) < end_previous
        ]
        
        previous_revenue = sum(o['total'] for o in previous_orders)
        previous_count = len(previous_orders)
        
        # Calculer les deltas
        revenue_delta = ((current_revenue - previous_revenue) / previous_revenue * 100) if previous_revenue > 0 else (100.0 if current_revenue > 0 else 0)
        count_delta = ((current_count - previous_count) / previous_count * 100) if previous_count > 0 else (100.0 if current_count > 0 else 0)
        
        # Calcul du panier moyen
        avg_current = current_revenue / current_count if current_count > 0 else 0
        avg_previous = previous_revenue / previous_count if previous_count > 0 else 0
        avg_delta = ((avg_current - avg_previous) / avg_previous * 100) if avg_previous > 0 else (100.0 if avg_current > 0 else 0)
        
        return {
            'revenue': {
                'current': current_revenue,
                'previous': previous_revenue,
                'delta': revenue_delta
            },
            'count': {
                'current': current_count,
                'previous': previous_count,
                'delta': count_delta
            },
            'average_cart': {
                'current': avg_current,
                'previous': avg_previous,
                'delta': avg_delta
            }
        }
    
    # --- 4. MÉTHODES AJOUTÉES POUR LE REFACTORING ---
    
    @staticmethod
    def get_top_products(limit: int, days: int) -> List[Dict]:
        """
        Récupère les produits les plus vendus sur une période.
        Méthode "façade" pour admin_7_Analyses.
        """
        return Order.get_top_products(limit=limit, days=days)

    @staticmethod
    def get_stock_alerts(threshold: int = 5) -> (List[Dict], List[Dict]):
        """
        Récupère les produits en rupture et en stock faible.
        Méthode "façade" pour admin_7_Analyses.
        """
        out_of_stock = Product.get_out_of_stock_products()
        low_stock_all = Product.get_low_stock_products(threshold=threshold)
        
        # Exclure les produits "out of stock" de la liste "low stock"
        low_stock = [p for p in low_stock_all if p['stock'] > 0]
        
        return out_of_stock, low_stock

    @staticmethod
    def get_orders_for_export(days: int) -> List[Dict]:
        """
        Récupère les commandes pour l'export.
        Méthode "façade" pour admin_7_Analyses.
        """
        return Order.get_orders_by_period(days)

    @staticmethod
    def get_products_for_export() -> List[Dict]:
        """
        Récupère tous les produits pour l'export.
        Méthode "façade" pour admin_7_Analyses.
        """
        return Product.get_all()

    # --- Fin des méthodes ajoutées ---
    
    @staticmethod
    def export_orders_to_csv(orders: List[Dict]) -> str:
        """
        Exporte les commandes en CSV
        """
        data = []
        
        for order in orders:
            client = order.get('clients', {})
            
            # Détails des produits
            products_detail = []
            for item in order.get('order_items', []):
                product = item.get('products', {})
                products_detail.append(f"{product.get('name', 'N/A')} x{item.get('quantity', 0)}")
            
            # 3. CORRIGÉ : Assurer la conversion en UTC
            order_date = pd.to_datetime(order['created_at'], utc=True)
            
            data.append({
                'ID Commande': order['id'],
                # Optionnel: convertir en heure locale pour l'export si besoin
                # 'Date': order_date.tz_convert('Europe/Paris').strftime('%d/%m/%Y %H:%M'),
                'Date': order_date.strftime('%d/%m/%Y %H:%M (UTC)'),
                'Client': f"{client.get('first_name', '')} {client.get('last_name', '')}",
                'Email': client.get('email', ''),
                'Téléphone': client.get('phone', ''),
                'Adresse': client.get('address', ''),
                'Produits': ' | '.join(products_detail),
                'Total': order['total'],
                'Statut': order['status'],
                'Vue': 'Oui' if order['viewed'] else 'Non'
            })
        
        df = pd.DataFrame(data)
        return df.to_csv(index=False, encoding='utf-8-sig')
    
    @staticmethod
    def export_products_to_csv(products: List[Dict]) -> str:
        """
        Exporte les produits en CSV
        """
        data = []
        
        for product in products:
            # 3. CORRIGÉ : Assurer la conversion en UTC
            created_date = pd.to_datetime(product['created_at'], utc=True)
            
            data.append({
                'ID': product['id'],
                'Nom': product['name'],
                'Type': product['type'],
                'Prix': product['price'],
                'Stock': product['stock'],
                'Description': product.get('description', ''),
                'Créé le': created_date.strftime('%d/%m/%Y')
            })
        
        df = pd.DataFrame(data)
        return df.to_csv(index=False, encoding='utf-8-sig')
    
    @staticmethod
    def get_recent_activity(limit: int = 10) -> List[Dict]:
        """
        Récupère l'activité récente (dernières commandes)
        """
        # Trier les commandes pour obtenir les plus récentes
        all_orders = Order.get_all()
        # Supposant que get_all() les retourne déjà triées par 'created_at' desc
        # Sinon, il faudrait trier ici :
        # all_orders.sort(key=lambda x: pd.to_datetime(x['created_at'], utc=True), reverse=True)
        
        orders = all_orders[:limit]
        
        activities = []
        for order in orders:
            client = order.get('clients', {})
            client_name = f"{client.get('first_name', '')} {client.get('last_name', '')}".strip()
            
            activities.append({
                'type': 'order',
                'order_id': order['id'],
                'client_name': client_name if client_name else "Client inconnu",
                'total': order['total'],
                'status': order['status'],
                'created_at': order['created_at'],
                'viewed': order['viewed']
            })
        
        return activities