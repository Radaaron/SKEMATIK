from django import forms

# fix form validations later

class UploadImageForm(forms.Form):
    name = forms.CharField()
    description = forms.CharField()
    image = forms.ImageField()

class EditSchematicForm(forms.Form):
    schemID = forms.IntegerField()
    name = forms.CharField()
    description = forms.CharField()

class DeleteSchematicForm(forms.Form):
    schemID = forms.IntegerField()

class AddTagForm(forms.Form):
    schemID = forms.IntegerField()
    name = forms.CharField()

class DeleteTagForm(forms.Form):
    schemID = forms.IntegerField()
