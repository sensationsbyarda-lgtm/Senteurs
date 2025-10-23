"""
Script pour corriger et compléter la structure du projet Sensations Arda
Exécuter dans le dossier Senteurs/
"""

import os
import shutil

def fix_project_structure():
    """Corrige la structure du projet et crée les fichiers manquants"""
    
    print("🔧 Correction de la structure du projet...")
    
    # 1. Créer tous les dossiers nécessaires
    print("\n📁 Création des dossiers...")
    directories = [
        'config',
        'models', 
        'utils',
        'pages',
        'pages/admin',
        '.streamlit'
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"  ✓ {directory}/")
    
    # 2. Créer les fichiers __init__.py
    print("\n📄 Création des __init__.py...")
    init_files = [
        'config/__init__.py',
        'models/__init__.py',
        'utils/__init__.py'
    ]
    
    for init_file in init_files:
        with open(init_file, 'w', encoding='utf-8') as f:
            f.write('# Package initialization\n')
        print(f"  ✓ {init_file}")
    
    # 3. Déplacer models.py vers models/client.py
    print("\n🔄 Déplacement de models.py...")
    if os.path.exists('models.py'):
        shutil.move('models.py', 'models/client.py')
        print("  ✓ models.py → models/client.py")
    
    # 4. Déplacer session.py vers utils/session.py  
    print("\n🔄 Déplacement de session.py...")
    if os.path.exists('session.py'):
        shutil.move('session.py', 'utils/session.py')
        print("  ✓ session.py → utils/session.py")
    
    # 5. Déplacer Acceuil.py vers pages/1_🏠_Accueil.py
    print("\n🔄 Déplacement de Acceuil.py...")
    if os.path.exists('Acceuil.py'):
        shutil.move('Acceuil.py', 'pages/1_🏠_Accueil.py')
        print("  ✓ Acceuil.py → pages/1_🏠_Accueil.py")
    
    # 6. Déplacer les fichiers admin
    print("\n🔄 Déplacement des fichiers admin...")
    admin_files = {
        '5_Produits.py': 'pages/admin/5_📦_Produits.py',
        '6_Commandes.py': 'pages/admin/6_📋_Commandes.py',
        '7_Analyses.py': 'pages/admin/7_📈_Analytics.py',
        'Login.py': 'pages/admin/Login.py'
    }
    
    for old, new in admin_files.items():
        if os.path.exists(old):
            shutil.move(old, new)
            print(f"  ✓ {old} → {new}")
    
    # 7. Déplacer config.toml
    print("\n🔄 Déplacement de config.toml...")
    if os.path.exists('config.toml'):
        shutil.move('config.toml', '.streamlit/config.toml')
        print("  ✓ config.toml → .streamlit/config.toml")
    
    # 8. Créer le fichier .env si nécessaire
    if not os.path.exists('.env'):
        print("\n📝 Création du fichier .env...")
        with open('.env', 'w', encoding='utf-8') as f:
            f.write("""# Supabase Configuration
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-anon-key-here
SUPABASE_SERVICE_KEY=your-service-role-key-here

# Email Configuration
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password
ADMIN_EMAIL=admin@sensations-arda.com

# Application Configuration
APP_NAME=Sensations Arda
APP_URL=http://localhost:8501
DEBUG=True
""")
        print("  ✓ .env créé (à configurer)")
    
    print("\n" + "="*60)
    print("✅ STRUCTURE CORRIGÉE AVEC SUCCÈS")
    print("="*60)
    
    print("\n⚠️  FICHIERS MANQUANTS À CRÉER:")
    print("Les fichiers suivants doivent être créés manuellement")
    print("ou copiés depuis les artifacts que je vous ai donnés:")
    print()
    print("📂 config/")
    print("  - supabase_client.py")
    print("  - email_config.py")
    print()
    print("📂 models/")
    print("  - product.py")
    print("  - order.py")
    print("  - analytics.py")
    print()
    print("📂 utils/")
    print("  - validators.py")
    print("  - formatters.py")
    print()
    print("📂 pages/")
    print("  - 2_🛒_Panier.py")
    print("  - 3_📦_Checkout.py")
    print()
    print("📂 pages/admin/")
    print("  - 4_📊_Dashboard.py")
    print()
    
    print("\n📋 Prochaines étapes:")
    print("1. Je vais vous donner tous les fichiers manquants")
    print("2. Vous les copiez dans les bons dossiers")
    print("3. Vous configurez le .env avec vos clés Supabase")
    print("4. Vous lancez: streamlit run app.py")

if __name__ == "__main__":
    print("=" * 60)
    print("🌸 CORRECTION STRUCTURE SENSATIONS ARDA")
    print("=" * 60)
    print()
    
    # Vérifier qu'on est dans le bon dossier
    if not os.path.exists('app.py'):
        print("⚠️  ATTENTION : Fichier app.py non trouvé !")
        print("Veuillez exécuter ce script dans le dossier Senteurs/")
        input("\nAppuyez sur Entrée pour quitter...")
    else:
        fix_project_structure()
        input("\n✅ Appuyez sur Entrée pour fermer...")