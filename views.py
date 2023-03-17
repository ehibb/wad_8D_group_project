from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Category, FlashCardSet, FlashCard
from .forms import CategoryForm, FlashCardSetForm, UserForm, UserProfileForm, FlashCardForm, TestForm, CommentForm


def index(request):

    category_list = Category.objects.order_by('-likes')[:5]
    flash_card_sets = FlashCardSet.objects.order_by('-likes')[:5]

    context_dict = {}
    context_dict['boldmessage'] = 'Welcome to Flash Card Master'
    context_dict['categories'] = category_list
    context_dict['flash_card_sets'] = flash_card_sets

    return render(request, 'card/index.html', context=context_dict)


def about(request):
    return render(request, 'card/about.html')

def show_flash_card_set(request, flash_card_set_slug):
    context_dict = {}
    
    try:
        card_set = FlashCardSet.objects.get(slug=flash_card_set_slug)
        
        cards = FlashCard.objects.filter(flash_card_set = card_set)
        
        context_dict['flash_card_set'] = card_set
        context_dict['flash_cards'] = cards
    except FlashCardSet.DoesNotExist:
        context_dict['flash_card_set'] = None
        context_dict['flash_cards'] = None
        
    return render(request, 'card/card_set.html', context=context_dict)

def show_category(request, category_name_slug):
    # Create a context dictionary which we can pass
    # to the template rendering engine.
    context_dict = {}

    try:
        # Can we find a category name slug with the given name?
        # If we can't, the .get() method raises a DoesNotExist exception.
        # The .get() method returns one model instance or raises an exception.
        category = Category.objects.get(slug=category_name_slug)

        # Retrieve all of the associated pages.
        # The filter() will return a list of page objects or an empty list.
        CardSets = FlashCardSet.objects.filter(category=category)

        # Adds our results list to the template context under name pages.
        context_dict['cardsets'] = CardSets

        # We also add the category object from # the database to the context dictionary.
        # We'll use this in the template to verify that the category exists.
        context_dict['category'] = category

    except Category.DoesNotExist:
        # We get here if we didn't find the specified category.
        # Don't do anything # the template will display the "no category" message for us.
        context_dict['category'] = None
        context_dict['pages'] = None

    # Go render the response and return it to the client.
    return render(request, 'card/category.html', context=context_dict)


def add_category(request):
    form = CategoryForm()

    # A HTTP POST?
    if request.method == 'POST':
        form = CategoryForm(request.POST)

        if form.is_valid():
            form.save(commit=True)
            return redirect('/card/')
        else:
            print(form.errors)

    return render(request, 'card/add_category.html', {'form': form})


def add_cardset(request, category_name_slug):
    try:
        category = Category.objects.get(slug=category_name_slug)
    except:
        category = None

    # You cannot add a page to a Category that does not exist... DM
    if category is None:
        return redirect('/card/')

    form = FlashCardSetForm()

    if request.method == 'POST':
        form = FlashCardSetForm(request.POST)

        if form.is_valid():
            if category:
                flash_card_set = form.save(commit=False)
                flash_card_set.user = request.user
                flash_card_set.category = category
                flash_card_set.save()

                return redirect(reverse('card:show_category', kwargs={'category_name_slug': category_name_slug}))
        else:
            print(form.errors)

    context_dict = {'form': form, 'category': category}
    return render(request, 'card/add_cardset.html', context=context_dict)

def add_card(request, flash_card_set_slug):
    try:
        cardset = FlashCardSet.objects.get(slug=flash_card_set_slug)
    except:
        cardset = None

    # You cannot add a page to a Category that does not exist... DM
    if cardset is None:
        return redirect('/card/')

    form = FlashCardForm()

    if request.method == 'POST':
        form = FlashCardForm(request.POST)

        if form.is_valid():
            if cardset:
                flash_card = form.save(commit=False)
                flash_card.flash_card_set = cardset
                flash_card.save()
                return redirect(reverse('card:show_category', kwargs={'category_name_slug': flash_card_set_slug}))
        else:
            print(form.errors)

    context_dict = {'form': form, 'cardset': cardset}
    return render(request, 'card/add_card.html', context=context_dict)

def register(request):
    registered = False

    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user

            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']

            profile.save()
            registered = True
        else:
            print(user_form.errors, profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    return render(request,
                  'card/register.html',
                  context={'user_form': user_form,
                           'profile_form': profile_form,
                           'registered': registered})


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return redirect(reverse('card:index'))
            else:
                return HttpResponse("Your  account is disabled.")
        else:
            print(f"Invalid login details: {username}, {password}")
            return HttpResponse("Invalid login details supplied.")
    else:
        return render(request, 'card/login.html')


@login_required
def restricted(request):
    return render(request, 'card/restricted.html')


# Use the login_required() decorator to ensure only those logged in can
# access the view.
@login_required
def user_logout(request):
    logout(request)
    # Take the user back to the homepage
    return redirect(reverse('card:index'))


def settings(request):
    return render(request, 'card/settings.html')


def account(request):
    return render(request, 'card/account.html')


def my_cards(request):
    return render(request, 'card/my_cards.html')


def comment(request, flash_card_set_slug):
    form = CommentForm()

    if request.method == 'POST':
        form = CommentForm(request.POST)
        
        comment = form.save()
        comment.flash_card_set = FlashCardSet.objects.get(slug = flash_card_set_slug)
        comment.save()
    return render(request, 'card/comment.html')

# TO BE MODIFIED
def test(request, question):
    try:
        card = FlashCard.objects.get(question_text = question)
    except:
        card = None

    if card is None:
        return redirect('/card/')

    form = TestForm()

    if request.method == 'POST':
        form = TestForm(request.POST)


        if card:
            testing_card = form.save(commit=False)
            if testing_card.answer == card.question_text:
                score = score + 1
        else:
            print(form.errors)

    context_dict = {'form': form, 'question': question}
    return render(request, 'card/test.html', context=context_dict)

# TO BE MODIFIED
def edit(request,card_slug):
    card = FlashCard.objects.get(slug = card_slug)
    form = FlashCardForm()
    if request.method == 'POST':
        form = FlashCardForm(request.POST)
        new_card = form.save(commit=False)
        card.question_text = new_card.question_text
        card.answer_text = new_card.answer_text
        card.save()
    context_dict = {'form': form, 'card': card}
    return render(request, 'card/edit.html', context=context_dict)

# search_name should be read from web, modify it as a text box after a search bottom should be better
def search(request):
    search_name = 'e'
    error_msg = ''

    if not search_name:
        error_msg = 'Please enter a card name'
        return render(request, 'card/', {'error_msg': error_msg})

    card_list = FlashCardSet.objects.filter(name__icontains=search_name)
    return render(request, 'card/search.html', {'error_msg': error_msg,
                                               'card_list': card_list})





