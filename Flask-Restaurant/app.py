from flask import Flask, request, render_template, session, redirect , url_for
import sqlite3

app = Flask(__name__)
#  Clave secreta para la sesion de la web
app.secret_key = 'havit'

#  Funcion que se conecta ala base de datos
def connect_database():
    conn = sqlite3.connect('database/restaurant.db')
    return conn

# Ruta Principal de web
@app.route('/')
def index():
    return render_template('index.html')

#  Ruta para Agregar Categoria
@app.route('/Categoria', methods=['GET', 'POST'])
def categoria():
    if request.method == 'POST':
        try:
            nombreCategoria = request.form['categoria'] # Obtiene el Nombre de la Categoria del formulario

            conn = connect_database() # Conexion a la Base De Batos
            cursor = conn.cursor()
            # Insertar el nombre de la categoria en la base de datos
            cursor.execute('INSERT INTO categoria (nombre) VALUES (?)', (nombreCategoria,))
            conn.commit() # Confirma la Transacion
            
            # Mensaje para Indicar al usuarion que se agrega la base de datos
            mensaje = 'La Cetegoria Se Agrego Corectamente'
        except sqlite3.IntegrityError:
            # Mesaje que indica al usuario que ya exista la categoria
            mensaje = 'Esta Categoria Ya Existe'
        
        conn.close() # Cierra la conecion
        return render_template('categoria.html', mensaje=mensaje)
            
    return render_template('categoria.html')

#  Ruta pata Agregar platos a la base de datos
@app.route('/Plato', methods=['GET', 'POST'])
def plato():
    conn = connect_database() # Conexion a la Base De Batos
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM categoria")
    categoria = cursor.fetchall() # Obtiene todas la categorias
    
    if request.method == 'POST':
        try:
            categoriaID = request.form['numCategoria'] # Obtiene el id de la Categoria del formulario
            plato = request.form['plato'] # Obtiene el Nombre del del plato del formulario

            # Inserta el Nombre del plato y el id de la categia en la base de datos
            cursor.execute("INSERT INTO plato (nombre, categoria_id) VALUES (?, ?)", (plato, categoriaID))
            conn.commit() # Confirma la Transacion
            mensaje = 'Plato Añadido Exitosamente'
        except KeyError:
            mensaje = 'Error En Los Datos Enviados'
        except sqlite3.IntegrityError:
            mensaje = 'Nose Puede Este Plato Ya Existe En Una Categoria'
            
        conn.close() # Cierra la conecion
        return render_template('platos.html', categorias = categoria, mensaje = mensaje)
    
    
    
    return render_template('platos.html', categorias = categoria)

@app.route('/mostrar_menu')
def mostrar_menu():
    conn = connect_database() # Conexion a la Base De Batos
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM categoria")
    categorias = cursor.fetchall() # Obtiene todas la categorias
    
    platos = []
    if categorias: # Si hay categorías en la base de datos
        for categoria in categorias: # Para cada categoría
            # Consulta los platos pertenecientes a la categoría actual
            cursor.execute("SELECT nombre FROM plato WHERE categoria_id=?", (categoria[0],))
            platos_categoria = cursor.fetchall()  # Obtiene los nombres de los platos
            platos.append((categoria, platos_categoria)) # Agrega la categoría y sus platos a la lista
    
    conn.close() # Cierra la conecion
    
    return render_template('menu.html', categorias_platos=platos)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username'] # Obtiene el nombre de usuario del formulario
        password = request.form['password'] # Obtiene la contraseña del formulario
        
        session['username'] = username # Almacena el nombre de usuario en la sesión
        
        conn = connect_database() # Conexion a la Base De Batos
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM user WHERE username=? AND password=?', (username, password))
        
        user = cursor.fetchone() # Obtiene usuario y la contraseña
        
        conn.close() # Cierra la conecion
        
        if user:
            return redirect(url_for('index'))
        else:    
            return render_template('login.html')
    return render_template('login.html')

@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        username = request.form['username'] # Obtiene el nombre de usuario del formulario
        email = request.form['email'] # Obtiene el Corro Elentronico del formulario
        password = request.form['password'] # Obtiene la contraseña del formulario
        session['username'] = username # Almacena el nombre de usuario en la sesión
        
        conn = connect_database() # Conexion a la Base De Batos
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM user WHERE username=? OR email=?', (username, email))
        user = cursor.fetchone() # Obtiene el usuario y el correo de la base de datos
        
        if user:
            conn.close() # Cierra la conecion
            return render_template('registro.html', mensaje='El Usuario Y El Correo Electrónico Ya Existe.')
        else:
            cursor.execute('INSERT INTO user (username, email, password) VALUES (?, ?, ?)', (username, email, password))
            conn.commit() # Confirma la Transacion
            conn.close() # Cierra la conecion

            return redirect(url_for('index'))
    
    return render_template('registro.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
