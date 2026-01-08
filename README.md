
#  📘 Transformation & Tests des Données — MongoDB 

🎯 Objectif du Projet
----------------------
Ce projet permet de :

- Charger les données météo provenant de trois sources :
  - la_madeleine.json
  - ichtegem.json
  - InfoClimat.json

- Vérifier l’intégrité des données avant migration
- Transformer les données au format compatible MongoDB
- Vérifier l’intégrité après transformation
- Exporter les données nettoyées dans :
                * la_madeleine_mongo.json
                * ichtegem_mongo.json
                * infoclimat_mongo.json

☁️ Ingestion des Données avec Airbyte → S3
*------------------------------------*
Mettre en place une plateforme d’ingestion automatisée permettant de récupérer les données météo au format Excel et JSON, puis de les charger dans un bucket S3 afin de les centraliser pour les étapes de transformation et migration.

      ⚙️ 1️⃣ Installation & Configuration Airbyte
       Airbyte a été installé afin de gérer la collecte et la synchronisation des données météo.
       Configuration réalisée :
              - Installation d’Airbyte
              - Configuration des connecteurs sources :
                          📄 Fichiers Excel
                          🧾 Fichiers JSON
             
       Configuration du connecteur destination :
             ☁️ Amazon S3

------
      🔗 2️⃣ Connexion aux Sources
       Trois fichiers sources météo ont été connectés :
           - ichetegem.json
           - madeleine.json
           - infoclimat_BHA.json
       Pour chaque source :
           - Vérification du format
           - Paramétrage du schéma
           - Planification des synchronisations

-------
       📦 3️⃣ Chargement vers S3
        Les données sont automatiquement transférées vers le bucket S3 :
        📌 Bucket cible : meteo_data
      Chaque fichier est envoyé dans le bucket sous forme de données brutes, prêtes à être exploitées dans l’étape suivante de transformation.
-------
       🧪 4️⃣ Bénéfices
         * Centralisation des données
         * Pipeline reproductible et industrialisable
         * Préparation optimale pour les transformations MongoDB

----------

** 🧠 Logique de Transformation **

 1 — Chargement des données
   -  Chaque fichier JSON est ouvert puis validé :
   -  Vérification de l’existence du fichier
   -  Vérification que le contenu est lisible et valide en JSON

 2 — Tests d’intégrité avant migration

Pour chaque dataset, les contrôles suivants sont effectués :
   - Colonnes disponibles
   - Types détectés
   - Valeurs manquantes
   - Doublons

   Exemple de sortie :
                     Code
                     Colonnes : ['date', 'temperature', 'humidity', ...]
                     Types : float64 / object
                     Valeurs manquantes : 7
                     Doublons : 404

Ces tests garantissent la qualité des données sources avant transformation.


 3 — Transformation des Stations Personnelles

Les fichiers la_madeleine.json et ichtegem.json sont restructurés au format MongoDB :

                     json
                     {
                     "_id": "ILAMAD25",
                    "provider": "personal_station",
                    "measures": [
                     {
                     "timestamp": "...",
                     "temperature": 12.5,
                     "humidity": 85,
                     "pressure": 1012
                     }]}
  

Champs extraits :timestamp, temperature, humidity, pressure

Nettoyage effectué :

  - Normalisation de la structure
  - Conservation uniquement des champs utiles pour MongoDB

Exports générés :

  - la_madeleine_mongo.json
  - ichtegem_mongo.json


-------

 4 — Transformation InfoClimat

Les données InfoClimat sont converties vers une structure MongoDB enrichie :

                            json
                          {
                            "_id": "00052",
                            "provider": "infoclimat",
                            "name": "Armentières",
                            "lat": 50.689,
                            "lon": 2.877,
                            "measures": [...]}
                           
  
  Export généré :
infoclimat_mongo.json

-----

 5 — Tests d’intégrité après migration

Les mêmes contrôles qu’avant migration sont réappliqués :
  - Validation de la structure
  - Cohérence des types
  - Détection de doublons restants
  - Détection de valeurs manquantes

Ces tests garantissent que la transformation n’ ont pas introduit des erreurs et que la donnée est prête pour ingestion dans MongoDB.


# Pipeline de Migration vers MongoDB

## Objectif
Ce projet a pour objectif de collecter, transformer puis migrer des données météorologiques dans une base MongoDB, tout en garantissant la qualité des données.

---

## 1️⃣ Pipeline général
- Collecte des données :
  - Stations personnelles (La Madeleine & Ichtegem)
  - Données InfoClimat
- Transformation :
  - Normalisation du format JSON
  - Création d’un schéma compatible MongoDB
- Migration :
  - Création de collections MongoDB
  - Insertion automatisée
- Contrôle qualité :
  - Vérification structure
  - Taux d’erreurs
  - Détection doublons

---

## 2️⃣ Script de migration
Le script `migration_mongo.py` :
- se connecte à MongoDB
- supprime l’ancienne collection
- insère les nouveaux documents
- affiche un rapport qualité

### Execution

---

## 3️⃣ Mesure qualité
Le script calcule :
- Documents importés
- Taux de champs manquants
- Doublons
- Types incorrects
- Score global qualité

---

## 4️⃣ Sécurité & Bonnes pratiques
- Suppression contrôlée avant insertion
- Structures validées
- Collections séparées par source
- Préparation à la réplication MongoDB

---

## 5️⃣ Requirements
Voir `requirements.txt`

---

