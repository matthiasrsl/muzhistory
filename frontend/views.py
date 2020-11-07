from django.shortcuts import render

def app(request, route):
    return render(request, "frontend/index.html")