from django.urls import path, include

from .views import *

urlpatterns = [
    path('', Index.as_view(), name='index'),
    path('datos/', Datos.as_view(), name='datos'),
    path('deudores/', DeudorListView.as_view(), name='deudor-list'),
    path('deudores/<int:pk>/', DeudorDetailView.as_view(), name='deudor-detail'),
    path('deudores/nuevo/', DeudorCreateView.as_view(), name='deudor-create'),
    path('deudores/<int:pk>/editar/', DeudorUpdateView.as_view(), name='deudor-update'),
    path('deudores/<int:pk>/eliminar/', DeudorDeleteView.as_view(), name='deudor-delete'),
    path('pagos/', PagoListView.as_view(), name='pago-list'),
    path('pagos-grupo/<int:deudor>/<int:anio>/<int:quincena>/', PagoListViewGpo.as_view(), name='pagos-grupo'), 
    path('pagos/<int:pk>/', PagoDetailView.as_view(), name='pago-detail'),
    path('pagos/nuevo/', PagoCreateView.as_view(), name='pago-create'),
    path('pagos/<int:pk>/editar/', PagoUpdateView.as_view(), name='pago-update'),
    path('pagos/<int:pk>/eliminar/', PagoDeleteView.as_view(), name='pago-delete'),
    path('crear_pagos/', CrearPagosView.as_view(), name='crear_pagos'),
    path('cobros/', CobroListView.as_view(), name='cobro-list'),
    path('cobros/<int:pk>/', CobroDetailView.as_view(), name='cobro-detail'),
    path('cobros/nuevo/', CobroCreateView.as_view(), name='cobro-create'),
    path('cobros/<int:pk>/editar/', CobroUpdateView.as_view(), name='cobro-update'),
    path('cobros/<int:pk>/eliminar/', CobroDeleteView.as_view(), name='cobro-delete'),
    path('crear_cobros/', CrearCobrosView.as_view(), name='crear_cobros'),
    path('sobrantes/', SobranteListView.as_view(), name='sobrante-list'),
    path('sobrantes/<int:pk>/', SobranteDetailView.as_view(), name='sobrante-detail'),
    path('sobrantes/nuevo/', SobranteCreateView.as_view(), name='sobrante-create'),
    path('sobrantes/<int:pk>/editar/', SobranteUpdateView.as_view(), name='sobrante-update'),
    path('sobrantes/<int:pk>/eliminar/', SobranteDeleteView.as_view(), name='sobrante-delete'),
]
