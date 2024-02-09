from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login, name="login"),
    path('register/', views.register, name="register"),
    path('panel/', views.home, name="home"),
    path('logout/', views.logout, name="logout"),
    path('', views.catalogo, name="catalogo"),
    # Clientes
    path('panel/cargar-cliente', views.cargarCliente, name="cargarCliente"),
    path('panel/eliminar-cliente', views.eliminarCliente, name="eliminarCliente"),
    path('panel/modificar-cliente', views.modificarCliente, name="modificarCliente"),
    # Stock
    path('panel/cargar-stock', views.cargarStock, name="cargarStock"),
    path('panel/modificar-producto', views.modificarProducto, name="modificarProducto"),
    path('panel/eliminar-producto', views.eliminarProducto, name="eliminarProducto"),
    # Pedidos
    path('panel/cargar-pedido', views.cargarPedido, name="cargarPedido"),
    path('panel/calendario-pedidos', views.calendarioPedidos, name="calendarioPedidos"),
    path('panel/eliminar-pedido', views.eliminarPedido, name="eliminarPedido"),
    path('panel/pedido-entregado', views.pedidoEntregado, name="pedidoEntregado"),
    path('panel/pedido-pagado', views.pedidoPagado, name="pedidoPagado"),
    path('panel/enviar-despacho', views.enviarDespacho, name="enviarDespacho"),
    # Catalogo
    path('panel/gestion-catalogo', views.gestionCatalogo, name="gestionCatalogo"),
    path('panel/modificar-imagen', views.modificarImagen, name="modificarImagen"),
    path('panel/eliminar-imagen', views.eliminarImagen, name="eliminarImagen"),


]