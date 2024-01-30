from django.shortcuts import render
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.views import View
from django.http import JsonResponse
from decimal import Decimal
from django.views.generic.edit import FormView


from .models import *
from .forms import *

class QnaContenido:
    def __init__(self, nombre='', estatus=0, importe=Decimal('0.00'), 
        fecha='', id=0, cantidad=0, quincena=0, anio=0, id_deudor=0):
        self.nombre = nombre
        self.estatus = estatus
        self.importe = importe
        self.fecha = fecha
        self.id = id
        self.cantidad = cantidad
        self.quincena = quincena
        self.anio = anio
        self.id_deudor = id_deudor

def arma_matriz(request, anio):

    deudores_matriz_encabezado = []
    deudores_matriz_contenido = []
    deudores_matriz_total_gasto = []
    deudores_matriz_total_cobro = []
    deudores_matriz_saldo = []
    deudores_matriz_saldo_anterior = []
    deudores_matriz_saldo_actual = []
    deudores_indice = []

    # Encabezado de la matriz
    encabezado = ['Deudor', 'Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre', 'Total']
    deudores_matriz_encabezado.append(encabezado)

    # Encabezado de las Qnas
    qnas_encabezado = ['1a Qna', '2a Qna'] * 12

    # Contenido celdas
    qnas_contenido1 = [Decimal('0.00').quantize(Decimal(f'1e-{2}')) for _ in range(25)]

    consecutivo = 0
    # Contenido de la matriz
    deudores = Deudor.objects.filter(estatus=1)
    for deudor in deudores:
        fila1 = [deudor.id, consecutivo]
        deudores_indice.append(fila1)
        consecutivo += 1
        qnas_contenido = [QnaContenido(nombre='',estatus=0, importe=Decimal('0.00'), \
            fecha='', id=0, cantidad=0, quincena=0, anio=0, id_deudor=0) for _ in range(24)]  # Lista de instancias QnaContenido
        fila = [deudor.nombre] + qnas_contenido + [Decimal('0.00').quantize(Decimal(f'1e-{2}'))]
        deudores_matriz_contenido.append(fila)

    renglon_total_gastos = consecutivo + 4

    # Contenido de la matriz total gasto
    fila = ['Total gasto'] + qnas_contenido1  # Agrega el total al final
    deudores_matriz_total_gasto.append(fila)

    # Contenido de la matriz total cobro
    fila = ['Total cobro'] + qnas_contenido1   # Agrega el total al final
    deudores_matriz_total_cobro.append(fila)

    # Contenido de la matriz total cobro
    fila = ['Sobrante mes anterior'] + qnas_contenido1   # Agrega el total al final
    deudores_matriz_saldo_anterior.append(fila)

    # Contenido de la matriz total cobro
    fila = ['Saldo'] + qnas_contenido1  # Agrega el total al final
    deudores_matriz_saldo.append(fila)

    # Contenido de la matriz total cobro
    fila = ['Saldo actual'] + qnas_contenido1  # Agrega el total al final
    deudores_matriz_saldo_actual.append(fila)

    pagos = Pago.objects.filter(anio_pagar=anio)

    for pago in pagos:
        fila = busca_deudor(pago.deudor.id, deudores_indice)
        columna = pago.qna_pagar
        if pago.importe_pagado > 0:
            importe = pago.importe_pagado
        else:
            importe = pago.importe_pagar
        
        deudores_matriz_contenido[fila][columna].importe += importe
        deudores_matriz_contenido[fila][columna].estatus = pago.estatus
        deudores_matriz_contenido[fila][columna].id = pago.id
        deudores_matriz_contenido[fila][columna].quincena = pago.qna_pagar
        deudores_matriz_contenido[fila][columna].nombre = pago.deudor.nombre
        deudores_matriz_contenido[fila][columna].anio = pago.anio_pagar
        deudores_matriz_contenido[fila][columna].cantidad += 1
        deudores_matriz_contenido[fila][columna].id_deudor = pago.deudor.id

        deudores_matriz_contenido[fila][25] += importe
        deudores_matriz_total_gasto[0][columna] += importe
        deudores_matriz_total_gasto[0][25] += importe
        


    cobros = Cobro.objects.filter(anio_cobro=anio)

    for cobro in cobros:
        columna = cobro.qna_cobro
        if cobro.importe_recibido > 0:
            importe = cobro.importe_recibido
        else:
            importe = cobro.importe_cobro

        deudores_matriz_total_cobro[0][columna] += importe
        deudores_matriz_total_cobro[0][25] += importe

        deudores_matriz_saldo[0][columna] = deudores_matriz_total_cobro[0][columna] - deudores_matriz_total_gasto[0][columna]

        deudores_matriz_saldo[0][25] = deudores_matriz_total_cobro[0][25] - deudores_matriz_total_gasto[0][25]

    saldo = Sobrante.objects.filter(anio_sobrante=anio, qna_sobrante=1).first()
    
    if saldo:
        saldo_inicial = saldo.importe_sobrante
    else:
        saldo_inicial = Decimal('0.00')

    deudores_matriz_saldo_anterior[0][1] = saldo_inicial

    for numero in range(1, 25):
        deudores_matriz_saldo_actual[0][numero] = deudores_matriz_saldo[0][numero] + deudores_matriz_saldo_anterior[0][numero]
        numero1 = numero + 1
        if numero < 24:
            deudores_matriz_saldo_anterior[0][numero1] += deudores_matriz_saldo_actual[0][numero]
    
    deudores_matriz_saldo_anterior[0][25] += saldo_inicial
    deudores_matriz_saldo_actual[0][25] = deudores_matriz_saldo[0][25] + deudores_matriz_saldo_anterior[0][25]

    context1 = {
        'deudores_matriz_encabezado': deudores_matriz_encabezado,
        'qnas_encabezado': qnas_encabezado,
        'deudores_matriz_contenido': deudores_matriz_contenido,
        'deudores_matriz_total_gasto': deudores_matriz_total_gasto,
        'deudores_matriz_total_cobro': deudores_matriz_total_cobro,
        'deudores_matriz_saldo_anterior': deudores_matriz_saldo_anterior,
        'deudores_matriz_saldo': deudores_matriz_saldo,
        'deudores_matriz_saldo_actual': deudores_matriz_saldo_actual,
        'anio': 'AÑO ' + str(anio),
    }

    tabla_cuerpo_html = render(request, 'core/tabla_cuerpo.html', context1).content.decode('utf-8')

    context = {
        'tabla_cuerpo_html': tabla_cuerpo_html
    }

    return context

