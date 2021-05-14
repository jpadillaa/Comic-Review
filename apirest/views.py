import os
from datetime import timedelta
from flask import request, current_app, send_from_directory
from werkzeug.utils import secure_filename
from flask_restful import Resource, reqparse
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from flask_restful import Api

from apirest import api, db
from apirest.models import Admin, Publicacion, admin_schema, publicacion_schema, publicaciones_schema

'''
Recurso que administra el servicio de login
'''
class RecursoLogin(Resource):
    def post(self):
        request.get_json(force=True)
        usuario = Admin.query.get(request.json['email'])
        if usuario is None:
            return {'message':'El email ingresado no está registrado'}, 400
        if not usuario.verificar_clave(request.json['password']):
            return {'message': 'Contraseña incorrecta'}, 400
        try:
            access_token = create_access_token(identity = request.json['email'], expires_delta = timedelta(days = 1))
            return {
                'message':'Sesion iniciada',
                'access_token':access_token
            }
        except:
            return {'message':'Ha ocurrido un error'}, 500
    
'''
Recurso que administra el servicio de registro
'''
class RecursoRegistro(Resource):
    def post(self):
        if Admin.query.filter_by(email=request.json['email']).first() is not None:
            return {'message': f'El correo({request.json["email"]}) ya está registrado'}, 400
        if request.json['email'] == '' or request.json['password'] == '' or request.json['nombres'] == '' or request.json['apellidos'] == '':
            return {'message': 'Campos invalidos'}, 400
        nuevo_admin = Admin(
            email = request.json['email'],
            password = request.json['password'],
            nombres = request.json['nombres'],
            apellidos = request.json['apellidos']
        )
        nuevo_admin.hashear_clave()

        try:
            db.session.add(nuevo_admin)
            db.session.commit()
            access_token = create_access_token(identity = request.json['email'], expires_delta=timedelta(days=1))
            return {
                'message': f'El correo {request.json["email"]} ha sido registrado',
                'access_token': access_token 
            }
        except:
            return {'message':'Ha ocurrido un error'}, 500

'''
Recurso que lista todas las publicaciones de los usuarios
'''
class RecursoPublicaciones(Resource):
    def get(self):        
        parser = reqparse.RequestParser()
        parser.add_argument('limit', type = int, help='Limit cannot be converted')
        parser.add_argument('order')
        args = parser.parse_args()
        
        if args['order'] == 'desc':
            publicaciones = Publicacion.query.order_by(db.desc(Publicacion.id)).limit(args['limit']).all()
        else:
            publicaciones = Publicacion.query.order_by(db.asc(Publicacion.id)).limit(args['limit']).all()
        
        return publicaciones_schema.dump(publicaciones)    

'''
Recurso que administra el servicio de todas las publicaciones de un usuario
'''
class RecursoMisPublicaciones(Resource):
    # @jwt_required
    def get(self):        
        #email = get_jwt_identity()
        email = "unemail@gmail.com"
        publicaciones = Publicacion.query.filter_by(admin_publicacion = email).order_by(db.desc(Publicacion.id)).all()
        return publicaciones_schema.dump(publicaciones)    
    
    #@jwt_required
    def post(self):
        #email = get_jwt_identity()
        email = "unemail@gmail.com"
        
        nueva_publicacion = Publicacion(
            capitulo = request.form['capitulo'],
            #fecha_publicacion = request.form['fecha_publicacion'],
            titulo = request.form['titulo'],
            autor = request.form['autor'],
            categoria = request.form['categoria'],
            descripcion = request.form['descripcion'],
            review = request.form['review'],
            idioma = request.form['idioma'],
            instagram = request.form['instagram'],                
            admin_publicacion = email
            )
        db.session.add(nueva_publicacion)
        db.session.commit()
        
        return publicacion_schema.dump(nueva_publicacion)

'''
Recurso que administra el servicio de una publicación (Detail)
'''
class RecursoMiPublicacion(Resource):
    #@jwt_required
    def get(self, id_publicacion):
        #email = get_jwt_identity()
        email = "unemail@gmail.com"
        publicacion = Publicacion.query.get_or_404(id_publicacion)

        if publicacion.admin_publicacion != email:
            return {'message':'No tiene acceso a esta publicación'}, 401
        else:
            return publicacion_schema.dump(publicacion)

    #@jwt_required
    def put(self, id_publicacion):
        #email = get_jwt_identity()
        email = "unemail@gmail.com"
        publicacion = Publicacion.query.get_or_404(id_publicacion)        
        
        if publicacion.admin_publicacion != email:
            return {'message':'No tiene acceso a este concurso'}, 401

        if 'capitulo' in request.form:
            publicacion.capitulo = request.form['capitulo']
        
        #if 'fecha_publicacion' in request.form:
        #    concurso.fechaInicio = request.form['fecha_publicacion']

        if 'titulo' in request.form:
            publicacion.fechaFin = request.form['titulo']

        if 'autor' in request.form:
            publicacion.costo = request.form['autor']

        if 'categoria' in request.form:
            publicacion.guion = request.form['categoria']

        if 'descripcion' in request.form:
            publicacion.descripcion = request.form['descripcion']

        if 'review' in request.form:
            publicacion.review = request.form['review']

        if 'idioma' in request.form:
            publicacion.idioma = request.form['idioma']

        if 'instagram' in request.form:
            publicacion.instagram = request.form['instagram']

        db.session.commit()
        return publicacion_schema.dump(publicacion)

    #@jwt_required
    def delete(self, id_publicacion):
        #email = get_jwt_identity()
        email = "unemail@gmail.com"
        publicacion = Publicacion.query.get_or_404(id_publicacion)
        
        if publicacion.admin_publicacion != email:
            return {'message':'No tiene acceso a esta publicación'}, 401
        
        db.session.delete(publicacion)
        db.session.commit()        
        return '', 204
        