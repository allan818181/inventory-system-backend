from django.http import JsonResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt    

@method_decorator(csrf_exempt, name='dispatch')
class DashboardStatsView(View):
    def get(self, request):
        return JsonResponse({"status": "OK", "message": "Dashboard stats working"})