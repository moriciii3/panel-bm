from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Users, Clientes, Productos, Pedidos, Imagenes
from twilio.rest import Client

# Create your views here.

def login(request):
    
    if 'userName' in request.session:
        return redirect('home')
    else:

        if request.method == 'GET':
            return render(request,'login.html')
        else:

            userName = request.POST['userName']
            password = request.POST['password']

            if len(Users.objects.filter(userName=userName)) == 0: # Verifico si existe ese usuario
                return render(request, 'login.html', {
                        'respuesta': "Ese usuario no existe"
                    })
            else:
                usuario_correspondiente = get_object_or_404(Users, userName=userName) # el 404 lo dejo porsia

                if usuario_correspondiente.password == password:
                    # La contrasena es correcta
                    request.session['userName'] = userName # Creamos la sesion
                    return redirect('home')
                else:
                    return render(request, 'login.html', {
                        'respuesta': "Contraseña incorrecta"
                    })

def home(request):
    if 'userName' not in request.session:
        return redirect('login')
    else:
        return render(request, 'home.html',{
            'userName': request.session['userName']
        })

def logout(request):
    if 'userName' in request.session: # Verifico a ver si hay sesion por si acaso el usuario copio en enlace

        try:
            del request.session['userName'] # Cierro la sesion
            return redirect('login') # Redirecciono al login
        except:
            return HttpResponse("Error al cerrar sesion") # En caso de que no haya habido sesion, al cerrarla que de un error
        
    else:
        return redirect('login')

def register(request):

    #Primero verificamos la sesion

    if 'userName' in request.session:
        return redirect('home')
    else:
        if request.method == 'GET':
            return render(request, 'register.html')
        else:
            userName = request.POST['userName']
            password = request.POST['password']

            listaIguales = Users.objects.filter(userName=userName) # extraemos lista de usuarios con el mismo userName

            if len(listaIguales) == 0: # Verificamos que no hayan usuarios con el mismo userName
                try:
                    usuario = Users.objects.create(userName=userName,password=password)
                    usuario.save() # Guardo al usuario en la base

                    request.session['userName'] = userName # Creo la sesion
                    return redirect('home')
                except:
                    return HttpResponse("Error en la entrada de datos")
            else:
                return render(request, 'register.html', {
                    'respuesta': "Este nombre de usuario ya existe, intente de nuevo."
                })

def cargarCliente(request):
    if 'userName' not in request.session:
        return redirect('login')
    else:

        # Aqui comienza 

        lista_clientes = Clientes.objects.all()
        clientes = []

        for cliente in lista_clientes:

            # Verificamos deuda

            lista_pedidos = Pedidos.objects.filter(cliente_id=cliente.id) # Filtro los pedidos del cliente
            total_deudas = 0 # Cuento las deudas para saber si debe 0 o no

            for pedido in lista_pedidos:
                if pedido.estado_pago == False:
                    total_deudas += 1

            if total_deudas == 0:
                cliente.deuda = False
                debe = "NO DEBE"
                cliente.save()
            else:
                cliente.deuda = True
                debe = "DEBE"
                cliente.save()            

            formateado = [cliente.id,cliente.nombre,cliente.direccion,cliente.comuna,cliente.telefono,cliente.cantidadPedidos,debe,cliente.extra]

            clientes.append(formateado)

        if request.method == 'GET':

            return render(request, 'cargarCliente.html',{
                'userName': request.session['userName'],
                'clientes': clientes,
            })
        
        else:

            # Entra por POST, envia datos

            nombre = request.POST['nombre']
            direccion = request.POST['direccion']
            comuna = request.POST['comuna']
            extra = request.POST['extra']
            telefono = request.POST['telefono']

            lista_similares = Clientes.objects.filter(telefono=telefono) # Aca sirve el unique del telefono

            if len(lista_similares) == 0:

                try:
                    cliente = Clientes.objects.create(nombre=nombre,direccion=direccion,comuna=comuna,extra=extra,telefono=telefono,cantidadPedidos=0,deuda=False)
                    cliente.save()

                    return render(request, 'cargarCliente.html',{
                        'userName': request.session['userName'],
                        'clientes': clientes,
                        'respuesta': '¡Cliente creado exitosamente!',
                    })
                
                except:
                    return HttpResponse('Error al crear cliente')
            else:
                return render(request, 'cargarCliente.html',{
                    'userName': request.session['userName'],
                    'clientes': clientes,
                    'respuesta': 'Ya existe este cliente',
                })

