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
        user=request.user
        if user.type == 2:
            return view_func(request, *args, **kwargs)
        else:
            return HttpResponse("Chức năng này chỉ dành cho Staff!")
    return function

def guest_only(view_func):
    def function(request, *args, **kwargs):
        user=request.user
        if user.type == 3:
            return view_func(request, *args, **kwargs)
        else:
            return HttpResponse("Chức năng này chỉ dành cho Guest!")
    return function

def user_only(view_func):
    def function(request, *args, **kwargs):
        user=request.user
        if user.type == 0:
            return view_func(request, *args, **kwargs)
        else:
            return HttpResponse("Chức năng này chỉ dành cho User!")
    return function
