from rest_framework import serializers

from .models import Company


class CreateCompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ("companyName",)

    def create(self, validated_data):
        company_owner = validated_data["company_owner"]
        company = Company.objects.create(companyName=validated_data["companyName"], companyOwner=company_owner)
        return company