def eliminarCliente(request):
    if 'userName' not in request.session:
        return redirect('login')
    else:

        if request.method == 'GET': # LO HAGO DE CAGON, SIEMPRE DEBERIA ENTRAR POR POST
            return redirect('home')
        else:

            id = request.POST['id']

            try:
                Clientes.objects.filter(id=id).delete()
                return redirect('cargarCliente')
            except:
                return HttpResponse('Error al eliminar cliente')

def modificarCliente(request):
    if 'userName' not in request.session:
        return redirect('login')
    else:

        if request.method == 'GET' and len(request.GET['id']) != 0:

            id = request.GET['id']

            try:

                usuarioModificar = get_object_or_404(Clientes,id=id)

                if usuarioModificar.deuda == False:
                    debe = "No debe"
                else:
                    debe = "Debe"

                datosModificar = [usuarioModificar.id,usuarioModificar.nombre,usuarioModificar.direccion,usuarioModificar.comuna,usuarioModificar.telefono,usuarioModificar.cantidadPedidos,debe,usuarioModificar.extra]

                return render(request, 'modificarCliente.html',{
                'datosModificar': datosModificar,
                })
            
            except:
                return HttpResponse('El id ingresado no corresponde a ningun usuario')
        
        elif request.method == 'POST': # POST
            
            idModificado = request.POST['id']

            usuarioModificado = Clientes.objects.filter(id=idModificado)

            nombreModificado = request.POST['nombreModificado']
            direccionModificada = request.POST['direccionModificada']
            comunaModificada = request.POST['comunaModificada']
            telefonoModificado = request.POST['telefonoModificado']
            cantidadPedidosModificada = request.POST['cantidadPedidosModificada']
            extraModificado = request.POST['extraModificado']

            if len(nombreModificado) != 0:
                usuarioModificado.update(nombre=nombreModificado)

            if len(direccionModificada) != 0:
                usuarioModificado.update(direccion=direccionModificada)
            
            if len(comunaModificada) != 0:
                usuarioModificado.update(comuna=comunaModificada)
            
            if len(telefonoModificado) != 0:
                usuarioModificado.update(telefono=telefonoModificado)
            
            if len(cantidadPedidosModificada) != 0:
                usuarioModificado.update(cantidadPedidos=cantidadPedidosModificada)

            if len(extraModificado) != 0:
                usuarioModificado.update(extra=extraModificado)
                        
            return redirect('cargarCliente')

        else: # Entra GET pero no envio ningun dato, (copio el link)

            return HttpResponse('Debes ingresar un id para modificar el cliente')

def cargarStock(request):
    if 'userName' not in request.session:
        return redirect('login')
    else:

        # Aqui comienza 

        lista_productos = Productos.objects.all()
        productos = []

        for producto in lista_productos:
            formateado = [producto.id,producto.nombreProducto,producto.identificador,producto.stock]
            productos.append(formateado)

        if request.method == 'GET':

            # Se entra a la pagina

            return render(request, 'cargarStock.html',{
                'userName': request.session['userName'],
                'productos': productos,
            })
        
        else:

            # Entra por POST, envia datos de producto nuevo

            nombreProducto = request.POST['nombreProducto']
            identificador = request.POST['identificador'].lower().strip()
            stockInicial = request.POST['stockInicial']

            print(identificador)

            lista_similares = Productos.objects.filter(identificador=identificador)

            if len(lista_similares) != 0:

                return render(request, 'cargarStock.html',{
                'userName': request.session['userName'],
                'productos': productos,
                'respuesta': 'Este producto ya existe',
                })

            else:

                try:
                    nuevoProducto = Productos.objects.create(nombreProducto=nombreProducto,identificador=identificador,stock=stockInicial)
                    nuevoProducto.save()

                    return render(request, 'cargarStock.html',{
                        'userName': request.session['userName'],
                        'productos': productos,
                        'respuesta': 'Producto creado existosamente',
                    })
                except:
                    return HttpResponse('Error al crear producto')

