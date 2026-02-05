# 🔊 ALICE_SON - Contrôle du Volume Sans Mode Hotspot

## 📖 Problème Résolu

**Avant :** Pour changer le volume, il fallait :
1. Se connecter en SSH au Raspberry Pi
2. Forcer le mode hotspot : `sudo bash /home/alice/autohotspot.sh force`
3. Se connecter au WiFi ALICE_SETUP avec le téléphone
4. Aller sur http://192.168.50.1
5. Configurer le volume
6. Valider → Le Pi redémarre et se reconnecte

**Maintenant :** 
1. Ouvrez simplement `http://<IP_DU_PI>:8080` dans votre navigateur
2. Ajustez le volume avec le slider
3. Cliquez sur "Sauvegarder"
4. Alice redémarre automatiquement avec le nouveau volume

✅ **Pas de coupure WiFi, pas de SSH nécessaire !**

---

## 🚀 Installation

### 1. Transférer les fichiers sur le Raspberry Pi

```bash
# Sur votre ordinateur, depuis le dossier ALICE_PI_INSTALL
scp -r . alice@<IP_DU_PI>:/home/alice/ALICE_PI_INSTALL/
```

### 2. Se connecter au Pi et installer

```bash
ssh alice@<IP_DU_PI>
cd /home/alice/ALICE_PI_INSTALL
chmod +x install_alice_son.sh
sudo ./install_alice_son.sh
```

Le script va :
- ✅ Installer Flask (dépendance Python)
- ✅ Copier ALICE_SON.py dans /home/alice/
- ✅ Créer et activer le service systemd
- ✅ Démarrer le serveur web
- ✅ Afficher l'URL d'accès

---

## 🌐 Utilisation

### Accéder à l'interface web

1. **Trouver l'IP du Pi:**
   ```bash
   hostname -I
   ```

2. **Ouvrir dans le navigateur:**
   ```
   http://<IP_DU_PI>:8080
   ```

3. **Ajuster le volume:**
   - Utilisez le slider pour choisir le volume (0-100%)
   - Ou cliquez sur les boutons rapides (25%, 50%, 75%, 100%)
   - Raccourcis clavier : ↑/↓ ou +/- pour ajuster, Entrée pour sauvegarder

4. **Sauvegarder:**
   - Cliquez sur "Sauvegarder et Redémarrer Alice"
   - Alice redémarre automatiquement avec le nouveau volume

---

## 🛠️ Commandes Utiles

### Voir les logs en temps réel
```bash
sudo journalctl -u alice_son.service -f
```

### Redémarrer le serveur
```bash
sudo systemctl restart alice_son.service
```

### Arrêter le serveur
```bash
sudo systemctl stop alice_son.service
```

### Démarrer le serveur
```bash
sudo systemctl start alice_son.service
```

### Vérifier le statut
```bash
sudo systemctl status alice_son.service
```

### Désactiver au démarrage
```bash
sudo systemctl disable alice_son.service
```

### Réactiver au démarrage
```bash
sudo systemctl enable alice_son.service
```

---

## 🔧 Architecture Technique

### Fichiers créés

```
ALICE_PI_INSTALL/
├── src/
│   └── ALICE_SON.py                    # Serveur web Flask
├── system/
│   └── alice_son.service               # Service systemd
├── requirements_son.txt                # Dépendances Python
├── install_alice_son.sh                # Script d'installation
└── README_ALICE_SON.md                 # Cette documentation
```

### Fichiers sur le Pi (après installation)

```
/home/alice/
├── ALICE_SON.py                        # Serveur web
├── media/
│   └── config.json                     # Configuration (volume, wifi, etc.)
└── /etc/systemd/system/
    └── alice_son.service               # Service systemd
```

### Comment ça marche ?

1. **ALICE_SON.py** est un serveur web Flask qui tourne en arrière-plan
2. Il lit et écrit dans `/home/alice/media/config.json`
3. Quand vous sauvegardez un nouveau volume, il :
   - Met à jour `config.json`
   - Redémarre `alice.service` pour appliquer le changement
4. **alice.py** lit automatiquement le volume depuis `config.json` au démarrage

---

## 🔒 Sécurité

**Note:** Le serveur écoute sur `0.0.0.0:8080` (toutes les interfaces).

Si vous voulez restreindre l'accès uniquement au réseau local :
- Configurez votre pare-feu/routeur pour bloquer le port 8080 depuis Internet
- Ou modifiez `ALICE_SON.py` ligne finale pour écouter uniquement sur `127.0.0.1` (local uniquement)

---

## 🐛 Dépannage

### Le serveur ne démarre pas

1. Vérifier les logs :
   ```bash
   sudo journalctl -u alice_son.service -n 50
   ```

2. Vérifier que Flask est installé :
   ```bash
   python3 -c "import flask; print(flask.__version__)"
   ```

3. Tester manuellement :
   ```bash
   cd /home/alice
   python3 ALICE_SON.py
   ```

### Impossible d'accéder à l'interface

1. Vérifier que le service tourne :
   ```bash
   sudo systemctl status alice_son.service
   ```

2. Vérifier l'IP du Pi :
   ```bash
   hostname -I
   ```

3. Tester depuis le Pi lui-même :
   ```bash
   curl http://localhost:8080
   ```

4. Vérifier le pare-feu :
   ```bash
   sudo ufw status
   # Si actif, autoriser le port :
   sudo ufw allow 8080/tcp
   ```

### Alice ne redémarre pas après sauvegarde

Vérifier que l'utilisateur `alice` peut exécuter `systemctl restart` sans mot de passe :

```bash
sudo visudo
# Ajouter la ligne :
alice ALL=(ALL) NOPASSWD: /usr/bin/systemctl restart alice.service
```

---

## 📱 Interface Mobile

L'interface est **responsive** et fonctionne parfaitement sur smartphone et tablette !

- Design moderne avec dégradé violet
- Slider tactile fluide
- Boutons rapides (25%, 50%, 75%, 100%)
- Affichage en temps réel du volume
- Feedback visuel lors de la sauvegarde

---

## 🎯 Prochaines Améliorations (Optionnel)

- [ ] Ajouter contrôle de la priorité WiFi
- [ ] Ajouter visualisation de la liste des réseaux disponibles
- [ ] Ajouter un bouton "Test du volume" (joue un son de test)
- [ ] Historique des changements de volume
- [ ] API REST complète (GET, POST, PUT, DELETE)
- [ ] Authentification avec mot de passe
- [ ] Interface en dark mode

---

## 📄 Licence

Ce code fait partie du projet Alice Box.
Libre d'utilisation et de modification.

---

## 👤 Auteur

Créé pour simplifier la gestion du volume d'Alice sans avoir à basculer en mode hotspot.

**Date :** 2026-02-05

---

## 🆘 Support

En cas de problème, vérifier :
1. Les logs du service : `sudo journalctl -u alice_son.service`
2. Le fichier config existe : `ls -l /home/alice/media/config.json`
3. Flask est installé : `python3 -c "import flask"`
4. Le port 8080 n'est pas déjà utilisé : `sudo netstat -tulpn | grep 8080`
