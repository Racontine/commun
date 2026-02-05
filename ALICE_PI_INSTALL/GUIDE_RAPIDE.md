# 🚀 Guide Rapide - ALICE_SON

## Installation (1 fois seulement)

```bash
# 1. Se connecter au Pi
ssh alice@<IP_DU_PI>

# 2. Aller dans le dossier d'installation
cd /home/alice/ALICE_PI_INSTALL

# 3. Rendre le script exécutable et lancer l'installation
chmod +x install_alice_son.sh
sudo ./install_alice_son.sh
```

L'installation prend environ 30 secondes.

---

## Utilisation Quotidienne

### Méthode Simple (Recommandée)

1. **Ouvrir votre navigateur** (téléphone, tablette, ou ordinateur)
2. **Taper l'adresse:** `http://<IP_DU_PI>:8080`
3. **Ajuster le volume** avec le slider
4. **Cliquer sur "Sauvegarder"**
5. **Attendre 5 secondes** → Alice redémarre avec le nouveau volume

✅ **C'est tout !** Pas besoin de SSH, pas de coupure WiFi !

---

## 🔍 Comment trouver l'IP du Pi ?

### Méthode 1 : Depuis votre routeur
- Se connecter à l'interface de votre box Internet
- Chercher "Alice" ou "Raspberry" dans la liste des appareils connectés

### Méthode 2 : Depuis le Pi (si vous avez un écran)
```bash
hostname -I
```

### Méthode 3 : Scanner le réseau
Sur votre ordinateur :
```bash
# Linux/Mac
arp -a | grep -i "raspberry\|b8:27:eb\|dc:a6:32\|e4:5f:01"

# Windows
arp -a
```

---

## 💡 Astuces

### Raccourcis Clavier (dans l'interface web)
- **↑** ou **+** : Augmenter le volume de 5%
- **↓** ou **-** : Diminuer le volume de 5%
- **Entrée** : Sauvegarder

### Boutons Rapides
Utilisez les boutons **25%**, **50%**, **75%**, **100%** pour un réglage rapide.

### Ajouter aux Favoris
Ajoutez `http://<IP_DU_PI>:8080` à vos favoris pour un accès en 1 clic !

---

## ⚠️ Problèmes Courants

### "La page ne charge pas"

**Solution 1 :** Vérifier que le service tourne
```bash
ssh alice@<IP_DU_PI>
sudo systemctl status alice_son.service
```

**Solution 2 :** Redémarrer le service
```bash
sudo systemctl restart alice_son.service
```

**Solution 3 :** Vérifier l'IP du Pi
```bash
hostname -I
```

### "Le volume ne change pas"

**Vérifier que :**
1. Vous avez bien cliqué sur "Sauvegarder"
2. Alice a bien redémarré (attendre 10 secondes)
3. Le son n'est pas muet sur le Pi

**Test manuel :**
```bash
ssh alice@<IP_DU_PI>
cat /home/alice/media/config.json
# Vérifier que "volume" a bien changé
```

---

## 🔧 Commandes de Maintenance

### Voir les logs en direct
```bash
sudo journalctl -u alice_son.service -f
```
Appuyer sur **Ctrl+C** pour quitter

### Redémarrer le serveur
```bash
sudo systemctl restart alice_son.service
```

### Vérifier le statut
```bash
sudo systemctl status alice_son.service
```

---

## 📱 QR Code pour Accès Rapide (Optionnel)

Vous pouvez créer un QR code pointant vers `http://<IP_DU_PI>:8080` et le coller sur votre frigo ou bureau !

Générateur en ligne : https://www.qr-code-generator.com/

---

## 🎯 Comparaison Avant/Après

| Étape | AVANT (Mode Hotspot) | MAINTENANT (ALICE_SON) |
|-------|----------------------|------------------------|
| 1 | SSH au Pi | Ouvrir navigateur |
| 2 | Force hotspot mode | Aller sur http://IP:8080 |
| 3 | Se connecter au WiFi ALICE_SETUP | Ajuster slider |
| 4 | Ouvrir 192.168.50.1 | Cliquer "Sauvegarder" |
| 5 | Configurer volume | ✅ **Terminé !** |
| 6 | Valider et attendre reboot | |
| 7 | Se reconnecter au WiFi maison | |
| **Temps total** | **~5 minutes** | **~30 secondes** |
| **Connexion WiFi** | ❌ Coupée | ✅ Maintenue |
| **Terminal requis** | ❌ Oui (SSH) | ✅ Non |

---

## 🎉 Astuce Pro

### Créer un raccourci sur l'écran d'accueil du téléphone

**Sur Android :**
1. Ouvrir Chrome et aller sur `http://<IP_DU_PI>:8080`
2. Menu (⋮) → "Ajouter à l'écran d'accueil"
3. L'icône apparaît comme une vraie application !

**Sur iOS :**
1. Ouvrir Safari et aller sur `http://<IP_DU_PI>:8080`
2. Partager → "Sur l'écran d'accueil"
3. Validez

Maintenant vous avez un **contrôle du volume d'Alice en 1 clic** sur votre téléphone ! 🎯

---

## 📞 Support

En cas de problème, consulter le fichier **README_ALICE_SON.md** pour une documentation complète.
