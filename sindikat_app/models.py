from django.db import models
import uuid 
from django.conf import settings
from user_app.models import Profile 
from ckeditor.fields import RichTextField
from django.db.models.signals import pre_save
from django.dispatch import receiver
import string 
# Create your models here.


class Company(models.Model): 
    class Meta:
        verbose_name = 'Company'
        verbose_name_plural = 'Companies'
    company_name = models.CharField(max_length=1000, blank=False)  
    company_address = models.CharField(max_length=1000, blank=False)  
    company_name_cyrillic = models.CharField(max_length=1000, blank=True, null=True)  
    company_address_cyrillic = models.CharField(max_length=1000, blank=True, null=True)  
    rates =  models.CharField(max_length=1000, blank=True, null=True) 
    created = models.DateTimeField(auto_now_add=True) 
    id = models.UUIDField(default=uuid.uuid4,unique=True, 
                                    primary_key=True, editable=False) 
    def __str__(self): 
        return self.company_name
    
    @property
    def documents(self): 
        return self.company_documents

class ImportantDocument(models.Model): 
    class Meta:
        verbose_name = 'Single Document'
        verbose_name_plural = 'Single Documents'
    file = models.FileField(upload_to='documents/', blank=True, null=True)
    important = models.BooleanField(default=False, null=True)
    title = models.CharField(max_length=200, blank=False, null=True) 
    title_cyrillic = models.CharField(max_length=200, blank=True, null=True) 
    created = models.DateTimeField(auto_now_add=True) 
    id = models.UUIDField(default=uuid.uuid4,unique=True, 
                                    primary_key=True, editable=False) 
    
    def __str__(self):
        try: 
            return self.title
        except: 
            return "File name not Created"

    @property
    def created_eu_time(self): 
        return str(self.created)[8:10] + "-" + str(self.created)[5:7] + "-" + str(self.created)[:4]

class Document(models.Model): 
    class Meta:
        verbose_name = 'Session Document'
        verbose_name_plural = 'Session Documents'
    session = models.ForeignKey("Session", null=True, blank=True, on_delete=models.SET_NULL, related_name="documents")
    file = models.FileField(upload_to='documents/', blank=True, null=True)
    title = models.CharField(max_length=200, blank=False)
    title_cyrillic = models.CharField(max_length=200, blank=True)
    created = models.DateTimeField(auto_now_add=True) 
    id = models.UUIDField(default=uuid.uuid4,unique=True, 
                                    primary_key=True, editable=False) 
    
    def __str__(self):
        return str(self.title)
    
    @property
    def created_eu_time(self): 
        return str(self.created)[8:10] + "-" + str(self.created)[5:7] + "-" + str(self.created)[:4]

class CompanyDocument(models.Model): 
    class Meta:
        verbose_name = 'Company Document'
        verbose_name_plural = 'Company Documents'
    company = models.OneToOneField(Company, on_delete=models.CASCADE, blank=True, null=True, related_name='company_documents')
    file = models.FileField(upload_to='documents/', blank=True, null=True)
    title = models.CharField(max_length=200, blank=False)
    title_cyrillic = models.CharField(max_length=200, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True) 
    id = models.UUIDField(default=uuid.uuid4,unique=True, 
                                    primary_key=True, editable=False) 
    
    def __str__(self):
        return self.title
    
    @property
    def created_eu_time(self): 
        return str(self.created)[8:10] + "-" + str(self.created)[5:7] + "-" + str(self.created)[:4]

class Agenda_Item(models.Model): 
    class Meta:
        verbose_name = 'Session Agenda Item'
        verbose_name_plural = 'Session Agenda Items'
    session = models.ForeignKey("Session", null=True, blank=False, on_delete=models.CASCADE, related_name="agenda_items")
    title = models.CharField(max_length=200, blank=False, null=True)
    title_cyrillic= models.CharField(max_length=200, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True) 
    id = models.UUIDField(default=uuid.uuid4,unique=True, 
                                    primary_key=True, editable=False)
    def __str__(self):
        return self.title 


