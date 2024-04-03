from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/registro', methods=['POST'])
def registro():
    
    name = request.form['full-name']
    email = request.form['email']
    password = request.form['password']
    phone = request.form['phone']    
    
    return render_template('user-registro.html', name=name, email=email, password=password, phone=phone)

if __name__ == '__main__':
    app.run(debug= True )