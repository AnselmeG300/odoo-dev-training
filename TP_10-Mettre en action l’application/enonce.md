https://www.odoo.com/documentation/19.0/developer/reference/backend/actions.html

https://www.odoo.com/documentation/19.0/developer/reference/backend/orm.html#reference-exceptions

---

# ✅ Checklists – Mettre en action l’application

---


## 🎯 Objectifs du chapitre

À la fin de ce chapitre, l’apprenant doit être capable de :

1. **Relier des boutons d’action dans les vues à des méthodes Python** pour exécuter de la logique métier.
2. **Créer des actions utilisateur** qui modifient l’état d’un enregistrement (par exemple : marquer un bien comme *vendu* ou *annulé*).
3. **Mettre en œuvre des règles métier** pour empêcher certaines actions invalides (ex : un bien vendu ne peut plus être annulé).
4. **Automatiser la mise à jour de champs liés** lors d’actions (ex : lorsqu’une offre est acceptée, mettre à jour le prix de vente et le nom de l’acheteur).

👉 Ce chapitre introduit un concept fondamental d’Odoo : **les actions déclenchées par l’utilisateur** à travers des **boutons**.

---

## 🧩 Notions abordées

### 1. **Les actions utilisateur (Object methods)**

Dans Odoo, une **action utilisateur** est une méthode Python qui s’exécute lorsqu’un utilisateur clique sur un bouton dans l’interface.

Exemple :

```xml
<button name="action_do_something" type="object" string="Do Something"/>
```

* `name` → le nom de la méthode Python à exécuter.
* `type="object"` → indique à Odoo qu’il s’agit d’un appel de méthode métier.
* `string` → le texte du bouton affiché dans l’interface.

Méthode associée :

```python
def action_do_something(self):
    for record in self:
        record.name = "Something"
    return True
```

🔹 **Règles importantes :**

* Les méthodes appelées par les boutons sont **publiques**, donc **pas de préfixe `_`**.
* Toujours boucler sur `self`, car l’action peut s’appliquer à plusieurs enregistrements.
* Toujours retourner une valeur (souvent `True`).

---

### 2. **Gestion des états (State machine)**

Le champ `state` d’un modèle permet de représenter les **étapes d’un processus métier** (workflow).

Exemple dans `estate.property` :

```python
state = fields.Selection(
    [
        ('new', 'New'),
        ('offer_received', 'Offer Received'),
        ('offer_accepted', 'Offer Accepted'),
        ('sold', 'Sold'),
        ('cancelled', 'Cancelled'),
    ],
    string='Status',
    required=True,
    copy=False,
    default='new'
)
```

Les actions que nous allons créer vont simplement **modifier la valeur du champ `state`** :

* `action_sold()` → `state = 'sold'`
* `action_cancel()` → `state = 'cancelled'`

💡 On parlera alors de **machine à états** : chaque bouton déplace l’enregistrement d’un état à un autre selon certaines règles.

---

### 3. **Lever des erreurs métier (UserError)**

Pour empêcher des actions invalides, Odoo permet de **lever des erreurs** via la classe `UserError` :

```python
from odoo.exceptions import UserError

if record.state == 'sold':
    raise UserError("A sold property cannot be cancelled.")
```

👉 L’erreur s’affiche à l’écran et bloque l’exécution.
C’est la manière recommandée d’imposer des **règles de validation métier** côté serveur.

---

### 4. **Actions sur d’autres modèles**

Une action peut aussi impacter un autre modèle.
Exemple : quand une **offre** est acceptée, cela modifie le bien immobilier associé :

* On définit l’acheteur (`buyer_id`) sur `estate.property`
* On met à jour le prix de vente (`selling_price`)

C’est ainsi qu’Odoo gère la cohérence des données entre modèles liés.

---

## 🛠️ Implémentation (Pratique)

### Étape 1️⃣ : Ajouter les boutons dans la vue `estate.property`

Dans `estate/views/estate_property_views.xml` :

