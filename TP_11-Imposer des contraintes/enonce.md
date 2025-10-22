https://www.odoo.com/documentation/19.0/developer/reference/backend/orm.html#constraints-and-indexes

https://www.odoo.com/documentation/19.0/developer/reference/backend/orm.html#odoo.api.constrains

---

# ✅ Checklists – Imposer des contraintes

---

## 🎯 **Objectif général du chapitre**

À la fin de ce chapitre, tu sauras :

1. 🔒 Empêcher **l’enregistrement de données incorrectes** (ex. prix négatif, doublons).
2. 🧮 Appliquer des **règles automatiques de validation** au niveau de la base de données (via SQL).
3. 🧠 Définir des **règles plus complexes côté Python** (via des méthodes de validation).
4. ⚖️ Comprendre **quand utiliser SQL et quand utiliser Python** pour gérer les contraintes.

---

## 🧱 **Contexte**

Jusqu’ici, on a construit notre module en ajoutant :

* des champs,
* des vues,
* des relations,
* et même des actions (pour vendre, annuler, etc.).

Mais actuellement, rien n’empêche :

* de créer un bien immobilier avec un **prix négatif**,
* d’avoir **deux types de propriété avec le même nom**,
* ou d’accepter une **offre trop basse**.

➡️ Il faut donc mettre en place des mécanismes de **contrôle automatique des données**.

Odoo propose deux outils puissants pour cela :

* Les **SQL Constraints** (côté base de données)
* Les **Python Constraints** (côté logique métier)

---

## 🧩 **1. Les contraintes SQL (`models.Constraints`)**

### 📖 Définition

Les **contraintes SQL** permettent de vérifier certaines règles directement **dans la base de données PostgreSQL**.
Elles sont rapides, efficaces et parfaites pour des validations simples (positif, unique, etc.).

### 🧠 Exemple conceptuel

```python
_my_check = models.Constraint("CHECK (x > y)", "x > y is not true")
```

Ce code dit :

> “La valeur du champ `x` doit toujours être supérieure la valeur du champ `y`”

### 💡 Dans notre module immobilier

On va définir les règles suivantes :

#### 🔸 Sur le modèle `estate.property` :

* Le **prix attendu** (`expected_price`) doit être **strictement positif**
* Le **prix de vente** (`selling_price`) doit être **positif**

#### 🔸 Sur le modèle `estate.property.offer` :

* Le **prix de l’offre** (`price`) doit être **strictement positif**

#### 🔸 Sur les modèles `estate.property.type` et `estate.property.tag` :

* Le **nom** (`name`) doit être **unique**

---

### 🧰 **Implémentation (Exemple dans Odoo 19)**

```python
from odoo import models, fields

class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Real Estate Property"

    name = fields.Char(required=True)
    expected_price = fields.Float(required=True)
    selling_price = fields.Float()

    _unique_property_name = models.Constraint("UNIQUE (name)", "The property name must be unique.")
    _check_expected_price_positive = models.Constraint("CHECK (expected_price > 0)", "The expected price must be strictly positive.")
    _check_selling_price_positive = models.Constraint("CHECK (selling_price >= 0)", "The selling price must be positive.")
```

Et pour le modèle des offres :

```python
class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Property Offer"

    price = fields.Float(required=True)

    _check_offer_price_positive = models.Constraint("CHECK (price > 0)", "The offer price must be strictly positive.")
    _check_validity_positive = models.Constraint("CHECK (validity > 0)", "The validity period must be positive.")
```

Pour les noms uniques :

```python
class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Property Type"

    name = fields.Char(required=True)

    _unique_property_type_name = models.Constraint("UNIQUE (name)", "The property type name must be unique.")
```

```python
class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Property Tag"

    name = fields.Char(required=True)

    _unique_property_tag_name = models.Constraint("UNIQUE (name)", "The property tag name must be unique.")
```

---

