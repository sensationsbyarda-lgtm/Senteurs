"""
Configuration et initialisation du client Supabase
"""

import os
import streamlit as st
from supabase import create_client, Client




def init_supabase() -> Client:
    """
    Initialise et retourne le client Supabase
    Utilise st.session_state pour cache le client
    """
    if 'supabase' not in st.session_state:
        url = os.getenv('SUPABASE_URL')
        key = os.getenv('SUPABASE_KEY') # Clé publique ANON
        
        if not url or not key:
            st.error("⚠️ Configuration Supabase manquante. Vérifiez votre fichier .env")
            st.stop()
        
        try:
            # Crée un client ANONYME. Il sera mis à jour après le login.
            st.session_state.supabase = create_client(url, key)
        except Exception as e:
            st.error(f"❌ Erreur de connexion à Supabase: {str(e)}")
            st.stop()
    
    return st.session_state.supabase

def get_supabase() -> Client:
    """Retourne le client Supabase depuis la session"""
    if 'supabase' not in st.session_state:
        return init_supabase()
    return st.session_state.supabase

# --- AJOUTÉ ---
def set_supabase_session(session):
    """
    Met à jour le client Supabase en cache avec la session de l'utilisateur
    et stocke les tokens dans st.session_state.
    
    À appeler DEPUIS VOTRE PAGE DE LOGIN après un 'sign_in'.
    """
    try:
        client = get_supabase()
        client.auth.set_session(
            session.access_token,
            session.refresh_token
        )
        
        # Stocker les tokens pour les recharges de page
        st.session_state.auth_token = session.access_token
        st.session_state.auth_refresh_token = session.refresh_token
        st.session_state.authenticated = True
        st.session_state.user = {'email': session.user.email, 'id': session.user.id}
    except Exception as e:
        st.error(f"Erreur lors de la configuration de la session: {e}")

# --- AJOUTÉ ---
def clear_supabase_session():
    """
    Déconnecte l'utilisateur et nettoie st.session_state.
    
    À appeler DEPUIS VOTRE BOUTON DE DÉCONNEXION.
    """
    try:
        client = get_supabase()
        client.auth.sign_out()
    except Exception:
        pass # Ignorer les erreurs si déjà déconnecté
    
    # Nettoyer st.session_state
    keys_to_del = ['auth_token', 'auth_refresh_token', 'authenticated', 'user']
    for key in keys_to_del:
        if key in st.session_state:
            del st.session_state[key]
    
    # Forcer la recréation du client anonyme au prochain get
    if 'supabase' in st.session_state:
        del st.session_state.supabase

# --- AJOUTÉ ---
def load_supabase_session():
    """
    Assure que le client Supabase a la session stockée.
    
    À appeler AU DÉBUT de chaque page admin sécurisée.
    """
    client = get_supabase()
    if st.session_state.get("authenticated") and "auth_token" in st.session_state:
        try:
            client.auth.set_session(
                st.session_state["auth_token"],
                st.session_state.get("auth_refresh_token")
            )
        except Exception:
            # Le token a peut-être expiré, forcer la déconnexion
            clear_supabase_session()
            st.warning("Votre session a expiré. Veuillez vous reconnecter.")
            st.switch_page("pages/admin_login.py")
            st.stop()

# --- SUPPRIMÉ ---
# La fonction get_storage_url construisait une URL manuellement, ce qui est risqué.
# Il est préférable d'utiliser client.storage.from_().get_public_url()

def upload_file(bucket: str, file, path: str) -> dict:
    """
    Upload un fichier vers Supabase Storage
    """
    try:
        # Récupère le client (qui sera authentifié si load_supabase_session a été appelé)
        supabase = get_supabase()
        
        # Rembobiner le fichier avant de le lire
        file.seek(0)
        file_bytes = file.read()
        
        # Upload vers Supabase
        supabase.storage.from_(bucket).upload(
            path=path,
            file=file_bytes,
            file_options={"content-type": file.type}
        )
        
        # --- CORRIGÉ ---
        # Utiliser la méthode client pour obtenir l'URL, pas une fonction manuelle
        public_url = supabase.storage.from_(bucket).get_public_url(path)
        
        return {
            'success': True,
            'url': public_url
        }
    
    except Exception as e:
        # Renvoyer l'erreur complète pour un meilleur débogage
        error_str = str(e)
        if "new row violates row-level security policy" in error_str:
             print("--- ERREUR RLS DÉTECTÉE --- Vérifiez que le client est authentifié ET que les policies RLS sont bonnes.")
        
        return {
            'success': False,
            'error': error_str
        }

def delete_file(bucket: str, path: str) -> bool:
    """
    Supprime un fichier de Supabase Storage
    """
    try:
        supabase = get_supabase()
        supabase.storage.from_(bucket).remove([path])
        return True
    except Exception as e:
        st.error(f"Erreur lors de la suppression: {str(e)}")
        return False