def busca_deudor(id_buscar, deudores_indice):
    consecutivo_encontrado = None
    for fila in deudores_indice:
        if fila[0] == id_buscar:
            consecutivo_encontrado = fila[1]
            break
    return consecutivo_encontrado

class Index(View):
    template_name = 'core/index.html'
    def get(self, request, *args, **kwargs):
        selected_value = int(request.GET.get('selected_value', 2024))
        context = arma_matriz(request, selected_value)
        return render(request, self.template_name, context)

class Datos(View):
    def get(self, request, *args, **kwargs):
        selected_value = int(request.GET.get('selected_value'))
        context = arma_matriz(request, selected_value)
        return JsonResponse(context)

class DeudorListView(ListView):
    model = Deudor
    template_name = 'core/deudor_list.html'
    context_object_name = 'deudores'

class DeudorDetailView(DetailView):
    model = Deudor
    template_name = 'core/deudor_detail.html'
    context_object_name = 'deudor'

class DeudorCreateView(CreateView):
    model = Deudor
    template_name = 'core/deudor_form.html' 
    success_url = reverse_lazy('deudor-list')
    form_class = Deudor_form

class DeudorUpdateView(UpdateView):
    model = Deudor
    template_name = 'core/deudor_form.html'
    success_url = reverse_lazy('deudor-list')
    form_class = Deudor_form

