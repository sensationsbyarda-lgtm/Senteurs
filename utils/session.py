"""
Gestion de la session Streamlit et du panier
"""

import streamlit as st
from typing import Dict, Any

def init_session_state():
    """Initialise les variables de session nécessaires"""
    
    # Panier
    if 'cart' not in st.session_state:
        st.session_state.cart = {}
    
    # Authentification admin
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    
    if 'user' not in st.session_state:
        st.session_state.user = None
    
    # Filtres et recherche
    if 'search_query' not in st.session_state:
        st.session_state.search_query = ""
    
    if 'filter_type' not in st.session_state:
        st.session_state.filter_type = "Tous"
    
    # Messages flash
    if 'flash_message' not in st.session_state:
        st.session_state.flash_message = None
    
    if 'flash_type' not in st.session_state:
        st.session_state.flash_type = "info"

def add_to_cart(product_id: int, product_data: Dict[str, Any], quantity: int = 1) -> bool:
    """
    Ajoute un produit au panier
    
    Args:
        product_id: ID du produit
        product_data: Données du produit (name, price, image, stock)
        quantity: Quantité à ajouter
    
    Returns:
        True si ajout réussi, False sinon
    """
    if 'cart' not in st.session_state:
        st.session_state.cart = {}
    
    # Vérifier le stock
    if quantity > product_data['stock']:
        return False
    
    # Si le produit est déjà dans le panier
    if str(product_id) in st.session_state.cart:
        current_qty = st.session_state.cart[str(product_id)]['quantity']
        new_qty = current_qty + quantity
        
        # Vérifier que la nouvelle quantité ne dépasse pas le stock
        if new_qty > product_data['stock']:
            return False
        
        st.session_state.cart[str(product_id)]['quantity'] = new_qty
    else:
        # Ajouter le produit au panier
        st.session_state.cart[str(product_id)] = {
            'product_id': product_id,
            'name': product_data['name'],
            'price': product_data['price'],
            'quantity': quantity,
            'image': product_data.get('image', ''),
            'stock': product_data['stock']
        }
    
    return True

def update_cart_quantity(product_id: str, quantity: int) -> bool:
    """
    Met à jour la quantité d'un produit dans le panier
    
    Args:
        product_id: ID du produit (string)
        quantity: Nouvelle quantité
    
    Returns:
        True si mise à jour réussie, False sinon
    """
    if 'cart' not in st.session_state:
        return False
    
    if product_id not in st.session_state.cart:
        return False
    
    # Vérifier le stock
    if quantity > st.session_state.cart[product_id]['stock']:
        return False
    
    if quantity <= 0:
        # Supprimer du panier si quantité = 0
        remove_from_cart(product_id)
    else:
        st.session_state.cart[product_id]['quantity'] = quantity
    
    return True

def remove_from_cart(product_id: str):
    """
    Supprime un produit du panier
    
    Args:
        product_id: ID du produit (string)
    """
    if 'cart' not in st.session_state:
        return
    
    if product_id in st.session_state.cart:
        del st.session_state.cart[product_id]

def clear_cart():
    """Vide complètement le panier"""
    st.session_state.cart = {}

def get_cart_total() -> float:
    """
    Calcule le total du panier
    
    Returns:
        Montant total du panier
    """
    if 'cart' not in st.session_state:
        return 0
    
    total = sum(
        item['price'] * item['quantity'] 
        for item in st.session_state.cart.values()
    )
    return total

def get_cart_count() -> int:
    """
    Retourne le nombre total d'articles dans le panier
    
    Returns:
        Nombre total d'articles
    """
    if 'cart' not in st.session_state:
        return 0
    
    return sum(item['quantity'] for item in st.session_state.cart.values())

def set_flash_message(message: str, message_type: str = "info"):
    """
    Définit un message flash à afficher
    
    Args:
        message: Texte du message
        message_type: Type de message (success, error, warning, info)
    """
    st.session_state.flash_message = message
    st.session_state.flash_type = message_type

def display_flash_message():
    """Affiche le message flash s'il existe et le supprime"""
    if st.session_state.get('flash_message'):
        msg_type = st.session_state.get('flash_type', 'info')
        
        if msg_type == 'success':
            st.success(st.session_state.flash_message)
        elif msg_type == 'error':
            st.error(st.session_state.flash_message)
        elif msg_type == 'warning':
            st.warning(st.session_state.flash_message)
        else:
            st.info(st.session_state.flash_message)
        
        # Supprimer le message après affichage
        st.session_state.flash_message = None
        st.session_state.flash_type = 'info'

def login_user(user_data: Dict[str, Any]):
    """
    Connecte un utilisateur (admin)
    
    Args:
        user_data: Données de l'utilisateur (id, email, etc.)
    """
    st.session_state.authenticated = True
    st.session_state.user = user_data

def logout_user():
    """Déconnecte l'utilisateur"""
    st.session_state.authenticated = False
    st.session_state.user = None

def require_auth(func):
    """
    Décorateur pour protéger les pages admin
    Redirige vers la page de login si non authentifié
    """
    def wrapper(*args, **kwargs):
        if not st.session_state.get('authenticated', False):
            st.warning("⚠️ Vous devez être connecté pour accéder à cette page.")
            if st.button("🔐 Se connecter"):
                st.switch_page("pages/admin_login.py")
            st.stop()
        return func(*args, **kwargs)
    return wrapper