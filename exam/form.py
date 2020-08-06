from django import forms
from .models import Profile
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [
            "firstname",
            "lastname",
            "school_name",
            "school_city",
            "About_me",
            "Class",
            "Mobile",
        ]
class SchoolForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [
            'school_name',
            'school_logo',
            'school_address',
            'school_city',
            'school_state',
            'school_country',
            'school_pincode',
            'school_contact_person',
            'school_email',
            'school_mobile',
        ]
