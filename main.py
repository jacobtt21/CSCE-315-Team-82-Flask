from flask import Flask, request, redirect, jsonify
import psycopg2
import psycopg2.extras

app = Flask(__name__)
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
      print("hello")
    except:
      connection.rollback()
    return jsonify({'quantity' :  item_quantity })
  else:
    return redirect("https://www.oustro.xyz", code=302)

@app.route('/fetch-menu-items', methods=['GET'])
def fetch_menu_items():
  if request.method == 'GET':
    rows = {}
    try:
      cur = connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
      cur.execute("SELECT order_type.order_id, order_type.name, order_type.nickname, order_type.type, order_type.price, order_type.orderable, item.name AS mainItemName FROM order_type LEFT JOIN item AS item ON (item_key = item.item_id)")
      rows = cur.fetchall()
      cur.close()
      connection.commit()
    except:
      connection.rollback()
    response = jsonify(rows)
    response.headers.add('Access-Control-Allow-Origin', '*') # allows flask to work for get requests
    return response
  else:
      return redirect("https://www.oustro.xyz", code=302)

@app.route('/get-order-type/<id>', methods=['GET'])
def get_order_type(id):
  if request.method == 'GET':
    rows = {}
    try:
      cur = connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
      cur.execute("SELECT order_type.order_id, order_type.name, order_type.nickname, order_type.type, order_type.price, order_type.orderable, item.name AS mainItemName, order_type.item_key FROM order_type LEFT JOIN item AS item ON (item_key = item.item_id) WHERE order_type.order_id = " + id)
      rows = cur.fetchall()
      cur.close()
      connection.commit()
    except:
      connection.rollback()
    response = jsonify(rows)
    response.headers.add('Access-Control-Allow-Origin', '*') # allows flask to work for get requests
    return response
  else:
      return redirect("https://www.oustro.xyz", code=302)

@app.route('/fetch-items', methods=['GET'])
def fetch_items():
  if request.method == 'GET':
    rows = {}
    try:
      cur = connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
      cur.execute("SELECT * from item")
      rows = cur.fetchall()
      cur.close()
      connection.commit()
    except:
      connection.rollback()
    response = jsonify(rows)
    response.headers.add('Access-Control-Allow-Origin', '*') # allows flask to work for get requests
    return response
  else:
      return redirect("https://www.oustro.xyz", code=302)

@app.route('/edit-menu-item/<id>', methods=['POST'])
def edit_menu_item(id):
    try:
      form = request.form.to_dict(flat=False)
      query = ""

      for i in form:
        print (i)

      # cur = connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
      # cur.execute("SELECT order_type.order_id, order_type.name, order_type.nickname, order_type.type, order_type.price, order_type.orderable, item.name AS mainItemName, order_type.item_key FROM order_type LEFT JOIN item AS item ON (item_key = item.item_id) WHERE order_type.order_id = " + id)
      # rows = cur.fetchall()
      # cur.close()
      connection.commit()
    except:
      connection.rollback()
    response = jsonify({})
    response.headers.add('Access-Control-Allow-Origin', '*') # allows flask to work for get requests
    return response

if __name__ == '__main__':
  app.run()
