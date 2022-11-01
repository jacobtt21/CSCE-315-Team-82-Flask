from flask import Flask, request, redirect, jsonify
import psycopg2

app = Flask(__name__)


@app.route('/', methods=['POST', 'GET'])
def index():
  if request.method == 'POST':
    connection = psycopg2.connect(user="csce315_908_hollenbeck",password="130009055", host="csce-315-db.engr.tamu.edu", port="5432", database="csce315_908_82")
    return jsonify({'res' :  connection.get_dsn_parameters()})
  else:
    return redirect("http://www.oustro.xyz", code=302)

if __name__ == '__main__':
    app.run()