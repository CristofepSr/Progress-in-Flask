from flask import Flask, request, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    nombre = request.form['nombre']
    coreo = request.form['email']
    password = request.form['password']
    
    return render_template('user.html', nombre=nombre, coreo=coreo, password=password)

if __name__ == "__main__":
    app.run( debug=True)