from django import forms
from django.core.validators import validate_email
from peat_uploader.models import PeatProject, PeatContractor
from django.contrib.auth.password_validation import validate_password

class PeatProjectForm(forms.ModelForm):
    
    class Meta:
        model = PeatProject
        fields =  ["name", "project_id"]


class PeatContractorForm(forms.ModelForm):

    class Meta:
        model = PeatContractor
        fields = ["name", "contact_email"]

