# Carrefour Product Scraper

## Description

Ce projet permet de récupérer automatiquement des informations sur des produits disponibles sur le site **Carrefour.fr** à l'aide de **Playwright et Python**.

Le script effectue une recherche sur un produit (ex: *yaourt fraise*) et extrait les informations suivantes pour chaque produit trouvé :

* lieu (magasin ciblé)
* nom du produit
* prix
* prix au kg
* note moyenne
* nombre d'avis

Les données sont ensuite sauvegardées dans un fichier **YAML**.

---

## Objectif du projet

Ce projet a été développé pour apprendre :

* le **web scraping avec Python**
* l'utilisation de **Playwright**
* l'extraction et la structuration de données
* la génération de fichiers **YAML**

Ce type d'outil peut être utilisé pour :

* analyser les prix
* comparer des produits
* construire des datasets pour de l'analyse ou du machine learning

---

## Structure du projet

```
web-Scrapping
│
├── code
│   └── main.py
│
├── data
│   └── resume.yaml
│
└── README.md
```

* **main.py** : script principal de scraping
* **resume.yaml** : fichier contenant les résultats
* **README.md** : documentation du projet

---

## Installation

### 1. Cloner le projet

```
git clone <url-du-repository>
cd web-Scrapping
```

### 2. Créer un environnement virtuel

Windows :

```
python -m venv .venv
.venv\Scripts\activate
```

Linux / Mac :

```
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Installer les dépendances

```
pip install playwright pyyaml
```

### 4. Installer les navigateurs Playwright

```
playwright install
```

---

## Utilisation

Lancer le script :

```
python code/main.py
```

Le script :

1. ouvre le site Carrefour
2. recherche un produit
3. récupère les informations des produits
4. enregistre les résultats dans :

```
data/resume.yaml
```

---

## Exemple de sortie

```
produits:

- lieu: Carrefour Express Brest Victor Eusen
  nom: Yaourts fraise bifidus ACTIVIA
  prix: 1.85 €
  prix_kg: 3.70 € / KG
  note: 4.6
  avis: 774

- lieu: Carrefour Express Brest Victor Eusen
  nom: Yaourts fraise Bio CARREFOUR BIO
  prix: 1.59 €
  prix_kg: 3.18 € / KG
  note: 4.4
  avis: 5
```

---

## Technologies utilisées

* **Python**
* **Playwright**
* **YAML**
* **Regex**

---

## Améliorations possibles

Améliorations envisageables :

* parcourir toutes les pages de résultats
* récupérer la **marque**
* récupérer le **nutriscore**
* récupérer le **EAN**
* exporter les données en **CSV / Pandas**
* scraper plusieurs magasins

---

## Avertissement

Ce projet est destiné à un usage **éducatif**.
Le scraping de sites web doit respecter les **conditions d'utilisation** des services concernés.

---

## Auteur

Projet réalisé par **Pierre Dauguet**.
