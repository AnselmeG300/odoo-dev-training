https://www.odoo.com/documentation/19.0/developer/reference/backend/orm.html#relational-fields

---

# ✅ Checklists – Relier les modèles

## 🎯 Objectif général

Nous allons enrichir notre module immobilier (`estate.property`) en :

1. Catégorisant les biens (ex. maison, appartement → `estate.property.type`),
2. Liant un bien à un acheteur et un vendeur (`res.partner` et `res.users`),
3. Ajoutant des **tags** multiples sur un bien (`estate.property.tag`),
4. Gérant la liste des **offres reçues** (`estate.property.offer`).

---

## 🔹 1. Concepts de base : les relations en Odoo

En Python pur, tu pourrais dire :

* Un objet **Maison** a **un type** (Many2one),
* Un objet **Maison** peut avoir **plusieurs tags** (Many2many),
* Un objet **Maison** peut recevoir **plusieurs offres** (One2many).

👉 En Odoo, ces liens se traduisent par 3 champs spéciaux :

1. **Many2one** : relation simple → champ de sélection (dropdown).

   ```python
   property_type_id = fields.Many2one("estate.property.type", string="Property Type")
   ```

   * Suffixe conseillé : `_id`.

2. **Many2many** : relation multiple ↔ multiple.

   ```python
   tag_ids = fields.Many2many("estate.property.tag", string="Tags")
   ```

   * Suffixe conseillé : `_ids`.

3. **One2many** : liste inversée → nécessite un Many2one dans le modèle enfant.

   ```python
   offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offers")
   ```

   * Le `property_id` doit exister dans le modèle `estate.property.offer`.

---

## 🔹 2. Implémentation étape par étape

### Étape 1 : **Créer le modèle `estate.property.type`**

📂 `estate/models/estate_property_type.py`

```python
from odoo import models, fields

class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Property Type"

    name = fields.Char(required=True)
```

📂 `estate/views/estate_property_type_views.xml`

```xml
<odoo>
    <record id="view_estate_property_type_form" model="ir.ui.view">
        <field name="name">estate.property.type.form</field>
        <field name="model">estate.property.type</field>
        <field name="arch" type="xml">
            <form string="Property Type">
                <sheet>
                    <field name="name"/>
                </sheet>
            </form>
        </field>
    </record>

    <record id="view_estate_property_type_list" model="ir.ui.view">
        <field name="name">estate.property.type.list</field>
        <field name="model">estate.property.type</field>
        <field name="arch" type="xml">
            <list string="Property Types">
                <field name="name"/>
            </list>
        </field>
    </record>

    <record id="action_estate_property_type" model="ir.actions.act_window">
        <field name="name">Property Types</field>
        <field name="res_model">estate.property.type</field>
        <field name="view_mode">list,form</field>
    </record>

    <menuitem id="menu_estate_property_type" name="Property Types"
              parent="estate_menu_root"
              action="action_estate_property_type"/>
</odoo>
```

Puis dans `estate/models/estate_property.py`, on ajoute le lien :

```python
property_type_id = fields.Many2one("estate.property.type", string="Property Type")
```

---

### Étape 2 : **Acheteur & Vendeur**

Toujours dans `estate_property.py` :

```python
buyer_id = fields.Many2one("res.partner", string="Buyer", copy=False)
salesman_id = fields.Many2one("res.users", string="Salesman",
                              default=lambda self: self.env.user)
```

👉 Explications :

* `res.partner` = personnes ou sociétés (clients, fournisseurs…).
* `res.users` = utilisateurs Odoo (ici, nos commerciaux).
* `copy=False` = le champ n’est pas copié quand on duplique un bien.
* `default=lambda self: self.env.user` = par défaut, le vendeur = l’utilisateur connecté.

Dans la vue `estate_property_views.xml`, ajoute un onglet **Other Info** :

```xml
<notebook>
    <page string="Other Info">
        <group>
            <field name="salesman_id"/>
            <field name="buyer_id"/>
        </group>
    </page>
</notebook>
```

---

### Étape 3 : **Créer le modèle `estate.property.tag`**

📂 `estate/models/estate_property_tag.py`

```python
from odoo import models, fields

class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Property Tag"

    name = fields.Char(required=True)
```

Dans `estate_property.py` :

```python
tag_ids = fields.Many2many("estate.property.tag", string="Tags")
```

Vue `estate_property_tag_views.xml` :

```xml
<odoo>
    <record id="view_estate_property_tag_form" model="ir.ui.view">
        <field name="name">estate.property.tag.form</field>
        <field name="model">estate.property.tag</field>
        <field name="arch" type="xml">
            <form string="Property Tag">
                <sheet>
                    <field name="name"/>
                </sheet>
            </form>
        </field>
    </record>

    <record id="view_estate_property_tag_list" model="ir.ui.view">
        <field name="name">estate.property.tag.list</field>
        <field name="model">estate.property.tag</field>
        <field name="arch" type="xml">
            <list string="Property Tags">
                <field name="name"/>
            </list>
        </field>
    </record>

    <record id="action_estate_property_tag" model="ir.actions.act_window">
        <field name="name">Property Tags</field>
        <field name="res_model">estate.property.tag</field>
        <field name="view_mode">list,form</field>
    </record>

    <menuitem id="menu_estate_property_tag" name="Property Tags"
              parent="estate_menu_root"
              action="action_estate_property_tag"/>
</odoo>
```

Dans la vue `estate_property_views.xml` :

```xml
<field name="tag_ids" widget="many2many_tags"/>
```

---

### Étape 4 : **Créer le modèle `estate.property.offer`**

📂 `estate/models/estate_property_offer.py`

```python
from odoo import models, fields

class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Property Offer"

    price = fields.Float()
    status = fields.Selection(
        [('accepted', 'Accepted'),
         ('refused', 'Refused')],
        copy=False
    )
    partner_id = fields.Many2one("res.partner", string="Partner", required=True)
    property_id = fields.Many2one("estate.property", string="Property", required=True)
```

Dans `estate_property.py` :

```python
offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offers")
```

Vue `estate_property_offer_views.xml` (pas de menu/action car accessible seulement via `estate.property`) :

```xml
<odoo>
    <record id="view_estate_property_offer_form" model="ir.ui.view">
        <field name="name">estate.property.offer.form</field>
        <field name="model">estate.property.offer</field>
        <field name="arch" type="xml">
            <form string="Property Offer">
                <sheet>
                    <group>
                        <field name="price"/>
                        <field name="partner_id"/>
                        <field name="status"/>
                    </group>
                </sheet>
            </form>
        </field>
    </record>

    <record id="view_estate_property_offer_list" model="ir.ui.view">
        <field name="name">estate.property.offer.list</field>
        <field name="model">estate.property.offer</field>
        <field name="arch" type="xml">
            <list string="Property Offers">
                <field name="price"/>
                <field name="partner_id"/>
                <field name="status"/>
            </list>
        </field>
    </record>
</odoo>
```

Dans `estate_property_views.xml`, ajoute un onglet **Offers** :

```xml
<page string="Offers">
    <field name="offer_ids"/>
</page>
```

---

## ✅ Résultat attendu

* Un bien a :

  * un **type** (`Many2one`),
  * un **acheteur** (`Many2one res.partner`),
  * un **vendeur** (`Many2one res.users`),
  * plusieurs **tags** (`Many2many`),
  * plusieurs **offres** (`One2many`).
* L’UI reflète tout cela avec des onglets (Description, Other Info, Offers).
* Tu peux créer un bien, lui associer un type, des tags, puis saisir des offres.
