
from flask import Flask, abort, request, jsonify, g, url_for, json, render_template
from socket import gethostname
from flask import Response
from flask_sqlalchemy import SQLAlchemy
from flask_httpauth import HTTPBasicAuth
from passlib.apps import custom_app_context as pwd_context
from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired)
import collections

#init
app = Flask(__name__)
app.config['SECRET_KEY'] = 'fuber iswill be the star'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True

#extension
db = SQLAlchemy(app)
auth = HTTPBasicAuth()


demands = db.Table('demands',
        db.Column('user_id', db.Integer, db.ForeignKey('users.id'), nullable=False),
        db.Column('offer_id', db.Integer, db.ForeignKey('offers.id'), nullable=False),
        db.PrimaryKeyConstraint('user_id', 'offer_id')
)


class Message(db.Model):
    __tablename__ = 'messages'
    id = db.Column(db.Integer, primary_key=True)
    type  = db.Column(db.String(4))
    text = db.Column(db.String(1024))
    date = db.Column(db.String(16))
    time  = db.Column(db.String(512))
    user_id_message = db.Column(db.Integer, db.ForeignKey('users.id'))


class Offer(db.Model):
    __tablename__ = 'offers'
    id = db.Column(db.Integer, primary_key=True)
    nombre_empresa = db.Column(db.String(64), index=True)
    descripcion = db.Column(db.String(512))
    fecha = db.Column(db.String(32))
    hora_recogida = db.Column(db.String(16))
    hora_entrega = db.Column(db.String(16))
    direccion_recogida = db.Column(db.String(128))
    direccion_entrega = db.Column(db.String(128))
    precio_hora = db.Column(db.String(8))
    tipo_vehiculo = db.Column(db.String(64))
    tipo_carga = db.Column(db.String(32))
    permiso_conducir = db.Column(db.String(12))
    recorrido_km = db.Column(db.String(12))
    metros = db.Column(db.String(12))
    telefono_recogida = db.Column(db.String(16))
    telefono_entrega = db.Column(db.String(16))
    encoded_imagen_empresa = db.Column(db.String(16000))
    asignada = db.Column(db.Boolean, default=False)
    realizada = db.Column(db.Boolean, default=False)
    user_id_asignado = db.Column(db.Integer, db.ForeignKey('users.id'))

################################################################################TABLE users
################################################################################USER MODEL
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), index=True)
    password_hash = db.Column(db.String(64))
    nombre = db.Column(db.String(32))
    apellidos = db.Column(db.String(64))
    dni = db.Column(db.String(16))
    fecha = db.Column(db.String(32))
    mail = db.Column(db.String(32))
    telefono = db.Column(db.String(16))
    cuenta = db.Column(db.String(32))
    permisos = db.Column(db.String(16))
    vehiculo = db.Column(db.String(32))
    matricula = db.Column(db.String(16))
    marca = db.Column(db.String(32))
    modelo = db.Column(db.String(32))
    tara = db.Column(db.String(8))
    plataforma = db.Column(db.String(16))
    carga = db.Column(db.String(16))
    turnos = db.Column(db.String(100))
    dias = db.Column(db.String(100))
    comunidad = db.Column(db.String(32))
    provincia = db.Column(db.String(32))
    municipio = db.Column(db.String(32))
    tipoVia = db.Column(db.String(32))
    nombreVia = db.Column(db.String(64))
    numero = db.Column(db.String(8))
    escalera = db.Column(db.String(8))
    piso = db.Column(db.String(8))
    puerta = db.Column(db.String(8))
    codigoPostal  = db.Column(db.String(8))
    disponibilidadGeo = db.Column(db.String(100))
    imagen = db.Column(db.String(16000))
    offers_pendientes = db.relationship('Offer', backref='offer')
    offers_realizadas = db.relationship('Offer', backref='offer_r')
    messages = db.relationship('Message', backref='message')
    demanded = db.relationship('Offer',
                            secondary=demands,
                            primaryjoin=(demands.c.user_id == id),
                            backref=db.backref('demands', lazy='dynamic'),
                            lazy='dynamic')

    def hash_password(self, password):
        self.password_hash = pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)

    def generate_auth_token(self, expiration=66600):
        s = Serializer(app.config['SECRET_KEY'], expires_in=expiration)
        return s.dumps({'id': self.id})

    def demand(self, offer):
        if not self.is_demanding(offer):
            self.demanded.append(offer)
            return self

    def undemand(self, offer):
        if self.is_demanding(offer):
            self.demanded.remove(offer)
            return self

    def is_demanding(self, offerr):
        return self.demanded.filter(demands.c.offer_id == offerr.id).count() > 0

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None    # valid token, but expired
        except BadSignature:
            return None    # invalid token
        user = User.query.get(data['id'])
        return user

