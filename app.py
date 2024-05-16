import os #proporciona una manera de utilizar funcionalidades dependientes del sistema operativo.
from flask import Flask
from flask_sqlalchemy import SQLAlchemy #es una biblioteca de asignación objeto-relacional (ORM) para Python
from flask_migrate import Migrate #Flask-Migrate es una extensión que maneja las migraciones de bases de datos SQLAlchemy para aplicaciones Flask
from flask_login import LoginManager


gestor = LoginManager() #instancia de login manager, esto se utilizará para gestionar las sesiones de usuario y la funcionalidad de inicio de sesión.
app = Flask(__name__)  #instaciamos la app con el argumento __name__, esta se establece con el modulo python en el que estamos

app.config['SECRET_KEY'] = 'paulruizclave1' #configuramos por tema de formularios de login, es decir La clave secreta se utiliza para firmar de manera segura las cookies de sesión y otras funcionalidades relacionadas con la seguridad.

directorio = os.path.abspath(os.path.dirname(__file__))

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(directorio, 'datos.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False #Desactiva el seguimiento de modificaciones de Flask-SQLAlchemy, ya que puede ser una fuente de sobrecarga y no es necesario para el app.

basededatos = SQLAlchemy(app) #conectamos la aplicacion con la base de datos
Migrate(app, basededatos)  #nos permitira en caso de hacer un cambio en el modelo de las tablas poder migrarlo para seguir utilizando la misma tablas. 

gestor.init_app(app) #Inicializa la extensión Flask-Login, asociándola con la nuestra app Flask.
gestor.login_view = 'login' #Establece la vista de la función que maneja las solicitudes de inicio de sesión. En este caso, la función de vista se llama 'login'.

#teoria de colas
#pronostica a quien se va liberar
#dividir capas: tenga aplicacion en front end objetos y base de datos.
#diferentes servidores