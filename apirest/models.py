import enum
from werkzeug.security import generate_password_hash, check_password_hash
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, date
from apirest import ma, db

class IdiomaCategoria(str, enum.Enum):
    EN = "Inglés"
    ES = "Español"
    JP = "Japones"

'''
Modelos
'''
class Admin(db.Model):
    nombres = db.Column(db.String(200))
    apellidos = db.Column(db.String(200))
    email = db.Column(db.String(100), primary_key = True)
    password = db.Column(db.String(100))
    comic = db.relationship('Publicacion', backref = 'admin', lazy = True)

    def hashear_clave(self):
        '''
        Hashea la clave en la base de datos
        '''
        self.password = generate_password_hash(self.password, 'sha256')

    def verificar_clave(self, clave):
        '''
        Verifica la clave hasheada con la del parámetro
        '''
        return check_password_hash(self.password, clave)

class Publicacion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    capitulo = db.Column(db.String(100))
    fecha_publicacion = db.Column(db.DateTime(), default = datetime.now)
    titulo = db.Column(db.String(100))
    autor = db.Column(db.String(100))
    categoria = db.Column(db.String(100))
    descripcion = db.Column(db.String(280))
    review = db.Column(db.String(280))
    idioma = db.Column(db.Enum(IdiomaCategoria))
    instagram = db.Column(db.String(200))
    admin_publicacion = db.Column(db.String(100), db.ForeignKey('admin.email'), nullable = False)

'''
Schemas
'''
class AdminSchema(ma.Schema):
    '''
    Representa el schema de un admin
    '''
    class Meta:
        fields = ("nombres", "apellidos", "email", "password")

class PublicacionSchema(ma.Schema):
    '''
    Representa el schema de un concurso
    '''
    class Meta:
        fields = ("id", "capitulo", "fecha_publicacion", "titulo", "autor", "categoria", "descripcion", "review", "idioma", "instagram")

admin_schema = AdminSchema()
publicacion_schema = PublicacionSchema()
publicaciones_schema = PublicacionSchema(many = True)
