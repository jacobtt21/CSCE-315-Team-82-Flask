from flask import Flask, request, redirect, jsonify
from decimal import *
import psycopg2
import psycopg2.extras
import jwt
import datetime


app = Flask(__name__)

connection = psycopg2.connect(user="csce315_908_hollenbeck",password="130009055", host="csce-315-db.engr.tamu.edu", port="5432", database="csce315_908_82")

# https://pynative.com/python-postgresql-tutorial/ <-- tutorial on how to use psycopg2. Refer to this if you have any questions

@app.route('/', methods=['POST', 'GET'])
def index():
  if request.method == 'POST':
    return jsonify({'res' :  connection.get_dsn_parameters()})   # this returns the stats of the connection and can be changed.
  else:
    return redirect("https://www.oustro.xyz", code=302)

# Get request for google OAUTH
@app.route('/authenticate/<google_id>', methods=['GET'])
def authenticate(google_id):
  if request.method == 'GET':
    rows = {}
    try:
      cur = connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
      cur.execute("SELECT * FROM users WHERE email = '" + google_id + "';")
      rows = cur.fetchall()
      cur.close()
      connection.commit()
    except:
      connection.rollback()

    response = {}
    authenticated = (len(rows) > 0)
    if authenticated:
      for column in rows[0]:
        response[column] = rows[0][column]
      response["authenticated"] = True
      response["jwt"] = jwt.encode({"google_id": google_id, "exp": datetime.datetime.now(tz=datetime.timezone.utc) + datetime.timedelta(seconds=3600)}, "FAKE SECRET", algorithm="HS256")
    else:
      response["authenticated"] = False

    response = jsonify(response)
    response.headers.add('Access-Control-Allow-Origin', '*') # allows flask to work for get requests
    return response
  else:
      return redirect("https://www.oustro.xyz", code=302)

# Request for Excess Report
# CAN'T USE PARENTHASES IN THE DATES
# Date format has to be 10-01-2022
@app.route('/get-excess-report/<start_date>/<end_date>', methods=['GET'])
def get_excess_report(start_date=None, end_date=None):
  if request.method == 'GET':
    rows = {}
    try:
      cur = connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
      excess_report = "SELECT item_id, name FROM item WHERE (( SELECT COUNT(order_type_key) FROM order_item LEFT JOIN bill AS bill ON (order_item.bill_key = bill.bill_id) LEFT JOIN order_type AS order_type ON (order_type_key = order_type.order_id) WHERE order_type.item_key = item_id AND bill.date_time < ' {1} ' AND bill.date_time > ' {0} ' ) * item.amount_used_per_order < (0.1 * item.quantity)) AND (( SELECT COUNT(item_key) FROM order_type WHERE item_key = item_id ) > 0)".format(start_date, end_date)
      cur.execute(excess_report)
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

# Request for Sales Report
# CAN'T USE PARENTHASES IN THE DATES
# Date format has to be 10-01-2022
@app.route('/get-sales-report/<start_date>/<end_date>/<order_id>', methods=['GET'])
def get_sales_report(start_date=None, end_date=None, order_id=None):
  if request.method == 'GET':
    rows = {}
    try:
      cur = connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
      excess_report = "SELECT COUNT(order_type_key) AS cnt, bill.date_time::date AS date, DATE_PART('day', bill.date_time - '{0}') AS x FROM order_item LEFT JOIN bill AS bill ON (bill_key = bill.bill_id) LEFT JOIN order_type AS order_type ON (order_type_key = order_type.order_id) WHERE bill.date_time < '{1}' AND bill.date_time > '{0}' AND order_type.order_id = {2} GROUP BY date, x ORDER BY date;".format(start_date, end_date, order_id)
      print(excess_report)
      cur.execute(excess_report)
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

# Request for Restock Report
# CAN'T USE PARENTHASES IN THE DATES
# Date format has to be 10-01-2022
@app.route('/get-restock-report/', methods=['GET'])
def get_restock_report():
  if request.method == 'GET':
    rows = {}
    try:
      cur = connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
      # excess_report = "SELECT * FROM (SELECT item.item_id, item.name, item.quantity, CASE WHEN order_count * COALESCE(item.amount_used_per_order,0) >= COALESCE(item.quantity,0)  THEN TRUE ELSE FALSE END restock, CEILING(order_count * COALESCE(item.amount_used_per_order,0) - COALESCE(item.quantity,0)) AS deficit FROM (SELECT order_type_key, order_type.name AS order_type_name, COUNT(order_type_key) AS order_count, item_key FROM order_item LEFT JOIN bill AS bill ON (bill_key = bill.bill_id) LEFT JOIN order_type AS order_type ON (order_type_key = order_type.order_id) AND order_type.item_key IS NOT NULL GROUP BY order_type_key, order_type_name, item_key ORDER BY order_type_key) sub LEFT JOIN item AS item ON (item_key = item.item_id)) sub WHERE restock = TRUE;"
      excess_report = "SELECT * FROM (SELECT item.item_id, item.name, item.quantity, CASE WHEN COALESCE(item.minimum_needed,0) > COALESCE(item.quantity,0)  THEN TRUE ELSE FALSE END restock, COALESCE(item.minimum_needed,0) - COALESCE(item.quantity,0) AS deficit FROM item) sub WHERE restock = TRUE;"
      cur.execute(excess_report)
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

