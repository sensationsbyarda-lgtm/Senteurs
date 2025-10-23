"""
Modèle Product avec méthodes CRUD
"""

from typing import List, Dict, Optional
from config.supabase_client import get_supabase
import streamlit as st

class Product:
    """Classe pour gérer les produits"""
    
    @staticmethod
    def get_all(search: str = "", filter_type: str = "Tous") -> List[Dict]:
        """
        Récupère tous les produits avec filtres optionnels
        
        Args:
            search: Terme de recherche
            filter_type: Filtre par type (Homme/Femme/Mixte/Tous)
        
        Returns:
            Liste des produits
        """
        try:
            supabase = get_supabase()
            
            # Requête de base
            query = supabase.table('products').select('*, product_images(*)')
            
            # Appliquer le filtre de type
            if filter_type != "Tous":
                query = query.eq('type', filter_type)
            
            # Appliquer la recherche
            if search:
                # --- CORRECTION APPLIQUÉE ICI ---
                # C'était .%search}%' au lieu de .%{search}%'
                query = query.or_(f'name.ilike.%{search}%,description.ilike.%{search}%')
            
            # Trier par nom
            query = query.order('name')
            
            response = query.execute()
            return response.data if response.data else []
        
        except Exception as e:
            st.error(f"Erreur lors de la récupération des produits: {str(e)}")
            return []
    
    @staticmethod
    def get_by_id(product_id: int) -> Optional[Dict]:
        """
        Récupère un produit par son ID
        
        Args:
            product_id: ID du produit
        
        Returns:
            Données du produit ou None
        """
        try:
            supabase = get_supabase()
            response = supabase.table('products').select('*, product_images(*)').eq('id', product_id).single().execute()
            return response.data
        except Exception as e:
            st.error(f"Erreur lors de la récupération du produit: {str(e)}")
            return None
    
    @staticmethod
    def create(name: str, type: str, description: str, price: float, stock: int, image_urls: List[str] = None) -> Optional[Dict]:
        """
        Crée un nouveau produit
        """
        try:
            supabase = get_supabase()
            
            # Créer le produit
            product_data = {
                'name': name,
                'type': type,
                'description': description,
                'price': price,
                'stock': stock
            }
            
            response = supabase.table('products').insert(product_data).execute()
            
            if not response.data:
                return None
            
            product = response.data[0]
            
            # Ajouter les images si fournies
            if image_urls:
                for url in image_urls:
                    supabase.table('product_images').insert({
                        'product_id': product['id'],
                        'url': url
                    }).execute()
            
            return product
        
        except Exception as e:
            st.error(f"Erreur lors de la création du produit: {str(e)}")
            print(f"--- ERREUR DB CREATE ---: {str(e)}") # Affiche l'erreur dans le terminal
            return None
    
    @staticmethod
    def update(product_id: int, name: str, type: str, description: str, price: float, stock: int) -> bool:
        """
        Met à jour un produit
        """
        try:
            supabase = get_supabase()
            
            update_data = {
                'name': name,
                'type': type,
                'description': description,
                'price': price,
                'stock': stock
            }
            
            supabase.table('products').update(update_data).eq('id', product_id).execute()
            return True
        
        except Exception as e:
            st.error(f"Erreur lors de la mise à jour du produit: {str(e)}")
            return False
    
    @staticmethod
    def delete(product_id: int) -> bool:
        """
        Supprime un produit
        """
        try:
            supabase = get_supabase()
            
            # Supprimer d'abord les images associées
            supabase.table('product_images').delete().eq('product_id', product_id).execute()
            
            # Supprimer le produit
            supabase.table('products').delete().eq('id', product_id).execute()
            return True
        
        except Exception as e:
            st.error(f"Erreur lors de la suppression du produit: {str(e)}")
            return False
    
    @staticmethod
    def update_stock(product_id: int, quantity_change: int) -> bool:
        """
        Met à jour le stock d'un produit (incrémentation ou décrémentation)
        """
        try:
            supabase = get_supabase()
            
            # Récupérer le stock actuel
            product = Product.get_by_id(product_id)
            if not product:
                return False
            
            new_stock = product['stock'] + quantity_change
            
            # S'assurer que le stock ne devient pas négatif
            if new_stock < 0:
                return False
            
            # Mettre à jour le stock
            supabase.table('products').update({'stock': new_stock}).eq('id', product_id).execute()
            return True
        
        except Exception as e:
            st.error(f"Erreur lors de la mise à jour du stock: {str(e)}")
            return False

    @staticmethod
    def add_image(product_id: int, image_url: str) -> bool:
        """
        Ajoute une image à un produit
        """
        try:
            supabase = get_supabase()
            supabase.table('product_images').insert({
                'product_id': product_id,
                'url': image_url
            }).execute()
            return True
        except Exception as e:
            st.error(f"Erreur lors de l'ajout de l'image: {str(e)}")
            print(f"--- ERREUR DB ADD_IMAGE ---: {str(e)}") # Affiche l'erreur dans le terminal
            return False
    
    @staticmethod
    def delete_image(image_id: int) -> bool:
        """
        Supprime une image
        """
        try:
            supabase = get_supabase()
            supabase.table('product_images').delete().eq('id', image_id).execute()
            return True
        except Exception as e:
            st.error(f"Erreur lors de la suppression de l'image: {str(e)}")
            return False
    
    @staticmethod
    def get_low_stock_products(threshold: int = 5) -> List[Dict]:
        """
        Récupère les produits avec un stock faible
        """
        try:
            supabase = get_supabase()
            response = supabase.table('products').select('*').lte('stock', threshold).order('stock').execute()
            return response.data if response.data else []
        except Exception as e:
            st.error(f"Erreur lors de la récupération des produits en rupture: {str(e)}")
            return []
    
    @staticmethod
    def get_out_of_stock_products() -> List[Dict]:
        """
        Récupère les produits en rupture de stock
        """
        return Product.get_low_stock_products(threshold=0)