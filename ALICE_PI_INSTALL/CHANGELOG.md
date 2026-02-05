# CHANGELOG - Alice Box

Historique des modifications du projet Alice Box.

---

## [v1.1.0] - 2026-02-05

### 🆕 Nouveautés - ALICE_SON

#### Ajout du Contrôle du Volume Sans Hotspot

**Problème résolu :**
- Avant : Pour changer le volume, il fallait basculer en mode hotspot (coupure WiFi, SSH requis, ~5 minutes)
- Maintenant : Interface web accessible sur http://<IP_PI>:8080 (~30 secondes, pas de coupure WiFi)

**Fichiers ajoutés :**

📂 **Code Source**
- `src/ALICE_SON.py` - Serveur web Flask pour contrôle du volume
- `requirements_son.txt` - Dépendances Python (Flask, Werkzeug)

📂 **Configuration Système**
- `system/alice_son.service` - Service systemd pour ALICE_SON
- `system/alice-sudoers` - Permissions sudo pour redémarrage sans mot de passe
- `install_alice_son.sh` - Script d'installation automatique
- `uninstall_alice_son.sh` - Script de désinstallation

📂 **Documentation**
- `README.md` - README principal mis à jour avec ALICE_SON
- `README_ALICE_SON.md` - Documentation complète ALICE_SON
- `GUIDE_RAPIDE.md` - Guide utilisateur rapide
- `RECAP_ALICE_SON.txt` - Récapitulatif visuel avec ASCII art
- `AIDE_ALICE_SON.txt` - Pense-bête commandes rapides
- `docs/ALICE_SON_DOCUMENTATION.md` - Documentation technique détaillée
- `config.json.example` - Exemple de fichier de configuration

**Fonctionnalités ALICE_SON :**
- ✅ Interface web moderne et responsive
- ✅ Slider de volume (0-100%)
- ✅ Boutons rapides (25%, 50%, 75%, 100%)
- ✅ Sauvegarde automatique dans config.json
- ✅ Redémarrage automatique d'alice.service
- ✅ Raccourcis clavier (↑/↓, +/-, Entrée)
- ✅ Compatible PC, Mac, Smartphone, Tablette
- ✅ Pas de coupure WiFi
- ✅ Pas besoin de SSH

**Améliorations :**
- Documentation complète et multi-niveaux (technique, utilisateur, rapide)
- Scripts d'installation/désinstallation automatiques
- Permissions sudo configurées automatiquement
- Service systemd avec auto-restart

---

## [v1.0.0] - 2026-01-XX

### 🎉 Version Initiale

**Fonctionnalités principales :**
- Scan de QR codes avec PiCamera2
- Téléchargement automatique des médias depuis URL
- Lecture audio MP3/WAV avec mpg123/aplay
- Contrôle via boutons GPIO (play/pause, reset)
- Configuration du volume via config.json
- Mode hotspot pour configuration initiale
- Bascule automatique WiFi/Hotspot
- Service systemd pour démarrage automatique

**Fichiers de base :**
- `src/alice.py` - Application principale
- `src/player.py` - Module de lecture audio
- `src/startup.py` - Script de démarrage
- `system/alice.service` - Service systemd
- `system/autohotspot.sh` - Script hotspot
- `system/autohotspot.service` - Service hotspot
- `system/setup_hostapd.conf` - Config point d'accès
- `system/setup_dnsmasq.conf` - Config DHCP

**Documentation de base :**
- `docs/HOW TO wifi.txt` - Guide WiFi
- `docs/HOW_TO_AUTOSTART.md` - Guide autostart
- `waltrhought.txt` - Notes d'installation

---

## Comparaison des Versions

| Fonctionnalité | v1.0.0 | v1.1.0 |
|----------------|--------|--------|
| Scan QR codes | ✅ | ✅ |
| Lecture audio | ✅ | ✅ |
| Boutons GPIO | ✅ | ✅ |
| Mode hotspot | ✅ | ✅ |
| **Contrôle volume sans hotspot** | ❌ | ✅ |
| **Interface web volume** | ❌ | ✅ |
| **Responsive mobile** | ❌ | ✅ |
| **Raccourcis clavier** | ❌ | ✅ |
| **Documentation complète** | Basique | Complète |

---

## Roadmap Future

### v1.2.0 - Prévu
- [ ] Interface web pour gestion WiFi complète
- [ ] Historique des médias lus
- [ ] Statistiques d'utilisation
- [ ] Contrôle de la priorité WiFi depuis l'interface

### v1.3.0 - Prévu
- [ ] Authentification avec mot de passe
- [ ] Mode sombre (dark mode)
- [ ] PWA (Progressive Web App)
- [ ] API REST complète

### v2.0.0 - Vision
- [ ] Application mobile dédiée
- [ ] Contrôle vocal
- [ ] Multi-langues (EN, ES, DE)
- [ ] Intégration cloud pour synchronisation

---

## Notes de Migration

### De v1.0.0 à v1.1.0

**Installation :**
```bash
cd /home/alice/ALICE_PI_INSTALL
chmod +x install_alice_son.sh
sudo ./install_alice_son.sh
```

**Aucune modification requise :**
- alice.py continue de fonctionner exactement pareil
- config.json reste compatible
- Les deux méthodes de contrôle du volume coexistent

**Compatibilité :**
- 100% rétrocompatible
- Aucun changement breaking
- Configuration existante préservée

---

## Support des Versions

| Version | Support | Fin de support |
|---------|---------|----------------|
| v1.1.0 | ✅ Actif | - |
| v1.0.0 | ⚠️ Limité | 2026-06-01 |

---

**Légende :**
- 🆕 Nouveauté
- ✅ Fonctionnel
- ⚠️ Support limité
- ❌ Non disponible
- 🐛 Correction de bug
- 🔧 Amélioration
- 📚 Documentation
