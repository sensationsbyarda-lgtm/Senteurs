"""
Modèle Order avec méthodes CRUD et logique métier
"""

from typing import List, Dict, Optional
from datetime import datetime, timedelta
from config.supabase_client import get_supabase
from models.product import Product
import streamlit as st

class Order:
    """Classe pour gérer les commandes"""
    
    @staticmethod
    def create(client_id: int, cart_items: Dict, total: float) -> Optional[Dict]:
        """
        Crée une nouvelle commande et ses items
        
        Args:
            client_id: ID du client
            cart_items: Items du panier {product_id: {quantity, price, name}}
            total: Total de la commande
        
        Returns:
            Données de la commande créée ou None
        """
        try:
            supabase = get_supabase()
            
            # Créer la commande
            order_data = {
                'client_id': client_id,
                'total': total,
                'status': 'en_cours',
                'viewed': False
            }
            
            response = supabase.table('orders').insert(order_data).execute()
            
            if not response.data:
                return None
            
            order = response.data[0]
            order_id = order['id']
            
            # Créer les items et mettre à jour les stocks
            for product_id, item in cart_items.items():
                # Créer l'item de commande
                order_item = {
                    'order_id': order_id,
                    'product_id': int(product_id),
                    'quantity': item['quantity'],
                    'price': item['price']
                }
                supabase.table('order_items').insert(order_item).execute()
                
                # Décrémenter le stock
                Product.update_stock(int(product_id), -item['quantity'])
            
            return order
        
        except Exception as e:
            st.error(f"Erreur lors de la création de la commande: {str(e)}")
            return None
    
    @staticmethod
    def get_all() -> List[Dict]:
        """
        Récupère toutes les commandes avec les infos client
        
        Returns:
            Liste des commandes
        """
        try:
            supabase = get_supabase()
            response = supabase.table('orders').select('*, clients(*), order_items(*, products(*))').order('created_at', desc=True).execute()
            return response.data if response.data else []
        except Exception as e:
            st.error(f"Erreur lors de la récupération des commandes: {str(e)}")
            return []
    
    @staticmethod
    def get_by_id(order_id: int) -> Optional[Dict]:
        """
        Récupère une commande par son ID avec tous les détails
        
        Args:
            order_id: ID de la commande
        
        Returns:
            Données de la commande ou None
        """
        try:
            supabase = get_supabase()
            response = supabase.table('orders').select('*, clients(*), order_items(*, products(*))').eq('id', order_id).single().execute()
            return response.data
        except Exception as e:
            st.error(f"Erreur lors de la récupération de la commande: {str(e)}")
            return None
    
    @staticmethod
    def get_new_orders() -> List[Dict]:
        """
        Récupère les commandes non vues
        
        Returns:
            Liste des nouvelles commandes
        """
        try:
            supabase = get_supabase()
            response = supabase.table('orders').select('*, clients(*), order_items(*, products(*))').eq('viewed', False).order('created_at', desc=True).execute()
            return response.data if response.data else []
        except Exception as e:
            st.error(f"Erreur lors de la récupération des nouvelles commandes: {str(e)}")
            return []
    
    @staticmethod
    def get_orders_last_24h() -> List[Dict]:
        """
        Récupère les commandes des dernières 24 heures
        
        Returns:
            Liste des commandes
        """
        try:
            supabase = get_supabase()
            yesterday = (datetime.now() - timedelta(hours=24)).isoformat()
            response = supabase.table('orders').select('*').gte('created_at', yesterday).execute()
            return response.data if response.data else []
        except Exception as e:
            st.error(f"Erreur lors de la récupération des commandes 24h: {str(e)}")
            return []
    
    @staticmethod
    def update_status(order_id: int, new_status: str) -> bool:
        """
        Met à jour le statut d'une commande
        
        Args:
            order_id: ID de la commande
            new_status: Nouveau statut (en_cours, livree, annulee)
        
        Returns:
            True si succès, False sinon
        """
        try:
            supabase = get_supabase()
            supabase.table('orders').update({'status': new_status}).eq('id', order_id).execute()
            return True
        except Exception as e:
            st.error(f"Erreur lors de la mise à jour du statut: {str(e)}")
            return False
    
    @staticmethod
    def mark_as_viewed(order_id: int) -> bool:
        """
        Marque une commande comme vue
        
        Args:
            order_id: ID de la commande
        
        Returns:
            True si succès, False sinon
        """
        try:
            supabase = get_supabase()
            supabase.table('orders').update({'viewed': True}).eq('id', order_id).execute()
            return True
        except Exception as e:
            st.error(f"Erreur lors du marquage de la commande: {str(e)}")
            return False
    
    @staticmethod
    def get_orders_by_period(days: int) -> List[Dict]:
        """
        Récupère les commandes d'une période donnée
        
        Args:
            days: Nombre de jours (7, 30, 90, 365)
        
        Returns:
            Liste des commandes
        """
        try:
            supabase = get_supabase()
            start_date = (datetime.now() - timedelta(days=days)).isoformat()
            response = supabase.table('orders').select('*, order_items(*, products(*))').gte('created_at', start_date).order('created_at').execute()
            return response.data if response.data else []
        except Exception as e:
            st.error(f"Erreur lors de la récupération des commandes par période: {str(e)}")
            return []
    
    @staticmethod
    def get_orders_by_status(status: str) -> List[Dict]:
        """
        Récupère les commandes par statut
        
        Args:
            status: Statut à filtrer
        
        Returns:
            Liste des commandes
        """
        try:
            supabase = get_supabase()
            response = supabase.table('orders').select('*, clients(*), order_items(*, products(*))').eq('status', status).order('created_at', desc=True).execute()
            return response.data if response.data else []
        except Exception as e:
            st.error(f"Erreur lors de la récupération des commandes par statut: {str(e)}")
            return []
    
    @staticmethod
    def get_total_revenue(days: int = None) -> float:
        """
        Calcule le chiffre d'affaires total
        
        Args:
            days: Période en jours (None = tout)
        
        Returns:
            Chiffre d'affaires total
        """
        try:
            orders = Order.get_orders_by_period(days) if days else Order.get_all()
            return sum(order['total'] for order in orders)
        except Exception as e:
            return 0.0
    
    @staticmethod
    def get_top_products(limit: int = 10, days: int = None) -> List[Dict]:
        """
        Récupère les produits les plus vendus
        
        Args:
            limit: Nombre de produits à retourner
            days: Période en jours (None = tout)
        
        Returns:
            Liste des produits avec quantités vendues
        """
        try:
            supabase = get_supabase()
            
            # Construire la requête
            query = supabase.table('order_items').select('product_id, quantity, products(name), orders(created_at)')
            
            # Filtrer par période si spécifié
            if days:
                start_date = (datetime.now() - timedelta(days=days)).isoformat()
                query = query.gte('orders.created_at', start_date)
            
            response = query.execute()
            
            if not response.data:
                return []
            
            # Agréger les quantités par produit
            product_sales = {}
            for item in response.data:
                product_id = item['product_id']
                product_name = item['products']['name'] if item.get('products') else f"Produit {product_id}"
                quantity = item['quantity']
                
                if product_id not in product_sales:
                    product_sales[product_id] = {
                        'product_id': product_id,
                        'product_name': product_name,
                        'total_quantity': 0
                    }
                
                product_sales[product_id]['total_quantity'] += quantity
            
            # Trier par quantité décroissante
            sorted_products = sorted(product_sales.values(), key=lambda x: x['total_quantity'], reverse=True)
            
            return sorted_products[:limit]
        
        except Exception as e:
            st.error(f"Erreur lors de la récupération des top produits: {str(e)}")
            return []
    
    @staticmethod
    def validate_cart_stock(cart_items: Dict) -> Dict[str, bool]:
        """
        Vérifie que tous les produits du panier ont un stock suffisant
        
        Args:
            cart_items: Items du panier {product_id: {quantity, ...}}
        
        Returns:
            Dict {product_id: is_available}
        """
        availability = {}
        
        for product_id, item in cart_items.items():
            product = Product.get_by_id(int(product_id))
            if product:
                availability[product_id] = product['stock'] >= item['quantity']
            else:
                availability[product_id] = False
        
        return availability