from django.contrib import admin

from .models import Appointment, InventoryItem, MedicalRecord, Pet, PrescriptionLine, Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "display_name", "phone", "role")
    search_fields = ("user__username", "user__email", "display_name", "phone")
    list_filter = ("role",)


@admin.register(Pet)
class PetAdmin(admin.ModelAdmin):
    list_display = ("name", "species", "owner", "sex")
    list_filter = ("species", "is_neutered")
    search_fields = ("name", "owner__username", "owner__profile__display_name", "owner__profile__phone")


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ("pet", "scheduled_at", "status")
    list_filter = ("status", "scheduled_at")
    search_fields = ("pet__name", "pet__owner__username")


@admin.register(InventoryItem)
class InventoryAdmin(admin.ModelAdmin):
    list_display = ("item_code", "name", "category", "stock_quantity", "price", "expiry_date")
    search_fields = ("item_code", "name")
    list_filter = ("category", "expiry_date")


class PrescriptionLineInline(admin.TabularInline):
    model = PrescriptionLine
    extra = 0


@admin.register(MedicalRecord)
class MedicalRecordAdmin(admin.ModelAdmin):
    list_display = ("appointment", "created_at")
    inlines = [PrescriptionLineInline]
