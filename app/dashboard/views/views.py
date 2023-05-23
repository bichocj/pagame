import datetime
from calendar import monthrange
from decimal import Decimal
from django.contrib.auth.decorators import login_required
from django.db.models import F, Sum
from django.db.models.functions import ExtractMonth, ExtractYear
from django.shortcuts import render
from rest_framework import routers

from core import models

from .apis.afp_onp import AfpOnpPathSerializer, AfpOnpViewSet
from .apis.companies import CompanyPathSerializer, CompanyViewSet
from .apis.daylies import DayliPathSerializer, DayliViewSet
from .apis.employees import EmployPathSerializer, EmployViewSet
from .apis.people import PersonPathSerializer, PersonViewSet
from .apis.users import UserPathSerializer, UserViewSet
from .apis.invoice_details import InvoiceDetailsPathSerializer, InvoiceDetailsViewSet


@login_required
def home_view(request):
    return render(request, "dashboard/home.html", locals())


def invoice_view(request, month_number, employ_id):
    is_closed = False
    if request.method == "POST":
        is_closed = bool(request.POST.get("closed", 0))

    today = datetime.date.today()
    current_year = today.year
    employ = models.Employ.objects.select_related("person", "afp_onp").get(id=employ_id)
    company = models.Company.objects.get(is_principal=True)
    period = datetime.datetime(current_year, month_number, 1).date()

    try:
        invoice = models.Invoice.objects.get(employ=employ, period=period)
        if is_closed:
            invoice.is_closed = True
            invoice.save()
            models.Dayli.objects.filter(
                employ=employ,
                start_at_1__month=month_number,
                start_at_1__year=current_year,
            ).update(is_closed=invoice.is_closed)

    except models.Invoice.DoesNotExist:
        invoice = models.Invoice.objects.create(employ=employ, period=period)
        if month_number == 7 or month_number == 12:
            models.InvoiceDetails.objects.create(
                invoice=invoice,
                concept="GRATIF. F.PATRIAS NAVIDAD LEY 29351 Y 30334",
                amount=employ.salary,
                concept_type=1,
            )
            models.InvoiceDetails.objects.create(
                invoice=invoice,
                concept="BONIF. EXTRAORD. TEMPORAL LEY 29351 y 30334",
                amount=employ.salary * Decimal(round(0.09, 2)),
                concept_type=1,
            )

    attendances = models.Dayli.objects.filter(
        employ=employ, start_at_1__month=month_number, start_at_1__year=current_year
    )
    _, last_day = monthrange(current_year, month_number)
    days_worked = len(attendances)
    days_without_worked = last_day - len(attendances)

    total_hn = 0
    total_hn_amount = 0
    total_h25 = 0
    total_h25_amount = 0
    total_h35 = 0
    total_h35_amount = 0
    total_total = 0

    for a in attendances:
        if invoice.is_closed:
            if a.is_closed:
                total_hn += a.hn
                total_hn_amount += a.hn_amount
                total_h25 += a.h25
                total_h25_amount += a.h25_amount
                total_h35 += a.h35
                total_h35_amount += a.h35_amount
                total_total += a.total
        else:
            total_hn += a.hn
            total_hn_amount += a.hn_amount
            total_h25 += a.h25
            total_h25_amount += a.h25_amount
            total_h35 += a.h35
            total_h35_amount += a.h35_amount
            total_total += a.total

    total_hextras = total_h25 + total_h35

    invoice_details = models.InvoiceDetails.objects.filter(invoice=invoice)
    familiar_amount = 0
    if employ.has_children:
        familiar_amount = company.familiar_amount

    total_outcome = round(
        (
            ((employ.afp_onp.mandatory / 100) * employ.salary)
            + ((employ.afp_onp.prima / 100) * employ.salary)
            + ((employ.afp_onp.commision / 100) * employ.salary)
        ),
        2,
    )
    total_income = round(
        (total_hn_amount + total_h25_amount + total_h35_amount + familiar_amount), 2
    )
    total_income_company = (company.essalud / 100) * employ.salary

    for i in invoice_details:
        if i.concept_type == 1:
            total_income += i.amount
        if i.concept_type == 2:
            total_outcome += i.amount
        if i.concept_type == 3:
            total_income_company += i.amount

    if not invoice.is_closed:
        invoice.salary = employ.salary
        invoice.hn_amount = total_hn_amount
        invoice.h25_amount = total_h25_amount
        invoice.h35_amount = total_h35_amount
        invoice.familiar_amount = familiar_amount
        invoice.essalud = company.essalud
        invoice.total_income = total_income
        invoice.total_outcome = total_outcome
        invoice.total_income_company = total_income_company
        invoice.afp_mandatory = employ.afp_onp.mandatory
        invoice.afp_prima = employ.afp_onp.prima
        invoice.afp_commision = employ.afp_onp.commision
        invoice.is_closed = is_closed

        invoice.save()

    return render(request, "dashboard/invoice.html", locals())


@login_required
def invoices_view(request):
    year = 2023
    employees = models.Employ.objects.all()
    months_available = (
        models.Dayli.objects.annotate(year=ExtractYear("start_at_1"))
        .annotate(month=ExtractMonth("start_at_1"))
        .values_list("month", flat=True)
        .distinct()
        .filter(start_at_1__year=year)
        .order_by("month")
    )
    return render(request, "dashboard/invoices.html", locals())


people_path = PersonPathSerializer.get_path()
user_path = UserPathSerializer.get_path()
employ_path = EmployPathSerializer.get_path()
afp_onp_path = AfpOnpPathSerializer.get_path()
dayli_path = DayliPathSerializer.get_path()
company_path = CompanyPathSerializer.get_path()
invoice_detail_path = InvoiceDetailsPathSerializer.get_path()

router = routers.DefaultRouter()
router.register(r"%s" % user_path, UserViewSet, basename=user_path)
router.register(r"%s" % people_path, PersonViewSet, basename=people_path)
router.register(r"%s" % employ_path, EmployViewSet, basename=employ_path)
router.register(r"%s" % afp_onp_path, AfpOnpViewSet, basename=afp_onp_path)
router.register(r"%s" % dayli_path, DayliViewSet, basename=dayli_path)
router.register(r"%s" % company_path, CompanyViewSet, basename=company_path)
router.register(
    r"%s" % invoice_detail_path, InvoiceDetailsViewSet, basename=invoice_detail_path
)
