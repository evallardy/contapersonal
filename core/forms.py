from bootstrap_datepicker_plus import DatePickerInput
from django import forms

from .models import *

class DateInput(forms.DateInput):
    input_type = 'date'

class Deudor_form(forms.ModelForm):
    class Meta:
        model = Deudor
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['corte'].widget.attrs['class'] = 'text-center'
        self.fields['tipo_pago'].widget.attrs['class'] = 'text-center'
        self.fields['anio_empieza'].widget.attrs['class'] = 'text-center'
        self.fields['qna_empieza'].widget.attrs['class'] = 'text-center'
        self.fields['anio_termina'].widget.attrs['class'] = 'text-center'
        self.fields['qna_termina'].widget.attrs['class'] = 'text-center'
        self.fields['estatus'].widget.attrs['class'] = 'text-center'

class Pago_form(forms.ModelForm):
    class Meta:
        model = Pago
        fields = '__all__'
        widgets = {
            'fecha_pagado': DateInput(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['importe_pagar'].widget.attrs['class'] = 'text-right'
        self.fields['importe_pagado'].widget.attrs['class'] = 'text-right'
        self.fields['anio_pagar'].widget.attrs['class'] = 'text-center'
        self.fields['qna_pagar'].widget.attrs['class'] = 'text-center'
        self.fields['fecha_pagado'].widget.attrs['class'] = 'text-center'
        self.fields['estatus'].widget.attrs['class'] = 'text-center'

class PagoForm(forms.ModelForm):
    desde_anio = forms.ChoiceField(choices=ANIOS, label='Desde Año')
    desde_quincena = forms.ChoiceField(choices=QUINCENAS, label='Desde Quincena')
    hasta_anio = forms.ChoiceField(choices=ANIOS, label='Hasta Año')
    hasta_quincena = forms.ChoiceField(choices=QUINCENAS, label='Hasta Quincena')
    deudor = forms.ModelChoiceField(queryset=Deudor.objects.filter(estatus=1), label='Deudor')
    importe_pagar = forms.DecimalField(label='Importe a Pagar')
    comentario = forms.CharField(max_length=256, label='Comentario', required=False)
    tipo_pagar = forms.ChoiceField(choices=TIPO_PAGO, label='Como agregar')

    class Meta:
        model = Pago
        fields = ['deudor', 'desde_anio', 'desde_quincena', 'hasta_anio', 'hasta_quincena', 'importe_pagar', 'comentario', 'tipo_pagar']

    def clean(self):
        cleaned_data = super().clean()
        desde_anio = int(cleaned_data.get('desde_anio'))
        desde_quincena = int(cleaned_data.get('desde_quincena'))
        hasta_anio = int(cleaned_data.get('hasta_anio'))
        hasta_quincena = int(cleaned_data.get('hasta_quincena'))
        importe_pagar = cleaned_data.get('importe_pagar')
        tipo_pagar = cleaned_data.get('tipo_pagar')

        if desde_anio > hasta_anio or (desde_anio == hasta_anio and desde_quincena >= hasta_quincena):
            raise forms.ValidationError('La fecha de inicio no puede ser posterior o igual a la fecha de fin.')

        return cleaned_data

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Convierte ANIOS y QUINCENAS a listas si no lo son
        ANIOS1 = list(ANIOS)
        QUINCENAS1 = list(QUINCENAS)
        TIPO_PAGO1 = list(TIPO_PAGO)

        # Actualizar las opciones de los campos de año
        self.fields['desde_anio'].choices = ANIOS1[1:]
        self.fields['hasta_anio'].choices = ANIOS1[1:]

        # Actualizar las opciones de los campos de quincena
        self.fields['desde_quincena'].choices = QUINCENAS1[1:]
        self.fields['hasta_quincena'].choices = QUINCENAS1[1:]

        # Actualizar las opciones de los campos de quincena
        self.fields['tipo_pagar'].choices = TIPO_PAGO1[0:]

        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

class Cobro_form(forms.ModelForm):
    class Meta:
        model = Cobro
        fields = '__all__'
        widgets = {
            'fecha_cobro': DateInput(),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['importe_cobro'].widget.attrs['class'] = 'text-right'
        self.fields['importe_recibido'].widget.attrs['class'] = 'text-right'
        self.fields['anio_cobro'].widget.attrs['class'] = 'text-center'
        self.fields['qna_cobro'].widget.attrs['class'] = 'text-center'
        self.fields['fecha_cobro'].widget.attrs['class'] = 'text-center'
        self.fields['estatus'].widget.attrs['class'] = 'text-center'

class CobroForm(forms.ModelForm):
    desde_anio = forms.ChoiceField(choices=ANIOS, label='Desde Año')
    desde_quincena = forms.ChoiceField(choices=QUINCENAS, label='Desde Quincena')
    hasta_anio = forms.ChoiceField(choices=ANIOS, label='Hasta Año')
    hasta_quincena = forms.ChoiceField(choices=QUINCENAS, label='Hasta Quincena')
    importe_cobro = forms.DecimalField(label='Importe a Pagar')
    comentario = forms.CharField(max_length=256, label='Comentario', required=False)
    tipo_cobro = forms.ChoiceField(choices=TIPO_PAGO, label='Como agregar')

    class Meta:
        model = Cobro
        fields = ['desde_anio', 'desde_quincena', 'hasta_anio', 'hasta_quincena', 'importe_cobro', 'comentario', 'tipo_cobro']

    def clean(self):
        cleaned_data = super().clean()
        desde_anio = int(cleaned_data.get('desde_anio'))
        desde_quincena = int(cleaned_data.get('desde_quincena'))
        hasta_anio = int(cleaned_data.get('hasta_anio'))
        hasta_quincena = int(cleaned_data.get('hasta_quincena'))
        importe_pagar = cleaned_data.get('importe_cobro')
        tipo_pagar = cleaned_data.get('tipo_cobro')

        if desde_anio > hasta_anio or (desde_anio == hasta_anio and desde_quincena >= hasta_quincena):
            raise forms.ValidationError('La fecha de inicio no puede ser posterior o igual a la fecha de fin.')

        return cleaned_data

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Convierte ANIOS y QUINCENAS a listas si no lo son
        ANIOS1 = list(ANIOS)
        QUINCENAS1 = list(QUINCENAS)
        TIPO_PAGO1 = list(TIPO_PAGO)

        # Actualizar las opciones de los campos de año
        self.fields['desde_anio'].choices = ANIOS1[1:]
        self.fields['hasta_anio'].choices = ANIOS1[1:]

        # Actualizar las opciones de los campos de quincena
        self.fields['desde_quincena'].choices = QUINCENAS1[1:]
        self.fields['hasta_quincena'].choices = QUINCENAS1[1:]

        # Actualizar las opciones de los campos de quincena
        self.fields['tipo_cobro'].choices = TIPO_PAGO1[0:]

        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

class Sobrante_form(forms.ModelForm):
    class Meta:
        model = Sobrante
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['importe_sobrante'].widget.attrs['class'] = 'text-right'
        self.fields['anio_sobrante'].widget.attrs['class'] = 'text-center'
        self.fields['qna_sobrante'].widget.attrs['class'] = 'text-center'