class DeudorDeleteView(DeleteView):
    model = Deudor
    template_name = 'core/deudor_confirm_delete.html'
    success_url = reverse_lazy('deudor-list') 

class PagoListView(ListView):
    model = Pago
    template_name = 'core/pago_list.html'
    context_object_name = 'pagos'

class PagoListViewGpo(ListView):
    model = Pago
    template_name = 'core/pago_list.html'
    context_object_name = 'pagos'

    def get_queryset(self):
        deudor = self.kwargs.get('deudor',0)
        anio = self.kwargs.get('anio',0)
        quincena = self.kwargs.get('quincena',0)
        queryset = Pago.objects.filter(deudor__id=deudor, anio_pagar=anio, qna_pagar=quincena)
        return queryset

class PagoDetailView(DetailView):
    model = Pago
    template_name = 'core/pago_detail.html'
    context_object_name = 'pago'

class PagoCreateView(CreateView):
    model = Pago
    template_name = 'core/pago_form.html'
    success_url = reverse_lazy('pago-list')
    form_class = Pago_form

class PagoUpdateView(UpdateView):
    model = Pago
    template_name = 'core/pago_form.html'
    success_url = reverse_lazy('pago-list')
    form_class = Pago_form

class PagoDeleteView(DeleteView):
    model = Pago
    template_name = 'core/pago_confirm_delete.html'
    success_url = reverse_lazy('pago-list')

class CrearPagosView(FormView):
    template_name = 'core/pago_genera.html'
    form_class = PagoForm

    def form_valid(self, form):
        # Aquí puedes procesar y guardar los datos según tus necesidades
        desde_anio = form.cleaned_data['desde_anio']
        desde_quincena = form.cleaned_data['desde_quincena']
        hasta_anio = form.cleaned_data['hasta_anio']
        hasta_quincena = form.cleaned_data['hasta_quincena']
        deudor = form.cleaned_data['deudor']
        importe_pagar = form.cleaned_data['importe_pagar']
        comentario = form.cleaned_data['comentario']
        tipo_pagar = form.cleaned_data['tipo_pagar']

        # Recuperar el ID del deudor
        id_deudor = deudor.id

        print(f"ID del deudor: {id_deudor}")
        print(f"Desde año: {desde_anio}")
        print(f"Desde quincena: {desde_quincena}")
        print(f"Hasta año: {hasta_anio}")
        print(f"Hasta quincena: {hasta_quincena}")
        print(f"Importe a pagar: {importe_pagar}")
        print(f"Comentario: {comentario}")
        print(f"Como agregar: {tipo_pagar}")

        contador_qna = 1
        prende_sw = 0
        prende_sw_year = 0

        if tipo_pagar == 'Q':
            rango = 1
        elif tipo_pagar == 'M':
            rango = 2
        elif tipo_pagar == 'B':
            rango = 4
        elif tipo_pagar == 'S':
            rango = 12
        else:
            rango = 0

        contador_qna = rango

        for year_tuple in ANIOS:
            year_value, year_display = year_tuple
            if year_value == int(desde_anio) or prende_sw_year == 1:
                prende_sw_year = 1
                for qna_tuple in QUINCENAS:
                    qna_value, qna_display = qna_tuple
                    if (qna_value == int(desde_quincena) or prende_sw == 1) and qna_value != 0:
                        prende_sw = 1
                        if rango == contador_qna:
                            # Agregamos registro
                            pago = Pago(
                                deudor_id=id_deudor,
                                importe_pagar=importe_pagar,
                                qna_pagar=qna_value,
                                anio_pagar=year_value,
                                comentario=comentario,
                            )
                            pago.save()
                            # inicializamos contador_qna
                            contador_qna = 1
                        else:
                            contador_qna += 1
                    if year_value == int(hasta_anio) and qna_value == int(hasta_quincena):
                        break
            if year_value == int(hasta_anio) and qna_value == int(hasta_quincena):
                break

        return super().form_valid(form)


    def get_success_url(self):
        return reverse_lazy('index')

