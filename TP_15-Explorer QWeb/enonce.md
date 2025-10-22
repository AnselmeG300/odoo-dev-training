https://www.odoo.com/documentation/19.0/fr/developer/tutorials/server_framework_101/08_compute_onchange.html.

---

# ✅ Checklists – A Brief History of QWeb

---

À la fin de ce chapitre, tu sauras :

* Ce qu’est **QWeb**, le moteur de templates d’Odoo ;
* Comment il est utilisé dans les **Kanban Views** (et dans les rapports PDF ou site web) ;
* Comment **créer ta propre vue Kanban** pour afficher les propriétés avec un design personnalisé ;
* Comment **utiliser les directives QWeb** (`t-if`, `t-foreach`, etc.) pour ajouter de la logique conditionnelle ;
* Et comment **grouper dynamiquement les cartes Kanban** (ici, par *Property Type*).

---

# 🧠 **1️⃣ Comprendre QWeb**

## 🔹 Qu’est-ce que QWeb ?

**QWeb** est le moteur de templating d’Odoo — c’est un langage XML utilisé pour **générer du HTML** dynamiquement.

C’est un peu comme **Jinja2** (Python), **Twig** (PHP) ou **ERB** (Ruby),
mais intégré directement dans Odoo, avec une syntaxe adaptée à son environnement.

---

### 🧩 QWeb dans Odoo est utilisé pour :

| Usage               | Exemple concret                                             |
| ------------------- | ----------------------------------------------------------- |
| 🖼️ Vues dynamiques | Les vues **Kanban** (comme dans CRM, projets, ventes, etc.) |
| 🧾 Rapports PDF     | Factures, bons de commande, etc.                            |
| 🌐 Pages web        | Modules *Website* et *Portal*                               |
| 🧱 Snippets visuels | Cartes, blocs HTML enrichis                                 |

---

## 🔹 Structure d’un template QWeb

```xml
<templates>
    <t t-name="kanban-box">
        <div>
            <field name="name"/>
        </div>
    </t>
</templates>
```

💡 **Explication :**

* `<templates>` : contient un ou plusieurs templates QWeb.
* `<t>` : balise spéciale “template” de QWeb.
* `t-name="kanban-box"` : nom du template racine pour le Kanban.
* `<field name="name"/>` : champ du modèle affiché.

---

## 🔹 Les objets disponibles dans un template Kanban

| Objet                        | Description                                          |
| ---------------------------- | ---------------------------------------------------- |
| `record`                     | Le record courant (ex: une propriété)                |
| `record.fieldname.value`     | Valeur du champ affichée selon le format utilisateur |
| `record.fieldname.raw_value` | Valeur brute en base de données                      |
| `t-if`, `t-foreach`          | Directives QWeb pour conditions et boucles           |

---

# 🧩 **2️⃣ Le Kanban View dans Odoo**

Les **vues Kanban** permettent de représenter des enregistrements sous forme de **cartes visuelles**.
Elles sont très utilisées dans les modules CRM, Project, Helpdesk, etc.

Exemple simple :

```xml
<kanban>
    <templates>
        <t t-name="kanban-box">
            <div>
                <field name="name"/>
            </div>
        </t>
    </templates>
</kanban>
```

---

# ⚙️ **3️⃣ Implémentation — Kanban View pour Real Estate**

Nous allons ajouter une **vue Kanban** pour les propriétés (`estate.property`).

---

## 🗂️ Fichier : `views/estate_property_views.xml`

### 🔸 Étape 1 — Vue minimale

```xml
<odoo>
    <record id="view_property_kanban" model="ir.ui.view">
        <field name="name">estate.property.kanban</field>
        <field name="model">estate.property</field>
        <field name="arch" type="xml">
            <kanban>
                <templates>
                    <t t-name="kanban-box">
                        <div class="oe_kanban_card">
                            <field name="name"/>
                        </div>
                    </t>
                </templates>
            </kanban>
        </field>
    </record>

    <!-- Action update -->
    <record id="action_estate_property" model="ir.actions.act_window">
        <field name="view_mode">kanban,list,form</field>
    </record>
</odoo>
```

💡 Cela crée une vue Kanban de base avec uniquement le nom de la propriété.

---

## 🧩 Étape 2 — Ajouter des champs et conditions (QWeb directives)

On va enrichir le Kanban :

* `expected_price`, `best_offer`, `selling_price`, `tag_ids`
* Afficher certaines infos **selon l’état** du bien :

  * `best_offer` → seulement si état = `offer_received`
  * `selling_price` → seulement si état = `offer_accepted`

```xml
<kanban default_group_by="property_type_id" group_create="false" class="o_kanban_example">
    <field name="state"/>
    <field name="expected_price"/>
    <field name="best_offer"/>
    <field name="selling_price"/>
    <field name="tag_ids"/>
    <templates>
        <t t-name="kanban-box">
            <div class="oe_kanban_card o_kanban_record">
                <div class="o_kanban_primary_left">
                    <strong><field name="name"/></strong>
                </div>

                <div>
                    <span>Expected Price: </span>
                    <field name="expected_price"/>
                </div>

                <div t-if="record.state.raw_value == 'offer_received'">
                    <span>Best Offer: </span>
                    <field name="best_offer"/>
                </div>

                <div t-if="record.state.raw_value == 'offer_accepted'">
                    <span>Selling Price: </span>
                    <field name="selling_price"/>
                </div>

                <div>
                    <field name="tag_ids" widget="many2many_tags"/>
                </div>
            </div>
        </t>
    </templates>
</kanban>
```

---

## 🧩 Étape 3 — Ajouter un **groupement automatique** (par type)

Grâce à l’attribut `default_group_by`, on regroupe les propriétés par **Property Type** :

```xml
<kanban default_group_by="property_type_id" group_create="false">
```

* `default_group_by` → regroupe automatiquement par le champ donné.
* `group_create="false"` → empêche le *drag & drop* pour éviter de changer le type d’un bien.

---

# 🎨 **4️⃣ Résultat attendu**

Tu obtiens un **Kanban propre et interactif** comme celui-ci 👇

📸 *(correspond à la capture que tu as envoyée)*

| Group         | Properties displayed               |
| ------------- | ---------------------------------- |
| **House**     | House in Brussels / House in Arlon |
| **Apartment** | Apartment in Namur                 |
| **Castle**    | Castle in Bouillon                 |

Chaque carte montre :

* Le **nom** de la propriété,
* Le **prix attendu**,
* Le **meilleur prix** (si offre reçue),
* Le **prix de vente** (si offre acceptée),
* Et les **tags colorés** (`cozy`, `exceptional`, etc.)

---

# 🧩 **5️⃣ En résumé**

| Élément                    | Description                                                      |
| -------------------------- | ---------------------------------------------------------------- |
| **QWeb**                   | Moteur de templates XML d’Odoo (génère HTML, PDF, etc.)          |
| **Kanban**                 | Vue flexible utilisant QWeb pour représenter les enregistrements |
| **t-if**                   | Directive conditionnelle QWeb                                    |
| **record.field.raw_value** | Accès à la valeur brute d’un champ                               |
| **default_group_by**       | Regroupe automatiquement les cartes par champ                    |
| **group_create="false"**   | Désactive le drag & drop de groupes                              |

---

# 🧠 Pour aller plus loin

Tu peux ensuite :

* Ajouter des **icônes** selon l’état (`fa-check`, `fa-clock`, etc.),
* Colorer les cartes avec du CSS conditionnel (`t-attf-class`),
* Intégrer des **images** (ex: photos de biens),
* Ou même utiliser les **actions rapides** (petits boutons à droite).

