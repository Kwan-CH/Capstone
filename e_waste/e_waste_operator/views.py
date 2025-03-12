from django.shortcuts import render

def homepage(request):
    return render(request, 'operator/homepage-operator.html')