class Session(models.Model): 
    SESSION_CATEGORIES = (('skupstina', 'Skupština'), ("izvrsni_odbor", "Izvršni Odbor"))
    class Meta: 
        ordering = ['-created']

    title = models.CharField(max_length=200, blank=False, null=True)
    title_cyrillic= models.CharField(max_length=200, blank=True, null=True)
    category = models.CharField(choices=SESSION_CATEGORIES, null=True, max_length=200)  
    created = models.DateField(default=None,null=True)
    id = models.UUIDField(default=uuid.uuid4,unique=True, 
                                    primary_key=True, editable=False) 
    
    
    def __str__(self):
        return self.title
    
    @property
    def created_eu_time(self): 
        return str(self.created)[8:10] + "-" + str(self.created)[5:7] + "-" + str(self.created)[:4]


class Image(models.Model): 
    news = models.ForeignKey("News",null=True, blank=True, on_delete=models.CASCADE, related_name="images")
    image_url = models.ImageField(blank=True, null=True, upload_to='', default='')
    created = models.DateTimeField(auto_now_add=True) 
    id = models.UUIDField(default=uuid.uuid4,unique=True, 
                                    primary_key=True, editable=False) 
    def __str__(self):
        return "Slika za Vijest: " + str(self.news)




class News(models.Model): 
    class Meta:
        verbose_name = 'News'
        verbose_name_plural = 'News'
        ordering = ['-created']

   
    title = models.CharField(max_length=200, blank=False, null=True)
    title_cyrillic = models.CharField(max_length=200, blank=True, null=True)
    main = models.BooleanField(default=False, blank=True)
    image_url = models.ImageField(blank=True, null=True, upload_to="", default=f"ArtBoard_2.png")
    content = RichTextField(null=True)
    content_cyrillic = RichTextField(null=True, blank=True)
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, blank=True)     
    created = models.DateField(default=None,null=True)
    id = models.UUIDField(default=uuid.uuid4,unique=True, 
                                    primary_key=True, editable=False) 
    
    def __str__(self):
        return self.title 
    
    @property
    def gallery(self): 
        return self.images 
    
    @property
    def created_eu_time(self): 
        return str(self.created)[8:10] + "-" + str(self.created)[5:7] + "-" + str(self.created)[:4]
 



LATINIC_TO_CYRILLIC = {
    'a': 'а', 'A': 'А',
    'b': 'б', 'B': 'Б',
    'c': 'ц', 'C': 'Ц',
    'č': 'ч', 'Č': 'Ч',
    'ć': 'ћ', 'Ć': 'Ћ',
    'd': 'д', 'D': 'Д',
    'dž': 'џ', 'Dž': 'Џ', 'DŽ': 'Џ',
    'đ': 'ђ', 'Đ': 'Ђ',
    'e': 'е', 'E': 'Е',
    'f': 'ф', 'F': 'Ф',
    'g': 'г', 'G': 'Г',
    'h': 'х', 'H': 'Х',
    'i': 'и', 'I': 'И',
    'j': 'ј', 'J': 'Ј',
    'k': 'к', 'K': 'К',
    'l': 'л', 'L': 'Л',
    'lj': 'љ', 'Lj': 'Љ', 'LJ': 'Љ',
    'm': 'м', 'M': 'М',
    'n': 'н', 'N': 'Н',
    'nj': 'њ', 'Nj': 'Њ', 'NJ': 'Њ',
    'o': 'о', 'O': 'О',
    'p': 'п', 'P': 'П',
    'r': 'р', 'R': 'Р',
    's': 'с', 'S': 'С',
    'š': 'ш', 'Š': 'Ш',
    't': 'т', 'T': 'Т',
    'u': 'у', 'U': 'У',
    'v': 'в', 'V': 'В',
    'z': 'з', 'Z': 'З',
    'ž': 'ж', 'Ž': 'Ж'
}

# HERE ARE SIGNALS FOR CYRILLIC 
from django.db.models.signals import pre_save
from django.dispatch import receiver
from bs4 import BeautifulSoup



