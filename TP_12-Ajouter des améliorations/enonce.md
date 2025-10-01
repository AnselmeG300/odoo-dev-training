https://www.odoo.com/documentation/19.0/fr/developer/tutorials/server_framework_101/08_compute_onchange.html.

---

# 📘 Chapitre 8 : Computed Fields et Onchanges

---

## 🎯 Objectifs du chapitre

À la fin de ce chapitre, l’apprenant doit être capable de :

1. **Créer des champs calculés (computed fields)** qui dépendent d’autres champs et se mettent à jour automatiquement.

   * Exemple : calculer la surface totale (`total_area`) d’un bien immobilier à partir de la surface habitable et de la surface du jardin.
   * Exemple : calculer la meilleure offre (`best_price`) parmi les offres reçues.

2. **Définir une fonction inverse (inverse function)** afin de rendre certains champs calculés modifiables par l’utilisateur.

   * Exemple : calculer la date limite d’une offre (`date_deadline`) à partir de la durée de validité, mais aussi permettre l’édition inverse.

3. **Mettre en place des `onchange`** pour faciliter la saisie utilisateur dans les formulaires.

   * Exemple : lorsqu’on coche le champ `garden`, initialiser automatiquement une surface de jardin et une orientation par défaut.

👉 L’objectif global est donc de rendre le module **plus intelligent et interactif**, en automatisant des calculs et en assistant l’utilisateur dans la saisie.

---

## 🧩 Notions abordées

### 1. **Computed Fields (Champs calculés)**

* Un champ calculé n’est **pas stocké directement en base** : sa valeur est **calculée à la volée** par Odoo en fonction d’autres champs.
* Il est défini avec l’attribut `compute`.
* On utilise le décorateur `@api.depends` pour indiquer sur quels champs repose le calcul.
* Par défaut, un champ calculé est **read-only**.

Exemple :

```python
total_area = fields.Float(compute="_compute_total_area")

@api.depends("living_area", "garden_area")
def _compute_total_area(self):
    for record in self:
        record.total_area = record.living_area + record.garden_area
```

---

### 2. **Inverse Function (Fonction inverse)**

* Permet à l’utilisateur de **modifier un champ calculé** depuis l’interface.
* Odoo met alors à jour automatiquement les champs dépendants via la fonction `inverse`.
* Utile pour les cas où deux champs dépendent l’un de l’autre (ex. validité ↔ date limite).

Exemple :

```python
date_deadline = fields.Date(
    compute="_compute_date_deadline",
    inverse="_inverse_date_deadline",
    store=True
)
```

---

### 3. **Onchange**

* Mécanisme qui modifie d’autres champs **dans le formulaire**, sans sauvegarde en base, dès qu’un champ change.
* Utile pour **aider l’utilisateur à la saisie**.
* À ne pas utiliser pour de la logique métier, car les `onchange` ne s’exécutent que dans l’interface.

Exemple :

```python
@api.onchange("garden")
def _onchange_garden(self):
    if self.garden:
        self.garden_area = 10
        self.garden_orientation = "North"
    else:
        self.garden_area = 0
        self.garden_orientation = False
```

---

## 🛠️ Implémentation (Pratique)

### Étape 1 : Calculer la surface totale (`total_area`)

Dans `estate_property.py` :

```python
from odoo import fapi

total_area = fields.Float(
    compute="_compute_total_area",
    string="Total Area (sqm)"
)

@api.depends("living_area", "garden_area")
def _compute_total_area(self):
    for record in self:
        record.total_area = record.living_area + record.garden_area
```

👉 Ajouter `total_area` dans l’onglet **Description** de la vue formulaire.

---

### Étape 2 : Calculer la meilleure offre (`best_price`)

Toujours dans `estate_property.py` :

```python
best_price = fields.Float(
    compute="_compute_best_price",
    string="Best Offer"
)

@api.depends("offer_ids.price")
def _compute_best_price(self):
    for record in self:
        if record.offer_ids:
            record.best_price = max(record.offer_ids.mapped("price"))
        else:
            record.best_price = 0.0
```

👉 Ajouter `best_price` dans la vue formulaire (colonne des prix).

---

### Étape 3 : Gérer la validité et la date limite (`estate.property.offer`)

Dans `estate_property_offer.py` :

```python
from datetime import timedelta

validity = fields.Integer(default=7)
date_deadline = fields.Date(
    compute="_compute_date_deadline",
    inverse="_inverse_date_deadline",
    store=True
)

@api.depends("validity", "create_date")
def _compute_date_deadline(self):
    for record in self:
        create_date = record.create_date or fields.Date.today()
        record.date_deadline = create_date + timedelta(days=record.validity)

def _inverse_date_deadline(self):
    for record in self:
        create_date = record.create_date or fields.Date.today()
        record.validity = (record.date_deadline - create_date).days
```

👉 Ajouter `validity` et `date_deadline` dans la **vue formulaire et liste des offres**.

---

### Étape 4 : Onchange pour `garden`

Toujours dans `estate_property.py` :

```python
@api.onchange("garden")
def _onchange_garden(self):
    if self.garden:
        self.garden_area = 10
        self.garden_orientation = "North"
    else:
        self.garden_area = 0
        self.garden_orientation = False
```

👉 Tester en cochant/décochant le champ dans le formulaire.

---

✅ **Objectifs atteints :**

* Champs calculés (`total_area`, `best_price`).
* Fonction inverse (`date_deadline` ↔ `validity`).
* Assistance utilisateur avec `onchange` (`garden`).


