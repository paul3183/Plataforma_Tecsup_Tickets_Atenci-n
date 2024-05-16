from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, login_required, logout_user, current_user
from app import app, basededatos
from modelos import Usuario, Ticket
from formulario import Formulario_Registro, Formulario_Login
from werkzeug.security import check_password_hash
from sqlalchemy.exc import IntegrityError

import numpy as np

def generar_ticket_para_area(area):
    contador = Ticket.query.filter_by(area=area).count() + 1
    while True:
        yield f"{area.upper()} - {contador:02d}"
        contador += 1

@app.route('/')
def principal():
    return render_template('principal.html')


@app.route('/salir')
@login_required  #antes de salir tendria que haber estado dentro 
def salir():
    logout_user() #esta funcion de flask_login, quita sesion al usuario que estaba logueado antes
    flash('Sesion de usuario cerrada')
    return redirect(url_for('principal')) #cuando sale encaminamos al usuario en la pagina principal

@app.route('/ingresar', methods= ['GET', 'POST'])
def ingresar():
    formulario = Formulario_Login()
    if formulario.validate_on_submit(): #si se ha enviado? entonces
        usuario = Usuario.query.filter_by(email = formulario.email.data).first() #coja el primero con first
        if usuario is not None:     #pasamos el usuario que hemos recuperado en basededatos, y la password que ha metido el usuario en el formulario con .data
            if check_password_hash(usuario.password_encriptada, formulario.password.data):
                login_user(usuario) #gracias a flask_login mediante loginuser damos de alta al usuario 
                flash('Usuario ha entrado correctamente')
                proxima_pagina = request.args.get('next')
                if proxima_pagina is None or not proxima_pagina.startswith('/'):
                    proxima_pagina = url_for('index')
                return redirect(proxima_pagina)
    return render_template('ingresar.html', formulario = formulario)

@app.route('/registrar', methods=['GET', 'POST'])
def registrar():
    formulario = Formulario_Registro()
    if formulario.validate_on_submit():
        try:
            usuario = Usuario(email=formulario.email.data, nombre=formulario.nombre.data, password=formulario.password.data)
            basededatos.session.add(usuario)
            basededatos.session.commit()
            flash('Usuario registrado correctamente')
            return redirect(url_for('ingresar'))
        except IntegrityError:
            basededatos.session.rollback()
            flash('El correo electrónico ya está registrado. Por favor, utiliza otro.')
    return render_template('registrar.html', formulario=formulario)

@app.route('/index')
@login_required   #con flask_login: obliga al usuario loguearse para poder entrar a index.html
def index():
    return render_template('index.html')

@app.route('/lista')
@login_required  
def lista():
    tickets = Ticket.query.all()
    return render_template('lista_tickets.html', tickets = tickets)

@app.route('/generar_ticket', methods=['GET', 'POST'])
@login_required
def generar_ticket_form():
    areas_servicios_educativos = {"SD": ["Secretaría Docente","Carola Rosas"], "PS": ["Psicopedagogía", "Roberto Molina"], "DPE": ["Desarrollo Profesional del Estudiante", "Jenny Fabián"], "GT": ["Grados y Titulos", "Elizabeth Del Aguila"], "SE": ["Coordinación de Servicios Educativos", "Katherine Ramirez"] , "B": ["Biblioteca", "Juan Pacotaipe"]}
    
    if request.method == 'POST':
        area = request.form.get('area').upper()
        
        if area in areas_servicios_educativos:
            ticket_area = next(generar_ticket_para_area(area))
            nuevo_ticket = Ticket(area=area, numero=ticket_area, usuario_id = current_user.id)
            basededatos.session.add(nuevo_ticket)
            basededatos.session.commit()
            area = nuevo_ticket.area
            texto = f"{ticket_area}"
            
            profesor_nombre = areas_servicios_educativos[area][1]
            area_nombre_completo = areas_servicios_educativos[area][0]
            minutos = np.random.randint(1,8)
            return render_template('ticket_emitido.html', texto=texto, ticket_area=ticket_area, usuario=current_user, profesor_nombre=profesor_nombre, area_nombre_completo=area_nombre_completo, minutos=minutos)
        
        else:
            message = 'Área no válida. Ingresa solo los siguientes valores: SD, PS, DPE, GT, SE, B'
            return render_template('index.html', message=message)

    else:
        formulario = Formulario_Registro()  
        return render_template('ticket_emitido.html', formulario=formulario)
    

if __name__ == '__main__':
    with app.app_context():
        basededatos.create_all()

    app.run(debug=True, host='0.0.0.0')




#ahora para actualizar los cambios debemos crear una variable de entorno:
    # set FLASK_APP = ejemplo07.py   para windows $env:FLASK_APP = "ejemplo08.py"
    # export  FLASK_APP = ejemplo07.py para mac
    #una vez exportada la variable d eentorno:
    #hacer la migracion , pasarle el modelo modificado ala base de datos sqlite
    #flask db init          #-- inicializa el cambio crea la carpeta migraciones etc
    #flask db migrate -m     "se agrego columna de color"
    #flask db upgrade   #finalizar los cambios


    

