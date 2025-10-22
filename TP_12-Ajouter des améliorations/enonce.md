https://www.odoo.com/documentation/19.0/developer/reference/user_interface/view_records.html

https://www.odoo.com/documentation/19.0/developer/reference/user_interface/view_architectures.html

---

# ✅ Checklists – Ajouter des améliorations

---

## 🎯 **Objectif général du chapitre**

À la fin de cette section, tu sauras :

1. Améliorer l’apparence et l’ergonomie des vues.
2. Créer des vues *inline* (listes intégrées à un formulaire).
3. Utiliser des *widgets* pour modifier la présentation des champs.
4. Définir des ordres d’affichage par défaut ou manuels.
5.  Gérer la visibilité et l’éditabilité conditionnelle de champs et boutons.
6. Ajouter des décorations et couleurs dans les listes.
7. Configurer les filtres et recherches avancées.
8. Ajouter des *stat buttons* pour accéder rapidement à des données liées.

Ce chapitre est donc un mélange de **concepts UI + notions avancées de vue XML + intégration de logique de présentation.**

---

## 🧩 SECTION 1 — **Inline Views (Vues intégrées)**

### Concept

Une *inline view* est une **vue définie directement à l’intérieur d’un formulaire**.
Elle permet d’afficher une liste liée (One2many) de manière plus concise ou personnalisée.

### Exemple

Dans notre cas, on veut que chaque **type de propriété** (`estate.property.type`) affiche la liste des propriétés qui lui sont liées (`estate.property`) dans son formulaire.

➡️ On ne veut pas toutes les colonnes, juste les plus importantes :
le nom (`name`), le prix attendu (`expected_price`), et l’état (`state`).

### Implémentation

**Modèle :**

```python
class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Property Type"

    name = fields.Char(required=True)
    sequence = fields.Integer()
    property_ids = fields.One2many("estate.property", "property_type_id", string="Properties")

    _order = "sequence, name"
```

**Vue XML :**

```xml
<record id="view_estate_property_type_form" model="ir.ui.view">
    <field name="name">estate.property.type.form</field>
    <field name="model">estate.property.type</field>
    <field name="arch" type="xml">
        <form string="Property Type">
            <sheet>
                <group>
                    <field name="name"/>
                </group>
                <notebook>
                    <page string="Properties">
                        <field name="property_ids">
                            <list>
                                <field name="name"/>
                                <field name="expected_price"/>
                                <field name="state"/>
                            </list>
                        </field>
                    </page>
                </notebook>
            </sheet>
        </form>
    </field>
</record>
```

👉 Cette liste est directement intégrée dans le formulaire, sans créer une vue séparée.
Elle donne un aperçu rapide des propriétés liées.

---

## 🎨 SECTION 2 — **Widgets**

### Concept

Un **widget** contrôle **la manière dont un champ est affiché** dans la vue (liste, formulaire, kanban…).
Par défaut, Odoo choisit le widget en fonction du type du champ, mais tu peux le personnaliser.

### Exemple 1 — `statusbar` pour le champ `state`

**Objectif :**
Afficher les états d’une propriété sous forme de barre visuelle (“New → Offer Received → Offer Accepted → Sold”).

**Code XML :**

```xml
<field name="state" widget="statusbar"
       statusbar_visible="new,offer_received,offer_accepted,sold"/>
```

✅ Cela rend le flux de statut clair pour l’utilisateur.

---

### Exemple 2 — `many2many_tags` avec couleurs

**Objectif :**
Donner une couleur aux tags (`estate.property.tag`).

**Modèle :**

```python
class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Property Tag"

    name = fields.Char(required=True)
    color = fields.Integer(string="Color")
```

**Vue XML :**

```xml
<field name="tag_ids" widget="many2many_tags" options="{'color_field': 'color'}"/>
```

✅ Chaque tag affiché dans le formulaire sera coloré selon son champ `color`.

---

## SECTION 3 — **Ordre d’affichage (List Order)**

### Concept

L’ordre par défaut des enregistrements peut être défini :

* soit dans le **modèle Python** via l’attribut `_order`,
* soit dans la **vue XML** via `default_order`.

### Implémentation

```python
class EstateProperty(models.Model):
    _name = "estate.property"
    _order = "id desc"
```

```python
class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _order = "price desc"
```

💡 `estate.property.type` et `estate.property.tag` peuvent être triés par `name` :

```python
_order = "name"
```

---

## ✋ SECTION 4 — **Ordre manuel avec `sequence`**

### Concept

Le champ `sequence` permet à l’utilisateur de **réorganiser les lignes manuellement** depuis la vue.

**Exemple sur `estate.property.type` :**