def modificarProducto(request):
    if 'userName' not in request.session:
        return redirect('login')
    else:

        if request.method == 'GET' and len(request.GET['id']) != 0: # Se clickeo un producto

            id = request.GET['id']

            try:
                productoModificar = get_object_or_404(Productos, id=id)

                datosModificar = [productoModificar.id,productoModificar.nombreProducto,productoModificar.identificador,productoModificar.stock]

                return render(request, 'modificarProducto.html',{
                    'datosModificar': datosModificar,
                })

            except:
                return HttpResponse('El id ingresado no corresponde a ningun producto')
        
        elif request.method == 'POST': # POST - Se enviaron los datos a modificar
            
            idModificado = request.POST['id']

            productoModificado = Productos.objects.filter(id=idModificado)

            nombreModificado = request.POST['nombreModificado']
            identificadorModificado = request.POST['identificadorModificado']
            stockModificado = request.POST['stockModificado']

            if len(nombreModificado) != 0:
                productoModificado.update(nombreProducto=nombreModificado)

            if len(identificadorModificado) != 0:
                productoModificado.update(identificador=identificadorModificado)
            
            if len(stockModificado) != 0:
                productoModificado.update(stock=stockModificado)
                        
            return redirect('cargarStock')
        
        else: # Entra GET pero no envio ningun dato, (copio el link)

            return HttpResponse('Debes ingresar un id para modificar el producto')
        
def eliminarProducto(request):
    if 'userName' not in request.session:
        return redirect('login')
    else:

        if request.method == 'GET': # LO HAGO DE CAGON, SIEMPRE DEBERIA ENTRAR POR POST
            return redirect('home')
        else:

            id = request.POST['id']

            try:
                Productos.objects.filter(id=id).delete()
                return redirect('cargarStock')
            
            except Exception as e:
                return HttpResponse(f'Error al eliminar producto: {str(e)}')

def cargarPedido(request):
    if 'userName' not in request.session:
        return redirect('login')
    else:

        # Aqui comienza

        lista_clientes = Clientes.objects.all()
        clientes = []

        for cliente in lista_clientes:
            formateado = [cliente.id,cliente.nombre,cliente.direccion]
            clientes.append(formateado)

        lista_productos = Productos.objects.all()
        productos = []

        for producto in lista_productos:
            if producto.stock != 0:
                datosProducto = [producto.id,producto.nombreProducto,producto.stock]
                productos.append(datosProducto)

        if request.method == 'GET': # Entra a la pagina

            return render(request, 'cargarPedido.html',{
                'userName': request.session['userName'],
                'clientes': clientes,
                'productos': productos,
            })
        
        else: # Envia datos de pedido nuevo

            # Aca empieza la fiesta xdddddddddd

            cliente_id = int(request.POST['cliente_id'])
            cantidadProductos = int(request.POST['cantidadProductos'])
            dia = request.POST['dia']
            hora = request.POST['hora']
            precio = int(request.POST['precio'])
            extra = request.POST['extra']

            # Extraer los productos y cantidades a una lista

            i = 1

            productosPedidos = []

            while i <= cantidadProductos: # producto1,cantidad1
                
                stringProducto = 'producto'+str(i)
                stringCantidad = 'cantidad'+str(i)

                productosPedidos.append([request.POST[stringProducto],request.POST[stringCantidad]])

                if int(request.POST[stringCantidad]) > Productos.objects.get(id=int(request.POST[stringProducto])).stock:
                    return render(request, 'cargarPedido.html',{
                        'userName': request.session['userName'],
                        'clientes': clientes,
                        'productos': productos,
                        'respuesta': 'La cantidad ingresada es mayor al stock disponible',
                    })

                i+=1

            # Creo el texto donde se ve el detalle del pedido producto a producto

            formatoPedido = "Producto: {} \nCantidad: {} \n"
            pedidoFormateadoTotal = ""

            for productoPedido in productosPedidos:

                objetoProducto = get_object_or_404(Productos,id=int(productoPedido[0]))

                # Dato sobre esto: Al hacer esto antes provoca que si yo elimino el pedido no se vuelva a actualizar el stock, esto debido a que no se puede modificar el pedido, lo mismo pasa con la cantidad de pedidos del cliente

                nuevoStock = objetoProducto.stock - int(productoPedido[1]) # Descuento el stock
                objetoProducto.stock=nuevoStock
                objetoProducto.save()

                pedidoFormateadoTotal += formatoPedido.format(objetoProducto.nombreProducto,productoPedido[1])

                pedidoFormateadoTotal += "\n"

                formatoPedido = "Producto: {} \nCantidad: {} \n" # Reinicio para proximos usos
            
            # Creamos objeto del pedido
                
            try:
                
                nuevoPedido = Pedidos.objects.create(cliente_id=cliente_id,precio=precio,resumenPedido=pedidoFormateadoTotal,estado_entrega=False,estado_pago=False,hora=hora,dia=dia,extra=extra)

                nuevoPedido.save()

            
                # Aumentar cantidad de pedidos del cliente
                
                clienteObjeto = get_object_or_404(Clientes, id=cliente_id)

                clienteObjeto.cantidadPedidos += 1

                clienteObjeto.save()

                return render(request, 'cargarPedido.html',{
                    'userName': request.session['userName'],
                    'clientes': clientes,
                    'productos': productos,
                    'respuesta': '¡Pedido creado exitosamente!',
                })
            
            except Exception as e:

                return render(request, 'cargarPedido.html',{
                    'userName': request.session['userName'],
                    'clientes': clientes,
                    'productos': productos,
                    'respuesta': f'Error al eliminar producto: {str(e)}',
                })

