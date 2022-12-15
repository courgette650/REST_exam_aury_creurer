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
        abort(204)
        
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
    nom_groupe = request.args.get('nom_groupe')
    groupe = execute_query("select * from groupes where nom_groupe = ?", (nom_groupe, ))
    
    if(len(groupe) > 0):
        abort(409)
        
    id = execute_query("insert into groupes(nom_groupe) values (?)", (nom_groupe,))
    
    return jsonify({"id" : id}), 201


@app.route('/groupes/<string:nom_groupe>', methods=['DELETE', ])
def delete_groupe(nom_groupe):
    """"Supprime un groupe"""
    groupe = execute_query("select * from groupes where nom_groupe = ?", (nom_groupe, ))
    
    if(len(groupe) < 1):
        jsonify({}), 204
        
    execute_query("delete from groupes where id = ?", (groupe[0]["id"],))
    
    return jsonify(groupe), 200

@app.route('/groupes/<string:nom_groupe>')
def get_groupe(nom_groupe):
    """"Récupère les infos d'un groupe"""
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
    concerts = execute_query("select c.* from groupes g, concerts c where nom_groupe = ? and c.groupe_id = g.id", (nom_groupe, ))
    if(len(concerts) < 1):
        jsonify({}), 204
    # ajout de _links aux concerts
    for i in range(0, len(concerts)):
        concerts[i]["_links"] = [{
                "href": "/concerts/" + urllib.parse.quote(concerts[i]["id"]),
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
        jsonify({}), 204
    # ajout de _links aux concerts
    for i in range(0, len(utilisateurs)):
        utilisateurs[i]["_links"] = [{
                "href": "/utilisateurs/" + urllib.parse.quote(utilisateurs[i]["id"]),
                "rel": "self"
            }, {
                "href": "/utilisateurs/" + urllib.parse.quote(utilisateurs[i]["id"]) + "/reservations",
                "rel": "reservations"
            }]
        
    return jsonify(utilisateurs), 200


@app.route('/utilisateurs/<string:utilsateur_id>')
def get_utilisateur(utilisateur_id):
    """Récupère un utilisateur"""
    utilisateur = execute_query("select * from utilisateurs where id = ?", (utilisateur_id, ))
    if(len(utilisateur) < 1):
        abort(404)
    # ajout de _links aux concerts
    utilisateur[0]["_links"] = [{
            "href": "/utilisateurs/" + urllib.parse.quote(utilisateur[0]["id"]),
            "rel": "self"
        }, {
            "href": "/utilisateurs/" + urllib.parse.quote(utilisateur[0]["id"]) + "/reservations",
            "rel": "reservations"
        }]
        
    return jsonify(utilisateur), 200

@app.route('/utilisateurs/', methods=['POST'])
def post_utilisateur():
    """Crée les utilisateurs"""
    nom_utilisateur = request.args.get('nom_utilisateur')
    utilisateur = execute_query("select * from utilisateurs where nom = ?", (nom_utilisateur, ))
    
    if(len(utilisateur) > 0):
        abort(409)
        
    id = execute_query("insert into utilisateurs(nom_utilisateur) values (?)", (nom_utilisateur, ))

    return jsonify({"id": id}), 200


@app.route('/utilisateurs/<string:utilisateur_id>', methods=['DELETE'])
def delete_utilisateur(utilisateur_id):
    """Crée les utilisateurs"""
    utilisateur = execute_query("select * from utilisateurs where id = ?", (utilisateur_id, ))
    
    if(len(utilisateur) < 1):
        jsonify({}), 204
        
    id = execute_query("delete from utilisateurs where id = ?", (utilisateur_id, ))

    return jsonify({"id": id}), 200

if __name__ == '__main__':
    # define the localhost ip and the port that is going to be used
    app.run(host='0.0.0.0', port=5000)