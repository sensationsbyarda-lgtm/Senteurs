"""
Fonctions de validation des données
"""

import re
from email_validator import validate_email, EmailNotValidError
import phonenumbers

def validate_email_address(email: str) -> tuple[bool, str]:
    """
    Valide une adresse email
    
    Args:
        email: Adresse email à valider
    
    Returns:
        Tuple (is_valid, error_message)
    """
    if not email or email.strip() == "":
        return False, "L'email est requis"
    
    try:
        validate_email(email)
        return True, ""
    except EmailNotValidError as e:
        return False, "Format d'email invalide"

def validate_phone(phone: str) -> tuple[bool, str]:
    """
    Valide un numéro de téléphone
    
    Args:
        phone: Numéro de téléphone à valider
    
    Returns:
        Tuple (is_valid, error_message)
    """
    if not phone or phone.strip() == "":
        return False, "Le numéro de téléphone est requis"
    
    try:
        # Parser le numéro (assume France par défaut)
        parsed = phonenumbers.parse(phone, "FR")
        if phonenumbers.is_valid_number(parsed):
            return True, ""
        else:
            return False, "Numéro de téléphone invalide"
    except phonenumbers.NumberParseException:
        return False, "Format de téléphone invalide"

def validate_name(name: str, field_name: str = "Nom") -> tuple[bool, str]:
    """
    Valide un nom (prénom ou nom de famille)
    
    Args:
        name: Nom à valider
        field_name: Nom du champ (pour le message d'erreur)
    
    Returns:
        Tuple (is_valid, error_message)
    """
    if not name or name.strip() == "":
        return False, f"{field_name} est requis"
    
    if len(name.strip()) < 2:
        return False, f"{field_name} doit contenir au moins 2 caractères"
    
    if len(name.strip()) > 50:
        return False, f"{field_name} ne peut pas dépasser 50 caractères"
    
    # Vérifier que le nom ne contient que des lettres, espaces, tirets et apostrophes
    if not re.match(r"^[a-zA-ZÀ-ÿ\s\-']+$", name):
        return False, f"{field_name} ne peut contenir que des lettres"
    
    return True, ""

def validate_address(address: str) -> tuple[bool, str]:
    """
    Valide une adresse postale
    
    Args:
        address: Adresse à valider
    
    Returns:
        Tuple (is_valid, error_message)
    """
    if not address or address.strip() == "":
        return False, "L'adresse est requise"
    
    if len(address.strip()) < 10:
        return False, "L'adresse semble trop courte (minimum 10 caractères)"
    
    if len(address.strip()) > 200:
        return False, "L'adresse ne peut pas dépasser 200 caractères"
    
    return True, ""

def validate_product_name(name: str) -> tuple[bool, str]:
    """
    Valide le nom d'un produit
    
    Args:
        name: Nom du produit
    
    Returns:
        Tuple (is_valid, error_message)
    """
    if not name or name.strip() == "":
        return False, "Le nom du produit est requis"
    
    if len(name.strip()) < 3:
        return False, "Le nom doit contenir au moins 3 caractères"
    
    if len(name.strip()) > 100:
        return False, "Le nom ne peut pas dépasser 100 caractères"
    
    return True, ""

def validate_price(price: float) -> tuple[bool, str]:
    """
    Valide un prix
    
    Args:
        price: Prix à valider
    
    Returns:
        Tuple (is_valid, error_message)
    """
    if price is None:
        return False, "Le prix est requis"
    
    if price < 0:
        return False, "Le prix ne peut pas être négatif"
    
    if price > 1000000:
        return False, "Le prix semble anormalement élevé"
    
    return True, ""

def validate_stock(stock: int) -> tuple[bool, str]:
    """
    Valide une quantité de stock
    
    Args:
        stock: Quantité de stock
    
    Returns:
        Tuple (is_valid, error_message)
    """
    if stock is None:
        return False, "Le stock est requis"
    
    if stock < 0:
        return False, "Le stock ne peut pas être négatif"
    
    if stock > 10000:
        return False, "Le stock semble anormalement élevé"
    
    return True, ""

def validate_product_type(product_type: str) -> tuple[bool, str]:
    """
    Valide le type de produit
    
    Args:
        product_type: Type de produit
    
    Returns:
        Tuple (is_valid, error_message)
    """
    valid_types = ["Homme", "Femme", "Mixte"]
    
    if not product_type or product_type not in valid_types:
        return False, f"Le type doit être parmi: {', '.join(valid_types)}"
    
    return True, ""

def validate_checkout_form(first_name: str, last_name: str, email: str, 
                          phone: str, address: str) -> dict:
    """
    Valide tous les champs du formulaire de checkout
    
    Args:
        first_name: Prénom
        last_name: Nom
        email: Email
        phone: Téléphone
        address: Adresse
    
    Returns:
        Dict avec 'is_valid' (bool) et 'errors' (dict)
    """
    errors = {}
    
    # Valider prénom
    is_valid, error = validate_name(first_name, "Le prénom")
    if not is_valid:
        errors['first_name'] = error
    
    # Valider nom
    is_valid, error = validate_name(last_name, "Le nom")
    if not is_valid:
        errors['last_name'] = error
    
    # Valider email
    is_valid, error = validate_email_address(email)
    if not is_valid:
        errors['email'] = error
    
    # Valider téléphone
    is_valid, error = validate_phone(phone)
    if not is_valid:
        errors['phone'] = error
    
    # Valider adresse
    is_valid, error = validate_address(address)
    if not is_valid:
        errors['address'] = error
    
    return {
        'is_valid': len(errors) == 0,
        'errors': errors
    }

def validate_product_form(name: str, product_type: str, price: float, 
                         stock: int, description: str = "") -> dict:
    """
    Valide tous les champs du formulaire produit
    
    Args:
        name: Nom du produit
        product_type: Type de produit
        price: Prix
        stock: Stock
        description: Description (optionnelle)
    
    Returns:
        Dict avec 'is_valid' (bool) et 'errors' (dict)
    """
    errors = {}
    
    # Valider nom
    is_valid, error = validate_product_name(name)
    if not is_valid:
        errors['name'] = error
    
    # Valider type
    is_valid, error = validate_product_type(product_type)
    if not is_valid:
        errors['type'] = error
    
    # Valider prix
    is_valid, error = validate_price(price)
    if not is_valid:
        errors['price'] = error
    
    # Valider stock
    is_valid, error = validate_stock(stock)
    if not is_valid:
        errors['stock'] = error
    
    # Description optionnelle mais limitée
    if description and len(description) > 1000:
        errors['description'] = "La description ne peut pas dépasser 1000 caractères"
    
    return {
        'is_valid': len(errors) == 0,
        'errors': errors
    }