################################################################################CREATE DATABASE
db.create_all()

##API based
@auth.verify_password
def verify_password(username_or_token, password):
    # first try to authenticate by token
    user = User.verify_auth_token(username_or_token)
    if not user:
        # try to authenticate with username/password
        user = User.query.filter_by(username=username_or_token).first()
        if not user or not user.verify_password(password):
           return False
    g.user = user
    return True

def verify_token(token):
    # first try to authenticate by token
    user = User.verify_auth_token(token)
    if not user:
        return False
    g.user = user
    return True

@app.route('/api/users', methods=['POST'])
def new_user():
    username = request.json.get('username')
    password = request.json.get('password')
    if username is None or password is None:
        abort(400)    # missing arguments
    if User.query.filter_by(username=username).first() is not None:
        abort(400)    # existing user
    user = User(username=username)
    user.hash_password(password)
    db.session.add(user)
    db.session.commit()
    return (jsonify({'username': user.username}), 201,
            {'Location': url_for('get_user', id=user.id, _external=True)})

@app.route('/api/users/<int:id>')
def get_user(id):
    user = User.query.get(id)
    if not user:
        abort(400)
    return jsonify({'username': user.username})

@app.route('/api/token')
@auth.login_required
def get_auth_token():
    token = g.user.generate_auth_token(600)
    return jsonify({'token': token.decode('ascii')})

@app.route('/api/resource')
@auth.login_required
def get_resource():
    return jsonify({'data': 'Hello, %s!' % g.user.username})

@app.route('/')
def home():
    return render_template('index.html')
    #return "Fuber is working baby"

@app.route('/index.html')
def index():
    return render_template('index.html')
    #return "Fuber is working baby"
################################################################################Private Funcs


################################################################################FUBER API

#User

