"""
Configuration et envoi d'emails SMTP - Version améliorée
"""

import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

def send_email(to_email: str, subject: str, html_content: str, attachment_path: str = None) -> bool:
    """
    Envoie un email via SMTP avec gestion d'erreurs améliorée
    
    Args:
        to_email: Email du destinataire
        subject: Sujet de l'email
        html_content: Contenu HTML de l'email
        attachment_path: Chemin vers une pièce jointe (optionnel)
    
    Returns:
        True si envoi réussi, False sinon
    """
    try:
        # Configuration SMTP
        smtp_host = os.getenv('SMTP_HOST')
        smtp_port = int(os.getenv('SMTP_PORT', 587))
        smtp_user = os.getenv('SMTP_USER')
        smtp_password = os.getenv('SMTP_PASSWORD')
        
        # Vérification de la configuration
        if not smtp_host or not smtp_user or not smtp_password:
            error_msg = "Configuration SMTP incomplète - Vérifiez votre fichier .env"
            print(f"❌ {error_msg}")
            print(f"   SMTP_HOST: {'✓' if smtp_host else '✗'}")
            print(f"   SMTP_USER: {'✓' if smtp_user else '✗'}")
            print(f"   SMTP_PASSWORD: {'✓' if smtp_password else '✗'}")
            return False
        
        print(f"📧 Préparation de l'email pour {to_email}...")
        
        # Créer le message
        message = MIMEMultipart('alternative')
        message['From'] = f"Sensations by Arda J <{smtp_user}>"
        message['To'] = to_email
        message['Subject'] = subject
        
        # Ajouter le contenu HTML
        html_part = MIMEText(html_content, 'html', 'utf-8')
        message.attach(html_part)
        
        # Ajouter la pièce jointe si présente
        if attachment_path and os.path.exists(attachment_path):
            with open(attachment_path, 'rb') as file:
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(file.read())
                encoders.encode_base64(part)
                part.add_header(
                    'Content-Disposition',
                    f'attachment; filename={os.path.basename(attachment_path)}'
                )
                message.attach(part)
                print(f"📎 Pièce jointe ajoutée: {os.path.basename(attachment_path)}")
        
        print(f"🔌 Connexion au serveur SMTP: {smtp_host}:{smtp_port}...")
        
        # Connexion et envoi
        with smtplib.SMTP(smtp_host, smtp_port, timeout=30) as server:
            server.set_debuglevel(0)  # Mettre à 1 pour voir tous les détails SMTP
            
            print("🔐 Démarrage TLS...")
            server.starttls()
            
            print("🔑 Authentification...")
            server.login(smtp_user, smtp_password)
            
            print("📤 Envoi de l'email...")
            server.send_message(message)
        
        print(f"✅ Email envoyé avec succès à {to_email}")
        return True
    
    except smtplib.SMTPAuthenticationError as e:
        print(f"❌ ERREUR D'AUTHENTIFICATION SMTP:")
        print(f"   {str(e)}")
        print("   → Vérifiez votre SMTP_USER et SMTP_PASSWORD")
        print("   → Si vous utilisez Gmail, assurez-vous d'utiliser un 'App Password'")
        return False
    
    except smtplib.SMTPException as e:
        print(f"❌ ERREUR SMTP:")
        print(f"   {str(e)}")
        print(f"   → Serveur: {smtp_host}:{smtp_port}")
        return False
    
    except Exception as e:
        print(f"❌ ERREUR lors de l'envoi de l'email:")
        print(f"   Type: {type(e).__name__}")
        print(f"   Message: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def send_order_confirmation(order_data: dict, client_data: dict) -> bool:
    """
    Envoie un email de confirmation de commande au client
    
    Args:
        order_data: Données de la commande
        client_data: Données du client
    
    Returns:
        True si envoi réussi
    """
    subject = f"✅ Confirmation de commande #{order_data['id']} - Sensations by Arda J"
    
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <style>
            body {{
                font-family: 'Arial', sans-serif;
                line-height: 1.6;
                color: #333;
                background: #f5f5f5;
                margin: 0;
                padding: 0;
            }}
            .container {{
                max-width: 600px;
                margin: 20px auto;
                background: white;
                border-radius: 10px;
                overflow: hidden;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            }}
            .header {{
                background: linear-gradient(135deg, #D4AF37 0%, #FFD700 100%);
                color: white;
                padding: 30px;
                text-align: center;
            }}
            .header h1 {{
                margin: 0;
                font-size: 28px;
                font-weight: 700;
            }}
            .header p {{
                margin: 10px 0 0 0;
                font-size: 16px;
                opacity: 0.9;
            }}
            .content {{
                padding: 30px;
            }}
            .order-details {{
                background: #f9fafb;
                padding: 20px;
                border-radius: 8px;
                margin: 20px 0;
                border-left: 4px solid #D4AF37;
            }}
            .order-details h3 {{
                margin-top: 0;
                color: #D4AF37;
            }}
            .product-item {{
                border-bottom: 1px solid #e5e7eb;
                padding: 15px 0;
                display: flex;
                justify-content: space-between;
            }}
            .product-item:last-child {{
                border-bottom: none;
            }}
            .product-name {{
                font-weight: 600;
                color: #1f2937;
            }}
            .product-quantity {{
                color: #6b7280;
                font-size: 14px;
            }}
            .product-price {{
                font-weight: 600;
                color: #D4AF37;
            }}
            .total {{
                font-size: 24px;
                font-weight: 700;
                color: #D4AF37;
                text-align: right;
                margin-top: 15px;
                padding-top: 15px;
                border-top: 2px solid #D4AF37;
            }}
            .info-box {{
                background: #e0f2fe;
                padding: 15px;
                border-radius: 8px;
                margin: 20px 0;
                border-left: 4px solid #0284c7;
            }}
            .info-box h4 {{
                margin-top: 0;
                color: #0284c7;
            }}
            .footer {{
                background: #1f2937;
                color: white;
                text-align: center;
                padding: 20px;
                font-size: 14px;
            }}
            .footer a {{
                color: #D4AF37;
                text-decoration: none;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🌸 Sensations by Arda J</h1>
                <p>Merci pour votre commande !</p>
            </div>
            <div class="content">
                <h2>Bonjour {client_data['first_name']} {client_data['last_name']},</h2>
                <p>Nous avons bien reçu votre commande et nous la préparons avec le plus grand soin.</p>
                
                <div class="order-details">
                    <h3>📦 Commande #{order_data['id']}</h3>
                    <p><strong>Date :</strong> {datetime.now().strftime('%d/%m/%Y à %H:%M')}</p>
                    <p><strong>Statut :</strong> En cours de préparation</p>
                    
                    <h4>Articles commandés :</h4>
                    {''.join([f'''
                    <div class="product-item">
                        <div>
                            <div class="product-name">{item['product_name']}</div>
                            <div class="product-quantity">Quantité: {item['quantity']}</div>
                        </div>
                        <div class="product-price">{item['price'] * item['quantity']:,} FCFA</div>
                    </div>
                    ''' for item in order_data['items']])}
                    
                    <div class="total">
                        TOTAL: {order_data['total']:,} FCFA
                    </div>
                </div>
                
                <div class="info-box">
                    <h4>📍 Adresse de livraison</h4>
                    <p>
                        {client_data['first_name']} {client_data['last_name']}<br>
                        {client_data['address']}<br>
                        📞 {client_data['phone']}<br>
                        ✉️ {client_data['email']}
                    </p>
                </div>
                
                <p><strong>Prochaines étapes :</strong></p>
                <ol>
                    <li>Préparation de votre commande (1-2 jours)</li>
                    <li>Expédition et notification par email</li>
                    <li>Livraison sous 3-5 jours ouvrés</li>
                </ol>
                
                <p>Vous recevrez un email de confirmation dès l'expédition de votre colis.</p>
                <p>Pour toute question, n'hésitez pas à nous contacter à <a href="mailto:sensationsbyarda@gmail.com">sensationsbyarda@gmail.com</a></p>
            </div>
            <div class="footer">
                <p><strong>✨ Sensations by Arda J ✨</strong></p>
                <p>Parfums & Essences d'Exception</p>
                <p style="margin-top: 10px; font-size: 12px; opacity: 0.8;">
                    © 2024 Sensations by Arda J - Tous droits réservés<br>
                    Cet email a été envoyé automatiquement, merci de ne pas y répondre.
                </p>
            </div>
        </div>
    </body>
    </html>
    """
    
    return send_email(client_data['email'], subject, html_content)

def send_admin_notification(order_data: dict, client_data: dict) -> bool:
    """
    Envoie une notification à l'admin pour une nouvelle commande
    
    Args:
        order_data: Données de la commande
        client_data: Données du client
    
    Returns:
        True si envoi réussi
    """
    admin_email = os.getenv('ADMIN_EMAIL')
    if not admin_email:
        print("❌ ADMIN_EMAIL non configuré dans .env")
        return False
    
    subject = f"🛒 Nouvelle commande #{order_data['id']} - {client_data['first_name']} {client_data['last_name']}"
    
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <style>
            body {{
                font-family: Arial, sans-serif;
                line-height: 1.6;
                color: #333;
                background: #f5f5f5;
            }}
            .container {{
                max-width: 600px;
                margin: 20px auto;
                background: white;
                border-radius: 10px;
                overflow: hidden;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            }}
            .alert {{
                background: linear-gradient(135deg, #10b981 0%, #059669 100%);
                color: white;
                padding: 30px;
                text-align: center;
            }}
            .alert h1 {{
                margin: 0;
                font-size: 28px;
            }}
            .content {{
                padding: 30px;
            }}
            .order-box {{
                background: #f9fafb;
                border-left: 4px solid #3b82f6;
                padding: 20px;
                margin: 20px 0;
                border-radius: 4px;
            }}
            .client-info {{
                background: #eff6ff;
                padding: 15px;
                border-radius: 8px;
                margin: 15px 0;
            }}
            .product-list {{
                margin: 15px 0;
            }}
            .product-item {{
                padding: 10px;
                border-bottom: 1px solid #e5e7eb;
            }}
            .total {{
                font-size: 24px;
                font-weight: 700;
                color: #3b82f6;
                text-align: right;
                margin-top: 15px;
                padding-top: 15px;
                border-top: 2px solid #3b82f6;
            }}
            .button {{
                display: inline-block;
                background: #3b82f6;
                color: white;
                padding: 12px 24px;
                text-decoration: none;
                border-radius: 8px;
                margin-top: 20px;
                font-weight: 600;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="alert">
                <h1>🔔 Nouvelle Commande Reçue !</h1>
                <p>Une nouvelle commande vient d'être passée</p>
            </div>
            
            <div class="content">
                <div class="order-box">
                    <h2>📦 Commande #{order_data['id']}</h2>
                    <p><strong>Date :</strong> {datetime.now().strftime('%d/%m/%Y à %H:%M')}</p>
                    <p><strong>Statut :</strong> En cours (nouvelle)</p>
                </div>
                
                <div class="client-info">
                    <h3>👤 Informations Client</h3>
                    <p>
                        <strong>Nom :</strong> {client_data['first_name']} {client_data['last_name']}<br>
                        <strong>Email :</strong> {client_data['email']}<br>
                        <strong>Téléphone :</strong> {client_data['phone']}<br>
                        <strong>Adresse :</strong><br>
                        {client_data['address']}
                    </p>
                </div>
                
                <h3>🛍️ Articles Commandés</h3>
                <div class="product-list">
                    {''.join([f'''
                    <div class="product-item">
                        <strong>{item["product_name"]}</strong><br>
                        Quantité: {item["quantity"]} × {item["price"]:,} FCFA = <strong>{item["price"] * item["quantity"]:,} FCFA</strong>
                    </div>
                    ''' for item in order_data['items']])}
                </div>
                
                <div class="total">
                    TOTAL: {order_data['total']:,} FCFA
                </div>
                
                <div style="text-align: center;">
                    <a href="{os.getenv('APP_URL', 'http://localhost:8501')}" class="button">
                        Voir dans le Dashboard Admin
                    </a>
                </div>
                
                <p style="margin-top: 30px; padding: 15px; background: #fef3c7; border-radius: 8px; border-left: 4px solid #f59e0b;">
                    <strong>⚡ Action requise :</strong> Préparez cette commande et mettez à jour son statut dans l'interface admin.
                </p>
            </div>
        </div>
    </body>
    </html>
    """
    
    return send_email(admin_email, subject, html_content)