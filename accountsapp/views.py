from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from schematicsapp.models import SchematicModel
from schematicsapp.views import upload_schematic
from django.contrib.sessions.models import Session
from django.conf import settings
from schematicsapp.forms import UploadImageForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

def Login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user != None:
            if user.is_active:
                login(request, user, backend=None)
                return HttpResponseRedirect('/home/')
            else:
                return HttpResponse("Inactive user.")
        else:
            return HttpResponse("User does not exist.")
    return render(request, "login.html")

def Register(request):
    if request.method == "POST":
        user = User.objects.create_user(username=request.POST['username'],
                                    email=request.POST['email'],
                                    password=request.POST['password'],
                                    first_name=request.POST['first_name'],
                                    last_name=request.POST['last_name'])
        user.save()
        if user != None:
            return HttpResponseRedirect('/login/')
        else:
            return render(request, "error.html", {})
    return render(request, "register.html", {'redirect_to': next})

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
    paginator = Paginator(images, 6)  # Show 25 contacts per page

    if request.method == 'POST':
        form = UploadImageForm(request.POST, request.FILES)
        if form.is_valid():
            # getting the schematic info
            schem = SchematicModel()
            schem.schematic_name = form.cleaned_data['name']
            schem.schematic_description = form.cleaned_data['description']
            schem.schematic_image = form.cleaned_data['image']
            # getting session user id to assign schematic to user logged in
            session_key = request.COOKIES.get(settings.SESSION_COOKIE_NAME, None)
            session = Session.objects.get(session_key=session_key)
            session_data = session.get_decoded()
            uid = session_data.get('_auth_user_id')
            schem.user_id = uid
            # save schematic
            schem.save()
            return HttpResponseRedirect('/home/')

    return render(request, "home.html", {'images': images})