class CrearCobrosView(FormView):
    template_name = 'core/cobro_genera.html'
    form_class = CobroForm

    def form_valid(self, form):
        # Aquí puedes procesar y guardar los datos según tus necesidades
        desde_anio = form.cleaned_data['desde_anio']
        desde_quincena = form.cleaned_data['desde_quincena']
        hasta_anio = form.cleaned_data['hasta_anio']
        hasta_quincena = form.cleaned_data['hasta_quincena']
        importe_cobro = form.cleaned_data['importe_cobro']
        comentario = form.cleaned_data['comentario']
        tipo_cobro = form.cleaned_data['tipo_cobro']

        print(f"Desde año: {desde_anio}")
        print(f"Desde quincena: {desde_quincena}")
        print(f"Hasta año: {hasta_anio}")
        print(f"Hasta quincena: {hasta_quincena}")
        print(f"Importe a cobrar: {importe_cobro}")
        print(f"Comentario: {comentario}")
        print(f"Como agregar: {tipo_cobro}")

        contador_qna = 1
        prende_sw = 0
        prende_sw_year = 0

        if tipo_cobro == 'Q':
            rango = 1
        elif tipo_cobro == 'M':
            rango = 2
        elif tipo_cobro == 'B':
            rango = 4
        elif tipo_cobro == 'S':
            rango = 12
        else:
            rango = 0

        contador_qna = rango

        for year_tuple in ANIOS:
            year_value, year_display = year_tuple
            if year_value == int(desde_anio) or prende_sw_year == 1:
                prende_sw_year = 1
                for qna_tuple in QUINCENAS:
                    qna_value, qna_display = qna_tuple
                    if (qna_value == int(desde_quincena) or prende_sw == 1) and qna_value != 0:
                        prende_sw = 1
                        if rango == contador_qna:
                            # Agregamos registro
                            cobro = Cobro(
                                importe_cobro=importe_cobro,
                                qna_cobro=qna_value,
                                anio_cobro=year_value,
                                comentario=comentario,
                            )
                            cobro.save()
                            # inicializamos contador_qna
                            contador_qna = 1
                        else:
                            contador_qna += 1
                    if year_value == int(hasta_anio) and qna_value == int(hasta_quincena):
                        break
            if year_value == int(hasta_anio) and qna_value == int(hasta_quincena):
                break

        return super().form_valid(form)


    def get_success_url(self):
        return reverse_lazy('index')

class CobroListView(ListView):
    model = Cobro
    template_name = 'core/cobro_list.html'
    context_object_name = 'cobros'

class CobroDetailView(DetailView):
    model = Cobro
    template_name = 'core/cobro_detail.html'
    context_object_name = 'cobro'

class CobroCreateView(CreateView):
    model = Cobro
    template_name = 'core/cobro_form.html'
    success_url = reverse_lazy('cobro-list')
    form_class = Cobro_form

class CobroUpdateView(UpdateView):
    model = Cobro
    template_name = 'core/cobro_form.html'
    success_url = reverse_lazy('cobro-list')
    form_class = Cobro_form

class CobroDeleteView(DeleteView):
    model = Cobro
    template_name = 'core/cobro_confirm_delete.html'
    success_url = reverse_lazy('cobro-list')

class SobranteListView(ListView):
    model = Sobrante
    template_name = 'core/sobrante_list.html'
    context_object_name = 'sobrantes'

class SobranteDetailView(DetailView):
    model = Sobrante
    template_name = 'core/sobrante_detail.html'
    context_object_name = 'sobrante'

class SobranteCreateView(CreateView):
    model = Sobrante
    template_name = 'core/sobrante_form.html'
    success_url = reverse_lazy('sobrante-list')
    form_class = Sobrante_form

class SobranteUpdateView(UpdateView):
    model = Sobrante
    template_name = 'core/sobrante_form.html'
    success_url = reverse_lazy('sobrante-list')
    form_class = Sobrante_form

class SobranteDeleteView(DeleteView):
    model = Sobrante
    template_name = 'core/sobrante_confirm_delete.html'
    success_url = reverse_lazy('sobrante-list')