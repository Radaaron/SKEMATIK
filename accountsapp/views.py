from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from schematicsapp.models import SchematicModel, TagModel
from schematicsapp.views import upload_schematic
from django.contrib.sessions.models import Session
from django.conf import settings
from schematicsapp.forms import UploadImageForm
from schematicsapp.views import upload_schematic
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from accountsapp.forms import AuthenticationForm
from accountsapp.forms import RegisterForm


def Login(request):
    auth_form = AuthenticationForm(None, request.POST or None)
    if request.method == "POST":
        if auth_form.is_valid():
            username = auth_form.cleaned_data.get('username')
            password = auth_form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user != None:
                if user.is_active:
                    login(request, user, backend = None)
                    return HttpResponseRedirect('/home/')
                else:
                    return HttpResponse("Inactive user.")
            else:
                return HttpResponse("User does not exist.")
    return render(request, "login.html", {'form':auth_form})

def Register(request):
    register_form = RegisterForm(data = request.POST or None)
    if request.method == 'POST':
        if register_form.is_valid():
            username = register_form.cleaned_data.get("username")
            first_name = register_form.cleaned_data.get("first_name")
            last_name = register_form.cleaned_data.get("last_name")
            email = register_form.cleaned_data.get("email")
            password1 = register_form.cleaned_data.get("password1")
            password2 = register_form.cleaned_data.get("password2")
            user = register_form.save(commit = False)
            user.save()
            login(request, user, backend = None)
            return HttpResponseRedirect('/home/')
        else:
            print("INVALID FORM")
            return HttpResponseRedirect('/login/')
    else:
        register_form = RegisterForm()
    return render(request, "login.html", {'redirect_to': next, 'reg_form':register_form})

def Logout(request):
    logout(request)
    return HttpResponseRedirect('/login/')

@login_required
def Home(request):
    session_key = request.COOKIES.get(settings.SESSION_COOKIE_NAME, None)
    session = Session.objects.get(session_key=session_key)
    session_data = session.get_decoded()
    uid = session_data.get('_auth_user_id')
    images = SchematicModel.objects.filter(user_id=uid)
    search_query = request.GET.get('searchquery')
    if search_query:
        tag_queryset = TagModel.objects.filter(tag_name=search_query)
        images = SchematicModel.objects.filter(user_id=uid).filter(schematic_tags__in=tag_queryset)
    paginator = Paginator(images, 6)
    upload_schematic(request)
    return render(request, "home.html", {'images': images})
