"""
Page Gestion des Produits Admin
"""

import streamlit as st
# --- MODIFIÉ ---
from config.supabase_client import init_supabase, upload_file, delete_file, load_supabase_session
# --- FIN MODIFIÉ ---
from models.product import Product
from utils.session import init_session_state, require_auth, set_flash_message, display_flash_message
from utils.validators import validate_product_form
from utils.formatters import format_price, format_stock_badge
import uuid

# Configuration
st.set_page_config(page_title="Produits Admin - Sensations Arda", page_icon="📦", layout="wide")

# Initialisation
init_supabase()
init_session_state()

# Protection de la page
@require_auth
def main():
    # --- AJOUTÉ ---
    # S'assure que le client Supabase a bien le token d'authentification
    load_supabase_session()
    
    st.title("📦 Gestion des Produits")
    
    # ... (le reste du fichier est identique) ...
    
    # Afficher les messages flash
    display_flash_message()
    
    # Tabs pour les différentes actions
    tab_list, tab_add, tab_edit = st.tabs(["📋 Liste des Produits", "➕ Ajouter un Produit", "✏️ Modifier un Produit"])
    
    # TAB 1: Liste des produits
    with tab_list:
        st.subheader("Liste des Produits")
        
        # Filtres
        col1, col2 = st.columns([3, 1])
        with col1:
            search = st.text_input("🔍 Rechercher", placeholder="Nom du produit...")
        with col2:
            filter_type = st.selectbox("Type", ["Tous", "Homme", "Femme", "Mixte"])
        
        # Récupérer les produits
        products = Product.get_all(search=search, filter_type=filter_type)
        
        st.markdown(f"**{len(products)} produit(s) trouvé(s)**")
        
        if products:
            # Afficher en grille
            cols_per_row = 3
            for i in range(0, len(products), cols_per_row):
                cols = st.columns(cols_per_row)
                
                for j, col in enumerate(cols):
                    idx = i + j
                    if idx < len(products):
                        product = products[idx]
                        
                        with col:
                            with st.container(border=True):
                                # Image
                                images = product.get('product_images', [])
                                image_url = images[0]['url'] if images else 'https://via.placeholder.com/300x200?text=No+Image'
                                st.image(image_url, use_container_width=True)
                                
                                # Infos
                                st.markdown(f"**{product['name']}**")
                                st.caption(f"Type: {product['type']}")
                                st.markdown(f"**Prix:** {format_price(product['price'])}")
                                st.markdown(format_stock_badge(product['stock']), unsafe_allow_html=True)
                                
                                # Actions
                                col_a, col_b = st.columns(2)
                                
                                with col_a:
                                    if st.button("✏️ Modifier", key=f"edit_{product['id']}", use_container_width=True):
                                        st.session_state['edit_product_id'] = product['id']
                                        st.rerun()
                                
                                with col_b:
                                    if st.button("🗑️ Supprimer", key=f"del_{product['id']}", use_container_width=True):
                                        st.session_state['delete_product_id'] = product['id']
                                        st.rerun()
        else:
            st.info("Aucun produit trouvé")

    # TAB 2: Ajouter un produit
    with tab_add:
        st.subheader("➕ Ajouter un Nouveau Produit")

        # Gestion d'état
        if st.session_state.get('product_added_success', False):
            
            st.success(f"✅ Produit '{st.session_state.get('last_product_name', '')}' créé avec succès !")
            st.balloons()
            
            if st.button("🔄 Ajouter un autre produit"):
                st.session_state.product_added_success = False
                if 'last_product_name' in st.session_state:
                    del st.session_state['last_product_name']
                st.rerun()

        else:
            # Formulaire
            with st.form("add_product_form"):
                name = st.text_input("Nom du produit *", placeholder="Ex: Eau de Parfum Élégance")
                col1, col2 = st.columns(2)
                with col1:
                    product_type = st.selectbox("Type *", ["Homme", "Femme", "Mixte"])
                with col2:
                    price = st.number_input("Prix (€) *", min_value=0.0, step=1.0, value=0.0)
                stock = st.number_input("Stock initial *", min_value=0, step=1, value=0)
                description = st.text_area("Description", placeholder="Description détaillée du produit...", height=100)
                uploaded_files = st.file_uploader(
                    "Choisir des images",
                    type=['jpg', 'jpeg', 'png', 'webp'],
                    accept_multiple_files=True,
                    help="Vous pouvez sélectionner plusieurs images"
                )
                st.caption("* Champs obligatoires")
                submit = st.form_submit_button("✅ Créer le produit", use_container_width=True, type="primary")
            
            # Traitement
            if submit:
                validation = validate_product_form(name, product_type, price, stock, description)
                
                if not validation['is_valid']:
                    st.error("❌ Veuillez corriger les erreurs:")
                    for field, error in validation['errors'].items():
                        st.error(f"• {error}")
                else:
                    image_urls = []
                    upload_failed = False # Flag pour suivre les échecs
                    
                    if uploaded_files:
                        progress_bar = st.progress(0)
                        for idx, file in enumerate(uploaded_files):
                            file_extension = file.name.split('.')[-1]
                            unique_filename = f"products/{uuid.uuid4()}.{file_extension}"
                            
                            result = upload_file('product-images', file, unique_filename)
                            
                            if result['success']:
                                image_urls.append(result['url'])
                            else:
                                upload_failed = True
                                error_msg = result.get('error', 'Raison inconnue')
                                st.error(f"❌ Échec de l'upload de '{file.name}'. Raison: {error_msg}")
                                print(f"--- ERREUR UPLOAD STORAGE ---: {error_msg}")
                            
                            progress_bar.progress((idx + 1) / len(uploaded_files))
                        progress_bar.empty()
                    
                    if not upload_failed:
                        product = Product.create(name, product_type, description, price, stock, image_urls)
                        
                        if product:
                            st.session_state.product_added_success = True
                            st.session_state.last_product_name = name
                            st.rerun()
                        else:
                            st.error("❌ Erreur lors de la création du produit en base de données.")

    # TAB 3: Modifier un produit
    with tab_edit:
        st.subheader("✏️ Modifier un Produit")
        
        if 'edit_product_id' not in st.session_state:
            st.session_state['edit_product_id'] = None
        
        products = Product.get_all()
        product_options = {p['id']: f"{p['name']} ({p['type']})" for p in products}
        
        selected_id = st.selectbox(
            "Sélectionner un produit",
            options=list(product_options.keys()),
            format_func=lambda x: product_options[x],
            index=list(product_options.keys()).index(st.session_state['edit_product_id']) if st.session_state['edit_product_id'] in product_options else 0
        )
        
        if selected_id:
            product = Product.get_by_id(selected_id)
            
            if product:
                # Afficher les images
                images = product.get('product_images', [])
                if images:
                    st.markdown("**Images actuelles:**")
                    cols = st.columns(len(images))
                    for idx, (col, img) in enumerate(zip(cols, images)):
                        with col:
                            st.image(img['url'], use_container_width=True)
                            if st.button("🗑️", key=f"del_img_{img['id']}", help="Supprimer cette image"):
                                path = img['url'].split('/product-images/')[-1] if '/product-images/' in img['url'] else None
                                if path:
                                    delete_file('product-images', path)
                                Product.delete_image(img['id'])
                                st.rerun()
                
                st.divider()
                
                # Formulaire de modification
                with st.form("edit_product_form"):
                    name = st.text_input("Nom du produit *", value=product['name'])
                    col1, col2 = st.columns(2)
                    with col1:
                        try:
                            current_type_index = ["Homme", "Femme", "Mixte"].index(product['type'])
                        except ValueError:
                            current_type_index = 0
                        product_type = st.selectbox("Type *", ["Homme", "Femme", "Mixte"], index=current_type_index)
                    with col2:
                        price = st.number_input("Prix (€) *", min_value=0.0, step=1.0, value=float(product['price']))
                    stock = st.number_input("Stock *", min_value=0, step=1, value=int(product['stock']))
                    description = st.text_area("Description", value=product.get('description', ''), height=100)
                    new_files = st.file_uploader(
                        "Choisir des images",
                        type=['jpg', 'jpeg', 'png', 'webp'],
                        accept_multiple_files=True,
                        key="new_images_edit"
                    )
                    
                    col_submit, col_cancel = st.columns(2)
                    with col_submit:
                        submit = st.form_submit_button("💾 Sauvegarder", use_container_width=True, type="primary")
                    with col_cancel:
                        cancel = st.form_submit_button("❌ Annuler", use_container_width=True)
                    
                    if cancel:
                        st.session_state['edit_product_id'] = None
                        st.rerun()
                    
                    if submit:
                        validation = validate_product_form(name, product_type, price, stock, description)
                        
                        if not validation['is_valid']:
                            st.error("❌ Veuillez corriger les erreurs:")
                            for field, error in validation['errors'].items():
                                st.error(f"• {error}")
                        else:
                            success = Product.update(selected_id, name, product_type, description, price, stock)
                            
                            if success:
                                # Upload des nouvelles images
                                upload_failed = False
                                if new_files:
                                    for file in new_files:
                                        file_extension = file.name.split('.')[-1]
                                        unique_filename = f"products/{uuid.uuid4()}.{file_extension}"
                                        
                                        result = upload_file('product-images', file, unique_filename)
                                        
                                        if result['success']:
                                            Product.add_image(selected_id, result['url'])
                                        else:
                                            upload_failed = True
                                            error_msg = result.get('error', 'Raison inconnue')
                                            st.error(f"❌ Échec de l'upload de '{file.name}'. Raison: {error_msg}")
                                            print(f"--- ERREUR UPLOAD STORAGE ---: {error_msg}")
                                
                                st.success(f"✅ Produit '{name}' mis à jour avec succès !")
                                
                                if upload_failed:
                                    st.warning("⚠️ Certaines nouvelles images n'ont pas pu être uploadées.")
                                
                                # On relance pour rafraîchir la page
                                st.rerun()
                            else:
                                st.error("❌ Erreur lors de la mise à jour")
    
    # Modal de confirmation de suppression
    if st.session_state.get('delete_product_id'):
        product = Product.get_by_id(st.session_state['delete_product_id'])
        
        if product:
            @st.dialog(f"🗑️ Supprimer {product['name']} ?")
            def confirm_delete():
                st.warning(f"⚠️ Êtes-vous sûr de vouloir supprimer le produit **{product['name']}** ?")
                st.markdown("Cette action est **irréversible** et supprimera également toutes les images associées.")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    if st.button("✅ Oui, supprimer", use_container_width=True, type="primary"):
                        # Supprimer les images du storage
                        images = product.get('product_images', [])
                        for img in images:
                            path = img['url'].split('/product-images/')[-1] if '/product-images/' in img['url'] else None
                            if path:
                                delete_file('product-images', path)
                        
                        # Supprimer le produit
                        if Product.delete(st.session_state['delete_product_id']):
                            st.session_state['delete_product_id'] = None
                            set_flash_message(f"🗑️ Produit '{product['name']}' supprimé", "success")
                            st.rerun()
                        else:
                            st.error("Erreur lors de la suppression")
                
                with col2:
                    if st.button("❌ Annuler", use_container_width=True):
                        st.session_state['delete_product_id'] = None
                        st.rerun()
            
            confirm_delete()

# Exécuter
main()