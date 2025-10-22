https://www.odoo.com/documentation/19.0/fr/developer/tutorials/server_framework_101/08_compute_onchange.html.

---

# ✅ Checklists – Étendre avec l’héritage
---


À la fin de ce chapitre, tu sauras :

1. Comment **étendre ou modifier le comportement** d’un modèle existant dans Odoo sans le réécrire.
2. Comment **intercepter les opérations CRUD** (`create`, `write`, `unlink`) pour ajouter des règles métier.
3. Comment **lier ton module à d’autres modèles existants** (comme `res.users`) en ajoutant des champs personnalisés.
4. Comment **modifier les vues existantes** sans les casser, grâce à l’**héritage de vues (`inherit_id`) et XPath**.

---

# 🧩 **1. Concepts fondamentaux**

## 🔹 A. L’héritage Python dans Odoo

Chaque modèle Odoo hérite de `models.Model`, qui fournit les méthodes CRUD :

* `create()` : création d’un enregistrement,
* `write()` : mise à jour,
* `unlink()` : suppression,
* `read()` : lecture.

Tu peux **surcharger ces méthodes** pour ajouter ta logique métier, **mais toujours en appelant `super()`** pour ne pas casser le comportement de base.

Exemple :

```python
@api.model
def create(self, vals):
    # ta logique avant la création
    record = super().create(vals)
    # ta logique après la création
    return record
```

---

## 🔹 B. Les décorateurs spécifiques à Odoo

* `@api.model` → utilisé quand le contenu de `self` n’est pas encore créé (utile pour `create`).
* `@api.ondelete` → permet de gérer les suppressions proprement (plus sûr que surcharger `unlink`).
* `@api.constrains` → valide des données après écriture (vu dans le chapitre sur les contraintes).

---

## 🔹 C. Les deux types d’héritage dans Odoo

L’image que tu as envoyée montre clairement **les deux approches possibles** 👇

| Type d’héritage                    | Mots-clés                                | But                                    | Caractéristiques                                                 |
| ---------------------------------- | ---------------------------------------- | -------------------------------------- | ---------------------------------------------------------------- |
| **Héritage classique (extension)** | `_inherit = 'model.name'`                | Étendre un modèle existant             | Même table en BDD, ajoute/override champs et méthodes            |
| **Héritage par délégation**        | `_inherits = {'model.name': 'field_id'}` | Créer un nouveau modèle lié à un autre | Nouvelle table, jointure automatique, accès aux champs du parent |

---

# 🧱 **2. Implémentation pas à pas**

## 🧩 Étape 1 — Étendre la logique CRUD du module

### 🔸 Objectif :

1. **Empêcher la suppression** d’une propriété sauf si son état est `New` ou `Cancelled`.
2. **Mettre à jour l’état** d’un bien à `Offer Received` lorsqu’une offre est créée.
3. **Empêcher la création d’une offre** avec un prix inférieur à une offre déjà existante.

---

### 🗂️ Fichier : `models/estate_property.py`

```python
from odoo import api, fields, models
from odoo.exceptions import UserError

class EstateProperty(models.Model):
    _inherit = "estate.property"

    @api.ondelete(at_uninstall=False)
    def _check_can_delete(self):
        for record in self:
            if record.state not in ['new', 'cancelled']:
                raise UserError("You can only delete properties that are New or Cancelled.")
```

🧠 **Explication :**

* Le décorateur `@api.ondelete` est préféré à `unlink` car il est plus sûr (s’exécute même lors d’une désinstallation du module).
* Si le `state` n’est pas dans `['new', 'cancelled']`, on bloque la suppression.

---

### 🗂️ Fichier : `models/estate_property_offer.py`

