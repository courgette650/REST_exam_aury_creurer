from flask import Flask, jsonify, abort, request
import mariadb
import urllib.parse

app = Flask(__name__)

app.config['JSON_AS_ASCII'] = False  # pour utiliser l'UTF-8 plutot que l'unicode


def execute_query(query, data=()):
    config = {
        'host': 'mariadb',
        'port': 3306,
        'user': 'root',
        'password': 'root',
        'database': 'mydatabase'
    }
    """Execute une requete SQL avec les param associés"""
    # connection for MariaDB
    conn = mariadb.connect(**config)
    # create a connection cursor
    cur = conn.cursor()
    # execute a SQL statement
    cur.execute(query, data)

    if cur.description:
        # serialize results into JSON
        row_headers = [x[0] for x in cur.description]
        rv = cur.fetchall()
        list_result = []
        for result in rv:
            list_result.append(dict(zip(row_headers, result)))
        return list_result
    else:
        conn.commit()
        return cur.lastrowid


# we define the route /
@app.route('/')
def welcome():
    liens = [{}]
    liens[0]["_links"] = [{
        "href": "/groupes",
        "rel": "groupes"
    }, {
        "href": "/concerts",
        "rel": "concerts"
    }, {
        "href": "/utilisateurs",
        "rel": "utilisateurs"
    }, {
        "href": "/reservations",
        "rel": "reservations"
    }]
    return jsonify(liens), 200


""" ################# Groupes #################
    #############################################"""

@app.route('/groupes')
def get_groupes():
    """"Récupère les groupes"""
    groupes = execute_query("select * from groupes")
    if(len(groupes) < 1):
        return jsonify({}), 204
        
    # ajout de _links aux groupes
    for i in range(0, len(groupes)):
        groupes[i]["_links"] = [{
                "href": "/groupes/" + urllib.parse.quote(groupes[i]["nom_groupe"]),
                "rel": "self"
            },{
                "href": "/groupes/" + urllib.parse.quote(groupes[i]["nom_groupe"]) + "/concerts",
                "rel": "concerts",
            }]
    return jsonify(groupes), 200

@app.route('/groupes', methods=['POST', ])
def post_groupe():
    """"Crée un groupes"""
    nom_groupe = request.args.get('nom_groupe') or ""
    nom_groupe = urllib.parse.unquote(nom_groupe)
    
    groupe = execute_query("select * from groupes where nom_groupe = ?", (nom_groupe, ))
    
    if(len(nom_groupe) < 1 or len(groupe) > 0):
        abort(409)
        
    id = execute_query("insert into groupes(nom_groupe) values (?)", (nom_groupe,))
    
    return jsonify({"id" : id}), 201


@app.route('/groupes/<string:nom_groupe>', methods=['DELETE', ])
def delete_groupe(nom_groupe):
    """"Supprime un groupe"""
    nom_groupe = urllib.parse.unquote(nom_groupe)
    groupe = execute_query("select * from groupes where nom_groupe = ?", (nom_groupe, ))
    
    if(len(groupe) < 1):
        return jsonify({}), 204
        
    execute_query("delete from groupes where id = ?", (groupe[0]["id"],))
    
    return jsonify(groupe), 200

@app.route('/groupes/<string:nom_groupe>')
def get_groupe(nom_groupe):
    """"Récupère les infos d'un groupe"""
    nom_groupe = urllib.parse.unquote(nom_groupe)
    groupe = execute_query("select * from groupes where nom_groupe = ?", (nom_groupe, ))
    if(len(groupe) < 1):
        abort(404)
    # ajout de _links à la région
    groupe[0]["_links"] = [{
            "href": "/groupes/" + urllib.parse.quote(groupe[0]["nom_groupe"]),
            "rel": "self"
        },{
            "href": "/groupes/" + urllib.parse.quote(groupe[0]["nom_groupe"]) + "/concerts",
            "rel": "concerts",
        }]
    return jsonify(groupe), 200


@app.route('/groupes/<string:nom_groupe>/concerts')
def get_groupe_concerts(nom_groupe):
    """"Récupère les concerts d'un groupe"""
    nom_groupe = urllib.parse.unquote(nom_groupe)
    concerts = execute_query("select c.* from groupes g, concerts c where nom_groupe = ? and c.groupe_id = g.id", (nom_groupe, ))
    if(len(concerts) < 1):
        return jsonify({}), 204
    # ajout de _links aux concerts
    for i in range(0, len(concerts)):
        concerts[i]["_links"] = [{
                "href": "/concerts/" + str(concerts[i]["id"]),
                "rel": "self"
            }]
        
    return jsonify(concerts), 200

""" ################# Utilisateurs #################
    #############################################"""

@app.route('/utilisateurs')
def get_utilisateurs():
    """Récupère les utilisateurs"""
    utilisateurs = execute_query("select * from utilisateurs")
    if(len(utilisateurs) < 1):
        return jsonify({}), 204
    # ajout de _links aux utilisateurs
    for i in range(0, len(utilisateurs)):
        utilisateurs[i]["_links"] = [{
                "href": "/utilisateurs/" + str(utilisateurs[i]["id"]),
                "rel": "self"
            }, {
                "href": "/utilisateurs/" + str(utilisateurs[i]["id"]) + "/reservations",
                "rel": "reservations"
            }]
        
    return jsonify(utilisateurs), 200


