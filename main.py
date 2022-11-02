from flask import Flask, request, redirect, jsonify
import psycopg2

app = Flask(__name__)
connection = psycopg2.connect(user="csce315_908_hollenbeck",password="130009055", host="csce-315-db.engr.tamu.edu", port="5432", database="csce315_908_82")

# https://pynative.com/python-postgresql-tutorial/ <-- tutorial on how to use psycopg2. Refer to this if you have any questions

@app.route('/', methods=['POST', 'GET'])
def index():
  if request.method == 'POST':
    return jsonify({'res' :  connection.get_dsn_parameters()})   # this returns the stats of the connection and can be changed.
  else:
    return redirect("https://www.oustro.xyz", code=302)

if __name__ == '__main__':
    app.run()