CREATE OR REPLACE TABLE groupes (
    id int(11) AUTO_INCREMENT PRIMARY KEY,
    nom_groupe VARCHAR(25) UNIQUE NOT NULL   
) ;

CREATE OR REPLACE TABLE utilisateurs (
    id int(11) AUTO_INCREMENT PRIMARY KEY,
    nom VARCHAR(255)  NOT NULL  
) ;

CREATE OR REPLACE TABLE concerts (
    id int(11) AUTO_INCREMENT PRIMARY KEY,
    groupe_id int(11),
    date_concert VARCHAR(10) NOT NULL,
    places_max int(11),
    FOREIGN KEY (groupe_id) REFERENCES groupes (id)
) ;

CREATE OR REPLACE TABLE reservations (
    id int(11) AUTO_INCREMENT PRIMARY KEY,
    concert_id int(11),
    utilisateur_id int(11),
    FOREIGN KEY (concert_id) REFERENCES concerts (id),
    FOREIGN KEY (utilisateur_id) REFERENCES utilisateurs (id) 
) ;

INSERT INTO groupes(id, nom_groupe) VALUES (1, "THE ZOZOS");
INSERT INTO groupes(id, nom_groupe) VALUES (2, "THE BAMBOULIDA");
INSERT INTO groupes(id, nom_groupe) VALUES (3, "THE ROCKEURS");

INSERT INTO utilisateurs(id, nom) VALUES (1, "BENJAMIN");
INSERT INTO utilisateurs(id, nom) VALUES (2, "ROMAIN");
INSERT INTO utilisateurs(id, nom) VALUES (3, "CHRISTOPHER");
INSERT INTO utilisateurs(id, nom) VALUES (4, "LOUNA");

INSERT INTO concerts(id, groupe_id, date_concert, places_max) VALUES (1, 2, "15/12/2022", 200);
INSERT INTO concerts(id, groupe_id, date_concert, places_max) VALUES (2, 1, "16/12/2022", 190);
INSERT INTO concerts(id, groupe_id, date_concert, places_max) VALUES (3, 3, "17/12/2022", 300);
INSERT INTO concerts(id, groupe_id, date_concert, places_max) VALUES (4, 3, "18/12/2022", 250);
INSERT INTO concerts(id, groupe_id, date_concert, places_max) VALUES (5, 2, "19/12/2022", 200);

INSERT INTO reservations(id, concert_id, utilisateur_id) VALUES (1, 3, 4);
INSERT INTO reservations(id, concert_id, utilisateur_id) VALUES (2, 4, 2);
INSERT INTO reservations(id, concert_id, utilisateur_id) VALUES (3, 1, 2);
INSERT INTO reservations(id, concert_id, utilisateur_id) VALUES (4, 1, 1);
INSERT INTO reservations(id, concert_id, utilisateur_id) VALUES (5, 1, 2);
INSERT INTO reservations(id, concert_id, utilisateur_id) VALUES (6, 5, 1);
INSERT INTO reservations(id, concert_id, utilisateur_id) VALUES (7, 5, 4);
INSERT INTO reservations(id, concert_id, utilisateur_id) VALUES (8, 2, 4);