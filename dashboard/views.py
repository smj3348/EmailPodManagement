from django.http import HttpResponse
def home(request):
    return HttpResponse("✅ Django up. Monitoring portal coming soon.")