#Create un nuevo usuario
@app.route('/users', methods=['POST'])
def create_user():
    """Witf form"""
    username=request.form['username']
    password=request.form['password']
    nombre=request.form['nombre']
    apellidos=request.form['apellidos']
    dni=request.form['dni']
    fecha=request.form['fecha']
    mail=request.form['mail']
    telefono=request.form['telefono']
    cuenta=request.form['cuenta']
    permisos=request.form['permisos']
    vehiculo=request.form['vehiculo']
    matricula=request.form['matricula']
    marca=request.form['marca']
    modelo=request.form['modelo']
    tara=request.form['tara']
    plataforma=request.form['plataforma']
    carga=request.form['carga']
    turnos=request.form['turnos']
    dias=request.form['dias']
    comunidad=request.form['comunidad']
    provincia=request.form['provincia']
    municipio=request.form['municipio']
    tipoVia=request.form['tipoVia']
    nombreVia=request.form['nombreVia']
    numero=request.form['numero']
    escalera=request.form['escalera']
    piso=request.form['piso']
    puerta=request.form['puerta']
    codigoPostal=request.form['codigoPostal']
    disponibilidadGeo=request.form['disponibilidadGeo']
    imagen=request.form['imagen']
    if username is None or password is None:
        abort(400)    # missing arguments
    if User.query.filter_by(username=username).first() is not None:
        abort(400)    # existing user
    if nombre is None or apellidos is None:
        abort(400)    # missing arguments
    if dni is None or fecha is None:
        abort(400)    # missing arguments
    if mail is None or telefono is None:
        abort(400)    # missing arguments
    if cuenta is None or permisos is None:
        abort(400)    # missing arguments
    if vehiculo is None or matricula is None:
        abort(400)    # missing arguments
    if marca is None or modelo is None:
        abort(400)    # missing arguments
    if tara is None or plataforma is None:
        abort(400)    # missing arguments
    if carga is None or turnos is None:
        abort(400)    # missing arguments
    if dias is None or comunidad is None:
        abort(400)    # missing arguments
    if provincia is None or municipio is None:
        abort(400)    # missing arguments
    if tipoVia is None or nombreVia is None:
        abort(400)    # missing arguments
    if numero is None or escalera is None:
        abort(400)    # missing arguments
    if piso is None or puerta is None:
        abort(400)    # missing arguments
    if codigoPostal is None or disponibilidadGeo is None:
        abort(400)    # missing arguments
    user = User(username=username,
                nombre=nombre,
                apellidos=apellidos,
                dni=dni,
                fecha=fecha,
                mail=mail,
                telefono=telefono,
                cuenta=cuenta,
                permisos=permisos,
                vehiculo=vehiculo,
                matricula=matricula,
                marca=marca,
                modelo=modelo,
                tara=tara,
                plataforma=plataforma,
                carga=carga,
                turnos=turnos,
                dias=dias,
                comunidad=comunidad,
                provincia=provincia,
                municipio=municipio,
                tipoVia=tipoVia,
                nombreVia=nombreVia,
                numero=numero,
                escalera=escalera,
                piso=piso,
                puerta=puerta,
                codigoPostal=codigoPostal,
                disponibilidadGeo=disponibilidadGeo,
                imagen=imagen)
    user.hash_password(password)
    db.session.add(user)
    db.session.commit()
    if verify_password(username, password):
        token = g.user.generate_auth_token(66600)
        return (jsonify({'token': token.decode('ascii')}), 201)
    #return (jsonify({'username': user.username}), 201)
    return abort(400)




#info de todos los usuarios
@app.route('/users', methods=['GET'])
def get_info_users():
    users = User.query.all()
    rowarray_list = []
    for user in users:
        d = collections.OrderedDict()
        d['id'] = user.id
        d['username'] = user.username
        d['nombre'] = user.nombre
        d['apellidos'] = user.apellidos
        d['dni'] = user.dni
        d['fecha'] = user.fecha
        d['mail'] = user.mail
        d['telefono'] = user.telefono
        d['cuenta'] = user.cuenta
        d['permisos'] = user.permisos
        d['vehiculo'] = user.vehiculo
        d['matricula'] = user.matricula
        d['marca'] = user.marca
        d['modelo'] = user.modelo
        d['tara'] = user.tara
        d['plataforma'] = user.plataforma
        d['carga'] = user.carga
        d['turnos'] = user.turnos
        d['dias'] = user.dias
        d['comunidad'] = user.comunidad
        d['provincia'] = user.provincia
        d['municipio'] = user.municipio
        d['tipoVia'] = user.tipoVia
        d['nombreVia'] = user.nombreVia
        d['numero'] = user.numero
        d['escalera'] = user.escalera
        d['piso'] = user.piso
        d['puerta'] = user.puerta
        d['codigoPostal'] = user.codigoPostal
        d['disponibilidadGeo'] = user.disponibilidadGeo
        d['imagen'] = user.imagen
        rowarray_list.append(d)
    j = json.dumps(rowarray_list)
    resp = Response(j, status=200, mimetype='application/json')
    resp.headers['Link'] = 'http://fuber.pythonanywhere.com'
    return resp



