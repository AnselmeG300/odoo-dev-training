https://www.odoo.com/documentation/19.0/fr/developer/tutorials/server_framework_101/08_compute_onchange.html.

---

# ✅ Checklists – Interagir avec d’autres modules

---


À la fin de ce chapitre, tu sauras :

1. Comment **faire communiquer deux modules** Odoo existants entre eux.
2. Comment **créer un module de lien (“bridge module”)**, ici `estate_account`, qui connecte le module *Real Estate* à *Accounting*.
3. Comment **générer automatiquement une facture client** dès qu’une propriété est marquée comme *Sold*.

---

# 🧩 **1️⃣ Comprendre le concept : le “link module”**

## 🏗️ A. Pourquoi un module de lien ?

Odoo est conçu de manière **modulaire** :

* Chaque module a une responsabilité claire (ex : `estate` gère les biens, `account` gère la comptabilité).
* On ne veut pas forcer tous les utilisateurs du module *Real Estate* à installer *Accounting*.

👉 Donc on crée un **troisième module**, par exemple `estate_account`, qui **dépend de** :

```python
'depends': ['estate', 'account']
```

✅ Si les deux sont installés → le lien s’active (facturation automatique).
❌ Si *account* est absent → *estate* continue de fonctionner seul.

C’est une **meilleure pratique Odoo** pour les intégrations modulaires.

---

# 🧠 **2️⃣ Concepts clés de ce chapitre**

### 🧩 Héritage inter-module

On va **hériter du modèle `estate.property`** (défini dans le module `estate`)
pour lui ajouter une logique de création de facture.

Exemple de squelette :

```python
class EstateProperty(models.Model):
    _inherit = "estate.property"

    def action_sold(self):
        # on ajoute notre logique ici
        return super().action_sold()
```

---

### 💳 Création d’une facture (modèle `account.move`)

Une facture dans Odoo est un enregistrement du modèle :

```python
account.move
```

Les champs essentiels :

| Champ              | Description                                               |
| ------------------ | --------------------------------------------------------- |
| `partner_id`       | Le client (ici, l’acheteur du bien)                       |
| `move_type`        | Type de facture (`'out_invoice'` pour une facture client) |
| `journal_id`       | Journal comptable associé                                 |
| `invoice_line_ids` | Lignes de la facture (produits, prix, quantité, etc.)     |

---

### 🧮 Commandes One2many (namespace `Command`)

Pour créer des lignes de facture au moment de la création, on utilise le namespace :

```python
from odoo import Command
```

Exemple :

```python
Command.create({
    'name': 'Administration fees',
    'quantity': 1,
    'price_unit': 100.00,
})
```

Ce mécanisme indique à Odoo de créer une ligne directement lors de la création du `account.move`.

---

# 🧱 **3️⃣ Implémentation pas à pas**

---

## 🧩 Étape 1 — Créer le module `estate_account`

Dans ton dossier `addons`, crée :

```
estate_account/
├── __init__.py
├── __manifest__.py
└── models/
    ├── __init__.py
    └── estate_property.py
```

---

### 🔹 `__manifest__.py`

```python
{
    'name': 'Estate Account',
    'version': '1.0',
    'depends': ['estate', 'account'],
    'data': [],
    'installable': True,
}
```

💡 Cela indique à Odoo que :

* Le module **étend** les fonctionnalités de `estate` et `account`.
* Il ne contient pas encore de vues (`data` est vide pour l’instant).

---

## 🧩 Étape 2 — Hériter du modèle `estate.property`

### 🔹 `models/__init__.py`

```python
from . import estate_property
```

---

### 🔹 `models/estate_property.py`

```python
from odoo import api, models, Command

class EstateProperty(models.Model):
    _inherit = "estate.property"

    def action_sold(self):
        """Extend the sold action to create an invoice."""
        res = super().action_sold()

        # On crée une facture pour l'acheteur
        for property in self:
            if property.buyer_id:
                move_vals = {
                    'partner_id': property.buyer_id.id,
                    'move_type': 'out_invoice',  # Facture client
                    'invoice_line_ids': [
                        # 1️⃣ Ligne : commission (6%)
                        Command.create({
                            'name': f"6% commission for property {property.name}",
                            'quantity': 1,
                            'price_unit': property.selling_price * 0.06,
                        }),
                        # 2️⃣ Ligne : frais administratifs
                        Command.create({
                            'name': 'Administrative fees',
                            'quantity': 1,
                            'price_unit': 100.00,
                        }),
                    ],
                }
                self.env['account.move'].create(move_vals)

        return res
```

---

## 🧩 Étape 3 — Explications détaillées

| Ligne de code                  | Rôle                                                                 |
| ------------------------------ | -------------------------------------------------------------------- |
| `_inherit = "estate.property"` | Étend le modèle existant sans le modifier directement                |
| `res = super().action_sold()`  | Appelle la méthode d’origine pour conserver le comportement existant |
| `if property.buyer_id:`        | Vérifie que la propriété a bien un acheteur                          |
| `move_type='out_invoice'`      | Définit une facture client (et non fournisseur)                      |
| `invoice_line_ids`             | Crée deux lignes automatiquement : commission + frais admin          |
| `Command.create({...})`        | Ajoute dynamiquement une ligne One2many à la création                |

---

## 🧩 Étape 4 — Installation et test

1️⃣ Mets à jour la liste des modules dans Odoo → `Apps > Update Apps List`.
2️⃣ Recherches **Estate Account**, puis installe-le.
3️⃣ Le module `account` sera installé automatiquement (car il est dans les dépendances).
4️⃣ Vends une propriété (`Sold`).
5️⃣ Va dans **Invoicing → Customers → Invoices**.
👉 Tu verras une facture créée automatiquement pour le client avec :

* une ligne “6% commission”,
* une ligne “Administrative fees”.

---

# ✅ **4️⃣ Résultat final**

* Lorsque tu cliques sur **“Sold”**, Odoo crée :

  * Une **facture client** (`account.move`) liée à l’acheteur du bien.
  * Deux lignes de facture :

    * 6 % du prix de vente,
    * 100 € de frais administratifs.
* Cette logique est **isolée** dans le module `estate_account`,
  donc *facultative et réutilisable*.

---

# 🧠 En résumé

| Élément                                 | Rôle                                           |
| --------------------------------------- | ---------------------------------------------- |
| `estate_account`                        | Module de lien entre Real Estate et Accounting |
| `_inherit = "estate.property"`          | Étend la logique de vente                      |
| `self.env['account.move'].create(vals)` | Crée une facture                               |
| `Command.create({...})`                 | Ajoute des lignes à la facture                 |
| `depends = ['estate', 'account']`       | Gère les dépendances modulaires                |


