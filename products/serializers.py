# tu_app_items/serializers.py
from rest_framework import serializers
from .models import Producto

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        # Campos que quieres incluir en el JSON de respuesta
        fields = ('id', 'title', 'description', 'price')