#info de un usuario by
@app.route('/users/<int:id>', methods=['GET'])
def get_user_info(id):
    token = request.headers.get('token')
    is_real = verify_token(token)
    if is_real:
        user = User.query.get(id)
        if not user:
            abort(400)
        d = collections.OrderedDict()
        d['id'] = user.id
        d['username'] = user.username
        d['nombre'] = user.nombre
        d['apellidos'] = user.apellidos
        d['dni'] = user.dni
        d['fecha'] = user.fecha
        d['mail'] = user.mail
        d['telefono'] = user.telefono
        d['cuenta'] = user.cuenta
        d['permisos'] = user.permisos
        d['vehiculo'] = user.vehiculo
        d['matricula'] = user.matricula
        d['marca'] = user.marca
        d['modelo'] = user.modelo
        d['tara'] = user.tara
        d['plataforma'] = user.plataforma
        d['carga'] = user.carga
        d['turnos'] = user.turnos
        d['dias'] = user.dias
        d['comunidad'] = user.comunidad
        d['provincia'] = user.provincia
        d['municipio'] = user.municipio
        d['tipoVia'] = user.tipoVia
        d['nombreVia'] = user.nombreVia
        d['numero'] = user.numero
        d['escalera'] = user.escalera
        d['piso'] = user.piso
        d['puerta'] = user.puerta
        d['codigoPostal'] = user.codigoPostal
        d['disponibilidadGeo'] = user.disponibilidadGeo
        d['imagen'] = user.imagen
        j = json.dumps(d)
        resp = Response(j, status=200, mimetype='application/json')
        resp.headers['Link'] = 'http://fuber.pythonanywhere.com'
        return resp
    return abort(400)



#informa si existe el usuario en la bd
@app.route('/users/validate', methods=['GET'])
def validate_user():
    username_=request.args.get('username')
    mail_=request.args.get('mail')
    user = User.query.filter_by(username=username_).first()
    if not user:
        user = User.query.filter_by(mail=mail_).first()
        if not user:
            return (jsonify({'noexist': 'True'}), 200)
    return (jsonify({'noexist': 'False'}), 200)



#Update info del usuario con nueva info
@app.route('/users/<int:id>', methods=['PUT'])
def update_user(id):
    token = request.headers.get('token')
    is_real = verify_token(token)
    if is_real:
        user = User.query.get(id)
        if not user:
            abort(400)
        user.username=request.form['username']
        password=request.form['password']
        user.nombre=request.form['nombre']
        user.apellidos=request.form['apellidos']
        user.dni=request.form['dni']
        user.fecha=request.form['fecha']
        user.mail=request.form['mail']
        user.telefono=request.form['telefono']
        user.cuenta=request.form['cuenta']
        user.permisos=request.form['permisos']
        user.vehiculo=request.form['vehiculo']
        user.matricula=request.form['matricula']
        user.marca=request.form['marca']
        user.modelo=request.form['modelo']
        user.tara=request.form['tara']
        user.plataforma=request.form['plataforma']
        user.carga=request.form['carga']
        user.turnos=request.form['turnos']
        user.dias=request.form['dias']
        user.comunidad=request.form['comunidad']
        user.provincia=request.form['provincia']
        user.municipio=request.form['municipio']
        user.tipoVia=request.form['tipoVia']
        user.nombreVia=request.form['nombreVia']
        user.numero=request.form['numero']
        user.escalera=request.form['escalera']
        user.piso=request.form['piso']
        user.puerta=request.form['puerta']
        user.codigoPostal=request.form['codigoPostal']
        user.disponibilidadGeo=request.form['disponibilidadGeo']
        user.imagen=request.form['imagen']
        if password:
            user.hash_password(password)
        db.session.commit()
        return (jsonify({'username': user.username}), 200)
    return abort(400)


#login del usuario
@app.route('/login', methods=['POST'])
def login_get_auth_token():
    username=request.form['username']
    password=request.form['password']
    if verify_password(username, password):
        token = g.user.generate_auth_token(66600)
        return jsonify({'token': token.decode('ascii')})
    return abort(401)



#Clear Database
@app.route('/cleardatabase', methods=['GET'])
def clear_db():
    db.session.commit()
    db.drop_all()
    db.create_all()
    db.session.commit()
    return json.dumps({'success':True}), 200, {'ContentType':'application/json'}



