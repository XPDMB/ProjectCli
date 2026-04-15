from django.contrib.auth.models import User
from django.db import transaction
from rest_framework import serializers

from .models import Appointment, InventoryItem, MedicalRecord, Pet, PrescriptionLine, Profile, StaffShift


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ("display_name", "role")


class UserSerializer(serializers.ModelSerializer):
    profile = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ("id", "username", "email", "profile")

    def get_profile(self, obj):
        prof = getattr(obj, "profile", None)
        if prof is None:
            return None
        return ProfileSerializer(prof).data


class RegisterSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=150)
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, min_length=6)
    role = serializers.ChoiceField(
        choices=[Profile.ROLE_CUSTOMER, Profile.ROLE_VET, Profile.ROLE_ASSISTANT], default=Profile.ROLE_CUSTOMER
    )

    def create(self, validated_data):
        email = validated_data["email"].strip().lower()
        if User.objects.filter(username__iexact=email).exists():
            raise serializers.ValidationError({"email": "อีเมลนี้ถูกใช้แล้ว"})
        user = User.objects.create_user(
            username=email,
            email=email,
            password=validated_data["password"],
        )
        Profile.objects.create(
            user=user,
            display_name=validated_data["name"],
            role=validated_data.get("role", Profile.ROLE_CUSTOMER),
        )
        return user


class PetSerializer(serializers.ModelSerializer):
    owner_name = serializers.CharField(source="owner.profile.display_name", read_only=True)
    class Meta:
        model = Pet
        fields = ("id", "name", "species", "breed", "birth_date", "owner", "owner_name")
        read_only_fields = ("owner",)


class AppointmentSerializer(serializers.ModelSerializer):
    pet_name = serializers.CharField(source="pet.name", read_only=True)
    owner_email = serializers.EmailField(source="pet.owner.email", read_only=True)

    class Meta:
        model = Appointment
        fields = (
            "id",
            "pet",
            "pet_name",
            "owner_email",
            "scheduled_at",
            "status",
            "reason",
            "notes",
            "created_at",
        )
        read_only_fields = ("created_at",)


class StaffShiftSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source="user.profile.display_name", read_only=True)
    role = serializers.CharField(source="user.profile.role", read_only=True)
    class Meta:
        model = StaffShift
        fields = ("id", "user", "user_name", "role", "date", "start_time", "end_time", "notes")


class PrescriptionLineSerializer(serializers.ModelSerializer):
    item_name = serializers.CharField(source="inventory_item.name", read_only=True)

    class Meta:
        model = PrescriptionLine
        fields = ("id", "inventory_item", "item_name", "quantity", "dosage", "unit_price", "unit_cost")
        read_only_fields = ("unit_price", "unit_cost")


class MedicalRecordSerializer(serializers.ModelSerializer):
    prescription_lines = PrescriptionLineSerializer(many=True, required=False)
    pet_name = serializers.CharField(source="appointment.pet.name", read_only=True)
    pet_id = serializers.IntegerField(source="appointment.pet.id", read_only=True)

    class Meta:
        model = MedicalRecord
        fields = (
            "id",
            "appointment",
            "pet_id",
            "pet_name",
            "symptoms",
            "diagnosis",
            "weight",
            "temperature",
            "medication_notes",
            "exam_fee",
            "prescription_lines",
            "is_paid",
            "total_amount",
            "created_at",
        )
        read_only_fields = ("created_at", "total_amount")

    def validate_appointment(self, value):
        if MedicalRecord.objects.filter(appointment=value).exists():
            raise serializers.ValidationError("นัดหมายนี้มีประวัติการรักษาแล้ว")
        return value

    def create(self, validated_data):
        lines_data = validated_data.pop("prescription_lines", [])
        total = validated_data.get("exam_fee", 0)
        with transaction.atomic():
            record = MedicalRecord.objects.create(**validated_data)
            for raw in lines_data:
                inv = raw["inventory_item"]
                qty = raw.get("quantity", 1)
                
                if inv.stock_quantity < qty:
                    raise serializers.ValidationError(f"สต็อก {inv.name} ไม่พอ")
                
                inv.stock_quantity -= qty
                inv.save(update_fields=["stock_quantity"])
                
                line_total = inv.price * qty
                total += line_total
                
                PrescriptionLine.objects.create(
                    medical_record=record,
                    inventory_item=inv,
                    quantity=qty,
                    dosage=raw.get("dosage", ""),
                    unit_price=inv.price,
                    unit_cost=inv.cost_price
                )
            
            record.total_amount = total
            record.save(update_fields=["total_amount"])
            return record


class InventorySerializer(serializers.ModelSerializer):
    class Meta:
        model = InventoryItem
        fields = "__all__"

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            prof = getattr(request.user, 'profile', None)
            if not prof or prof.role != Profile.ROLE_VET:
                ret.pop('cost_price', None)
        return ret
