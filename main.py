from flask import Flask, request, redirect, jsonify

app = Flask(__name__)

@app.route('/', methods=['POST', 'GET'])
def index():
  if request.method == 'POST':
      return jsonify({'res' :  "hi there cutie ;)" })
  else:
    return redirect("http://www.oustro.xyz", code=302)

if __name__ == '__main__':
    app.run()