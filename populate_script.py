import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'flashcard_website.settings')

import django

django.setup()
from card.models import Category, Page, FlashCardSet, FlashCard
from django.contrib.auth.models import User
from django.contrib.auth import authenticate


# Populate()对已创建的类别保持tab。
# 例如，对一个新类别的引用被存储在本地变量c中。
# 这是因为Page需要Category reference。在populate()中调用add_cat()和add_page()之后，该函数将循环遍历全新的Category和相关的Page对象，并在终端上显示它们的名称。
def populate():
    # 首先，我们将创建包含要添加到每个类别中的页面的词典列表。
    # 然后，我们将为我们的类别创建一个字典的字典。
    # 这可能看起来有点混乱，但它允许我们遍历每个数据结构，并将数据添加到我们的模型中

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

    cats = {'Python': {'pages': python_pages, 'views': 128, 'likes': 64},
            'Django': {'pages': django_pages, 'views': 64, 'likes': 32},
            'Other Frameworks': {'pages': other_pages, 'views': 32, 'likes': 16}}
            
    #Create user, if not already created
    #Flash card sets will be created with this user as the creator
    
    user = authenticate(username="FlashCardMan", password="jyRquc318X!w9ewnZf^")
    if user is None:
        user = User.objects.create_user(username="FlashCardMan", email ="flashcardman@gmail.com", password="jyRquc318X!w9ewnZf^")
    user.save()
    #Creating flash card sets: one for math, english and physics

    math_flash_cards = [
        {'question_text':'5+5?','answer_text':'10'},
        {'question_text':'12+9=?','answer_text':'21'},
        {'question_text':'40+0=?','answer_text':'40'}
    ]
    
    computing_flash_cards = [
        {'question_text':'What does the function print("Hello World") do?','answer_text':'Prints "Hello World" to the screen'},
        {'question_text':'What function may we use to find the length of an array?','answer_text':'len(array)'},
        {'question_text':'What function could we call the find the maximum value in an array?','answer_text':'max(array)'}
    ]
    
    physics_flash_cards = [
        {'question_text':'State N1.','answer_text':'In an inertial frame every body continues in a state of rest of uniform motino unless acted on by a force.'},
        {'question_text':'State N2.','answer_text':'In an inertial frame the force acting on a body is equal to its rate of change of momentum.'},
        {'question_text':'State N3','answer_text':'Action and reaction are equal and opposite forces.'}
    ]
    
    flash_card_sets = {
        'Basic Addition Questions':{'user': user,'subject':'math','likes':20, 'flash_cards': math_flash_cards},
        'Python predefined functions':{'user': user,'subject':'math','likes':0, 'flash_cards': computing_flash_cards},
        'Newtons Laws of Motion':{'user': user,'subject':'math','likes':2, 'flash_cards': physics_flash_cards}
    }
    
    for flash_card_set, flash_card_set_data in flash_card_sets.items():
        fcs = add_flash_card_set(user=user, name=flash_card_set, subject=flash_card_set_data['subject'])
        for fc in flash_card_set_data['flash_cards']:
            add_flash_card(fcs, fc['question_text'], fc['answer_text'])
        
    for fcs in FlashCardSet.objects.all():
        for fc in FlashCard.objects.filter(flash_card_set = fcs):
            print(f'- {fcs}: {fc}')
     
        
    # 如果你想添加更多的类别或页面，将它们添加到上面的字典中

    # 下面的代码遍历cats字典，然后添加每个类别，然后添加该类别的所有相关页面。
    for cat, cat_data in cats.items():
        c = add_cat(cat, views=cat_data['views'], likes=cat_data['likes'])
        for p in cat_data['pages']:
            add_page(c, p['title'], p['url'], views=p['views'])

    # Print out the categories we have added.
    for c in Category.objects.all():
        for p in Page.objects.filter(category=c):
            print(f'- {c}: {p}')

            # 创建新的page

def add_flash_card_set(user, name,subject='default',likes=0):
    fcs = FlashCardSet.objects.get_or_create(user=user, name=name)[0]
    fcs.subject = subject
    fcs.likes = likes
    fcs.save()
    return fcs
    
def add_flash_card(fcs, question_text, answer_text):
    fc = FlashCard.objects.get_or_create(flash_card_set = fcs, question_text=question_text,answer_text=answer_text)[0]
    fc.save()
    return fc

def add_page(cat, title, url, views=0):
    p = Page.objects.get_or_create(category=cat, title=title)[0]
    p.url = url
    p.views = views
    p.save()
    return p


# 创建新的category
def add_cat(name, views=0, likes=0):
    c = Category.objects.get_or_create(name=name)[0]
    # get_or_create returns a tuple, in which the first element is the object,
    # the second is the boolean indicating if new object is created
    c.views = views
    c.likes = likes
    c.save()
    return c


# 从这里开始执行
# __name__ == '__main__' 允许Python模块充当可重用模块或独立的Python脚本
# 因此，if中的代码将只在模块作为一个独立的Python脚本运行时执行。导入模块不会运行这段代码;不过可以完全访问任何类或函数
if __name__ == '__main__':
    print('Starting population script...')
    populate()
