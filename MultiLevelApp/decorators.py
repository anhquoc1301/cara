from django.http import HttpResponse
from django.shortcuts import redirect, render
def admin_only(view_func):
    def function(request, *args, **kwargs):
        user=request.user.username
        if user=='admin':
            return view_func(request, *args, **kwargs)
        else:
            return HttpResponse("Chức năng này chỉ dành cho Admin!")
    return function

def staff_only(view_func):
    def function(request, *args, **kwargs):
        user=request.user.username
        if user=='staff':
            return view_func(request, *args, **kwargs)
        else:
            return HttpResponse("Chức năng này chỉ dành cho Staff!")
    return function
