https://www.odoo.com/documentation/19.0/fr/contributing/development.html#environment-setup


---

# ✅ Checklist Setup Odoo Community

### 🔹 Préparation de l’environnement

* [ ] Créer un **compte GitHub** (si tu n’en as pas déjà un).
* [ ] Générer une **clé SSH** et l’ajouter à ton compte GitHub.
  👉 Commande utile : `ssh-keygen -t ed25519 -C "youremail@example.com"`
* [ ] Installer **Git** sur ta machine.
  👉 Vérifie avec : `git --version`
* [ ] Vérifier que le dossier d’installation de Git est bien dans la **variable PATH** (Windows/Linux/macOS).

---

### 🔹 Configuration Git

* [ ] Configurer ton identité Git avec le même nom et email que ton compte GitHub :

  ```bash
  git config --global user.name "Ton Nom"
  git config --global user.email "tonemail@example.com"
  ```

---

### 🔹 Récupération du code source

* [ ] Faire un **fork** du dépôt `odoo/odoo` (Community Edition) depuis GitHub.
* [ ] Cloner ton fork en local avec SSH :

  ```bash
  git clone git@github.com:<ton_compte_github>/odoo.git
  ```

---


