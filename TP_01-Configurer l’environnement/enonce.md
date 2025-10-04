https://www.odoo.com/documentation/19.0/fr/contributing/development.html#contributing-development-setup

# ✅ Checklist complète – Configurer l’environnement

### 🔹 Partie Git & Dépôts

* [ ] Créer un **compte GitHub** et générer une **clé SSH**.
* [ ] Faire un **fork** du dépôt [`odoo/odoo`](https://github.com/odoo/odoo) (version communautaire).
* [ ] Cloner tes dépôts en local :

  ```bash
  git clone git@github.com:<ton_compte_github>/odoo.git
  ```
* [ ] Ajouter les **remotes Git** pour pousser vers tes forks :

  ```bash
  cd odoo
  ```

---

### 🔹 Partie VS Code (IDE)

* [ ] Installer **VS Code** si ce n’est pas déjà fait.
* [ ] Ajouter les extensions :

  * **Python** (Microsoft)
  * **Python Environment**
  * **Python Debugger**


---

### 🔹 Partie Python & Environnement

* [ ] Vérifier que **Python 3.10+** est installé :

  ```bash
  python3 --version
  ```
* [ ] Créer un **environnement virtuel** et Installer les **dépendances Python** pour Odoo :

Au lieu d'executer les commandes suivantes vous pouvez directement utiliser **Python Environment** comme dans la vidéo

  ```bash
  cd odoo
  python3 -m venv venv
  source venv/bin/activate   # (Linux/macOS)
  venv\Scripts\activate      # (Windows)
  ```

  ```bash
  pip install -r requirements.txt
  ```

* [ ] Installer **PostgreSQL** (nécessaire pour la base de données Odoo).

---

### 🔹 Configurer odoo.conf


### 🔹 Lancer Odoo 

Au lieu d'executer les commandes suivantes vous pouvez directement utiliser **[Python Debugger](launch.json)** comme dans la vidéo

* [ ] Se placer dans le répertoire `odoo` et lancer le serveur :

  ```bash
  ./odoo-bin -c odoo.conf
  ```

  *(ou ajouter l’option `-d <dbname>` pour choisir une base de données)*

* [ ] Vérifier qu’Odoo est accessible sur :
  👉 [http://localhost:8069](http://localhost:8069)

---

### 🔹 Finalisation

* [ ] Activer le **mode développeur** dans l’interface Odoo :

  1. Connecte-toi avec ton compte admin.
  2. Va dans **Paramètres** → **Activer le mode développeur**.

---

✅ À ce stade :

* Ton code est prêt (forks + dépôts locaux).
* Ton environnement Python est isolé (venv).
* Ton IDE (VS Code) est configuré.
* Ton serveur Odoo tourne en local.
* Le mode développeur est activé.
