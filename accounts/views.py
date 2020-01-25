from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def display_profile(request):
    profile = request.user.profile
    
    return render(request, 'accounts/display_profile.html', locals())