# Request for Pairings Report
# CAN'T USE PARENTHASES IN THE DATES
# Date format has to be 10-01-2022
@app.route('/get-pairings-report/<start_date>/<end_date>', methods=['GET'])
def get_pairings_report(start_date=None, end_date=None):
  if request.method == 'GET':
    rows = {}
    try:
      cur = connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
      excess_report = "With temp AS (SELECT bill_key, order_type_key FROM order_item LEFT JOIN bill AS bill ON (order_item.bill_key = bill.bill_id) WHERE bill.date_time < '{1}' AND bill.date_time > '{0}' GROUP BY 1,2) SELECT item_1.name AS item_1, item_2.name AS item_2, frequency FROM (SELECT * FROM (SELECT u1.order_type_key AS item_1_key, u2.order_type_key AS item_2_key, COUNT(*) AS frequency, RANK() OVER (ORDER BY COUNT(*) DESC) Rnk FROM temp u1 JOIN temp u2 ON u1.order_type_key < u2.order_type_key AND u1.bill_key = u2.bill_key WHERE (u1.order_type_key < 20 OR u1.order_type_key > 24) GROUP by 1,2) sub WHERE Rnk < 10) sub LEFT JOIN order_type AS item_1 ON (item_1_key = item_1.order_id) LEFT JOIN order_type AS item_2 ON (item_2_key = item_2.order_id);".format(start_date, end_date)
      cur.execute(excess_report)
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

#
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

# Request to get menu items
@app.route('/fetch-menu-items', methods=['GET'])
def fetch_menu_items():
  if request.method == 'GET':
    rows = {}
    try:
      cur = connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
      cur.execute("SELECT order_type.order_id, order_type.name, order_type.nickname, order_type.type, order_type.price, order_type.orderable, order_type.image, item.name AS mainItemName FROM order_type LEFT JOIN item AS item ON (item_key = item.item_id)")
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

# Request to get order type
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

# Request to get item by id
@app.route('/get-item/<id>', methods=['GET'])
def get_item(id):
  if request.method == 'GET':
    rows = {}
    try:
      cur = connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
      cur.execute("SELECT item.name, item.type, item.quantity, item.price, item.minimum_needed, item.amount_used_per_order FROM item WHERE item.item_id =" + id)
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

# Request to get all items
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

# Request to add item
@app.route('/edit-inventory-item/<id>', methods=['POST'])
def edit_inventory_item(id):
    try:
      form = request.form.to_dict(flat=True)

      if (len(form) == 0):
        response = jsonify({})
        response.headers.add('Access-Control-Allow-Origin', '*') # allows flask to work for get requests
        return response

      strings = ["name", "quantity", "type"]
      query = "UPDATE item SET "

      form = dict( [(k,v) for k,v in form.items() if len(v)>0])

      i = 0
      for column in form:
        if (strings.count(column) > 0):
          query += column + " = " + "'" + form[column] + "'"
        else:
          query += column + " = " + form[column]

        if i < len(form) - 1:
          query += ", "

        i = i + 1

      query += " WHERE item_id = " + id

      print(query)

      cur = connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
      cur.execute(query)
      cur.close()
      connection.commit()
    except:
      connection.rollback()
    response = jsonify({})
    response.headers.add('Access-Control-Allow-Origin', '*') # allows flask to work for get requests
    return response

# Request to edit menu item
@app.route('/edit-menu-item/<id>', methods=['POST'])
def edit_menu_item(id):
    try:
      form = request.form.to_dict(flat=True)

      if (len(form) == 0):
        response = jsonify({})
        response.headers.add('Access-Control-Allow-Origin', '*') # allows flask to work for get requests
        return response

      strings = ["name", "nickname", "type", "image"]
      query = "UPDATE order_type SET "

      form = dict( [(k,v) for k,v in form.items() if len(v)>0])

      i = 0
      for column in form:
        if (strings.count(column) > 0):
          query += column + " = " + "'" + form[column] + "'"
        else:
          query += column + " = " + form[column]

        if i < len(form) - 1:
          query += ", "

        i = i + 1

      query += " WHERE order_id = " + id

      print(query)

      cur = connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
      cur.execute(query)
      cur.close()
      connection.commit()
    except:
      connection.rollback()
    response = jsonify({})
    response.headers.add('Access-Control-Allow-Origin', '*') # allows flask to work for get requests
    return response

