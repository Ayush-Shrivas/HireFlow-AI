from django.utils import timezone
from django.utils.text import slugify
from rest_framework import serializers
from .models import Job, JobSkill, Skill


class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = ("id", "name", "slug")
        read_only_fields = ("id", "slug")

    def create(self, validated_data):
        name = validated_data["name"].strip()
        skill, _ = Skill.objects.get_or_create(name__iexact=name, defaults={"name": name, "slug": slugify(name)})
        return skill


class JobSerializer(serializers.ModelSerializer):
    company_name = serializers.CharField(source="company.name", read_only=True)
    skills = SkillSerializer(many=True, read_only=True)
    skill_ids = serializers.PrimaryKeyRelatedField(many=True, source="_skill_ids", queryset=Skill.objects.all(), write_only=True, required=False)

    class Meta:
        model = Job
        fields = ("id", "company", "company_name", "created_by", "title", "description", "location", "employment_type", "min_experience", "salary_min", "salary_max", "status", "skills", "skill_ids", "published_at", "created_at", "updated_at")
        read_only_fields = ("id", "company_name", "created_by", "status", "published_at", "created_at", "updated_at", "skills")

    def create(self, validated_data):
        skill_ids = validated_data.pop("_skill_ids", [])
        job = Job.objects.create(**validated_data)
        JobSkill.objects.bulk_create([JobSkill(job=job, skill=skill) for skill in skill_ids])
        return job

    def update(self, instance, validated_data):
        skill_ids = validated_data.pop("_skill_ids", None)
        instance = super().update(instance, validated_data)
        if skill_ids is not None:
            instance.skills.set(skill_ids, through_defaults={})
        return instance
