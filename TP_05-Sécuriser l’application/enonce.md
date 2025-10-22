https://www.odoo.com/documentation/19.0/developer/tutorials/restrict_data_access.html

---

# ✅ Checklists – Sécuriser l’application

### 🎯 Objectif général

Maintenant que nous avons un modèle `estate.property` et une table en base, il faut définir **qui a le droit d’accéder aux données** (et comment).
Dans ce chapitre, on apprend à :

* Charger des données initiales avec des fichiers **CSV**,
* Créer des **règles d’accès (Access Rights)** pour contrôler lecture/écriture,
* Faire disparaître les warnings d’Odoo concernant l’absence de règles de sécurité.

---

## 🔹 1. Les fichiers de données (CSV)

Odoo est **data-driven** : beaucoup de comportements reposent sur des **fichiers de données** chargés lors de l’installation ou de la mise à jour d’un module.

### Exemple : les états/provinces

Dans `res.country.state`, les états d’un pays sont chargés depuis un fichier CSV :

```csv
"id","country_id:id","name","code"
state_au_1,au,"Australian Capital Territory","ACT"
state_au_2,au,"New South Wales","NSW"
```

* **id** : identifiant externe (sert à faire référence au record sans connaître son ID en base).
* **country\_id\:id** : référence vers un autre record (ici un pays) via son identifiant externe.
* **name** : nom de l’état.
* **code** : abréviation.

👉 Convention :

* **dossier `data/`** → données générales (ex. pays, devises).
* **dossier `security/`** → règles de sécurité.
* **dossier `views/`** → définitions d’interfaces.

⚠️ Les fichiers listés dans `__manifest__.py` sont **chargés dans l’ordre** → si A dépend de B, B doit être chargé avant.

---

## 🔹 2. Pourquoi est-ce important pour la sécurité ?

Parce que **toutes les règles de sécurité** (qui peut lire, créer, modifier, supprimer) sont elles aussi chargées via des fichiers CSV.
Sans règles définies : Odoo considère que **personne n’a accès** aux données → d’où les **warnings** dans les logs.

---

## 🔹 3. Les droits d’accès (Access Rights)

Les droits d’accès sont définis dans le modèle `ir.model.access`.
Chaque règle associe :

* **Un modèle** (par ex. `estate.property`),
* **Un groupe d’utilisateurs** (ex. `base.group_user`),
* **Des permissions** (lecture, écriture, création, suppression).

### Exemple

```csv
id,name,model_id/id,group_id/id,perm_read,perm_write,perm_create,perm_unlink
access_test_model,access_test_model,model_test_model,base.group_user,1,0,0,0
```

* **id** : identifiant externe.
* **name** : nom de la règle.
* **model\_id/id** : modèle concerné (`model_nom_du_modele`).
* **group\_id/id** : groupe Odoo qui a ce droit (ex. `base.group_user` = tous les utilisateurs internes).
* **perm\_read, perm\_write, perm\_create, perm\_unlink** : permissions (1 = autorisé, 0 = interdit).

---

## 🔹 4. Étapes pratiques – Sécuriser `estate.property`

### Étape 1 : Créer le fichier d’accès

Dans ton module `estate`, crée le fichier suivant :

```
estate/security/ir.model.access.csv
```

Contenu minimal :

```csv
id,name,model_id:id,group_id:id,perm_read,perm_write,perm_create,perm_unlink
access_estate_property,access_estate_property,model_estate_property,base.group_user,1,1,1,1
```

💡 Ici, on donne **tous les droits** (lecture, écriture, création, suppression) aux utilisateurs internes (`base.group_user`).

---

### Étape 2 : Déclarer le fichier dans le manifest

Dans `estate/__manifest__.py`, ajoute :

```python
'data': [
    'security/ir.model.access.csv',
],
```

👉 Ainsi, Odoo sait qu’il doit charger ce fichier quand le module est installé/mis à jour.

---

### Étape 3 : Redémarrer et mettre à jour le module

```bash
./odoo-bin --addons-path=addons,../tutorials/ -d rd-demo -u estate
```

👉 Résultat attendu :

* Le warning *“no access rules”* disparaît.
* Les utilisateurs internes peuvent gérer des enregistrements `estate.property`.

---

## 🔹 5. Compréhension finale

* Chaque **colonne du CSV** joue un rôle précis (id = identifiant externe, model\_id = modèle ciblé, group\_id = groupe utilisateur, permissions = droits).
* Sans ce fichier, le modèle est **inaccessible** → même les admins ne peuvent pas manipuler les données.
* Le **jeu de données de sécurité** s’initialise **à l’installation/mise à jour** du module via le manifest.

---

## ✅ Résultat final attendu

* Le modèle `estate.property` est désormais **sécurisé**.
* Les utilisateurs internes (`base.group_user`) peuvent créer, lire, modifier et supprimer des biens immobiliers.
* Odoo ne génère plus de warnings dans les logs concernant l’absence de règles de sécurité.





Prenons l’exemple classique pour notre module `estate` :

```csv
id,name,model_id:id,group_id:id,perm_read,perm_write,perm_create,perm_unlink
access_estate_property,access_estate_property,model_estate_property,base.group_user,1,1,1,1
```

---

## 🔎 Matching colonne par colonne

1. **id**

   * **Valeur** : `access_estate_property`
   * **Signification** : identifiant externe unique de la règle d’accès (utilisé pour la référencer ailleurs).

2. **name**

   * **Valeur** : `access_estate_property`
   * **Signification** : nom lisible de la règle (souvent le même que `id` par convention).

3. **model\_id\:id**

   * **Valeur** : `model_estate_property`
   * **Signification** : référence au modèle Odoo concerné.
     👉 Ici, c’est notre modèle `estate.property`.
     ⚠️ Règle de syntaxe : le `_name` du modèle avec les points remplacés par des underscores → `estate.property` devient `model_estate_property`.

4. **group\_id\:id**

   * **Valeur** : `base.group_user`
   * **Signification** : indique le groupe d’utilisateurs qui a ces droits.
     👉 Ici, `base.group_user` = **tous les utilisateurs internes** d’Odoo.

5. **perm\_read**

   * **Valeur** : `1`
   * **Signification** : lecture autorisée ✅.

6. **perm\_write**

   * **Valeur** : `1`
   * **Signification** : modification autorisée ✅.

7. **perm\_create**

   * **Valeur** : `1`
   * **Signification** : création autorisée ✅.

8. **perm\_unlink**

   * **Valeur** : `1`
   * **Signification** : suppression (unlink = delete) autorisée ✅.

---

## 📝 Résumé du matching pour cet exemple

* `id` → **access\_estate\_property** = identifiant technique de la règle.
* `name` → **access\_estate\_property** = nom de la règle.
* `model_id:id` → **model\_estate\_property** = modèle cible (`estate.property`).
* `group_id:id` → **base.group\_user** = groupe cible (utilisateurs internes).
* `perm_read` → 1 (lecture autorisée).
* `perm_write` → 1 (écriture autorisée).
* `perm_create` → 1 (création autorisée).
* `perm_unlink` → 1 (suppression autorisée).

👉 Résultat : **tous les utilisateurs internes** (`base.group_user`) ont **tous les droits** sur les biens immobiliers (`estate.property`).

---


