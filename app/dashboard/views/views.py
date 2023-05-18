from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from rest_framework import routers
from .apis.people import PersonViewSet, PersonPathSerializer
from .apis.employees import EmployViewSet, EmployPathSerializer
from .apis.users import UserViewSet, UserPathSerializer
from .apis.afp_onp import AfpOnpViewSet, AfpOnpPathSerializer
from .apis.daylies import DayliViewSet, DayliPathSerializer
from .apis.companies import CompanyViewSet, CompanyPathSerializer
from core import models


@login_required
def home_view(request):
    company = models.Company.objects.filter(is_principal=True).first()
    message = "hello low"
    return render(request, "dashboard/home.html", locals())


people_path = PersonPathSerializer.get_path()
user_path = UserPathSerializer.get_path()
employ_path = EmployPathSerializer.get_path()
afp_onp_path = AfpOnpPathSerializer.get_path()
dayli_path = DayliPathSerializer.get_path()
company_path = CompanyPathSerializer.get_path()

router = routers.DefaultRouter()
router.register(r"%s" % user_path, UserViewSet, basename=user_path)
router.register(r"%s" % people_path, PersonViewSet, basename=people_path)
router.register(r"%s" % employ_path, EmployViewSet, basename=employ_path)
router.register(r"%s" % afp_onp_path, AfpOnpViewSet, basename=afp_onp_path)
router.register(r"%s" % dayli_path, DayliViewSet, basename=dayli_path)
router.register(r"%s" % company_path, CompanyViewSet, basename=company_path)
