from django.utils.text import slugify
from rest_framework import serializers
from .models import Company, CompanyMembership


class CompanyMembershipSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source="user.email", read_only=True)

    class Meta:
        model = CompanyMembership
        fields = ("id", "user", "email", "role", "created_at")
        read_only_fields = ("id", "email", "created_at")


class CompanySerializer(serializers.ModelSerializer):
    memberships = CompanyMembershipSerializer(many=True, read_only=True)

    class Meta:
        model = Company
        fields = ("id", "name", "slug", "description", "website", "location", "memberships", "created_by", "created_at", "updated_at")
        read_only_fields = ("id", "slug", "created_by", "memberships", "created_at", "updated_at")

    def create(self, validated_data):
        validated_data["slug"] = slugify(validated_data["name"])
        if Company.objects.filter(slug=validated_data["slug"]).exists():
            raise serializers.ValidationError({"name": "A company with this name already exists."})
        return Company.objects.create(**validated_data)
