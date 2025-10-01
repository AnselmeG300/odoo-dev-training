

---

# 📘 Chapitre 2 : Nouvelle Application (Real Estate Module)

### 🎯 Objectif général

Créer la base d’un **nouveau module Odoo** (Real Estate Advertisement).
Au départ, ce module est une **coquille vide**, uniquement reconnue par Odoo.
Ensuite, on l’enrichira progressivement avec des fonctionnalités.

---

## 🔹 Ce que le module couvre

* Domaine métier : **immobilier** (non inclus dans Odoo de base).
* Vues principales prévues :

  * **Vue liste** : toutes les annonces (titres, type, code postal, prix, etc.).
  * **Vue formulaire** :

    * Onglet 1 : description du bien (chambres, surface, garage, jardin…).
    * Onglet 2 : offres d’acheteurs potentiels (au-dessus ou en dessous du prix demandé).
* Le vendeur choisit d’accepter ou refuser une offre.

*(les images que tu as envoyées montrent déjà un aperçu du rendu final attendu 👀)*

---

## 🔹 Étapes pratiques – Préparation du module

### 1. Créer le dossier du module

Dans ton répertoire `tutorials`, ajoute un dossier `estate` :

```bash
/home/$USER/src/tutorials/estate/
```

---

### 2. Ajouter les fichiers obligatoires

Un module Odoo doit contenir **au minimum** deux fichiers :

1. `__init__.py` → pour l’instant vide.

   ```bash
   /home/$USER/src/tutorials/estate/__init__.py
   ```

2. `__manifest__.py` → obligatoire, décrit le module.
   Exemple minimal :

   ```python
   {
       'name': 'estate',
       'depends': ['base'],
   }
   ```

---

### 3. Relancer Odoo et vérifier

* Redémarre ton serveur Odoo.
* Va dans **Apps** → clique sur **Update Apps List**.
* Recherche **estate**.
* Si tu ne vois pas le module : enlève le filtre “Apps” par défaut.

⚠️ **Astuce** : tu dois activer le **mode développeur** pour voir “Update Apps List”.

---

### 4. Faire apparaître ton module comme une “Application”

* Dans ton `__manifest__.py`, ajoute :

  ```python
  'application': True,
  ```
* Ainsi, ton module apparaîtra dans la liste filtrée des **Apps**.

---

### 5. Installer ton module

* Clique sur **Installer**.
* Ton module est reconnu par Odoo ✅ mais reste une **coquille vide** (pas encore de menus ni de logique).

---

## ✅ Conclusion

À la fin de ce chapitre :

* Tu as un **module vide** (`estate`) détecté par Odoo.
* Il est visible dans les **Apps**.
* Tu peux l’installer, même s’il ne fait encore rien.

👉 Prochaine étape : **créer ton premier modèle de données** pour gérer les biens immobiliers.


