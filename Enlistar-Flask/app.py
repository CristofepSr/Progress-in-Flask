from flask import Flask,render_template, request, session,redirect,url_for
import sqlite3

app = Flask(__name__)
app.secret_key = 'havit'

def connect_db():
    conn = sqlite3.connect('database/enlistar.db')
    return conn

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/userlist')
def userlist():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('SELECT id,username, email, creado_en FROM user')
    datos = cursor.fetchall()
    conn.close()
    
    return render_template('userlist.html', datos=datos)

@app.route('/product')
def product():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM productos')
    producto = cursor.fetchall()
    conn.close()
        
    return render_template('producto/productos.html', producto=producto)

# Ruta para mostrar el formulario de edición de un producto específico
@app.route('/edit_product/<int:id>', methods=['GET', 'POST'])
def editar_producto(id):
    db = connect_db()
    cursor = db.cursor()
    if request.method == 'POST':
        nombre = request.form['nombre']
        descripcion = request.form['descripcion']
        precio = request.form['precio']
        stock = request.form['stock']
        cursor.execute("UPDATE Productos SET Nombre=?, Descripcion=?, Precio=?, Stock=? WHERE ID=?", (nombre, descripcion, precio, stock, id))
        db.commit()
        db.close()
        return redirect('/product')
    else:
        cursor.execute("SELECT * FROM Productos WHERE ID=?", (id,))
        producto = cursor.fetchone()
        db.close()
        return render_template('producto/editar.html', producto=producto)

@app.route('/add_product', methods=['GET', 'POST'])
def add_product():
    if request.method == 'POST':
        nombre = request.form['nombre']
        descripcion = request.form['descripcion']
        precio = request.form['precio']
        stock = request.form['stock']

        if 'username' in session:
            creador = session['username']
        else:
            creador = 'Anonimo'

        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO productos (nombre, descripcion, precio, stock, creador) VALUES (?, ?, ?, ?, ?)', (nombre, descripcion, precio, stock, creador))
        conn.commit() 
        cursor.close() 

        return redirect(url_for('product'))
    return render_template('producto/agregar.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username'] 
        password = request.form['password'] 
        
        conn = connect_db() 
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM user WHERE username=? AND password=?', (username, password))
        
        user = cursor.fetchone() 
        conn.close() 
        
        if user:
            session['username'] = username 
            return redirect(url_for('index'))
        else: 
            return render_template('auth/login.html')
    return render_template('auth/login.html')

@app.route('/register', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        username = request.form['username'] 
        email = request.form['email']
        password = request.form['password']
        
        session['username'] = username 
        
        conn = connect_db() 
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM user WHERE username=? OR email=?', (username, email))
        user = cursor.fetchone()
        
        if user:
            conn.close() 
            return render_template('auth/registel.html')
        else:
            cursor.execute('INSERT INTO user (username, email, password) VALUES (?, ?, ?)', (username, email, password))
            conn.commit() 
            conn.close() 

            return redirect(url_for('index'))
    return render_template('auth/register.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)