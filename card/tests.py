from django.test import TestCase, Client
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.urls import reverse
from card.models import FlashCardSet, Category, FlashCard, Comment
import string
import random


"""
Unit Tests for models:
    FlashCardSet
    FlashCard
    Comment
    
"""

class FlashCardSetTestCase(TestCase):
    def setUp(self):
        #Create sample user for flash card sets to be made with
        user = User.objects.create_user(username='TestModelUser', password='1234')
        
        #Create sample category for flash card sets to be made with
        category = Category.objects.get_or_create(name="Test")[0]
        
        #Create models to test
        FlashCardSet.objects.get_or_create(user=user, category=category, name="Test Flash Card Set")
        
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
        
    def test_add_flashcard_check_length(self):
        """Check number_of_questions is 1 after adding a flash card"""
        fcs = FlashCardSet.objects.get(name="Test Flash Card Set")
        fc = FlashCard.objects.get_or_create(flash_card_set = fcs, question_text="Is this a test?", answer_text="Yes!")[0]
        fc.save()       
        self.assertEqual(fcs.number_of_questions, 1)
    
class FlashCardTestCase(TestCase):
    def setUp(self):
        #Create sample user for flash card sets to be made with
        user = User.objects.create_user(username='TestModelUser', password='1234')
        
        #Create sample category for flash card sets to be made with
        category = Category.objects.get_or_create(name="Test")[0]
        
        #Create sample flash card set
        FlashCardSet.objects.get_or_create(user=user, category=category, name="Test Flash Card Set")
        
    def test_question_text(self):
        """Check the question_text of the flash card are OK"""

        fcs = FlashCardSet.objects.get(name="Test Flash Card Set")
        question = "Is this a test?"
        answer = "Yes!"
        fc = FlashCard.objects.get_or_create(flash_card_set = fcs, question_text=question, answer_text=answer)[0]
        fc.save()
        
        self.assertEqual(fc.question_text, question)
        self.assertEqual(fc.answer_text, answer)
    
    def test_answer_text(self):
        """Check the answer_text of the flash card are OK"""

        fcs = FlashCardSet.objects.get(name="Test Flash Card Set")
        question = "Is this a test?"
        answer = "Yes!"
        fc = FlashCard.objects.get_or_create(flash_card_set = fcs, question_text=question, answer_text=answer)[0]
        fc.save()
        
        self.assertEqual(fc.answer_text, answer)

class CommentTestCase(TestCase):
    def setUp(self):
        #Create sample user for flash card sets to be made with
        user = User.objects.create_user(username='TestModelUser', password='1234')
        
        #Create sample category for flash card sets to be made with
        category = Category.objects.get_or_create(name="Test")[0]
        
        #Create sample flash card set
        FlashCardSet.objects.get_or_create(user=user, category=category, name="Test Flash Card Set")
        
        
    def test_comment_text(self):
        """Test that commment_text is OK"""
        user = authenticate(username='TestModelUser', password='1234')
        fcs = FlashCardSet.objects.get(name="Test Flash Card Set")
        comment_string = "This is a test!"
        
        comment = Comment.objects.get_or_create(user=user, flash_card_set=fcs, comment_text=comment_string)[0]
        comment.save()
        
        self.assertEqual(comment.comment_text, comment_string)
    
    def test_user_makes_two_comments(self):
        """Test that a user is able to comment more than once on a flash card set"""
        
        user = authenticate(username='TestModelUser', password='1234')
        fcs = FlashCardSet.objects.get(name="Test Flash Card Set")
        
        Comment.objects.get_or_create(user=user, flash_card_set=fcs, comment_text="This is the first comment!")[0].save()
        Comment.objects.get_or_create(user=user, flash_card_set=fcs, comment_text="This is the second comment!")[0].save()
        
        self.assertEqual(Comment.objects.filter(user=user, flash_card_set=fcs).count(), 2)        
        
"""
Unit tests for views:
    index
    about
    view_categories
    view_cardsets    
    
"""        
class TestViews(TestCase):
    def setUp(self):
        user = User.objects.create_user(username='TestViewsUser', password='1234')
        
    def test_index(self):
        """Check status code is 200"""
        
        response = self.client.get(reverse('card:index'))
        
        self.assertEqual(response.status_code, 200)
        
    def test_about(self):
        """Check status code is 200"""
        
        response = self.client.get(reverse('card:about'))
        
        self.assertEqual(response.status_code, 200)
        
    def test_view_categories_no_categories(self):
        """Check category queryset in context_dict is empty """
        
        response = self.client.get(reverse('card:view_categories'))
        
        self.assertQuerysetEqual(response.context['categories'], [])
        
    def test_view_categories_one_category(self):    
        """Check category queryset in context_dict has one category"""
        
        category = Category.objects.get_or_create(name="Test")[0]
        response = self.client.get(reverse('card:view_categories'))
        
        self.assertIn(category, response.context['categories'])
        
    def test_view_cardsets_no_cardsets(self):
        """Check cardset queryset in context_dict is empty """
        response = self.client.get(reverse('card:view_cardsets'))
        
        self.assertQuerysetEqual(response.context['flash_card_sets'], [])
    
    def test_view_cardsets_one_cardsets(self):    
        """Check category queryset in context_dict has one category"""
        category = Category.objects.get_or_create(name="Test")[0]
        user = authenticate(username='TestViewsUser', password='1234')
        fcs = FlashCardSet.objects.get_or_create(user=user, category=category, name="Test Flash Card Set")[0]
        response = self.client.get(reverse('card:view_cardsets'))
        
        self.assertIn(fcs, response.context['flash_card_sets'])

    