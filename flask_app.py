
from flask import Flask, abort, request, jsonify, g, url_for
from socket import gethostname
from flask_sqlalchemy import SQLAlchemy
from flask_httpauth import HTTPBasicAuth
from passlib.apps import custom_app_context as pwd_context
from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired)

#init
app = Flask(__name__)
app.config['SECRET_KEY'] = 'fuber iswill be the star'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True

#extension
db = SQLAlchemy(app)
auth = HTTPBasicAuth()

####################### - TABLE users -###############################
####################### - USER-MODEL  -###############################
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
    imagen = db.Column(db.String(2048))


    def hash_password(self, password):
        self.password_hash = pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)

    def generate_auth_token(self, expiration=600):
        s = Serializer(app.config['SECRET_KEY'], expires_in=expiration)
        return s.dumps({'id': self.id})

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
######### USER - end.############################

db.create_all()


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
    return jsonify({'token': token.decode('ascii'), 'duration': 600})


@app.route('/api/resource')
@auth.login_required
def get_resource():
    return jsonify({'data': 'Hello, %s!' % g.user.username})

@app.route('/')
def home():
    return "Fuber is working baby"


#####################################################################
#######################FUBER API#####################################

#Create un nuevo usuario
@app.route('/users', methods=['POST'])
def create_user():
    username=request.json.get('username')
    password=request.json.get('contrasena')
    nombre=request.json.get('nombre')
    apellidos=request.json.get('apellidos')
    dni=request.json.get('dni')
    fecha=request.json.get('fecha')
    mail=request.json.get('mail')
    telefono=request.json.get('telefono')
    cuenta=request.json.get('cuenta')
    permisos=request.json.get('permisos')
    vehiculo=request.json.get('vehiculo')
    matricula=request.json.get('matricula')
    marca=request.json.get('marca')
    modelo=request.json.get('modelo')
    tara=request.json.get('tara')
    plataforma=request.json.get('plataforma')
    carga=request.json.get('carga')
    turnos=request.json.get('turnos')
    dias=request.json.get('dias')
    comunidad=request.json.get('comunidad')
    provincia=request.json.get('provincia')
    municipio=request.json.get('municipio')
    tipoVia=request.json.get('tipoVia')
    nombreVia=request.json.get('nombreVia')
    numero=request.json.get('numero')
    escalera=request.json.get('escalera')
    piso=request.json.get('piso')
    puerta=request.json.get('puerta')
    codigoPostal=request.json.get('codigoPostal')
    disponibilidadGeo=request.json.get('disponibilidadGeo')
    imagen      = request.json.get('imagen')

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
    return (jsonify({'username': user.username}), 201)



if __name__ == '__main__':
    db.create_all()
    if 'liveconsole' not in gethostname():
        app.run(debug=True)