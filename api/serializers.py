from rest_framework import serializers 
from sindikat_app.models import Agenda_Item, Company, CompanyDocument, Document, News, Image, Session, ImportantDocument
from user_app.models import Profile 
from django.conf import settings
from bs4 import BeautifulSoup



def remove_dollars_sign(text): 
    test_text = text.split(" ")
    translated_text = ''
    for word in test_text: 
        if word[0:2] == "$$" and word[-2:] == "$$": 
            translated_text += word[2:len(word)-2] + " "
            continue  
        else: 
            translated_text += word + " "
    return translated_text


class ProfileSerializer(serializers.ModelSerializer): 
    profile_image = serializers.SerializerMethodField()
    active_role = serializers.SerializerMethodField()
    nice_bio = serializers.SerializerMethodField()
    class Meta: 
        model = Profile
        fields = "__all__"
    
    def get_active_role(request, obj): 
        if obj.active_president: 
            if obj.male_female == True: 
                return ("Predsjednica", "Предсједница")
            return ("Predsjednik", "Предсједник")
        elif obj.vice_president: 
            if obj.male_female == True:
                  return ("Zamjenica predsjednika", "Замјеница предсједника")
            return ("Zamjenik predsjednika", "Замјеник предсједника")
        elif obj.board_member: 
            if obj.male_female == True:
                return ("Članica Izvršnog odbora", "Чланица Извршног одбора")
            return ("Član Izvršnog odbora", "Члан Извршног одбора")
        elif obj.commission:
            if obj.male_female == True:
                return ("Članica Statutarne komisije", "Чланица Статутарне комисије")
            return ("Član Statutarne komisije", "Члан Статутарне комисије")
        elif obj.main_board_member: 
            return ("Nadzorni odbor", "Надзорни одбор")
        elif obj.president: 
            if obj.male_female == True:
                return ("Ranija predsjednica", "Ранија Предсједница")
            return ("Raniji predsjednik", "Ранији предсједник")
        else: 
            if obj.male_female == True:
                return ("Članica sindikata", "Чланица синдиката")
            return ("Član sindikata", "Члан синдиката")
        


    def get_profile_image(self,obj): 
        profile_image = settings.IMAGES_URL + str(obj.profile_image)
        return profile_image 
    
    def get_nice_bio(self,obj): 
        content = obj.bio 
        if obj.bio: 
            soup = BeautifulSoup(content, 'html.parser')

            # Translate text nodes within the HTML
            for element in soup.find_all(string=True):
                if element.parent.name not in ['script', 'style']:
                    translated_text = remove_dollars_sign(element.string)
                    element.string.replace_with(translated_text)
            # Print the modified HTML content
            soup = str(soup) 
            return soup 
        else: 
            return ""


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
        download_link = "https://apisindikat.skupstina.me/api/importantDocuments/" + str(obj.id) + "/download/" 
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
        if len(obj.company_documents) != 0:
            serializers = CompanyDocumentSerializer(instance=obj.company_documents, many=False)
            return serializers.data
        return {}

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
        download_link = "https://apisindikat.skupstina.me/api/importantDocuments/" + str(obj.id) + "/download/" 
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
        download_link = "https://apisindikat.skupstina.me/api/importantDocuments/" + str(obj.id) + "/download/" 
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
    nice_content = serializers.SerializerMethodField()
    nice_title = serializers.SerializerMethodField()
    class Meta: 
        model = News
        fields = "__all__"
    
    def get_image_url(self,obj): 
        profile_image = settings.IMAGES_URL + str(obj.image_url)
        return profile_image 
    
    def get_nice_title(self, obj): 
        if obj.title: 
            return remove_dollars_sign(obj.title)
        else: 
            return ""

    def get_nice_content(self,obj): 
        if obj.content: 
            soup = BeautifulSoup(obj.content, 'html.parser')

            # Translate text nodes within the HTML
            for element in soup.find_all(string=True):
                if element.parent.name not in ['script', 'style']:
                    translated_text = remove_dollars_sign(element.string)
                    element.string.replace_with(translated_text)
            # Print the modified HTML content
            soup = str(soup) 
            return soup 
        else: 
            return ""

class NewsSerializer(serializers.ModelSerializer): 
    owner = ProfileSerializer() 
    image_url = serializers.SerializerMethodField()
    gallery = serializers.SerializerMethodField()
    created_eu_time = serializers.SerializerMethodField()
    nice_content = serializers.SerializerMethodField()
    nice_title = serializers.SerializerMethodField()
    
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

    def get_nice_title(self, obj): 
        if obj.title: 
            return remove_dollars_sign(obj.title)
        else: 
            return ""

    def get_nice_content(self,obj): 
        if obj.content: 
            soup = BeautifulSoup(obj.content, 'html.parser')

            # Translate text nodes within the HTML
            for element in soup.find_all(string=True):
                if element.parent.name not in ['script', 'style']:
                    translated_text = remove_dollars_sign(element.string)
                    element.string.replace_with(translated_text)
            # Print the modified HTML content
            soup = str(soup) 
            return soup 
        else: 
            return ""
