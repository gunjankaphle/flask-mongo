from flask import Flask, jsonify, request, url_for, redirect
import mongo_connector
import re

app = Flask(__name__)


db_client = mongo_connector.get_connection()
db = db_client.fifa


@app.route('/teams', methods=['GET'])
def get_teams():
    teams = db.teams
    result = []
    for each_team in teams.find():
        print(str(each_team))
        result.append({
            '_id': each_team.get('_id'),
            'name': each_team.get('name'),
            'code': each_team.get('code'),
            'continent': each_team.get('continent'),
            'association': each_team.get('assoc').get('name') if each_team.get('assoc') else None
        })

    return jsonify({'result': result})


@app.route('/teams/<code>', methods=['GET'])
def get_team_by_code(code):
    teams = db.teams

    one_team = teams.find_one({'code': re.compile(code, re.IGNORECASE)})
    result = {
                '_id': one_team.get('_id'),
                'name': one_team.get('name'),
                'code': one_team.get('code'),
                'continent': one_team.get('continent')
            }

    return jsonify({'result': result})


@app.route('/team', methods=['POST'])
def add_team():
    teams = db.teams
    name = request.json['name']
    code = request.json['code']
    continent = request.json['continent']

    new_team_id = teams.insert({
        'name': name,
        'code': code.upper(),
        'continent': continent
    })

    new_team = teams.find_one({'_id': new_team_id})
    result = {'name': new_team['name'], 'code': new_team['code']}

    return jsonify({'result': result})


@app.route('/teams/<code>', methods=['DELETE'])
def delete_team_by_code(code):
    teams = db.teams
    teams.remove({'code': re.compile(code, re.IGNORECASE)})

    return redirect(url_for("get_teams"))


if __name__ == '__main__':
    app.run(debug=True)