"""import os
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

directorio = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(directorio, 'datos.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

basededatos = SQLAlchemy(app)

class Ticket(basededatos.Model):
    __tablename__ = 'Tickets'
    id = basededatos.Column(basededatos.Integer, primary_key=True)
    area = basededatos.Column(basededatos.String(20))
    numero = basededatos.Column(basededatos.String(5))

    def __init__(self, area, numero):
        self.area = area
        self.numero = numero

    def __repr__(self):
        texto = f"<Ticket : {self.area} - {self.numero}>"
        return texto

# Rutas

def generar_ticket_para_area(area):
    contador = 1
    while True:
        yield f"{area.upper()} - {contador:02d}"
        contador += 1

@app.route('/')
def index():
    tickets = Ticket.query.all()
    return render_template('index.html', tickets=tickets)

@app.route('/generar_ticket', methods=['POST'])
def generar_ticket_form():
    area = request.form.get('area')
    if area:
        ticket_area = next(generar_ticket_para_area(area))
        nuevo_ticket = Ticket(area=area, numero=ticket_area)
        basededatos.session.add(nuevo_ticket)
        basededatos.session.commit()
        return f"Ticket generado para {area}: {ticket_area}"
    else:
        return render_template('error.html', message='Área no válida')

if __name__ == '__main__':
    with app.app_context():
        basededatos.create_all()
    app.run(debug=True)

"""



""""
import os
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

directorio = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(directorio, 'datos.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

basededatos = SQLAlchemy(app)

class Ticket(basededatos.Model):
    __tablename__ = 'Tickets'
    id = basededatos.Column(basededatos.Integer, primary_key=True)
    area = basededatos.Column(basededatos.String(20))
    numero = basededatos.Column(basededatos.String(5))

    def __init__(self, area, numero):
        self.area = area
        self.numero = numero

    def __repr__(self):
        texto = f"<Ticket : {self.area} - {self.numero}>"
        return texto

def secretaria_docente():
    for n in range(1, 10000):
        yield f"SD - {n:04d}"
sd = secretaria_docente()

def psicopedagogia():
    for n in range(1, 10000):
        yield f"PS - {n:04d}"
ps = psicopedagogia()

def desarrollo_profesional_estudiante():
    for n in range(1, 10000):
        yield f"DPE - {n:04d}"
dpe = desarrollo_profesional_estudiante()

def grados_titulos():
    for n in range(1, 10000):
        yield f"GT - {n:04d}"
gt = grados_titulos()

def servicios_educativos():
    for n in range(1, 10000):
        yield f"SE - {n:04d}"
se = servicios_educativos()

def biblioteca():
    for n in range(1, 10000):
        yield f"B - {n:04d}"
b = biblioteca()

# Rutas

@app.route('/')
def index():
    tickets = Ticket.query.all()
    return render_template('index.html', tickets=tickets)

@app.route('/listar')
def listar():


@app.route('/generar_ticket', methods=['POST'])
def generar_ticket_form():
    area = request.form.get('area')
    if area:
        ticket_area = next(generar_ticket_para_area(area))
        nuevo_ticket = Ticket(area=area, numero=ticket_area)
        basededatos.session.add(nuevo_ticket)
        basededatos.session.commit()
        return f"Ticket generado para {area}: {ticket_area}"
    else:
        return render_template('error.html', message='Área no válida')

def generar_ticket_para_area(area):
    if area == 'secretaria_docente':
        for n in range(1, 10000):
            yield f"SD - {n:04d}"
    elif area == 'psicopedagogia':
        for n in range(1, 10000):
            yield f"PS - {n:04d}"
    elif area == 'desarrollo_profesional_estudiante':
        for n in range(1, 10000):
            yield f"DPE - {n:04d}"
    elif area == 'grados_titulos':
        for n in range(1, 10000):
            yield f"GT - {n:04d}"
    elif area == 'servicios_educativos':
        for n in range(1, 10000):
            yield f"SE - {n:04d}"
    elif area == 'biblioteca':
        for n in range(1, 10000):
            yield f"B - {n:04d}"
    else:
        yield f"{area} - ???"""""

""""@app.route('/generar_ticket/<area>')
def generar_ticket(area):
    if area == 'secretaria_docente':
        ticket_area = next(sd)
    elif area == 'psicopedagogia':
        ticket_area = next(ps)
    elif area == 'desarrollo_profesional_estudiante':
        ticket_area = next(dpe)
    elif area == 'grados_titulos':
        ticket_area = next(gt)
    elif area == 'servicios_educativos':
        ticket_area = next(se)
    elif area == 'biblioteca':
        ticket_area = next(b)
    else:
        return render_template('error.html', message='Área no válida')

    nuevo_ticket = Ticket(area=area, numero=ticket_area)
    basededatos.session.add(nuevo_ticket)
    basededatos.session.commit()

    return f"Ticket generado para {area}: {ticket_area}"
"""

