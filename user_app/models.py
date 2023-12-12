from django.db import models
from django.contrib.auth.models import User 
import uuid 
import string 
from ckeditor.fields import RichTextField
from django.conf import settings
from bs4 import BeautifulSoup

# Create your models here.

# HERE ARE SIGNALS FOR POST DELETE AND POST SAVE 
# -----------------------------------------------------------------------
from django.db.models.signals import post_save, post_delete 

from django.db.models.signals import pre_save
from django.dispatch import receiver



def createProfile(sender, instance, created, **kwargs):
    if created: 
        user = instance 
        profile = Profile.objects.create(
           user = user, 
           username = user.username, 
        )


def deleteUser(sender,instance,**kwargs): 
    try:
        user = instance.user 
        user.delete()
    except: 
        pass 
post_save.connect(createProfile,sender=User)
post_delete.connect(deleteUser,sender='user_app.Profile')

@receiver(pre_save, sender="user_app.Profile")
def populate_content_cyrillic(sender, instance, **kwargs):

    if instance.name:  # Assuming name_latinic is the field to be translated
        translated_name = translate_latinic_to_cyrillic(instance.name)
        instance.name_cyrillic = translated_name

    if instance.bio:  # Assuming name_latinic is the field to be translated
        content = instance.bio 
        # Parse the HTML content using Beautiful Soup
        soup = BeautifulSoup(content, 'html.parser')

        # Translate text nodes within the HTML
        for element in soup.find_all(string=True):
            if element.parent.name not in ['script', 'style']:
                translated_text = translate_latinic_to_cyrillic(element.string)
                element.string.replace_with(translated_text)
        # Print the modified HTML content
        soup = str(soup) 
        instance.bio_cyrillic = soup


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

def translate_latinic_to_cyrillic(text):
    test_text = text.split(" ")
    translated_text = ''
    
    for word in test_text: 
        if word[0:2] == "$$" and word[-2:] == "$$": 
            translated_text += " " + word[2:len(word)-2] + " "
            continue 
        else: 
            char = 0
            while char < len(word):
                if word[char] not in string.punctuation:
                    if word[char] == "L" or word[char] == "l":
                        if char + 1 < len(word) and word[char + 1] == "j":
                            translated_char = LATINIC_TO_CYRILLIC.get(word[char:char + 2], word[char:char + 2])
                            translated_text += translated_char
                            char = char + 2
                        else:
                            translated_char = LATINIC_TO_CYRILLIC.get(word[char], word[char])
                            translated_text += translated_char
                            char = char + 1
                    elif word[char] == "N" or word[char] == "n":
                        if char + 1 < len(word) and word[char + 1] == "j":
                            translated_char = LATINIC_TO_CYRILLIC.get(word[char:char + 2], word[char:char + 2])
                            translated_text += translated_char
                            char = char + 2
                        else:
                            translated_char = LATINIC_TO_CYRILLIC.get(word[char], word[char])
                            translated_text += translated_char
                            char = char + 1
                    elif word[char] == "D" or word[char] == "d":
                        if char + 1 < len(word) and word[char + 1] == "\u017E":
                            translated_char = LATINIC_TO_CYRILLIC.get(word[char:char + 2], word[char:char + 2])
                            translated_text += translated_char
                            char = char + 2
                        else:
                            translated_char = LATINIC_TO_CYRILLIC.get(word[char], word[char])
                            translated_text += translated_char
                            char = char + 1
                    else:
                        translated_char = LATINIC_TO_CYRILLIC.get(word[char], word[char])
                        translated_text += translated_char
                        char = char + 1
                else:
                    translated_text += word[char]
                    char = char + 1 
        translated_text += " "

    return translated_text


# MODELS FOR USERS ....................................................................

class Profile(models.Model): 
    SEX_CHOICES = [("male", "Male"), ("female", "Female")]
    class Meta: 
        ordering = ['username']
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True, related_name='profile') 
    name = models.CharField(max_length=200, null=True) 
    name_cyrillic = models.CharField(max_length=200, blank=True, null=True) 
    username = models.CharField(max_length=200, null=True) 
    email = models.EmailField(max_length=500, null=True, blank=True)  
    phone = models.CharField(max_length=15, null=True, blank=True)
    active_president = models.BooleanField(default=False, blank=True, null=True)
    president = models.BooleanField(default=False, blank=True, null=True)
    vice_president = models.BooleanField(default=False, blank=True, null=True)
    main_board_member = models.BooleanField(default=False, blank=True, null=True)
    board_member = models.BooleanField(default=False, blank=True, null=True)
    commission = models.BooleanField(default=False, blank=True, null=True)
    sex = models.CharField(blank=True, null=True, default='male', max_length=99)
    bio = RichTextField(null=True, blank=True)   
    bio_cyrillic= RichTextField(blank=True, null=True) 
    profile_image = models.ImageField(blank=True, null=True, upload_to='', default=f"ArtBoard_2.png")
    created = models.DateTimeField(auto_now_add=True) 
    id = models.UUIDField(default=uuid.uuid4,unique=True, 
                                    primary_key=True, editable=False) 
                                
    def __str__(self): 
        try: 
            return self.username 
        except: 
            return self.id 

    @property
    def get_active_role(self): 
        if self.active_president: 
            return ("Predsjednik", "Предсједник")
        elif self.vice_president: 
            return ("Zamjenik predsjednika", "Замјеник предсједника")
        elif self.board_member: 
            return ("Član Izvršnog odbora", "Члан Извршног одбора")
        elif self.commission:
            return ("Član Statutarne komisije", "Члан Статутарне комисије")
        elif self.main_board_member: 
            return ("Nadzorni odbor", "Надзорни одбор")
        elif self.president: 
            return ("Bivši predsjednik", "Бивши предсједник")
        else: 
            return ("Član sindikata", "Члан синдиката")

