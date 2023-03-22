from django.test import TestCase
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from card.models import FlashCardSet, Category, FlashCard

class FlashCardSetTestCase(TestCase):
    def setUp(self):
        #Create sample user for flash card sets to be made with
        user = User.objects.create_user(username='TestModelUser', password='1234')
        
        #Create sample category for flash card sets to be made with
        category = Category.objects.get_or_create(name="Test")[0]
        
        #Create models to test
        FlashCardSet.objects.create(user=user, category=category, name="Test Flash Card Set")
        
    def test_default_likes(self):
        """Check the flash card set has initally no likes"""
        fcs = FlashCardSet.objects.get(name="Test Flash Card Set")
        self.assertEqual(fcs.likes, 0)
    def test_default_questions(self):
        """Check the flash card set initially has no associated flash cards"""
        fcs = FlashCardSet.objects.get(name="Test Flash Card Set")
        self.assertEqual(fcs.number_of_questions, 0)
        
    def test_slug(self):
        """Check the slug is created correctly"""
        fcs = FlashCardSet.objects.get(name="Test Flash Card Set")
        self.assertEqual(fcs.slug, "test-flash-card-set")
        
    def test_add_flashcard(self):
        """Check if a flash card can be added successfully to the set"""
        fcs = FlashCardSet.objects.get(name="Test Flash Card Set")
        fc = FlashCard.objects.get_or_create(flash_card_set = fcs, question_text="Is this a test?", answer_text="Yes!")[0]
        fc.save()
        
        self.assertEqual(fcs.number_of_questions, 1)