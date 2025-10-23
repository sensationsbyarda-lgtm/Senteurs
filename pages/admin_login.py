"""
Page de connexion Admin
"""

import streamlit as st
# --- MODIFIÉ ---
from config.supabase_client import init_supabase, get_supabase, set_supabase_session
from utils.session import init_session_state, display_flash_message
# --- FIN MODIFIÉ ---

# Configuration
st.set_page_config(page_title="Admin Login - Sensations Arda", page_icon="🔐", layout="centered")

# Initialisation
init_supabase() # Initialise le client (anonyme pour l'instant)
init_session_state()

# Vérifier si déjà connecté
if st.session_state.get('authenticated', False):
    st.success("✅ Vous êtes déjà connecté !")
    if st.button("📊 Accéder au dashboard"):
        st.switch_page("pages/admin_4_Dashboard.py")
    if st.button("🏠 Retour à l'accueil"):
        st.switch_page("app.py")
    st.stop()

# En-tête
st.title("🔐 Connexion Administrateur")
st.markdown("Accédez à l'interface d'administration de Sensations Arda")

# Afficher les messages flash
display_flash_message()

st.divider()

# Formulaire de connexion
with st.form("login_form"):
    email = st.text_input("Email", placeholder="admin@sensations-arda.com")
    password = st.text_input("Mot de passe", type="password", placeholder="••••••••")
    
    submit = st.form_submit_button("Se connecter", use_container_width=True, type="primary")

    if submit:
        supabase = get_supabase()
        try:
            response = supabase.auth.sign_in_with_password({
                "email": email,
                "password": password,
            })
            
            # --- CORRIGÉ ---
            # Au lieu d'appeler login_user, nous appelons set_supabase_session
            # qui met à jour le client ET st.session_state
            if response.session:
                # Connexion réussie
                set_supabase_session(response.session)
                
                st.success("✅ Connexion réussie ! Redirection...")
                st.balloons()
                
                st.switch_page("pages/admin_4_Dashboard.py")
            else:
                st.error("❌ Email ou mot de passe incorrect")
            # --- FIN CORRIGÉ ---
        
        except Exception as e:
            error_msg = str(e)
            if "Invalid login credentials" in error_msg:
                st.error("❌ Email ou mot de passe incorrect")
            elif "Email not confirmed" in error_msg:
                st.error("❌ Veuillez confirmer votre email avant de vous connecter")
            else:
                st.error(f"❌ Erreur de connexion: {error_msg}")

st.divider()

st.info("""
💡 **Première connexion ?**
Si vous n'avez pas encore de compte administrateur, contactez le support technique.
""")

if st.button("← Retour à l'accueil", use_container_width=True):
    st.switch_page("app.py")