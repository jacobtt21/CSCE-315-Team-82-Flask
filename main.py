from flask import Flask, request, redirect, jsonify
import psycopg2
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
connection = psycopg2.connect(user="csce315_908_hollenbeck",password="130009055", host="csce-315-db.engr.tamu.edu", port="5432", database="csce315_908_82")

# https://pynative.com/python-postgresql-tutorial/ <-- tutorial on how to use psycopg2. Refer to this if you have any questions


@app.route('/', methods=['POST', 'GET'])
def index():
  if request.method == 'POST':
    return jsonify({'res' :  connection.get_dsn_parameters()})   # this returns the stats of the connection and can be changed.
  else:
    return redirect("https://www.oustro.xyz", code=302)


@app.route('/item_price', methods=['POST', 'GET'])
def get_item_price():
  if request.method == 'POST':
    cur = connection.cursor()
    try:
      # item = request.form['item'] <-- getting the item from the API call to the server which can be used in the SQL query
      cur.execute("select quantity from item where item_id = 1")
      rows = cur.fetchall()
      item_quantity = str(rows[0][0])
      cur.close()
      connection.commit()
    except:
      connection.rollback()
    return jsonify({'quantity' :  item_quantity })
  else:
    return redirect("https://www.oustro.xyz", code=302)

if __name__ == '__main__':
  app.run()