
import qrcode
import os
import sys

def create_qr():
    print("="*40)
    print("🎨 GÉNÉRATEUR DE QR CODE RACONTINE")
    print("="*40)
    
    # 1. Demander l'URL
    url = input("\n👉 Entrez l'URL ou le texte à coder\n(Ex: http://192.168.68.113:8080/) : ").strip()
    
    if not url:
        print("❌ Erreur : L'URL ne peut pas être vide.")
        return

    # 2. Demander le nom du fichier
    default_name = "qrcode_racontine.png"
    filename = input(f"\n👉 Nom du fichier de sortie ? (Entrée pour '{default_name}') : ").strip()
    
    if not filename:
        filename = default_name
    
    # Ajouter l'extension .png si absente
    if not filename.lower().endswith(('.png', '.jpg', '.jpeg')):
        filename += ".png"

    # 3. Génération du QR Code
    try:
        print(f"\n⚙️  Génération du QR Code pour : {url}...")
        
        # Configuration avancée pour un meilleur rendu
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_H, # Haute correction d'erreur (taches, etc.)
            box_size=10,
            border=4,
        )
        
        qr.add_data(url)
        qr.make(fit=True)

        # Création de l'image (Noir sur Blanc)
        img = qr.make_image(fill_color="black", back_color="white")
        
        # Sauvegarde
        save_path = os.path.join(os.getcwd(), filename)
        img.save(save_path)
        
        print("\n" + "="*40)
        print(f"✅ SUCCÈS ! QR Code sauvegardé ici :")
        print(f"📂 {save_path}")
        print("="*40)
        
        # Tenter d'ouvrir l'image automatiquement
        if sys.platform.startswith('win'):
            os.startfile(save_path)
        elif sys.platform.startswith('darwin'): # macOS
            os.system(f'open "{save_path}"')
        elif sys.platform.startswith('linux'):
            os.system(f'xdg-open "{save_path}"')
            
    except Exception as e:
        print(f"\n❌ Une erreur est survenue : {e}")

if __name__ == "__main__":
    try:
        create_qr()
        input("\nAppuyez sur Entrée pour quitter...")
    except KeyboardInterrupt:
        print("\n\nAu revoir !")