def calendarioPedidos(request):
    if 'userName' not in request.session:
        return redirect('login')
    else:

        listado_pedidos = Pedidos.objects.all()
        pedidos = []
        strings_mensaje_whatsapp = []

        for pedido_objeto in listado_pedidos:

            # Con el id del cliente procedemos a pedir la direccion, nombre y telefono del mismo

            cliente = get_object_or_404(Clientes, id=pedido_objeto.cliente_id)

            if pedido_objeto.estado_entrega:
                entregado = 'SI'
            else:
                entregado = 'NO'

            if pedido_objeto.estado_pago:
                pagado = 'SI'
            else:
                pagado = 'NO'

            x = [pedido_objeto.id , cliente.nombre , cliente.direccion, cliente.telefono , pedido_objeto.precio , pedido_objeto.resumenPedido , entregado , pagado , pedido_objeto.hora , pedido_objeto.dia , pedido_objeto.extra]

            informacion_formateada = (
                f"{x[8]} hs {x[9]}\n"  # Hora y día
                f"{x[1]}\n"             # Nombre
                f"+56 {x[3]}\n"             # Teléfono
                f"{x[2]}\n"             # Dirección
                f"\n{x[5]}"             # Resumen del pedido
                f"${x[4]}\n"             # Precio
                f"Pagado: {x[7]}\n"     # Estado de pago
                f"Información extra: {x[10]}"        # Extra
            )

            x.append(informacion_formateada)

            pedidos.append(x)

            print(informacion_formateada)
            print('\n')

        return render(request, 'calendarioPedidos.html',{
            'userName': request.session['userName'],
            'pedidos': pedidos,
        }) 
        
def eliminarPedido(request):
    if 'userName' not in request.session:
        return redirect('login')
    else:

        if request.method == 'GET': # LO HAGO DE CAGON, SIEMPRE DEBERIA ENTRAR POR POST
            return redirect('home')
        else:

            id = request.POST['id']

            try:
                Pedidos.objects.filter(id=id).delete()
                return redirect('calendarioPedidos')
            
            except Exception as e:
                return HttpResponse(f'Error al eliminar pedido: {str(e)}')
            