#crea una oferta
@app.route('/ofertas', methods=['POST'])
def create_oferta():
    nombre_empresa = request.form['nombre_empresa']
    descripcion = request.form['descripcion']
    fecha = request.form['fecha']
    hora_recogida = request.form['hora_recogida']
    hora_entrega = request.form['hora_entrega']
    direccion_recogida = request.form['direccion_recogida']
    direccion_entrega = request.form['direccion_entrega']
    precio_hora = request.form['precio_hora']
    tipo_vehiculo = request.form['tipo_vehiculo']
    tipo_carga = request.form['tipo_carga']
    permiso_conducir = request.form['permiso_conducir']
    recorrido_km = request.form['recorrido_km']
    metros = request.form['metros']
    telefono_recogida = request.form['telefono_recogida']
    telefono_entrega = request.form['telefono_entrega']
    encoded_imagen_empresa = request.form['encoded_imagen_empresa']
    if nombre_empresa is None or descripcion is None:
        abort(400)    # missing arguments
    if fecha is None or hora_recogida is None:
        abort(400)    # missing arguments
    if hora_entrega is None:
        abort(400)    # missing arguments
    if direccion_recogida is None or direccion_entrega is None:
        abort(400)    # missing arguments
    if precio_hora is None or tipo_vehiculo is None:
        abort(400)    # missing arguments
    if tipo_carga is None or permiso_conducir is None:
        abort(400)    # missing arguments
    if recorrido_km is None or metros is None:
        abort(400)    # missing arguments
    if telefono_recogida is None or telefono_entrega is None:
        abort(400)    # missing arguments

    oferta = Offer(
                nombre_empresa = nombre_empresa,
                descripcion = descripcion,
                fecha = fecha,
                hora_recogida = hora_recogida,
                hora_entrega = hora_entrega,
                direccion_recogida = direccion_recogida,
                direccion_entrega = direccion_entrega,
                precio_hora = precio_hora,
                tipo_vehiculo = tipo_vehiculo,
                tipo_carga = tipo_carga,
                permiso_conducir = permiso_conducir,
                recorrido_km = recorrido_km,
                metros = metros,
                telefono_recogida = telefono_recogida,
                telefono_entrega = telefono_entrega,
                encoded_imagen_empresa = encoded_imagen_empresa
            )
    db.session.add(oferta)
    db.session.commit()
    return (jsonify({'oferta': oferta.nombre_empresa}), 201)



@app.route('/ofertas', methods=['GET'])
def get_ofertas():
    offers = Offer.query.all()
    rowarray_list = []
    for offer in offers:
        d = collections.OrderedDict()
        d['id'] = offer.id
        d['nombre_empresa'] = offer.nombre_empresa
        d['descripcion'] = offer.descripcion
        d['fecha'] = offer.fecha
        d['hora_recogida'] = offer.hora_recogida
        d['hora_entrega'] = offer.hora_entrega
        d['direccion_recogida'] = offer.direccion_recogida
        d['direccion_entrega'] = offer.direccion_entrega
        d['precio_hora'] = offer.precio_hora
        d['tipo_vehiculo'] = offer.tipo_vehiculo
        d['tipo_carga'] = offer.tipo_carga
        d['permiso_conducir'] = offer.permiso_conducir
        d['recorrido_km'] = offer.recorrido_km
        d['metros'] = offer.metros
        d['telefono_recogida'] = offer.telefono_recogida
        d['telefono_entrega'] = offer.telefono_entrega
        d['encoded_imagen_empresa'] = offer.encoded_imagen_empresa
        #d['asignada'] = offer.asignada
        #d['realizada'] = offer.realizada
        #d['user_id_asignado'] = offer.user_id_asignado
        rowarray_list.append(d)
    j = json.dumps(rowarray_list)
    resp = Response(j, status=200, mimetype='application/json')
    resp.headers['Link'] = 'http://fuber.pythonanywhere.com'
    return resp



