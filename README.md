**API  FUBER**
---
---
**URL base:** http://fuber.pythonanywhere.com


#### Models:
- Message
- Offer
- User



##### CREATE new user
##### route(```'/users'```, methods=[```'POST'```])
+ **Form-data accepted parameters:**
    + username
    + nombre
    + apellidos
    + dni
    + fecha
    + mail
    + telefono
    + cuenta
    + permisos
    + vehiculo
    + matricula
    + marca
    + modelo
    + tara
    + plataforma
    + carga
    + turnos
    + dias
    + comunidad
    + provincia
    + municipio
    + tipoVia
    + nombreVia
    + numero
    + escalera
    + piso
    + puerta
    + codigoPostal
    + disponibilidadGeo
    + imagen
+ **Return:**
    + (json({'token': token.decode('ascii')}), 201)
+ **Errors:**
    + 400 missing arguments or user exist


##### ALL users from db
##### route(```'/users'```, methods=[```'GET'```])
+ **Return List of users. FIELDS:**
    + id
    + username
    + nombre
    + apellidos
    + dni
    + fecha
    + mail
    + telefono
    + cuenta
    + permisos
    + vehiculo
    + matricula
    + marca
    + modelo
    + tara
    + plataforma
    + carga
    + turnos
    + dias
    + comunidad
    + provincia
    + municipio
    + tipoVia
    + nombreVia
    + numero
    + escalera
    + piso
    + puerta
    + codigoPostal
    + disponibilidadGeo
    + imagen
+ **Return type:**
    + resp = Response(list_users, status=200, mimetype='application/json')
    resp.headers['Link'] = 'URL_base'



##### USER by id
##### route(```'/users/<int:id>'```, methods=[```'GET'```])
+ **Headers accepted parameters:**
    + token
+ **Path accepted param:**
    + id
+ **Return User by id. FIELDS:**
    + id
    + username
    + nombre
    + apellidos
    + dni
    + fecha
    + mail
    + telefono
    + cuenta
    + permisos
    + vehiculo
    + matricula
    + marca
    + modelo
    + tara
    + plataforma
    + carga
    + turnos
    + dias
    + comunidad
    + provincia
    + municipio
    + tipoVia
    + nombreVia
    + numero
    + escalera
    + piso
    + puerta
    + codigoPostal
    + disponibilidadGeo
    + imagen
+ **Return type:**
    + resp = Response(user, status=200, mimetype='application/json')
    resp.headers['Link'] = 'URL_base'

**Error:**
+ 400 is user no exist or token invalid



##### Validate the existence of a user
##### route(```'/users/validate'```, methods=[```'GET'```)
+ **Query-param accepted:**
    + username
    + mail
+ **Return:**
+ **if** user not exist:
    + (json({'noexist': 'True'}), 200)
+ **if** user exist:
    + (json({'noexist': 'False'}), 200)



##### UPDATE user
##### route(```'/users/<int:id>'```, methods=[```'PUT'```])
+ **Headers accepted parameters:**
    + token
+ **Path accepted param:**
    + id
+ **Form-data accepted parameters:**
    + username
    + password
    + nombre
    + apellidos
    + dni
    + fecha
    + mail
    + telefono
    + cuenta
    + permisos
    + vehiculo
    + matricula
    + marca
    + modelo
    + tara
    + plataforma
    + carga
    + turnos
    + dias
    + comunidad
    + provincia
    + municipio
    + tipoVia
    + nombreVia
    + numero
    + escalera
    + piso
    + puerta
    + codigoPostal
    + disponibilidadGeo
    + imagen
+ **Return:**
    + (json({'username': user.username}), 200)
+ **Error :**
    + 400 if user not exist



##### LOGIN
##### route('```/login```', methods=[```'POST'```])
+ **Form-data accepted parameters:**
    + username
    + password
+ **Return:**
    + json({'token': token.decode('ascii'), 'duration': 66600})
+ **Error:**
    + 401 if username or password is incorrect



##### DROP database
##### route(```'/cleardatabase'```, methods=[```'GET'```])
+ **Return:**
    + json.dumps({'success':True}), 200, {'ContentType':'application/json'}



