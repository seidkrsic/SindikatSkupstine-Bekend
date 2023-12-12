from django.contrib import admin
from .models import Profile 
from django import forms 
from django.utils.html import format_html
# Register your models here.



class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = '__all__'
        widgets = {
            'active_president': forms.RadioSelect(choices=((True, 'Yes'), (False, 'No'))), 
            'vice_president': forms.RadioSelect(choices=((True, 'Yes'), (False, 'No'))),
            'president': forms.RadioSelect(choices=((True, 'Yes'), (False, 'No'))),
            'main_board_member': forms.RadioSelect(choices=((True, 'Yes'), (False, 'No'))), 
            'board_member': forms.RadioSelect(choices=((True, 'Yes'), (False, 'No'))),
            'commission': forms.RadioSelect(choices=((True, 'Yes'), (False, 'No'))),
    
        }


class ProfileAdmin(admin.ModelAdmin): 
    form = ProfileForm
    list_display = ["username", "image", "phone", "Role"]
    readonly_fields = ["user", "image", "username"]
    exclude = ["name_cyrillic", "bio_cyrillic"]

    def image(self, obj): 
        return format_html(f"<img src='/images/{obj.profile_image}' alt='img' style='width: 50px; height: 50px' />")

    def Role(self, obj): 
        # get_activ_role is a tuple ("predsjednik", "predsjednik na cirilici")
        return obj.get_active_role[0]

admin.site.register(Profile, ProfileAdmin)

