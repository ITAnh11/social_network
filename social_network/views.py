from django.http import HttpResponse

def handler404(request, exception):
    return HttpResponse("page not found bruh")