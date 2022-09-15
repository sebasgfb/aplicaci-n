from contextlib import redirect_stderr
from wsgiref.util import request_uri
from flask import Flask,render_template,request,session,url_for,redirect
from flask_mysqldb import MySQL, MySQLdb
import MySQLdb.cursors

app = Flask(__name__)

app.secret_key = 'clavesecreta'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'alquilerinstrumentos'

mysql = MySQL(app)

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method=='POST' and 'usuario' in request.form and 'contrasena' in request.form:
        username=request.form['usuario']
        password=request.form['contrasena']
        print(username, password)
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM usuarios WHERE nombreusuario = %s AND contraseñausuario = %s', (username, password,))
        cuenta = cursor.fetchone()
        if cuenta:
            session['loggedin'] = True
            session['username'] = cuenta['nombreusuario']
            return render_template ("inicio.html")
        else:
            return render_template("login.html")
    return render_template("login.html")

@app.route('/inicio')
def inicio():
    return render_template("inicio.html")

@app.route('/instrumentos')
def instrumentos():
    return render_template("instrumentos.html")

@app.route('/alquileres', methods=['GET', 'POST'])
def alquileres():
    if request.method=='GET':
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM alquileres')
        alquileres = cursor.fetchall()
        if alquileres:
            cursor.close()
            return render_template ("alquileres.html", alquileres=alquileres)
        else:
            cursor.close()
            return render_template("alquileres.html")
    elif request.method == 'POST' and 'nombrec' in request.form and 'nombrec' in request.form and 'apellidoc' in request.form and 'telefonoc' in request.form and 'direccionc' in request.form and 'wip1' in request.form and 'wip2' in request.form:
        nombrec=request.form["nombrec"]
        apellidoc=request.form["apellidoc"]
        telefonoc=request.form["telefonoc"]
        direccionc=request.form["direccionc"]
        wip1=request.form["wip1"]
        wip2=request.form["wip2"]
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        print(nombrec,apellidoc,telefonoc,direccionc,wip1,wip2)
        cursor.execute('INSERT INTO alquileres (idalquiler,nombrec,apellidoc,telefonoc,direccionc,wip1,wip2) VALUES (NULL,%s,%s,%s,%s,%s,%s)', (nombrec,apellidoc,telefonoc,direccionc,wip1,wip2))
        mysql.connection.commit()
        return redirect(url_for('alquileres'))
    else:
        return render_template("alquileres.html")

@app.route('/delete/<string:id_data>', methods = ['GET'])
def delete(id_data):
    cursor = mysql.connection.cursor()
    cursor.execute("DELETE FROM alquileres WHERE idalquiler=%s", (id_data))
    mysql.connection.commit()
    return redirect(url_for('alquileres'))

@app.route('/update',methods=['POST','GET'])
def update():

    if request.method == 'POST':
        id_alquiler = request.form['idalquiler']
        nombrec = request.form['nombrec']
        apellidoc = request.form['apellidoc']
        telefonoc = request.form['telefonoc']
        direccionc = request.form['direccionc']
        wip1 = request.form['wip1']
        wip2 = request.form['wip2']
        cur = mysql.connection.cursor()
        cur.execute("""
               UPDATE alquileres
               SET nombrec=%s, apellidoc=%s, telefonoc=%s, direccionc=%s, wip1=%s, wip2=%s
               WHERE idalquiler=%s
            """, (nombrec, apellidoc, telefonoc, direccionc, wip1, wip2, id_alquiler))
        mysql.connection.commit()
        return redirect(url_for('alquileres'))
    return redirect(url_for('alquileres'))

if __name__ == '__main__':
    app.run(debug = True, port = 5000, )