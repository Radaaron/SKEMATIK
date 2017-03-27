from django.shortcuts import render, HttpResponseRedirect
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.contrib.sessions.models import Session
from django.contrib.auth.models import User
from django.views.generic import ListView
from .forms import UploadImageForm, EditSchematicForm
from .models import SchematicModel


def upload_schematic(request):
    if request.method == 'POST':
        form = UploadImageForm(request.POST, request.FILES)
        if form.is_valid():
            # getting the schematic info
            schem = SchematicModel()
            schem.schematic_name = form.cleaned_data.get("name")
            schem.schematic_description = form.cleaned_data.get("description")
            schem.schematic_image = form.cleaned_data.get("image")
            # getting session user id to assign schematic to user logged in
            session_key = request.COOKIES.get(settings.SESSION_COOKIE_NAME, None)
            session = Session.objects.get(session_key=session_key)
            session_data = session.get_decoded()
            uid = session_data.get('_auth_user_id')
            schem.user_id = uid
            # save schematic
            schem.save()
            return HttpResponseRedirect('/home/')
        print("Invalid Form")
    # default
    return render(request, 'home.html', {'user': request.user})

def edit_schematic(request):
    form = EditSchematicForm(request.POST, request.FILES)
    if form.is_valid():
        schemID = form.cleaned_data.get("schemID")
        # find schematic based on pk
        schem = SchematicModel.objects.get(id=schemID)
        schem.schematic_name = form.cleaned_data.get("name")
        schem.schematic_description = form.cleaned_data.get("description")
        schem.save()
        return HttpResponseRedirect('/home/')
    else:
        print("Invalid Form")
    # default
    return render(request, 'home.html', {'user': request.user})
