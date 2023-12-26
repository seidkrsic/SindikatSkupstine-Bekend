from django.contrib import admin
from django import forms
from multiupload.fields import MultiFileField  # Import the MultiFileField
from .models import CompanyDocument, Document, ImportantDocument, News, Image, Agenda_Item, Session, Company 
from django.utils.html import format_html
# Register your models here.
from django.db.models.signals import pre_save
from django.dispatch import receiver
from unidecode import unidecode

class ImageInline(admin.TabularInline):
    model = Image
    fields = ["image_preview", 'image_url']
    readonly_fields = ["image_preview"]
    extra = 0

    def image_preview(self, obj):
        if obj.image_url:
            return format_html(f'<img src="/images/{obj.image_url}" style="max-width: 100px; max-height: 100px;" />')
        else:
            return 'No image'
   
    

class CompanyDocumentsInline(admin.TabularInline):
    model = CompanyDocument
    exclude = ["title_cyrillic"]
    extra = 0



class Agenda_ItemsInline(admin.TabularInline):
    model = Agenda_Item
    exclude = ["title_cyrillic"]
    extra = 0

class DocumentsInline(admin.TabularInline):
    model = Document
    exclude = ["title_cyrillic"]
    extra = 0


class Agenda_ItemsAdmin(admin.ModelAdmin):
    # Customize the child model admin as needed
    exclude = ["title_cyrillic"]
    # Override get_model_perms to hide the child model from admin index
    def get_model_perms(self, request):
        """
        Return an empty dictionary to hide the model from the admin index.
        """
        return {}

class DocumentsAdmin(admin.ModelAdmin):
    # Customize the child model admin as needed
    exclude = ["title_cyrillic"]
    # Override get_model_perms to hide the child model from admin index
    def get_model_perms(self, request):
        """
        Return an empty dictionary to hide the model from the admin index.
        """
        return {}

class CompanyDocumentsAdmin(admin.ModelAdmin):
    # Customize the child model admin as needed
     def get_model_perms(self, request):
        """
        Return an empty dictionary to hide the model from the admin index.
        """
        return {}


class CompanyAdmin(admin.ModelAdmin):
    # Customize the child model admin as needed
    inlines = [CompanyDocumentsInline]
    list_display = ['company_name', "created"]
    exclude = ['company_name_cyrillic', "company_address_cyrillic"]
    list_filter = ['created']




class ImportantDocumentsForm(forms.ModelForm):
    class Meta:
        model = ImportantDocument
        fields = '__all__'
        widgets = {
                'important': forms.RadioSelect(choices=((True, 'Yes'), (False, 'No'))), 
                'legislation': forms.RadioSelect(choices=((True, 'Yes'), (False, 'No'))), 
                'laws': forms.RadioSelect(choices=((True, 'Yes'), (False, 'No'))), 
                'regulations': forms.RadioSelect(choices=((True, 'Yes'), (False, 'No'))), 
                'other': forms.RadioSelect(choices=((True, 'Yes'), (False, 'No'))), 
                'main': forms.RadioSelect(choices=((True, 'Yes'), (False, 'No'))), 
            
        }

class ImportantDocumentsAdmin(admin.ModelAdmin):
    # Customize the child model admin as needed
    form = ImportantDocumentsForm
    list_filter = ['created']
    list_display = ['title', "created"]
    exclude = ['title_cyrillic']
    
    def save_model(self, request, obj, form, change):
        obj.save()
   


@receiver(pre_save, sender=ImportantDocument)
@receiver(pre_save, sender=CompanyDocument)
@receiver(pre_save, sender=Document)
def convert_filenames(sender, instance, **kwargs):
    # Konverzija imena fajla
    if instance.file:
        original_filename = instance.file.name
        ascii_filename = unidecode(original_filename)
        instance.file.name = f"{ascii_filename}"


@receiver(pre_save, sender=Image)
@receiver(pre_save, sender=News)
def convert_image_filenames(sender, instance, **kwargs):
    # Konverzija imena fajla
    if instance.image_url:
        original_filename = instance.image_url.name
        ascii_filename = unidecode(original_filename)
        instance.image_url.name = f'{ascii_filename}'

class ImagesAdmin(admin.ModelAdmin):
    # Customize the child model admin as needed
    list_filter = ['created']
    list_display = ['image_url', "image" ,"created"]

    def image(self, obj): 
        if obj.image_url: 
            return format_html(f"<img src='/images/{obj.image_url}' alt='img' style='width: 50px; height: 50px' />")
        else: 
            return None

    # Override get_model_perms to hide the child model from admin index
    def get_model_perms(self, request):
        """
        Return an empty dictionary to hide the model from the admin index.
        """
        return {}
    

class SessionAdmin(admin.ModelAdmin): 
    inlines = [Agenda_ItemsInline, DocumentsInline]
    exclude = ['title_cyrillic']
    list_filter = ['created', "category"]
    list_display = ['title', "category", "created"]
    radio_fields = {"category" : admin.HORIZONTAL}



class NewsAdminForm(forms.ModelForm):
    # Define your other fields here
    gallery = MultiFileField(max_file_size=1024 * 1024 * 5, max_num=30, required=False)
    class Meta:
        model = News
        fields = '__all__'


class NewsAdmin(admin.ModelAdmin):
    form = NewsAdminForm  # Use the custom admin form
    inlines = [ImageInline]
    readonly_fields = ['owner']
    exclude = ['title_cyrillic', 'content_cyrillic']
    list_display = ["title", "created", 'main'] 
    list_filter = ['created', 'main']


    def save_model(self, request, obj, form, change):
        if not obj.owner and request.user.is_authenticated:
            obj.owner = request.user.profile 
        
        obj.save()
        print(request.FILES)
        for file in request.FILES.getlist("gallery"):    
            file_format = file.content_type
            print("File format:", file_format)
            if file_format in ['image/jpeg', 'image/jpg', 'image/png']:
                    news_image = Image(news=obj, image_url=f'{file.image_url}')
                    news_image.save()
            else:
                print("Skipping non-image file:", file)



admin.site.register(News, NewsAdmin)
admin.site.register(Session, SessionAdmin)
admin.site.register(Agenda_Item, Agenda_ItemsAdmin)
admin.site.register(Document, DocumentsAdmin) 
admin.site.register(Image, ImagesAdmin)
admin.site.register(ImportantDocument, ImportantDocumentsAdmin)
admin.site.register(Company, CompanyAdmin)
admin.site.register(CompanyDocument, CompanyDocumentsAdmin)

