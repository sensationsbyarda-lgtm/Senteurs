"""
Modèle Client avec méthodes CRUD
"""

from typing import List, Dict, Optional
from config.supabase_client import get_supabase
import streamlit as st

class Client:
    """Classe pour gérer les clients"""
    
    @staticmethod
    def create(first_name: str, last_name: str, email: str, phone: str, address: str) -> Optional[Dict]:
        """
        Crée un nouveau client
        
        Args:
            first_name: Prénom
            last_name: Nom
            email: Email
            phone: Téléphone
            address: Adresse
        
        Returns:
            Données du client créé ou None
        """
        try:
            supabase = get_supabase()
            
            client_data = {
                'first_name': first_name,
                'last_name': last_name,
                'email': email,
                'phone': phone,
                'address': address
            }
            
            response = supabase.table('clients').insert(client_data).execute()
            return response.data[0] if response.data else None
        
        except Exception as e:
            st.error(f"Erreur lors de la création du client: {str(e)}")
            return None
    
    @staticmethod
    def get_by_id(client_id: int) -> Optional[Dict]:
        """
        Récupère un client par son ID
        
        Args:
            client_id: ID du client
        
        Returns:
            Données du client ou None
        """
        try:
            supabase = get_supabase()
            response = supabase.table('clients').select('*').eq('id', client_id).single().execute()
            return response.data
        except Exception as e:
            st.error(f"Erreur lors de la récupération du client: {str(e)}")
            return None
    
    @staticmethod
    def get_by_email(email: str) -> Optional[Dict]:
        """
        Récupère un client par son email
        
        Args:
            email: Email du client
        
        Returns:
            Données du client ou None
        """
        try:
            supabase = get_supabase()
            response = supabase.table('clients').select('*').eq('email', email).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            return None
    
    @staticmethod
    def get_all() -> List[Dict]:
        """
        Récupère tous les clients
        
        Returns:
            Liste des clients
        """
        try:
            supabase = get_supabase()
            response = supabase.table('clients').select('*').order('created_at', desc=True).execute()
            return response.data if response.data else []
        except Exception as e:
            st.error(f"Erreur lors de la récupération des clients: {str(e)}")
            return []
    
    @staticmethod
    def update(client_id: int, first_name: str, last_name: str, email: str, phone: str, address: str) -> bool:
        """
        Met à jour un client
        
        Args:
            client_id: ID du client
            first_name: Nouveau prénom
            last_name: Nouveau nom
            email: Nouvel email
            phone: Nouveau téléphone
            address: Nouvelle adresse
        
        Returns:
            True si succès, False sinon
        """
        try:
            supabase = get_supabase()
            
            update_data = {
                'first_name': first_name,
                'last_name': last_name,
                'email': email,
                'phone': phone,
                'address': address
            }
            
            supabase.table('clients').update(update_data).eq('id', client_id).execute()
            return True
        
        except Exception as e:
            st.error(f"Erreur lors de la mise à jour du client: {str(e)}")
            return False