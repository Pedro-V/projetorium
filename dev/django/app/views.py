from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def profile(request):
    template_name = 'profile.html'
    return render(request, template_name)
