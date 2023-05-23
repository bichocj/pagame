import datetime
from django.db import models
from django.forms import ValidationError


class Person(models.Model):
    class Sexs(models.IntegerChoices):
        FEMALE = 0, ("femenino")
        MALE = 1, ("masculino")

    class Titles(models.IntegerChoices):
        tec = 0, ("tec.")
        mvz = 1, ("mvz.")

    class Meta:
        verbose_name = "persona"
        verbose_name_plural = "personas"
        ordering = ("name",)

    dni = models.CharField("dni", max_length=8, null=True, blank=True)
    name = models.CharField("nombres", max_length=50)
    last_name = models.CharField("apellidos", max_length=50, null=True, blank=True)
    sex = models.IntegerField("sexo", choices=Sexs.choices, blank=True, null=True)
    title = models.IntegerField("titulo", choices=Titles.choices, blank=True, null=True)

    def __str__(self) -> str:
        return f"{self.name} {self.last_name}"


class AfpOnp(models.Model):
    name = models.CharField("name", max_length=20)
    commision = models.DecimalField(
        "comision", default=0.0, max_digits=6, decimal_places=2
    )
    prima = models.DecimalField("prima", default=0.0, max_digits=6, decimal_places=2)
    mandatory = models.DecimalField(
        "obligatorio", default=0.0, max_digits=6, decimal_places=2
    )
    is_onp = models.DecimalField(
        "es onp", default=False, max_digits=6, decimal_places=2
    )

    class Meta:
        verbose_name = "AFP/ONP"
        verbose_name_plural = "AFPs/ONP"
        ordering = ("name",)

    def __str__(self) -> str:
        return self.name


class Employ(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE, verbose_name="persona")
    start_at = models.DateField("Fec. Ingreso", null=True, blank=True)
    employ_type = models.CharField(
        "Tipo de Trabajador", max_length=50, default="OBRERO"
    )

    afp_onp = models.ForeignKey(
        AfpOnp, on_delete=models.CASCADE, verbose_name="AFP/ONP"
    )
    cuspp = models.CharField(max_length=20, default="")
    has_children = models.BooleanField("tiene hijos", default=False)
    salary = models.DecimalField("Salario", max_digits=7, decimal_places=2)
    bank_name = models.CharField("Banco donde se le paga", max_length=100)
    bank_account_number = models.CharField("Número de cuenta", max_length=100)
    bank_account_number_cci = models.CharField(
        "Número de cuenta interbancario", max_length=100
    )

    class Meta:
        verbose_name = "empleado"
        verbose_name_plural = "empleados"
        ordering = ("person__name",)

    def __str__(self) -> str:
        return str(self.person)


class Dayli(models.Model):
    employ = models.ForeignKey(
        Employ, on_delete=models.CASCADE, verbose_name="empleado"
    )
    start_at_1 = models.DateTimeField("entrada 1")
    end_at_1 = models.DateTimeField("salida 1")
    start_at_2 = models.DateTimeField("entrada 2", blank=True, null=True)
    end_at_2 = models.DateTimeField("salida 2", blank=True, null=True)
    hn = models.DecimalField(
        "horas normales", blank=True, null=True, max_digits=6, decimal_places=2
    )
    hn_amount = models.DecimalField(
        "s/. horas normales", blank=True, null=True, max_digits=6, decimal_places=2
    )
    h25 = models.DecimalField(
        "horas al 25%", blank=True, null=True, max_digits=6, decimal_places=2
    )
    h25_amount = models.DecimalField(
        "s/. horas al 25%", blank=True, null=True, max_digits=6, decimal_places=2
    )
    h35 = models.DecimalField(
        "horas al 35%", blank=True, null=True, max_digits=6, decimal_places=2
    )
    h35_amount = models.DecimalField(
        "s/. horas al 35%", blank=True, null=True, max_digits=6, decimal_places=2
    )
    total = models.DecimalField(
        "s/.", blank=True, null=True, max_digits=6, decimal_places=2
    )
    is_closed = models.BooleanField("bloqueado", default=False)

    class Meta:
        verbose_name = "asistencia"
        verbose_name_plural = "asistencias"
        ordering = ("-id",)


class Invoice(models.Model):
    is_closed = models.BooleanField("bloqueado", default=False)
    employ = models.ForeignKey(
        Employ, on_delete=models.CASCADE, verbose_name="empleado"
    )
    period = models.DateField()
    days_worked = models.IntegerField(default=0)
    days_lazy = models.IntegerField(default=0)
    salary = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    hn_amount = models.DecimalField(max_digits=7, decimal_places=2, default=0)
    h25_amount = models.DecimalField(max_digits=7, decimal_places=2, default=0)
    h35_amount = models.DecimalField(max_digits=7, decimal_places=2, default=0)
    familiar_amount = models.DecimalField(max_digits=7, decimal_places=2, default=0)
    afp_mandatory = models.DecimalField(max_digits=7, decimal_places=2, default=0)
    afp_prima = models.DecimalField(max_digits=7, decimal_places=2, default=0)
    afp_commision = models.DecimalField(max_digits=7, decimal_places=2, default=0)
    total_income = models.DecimalField(max_digits=7, decimal_places=2, default=0)
    total_income_company = models.DecimalField(
        max_digits=7, decimal_places=2, default=0
    )
    total_outcome = models.DecimalField(max_digits=7, decimal_places=2, default=0)
    essalud = models.DecimalField(max_digits=7, decimal_places=2, default=0)
    created_at = models.DateField(auto_created=True, auto_now=True)

    class Meta:
        verbose_name = "boleta"
        verbose_name_plural = "boletas"
        ordering = ("employ__person__name",)


class InvoiceDetails(models.Model):
    class ConcetType(models.IntegerChoices):
        INCOME = 1, ("Ingresos")
        OUTCOME = 2, ("Descuentos")
        INCOME_COMPANY = 3, ("Aportaciones")

    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True, auto_created=True)
    concept = models.CharField("concepto", max_length=50)
    amount = models.DecimalField(
        "monto", blank=True, null=True, max_digits=7, decimal_places=2
    )
    concept_type = models.IntegerField(choices=ConcetType.choices)


class Company(models.Model):
    is_principal = models.BooleanField("es principal", unique=True)
    name = models.CharField("nombre", max_length=200)
    ruc = models.CharField("ruc", max_length=200)
    address = models.CharField("dirección", max_length=200)
    signer_name = models.CharField("nombre del firmador", max_length=200)
    signer_title = models.CharField("cargo del firmador", max_length=200)
    familiar_amount = models.DecimalField(
        "asignación familiar s/.", blank=True, null=True, max_digits=5, decimal_places=2
    )
    essalud = models.DecimalField(
        "essalud %", blank=True, null=True, max_digits=5, decimal_places=2
    )

    class Meta:
        verbose_name = "empresa"
        verbose_name_plural = "empresas"
