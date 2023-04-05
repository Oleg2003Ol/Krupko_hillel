from django.shortcuts import render


def products(request, *args, **kwargs):
    return render(request, 'feedbacks/index.html')
