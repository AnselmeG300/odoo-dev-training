https://www.odoo.com/documentation/19.0/developer/reference/backend/orm.html#reference-orm-model

https://www.odoo.com/documentation/19.0/developer/reference/backend/orm.html#fields

# ✅ Checklists – Définir les modèles et leurs champs

### 🎯 Objectif général

Dans ce chapitre, nous allons transformer notre module vide (`estate`) en un module capable de **stocker des données**. Pour cela, nous allons créer un **modèle Python** qui correspondra à une **table SQL** dans la base de données, et lui ajouter des **champs de base** (nom, description, prix, surface, etc.) afin de représenter les propriétés immobilières.

---

## 🔹 Étapes détaillées

### Étape 1 : Vérifier que le module est installé

Avant de commencer, assure-toi que le module `estate` est bien installé.
👉 Il doit apparaître comme **Installed** dans la liste des Apps.

⚠️ Si ce n’est pas le cas : installe-le via Apps → Update Apps List → recherche `estate`.

---

### Étape 2 : Créer la structure du modèle

1. Dans ton module `estate`, crée un dossier **models** :

   ```
   costum_addons/tutorials/estate/models/
   ```

2. Dans ce dossier, crée un fichier `estate_property.py`.
   👉 C’est dans ce fichier qu’on va définir la table des propriétés immobilières.

3. Modifie `estate/__init__.py` pour importer ton dossier models :

   ```python
   from . import models
   ```

4. Modifie `estate/models/__init__.py` pour importer ton fichier :

   ```python
   from . import estate_property
   ```

---

### Étape 3 : Définir le modèle minimal

Dans `estate/models/estate_property.py`, ajoute :

```python
from odoo import models

class EstateProperty(models.Model):
    _name = "estate.property"   
```

💡 Explication :

* `_name` = définit le nom de la table (`estate_property`) qui sera créée dans PostgreSQL.
* Le fait d’hériter de `models.Model` dit à Odoo que c’est un **objet métier** qui doit être persisté en base.

---

### Étape 4 : Redémarrer le serveur et mettre à jour le module

Relance Odoo avec les options :

```bash
./odoo-bin --addons-path=addons,../tutorials/ -d rd-demo -u estate
```

* `-d rd-demo` = base de données cible.
* `-u estate` = met à jour ton module pour appliquer la création de la table.

👉 Résultat attendu : une nouvelle table `estate_property` est créée en base.

⚠️ Tu verras peut-être des **warnings** :

* *“no \_description”* → on y remédie à l’étape suivante.
* *“no access rules”* → on traitera plus tard avec la sécurité.

---

### Étape 5 : Ajouter une description

Dans ta classe, ajoute :

```python
_description = "Real Estate Property"
```

👉 Cela permet à Odoo d’afficher une **description lisible** du modèle dans l’interface et supprime le warning.

---

### Étape 6 : Ajouter les champs de base

Toujours dans `estate_property.py` :

```python
from odoo import fields, models

class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Real Estate Property"

    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date()
    expected_price = fields.Float(required=True)
    selling_price = fields.Float()
    bedrooms = fields.Integer()
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        [
            ('north', 'North'),
            ('south', 'South'),
            ('east', 'East'),
            ('west', 'West'),
        ],
        string="Garden Orientation"
    )
```

💡 Explication :

* Chaque attribut de la classe correspond à une **colonne SQL** dans `estate_property`.
* Exemple : `name = fields.Char(required=True)` → crée une colonne `name` de type VARCHAR qui est obligatoire.
* `Selection` crée une liste de choix (ici : orientation du jardin).

---

### Étape 7 : Redémarrer Odoo pour appliquer les changements

À chaque fois que tu modifies un modèle Python, tu dois redémarrer et mettre à jour :

```bash
./odoo-bin --addons-path=addons,../tutorials/ -d rd-demo -u estate
```

👉 Cela met à jour la base avec les nouveaux champs.

---

### Étape 8 : Vérifier la table dans PostgreSQL

Connecte-toi à PostgreSQL :

```bash
psql -d rd-demo
```

Puis :

```sql
\d estate_property;
```

👉 Tu dois voir toutes les colonnes (name, description, price, etc.).
Odoo a aussi ajouté automatiquement :

* `id` (identifiant unique)
* `create_date`, `create_uid`, `write_date`, `write_uid` (pistes de modifications).

---

## ✅ Résultat final attendu

* Ton module `estate` contient un modèle **estate.property**.
* La table SQL `estate_property` existe dans ta base.
* Les champs principaux (nom, prix, surface, chambres, jardin, etc.) sont créés.
* Les champs `name` et `expected_price` sont obligatoires.

👉 Ton module peut maintenant **stocker de vraies données** de biens immobiliers.