@app.route('/ofertas/disponibles', methods=['GET'])
def get_ofertas_disponibles():
    offers = Offer.query.filter_by(asignada=False).all()
    rowarray_list = []
    for offer in offers:
        d = collections.OrderedDict()
        d['id'] = offer.id
        d['nombre_empresa'] = offer.nombre_empresa
        d['descripcion'] = offer.descripcion
        d['fecha'] = offer.fecha
        d['hora_recogida'] = offer.hora_recogida
        d['hora_entrega'] = offer.hora_entrega
        d['direccion_recogida'] = offer.direccion_recogida
        d['direccion_entrega'] = offer.direccion_entrega
        d['precio_hora'] = offer.precio_hora
        d['tipo_vehiculo'] = offer.tipo_vehiculo
        d['tipo_carga'] = offer.tipo_carga
        d['permiso_conducir'] = offer.permiso_conducir
        d['recorrido_km'] = offer.recorrido_km
        d['metros'] = offer.metros
        d['telefono_recogida'] = offer.telefono_recogida
        d['telefono_entrega'] = offer.telefono_entrega
        d['encoded_imagen_empresa'] = offer.encoded_imagen_empresa
        #d['asignada'] = offer.asignada
        #d['realizada'] = offer.realizada
        #d['user_id_asignado'] = offer.user_id_asignado
        rowarray_list.append(d)
    j = json.dumps(rowarray_list)
    resp = Response(j, status=200, mimetype='application/json')
    resp.headers['Link'] = 'http://fuber.pythonanywhere.com'
    return resp




#info de una oferta by id
@app.route('/ofertas/<int:id>', methods=['GET'])
def get_ofertas_id(id):
    offer = Offer.query.get(id)
    if not offer:
        abort(400)
    d = collections.OrderedDict()
    d['id'] = offer.id
    d['nombre_empresa'] = offer.nombre_empresa
    d['descripcion'] = offer.descripcion
    d['fecha'] = offer.fecha
    d['hora_recogida'] = offer.hora_recogida
    d['hora_entrega'] = offer.hora_entrega
    d['direccion_recogida'] = offer.direccion_recogida
    d['direccion_entrega'] = offer.direccion_entrega
    d['precio_hora'] = offer.precio_hora
    d['tipo_vehiculo'] = offer.tipo_vehiculo
    d['tipo_carga'] = offer.tipo_carga
    d['permiso_conducir'] = offer.permiso_conducir
    d['recorrido_km'] = offer.recorrido_km
    d['metros'] = offer.metros
    d['telefono_recogida'] = offer.telefono_recogida
    d['telefono_entrega'] = offer.telefono_entrega
    d['encoded_imagen_empresa'] = offer.encoded_imagen_empresa
    #d['asignada'] = offer.asignada
    #d['realizada'] = offer.realizada
    #d['user_id_asignado'] = offer.user_id_asignado
    j = json.dumps(d)
    resp = Response(j, status=200, mimetype='application/json')
    resp.headers['Link'] = 'http://fuber.pythonanywhere.com'
    return resp



#Update la oferta by id
@app.route('/ofertas/<int:id>', methods=['PUT'])
def upate_oferta_id(id):
    offer = Offer.query.get(id)
    if not offer:
        abort(400)
    offer.nombre_empresa = request.form['nombre_empresa']
    offer.descripcion = request.form['descripcion']
    offer.fecha = request.form['fecha']
    offer.hora_recogida = request.form['hora_recogida']
    offer.hora_entrega = request.form['hora_entrega']
    offer.direccion_recogida = request.form['direccion_recogida']
    offer.direccion_entrega = request.form['direccion_entrega']
    offer.precio_hora = request.form['precio_hora']
    offer.tipo_vehiculo = request.form['tipo_vehiculo']
    offer.tipo_carga = request.form['tipo_carga']
    offer.permiso_conducir = request.form['permiso_conducir']
    offer.recorrido_km = request.form['recorrido_km']
    offer.metros = request.form['metros']
    offer.telefono_recogida = request.form['telefono_recogida']
    offer.telefono_entrega = request.form['telefono_entrega']
    offer.encoded_imagen_empresa = request.form['encoded_imagen_empresa']
    db.session.commit()
    return (jsonify({'nombre_empresa': offer.nombre_empresa}), 200)



#user solicita empleo con oferta id
@app.route('/ofertas/<int:id>/solicitar', methods=['PUT'])
def solicitar_oferta_id(id):
    token = request.headers.get('token')
    is_real = verify_token(token)
    if is_real:
        user = User.query.get(request.form['user_id'])
        if not user:
            abort(400)
        offer = Offer.query.get(id)
        if not offer:
            abort(400)
        u = user.demand(offer)
        db.session.add(u)
        db.session.commit()
        return (jsonify({'user_id':user.id,'oferta_id':offer.id}), 200)
    return abort(400)