### ⚠️ **Erreurs fréquentes**

Si ta base contient déjà des valeurs invalides (ex. `expected_price = 0`), Odoo te refusera d’ajouter la contrainte, avec un message :

```
ERROR odoo.schema: Table 'estate_property': unable to add constraint 'estate_property_check_price' as CHECK(expected_price > 0)
```

➡️ Supprime ou corrige les données avant d’ajouter la contrainte.

---

## 🧠 **2. Les contraintes Python (`@api.constrains`)**

### 📖 Définition

Les contraintes Python servent à effectuer **des vérifications plus complexes** que celles possibles avec SQL.

Elles sont exécutées **automatiquement** dès qu’un champ concerné est modifié.
Si la règle n’est pas respectée, Odoo lève une **exception** (erreur bloquante).

### 🧠 Exemple conceptuel

```python
from odoo.exceptions import ValidationError

@api.constrains('end_date')
def _check_date_end(self):
    for record in self:
        if record.end_date < fields.Date.today():
            raise ValidationError("End date cannot be in the past.")
```

---

### 💡 Dans notre module immobilier

Nous voulons qu’une **offre acceptée** ne puisse pas avoir un prix trop bas.
➡️ Le prix de vente (`selling_price`) ne doit pas être **inférieur à 90% du prix attendu (`expected_price`)**.

### 🧰 **Implémentation**

```python
from odoo import api, fields, models
from odoo.exceptions import ValidationError
from odoo.tools.float_utils import float_compare, float_is_zero

class EstateProperty(models.Model):
    _inherit = "estate.property"

    @api.constrains('selling_price', 'expected_price')
    def _check_selling_price(self):
        for record in self:
            if float_is_zero(record.selling_price, precision_rounding=0.01):
                continue  # pas encore de prix de vente, on ne bloque pas
            if float_compare(record.selling_price, record.expected_price * 0.9, precision_rounding=0.01) < 0:
                raise ValidationError("The selling price cannot be lower than 90% of the expected price.")
```

### 🔎 Explication :

* `@api.constrains('selling_price', 'expected_price')`
  → La méthode s’exécute dès que l’un de ces champs change.
* `float_is_zero` et `float_compare`
  → Fonctions précises pour comparer des nombres flottants (évite les erreurs d’arrondi).
* `ValidationError`
  → Bloque l’enregistrement si la condition n’est pas respectée.

---

## ⚖️ **Comparaison SQL vs Python**

| Critère             | SQL Constraint          | Python Constraint                   |
| ------------------- | ----------------------- | ----------------------------------- |
| Exécution           | Base de données         | Serveur Odoo                        |
| Performance         | ⚡ Très rapide           | 🧮 Plus lent                        |
| Complexité          | Simple (>=, <=, unique) | Complexe (calculs, relations)       |
| Message utilisateur | Automatique             | Personnalisé                        |
| Exemple d’usage     | Prix > 0                | Prix de vente ≥ 90% du prix attendu |

💡 **Bon réflexe :**

> Utilise SQL pour les validations simples et Python pour les règles métier avancées.

---

## 📸 **Résultats visibles dans l’interface**

1. 🚫 Si l’utilisateur entre un prix négatif et clique sur **Save**, une erreur s’affiche.
2. 🚫 Si deux “Property Types” ont le même nom → message d’erreur.
3. 🚫 Si le vendeur entre un prix de vente inférieur à 90% du prix attendu → validation bloquée.

---

## ✅ **Résumé du chapitre**

| Élément appris       | Description                                                 |
| -------------------- | ----------------------------------------------------------- |
| `SQL Constraints`    | Vérifications automatiques en base (rapides, simples)       |
| `Python Constraints` | Règles complexes via code (ValidationError)                 |
| `Objectif global`      | Garantir la cohérence et la fiabilité des données           |
| `Exemple concret`      | Prix > 0, noms uniques, prix de vente ≥ 90% du prix attendu |


