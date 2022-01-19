from django.http import Http404, JsonResponse, HttpResponse, HttpResponseRedirect
from django.shortcuts import render

from django.urls import reverse

def index(request):
    return render(request, 'mainApp/homepage.html')