```python
sequence = fields.Integer()
_order = "sequence, name"
```

**Vue XML :**

```xml
<list>
    <field name="sequence" widget="handle"/>
    <field name="name"/>
</list>
```

➡️ Le petit symbole de poignée “≡” permet de glisser-déposer les lignes.

---

## 🧠 SECTION 5 — **Options et attributs : invisible, readonly, required**

### Concept

Ces attributs rendent les champs ou boutons **visibles, modifiables ou obligatoires** en fonction d’une condition.

---

### Exemple 1 — Condition sur les boutons

Les boutons “Sold” et “Cancel” doivent disparaître une fois la propriété vendue ou annulée :

```xml
<button name="action_sold" type="object" string="Sold"
        class="btn-primary" invisible="state in ['sold', 'cancelled']"/>
<button name="action_cancel" type="object" string="Cancel"
        class="btn-secondary" invisible="state in ['sold', 'cancelled']"/>
```

---

### Exemple 2 — Condition sur des champs

Si `garden` n’est pas coché, on masque la surface et l’orientation :

```xml
<field name="garden_area" invisible="not garden"/>
<field name="garden_orientation" invisible="not garden"/>
```

---

### Exemple 3 — Boutons d’offre invisibles selon l’état

Dans `estate.property.offer` :

```xml
<button name="action_accept" type="object" string="Accept" class="btn-primary"
    invisible="status == 'accepted'"/>
<button name="action_refuse" type="object" string="Refuse" class="btn-secondary"
    invisible="status == 'refused'"/>
```

---

## 🖌️ SECTION 6 — **Décorations et couleurs dans les listes**

### Concept

Les attributs `decoration-*` permettent de colorer les lignes selon certaines conditions.

**Exemples :**

```xml
<list decoration-muted="state=='sold'"
      decoration-success="state in ('offer_received','offer_accepted')"
      decoration-bf="state=='offer_accepted'">
```

**Dans les offres :**

```xml
<list decoration-danger="status=='refused'" decoration-success="status=='accepted'">
    <field name="price"/>
    <field name="partner_id"/>
</list>
```

---

## 🧩 SECTION 7 — **Recherche (Search View)**

### Concepts clés

* `search_default_{name}` → applique un filtre par défaut.
* `filter_domain` → personnalise la logique de recherche sur un champ.

**Exemples :**

```xml
<field name="living_area" filter_domain="[('living_area', '>=', self)]"/>
```

```xml
<filter name="available" string="Available" domain="[('state', '=', 'new')]"/>
```

Puis dans l’action :

```xml
<context>{'search_default_available': 1}</context>
```

✅ Cela applique automatiquement le filtre “Available” au démarrage.

---

## 📊 SECTION 8 — **Stat Buttons**

### Concept

Les *stat buttons* sont des boutons d’action affichés en haut à droite d’un formulaire.
Ils servent à accéder rapidement à des données liées.

---

### Exemple complet

**1️⃣ Ajout d’un champ lié dans `estate.property.offer`:**

```python
property_type_id = fields.Many2one(related="property_id.property_type_id", store=True)
```

**2️⃣ Ajout du champ inverse dans `estate.property.type`:**

```python
offer_ids = fields.One2many("estate.property.offer", "property_type_id")
offer_count = fields.Integer(compute="_compute_offer_count")

def _compute_offer_count(self):
    for record in self:
        record.offer_count = len(record.offer_ids)
```

**3️⃣ Vue avec bouton :**

```xml
<header>
    <button name="%(estate.action_property_offer)d" type="action"
            icon="fa-envelope" string="Offers"
            context="{'search_default_property_type_id': active_id}"
            invisible="offer_count == 0"/>
    <field name="offer_count" widget="statinfo" string="Offers"/>
</header>
```

✅ Cliquer sur le bouton affiche les offres liées à ce type de propriété.

---

## 🧾 **Résumé du chapitre**

| Thème        | Objectif principal                  | Exemple                            |
| ------------ | ----------------------------------- | ---------------------------------- |
| Inline views | Lier une liste au formulaire parent | Liste des propriétés par type      |
| Widgets      | Modifier l’affichage d’un champ     | `statusbar`, `many2many_tags`      |
| Ordering     | Définir l’ordre des listes          | `_order = 'id desc'`               |
| Sequence     | Ordre manuel des types              | Champ `sequence` + widget `handle` |
| Attributes   | Conditions d’affichage              | `attrs="{'invisible': [...]}"`     |
| Decorations  | Colorer les lignes                  | `decoration-success`               |
| Search       | Filtres et domaines personnalisés   | `search_default_available`         |
| Stat Buttons | Accès rapide aux données liées      | Bouton “Offers” sur Property Type  |