def translate_latinic_to_cyrillic(text):
    if text[0:2] == "$$" and text[-2:] == "$$": 
        return text  
    translated_text = ''
    char = 0
    while char < len(text):
        if text[char] not in string.punctuation:
            if text[char] == "L" or text[char] == "l":
                if char + 1 < len(text) and text[char + 1] == "j":
                    translated_char = LATINIC_TO_CYRILLIC.get(text[char:char + 2], text[char:char + 2])
                    translated_text += translated_char
                    char = char + 2
                else:
                    translated_char = LATINIC_TO_CYRILLIC.get(text[char], text[char])
                    translated_text += translated_char
                    char = char + 1
            elif text[char] == "N" or text[char] == "n":
                if char + 1 < len(text) and text[char + 1] == "j":
                    translated_char = LATINIC_TO_CYRILLIC.get(text[char:char + 2], text[char:char + 2])
                    translated_text += translated_char
                    char = char + 2
                else:
                    translated_char = LATINIC_TO_CYRILLIC.get(text[char], text[char])
                    translated_text += translated_char
                    char = char + 1
            elif text[char] == "D" or text[char] == "d":
                if char + 1 < len(text) and text[char + 1] == "\u017E":
                    translated_char = LATINIC_TO_CYRILLIC.get(text[char:char + 2], text[char:char + 2])
                    translated_text += translated_char
                    char = char + 2
                else:
                    translated_char = LATINIC_TO_CYRILLIC.get(text[char], text[char])
                    translated_text += translated_char
                    char = char + 1
            else:
                translated_char = LATINIC_TO_CYRILLIC.get(text[char], text[char])
                translated_text += translated_char
                char = char + 1
        else:
            translated_text += text[char]
            char = char + 1

    return translated_text




@receiver(pre_save, sender=ImportantDocument)
def translate_and_populate(sender, instance, **kwargs):
    if instance.title:  # Assuming name_latinic is the field to be translated
        translated_name = translate_latinic_to_cyrillic(instance.title)
        instance.title_cyrillic = translated_name


@receiver(pre_save, sender=Document)
def translate_and_populate(sender, instance, **kwargs):
    if instance.title:  # Assuming name_latinic is the field to be translated
        translated_name = translate_latinic_to_cyrillic(instance.title)
        instance.title_cyrillic = translated_name

@receiver(pre_save, sender=Agenda_Item)
def translate_and_populate(sender, instance, **kwargs):
    if instance.title:  # Assuming name_latinic is the field to be translated
        translated_name = translate_latinic_to_cyrillic(instance.title)
        instance.title_cyrillic = translated_name


@receiver(pre_save, sender=Session)
def translate_and_populate(sender, instance, **kwargs):
    if instance.title:  # Assuming name_latinic is the field to be translated
        translated_name = translate_latinic_to_cyrillic(instance.title)
        instance.title_cyrillic = translated_name
    


@receiver(pre_save, sender=Company)
def translate_and_populate(sender, instance, **kwargs):
    if instance.company_name:  # Assuming name_latinic is the field to be translated
        translated_name = translate_latinic_to_cyrillic(instance.company_name)
        instance.company_name_cyrillic = translated_name
    if instance.company_address: 
        translated_name = translate_latinic_to_cyrillic(instance.company_address)
        instance.company_address_cyrillic = translated_name

    
@receiver(pre_save, sender=CompanyDocument)
def populate_content_cyrillic(sender, instance, **kwargs): 
    if instance.title:  # Assuming name_latinic is the field to be translated
        translated_name = translate_latinic_to_cyrillic(instance.title)
        instance.title_cyrillic = translated_name

@receiver(pre_save, sender=News)
def populate_content_cyrillic(sender, instance, **kwargs): 
    if instance.title:  # Assuming name_latinic is the field to be translated
        translated_name = translate_latinic_to_cyrillic(instance.title)
        instance.title_cyrillic = translated_name

    # if not instance.owner:
    #     instance.owner = request.user.profile

    
    content = instance.content 
    # Parse the HTML content using Beautiful Soup
    soup = BeautifulSoup(content, 'html.parser')

    # Translate text nodes within the HTML
    for element in soup.find_all(string=True):
        if element.parent.name not in ['script', 'style']:
            translated_text = translate_latinic_to_cyrillic(element.string)
            element.string.replace_with(translated_text)
    # Print the modified HTML content
    soup = str(soup) 
    instance.content_cyrillic = soup



# _________________________________________________________________________