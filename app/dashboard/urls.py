from django.urls import path, include
from .views import views

app_name = "dashboard"

urlpatterns = [
    path("", view=views.home_view, name="home"),
    path(
        "invoices/detail/<int:month_number>/<int:employ_id>/",
        view=views.invoice_view,
        name="invoices_detail",
    ),
    path("invoices/", view=views.invoices_view, name="invoices"),
    path(r"api/", include(views.router.urls)),
]
