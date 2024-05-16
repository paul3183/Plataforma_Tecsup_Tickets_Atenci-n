#formulario de registro y de login:
from modelos import Usuario
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField #importamos campos de tipo
from wtforms.validators import DataRequired, Email, EqualTo #para obligar que tenga datos, que sea email, comparar si son iguales
from wtforms import ValidationError

class Formulario_Registro(FlaskForm): #hereda de la clase FlaskForm
    email = StringField('Correo Electrónico', validators=[DataRequired(), Email()]) #primer campo de tipo string el label es Email
    nombre = StringField('Nombre', validators=[DataRequired()]) #la etiqueta es 'Nombre'
    password = PasswordField('Contraseña', validators = [DataRequired(),EqualTo('password_repetida', message='Las password no coinciden') ])
    password_repetida = PasswordField('Confirma tu contraseña', validators=[DataRequired()])
    boton = SubmitField('Registrar')

    def verificar_email(self, parametro):
        if Usuario.query.filter_by(email = parametro.data).first(): #si el dato del parametro, el valor con data, es igual mandamos un error:
            raise ValidationError('Error, este email ya ha sido utilizado , prueba con otro')

    def verificar_nombre(self, parametro):
        if Usuario.query.filter_by(nombre = parametro.data).first():
            raise ValidationError('Error, este nombre ya ha sido utilizado, prueba con otro')

class Formulario_Login(FlaskForm):
     email = StringField('Correo Electrónico', validators=[DataRequired(), Email()])
     password = PasswordField('Contraseña', validators = [DataRequired()])
     boton = SubmitField('Entrar')    