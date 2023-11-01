from django.db import models
from django.contrib.auth.models import User 
import uuid 
import string 
from django.conf import settings

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
        translated_name = translate_latinic_to_cyrillic(instance.bio)
        instance.bio_cyrillic = translated_name


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





# MODELS FOR USERS ....................................................................

class Profile(models.Model): 
    class Meta: 
        ordering = ['username']
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True, related_name='profile') 
    name = models.CharField(max_length=200, null=True) 
    name_cyrillic = models.CharField(max_length=200, blank=True, null=True) 
    username = models.CharField(max_length=200, null=True) 
    email = models.EmailField(max_length=500, null=True) 
    phone = models.CharField(max_length=15, null=True)
    active_president = models.BooleanField(default=False, blank=True, null=True)
    president = models.BooleanField(default=False, blank=True, null=True)
    vice_president = models.BooleanField(default=False, blank=True, null=True)
    secretary = models.BooleanField(default=False, blank=True, null=True)
    board_member = models.BooleanField(default=False, blank=True, null=True)
    commission = models.BooleanField(default=False, blank=True, null=True)
    bio = models.TextField(null=True) 
    bio_cyrillic= models.TextField(blank=True, null=True) 
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
            return ("Zamjenik Predsjednika", "Замјеник Предсједника")
        elif self.board_member: 
            return ("Član Izvršnog Odbora", "Члан Извршног Одбора")
        elif self.commission:
            return ("Član Statutarne Komisije", "Члан Статутарне Комисије")
        elif self.secretary: 
            return ("Generalni Sekretar", "Генерални Секретар")
        elif self.president: 
            return ("Bivši predsjednik", "Бивши предсједник")
        else: 
            return ("Član Sindikata", "Члан Синдиката")

