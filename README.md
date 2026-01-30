
#  📘 Transformation & Tests des Données — MongoDB 

🎯 Objectif
----------------------
Mettre en place un pipeline de données complet permettant :

  * d’ingérer des données météorologiques provenant de fichiers Excel et JSON via Airbyte ;
  * de centraliser les données brutes dans un bucket Amazon S3 ;
  * de transformer les données dans un format unifié et compatible MongoDB ;
  * d’automatiser des tests d’intégrité (doublons, valeurs manquantes, cohérence des types) ;
  * d’enrichir les données avec des métadonnées liées aux stations météo ;
  * de migrer les données finales vers une base MongoDB.

☁️ Ingestion des Données avec Airbyte → Amazon S3

*------------------------------------*
Mettre en place une plateforme d’ingestion automatisée permettant de récupérer des données météo au format Excel et JSON, puis de les charger dans un bucket Amazon S3 afin de les préparer aux étapes de transformation et de migration

      ⚙️ (1) Installation & Configuration Airbyte
       Airbyte a été installé afin de gérer la collecte et la synchronisation des données météo.
       Configuration réalisée :
              - Installation d’Airbyte
              - Configuration des connecteurs sources :
                          📄 Fichiers Excel
                          🧾 Fichiers JSON
             
       Configuration du connecteur destination :
             ☁️ Amazon S3

------
      🔗 (2) Connexion aux Sources
       Trois fichiers sources météo ont été connectés :
           - ichetegem.json
           - madeleine.json
           - infoclimat_BHA.json
       Pour chaque source :
           - Vérification du format
           - Paramétrage du schéma
           - Planification des synchronisations

-------
       📦 (3) Chargement vers S3
        Les données sont automatiquement transférées vers le bucket S3 :
        📌 Bucket cible : meteo_data
      Chaque fichier est envoyé dans le bucket sous forme de données brutes, prêtes à être exploitées dans l’étape suivante de transformation.
-------
       🧪 (4) Bénéfices de l'ingestion
         * Centralisation des données
         * Pipeline reproductible et industrialisable
         * Préparation optimale pour les transformations MongoDB

----------

** 🧠 Logique de Transformation des données **

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

## 🔄 Pipeline de traitement des données

- Collecte : 
Récupération des fichiers JSON provenant de La Madeleine, Ichtegem et InfoClimat.
- Transformation : 
Normalisation du schéma, nettoyage des champs et ajout du champ source.
- Migration vers MongoDB  :
Insertion automatisée de toutes les données dans une collection unique : stations_meteo.
- Contrôle qualité  :
Vérification de la structure, détection des erreurs (coordonnées, noms manquants) et comptage final des documents.

---

## 🐍 Script de migration (migration_mongo.py)

- se connecte à MongoDB
- réinitialise la collection stations_meteo
- charge et insère les données normalisées
- ajoute automatiquement le champ source
- affiche un rapport qualité (totaux, erreurs détectées)

### Execution

---

## Mesure qualité
Le script calcule :
- Documents importés
- Taux de champs manquants
- Doublons
- Types incorrects
- Score global qualité

---

## Sécurité & Bonnes pratiques
- Suppression contrôlée avant insertion
- Structures validées
- Collections séparées par source
- Préparation à la réplication MongoDB

---
# 🐳 Conteneurisation de l’application avec Docker

## 🎯 Objectif

Conteneuriser l’ensemble du pipeline de migration afin de garantir :
  - la portabilité de l’application,
  - la reproductibilité des traitements,
  - l’isolement entre les services (MongoDB / scripts Python).
-------
## 🧱 Architecture Docker

L’architecture Docker repose sur :
   * un conteneur MongoDB
   * un conteneur Python chargé de la migration et des tests
   * un volume Docker pour la persistance des données MongoDB
-----

## 📦 docker-compose.yml

Le fichier docker-compose.yml permet de déployer l’ensemble de l’environnement en une seule commande.

Fonctionnalités :
- Importation des images Docker officielles (mongo:6, python)
- Exécution automatique du script de migration
- Utilisation d’un volume Docker pour la persistance des données

Exemple de services :
             mongodb
             Image : mongo:6
             Port exposé : 27017
             Volume : données persistantes
             migration_service
             Image Python personnalisée

* Exécution du script migration_mongo.py
* Connexion automatique à MongoDB

💾 Volumes Docker:

Un volume Docker est utilisé afin de garantir la persistance des données MongoDB, même après l’arrêt ou la suppression des conteneurs.

Avantages :Conservation des données,Séparation données / application, Facilité de sauvegarde

▶️ Exécution
            docker-compose up --build

Vérifications possibles :

            docker ps
            docker logs migration_service
            docker exec -it mongodb mongosh


# ☁️ Déploiement sur AWS
## 🎯 Objectif

Déployer MongoDB dans un environnement cloud scalable afin de :

- rendre la base accessible à distance,
- mesurer les performances d’accès aux données,
- mettre en place une stratégie de sauvegarde et de surveillance.

## 🚀 Déploiement MongoDB sur Amazon ECS

Le déploiement repose sur :

* Amazon ECS (Elastic Container Service)
* un cluster ECS basé sur EC2
* une tâche ECS exécutant un conteneur MongoDB Docker

## Étapes principales :

1- Création d’un cluster ECS
2- Définition d’une task definition MongoDB
3- Lancement d’une instance EC2 ECS-Optimized
4- Déploiement du service ECS
5- Ouverture du port MongoDB (27018) via les Security Groups

## 🔌 Connexion MongoDB

Connexion validée depuis un poste local via mongosh :

mongosh mongodb://13.237.248.223:27018


 La connexion distante confirme le bon fonctionnement du déploiement ECS.

##  ⏱️ Reporting – Temps d’accessibilité aux données

Un script Python (test_performance_mongo.py) permet de mesurer le temps d’exécution d’une requête MongoDB.
Exemple de requête :
 - Récupération des données météo
 - Filtrage par ville et date

Résultat observé :
Documents récupérés : 288
Temps d'exécution : 70.73 ms

👉 Ce résultat démontre une excellente réactivité de la base MongoDB déployée sur AWS.

## 💾 Sauvegardes MongoDB (Backup)

Les sauvegardes sont réalisées via l’outil mongodump.

Commande utilisée :
                 mongodump --host 13.37.248.173 --port 27018 --db meteo


Les fichiers de sauvegarde sont ensuite :
   1- stockés localement
   2- transférés vers Amazon S3 pour un stockage durable

👉 Amazon S3 garantit :haute durabilité,sauvegarde externalisée,restauration possible à tout moment

##  📊 Surveillance avec Amazon CloudWatch

La surveillance repose sur Amazon CloudWatch

## Requirements
Voir `requirements.txt`

---

