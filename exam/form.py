from django import forms
from .models import Profile
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [
            "firstname",
            "lastname",
            "schoolName",
            "city",
            "About_me",
            "Class",
            "Mobile",
        ]
