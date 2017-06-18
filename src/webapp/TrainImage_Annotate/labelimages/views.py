from django.http import HttpResponse
from django.shortcuts import render

def index(request):
	return render(request, 'index.html', {})
    #return HttpResponse("Hello, world. You're at the label images index.")

def upload_pic(request, pk):
	return HttpResponse("Hello, world. You're at the label images index.")