#info o solo id, de todos los usuarios que quieran la oferta ofrecida
@app.route('/ofertas/<int:id>/solicitar', methods=['GET'])
def solicitar_info_oferta_id(id):
    offer = Offer.query.get(id)
    if not offer:
        abort(400)
    users = User.query.filter(Offer.id==offer.id).all()
    rowarray_list = []
    for user in users:
        d = collections.OrderedDict()
        d['id'] = user.id
        d['username'] = user.username
        d['nombre'] = user.nombre
        d['apellidos'] = user.apellidos
        d['dni'] = user.dni
        d['fecha'] = user.fecha
        d['mail'] = user.mail
        d['telefono'] = user.telefono
        d['cuenta'] = user.cuenta
        d['permisos'] = user.permisos
        d['vehiculo'] = user.vehiculo
        d['matricula'] = user.matricula
        d['marca'] = user.marca
        d['modelo'] = user.modelo
        d['tara'] = user.tara
        d['plataforma'] = user.plataforma
        d['carga'] = user.carga
        d['turnos'] = user.turnos
        d['dias'] = user.dias
        d['comunidad'] = user.comunidad
        d['provincia'] = user.provincia
        d['municipio'] = user.municipio
        d['tipoVia'] = user.tipoVia
        d['nombreVia'] = user.nombreVia
        d['numero'] = user.numero
        d['escalera'] = user.escalera
        d['piso'] = user.piso
        d['puerta'] = user.puerta
        d['codigoPostal'] = user.codigoPostal
        d['disponibilidadGeo'] = user.disponibilidadGeo
        d['imagen'] = user.imagen
        rowarray_list.append(d)
    j = json.dumps(rowarray_list)
    resp = Response(j, status=200, mimetype='application/json')
    resp.headers['Link'] = 'http://fuber.pythonanywhere.com'
    return resp



#oferta asignada. asigna oferta(id) a user_id
@app.route('/ofertas/<int:id>/pendientes', methods=['PUT'])
def asignar_oferta(id):
    user = User.query.get(request.form['user_id'])
    if not user:
        abort(400)
    offer = Offer.query.get(id)
    if not offer:
        abort(400)
    offer.asignada = True
    offer.user_id_asignado = user.id
    db.session.commit()
    user.offers_pendientes.append(offer)
    db.session.commit()
    return (jsonify({'user_id':user.id,'oferta_id':offer.id}), 200)



#oferta realizada. Marca como realizada una oferta(id) por un user_is
@app.route('/ofertas/<int:id>/realizadas', methods=['PUT'])
def finalizar_oferta(id):
    user = User.query.get(request.form['user_id'])
    if not user:
        abort(400)
    offer = Offer.query.get(id)
    if not offer:
        abort(400)
    offer.realizada = True
    db.session.commit()
    user.offers_pendientes.remove(offer)
    user.offers_realizadas.append(offer)
    db.session.add(user)
    db.session.commit()
    return (jsonify({'user_id':user.id,'oferta_id':offer.id}), 200)



#info de las ofertas/pedidos que ha realizado dado su id
@app.route('/users/<int:id>/realizadas', methods=['GET'])
def get_user_realizadas(id):
    token = request.headers.get('token')
    is_real = verify_token(token)
    if is_real:
        user = User.query.get(id)
        if not user:
            abort(400)
        offers = user.offers_realizadas
        #print (offers)
        rowarray_list = []
        for offer in offers:
            d = collections.OrderedDict()
            d['id'] = offer.id
            d['nombre_empresa'] = offer.nombre_empresa
            d['descripcion'] = offer.descripcion
            d['fecha'] = offer.fecha
            d['hora_recogida'] = offer.hora_recogida
            d['hora_entrega'] = offer.hora_entrega
            d['direccion_recogida'] = offer.direccion_recogida
            d['direccion_entrega'] = offer.direccion_entrega
            d['precio_hora'] = offer.precio_hora
            d['tipo_vehiculo'] = offer.tipo_vehiculo
            d['tipo_carga'] = offer.tipo_carga
            d['permiso_conducir'] = offer.permiso_conducir
            d['recorrido_km'] = offer.recorrido_km
            d['metros'] = offer.metros
            d['telefono_recogida'] = offer.telefono_recogida
            d['telefono_entrega'] = offer.telefono_entrega
            d['encoded_imagen_empresa'] = offer.encoded_imagen_empresa
            rowarray_list.append(d)
        j = json.dumps(rowarray_list)
        resp = Response(j, status=200, mimetype='application/json')
        resp.headers['Link'] = 'http://fuber.pythonanywhere.com'
        return resp
    return abort(400)


