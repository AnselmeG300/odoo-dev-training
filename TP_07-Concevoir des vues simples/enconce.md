https://www.odoo.com/documentation/19.0/developer/tutorials/backend.html?highlight=views#basic-views


---

# ✅ Checklists – Concevoir des vues simples

### 🎯 Objectif général

Nous allons créer **trois vues personnalisées** pour notre modèle `estate.property` :

1. **List view (vue liste)** → afficher les propriétés sous forme de tableau avec plusieurs colonnes utiles.
2. **Form view (vue formulaire)** → organiser les champs d’un bien immobilier de façon claire (groupes, onglets).
3. **Search view (vue de recherche)** → ajouter des filtres et un regroupement (`group by`) pour faciliter la navigation.

👉 À la fin, tu auras une **interface utilisateur complète** pour gérer les propriétés.

---

## 🔹 1. Les List Views

### Rôle

* Affichent les enregistrements dans un **tableau**.
* Chaque `<field>` = une **colonne**.
* Attribut important :

  * `string="..."` → titre du tableau.

### Exemple pour notre modèle

Fichier : `estate/views/estate_property_views.xml`

```xml
<odoo>
    <record id="view_estate_property_list" model="ir.ui.view">
        <field name="name">estate.property.list</field>
        <field name="model">estate.property</field>
        <field name="arch" type="xml">
            <list string="Properties">
                <field name="name" string="Title"/>
                <field name="postcode"/>
                <field name="bedrooms"/>
                <field name="living_area" string="Living Area (sqm)"/>
                <field name="expected_price"/>
                <field name="selling_price"/>
                <field name="date_availability" string="Available From"/>
            </list>
        </field>
    </record>
</odoo>
```



EXPLICATION DES PARAMETRES: 


---

# 📘 Décryptage du code

---

## 🔹 1. `<odoo> ... </odoo>`

C’est l’**enveloppe** de tout fichier XML d’un module Odoo.
👉 Sans cette balise racine, le module ne peut pas être chargé.

---

## 🔹 2. `<record id="..." model="ir.ui.view">`

Ici on dit à Odoo :

> “Crée (ou mets à jour) un enregistrement dans le modèle `ir.ui.view`.”

* `model="ir.ui.view"` → c’est le **modèle technique d’Odoo** qui stocke toutes les définitions de vues (listes, formulaires, recherches, etc.).
* `id="view_estate_property_list"` → identifiant **externe** de l’enregistrement.

  * Ce nom doit être **unique dans ton module**.
  * Par convention, on met : `view_<nom_module>_<type_vue>`.

    * Ici : `view_estate_property_list` = vue liste du modèle `estate.property`.
  * Tu aurais pu écrire autre chose (`view_properties_table` par ex.), ça marcherait aussi. Mais la convention sert à **rester lisible** quand ton module grossit.

---

## 🔹 3. `<field name="name">estate.property.list</field>`

C’est le **nom interne** de la vue (en base de données).

* Convention : `<nom_modèle>.<type_vue>`

  * `estate.property.list` → vue liste du modèle `estate.property`.
* Ce champ est utilisé **en back-office** par Odoo pour distinguer les vues.

👉 Tu pourrais mettre autre chose (ex. `"My Property List"`), mais ce serait moins clair et risqué pour la maintenance.

---

## 🔹 4. `<field name="model">estate.property</field>`

Ici, on dit à Odoo :

> “Cette vue est liée au modèle `estate.property`.”

👉 Donc dès qu’on ouvre ce modèle dans une action, Odoo sait quelle vue appliquer.

---

## 🔹 5. `<field name="arch" type="xml"> ... </field>`

* `arch` = architecture de la vue → la structure de l’interface.
* `type="xml"` → ce champ contient du code XML, et pas du texte brut.

👉 Tout ce qui est à l’intérieur de ce `<field>` décrit **comment la vue doit s’afficher**.

---

## 🔹 6. `<list string="Properties"> ... </list>`

* `<list>` = on définit une vue de type **liste/tableau**.
* `string="Properties"` → titre affiché en haut de la vue.

---

## 🔹 7. `<field name="..."/>`

Chaque `<field>` = une **colonne** dans la vue liste.

Exemples :

* `<field name="name" string="Title"/>` → affiche la colonne du champ `name`, avec libellé “Title”.
* `<field name="postcode"/>` → affiche le champ `postcode`. Comme on n’a pas mis `string`, Odoo affiche le nom du champ (par défaut défini dans le Python ou via traduction).
* `<field name="living_area" string="Living Area (sqm)"/>` → on personnalise le label en “Living Area (sqm)”.

---

# ❓ Tes questions précises

### 👉 Pourquoi `estate.property.list` comme nom ?

* C’est **une convention** : `<nom_modèle>.<type_vue>`.
* Tu pourrais mettre un autre nom, mais :

  * C’est plus propre de rester sur la convention (lisibilité).
  * Certaines équipes ou modules Odoo attendent cette convention → ça évite les conflits et aide au débogage.

### 👉 Que fait concrètement cette vue ?

