from rest_framework import serializers 
from sindikat_app.models import Agenda_Item, Company, CompanyDocument, Document, News, Image, Session, ImportantDocument
from user_app.models import Profile 
from django.conf import settings




class ProfileSerializer(serializers.ModelSerializer): 
    profile_image = serializers.SerializerMethodField()
    active_role = serializers.SerializerMethodField()
    class Meta: 
        model = Profile
        fields = "__all__"
    
    def get_active_role(request, obj): 
        if obj.active_president: 
            return ("Predsjednik", "Предсједник")
        elif obj.vice_president: 
            return ("Zamjenik Predsjednika", "Замјеник Предсједника")
        elif obj.board_member: 
            return ("Član Izvršnog Odbora", "Члан Извршног Одбора")
        elif obj.commission:
            return ("Član Statutarne Komisije", "Члан Статутарне Комисије")
        elif obj.secretary: 
            return ("Generalni Sekretar", "Генерални Секретар")
        elif obj.president: 
            return ("Bivši Predsjednik", "Бивши Предсједник")
        else: 
            return ("Član Sindikata", "Члан Синдиката")
        


    def get_profile_image(self,obj): 
        profile_image = settings.IMAGES_URL + str(obj.profile_image)
        return profile_image 

class ImportantDocumentSerializer(serializers.ModelSerializer): 
    file = serializers.SerializerMethodField()
    download_link = serializers.SerializerMethodField()
    created_eu_time = serializers.SerializerMethodField()
    class Meta: 
        model = ImportantDocument
        fields = "__all__"
    
    def get_file(self,obj): 
        file = settings.IMAGES_URL + str(obj.file)
        return file

    def get_download_link(self,obj): 
        download_link = "http://www.apisindikat.skupstina.me/api/importantDocuments/" + str(obj.id) + "/download/" 
        return download_link
    
    def get_created_eu_time(self,obj): 
        return obj.created_eu_time


class Agenda_ItemsSerializer(serializers.ModelSerializer): 
    class Meta: 
        model = Agenda_Item
        fields = "__all__"


class CompanySerializer(serializers.ModelSerializer): 
    document = serializers.SerializerMethodField()
    class Meta: 
        model = Company
        fields = "__all__"

    def get_document(self,obj): 
        serializers = CompanyDocumentSerializer(instance=obj.company_documents, many=False)
        return serializers.data

class CompanyDocumentSerializer(serializers.ModelSerializer): 
    download_link = serializers.SerializerMethodField()
    file = serializers.SerializerMethodField()
    created_eu_time = serializers.SerializerMethodField()
    class Meta: 
        model = CompanyDocument
        fields = "__all__"
    
    def get_file(self,obj): 
        file = settings.IMAGES_URL + str(obj.file)
        return file
    
    def get_download_link(self,obj): 
        download_link = "http://www.apisindikat.skupstina.me/api/importantDocuments/" + str(obj.id) + "/download/" 
        return download_link
    
    def get_created_eu_time(self,obj): 
        return obj.created_eu_time



class DocumentSerializer(serializers.ModelSerializer): 
    download_link = serializers.SerializerMethodField()
    created_eu_time = serializers.SerializerMethodField()
    class Meta: 
        model = Document
        fields = "__all__"
    
    def get_download_link(self,obj): 
        download_link = "http://www.apisindikat.skupstina.me/api/importantDocuments/" + str(obj.id) + "/download/" 
        return download_link
    
    def get_created_eu_time(self,obj): 
        return obj.created_eu_time


class SessionSerializer(serializers.ModelSerializer): 
    agenda_items = serializers.SerializerMethodField()
    documents = serializers.SerializerMethodField()
    created_eu_time = serializers.SerializerMethodField()
    class Meta: 
        model = Session
        fields = "__all__" 
    
    def get_agenda_items(self, obj): 
        agenda_items = obj.agenda_items 
        serializer = Agenda_ItemsSerializer(instance=agenda_items, many=True)
        return serializer.data 
    
    def get_documents(self,obj): 
        documents = obj.documents 
        serializer = DocumentSerializer(instance=documents, many=True)
        return serializer.data
    
    def get_created_eu_time(self,obj): 
        return obj.created_eu_time
    



class ImageSerializer(serializers.ModelSerializer): 
    image_url = serializers.SerializerMethodField()
    class Meta: 
        model = Image 
        fields = ['image_url']
    
    def get_image_url(self,obj): 
        profile_image = settings.IMAGES_URL + str(obj.image_url)
        return profile_image 



class ImageSerializerForSlides(serializers.ModelSerializer): 
    image_url = serializers.SerializerMethodField()
    class Meta: 
        model = Image 
        fields = '__all__'
    
    def get_image_url(self,obj): 
        profile_image = settings.IMAGES_URL + str(obj.image_url)
        return profile_image 



class NewsSerializerForSlides(serializers.ModelSerializer): 
    owner = ProfileSerializer(many=False) 
    image_url = serializers.SerializerMethodField()
    class Meta: 
        model = News
        fields = "__all__"
    
    def get_image_url(self,obj): 
        profile_image = settings.IMAGES_URL + str(obj.image_url)
        return profile_image 



class NewsSerializer(serializers.ModelSerializer): 
    owner = ProfileSerializer() 
    image_url = serializers.SerializerMethodField()
    gallery = serializers.SerializerMethodField()
    created_eu_time = serializers.SerializerMethodField()
    
    class Meta: 
        model = News
        fields = "__all__"
    
    def get_image_url(self,obj): 
        profile_image = settings.IMAGES_URL + str(obj.image_url)
        return profile_image 
    
    def get_created_eu_time(self,obj): 
        return obj.created_eu_time
    
    def get_gallery(self, obj):
        gallery = obj.gallery 
        serializer = ImageSerializer(instance=gallery, many=True)
        return serializer.data  

   