#info de las ofertas/pedidos que  tiene pendientes dado su id
@app.route('/users/<int:id>/pendientes', methods=['GET'])
def get_user_pendientes(id):
    user = User.query.get(id)
    if not user:
        abort(400)
    offers = user.offers_pendientes
    #print (offers)
    rowarray_list = []
    for offer in offers:
        d = collections.OrderedDict()
        d['id'] = offer.id
        d['nombre_empresa'] = offer.nombre_empresa
        d['descripcion'] = offer.descripcion
        d['fecha'] = offer.fecha
        d['hora_recogida'] = offer.hora_recogida
        d['hora_entrega'] = offer.hora_entrega
        d['direccion_recogida'] = offer.direccion_recogida
        d['direccion_entrega'] = offer.direccion_entrega
        d['precio_hora'] = offer.precio_hora
        d['tipo_vehiculo'] = offer.tipo_vehiculo
        d['tipo_carga'] = offer.tipo_carga
        d['permiso_conducir'] = offer.permiso_conducir
        d['recorrido_km'] = offer.recorrido_km
        d['metros'] = offer.metros
        d['telefono_recogida'] = offer.telefono_recogida
        d['telefono_entrega'] = offer.telefono_entrega
        d['encoded_imagen_empresa'] = offer.encoded_imagen_empresa
        rowarray_list.append(d)
    j = json.dumps(rowarray_list)
    resp = Response(j, status=200, mimetype='application/json')
    resp.headers['Link'] = 'http://fuber.pythonanywhere.com'
    return resp



#Return user.id by token
@app.route('/me', methods=['GET'])
def get_user_me():
    token = request.headers.get('token')
    is_real = verify_token(token)
    if is_real:
        return (jsonify({'user_id':g.user.id}), 200)
    return abort(400)



#enviar mensaje a fuber
@app.route('/users/<int:id>/mensajes', methods=['POST'])
def mensaje_to_fuber(id):
    type_ = request.form['type']
    if type_ == 1:
        token = request.headers.get('token')
        is_real = verify_token(token)
        if is_real:
            user = User.query.get(id)
    else: user = User.query.get(id)
    if not user:
        abort(400)
    text_ = request.form['text']
    date_ = request.form['date']
    time_ = request.form['time']
    message = Message(
                    type=type_,
                    text=text_,
                    date=date_,
                    time=time_,
                    user_id_message=user.id)
    db.session.add(message)
    db.session.commit()
    user.messages.append(message)
    db.session.commit()
    return (jsonify({'message.id':message.id}), 200)



#info de todos los mensajes de fuber con usuario by id
@app.route('/users/<int:id>/mensajes', methods=['GET'])
def get_mansajes_id(id):
    user = User.query.get(id)
    if not user:
        abort(400)
    messages = user.messages
    rowarray_list = []
    for mess in messages:
        d = collections.OrderedDict()
        #d['id'] = mess.id
        d['type'] = mess.type
        d['text'] = mess.text
        d['date'] = mess.date
        d['time'] = mess.time
        #d['user_id_message'] = mess.user_id_message
        rowarray_list.append(d)
    j = json.dumps(rowarray_list)
    resp = Response(j, status=200, mimetype='application/json')
    resp.headers['Link'] = 'http://fuber.pythonanywhere.com'
    return resp



if __name__ == '__main__':
    db.create_all()
    if 'liveconsole' not in gethostname():
        app.run(debug=True)