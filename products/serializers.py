from rest_framework import serializers
from .models import Producto

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        # Agregamos 'datecompleted' para que el frontend sepa cuándo fue enviado.
        # También 'imagen' y 'user_id' por si son relevantes.
        fields = ('id', 'title', 'description', 'price', 'datecompleted', 'imagen', 'user')