```python
from odoo import api, fields, models
from odoo.exceptions import UserError

class EstatePropertyOffer(models.Model):
    _inherit = "estate.property.offer"

    @api.model
    def create(self, vals):
        property_id = vals.get("property_id")
        if property_id:
            property_rec = self.env["estate.property"].browse(property_id)
            # Vérifier qu’il n’existe pas déjà une offre supérieure
            existing_offer = self.search([("property_id", "=", property_id)], order="price desc", limit=1)
            if existing_offer and vals.get("price", 0) < existing_offer.price:
                raise UserError("You cannot create an offer lower than an existing one.")

            # Met à jour l’état du bien
            property_rec.state = "offer_received"

        return super().create(vals)
```

🧠 **Explication :**

* `self.env["estate.property"].browse(property_id)` crée un recordset basé sur l’ID du bien.
* On cherche la meilleure offre existante (`order="price desc"`) pour la comparaison.
* Si le prix proposé est inférieur → `UserError`.
* On met à jour le champ `state` du bien à `"offer_received"`.

---

## 🧩 Étape 2 — Hériter du modèle `res.users`

### 🔸 Objectif :

Afficher, dans la fiche utilisateur, la **liste des propriétés** dont il est le commercial (`salesperson_id`).

### 🗂️ Fichier : `models/res_users.py`

```python
from odoo import fields, models

class ResUsers(models.Model):
    _inherit = "res.users"

    property_ids = fields.One2many(
        "estate.property",
        "salesperson_id",
        string="Properties",
        domain=[("state", "in", ["new", "offer_received", "offer_accepted"])],
    )
```

🧠 **Explication :**

* `_inherit` → on étend le modèle `res.users`.
* `property_ids` → inverse du champ `salesperson_id` déjà existant sur `estate.property`.
* Le `domain` filtre les propriétés visibles selon leur état.

---

## 🧩 Étape 3 — Étendre la vue `res.users`

### 🔸 Objectif :

Ajouter un onglet "Properties" dans la fiche utilisateur.

### 🗂️ Fichier : `views/res_users_views.xml`

```xml
<odoo>
    <record id="view_users_form_inherit_estate" model="ir.ui.view">
        <field name="name">res.users.form.inherit.estate</field>
        <field name="model">res.users</field>
        <field name="inherit_id" ref="base.view_users_form"/>
        <field name="arch" type="xml">
            <xpath expr="//notebook" position="inside">
                <page string="Properties">
                    <field name="property_ids">
                        <list>
                            <field name="name"/>
                            <field name="expected_price"/>
                            <field name="state"/>
                        </list>
                    </field>
                </page>
            </xpath>
        </field>
    </record>
</odoo>
```

🧠 **Explication :**

* `inherit_id="base.view_users_form"` → on hérite de la vue utilisateur standard.
* `xpath` → localise le `<notebook>` pour y insérer un nouvel onglet.
* L’onglet affiche la liste des propriétés gérées par l’utilisateur.

---

# ✅ **3. Résultat attendu**

### Dans la fiche d’un utilisateur :

* Un nouvel onglet “Properties” apparaît.
* Il liste toutes les propriétés où il est le commercial.
* Les propriétés sont filtrées selon leur état (`New`, `Offer Received`, `Offer Accepted`).

### Dans le module “Estate” :

* Impossible de supprimer un bien sauf s’il est `New` ou `Cancelled`.
* Quand une offre est créée → le bien passe en `Offer Received`.
* Impossible de créer une offre plus basse qu’une précédente.

---

# 🧩 **Structure finale des fichiers**

```
estate/
│
├── models/
│   ├── estate_property.py              → logique CRUD (unlink)
│   ├── estate_property_offer.py        → logique create
│   └── res_users.py                    → extension du modèle utilisateur
│
└── views/
    └── res_users_views.xml             → héritage de la vue utilisateur
```

---

Souhaites-tu que je t’ajoute à la suite la **section suivante du tutoriel (chapitre 13)**, où on aborde l’**interaction entre modules** (et notamment la relation entre “Estate” et “Accounting” dans Odoo) ?
