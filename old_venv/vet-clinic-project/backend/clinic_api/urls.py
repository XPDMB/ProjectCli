from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    AppointmentViewSet,
    BookAppointmentView,
    InventoryViewSet,
    MedicalRecordViewSet,
    StaffShiftViewSet,
    FinancialReportView,
    MeView,
    PetViewSet,
    StaffListView,
    UserManagementView,
    login,
    register,
)

router = DefaultRouter()
router.register(r"pets", PetViewSet, basename="pet")
router.register(r"appointments", AppointmentViewSet, basename="appointment")
router.register(r"inventory", InventoryViewSet, basename="inventory")
router.register(r"medical-records", MedicalRecordViewSet, basename="medicalrecord")
router.register(r"staff-shifts", StaffShiftViewSet, basename="staffshift")

urlpatterns = [
    path("auth/register/", register),
    path("auth/login/", login),
    path("login/", login),
    path("me/", MeView.as_view()),
    path("book-appointment/", BookAppointmentView.as_view()),
    path("report/financial/", FinancialReportView.as_view()),
    path("staff/", StaffListView.as_view()),
    path("users/", UserManagementView.as_view()),
    path("users/<int:pk>/", UserManagementView.as_view()),
    path("", include(router.urls)),
]
