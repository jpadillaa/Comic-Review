import os
from datetime import timedelta
from flask import request, current_app, send_from_directory
from werkzeug.utils import secure_filename
from flask_restful import Resource, reqparse
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, JWTManager
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
            access_token = create_access_token(identity = request.json['email'], expires_delta = timedelta(days = 1))
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
    @jwt_required()
    def get(self):        
        email = get_jwt_identity()        
        publicaciones = Publicacion.query.filter_by(admin_publicacion = email).order_by(db.desc(Publicacion.id)).all()
        return publicaciones_schema.dump(publicaciones)    
    
    @jwt_required()
    def post(self):
        email = get_jwt_identity()
        
        nueva_publicacion = Publicacion(
            capitulo = request.json['capitulo'],
            fecha_publicacion = request.json['fecha_publicacion'],
            titulo = request.json['titulo'],
            autor = request.json['autor'],
            categoria = request.json['categoria'],
            descripcion = request.json['descripcion'],
            review = request.json['review'],
            idioma = request.json['idioma'],
            instagram = request.json['instagram'],                
            admin_publicacion = email
            )
        db.session.add(nueva_publicacion)
        db.session.commit()
        
        return publicacion_schema.dump(nueva_publicacion)

'''
Recurso que administra el servicio de una publicación (Detail)
'''
class RecursoMiPublicacion(Resource):
    @jwt_required()
    def get(self, id_publicacion):
        email = get_jwt_identity()
        publicacion = Publicacion.query.get_or_404(id_publicacion)

        if publicacion.admin_publicacion != email:
            return {'message':'No tiene acceso a esta publicación'}, 401
        else:
            return publicacion_schema.dump(publicacion)

    @jwt_required()
    def put(self, id_publicacion):
        email = get_jwt_identity()
        publicacion = Publicacion.query.get_or_404(id_publicacion)        
        
        if publicacion.admin_publicacion != email:
            return {'message':'No tiene acceso a este concurso'}, 401

        if 'capitulo' in request.json:
            publicacion.capitulo = request.json['capitulo']
        
        if 'fecha_publicacion' in request.json:
            publicacion.fecha_publicacion = request.json['fecha_publicacion']

        if 'titulo' in request.json:
            publicacion.fechaFin = request.json['titulo']

        if 'autor' in request.json:
            publicacion.costo = request.json['autor']

        if 'categoria' in request.json:
            publicacion.guion = request.json['categoria']

        if 'descripcion' in request.json:
            publicacion.descripcion = request.json['descripcion']

        if 'review' in request.json:
            publicacion.review = request.json['review']

        if 'idioma' in request.json:
            publicacion.idioma = request.json['idioma']

        if 'instagram' in request.json:
            publicacion.instagram = request.json['instagram']

        db.session.commit()
        return publicacion_schema.dump(publicacion)

    @jwt_required()
    def delete(self, id_publicacion):
        email = get_jwt_identity()
        publicacion = Publicacion.query.get_or_404(id_publicacion)
        
        if publicacion.admin_publicacion != email:
            return {'message':'No tiene acceso a esta publicación'}, 401
        
        db.session.delete(publicacion)
        db.session.commit()        
        return '', 204
        