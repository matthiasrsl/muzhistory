from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def app(request, route):
    return render(request, "frontend/index.html")