from apirest import api
from apirest.views import RecursoRegistro, RecursoLogin, RecursoPublicaciones, RecursoMisPublicaciones, RecursoMiPublicacion
#, RecursoTarjeta, RecursoTarjetas

api.add_resource(RecursoRegistro, '/api/auth/registro')
api.add_resource(RecursoLogin, '/api/auth/login')

# /api/reviews?limit=num_post&order=desc|asc
api.add_resource(RecursoPublicaciones, '/api/reviews')

api.add_resource(RecursoMisPublicaciones, '/api/publicaciones')
api.add_resource(RecursoMiPublicacion, '/api/publicaciones/<string:id_publicacion>')