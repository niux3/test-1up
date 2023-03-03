# Test Technique 1up

## Contexte

On souhaite créer une API qui permet de donner la liste des villes les plus intéressantes pour l’utilisateur en fonction du prix au m² (pour de la location d’appartement) ainsi que de la note de la ville.

## Ressources

Ressources externes à utiliser :

- https://www.bien-dans-ma-ville.fr/ : permet de récupérer la note globale d’une ville.
- https://www.data.gouv.fr/fr/datasets/carte-des-loyers-indicateurs-de-loyers-dannonce-par-commune-en-2018/ : permet de récupérer le loyer moyen d’une ville par code INSEE
- https://api.gouv.fr/documentation/api-geo : permet de récupérer les informations d’une ville en renseignant le code INSEE de la ville

## L’API à développer

L’API contient une seule requête avec :
Les paramètres d’entrée de la requête sont : 

- Un département
- Une surface souhaitée pour le logement
- Un loyer maximum

Les données en sortie seront une liste de villes avec :

- Le loyer moyen du bien pour la surface donnée
- La note de la ville
- Le nom de la ville
- Son code postal
- La population de la ville

La manière de stocker les informations récupérées est à déterminer par le candidat.

## Contraintes

Contraintes techniques :

- Docker
- FastAPI

## Exemple

Pour le département 64, avec un loyer maximum de 800€ pour une surface de 50m², je m’attends à trouver les villes suivantes :

- Anglet (note 3.8 et loyer moyen à 12.89)
- Pau (note 3.6 et loyer moyen à 10.22)
- Bayonne (note 3.5 et loyer moyen à 12.18)
- Biarritz (note 3.5 et loyer moyen à 13.88)
- Saint-Jean-de-Luz (note 3.5 et loyer moyen à 12.78)
-  ...
