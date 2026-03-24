from rest_framework import viewsets, status
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import User, Product, Supplier, StockMovement
from .serializers import UserSerializer, MyTokenObtainPairSerializer, ProductSerializer, SupplierSerializer, StockMovementSerializer, SignupSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated, SAFE_METHODS
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import action
from django.db.models import F, Sum, Count, Q
from django.utils import timezone
from datetime import timedelta
from django.db.utils import OperationalError

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

    def get(self, request, *args, **kwargs):
        """
        Friendly GET response for browser access. POST remains the way to obtain tokens.
        """
        return Response({
            "detail": "This endpoint issues JWT tokens. Use POST with 'email'/'username' and 'password' to obtain tokens.",
            "post_example": {
                "username_or_email": "user@example.com",
                "password": "your_password"
            }
        }, status=status.HTTP_200_OK)

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class DashboardStatsView(APIView):
    """
    Minimal dashboard stats endpoint. Returns basic counts so the dashboard URL works.
    """
    def get(self, request, format=None):
        users_count = User.objects.count()
        data = {
            "users_count": users_count,
        }
        return Response(data)

# New endpoints / viewsets

class SignupAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        return Response({
            'user': UserSerializer(user).data,
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_201_CREATED)

class GoogleAuthPlaceholderView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        # Frontend placeholder. Backend integration required to actually verify Google token.
        return Response({'detail': 'Google OAuth placeholder. Connect backend to verify tokens.'}, status=status.HTTP_501_NOT_IMPLEMENTED)

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all().order_by('-updated_at')
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        # Allow anyone to list/retrieve (safe methods). Require auth for mutating actions.
        if self.request.method in SAFE_METHODS:
            return [AllowAny()]
        return [IsAuthenticated()]

class SupplierViewSet(viewsets.ModelViewSet):
    queryset = Supplier.objects.all().order_by('-created_at')
    serializer_class = SupplierSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.request.method in SAFE_METHODS:
            return [AllowAny()]
        return [IsAuthenticated()]

class StockMovementViewSet(viewsets.ModelViewSet):
    queryset = StockMovement.objects.all().order_by('-created_at')
    serializer_class = StockMovementSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.request.method in SAFE_METHODS:
            return [AllowAny()]
        return [IsAuthenticated()]

    def perform_create(self, serializer):
        # attach user if available
        serializer.save(created_by=self.request.user)

class LowStockAlertsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        low_products = Product.objects.filter(quantity__lte=F('min_stock_level')).order_by('quantity')
        serializer = ProductSerializer(low_products, many=True)
        return Response({'low_stock': serializer.data})

class LowStockReportView(APIView):
    """
    GET /api/reports/low-stock/
    Returns detailed low-stock report for frontend reporting/export.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            qs = Product.objects.filter(quantity__lte=F('min_stock_level')).order_by('quantity')
            serializer = ProductSerializer(qs, many=True)
            return Response({'report': serializer.data})
        except OperationalError as exc:
            return Response({'detail': 'DB schema mismatch. Run migrations.', 'error': str(exc), 'report': []}, status=200)

class FastMovingReportView(APIView):
    """
    GET /api/reports/fast-moving/
    Returns products ordered by number of 'sale' movements in the last 30 days.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            since = timezone.now() - timedelta(days=30)
            sales = (
                StockMovement.objects.filter(reason='sale', created_at__gte=since)
                .values('product')
                .annotate(sales_count=Count('id'))
                .order_by('-sales_count')[:50]
            )
            results = []
            product_map = {p.id: p for p in Product.objects.filter(id__in=[s['product'] for s in sales])}
            for s in sales:
                prod = product_map.get(s['product'])
                if prod:
                    results.append({
                        'product_id': prod.id,
                        'name': prod.name,
                        'category': prod.category,
                        'sales_count': s['sales_count'],
                        'quantity': prod.quantity,
                    })
            return Response({'fast_moving': results})
        except OperationalError as exc:
            return Response({'detail': 'DB schema mismatch. Run migrations.', 'error': str(exc), 'fast_moving': []}, status=200)

class SalesVsRestockReportView(APIView):
    """
    GET /api/reports/sales-vs-restock/
    Returns aggregated sums of adds/restocks vs sales/removals for the last 30 days.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            since = timezone.now() - timedelta(days=30)
            agg = StockMovement.objects.filter(created_at__gte=since).aggregate(
                total_added=Sum('change', filter=Q(change__gt=0)),
                total_removed=Sum('change', filter=Q(change__lt=0)),
            )
            # total_removed will be negative; convert to positive magnitude for frontend
            total_added = agg.get('total_added') or 0
            total_removed = -(agg.get('total_removed') or 0)
            return Response({
                'since': since.isoformat(),
                'total_added': total_added,
                'total_removed': total_removed,
            })
        except OperationalError as exc:
            return Response({'detail': 'DB schema mismatch. Run migrations.', 'error': str(exc), 'total_added': 0, 'total_removed': 0}, status=200)
