"""
Fonctions de formatage des données (prix, dates, etc.)
"""

from datetime import datetime
from typing import Union

def format_price(price: Union[int, float], include_currency: bool = True) -> str:
    """
    Formate un prix au format français (espace comme séparateur de milliers)
    
    Args:
        price: Prix à formater
        include_currency: Inclure le symbole € ou non
    
    Returns:
        Prix formaté (ex: "25 000 €" ou "25 000")
    """
    if price is None:
        return "0 €" if include_currency else "0"
    
    # Convertir en entier (pas de décimales)
    price_int = int(price)
    
    # Formater avec espace comme séparateur de milliers
    formatted = f"{price_int:,}".replace(",", " ")
    
    if include_currency:
        return f"{formatted} €"
    
    return formatted

def format_date(date: Union[datetime, str], format_type: str = "full") -> str:
    """
    Formate une date
    
    Args:
        date: Date à formater (datetime ou string ISO)
        format_type: Type de format ("full", "short", "time")
    
    Returns:
        Date formatée
    """
    if isinstance(date, str):
        try:
            date = datetime.fromisoformat(date.replace('Z', '+00:00'))
        except:
            return date
    
    if format_type == "full":
        return date.strftime("%d/%m/%Y à %H:%M")
    elif format_type == "short":
        return date.strftime("%d/%m/%Y")
    elif format_type == "time":
        return date.strftime("%H:%M")
    else:
        return date.strftime("%d/%m/%Y")

def format_phone(phone: str) -> str:
    """
    Formate un numéro de téléphone français
    
    Args:
        phone: Numéro de téléphone
    
    Returns:
        Numéro formaté (ex: "06 12 34 56 78")
    """
    # Enlever tous les caractères non numériques
    digits = ''.join(filter(str.isdigit, phone))
    
    # Formater par paires
    if len(digits) == 10:
        return f"{digits[0:2]} {digits[2:4]} {digits[4:6]} {digits[6:8]} {digits[8:10]}"
    
    return phone

def format_stock_badge(stock: int) -> str:
    """
    Génère un badge HTML pour l'état du stock
    
    Args:
        stock: Quantité en stock
    
    Returns:
        HTML du badge
    """
    if stock <= 0:
        return '<span class="out-of-stock">Rupture de stock</span>'
    elif stock <= 5:
        return f'<span style="background: #fef3c7; color: #92400e; padding: 0.25rem 0.75rem; border-radius: 9999px; font-size: 0.75rem; font-weight: 600;">Stock faible ({stock})</span>'
    else:
        return f'<span style="background: #d1fae5; color: #065f46; padding: 0.25rem 0.75rem; border-radius: 9999px; font-size: 0.75rem; font-weight: 600;">En stock ({stock})</span>'

def format_order_status(status: str) -> str:
    """
    Formate le statut d'une commande avec un badge HTML
    
    Args:
        status: Statut de la commande
    
    Returns:
        HTML du badge de statut
    """
    status_config = {
        "en_cours": {
            "label": "En cours",
            "color": "#3b82f6",
            "bg": "#dbeafe"
        },
        "livree": {
            "label": "Livrée",
            "color": "#059669",
            "bg": "#d1fae5"
        },
        "annulee": {
            "label": "Annulée",
            "color": "#dc2626",
            "bg": "#fee2e2"
        }
    }
    
    config = status_config.get(status, status_config["en_cours"])
    
    return f'<span style="background: {config["bg"]}; color: {config["color"]}; padding: 0.25rem 0.75rem; border-radius: 9999px; font-size: 0.875rem; font-weight: 600;">{config["label"]}</span>'

def truncate_text(text: str, max_length: int = 100, suffix: str = "...") -> str:
    """
    Tronque un texte à une longueur maximale
    
    Args:
        text: Texte à tronquer
        max_length: Longueur maximale
        suffix: Suffixe à ajouter si tronqué
    
    Returns:
        Texte tronqué
    """
    if not text:
        return ""
    
    if len(text) <= max_length:
        return text
    
    return text[:max_length].rsplit(' ', 1)[0] + suffix

def format_relative_time(date: Union[datetime, str]) -> str:
    """
    Formate une date en temps relatif (il y a X minutes/heures/jours)
    
    Args:
        date: Date à formater
    
    Returns:
        Temps relatif formaté
    """
    if isinstance(date, str):
        try:
            date = datetime.fromisoformat(date.replace('Z', '+00:00'))
        except:
            return date
    
    now = datetime.now(date.tzinfo)
    diff = now - date
    
    seconds = diff.total_seconds()
    
    if seconds < 60:
        return "À l'instant"
    elif seconds < 3600:
        minutes = int(seconds / 60)
        return f"Il y a {minutes} minute{'s' if minutes > 1 else ''}"
    elif seconds < 86400:
        hours = int(seconds / 3600)
        return f"Il y a {hours} heure{'s' if hours > 1 else ''}"
    elif seconds < 604800:
        days = int(seconds / 86400)
        return f"Il y a {days} jour{'s' if days > 1 else ''}"
    else:
        return format_date(date, "short")

def pluralize(count: int, singular: str, plural: str = None) -> str:
    """
    Gère le pluriel en français
    
    Args:
        count: Nombre
        singular: Forme singulière
        plural: Forme plurielle (optionnel, ajoute 's' par défaut)
    
    Returns:
        Forme correcte avec le nombre
    """
    if plural is None:
        plural = singular + "s"
    
    return f"{count} {singular if count <= 1 else plural}"