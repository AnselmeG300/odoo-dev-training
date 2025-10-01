https://www.odoo.com/documentation/19.0/fr/developer/tutorials/setup_guide.html


# ✅ Checklists – Setup du tutoriel Odoo

### 🔹 Étape 1 : Fork du dépôt tutoriel

* [ ] Aller sur la page GitHub [`odoo/tutorials`](https://github.com/odoo/tutorials).
* [ ] Cliquer sur le bouton **Fork** en haut à droite.
* [ ] Vérifier que le dépôt apparaît bien sur ton compte GitHub personnel (`github.com/<ton_compte>/tutorials`).

---

### 🔹 Étape 2 : Cloner le dépôt tutoriel

* [ ] Copier l’URL SSH de ton fork (`git@github.com:<ton_compte>/tutorials.git`).
* [ ] Ouvrir un terminal et exécuter :

  ```bash
  git clone git@github.com:<ton_compte>/tutorials.git
  ```
* [ ] Vérifier que le dossier `tutorials` est bien créé en local.

---

### 🔹 Étape 3 : Déplacer le dépôt tutoriel

* [ ] Se rendre dans le répertoire où est installé Odoo.
* [ ] Vérifier qu’il existe un dossier `custom_addons` (sinon, le créer).

  ```bash
  mkdir -p custom_addons
  ```
* [ ] Déplacer le dossier cloné `tutorials` dans `custom_addons` :

  ```bash
  mv tutorials custom_addons/
  ```
* [ ] Vérifier que la structure ressemble à :

  ```
  odoo/
  ├── addons/
  ├── custom_addons/
  │   └── tutorials/
  ```

---

