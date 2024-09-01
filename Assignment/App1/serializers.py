from rest_framework import serializers
from .models import Product, Leads


class ProductSerializer(serializers.ModelSerializer):
    
    
    class Meta:
        model = Product
        fields = ("id","name", "description", "price", "created_at", "updated_at")
    

class LeadSerializer(serializers.ModelSerializer):

    class Meta:
        model = Leads
        fields = ("lead_name","email","phone_number","product","created_at")


class ProductSerializer1(serializers.ModelSerializer):
    num_leads = serializers.SerializerMethodField()
    
    class Meta:
        model = Product
        fields = ("name","price","num_leads")

    def get_num_leads(self, obj):
        return getattr(obj, 'num_leads', 0)