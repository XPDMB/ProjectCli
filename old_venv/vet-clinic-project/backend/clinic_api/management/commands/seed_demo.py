from datetime import date, timedelta

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.utils import timezone

from clinic_api.models import Appointment, InventoryItem, Pet, Profile


class Command(BaseCommand):
    help = "สร้างข้อมูลทดสอบ (ยา สัตว์เลี้ยง คิวตัวอย่าง)"

    def handle(self, *args, **options):
        vet, _ = User.objects.get_or_create(
            username="vet@clinic.test",
            defaults={"email": "vet@clinic.test"},
        )
        vet.set_password("vet12345")
        vet.save()
        Profile.objects.update_or_create(
            user=vet,
            defaults={"display_name": "สัตวแพทย์ทดสอบ", "role": Profile.ROLE_VET},
        )

        cust, _ = User.objects.get_or_create(
            username="owner@test.com",
            defaults={"email": "owner@test.com"},
        )
        cust.set_password("pass12345")
        cust.save()
        Profile.objects.update_or_create(
            user=cust,
            defaults={"display_name": "เจ้าของสัตว์ทดสอบ", "role": Profile.ROLE_CUSTOMER},
        )

        pet, _ = Pet.objects.get_or_create(
            owner=cust,
            name="มะลิ",
            defaults={"species": "สุนัข", "breed": "ไทยหลังอาน", "birth_date": date(2020, 1, 1)},
        )

        InventoryItem.objects.get_or_create(
            item_code="MED001",
            defaults={
                "name": "ยาปฏิชีวนะ Amoxicillin",
                "stock_quantity": 50,
                "price": "150.00",
                "expiry_date": date.today() + timedelta(days=365),
            },
        )
        InventoryItem.objects.get_or_create(
            item_code="MED002",
            defaults={
                "name": "ยาลดปวด Meloxicam",
                "stock_quantity": 30,
                "price": "220.00",
                "expiry_date": date.today() + timedelta(days=200),
            },
        )

        when = timezone.now().replace(hour=10, minute=0, second=0, microsecond=0)
        if when < timezone.now():
            when += timedelta(days=1)
        Appointment.objects.get_or_create(
            pet=pet,
            scheduled_at=when,
            defaults={"status": Appointment.STATUS_PENDING, "notes": "ตรวจสุขภาพประจำปี"},
        )

        self.stdout.write(self.style.SUCCESS("seed_demo: OK"))
