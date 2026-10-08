from rest_framework import serializers  
from .models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.models import User 

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']
  
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username
        token['email'] = user.email
        return token

from .models import Product, Supplier, StockMovement

class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = ['id', 'name', 'contact_email', 'phone', 'address', 'created_at']

class ProductSerializer(serializers.ModelSerializer):
    supplier = SupplierSerializer(read_only=True)
    supplier_id = serializers.PrimaryKeyRelatedField(queryset=Supplier.objects.all(), source='supplier', write_only=True, required=False, allow_null=True)

    class Meta:
        model = Product
        fields = ['id', 'name', 'category', 'quantity', 'min_stock_level', 'cost_price', 'selling_price', 'supplier', 'supplier_id', 'image_url', 'created_at', 'updated_at']

class StockMovementSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(), source='product', write_only=True)

    class Meta:
        model = StockMovement
        fields = ['id', 'product', 'product_id', 'change', 'reason', 'note', 'created_by', 'created_at']
        read_only_fields = ['created_by', 'created_at']
 
class SignupSerializer(serializers.Serializer):
    name = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, min_length=12)

    def validate_email(self, value):
        if User.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError("A user with that email already exists,put another one.")
        return value

    def create(self, validated_data):
        name = validated_data.get('name')
        email = validated_data.get('email')
        password = validated_data.get('password')
        user = User.objects.create_user(username=email, email=email, first_name=name)
        user.set_password(password)
        user.save()
        return user
