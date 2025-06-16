# Gestion-Hotel
Projet de resvervation de chambre d'hotel 

Il s'agit d'un projet académique de gestion d'hotel proposé pour s'excercer à la manupulation des bases de données.
Dans notre contexte , nous nous sommes penchés sur PostgreSQL pour un meilleur gestion des requettes.

L'objectif est de controler le flux de service d'un client depuis son inscription jusqu'à son départ.
En passant par la restauration et le nettoyage des chambre . Nous avons pris en compte la dépendance de tout les département d'un hotel
(le parking , l'acceuil , la restauration , le service de chambre , les ressources humaines ) tout en prenant en compte les interactions 
entre ces différents département .

**Fonctionnamité disponible**

- clients : Créer un compte/se connecter , faire un reservation , choisir le type de restauration , annuler une reservation , Noter le service
- Service acceuil : Ajouter/annuler une reservation , changer le staut d'une chambre (en cas de defaillance ) , ajouter un objet perdus
- Restauration : Consulter les commandes des clients , changer le statut d'une commande , Ajouter un menu/ Boisson 
- Resources humaines: verifier la presences des employés , consulter les activités au sein de l'hôtel , Retirer les accès un employés , 
- service de netoyyages : consulter les chambre à maintenir , changer le statut des chambres .
- l'admin : SUPERUSER

  **TECHNOLOGIE**
  Pyton principale langage  : Pandas pour la manupulation des données
                              tkinter pour une interface
                              PIL pour la gestion des images
                              psycopg2 pour l'interaction avec postgreSQL
                              OS
                              datetime pour le controle des reservation
                              fpdf pour générer les reçus et les rapports
                              
