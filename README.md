## Cloner le projet

```bash
git clone https://github.com/AyoubEchcharrat/Nexa-BigData.git
cd Nexa-BigData
```

---

## Lancer la stack Big Data

```bash
docker compose up -d --build
```

Vérifier que les services sont bien lancés :

```bash
docker compose ps
```

---

## Ingestion des données (API Vélib)

Le script `getapi.py` permet de :

- appeler l’API OpenData Paris
- récupérer un snapshot des stations Vélib
- sauvegarder un fichier JSON horodaté

Lancer l’ingestion :

```bash
python py/getapi.py
```

Fichier généré :

```text
datas/velib-YYYYMMDD_HHMMSS.json
```

---

## Stockage dans HDFS (RAW)

Créer le dossier HDFS :

```bash
hdfs dfs -mkdir -p /user/root/data/velib/raw
```

Copier le fichier brut dans HDFS :

```bash
hdfs dfs -put datas/velib-*.json /user/root/data/velib/raw/
```

Vérifier le contenu :

```bash
hdfs dfs -ls /user/root/data/velib/raw
```

---

## Traitement Spark (Nettoyage)

Le nettoyage est effectué avec Spark (spark-shell ou spark-submit).

Étapes :

- lecture du JSON multi-lignes
- explosion du tableau `records`
- sélection des champs utiles
- suppression des enregistrements invalides
- normalisation des types
- suppression des doublons
- filtrage métier

Sortie du traitement :

```text
/user/root/output/velib_clean/
```

---

## Récupération des résultats

Fusionner les fichiers Spark en un seul fichier local :

```bash
hdfs dfs -getmerge /user/root/output/velib_clean ./velib_clean.json
```

---

## Orchestration avec Airflow

Les DAGs sont définis dans le dossier `dags/`.

Pipeline type :

1. ingestion API
2. stockage HDFS (raw)
3. traitement Spark
4. sauvegarde HDFS (clean)

Accès à l’interface Airflow (par défaut) :

```text
http://localhost:8080
```

---

## Commandes utiles

HDFS :

```bash
hdfs dfs -ls /
hdfs dfs -du -h /user/root/data
hdfs dfs -rm -r /user/root/output/velib_clean
```

Spark :

```bash
spark-shell
```

---

## Remarques

- Projet volontairement pédagogique
- Exécution en ligne de commande pour comprendre les bases
- Objectif : compréhension des briques Big Data

---

## Auteur

Ayoub ECH-CHARRAT

Projet réalisé dans le cadre de l’apprentissage des technologies Big Data :
Hadoop, HDFS, Spark, Airflow