##### CREATE new offer
##### route(```'/ofertas'```, methods=[```'POST'```])
+ **FORM parameters:**
    + nombre_empresa
    + descripcion
    + fecha
    + hora_recogida
    + hora_entrega
    + direccion_recogida
    + direccion_entrega
    + precio_hora
    + tipo_vehiculo
    + tipo_carga
    + permiso_conducir
    + recorrido_km
    + metros
    + telefono_recogida
    + telefono_entrega
    + encoded_imagen_empresa
+ **Return:**
    + (json({'oferta': oferta.nombre_empresa}), 201)
+ **Error:**
    + 400 missing arguments



##### ALL offers from db
##### route(```'/ofertas'```, methods=[```'GET'```])
+ **Return list ofertas. FILEDS:**
    + id
    + nombre_empresa
    + descripcion
    + fecha
    + hora_recogida
    + hora_entrega
    + direccion_recogida
    + direccion_entrega
    + precio_hora
    + tipo_vehiculo
    + tipo_carga
    + permiso_conducir
    + recorrido_km
    + metros
    + telefono_recogida
    + telefono_entrega
    + encoded_imagen_empresa
+ **Return type:**
    + resp = Response(list_offers, status=200, mimetype='application/json')
    resp.headers['Link'] = 'URL_base'



##### ALL offers available
##### route(```'/ofertas/disponibles'```, methods=[```'GET'```])
+ **Return list of offers. FILEDS:**
    + id
    + nombre_empresa
    + descripcion
    + fecha
    + hora_recogida
    + hora_entrega
    + direccion_recogida
    + direccion_entrega
    + precio_hora
    + tipo_vehiculo
    + tipo_carga
    + permiso_conducir
    + recorrido_km
    + metros
    + telefono_recogida
    + telefono_entrega
    + encoded_imagen_empresa
+ **Return type:**
    + resp = Response(list_offers, status=200, mimetype='application/json')
    resp.headers['Link'] = 'URL_base'



##### Offer by id
##### route(```'/ofertas/<int:id>'```, methods=[```'GET'```])
+ **Path accepted param:**
    + id
+ **Return offer by id. FILEDS:**
    + id
    + nombre_empresa
    + descripcion
    + fecha
    + hora_recogida
    + hora_entrega
    + direccion_recogida
    + direccion_entrega
    + precio_hora
    + tipo_vehiculo
    + tipo_carga
    + permiso_conducir
    + recorrido_km
    + metros
    + telefono_recogida
    + telefono_entrega
    + encoded_imagen_empresa
+ **Return type:**
    + resp = Response(offer, status=200, mimetype='application/json')
    resp.headers['Link'] = 'URL_base'
+ **Error:**
    + 400 offer not exist



##### UPDATE offer by id
##### route(```'/ofertas/<int:id>'```, methods=[```'PUT'```])
+ **Path accepted param:**
    + id
+ **Form-data accepted parameters:**
    + nombre_empresa
    + descripcion
    + fecha
    + hora_recogida
    + hora_entrega
    + direccion_recogida
    + direccion_entrega
    + precio_hora
    + tipo_vehiculo
    + tipo_carga
    + permiso_conducir
    + recorrido_km
    + metros
    + telefono_recogida
    + telefono_entrega
    + encoded_imagen_empresa
+ **Return:**
    + (json({'nombre_empresa': offer.nombre_empresa}), 200)
+ **Error:**
    + 400 offer not exist



##### REQUEST offer by user
##### route(```'/ofertas/<int:id>/solicitar'```, methods=[```'PUT'```])
+ **Headers accepted parameters:**
    + token
+ **Path accepted param:**
    + id
+ **Form-data accepted parameters:**
    + user_id
+ **Return:**
    + (json({'user_id':user.id,'oferta_id':offer.id}), 200)
+ **Error:**
    + 400 user or offer not exist or invalid token



##### USERS who requested offer
##### route(```'/ofertas/<int:id>/solicitar'```, methods=[```'GET'```])
+ **Return List of users FIELDS:**
    + id
    + username
    + nombre
    + apellidos
    + dni
    + fecha
    + mail
    + telefono
    + cuenta
    + permisos
    + vehiculo
    + matricula
    + marca
    + modelo
    + tara
    + plataforma
    + carga
    + turnos
    + dias
    + comunidad
    + provincia
    + municipio
    + tipoVia
    + nombreVia
    + numero
    + escalera
    + piso
    + puerta
    + codigoPostal
    + disponibilidadGeo
    + imagen
