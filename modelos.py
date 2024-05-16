from app import basededatos, gestor
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

#gracias a flask_login, permitimos cargar al usuario actual:
@gestor.user_loader
def load_user(Usuario_id):  #hemos creado una funcion que permite recoger de la base de datos
    return Usuario.query.get(Usuario_id) #el identificador de usuario y si esta logado pues cargarlo en memoria, 
#Con lo cual esto nos permite saber cual es el usuario actual o que esta logeado en nuestra aplicacion

class Usuario(basededatos.Model, UserMixin): #proporciona funcionalidades de manejo de sesiones y autenticación

    __tablename__ = 'Usuarios'
    id = basededatos.Column(basededatos.Integer, primary_key = True)
    email = basededatos.Column(basededatos.String(64), unique= True, index= True)#sea unico y la busqueda mas rapida por index
    nombre = basededatos.Column(basededatos.String(64), unique=True, index=True)
    password_encriptada = basededatos.Column(basededatos.String(200))#200 por el largo de las encriptadas

    def __init__(self, nombre, email, password):
        self.email = email
        self.nombre = nombre
        self.password_encriptada = generate_password_hash(password)

    def verificar_password(self, password):
        return check_password_hash(self.password_encriptada, password)
    
class Ticket(basededatos.Model):
    __tablename__ = 'Tickets'
    id = basededatos.Column(basededatos.Integer, primary_key=True)
    area = basededatos.Column(basededatos.String(20))
    numero = basededatos.Column(basededatos.Integer)
    usuario_id = basededatos.Column(basededatos.Integer, basededatos.ForeignKey('Usuarios.id'))

    def __init__(self, area, numero, usuario_id):
        self.area = area
        self.numero = numero
        self.usuario_id = usuario_id
    
    def __repr__(self):
        texto = f"<Ticket : {self.area} - {self.numero:02d}>"
        return texto
