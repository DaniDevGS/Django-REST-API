from rest_framework import serializers
from .models import Producto

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        # Agregamos 'cantidad' a la lista de campos
        fields = ['id', 'imagen', 'title', 'description', 'price', 'cantidad', 'datecompleted', 'user']