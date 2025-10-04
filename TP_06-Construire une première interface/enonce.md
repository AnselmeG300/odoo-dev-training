https://www.odoo.com/documentation/19.0/fr/developer/tutorials/server_framework_101/05_firstui.html

Parfait 👌 Tu touches ici à un point crucial : **l’introduction des vues en XML dans Odoo**.
C’est là où beaucoup d’apprenants se perdent, car ils recopient des bouts de code sans comprendre :

* ce qu’est une **action**,
* ce qu’est un **menuitem**,
* à quoi sert chaque **attribut** XML,
* et surtout comment tout cela **s’articule avec les modèles Python**.

Je vais donc t’expliquer **pas à pas** :

1. la logique générale (avec analogies objet),
2. le rôle de chaque élément XML,
3. les étapes pratiques du chapitre,
   pour que toi et tes apprenants compreniez vraiment **le “pourquoi” derrière le code**.

---

# ✅ Checklists – Construire une première interface

### 🎯 Objectif général

Nous allons enfin connecter notre modèle Python `estate.property` avec une **interface graphique** dans Odoo.
Concrètement, nous allons :

1. Définir une **action** → lien entre un modèle et des vues,
2. Créer des **menus** → pour naviguer dans l’UI et atteindre cette action,
3. Personnaliser des **champs et comportements** dans la vue (valeurs par défaut, champs en lecture seule, champs réservés comme `active` ou `state`).

---

## 🔹 1. Comprendre la logique XML dans Odoo

Odoo est conçu comme une **application orientée objets**, où :

* **Les modèles (Python)** = les classes (logique métier + stockage en DB),
* **Les vues (XML)** = la manière de représenter les objets (UI),
* **Les actions** = les ponts qui disent : *“ouvre ce modèle, avec ces vues, via ce menu”*.

👉 C’est comme en POO : un objet peut être instancié, mais il faut un **contrat d’accès** pour savoir comment l’afficher ou l’utiliser.

---

## 🔹 2. Les fichiers XML de vues

### Exemple : une action de base

```xml
<odoo>
  <record id="estate_property_action" model="ir.actions.act_window">
      <field name="name">Properties</field>
      <field name="res_model">estate.property</field>
      <field name="view_mode">list,form</field>
  </record>
</odoo>
```

### Décryptage attribut par attribut

* `<record>`

  * **id="estate\_property\_action"** → identifiant externe unique (sert de référence dans les menus).
  * **model="ir.actions.act\_window"** → type d’objet créé : une *action de fenêtre* (affiche des vues list/form).

* `<field name="name">Properties</field>`
  👉 Nom affiché de l’action.

* `<field name="res_model">estate.property</field>`
  👉 Le modèle Python concerné.

* `<field name="view_mode">list,form</field>`
  👉 Quelles vues utiliser par défaut (liste + formulaire).

⚠️ Retenir :
Une **action** = lien entre *un modèle* et *des vues*. Sans action, impossible d’ouvrir un modèle depuis l’interface.

---

## 🔹 3. Les menus (navigation)

### Exemple

```xml
<odoo>
  <menuitem id="estate_menu_root" name="Real Estate"/>
  <menuitem id="estate_menu_property" name="Properties" parent="estate_menu_root" action="estate_property_action"/>
</odoo>
```

### Décryptage

* `<menuitem>` crée une entrée de menu.
* **id** : identifiant externe.
* **name** : libellé affiché dans l’UI.
* **parent** : permet d’imbriquer ce menu sous un autre.
* **action** : relie le menu à une action (et donc à un modèle).

👉 Structure hiérarchique typique :

* **Root menu** (visible dans le sélecteur d’applications).
* **First level menu** (barre horizontale).
* **Action menus** (ouvrent les vues).

Sans **menuitem**, tes modèles existent mais sont invisibles à l’utilisateur.

---

## 🔹 4. Personnalisation des champs (via attributs Python)

Certains attributs affectent **le comportement du champ dans la vue** :

* `required=True` → champ obligatoire.
* `readonly=True` → champ en lecture seule.
* `copy=False` → la valeur ne sera pas copiée lors de la duplication.
* `default=...` → valeur par défaut.

### Exemple (dans `estate_property.py`) :

```python
from dateutil.relativedelta import relativedelta

selling_price = fields.Float(readonly=True, copy=False)
bedrooms = fields.Integer(default=2)
date_availability = fields.Date(default=lambda self: fields.Date.today() + relativedelta(months=3), copy=False)
```

👉 Ainsi :

* `selling_price` = calculé plus tard, donc interdit en saisie directe.
* `bedrooms` = 2 par défaut.
* `date_availability` = 3 mois après la date du jour, et ne se copie pas.

---

## 🔹 5. Champs réservés

Certains champs ont un comportement **spécial** si tu les ajoutes à ton modèle :

* `active = fields.Boolean(default=True)`
  👉 Si `active=False`, l’enregistrement est **invisible par défaut** dans les vues.
* `state = fields.Selection([...], required=True, default="new", copy=False)`
  👉 Champ d’état (workflow) utilisé pour gérer les étapes métier (ex. `New`, `Sold`).

⚠️ Ces champs ne sont pas “magiques”, mais Odoo les traite avec un comportement spécifique intégré dans son framework.

---

## 🔹 6. Étapes pratiques du chapitre

### Étape 1 : Créer le fichier des vues

Créer `estate/views/estate_property_views.xml` et l’ajouter dans `__manifest__.py` :

```python
'data': [
    'security/ir.model.access.csv',
    'views/estate_property_views.xml',
],
```

### Étape 2 : Définir une action

Ajoute une action de type `ir.actions.act_window` pour `estate.property`.

### Étape 3 : Définir les menus

Créer `estate/views/estate_menus.xml` avec une structure 3 niveaux :

* Root menu = “Real Estate”
* First level = “Properties”
* Action menu = qui appelle `estate_property_action`.

### Étape 4 : Personnaliser le modèle Python

Dans `estate_property.py` :

* `selling_price` → readonly + copy=False
* `date_availability` → default + copy=False
* `bedrooms` → default=2
* Ajouter `active` avec `default=True`
* Ajouter `state` avec 5 valeurs (`new`, `offer_received`, `offer_accepted`, `sold`, `cancelled`).

### Étape 5 : Redémarrer et tester

```bash
./odoo-bin --addons-path=addons,../tutorials/ -d rd-demo -u estate
```

Puis dans l’UI :

* Naviguer via le nouveau menu.
* Créer un bien immobilier.
* Vérifier que les comportements par défaut (readonly, defaults, copy) fonctionnent.

---

## ✅ Résultat attendu

* Tu as une **interface complète** : menus → action → vues.
* Tu comprends chaque **attribut XML** et son rôle.
* Les champs sensibles (`selling_price`, `date_availability`) ont un comportement correct.
* Tu sais maintenant **lire et t’inspirer des vues existantes** pour construire les tiennes.