```xml
<record id="view_estate_property_form" model="ir.ui.view">
    <field name="name">estate.property.form</field>
    <field name="model">estate.property</field>
    <field name="arch" type="xml">
        <form string="Properties">
            <header>
                <button name="action_sold" type="object" string="Sold"
                        class="btn-primary" invisible="state in ['sold', 'cancelled']"/>
                <button name="action_cancel" type="object" string="Cancel"
                        class="btn-secondary" invisible="state in ['sold', 'cancelled']"/>
                <field name="state" widget="statusbar"/>
            </header>

            <sheet>
                <!-- ton contenu existant -->
            </sheet>
        </form>
    </field>
</record>
```

---

### Étape 2️⃣ : Ajouter la logique métier dans `estate_property.py`

```python
from odoo import fields, models, api
from odoo.exceptions import UserError

class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Real Estate Property"

    state = fields.Selection([
        ('new', 'New'),
        ('offer_received', 'Offer Received'),
        ('offer_accepted', 'Offer Accepted'),
        ('sold', 'Sold'),
        ('cancelled', 'Cancelled')
    ], string='Status', required=True, copy=False, default='new')

    def action_sold(self):
        for record in self:
            if record.state in ['sold', 'cancelled']:
                raise UserError("A cancelled property cannot be sold.")
            record.state = 'sold'
        return True

    def action_cancel(self):
        for record in self:
            if record.state in ['sold', 'cancelled']:
                raise UserError("A sold property cannot be cancelled.")
            record.state = 'cancelled'
        return True
```

---

### Étape 3️⃣ : Ajouter les boutons dans la vue `estate.property.offer`

Dans `estate/views/estate_property_offer_views.xml` :

```xml
<record id="view_estate_property_offer_form" model="ir.ui.view">
    <field name="name">estate.property.offer.form</field>
    <field name="model">estate.property.offer</field>
    <field name="arch" type="xml">
        <form string="Offers">
            <header>
                <button name="action_accept" type="object" string="Accept" class="btn-primary"
                        invisible="status = 'accepted'"/>
                <button name="action_refuse" type="object" string="Refuse" class="btn-secondary"
                        invisible="status = 'refused'"/>
                <field name="status" widget="statusbar"/>
            </header>
            <sheet>
                <group>
                    <field name="price"/>
                    <field name="partner_id"/>
                    <field name="validity"/>
                    <field name="date_deadline"/>
                </group>
            </sheet>
        </form>
    </field>
</record>
```

---

### Étape 4️⃣ : Logique métier pour accepter ou refuser une offre

Dans `estate_property_offer.py` :

```python
from odoo import models, fields
from odoo.exceptions import UserError

class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property Offer"

    status = fields.Selection([
        ('accepted', 'Accepted'),
        ('refused', 'Refused')
    ], copy=False)

    def action_accept(self):
        for record in self:
            if record.property_id.state in ['sold', 'cancelled']:
                raise UserError("Cannot accept an offer for a sold or cancelled property.")
            # Une seule offre acceptée par bien
            other_offers = record.property_id.offer_ids - record
            other_offers.write({'status': 'refused'})
            record.status = 'accepted'
            record.property_id.selling_price = record.price
            record.property_id.buyer_id = record.partner_id
            record.property_id.state = 'offer_accepted'
        return True

    def action_refuse(self):
        for record in self:
            record.status = 'refused'
        return True
```

---

## ✅ Résultat attendu

* Les boutons **“Sold”** et **“Cancel”** apparaissent en haut du formulaire du bien immobilier.

  * Un bien *annulé* ne peut plus être vendu.
  * Un bien *vendu* ne peut plus être annulé.

* Dans les offres :

  * Les boutons **“Accept”** et **“Refuse”** sont visibles.
  * Lorsqu’une offre est acceptée :

    * Le **prix de vente** et le **nom de l’acheteur** sont automatiquement mis à jour sur le bien.
    * Les autres offres sont automatiquement refusées.

---

## 🧠 À retenir

| Élément                          | Rôle                                                           |
| -------------------------------- | -------------------------------------------------------------- |
| **type="object"**                | Appelle une méthode Python                                     |
| **Public method**                | Pas de `_` devant le nom                                       |
| **UserError**                    | Empêche les actions invalides                                  |
| **State field**                  | Sert à suivre le statut d’un enregistrement                    |
| **Actions sur d’autres modèles** | Permettent de propager des effets logiques entre entités liées |


