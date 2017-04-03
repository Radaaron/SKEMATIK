from django.shortcuts import render, HttpResponseRedirect
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.contrib.sessions.models import Session
from django.contrib.auth.models import User
from django.views.generic import ListView
from .forms import UploadImageForm, EditSchematicForm, AddTagForm
from .models import SchematicModel, TagModel


def upload_schematic(request):
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
        # find schematic based on pk
        schemID = form.cleaned_data.get("schemID")
        schem = SchematicModel.objects.get(id=schemID)
        # update schematic details
        schem.schematic_name = form.cleaned_data.get("name")
        schem.schematic_description = form.cleaned_data.get("description")
        schem.save()
        return HttpResponseRedirect('/home/')
    print("Invalid Form")
    # default
    return render(request, 'home.html', {'user': request.user})

def add_schematic_tag(request):
    form = AddTagForm(request.POST, request.FILES)
    if form.is_valid():
        # find schematic based on pk
        schemID = form.cleaned_data.get("schemID")
        schem = SchematicModel.objects.get(id=schemID)
        # create new tag
        tag = TagModel()
        tag.tag_name = form.cleaned_data.get("name")
        tag.user_id = schem.user_id
        tag.save()
        # add tag to schematic
        schem.schematic_tags.add(tag)
        return HttpResponseRedirect('/home/')
    print("Invalid Form")
    # default
    return render(request, 'home.html', {'user': request.user})
