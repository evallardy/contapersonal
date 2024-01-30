from django.db import models
from django.contrib.auth.mixins import PermissionRequiredMixin

ANIOS = (
    (0, ''),
    (2024, '2024'),
    (2025, '2025'),
    (2026, '2026'),
    (2027, '2027'),
    (2028, '2028'),
    (2029, '2029'),
    (2030, '2030'),
)
ESTATUS_COBROS = (
    (0, 'Pendiente'),
    (1, 'Recibido'),
)
ESTATUS_PAGAR = (
    (0, 'Baja'),
    (1, 'Activo'),
)
ESTATUS_PAGOS = (
    (0, 'Pendiente'),
    (1, 'Pagado'),
    (2, 'Cancelado'),
)
QUINCENAS = (
    (0, ''),
    (1, '1a. qna.'),
    (2, '2a. qna.'),
    (3, '3a. qna.'),
    (4, '4a. qna.'),
    (5, '5a. qna.'),
    (6, '6a. qna.'),
    (7, '7a. qna.'),
    (8, '8a. qna.'),
    (9, '9a. qna.'),
    (10, '10a. qna.'),
    (11, '11a. qna.'),
    (12, '12a. qna.'),
    (13, '13a. qna.'),
    (14, '14a. qna.'),
    (15, '15a. qna.'),
    (16, '16a. qna.'),
    (17, '17a. qna.'),
    (18, '18a. qna.'),
    (19, '19a. qna.'),
    (20, '20a. qna.'),
    (21, '21a. qna.'),
    (22, '22a. qna.'),
    (23, '23a. qna.'),
    (24, '24a. qna.'),
)
TIPO_PAGO = (
    ('Q', 'Quincena'),
    ('M', 'Mensual'),
    ('B', 'Bimestral'),
    ('S', 'Semestral'),
)

# Create your models here.

class Deudor(models.Model, PermissionRequiredMixin):
    nombre = models.CharField('Nombre', max_length=80)
    corte = models.DecimalField('Corte', max_digits=2, decimal_places=0, default=1)
    tipo_pago = models.CharField('Tipo pago', max_length=1, choices=TIPO_PAGO, default='Q')
    qna_empieza = models.IntegerField('Qna empieza', choices=QUINCENAS, default=1)
    anio_empieza = models.IntegerField('Año empieza', choices=ANIOS, default=2024)
    qna_termina = models.IntegerField('Qna termina', choices=QUINCENAS, default=0)
    anio_termina = models.IntegerField('Año termina', choices=ANIOS, default=0)
    estatus = models.IntegerField('Estatus', choices=ESTATUS_PAGAR, default=1)
    created = models.DateTimeField("Creado", auto_now_add=True)
    modified = models.DateTimeField("Actualizado", auto_now=True)
    
    class Meta:
        verbose_name = 'Deudor'
        verbose_name_plural = 'Deudores'
        ordering = ['nombre',]
        unique_together = ['nombre']
        db_table = 'Deudor'

    def __str__(self):
        return '%s' % (self.nombre)

class Pago(models.Model, PermissionRequiredMixin):
    deudor = models.ForeignKey('Deudor', related_name='pago_deudor', on_delete=models.CASCADE)
    importe_pagar = models.DecimalField('Pagar', max_digits=8, decimal_places=2, default=0)
    importe_pagado = models.DecimalField('Pagado', max_digits=8, decimal_places=2, default=0)
    qna_pagar = models.IntegerField('Qna. pagar', choices=QUINCENAS, default=1)
    anio_pagar = models.IntegerField('Año pagar', choices=ANIOS, default=2024)
    comentario = models.CharField('Comentario', max_length=256, blank=True, null=True)
    fecha_pagado = models.DateField("Fecha pagado", blank=True, null=True)
    estatus = models.IntegerField('Estatus', choices=ESTATUS_PAGOS, default=0)
    created = models.DateTimeField("Creado", auto_now_add=True)
    modified = models.DateTimeField("Actualizado", auto_now=True)
    
    class Meta:
        verbose_name = 'Pago'
        verbose_name_plural = 'Pagos'
        ordering = ['deudor','anio_pagar','qna_pagar']
        db_table = 'Pago'

    def __str__(self):
        return '%s' % (self.deudor, self.anio_pagar, self.qna_pagar)

class Cobro(models.Model, PermissionRequiredMixin):
    importe_cobro = models.DecimalField('Cobrar', max_digits=8, decimal_places=2, default=0)
    importe_recibido = models.DecimalField('Recibido', max_digits=8, decimal_places=2, default=0)
    qna_cobro = models.IntegerField('Qna. cobro', choices=QUINCENAS, default=1)
    anio_cobro = models.IntegerField('Año cobro', choices=ANIOS, default=2024)
    comentario = models.CharField('Comentario', max_length=256, blank=True, null=True)
    fecha_cobro = models.DateField("Fecha cobro", blank=True, null=True)
    estatus = models.IntegerField('Estatus', choices=ESTATUS_COBROS, default=0)
    created = models.DateTimeField("Creado", auto_now_add=True)
    modified = models.DateTimeField("Actualizado", auto_now=True)
    
    class Meta:
        verbose_name = 'Cobro'
        verbose_name_plural = 'Cobros'
        ordering = ['anio_cobro','qna_cobro','id']
        db_table = 'Cobro'

    def __str__(self):
        return '%s' % (self.comentario, self.anio_cobro, self.qna_cobro, importe_recibido)

class Sobrante(models.Model, PermissionRequiredMixin):
    importe_sobrante = models.DecimalField('Sobrante', max_digits=8, decimal_places=2, default=0)
    qna_sobrante = models.IntegerField('Qna. sobrante', choices=QUINCENAS, default=1)
    anio_sobrante = models.IntegerField('Año sobrante', choices=ANIOS, default=2024)
    comentario = models.CharField('Comentario', max_length=256, blank=True, null=True)
    created = models.DateTimeField("Creado", auto_now_add=True)
    modified = models.DateTimeField("Actualizado", auto_now=True)
    
    class Meta:
        verbose_name = 'Sobrante'
        verbose_name_plural = 'Sobrantes'
        ordering = ['anio_sobrante','qna_sobrante']
        unique_together = ['anio_sobrante','qna_sobrante']
        db_table = 'Sobrante'

    def __str__(self):
        return '%s' % (self.anio_sobrante, self.qna_sobrante, importe_sobrante)
