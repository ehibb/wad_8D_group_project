import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'flashcard_website.settings')

import django

django.setup()
from card.models import Category, FlashCardSet, FlashCard, Comment
from django.contrib.auth.models import User
from django.contrib.auth import authenticate


def populate():

    python_pages = [
        {'title': 'Official Python Tutorial',
         'url': 'http://docs.python.org/3/tutorial/',
         'views': 12},
        {'title': 'How to Think like a Computer Scientist',
         'url': 'http://www.greenteapress.com/thinkpython/',
         'views': 112},
        {'title': 'Learn Python in 10 Minutes',
         'url': 'http://www.korokithakis.net/tutorials/python/',
         'views': 172}
    ]

    django_pages = [
        {'title': 'Official Django Tutorial', 'url': 'https://docs.djangoproject.com/en/2.1/intro/tutorial01/', 'views': 12},
        {'title': 'Django Rocks', 'url': 'http://www.djangorocks.com/', 'views': 122},
        {'title': 'How to Tango with Django', 'url': 'http://www.tangowithdjango.com/', 'views': 124}
    ]

    other_pages = [
        {'title': 'Bottle', 'url': 'http://bottlepy.org/docs/dev/', 'views': 212},
        {'title': 'Flask', 'url': 'http://flask.pocoo.org', 'views': 422}
    ]

    cats = {'Maths': {'views': 128, 'likes': 64},
            'Physics': {'views': 64, 'likes': 32},
            'Computing': {'views': 32, 'likes': 16},
            'Other':{'views': 128, 'likes': 64}}


    #Create example users, if not already created
    #Flash card sets will be created with this user as the creator
    example_users = [
        {'username':'FlashCardMan', 'password':'jyRquc318X', 'email':'flashcardman@gmail.com'},
        {'username':'FlashCardWoman', 'password':'=6r76vQ=Z2!Az+gW', 'email':'flashcardwoman@gmail.com'},
        {'username':'Yosemite', 'password':'UVyLCLS!2-r^[*yx', 'email':'yosemite@yahoo.com'},
        {'username':'Uncle_Randy', 'password':'&9*m_4.^Q3{q$2vS', 'email':'unclerandy@outlook.com'},
    ]
    
    for example_user in example_users:
        user = authenticate(username=example_user['username'], password=example_user['password'])
        if user is None:
            user = User.objects.create_user(username=example_user['username'], email=example_user['email'], password=example_user['password'])
        user.save()
        
    #Creating flash card sets: one for math, english and physics
    math_flash_cards = [
        {'question_text':'5+5?','answer_text':'10'},
        {'question_text':'12+9=?','answer_text':'21'},
        {'question_text':'40+0=?','answer_text':'40'}
    ]
    
    computing_flash_cards = [
        {'question_text':'What does the function print("Hello World") do?', 'answer_text': 'Prints "Hello World" to the screen'},
        {'question_text':'What function may we use to find the length of an array?', 'answer_text': 'len(array)'},
        {'question_text':'What numpy function could we call the find the maximum value in an array?', 'answer_text': 'max(array)'}
    ]
    
    physics_flash_cards = [
        {'question_text':'State N1.','answer_text': 'In an inertial frame every body continues in a state of rest of uniform motino unless acted on by a force.'},
        {'question_text':'State N2.','answer_text': 'In an inertial frame the force acting on a body is equal to its rate of change of momentum.'},
        {'question_text':'State N3','answer_text': 'Action and reaction are equal and opposite forces.'}
    ]
    
    flash_card_sets = {
        'Basic Addition Questions':{'user': authenticate(username=example_users[2]['username'], password=example_users[2]['password']),'subject':'Maths','likes':20, 'flash_cards': math_flash_cards},
        'Python predefined functions':{'user': authenticate(username=example_users[1]['username'], password=example_users[1]['password']),'subject':'Computing','likes':0, 'flash_cards': computing_flash_cards},
        'Newtons Laws of Motion':{'user': authenticate(username=example_users[0]['username'], password=example_users[0]['password']),'subject':'Physics','likes':2, 'flash_cards': physics_flash_cards}
    }
    for cat, cat_data in cats.items():
        c = add_cat(cat, views=cat_data['views'], likes=cat_data['likes'])
    
    for flash_card_set, flash_card_set_data in flash_card_sets.items():
        fcs = add_flash_card_set(user=flash_card_set_data['user'], name=flash_card_set, category=Category.objects.get(name=flash_card_set_data['subject']), subject=flash_card_set_data['subject'])
        for fc in flash_card_set_data['flash_cards']:
            add_flash_card(fcs, fc['question_text'], fc['answer_text'])
    # Print out the categories we have added.
    for c in Category.objects.all():
        for fcs in FlashCardSet.objects.filter(subject=c.name):
            for fc in FlashCard.objects.filter(flash_card_set = fcs):
                print(f'- {c.name}: {fcs} - {fc}')
    
    #Creating example comments
    comments = [
        {'user': authenticate(username=example_users[0]['username'], password=example_users[0]['password']), 'flash_card_set': FlashCardSet.objects.get(name='Basic Addition Questions'), 'comment_text':'This helped me do my taxes - thanks!'},
        {'user': authenticate(username=example_users[3]['username'], password=example_users[3]['password']), 'flash_card_set': FlashCardSet.objects.get(name='Newtons Laws of Motion'), 'comment_text':'What even is an inertial frame???'},
        {'user': authenticate(username=example_users[3]['username'], password=example_users[3]['password']), 'flash_card_set': FlashCardSet.objects.get(name='Python predefined functions'), 'comment_text':'mmmm... hamburger'}
    ]
    
    for comment in comments:
        c = add_comment(comment['user'], comment['flash_card_set'], comment['comment_text'])
        print(f'- {comment["flash_card_set"]} comment: {c}')
        
def add_flash_card_set(user, name, category, subject='other',likes=0):
    fcs = FlashCardSet.objects.get_or_create(user=user, name=name, category=category)[0]
    fcs.subject = subject
    fcs.likes = likes
    fcs.save()
    return fcs

    
def add_flash_card(fcs, question_text, answer_text):
    fc = FlashCard.objects.get_or_create(flash_card_set = fcs, question_text=question_text,answer_text=answer_text)[0]
    fc.save()
    return fc


def add_comment(user, flash_card_set, comment_text):
    c = Comment.objects.get_or_create(user=user, flash_card_set=flash_card_set, comment_text=comment_text)[0]
    c.save()
    return c


def add_cat(name, views=0, likes=0):
    c = Category.objects.get_or_create(name=name)[0]
    # get_or_create returns a tuple, in which the first element is the object,
    # the second is the boolean indicating if new object is created
    c.views = views
    c.likes = likes
    c.save()
    return c


if __name__ == '__main__':
    print('Starting population script...')
    populate()