# Request to add new menu item
@app.route('/new-menu-item', methods=['POST'])
def new_menu_item():
    try:
      form = request.form.to_dict(flat=True)
      print(form)

      if (len(form) == 0):
        response = jsonify({})
        response.headers.add('Access-Control-Allow-Origin', '*') # allows flask to work for get requests
        return response

      strings = ["name", "nickname", "type", "image"]
      columns = ""
      values = ""
      subquery = "SELECT MAX(order_id) from order_type"

      last_column = "order_id"
      last_value = "(" + subquery + ") + 1"

      form = dict( [(k,v) for k,v in form.items() if len(v)>0])

      i = 0
      for column in form:
        columns += column
        if (strings.count(column) > 0):
          values += "'" + form[column] + "'"
        else:
          values += form[column]

        columns += ", "
        values += ", "

        i = i + 1

      columns += last_column
      values += last_value

      query = "INSERT INTO order_type (" + columns + ") VALUES (" + values + ")"
      print(query)

      cur = connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
      cur.execute(query)
      cur.close()
      connection.commit()
    except:
      connection.rollback()
    response = jsonify({})
    response.headers.add('Access-Control-Allow-Origin', '*') # allows flask to work for get requests
    return response

# Request to delete menu item
@app.route('/delete-menu-item/<id>', methods=['POST'])
def delete_menu_item(id):
    try:
      query = ""
      if (id.isnumeric() and int(id) > 0):
        query = "DELETE FROM order_type WHERE order_id = " + id
        cur = connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cur.execute(query)
        cur.close()
        connection.commit()
    except:
      connection.rollback()
    response = jsonify({})
    response.headers.add('Access-Control-Allow-Origin', '*') # allows flask to work for get requests
    return response

# Request to add new menu item
@app.route('/new-item', methods=['POST'])
def new_item():
    try:
      form = request.form.to_dict(flat=True)
      print(form)

      if (len(form) == 0):
        response = jsonify({})
        response.headers.add('Access-Control-Allow-Origin', '*') # allows flask to work for get requests
        return response

      strings = ["name", "type"]
      columns = ""
      values = ""
      subquery = "SELECT MAX(item_id) from item"

      last_column = "item_id"
      last_value = "(" + subquery + ") + 1"

      form = dict( [(k,v) for k,v in form.items() if len(v)>0])

      i = 0
      for column in form:
        columns += column
        if (strings.count(column) > 0):
          values += "'" + form[column] + "'"
        else:
          values += form[column]

        columns += ", "
        values += ", "

        i = i + 1

      columns += last_column
      values += last_value

      query = "INSERT INTO item (" + columns + ") VALUES (" + values + ")"
      print(query)

      cur = connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
      cur.execute(query)
      cur.close()
      connection.commit()
    except:
      connection.rollback()
    response = jsonify({})
    response.headers.add('Access-Control-Allow-Origin', '*') # allows flask to work for get requests
    return response

# Request to delete item
@app.route('/delete-item/<id>', methods=['POST'])
def delete_item(id):
    try:
      query = ""
      if (id.isnumeric() and int(id) > 0):
        query = "DELETE FROM item WHERE item_id = " + id
        cur = connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cur.execute(query)
        cur.close()
        connection.commit()
    except:
      connection.rollback()
    response = jsonify({})
    response.headers.add('Access-Control-Allow-Origin', '*') # allows flask to work for get requests
    return response

# Request to add new order
@app.route('/take-order', methods=['POST'])
def take_order():
    try:
      bid = request.form['bid']
      fid = request.form['fid']
      print(bid)
      print(fid)
      subquery = "SELECT order_key FROM order_item ORDER BY order_key DESC LIMIT 1"
      last_value = "(" + subquery + ") + 1"

      query = "INSERT INTO order_item (order_key, bill_key, order_type_key) VALUES ("+ last_value + ", '" + bid + "', '" + fid + "');"
      print(query)
      cur = connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
      cur.execute(query)

      query = "UPDATE item SET quantity = quantity - amount_used_per_order WHERE amount_used_per_order IS NOT NULL AND item_id = (SELECT item_key from order_type WHERE order_id = " + fid + ");"
      cur.execute(query)

      cur.close()
      connection.commit()
    except:
      connection.rollback()
    response = jsonify({})
    response.headers.add('Access-Control-Allow-Origin', '*') # allows flask to work for get requests
    return response

# Request to add new bill
@app.route('/new-bill', methods=['POST'])
def new_bill():
    BillID = {}
    try:
      price = request.form['price']
      server = request.form['served']

      if (price == 0):
        response = jsonify({})
        response.headers.add('Access-Control-Allow-Origin', '*') # allows flask to work for get requests
        return response

      subquery = "SELECT bill_id FROM bill ORDER BY bill_id DESC LIMIT 1"
      last_value = "(" + subquery + ") + 1"

      query = "INSERT INTO bill (served_by_employee_key, price, bill_id, date_time) VALUES ('" + server + "', '" + price + "', " + last_value + ", NOW());"
      cur = connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
      cur.execute(query)
      cur.execute(subquery)
      BillID = cur.fetchall()
      cur.close()
      connection.commit()
    except:
      connection.rollback()
    response = jsonify(BillID)
    response.headers.add('Access-Control-Allow-Origin', '*') # allows flask to work for get requests
    return response