+ **Return type:**
    + resp = Response(list_users, status=200, mimetype='application/json')
    resp.headers['Link'] = 'URL_base'
+ **Error:**
    + 400 offer not exist or token invalid



##### ASSIGN offer to user
##### route(```'/ofertas/<int:id>/pendientes'```, methods=[```'PUT'```])
+ **Path accepted param:**
    + id
+ **Form-data accepted parameters:**
    + user_id
+ **Return:**
    + (json({'user_id':user.id,'oferta_id':offer.id}), 200)
+ **Error:**
    + 400 user or offer not exist



#@### MARK FULFILLED offer
##### route(```'/ofertas/<int:id>/realizadas'```, methods=[```'PUT'```])
+ **Path accepted param:**
    + id
+ **Form-data accepted parameters:**
    + user_id
+ **Return:**
    + (json({'user_id':user.id,'oferta_id':offer.id}), 200)
+ **Error:**
    + 400 user or offer not exist



##### ALL offers fulfilled by user id
##### route(```'/users/<int:id>/realizadas'```, methods=[```'GET'```])
+ **Headers accepted parameters:**
    + token
+ **Path accepted param:**
    + id
+ **Return list offers. FIELDS:**
    + id
    + nombre_empresa
    + descripcion
    + fecha
    + hora_recogida
    + hora_entrega
    + direccion_recogida
    + direccion_entrega
    + precio_hora
    + tipo_vehiculo
    + tipo_carga
    + permiso_conducir
    + recorrido_km
    + metros
    + telefono_recogida
    + telefono_entrega
    + encoded_imagen_empresa
+ **Return type:**
    + resp = Response(list_offers, status=200, mimetype='application/json')
    resp.headers['Link'] = 'URL_base'
+ **Error:**
    + 400 user not exist or token inavalid



##### ALL offers pendings by user id
##### route(```'/users/<int:id>/pendientes'```, methods=[```'GET'```])
+ **Path accepted param:**
    + id
+ **Return list users. FIELDS**
    + id
    + nombre_empresa
    + descripcion
    + fecha
    + hora_recogida
    + hora_entrega
    + direccion_recogida
    + direccion_entrega
    + precio_hora
    + tipo_vehiculo
    + tipo_carga
    + permiso_conducir
    + recorrido_km
    + metros
    + telefono_recogida
    + telefono_entrega
    + encoded_imagen_empresa
+ **Return type:**
    + resp = Response(list_offers, status=200, mimetype='application/json')
    resp.headers['Link'] = 'URL_base'
+ **Error:**
    + 400 user not exist



##### USER by token
##### route(```'/me'```, methods=[```'GET'```])
+ **Headers accepted parameters:**
    + token
+ **Return:**
    + (json({'user_id':g.user.id}), 200)
+ **Error:**
    + 400 token is invalid




##### SEND message to fuber
##### route(```'/users/<int:id>/mensajes'```, methods=[```'POST'```])
+ **Headers accepted parameters (if type is 1):**
    + token
+ **Path accepted param:**
    + id
+ **Query-param accepted:**
    + type
    + text
    + date
    + time
+ **Return:**
    + (json({'user_id':user.id}), 200)
+ **Error:**
    + 400 is user not exist



##### ALL messages from db
##### route(```'/users/<int:id>/mensajes'```, methods=[```'GET'```])
+ **Path accepted param:**
    + id
+ **Return list messages. FIELDS:**
    + type
    + text
    + date
    + time
+ **Return:**
    + resp = Response(list_messages, status=200, mimetype='application/json')
    + resp.headers['Link'] = 'URL_base'
+ **Error:**
    + 400 is user not exist


#### DELETE user
##### route(```'/users/<int:id>'```, methods=[```'DELETE'```])
+ **Headers accepted parameters (if type is 1):**
    + token
+ **Path accepted param:**
    + id
+ **Return:**
    + (json({'delete':True}), 200)
+ **Error:**
    + 400 is user not exist



#### **DELETE offer**
##### route(```'/ofertas/<int:id>'```, methods=[```'DELETE'```])
+ **Path accepted param:**
    + id
+ **Return:**
    + (json({'delete':True}), 200)
+ **Error:**
    + 400 is offer not exist

