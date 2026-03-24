from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    UserViewSet, MyTokenObtainPairView, SignupAPIView, GoogleAuthPlaceholderView,
    ProductViewSet, SupplierViewSet, StockMovementViewSet, LowStockAlertsView,
    LowStockReportView, FastMovingReportView, SalesVsRestockReportView,
    DashboardStatsView
)
from rest_framework_simplejwt.views import TokenRefreshView

router = DefaultRouter()
router.register('users', UserViewSet, basename='user')
router.register('products', ProductViewSet, basename='product')
router.register('suppliers', SupplierViewSet, basename='supplier')
# register stock movements endpoint as "stock-movements"
router.register('stock-movements', StockMovementViewSet, basename='stockmovement')

urlpatterns = [
    path('', include(router.urls)),
    # Authentication placeholders
    path('auth/login/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/signup/', SignupAPIView.as_view(), name='signup'),
    path('auth/google/', GoogleAuthPlaceholderView.as_view(), name='auth_google'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # Alerts
    path('alerts/low-stock/', LowStockAlertsView.as_view(), name='low_stock_alerts'),
    # Reports
    path('reports/low-stock/', LowStockReportView.as_view(), name='report_low_stock'),
    path('reports/fast-moving/', FastMovingReportView.as_view(), name='report_fast_moving'),
    path('reports/sales-vs-restock/', SalesVsRestockReportView.as_view(), name='report_sales_vs_restock'),
    # Dashboard stats under /api/
    path('dashboard/stats/', DashboardStatsView.as_view(), name='api_dashboard_stats'),
]