* Elle dit à Odoo : “Quand tu affiches les enregistrements du modèle `estate.property`, montre ces colonnes dans un tableau.”
* Concrètement, tu obtiens l’écran avec la table (ta capture 1 du chapitre 6).

### 👉 Est-ce qu’on doit supprimer l’action qu’on avait créée avant ?

* Non ❌.
* **Une action ≠ une vue.**

  * L’action (`ir.actions.act_window`) est le **pont** entre le menu et le modèle.
  * La vue (`ir.ui.view`) est juste **la manière d’afficher les données**.
* Les deux se complètent :

  * Sans action → tu ne peux pas ouvrir le modèle depuis l’UI.
  * Sans vue → Odoo utilise une vue **par défaut** (pas adaptée).

### 👉 Que signifie `<field name="arch" type="xml">` ?

* `arch` = champ spécial du modèle `ir.ui.view`.
* Ce champ contient la **description XML** de la vue.
* `type="xml"` → pour dire à Odoo : *“ce n’est pas du texte, mais du code XML que tu dois interpréter”*.

---

# ✅ Résumé simple

* **Action** = *ouvre un modèle* (mais sans action, tu ne vois rien dans le menu).
* **Vue** = *comment afficher le modèle* (listes, formulaires, recherches, etc.).
* `estate.property.list` = juste un **nom lisible et conventionnel** pour dire “c’est la vue liste du modèle `estate.property`”.
* `<field name="arch" type="xml">` = le cœur de la vue, qui décrit son interface en XML.

---


## 🔹 2. Les Form Views

### Rôle

* Permettent de **créer/éditer un enregistrement**.
* Organisation :

  * `<sheet>` → cadre principal du formulaire.
  * `<group>` → regroupe les champs horizontalement.
  * `<notebook>` → permet de créer des **onglets** (`<page>`).

### Exemple

Toujours dans `estate_property_views.xml` :

```xml
<odoo>
    <record id="view_estate_property_form" model="ir.ui.view">
        <field name="name">estate.property.form</field>
        <field name="model">estate.property</field>
        <field name="arch" type="xml">
            <form string="Properties">
                <sheet>
                    <group>
                        <group>
                            <field name="postcode"/>
                            <field name="date_availability"/>
                        </group>
                        <group>
                            <field name="expected_price"/>
                            <field name="selling_price" readonly="1"/>
                        </group>
                    </group>
                    <notebook>
                        <page string="Description">
                            <field name="description"/>
                            <field name="bedrooms"/>
                            <field name="living_area"/>
                            <field name="facades"/>
                            <field name="garage"/>
                            <field name="garden"/>
                            <field name="garden_area"/>
                            <field name="garden_orientation"/>
                        </page>
                    </notebook>
                </sheet>
            </form>
        </field>
    </record>
</odoo>
```

👉 Ça correspond à ta **capture 2 (form view)** avec le champ “Description” et les champs regroupés.

---

## 🔹 3. Les Search Views

### Rôle

* Servent uniquement à **filtrer et organiser les données**.
* Attributs importants :

  * `<field>` → champs visibles dans la recherche.
  * `<filter>` → boutons pour activer un **filtre prédéfini**.
  * `<groupby>` via `context="{'group_by': '...'}"` → regrouper par un champ.

### Exemple

Toujours dans `estate_property_views.xml` :

```xml
<odoo>
    <record id="view_estate_property_search" model="ir.ui.view">
        <field name="name">estate.property.search</field>
        <field name="model">estate.property</field>
        <field name="arch" type="xml">
            <search string="Search Properties">
                <field name="name"/>
                <field name="postcode"/>
                <field name="expected_price"/>
                <field name="selling_price"/>
                <field name="date_availability"/>

                <!-- Filtre "Available" -->
                <filter name="filter_available"
                        string="Available"
                        domain="[('state', 'in', ['new','offer_received'])]"/>

                <!-- Group by postcode -->
                <filter name="group_by_postcode"
                        string="Group by Postcode"
                        context="{'group_by': 'postcode'}"/>
            </search>
        </field>
    </record>
</odoo>
```

👉 Cela correspond à ta **capture 3 (search avec filtre “Available” et Group By “Postcode”)**.

---

## 🔹 4. Mise en place dans `__manifest__.py`

Il faut déclarer le fichier XML dans ton `__manifest__.py` :

```python
'data': [
    'security/ir.model.access.csv',
    'views/estate_property_views.xml',
],
```

---

## 🔹 5. Commande pour tester

```bash
./odoo-bin --addons-path=addons,../tutorials/ -d rd-demo -u estate --dev xml
```

👉 `--dev xml` = pas besoin de redémarrer entièrement Odoo, un simple **refresh navigateur** suffit.

---

# ✅ Résultat attendu

1. **Vue liste** → tableau avec colonnes : titre, code postal, chambres, surface, prix attendu, prix de vente, dispo.
2. **Vue formulaire** → bien structuré avec groupes et onglet description.
3. **Vue recherche** → filtres + group by utilisables.



