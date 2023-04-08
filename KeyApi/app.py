from flask import Flask, jsonify
from flask_restful import Resource, Api, reqparse
import sqlite3
from config import SQL_PATH
app = Flask(__name__)
api = Api(app)
parser = reqparse.RequestParser()
parser.add_argument('id')
parser.add_argument('key')

def con(query):
    con = sqlite3.connect('db_.sqlite3')
    cur = con.cursor()
    return cur.execute(query)


class GetKey(Resource):
    def get(self, id_user):

        try:
            sqlite_connection = sqlite3.connect('db_.sqlite3')
            cursor = sqlite_connection.cursor()
            resalt = cursor.execute(
                "SELECT key FROM keys WHERE id_user=?", [id_user]).fetchone()

            sqlite_connection.commit()
            cursor.close()
            return {'key': resalt}

        except Exception as e:
            return jsonify({'error': e})


        return {'hello': 'world'}

class SaveKey(Resource):
    def post(self):
        args = parser.parse_args()
        ln = args['id']
        fn = args['key']
        try:
            sqlite_connection = sqlite3.connect('db_.sqlite3')
            cursor = sqlite_connection.cursor()
            cursor.execute(
                "INSERT INTO keys (id_user, key) VALUES(?, ?)", (ln, fn))
            sqlite_connection.commit()
            cursor.close()
        except Exception as e:
            return jsonify({'error': e})

        return jsonify({'response': 'ok'})



api.add_resource(GetKey, '/get_key/<int:id_user>')
api.add_resource(SaveKey, '/post_key')

if __name__ == '__main__':
    # con('CREATE TABLE keys (id integer primary key ,id_user INTEGER,key VARCHAR(255));')
    app.run(debug=True)
