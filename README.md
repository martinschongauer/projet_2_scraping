## Scraping du site Books Online
Version Beta d'un projet de surveillance du marché des livres pour Books Online

***

### Installation et lancement
Se placer dans un dossier de travail vide et récupérer le code:
```
$ git clone https://github.com/martinschongauer/projet_2_scraping
```

Créer et activer un environnement Python pour ce projet:
```
$ python3 -m venv env
$ source env/bin/activate
```

Installer les dépendances listées dans le fichier requirements.txt:
```
$ pip install -r requirements.txt
```

Lancer le programme:
```
$ python3 main.py
```

### Usage général
Le main contient des appels à cinq "tests" dont la complexité est croissante, allant de la récupération des informations pour un livre particulier à la récupération de toutes les informations du site.<br/><br/>
Il faut avant tout décommenter, dans la fonction main, l'appel vers le "test" qui nous intéresse. Par défaut on lance le test 5, c'est-à-dire la récupération de toutes les catégories de livres et de leur contenu.<br/><br/>
Les sorties se présentent sous forme de dossiers créés au même emplacement que les scripts, contenant à chaque fois des fichiers CSV pour les informations (un par catégorie de livre) et un sous-dossier avec les images.<br/>
