# OpenClassRooms - Python - Projet 12 : Epic Events

Ce projet consiste à créer une application CRM privée pour une entreprise :  
<!-- 2 espaces à la fin de la ligne pour un saut de ligne -->
	- élaboration d'un modèle relationnelle,
	- utilisation des framework Django et Django REST,
	- utilisation de la base de données PostgreSQL,
    - utilisation du site d'administration Django en tant qu'interface front-end,
    - mise en place de groupes d'utilisateurs avec des permissions différentes,  
    - mise en place d'endpoints d'API permettant la recherche et le filtre de données.


## Application du script

A partir du terminal, se placer dans le répertoire souhaité

### 1. Récupérer le repository GitHub et créer un environnement virtuel

Cloner le repository GitHub :
```bash
git clone https://github.com/Jennifer789C/Projet_12.git
```
Puis se placer dans le répertoire du projet :
```bash
cd Projet_12
```
*Pour ma part, je travaille sous Windows et avec l'IDE PyCharm, la création d'un environnement virtuel se fait via les paramètres de l'IDE*

Depuis un terminal sous Windows :
```bash
python -m venv env
env/Scripts/activate
```

Depuis un terminal sous Linux ou Mac :
```bash
python3 -m venv env
source env/bin/activate
```

### 2. Installer les packages du fichier requirements.txt

Dans l'environnement virtuel, télécharger l'ensemble des packages indiqués 
dans le fichier requirements.txt :
```bash
pip install -r requirements.txt
```

### 3. Configurer la base de données PostgreSQL

Installer PostgreSQL : https://www.postgresql.org/download/  
Créer la base de données :
```bash
createdb EpicEvents_bdd
```
Mettre à jour les informations de votre utilisateur dans le fichier 
settings.py :
```bash
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'EpicEvents_bdd',
        'USER': 'votre_utilisateur_postgresql',
        'PASSWORD': 'votre_mot_de_pass_postgresql',
    }
}
```
Attention!! Si vous souhaitez lancer les tests avec pytest, votre 
utilisateur doit avoir les autorisations de se connecter et créer des bases 
de données.

### 4. Lancer le serveur

```bash
cd EpicEvents
```
Lancer le script python :
```bash
python manage.py runserver
```
Les utilisateurs administrateurs ont accès à : http://localhost:8000/admin  
Les autres utilisateurs ont accès aux données via l'API.
 
La documentation de cette API se trouve à l'adresse suivante :  
https://documenter.getpostman.com/view/23176759/2s93CUKAzi
