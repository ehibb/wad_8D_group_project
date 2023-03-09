from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User


class Category(models.Model):
    NAME_MAX_LENGTH = 128

    name = models.CharField(max_length=NAME_MAX_LENGTH, unique=True)
    views = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name


class Page(models.Model):
    TITLE_MAX_LENGTH = 128
    URL_MAX_LENGTH = 200

    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(max_length=TITLE_MAX_LENGTH)
    url = models.URLField(max_length=URL_MAX_LENGTH)
    views = models.IntegerField(default=0)

    def __str__(self):
        return self.title


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    website = models.URLField(blank=True)
    picture = models.ImageField(upload_to='profile_images', blank=True)

    def __str__(self):
        return self.user.username



"""
FLASHCARDSET MODEL: Contains information on a given set of flash cards
Fields:
    user: The user who created the flash card set
    name: Name of flash card set (max 50 chars)
    number_of_questions: Number of flash cards in the set; updates when flash cards are added and removed
    subject: The subject the contents of the set cover, given by subject_choices
    likes: The amount of times the flash card set has been liked
"""

SUBJECT_CHOICES = (
    ('general','General'),
    ('math','Math'),
    ('english','English'),
    ('computing','Computing'),
    ('physics','Physics'),
)

class FlashCardSet(models.Model):
    NAME_MAX_LENGTH = 50
    SUBJECT_MAX_LENGTH = 20
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=NAME_MAX_LENGTH, unique=True)
    number_of_questions=models.IntegerField(default=0)
    subject = models.CharField(max_length = SUBJECT_MAX_LENGTH, choices=SUBJECT_CHOICES, default='general')
    likes = models.IntegerField(default=0)
    slug = models.SlugField(unique=True)
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(FlashCardSet, self).save(*args, **kwargs)        
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = 'Flash Card Sets'
 
"""
FLASHCARD MODEL: Contains information on a given flash card
Fields:
    flash_card_set: The flash card set it belongs to
    question_text: String holding the question
    answer_text: Text holding the answer
"""

class FlashCard(models.Model):
    QUESTION_MAX_LENGTH = 500
    ANSWER_MAX_LENGTH = QUESTION_MAX_LENGTH
    
    flash_card_set = models.ForeignKey(FlashCardSet, on_delete=models.CASCADE)
    question_text = models.CharField(max_length = QUESTION_MAX_LENGTH)
    answer_text = models.CharField(max_length = ANSWER_MAX_LENGTH)
    
    def __str__(self):
        return self.question_text