@app.route('/utilisateurs/<string:utilsateur_id>')
def get_utilisateur(utilisateur_id):
    """Récupère un utilisateur"""
    utilisateur = execute_query("select * from utilisateurs where id = ?", (utilisateur_id, ))
    if(len(utilisateur) < 1):
        abort(404)
    # ajout de _links aux utilisateurs
    utilisateur[0]["_links"] = [{
            "href": "/utilisateurs/" + str(utilisateur[0]["id"]),
            "rel": "self"
        }, {
            "href": "/utilisateurs/" + str(utilisateur[0]["id"]) + "/reservations",
            "rel": "reservations"
        }]
        
    return jsonify(utilisateur), 200

@app.route('/utilisateurs/', methods=['POST'])
def post_utilisateur():
    """Crée un utilisateur"""
    nom_utilisateur = request.args.get('nom_utilisateur') or ""
    nom_utilisateur = urllib.parse.unquote(nom_utilisateur)
    
    utilisateur = execute_query("select * from utilisateurs where nom = ?", (nom_utilisateur, ))
    
    if(len(nom_utilisateur) < 1 or len(utilisateur) > 0):
        abort(409)
        
    id = execute_query("insert into utilisateurs(nom_utilisateur) values (?)", (nom_utilisateur, ))

    return jsonify({"id": id}), 200


@app.route('/utilisateurs/<string:utilisateur_id>', methods=['DELETE'])
def delete_utilisateur(utilisateur_id):
    """supprime un utilisateur"""
    utilisateur = execute_query("select * from utilisateurs where id = ?", (utilisateur_id, ))
    
    if(len(utilisateur) < 1):
        return jsonify({}), 204
        
    id = execute_query("delete from utilisateurs where id = ?", (utilisateur_id, ))

    return jsonify({"id": id}), 200


@app.route('/utilisateurs/<string:utilisateur_id>/reservations')
def get_utilisateur_reservations(utilisateur_id):
    """Récupère les réservations d'un utilisateur"""
    reservations = execute_query("select r.id, g.nom_groupe, c.date_concert, c.places_max from utilisateurs u, reservations r, concerts c, groupes g where u.id = ? and r.utilisateur_id = u.id and c.id = r.concert_id and g.id = c.groupe_id", (utilisateur_id, ))
    
    if(len(reservations) < 1):
        return jsonify({}), 204
        
    # ajout de _links aux reservations
    for i in range(0, len(reservations)):
        reservations[i]["_links"] = [{
                "href": "/reservation/" + urllib.parse.quote(reservations[i]["id"]),
                "rel": "self"
            }]
        
    return jsonify(reservations), 200


""" ################# Concerts #################
    #############################################"""
    
    
@app.route('/concerts')
def get_concerts():
    """Récupère les concerts"""
    concerts = execute_query("select g.nom_groupe, c.* from concerts c, groupes g where c.groupe_id = g.id")
    
    if(len(concerts) < 1):
        return jsonify({}), 204
        
    # ajout de _links aux concerts
    for i in range(0, len(concerts)):
        concerts[i]["_links"] = [{
                "href": "/concerts/" + urllib.parse.quote(concerts[i]["id"]),
                "rel": "self"
            }]

    return jsonify(concerts), 200

    
@app.route('/concerts', methods=['POST',])
def post_concert():
    """crée un concert"""
    groupe_id = request.args.get('groupe_id') or ""
    date_concert = request.args.get('date_concert') or ""
    places_max = request.args.get('places_max') or ""
    
    groupe_id = urllib.parse.unquote(groupe_id)
    date_concert = urllib.parse.unquote(date_concert)
    places_max = urllib.parse.unquote(places_max)
    
    
    concert = execute_query("select * from concerts")
    
    if(len(groupe_id) < 1 or len(date_concert) < 1 or len(places_max) < 1 or len(concert) > 0):
        abort(409)
    
    id = execute_query("insert into concerts(groupe_id, date_concert, places_max) values (?, ?, ?)", (groupe_id, date_concert, places_max))
    # ajout de _links aux concerts
    concert[0]["_links"] = [{
            "href": "/concerts/" + str(concert[0]["id"]),
            "rel": "self"
        }]
    
    return jsonify({"id": id})


@app.route('/concerts/<string:concert_id>', methods=['DELETE'])
def delete_concerts(concert_id):
    """Récupère les concerts"""
    concert = execute_query("select * from concerts where c.concert_id = ?", (concert_id,))
    
    if(len(concert) < 1):
        return jsonify({}), 204
    
    execute_query("delete from concerts where concert_id = ?", (concert_id,))

    return jsonify(concert), 200

if __name__ == '__main__':
    # define the localhost ip and the port that is going to be used
    app.run(host='0.0.0.0', port=5000)