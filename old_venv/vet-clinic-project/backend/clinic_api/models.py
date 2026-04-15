from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    ROLE_CUSTOMER = "customer"
    ROLE_VET = "vet"
    ROLE_ASSISTANT = "assistant"
    ROLE_CHOICES = [
        (ROLE_CUSTOMER, "Customer"),
        (ROLE_VET, "Veterinarian"),
        (ROLE_ASSISTANT, "Assistant"),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    display_name = models.CharField(max_length=150, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default=ROLE_CUSTOMER)

    def __str__(self):
        return f"{self.display_name or self.user.username} ({self.role})"


class Pet(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="pets")
    name = models.CharField(max_length=100)
    species = models.CharField(max_length=50)
    breed = models.CharField(max_length=50, blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)
    sex = models.CharField(max_length=10, blank=True, null=True, help_text="เพศ")
    markings = models.TextField(blank=True, help_text="ตำหนิ/จุดสังเกต")
    is_neutered = models.BooleanField(default=False, help_text="ทำหมันแล้วหรือไม่")
    allergies = models.TextField(blank=True, help_text="ประวัติแพ้ยา/อาหาร")

    def __str__(self):
        return f"{self.name} ({self.species})"


class Appointment(models.Model):
    STATUS_PENDING = "pending"
    STATUS_CONFIRMED = "confirmed" # จองล่วงหน้ายืนยันแล้ว
    STATUS_WAITING = "waiting" # กำลังรอตรวจ (Walk-in / มาถึงแล้ว)
    STATUS_EXAMINING = "examining" # กำลังตรวจ
    STATUS_PAYMENT = "payment" # รอชำระเงิน
    STATUS_COMPLETED = "completed" # เสร็จสิ้น
    STATUS_CANCELLED = "cancelled"
    STATUS_CHOICES = [
        (STATUS_PENDING, "Pending (รอยืนยัน)"),
        (STATUS_CONFIRMED, "Confirmed (ยืนยันแล้ว)"),
        (STATUS_WAITING, "Waiting (กำลังรอตรวจ)"),
        (STATUS_EXAMINING, "Examining (กำลังตรวจ)"),
        (STATUS_PAYMENT, "Payment (รอชำระเงิน)"),
        (STATUS_COMPLETED, "Completed (เสร็จสิ้น)"),
        (STATUS_CANCELLED, "Cancelled (ยกเลิก)"),
    ]
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE, related_name="appointments")
    scheduled_at = models.DateTimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_PENDING)
    reason = models.CharField(max_length=200, blank=True, help_text="อาการเบื้องต้น/เหตุผลที่นัดหมาย")
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["scheduled_at"]

    def __str__(self):
        return f"{self.pet.name} @ {self.scheduled_at}"


class InventoryItem(models.Model):
    CATEGORY_CHOICES = [
        ("medicine", "ยาเม็ด/ยาน้ำ"),
        ("vaccine", "วัคซีน"),
        ("supply", "เวชภัณฑ์"),
        ("food", "อาหารสัตว์"),
        ("accessory", "อุปกรณ์/ปลอกคอ"),
        ("other", "อื่นๆ")
    ]
    item_code = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=200)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default="other")
    stock_quantity = models.IntegerField(default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2, help_text="ราคาขายต่อหน่วย")
    cost_price = models.DecimalField(max_digits=10, decimal_places=2, default=0, help_text="ราคาต้นทุนต่อหน่วย")
    expiry_date = models.DateField()

    def __str__(self):
        return self.name


class StaffShift(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="shifts")
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.user.username} on {self.date}"


class MedicalRecord(models.Model):
    appointment = models.OneToOneField(
        Appointment, on_delete=models.CASCADE, related_name="medical_record"
    )
    symptoms = models.TextField()
    diagnosis = models.TextField(blank=True, help_text="การวินิจฉัยโรค")
    weight = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, help_text="น้ำหนัก (kg)")
    temperature = models.DecimalField(max_digits=4, decimal_places=1, null=True, blank=True, help_text="อุณหภูมิ (°C)")
    medication_notes = models.TextField(blank=True)
    exam_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0, help_text="ค่าตรวจรักษา")
    is_paid = models.BooleanField(default=False)
    payment_method = models.CharField(max_length=50, blank=True, help_text="เงินสด, โอนเงิน, บัตรเครดิต")
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)


class PrescriptionLine(models.Model):
    medical_record = models.ForeignKey(
        MedicalRecord, on_delete=models.CASCADE, related_name="prescription_lines"
    )
    inventory_item = models.ForeignKey(InventoryItem, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField(default=1)
    dosage = models.CharField(max_length=200, blank=True, help_text="วิธีใช้ (Dosage)")
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    unit_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