def pedidoEntregado(request):
    if 'userName' not in request.session:
        return redirect('login')
    else:

        if request.method == 'GET': # LO HAGO DE CAGON, SIEMPRE DEBERIA ENTRAR POR POST
            return redirect('home')
        else:

            id = request.POST['id']

            try:
                pedido = get_object_or_404(Pedidos, id=id)

                if pedido.estado_entrega == False:
                    pedido.estado_entrega = True
                else:
                    pedido.estado_entrega = False
                
                pedido.save()

                return redirect('calendarioPedidos')
            
            except Exception as e:
                return HttpResponse(f'Error al modificar pedido: {str(e)}')

def pedidoPagado(request):
    if 'userName' not in request.session:
        return redirect('login')
    else:

        if request.method == 'GET': # LO HAGO DE CAGON, SIEMPRE DEBERIA ENTRAR POR POST
            return redirect('home')
        else:

            id = request.POST['id']

            try:
                pedido = get_object_or_404(Pedidos, id=id)

                if pedido.estado_pago == False:
                    pedido.estado_pago = True
                else:
                    pedido.estado_pago = False
                
                pedido.save()

                return redirect('calendarioPedidos')
            
            except Exception as e:
                return HttpResponse(f'Error al modificar pedido: {str(e)}')
            
def enviarDespacho(request):
    if 'userName' not in request.session:
        return redirect('login')
    else:

        if request.method == 'GET': # LO HAGO DE CAGON, SIEMPRE DEBERIA ENTRAR POR POST
            return redirect('home')
        else:
            
            # Credenciales de Twilio
            auth_token = 'afaf42eaf97f0d90022d58551f903845'
            account_sid = 'AC34c7c220577f11411ccd59c969e3a539'
            client = Client(account_sid, auth_token)

            message = client.messages.create(
                from_='whatsapp:+14155238886',
                body= request.POST['mensaje'],
                to='whatsapp:+56973688125'
            )
            
            return redirect('calendarioPedidos')
        
# Apartado de catalogo
        
def catalogo(request):

    imagenes = Imagenes.objects.all()

    return render(request,'index.html',{
        'imagenes': imagenes,
    })
        
def gestionCatalogo(request):
    if 'userName' not in request.session:
        return redirect('login')
    else:

        # Creacion de imagen POST, Modificacion/Eliminacion GET (a otro archivo)

        imagenes = Imagenes.objects.all()

        if request.method == 'GET':

            # Visualiza

            return render(request, 'gestionCatalogo.html',{
                'userName': request.session['userName'],
                'imagenes': imagenes,
            })
    
        else:

            # Crea imagen

            if 'imagen' in request.FILES:
                imagen = request.FILES['imagen']
                nueva_imagen = Imagenes(imagen=imagen)
                nueva_imagen.save()

                return render(request, 'gestionCatalogo.html',{
                    'userName': request.session['userName'],
                    'imagenes': imagenes,
                    'respuesta': 'Imagen guardada exitosamente',
                })
            else:
                return HttpResponse('No se ha subido ninguna imagen')

def modificarImagen(request):
    if 'userName' not in request.session:
        return redirect('login')
    else:

        if request.method == 'GET':

            if 'id' not in request.GET: # Se entra sin enviar datos
                return redirect('gestionCatalogo')
            else:

                # Se enviaron datos por GET

                id_imagen = request.GET['id'] 

                imagen_modificar = get_object_or_404(Imagenes,id=id_imagen)

                return render(request,'modificarImagen.html',{
                    'imagen_modificar': imagen_modificar,
                })
        
        else:

            id_modificada = request.POST['id']
            imagen_modificar = Imagenes.objects.get(id=id_modificada)
            
            if 'imagen' in request.FILES:
                imagen_cargada = request.FILES['imagen']
                
                # Guardar la imagen en la carpeta de medios
                imagen_modificar.imagen.save(imagen_cargada.name, imagen_cargada) # Chatcito trucos
                
            return redirect('gestionCatalogo')

def eliminarImagen(request):
    if 'userName' not in request.session:
        return redirect('login')
    else:

        if request.method == 'GET':
            return redirect('home')
        else:

            try:
                Imagenes.objects.filter(id=request.POST['id']).delete()
                return redirect('gestionCatalogo')
            except:
                return HttpResponse('Error al eliminar la imagen')

            
