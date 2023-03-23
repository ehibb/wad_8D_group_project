from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Category, FlashCardSet, FlashCard, Comment
from .forms import CategoryForm, FlashCardSetForm, UserForm, CommentForm, FlashCardForm
from django.utils.decorators import method_decorator
from django.views import View

# The View responsible for serving the user the Home Page
def index(request):

    category_list = Category.objects.order_by('-views')[:5]
    flash_card_sets = FlashCardSet.objects.order_by('-likes')[:5]

    context_dict = {}
    context_dict['boldmessage'] = 'Welcome to Flash Card Master'
    context_dict['categories'] = category_list
    context_dict['flash_card_sets'] = flash_card_sets

    return render(request, 'card/index.html', context=context_dict)


# The View Responsible for serving the user with the About Page
def about(request):
    return render(request, 'card/about.html')


# The View responsible for displaying a Flash Card Set along with information about said set
def show_flash_card_set(request, flash_card_set_slug):
    context_dict = {}
    
    try:
        card_set = FlashCardSet.objects.get(slug=flash_card_set_slug)
        
        cards = FlashCard.objects.filter(flash_card_set = card_set)

        comments = Comment.objects.filter(flash_card_set = card_set)
        
        context_dict['flash_card_set'] = card_set
        context_dict['flash_cards'] = cards
        context_dict['flash_card_comments'] = comments
        if request.user == card_set.user:
            context_dict['isCreator'] = True
        else:
            context_dict['isCreator'] = False
        
        if request.user.is_authenticated:
            context_dict['userLoggedIn'] = True

    except FlashCardSet.DoesNotExist:
        context_dict['flash_card_set'] = None
        context_dict['flash_cards'] = None
        
    return render(request, 'card/card_set.html', context=context_dict)


# The View Functionality responsible for incrementing a Flash Card Set's likes.
class LikeCardSetView(View):

    @method_decorator(login_required)
    def get(self, request):
        cardset_name = request.GET['name']
        try:
            cardset = FlashCardSet.objects.get(name=cardset_name)
        except Category.DoesNotExist:
            return HttpResponse(-1)
        except ValueError:
            return HttpResponse(-1)
        
        cardset.likes = cardset.likes + 1
        cardset.save()
        return HttpResponse(cardset.likes)
    

# The View responsible for displaying info about a Category
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
        CardSets = FlashCardSet.objects.filter(category=category).order_by('-likes')

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


# The View responsible for the creation of new Categories
@login_required
def add_category(request):
    form = CategoryForm()

    # A HTTP POST?
    if request.method == 'POST':
        form = CategoryForm(request.POST)

        if form.is_valid():
            category_name = str(form['name'].value()).capitalize()
            category = form.save(commit=False)
            category.name = category_name
            category.save()
            return redirect('/card/')
        else:
            print(form.errors)

    return render(request, 'card/add_category.html', {'form': form})


# The View responsible for the creation of new Card Sets
def add_cardset(request, category_name_slug=""):
    try:
        category = Category.objects.get(slug=category_name_slug)
    except:
        category = None

    form = FlashCardSetForm(category_name_slug=category_name_slug)

    if request.method == 'POST':
        form = FlashCardSetForm(request.POST, category_name_slug=category_name_slug)
        if form.is_valid():           
            flash_card_set = form.save(commit=False)
            flash_card_set.user = request.user
            if category:
                flash_card_set.category = category
                flash_card_set.subject = category.name
                flash_card_set.save()
                return redirect(reverse('card:show_category', kwargs={'category_name_slug': category_name_slug}))
            else:
                flash_card_set.category = Category.objects.get(name=form['subject'].value())
                flash_card_set.save()
                return redirect(reverse('card:index'))
        else:
            print(form.errors)

    context_dict = {'form': form, 'category': category}
    return render(request, 'card/add_cardset.html', context=context_dict)


# The View responsible for registering users to the site
def register(request):
    registered = False

    if request.method == 'POST':
        user_form = UserForm(request.POST)


        if user_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            registered = True
        else:
            print(user_form.errors)
    else:
        user_form = UserForm()

    return render(request,
                  'card/register.html',
                  context={'user_form': user_form,
                           'registered': registered})


# The View responsible for allowing registered users to sign into the site
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


# Use the login_required() decorator to ensure only those logged in can
# access the view.
@login_required
def user_logout(request):
    logout(request)
    # Take the user back to the homepage
    return redirect(reverse('card:index'))


# The View responsible for displaying all of a Users created Flash Card Sets
@login_required
def my_cards(request):

    context_dict = {}
    
    try:
        card_sets = FlashCardSet.objects.filter(user=request.user)
        context_dict["flash_card_sets"] = card_sets
        context_dict['user'] = request.user

    except FlashCardSet.DoesNotExist:
        context_dict["flash_card_sets"] = None


    return render(request, 'card/my_cards.html',context=context_dict)


# The View repsonsible for displaying comments, as well as allowing users to upload a comment to a Card Set
@login_required
def comment(request, flash_card_set_slug):

    context_dict = {}
    try:
        cardset = FlashCardSet.objects.get(slug=flash_card_set_slug)
        cardsetcomments = Comment.objects.filter(flash_card_set=cardset)
    except:
        cardset = None
        cardsetcomments =None

    if cardset is None:
        return redirect('/card/')
    
    context_dict["flash_card_set"] = cardset
    context_dict["comments"] = cardsetcomments

    form = CommentForm()

    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            if cardset:
                comment = form.save(commit=False)
                comment.user = request.user
                comment.flash_card_set = cardset
                comment.save()

                return redirect(reverse('card:comment',kwargs={'flash_card_set_slug':flash_card_set_slug}))

    context_dict["form"] = form

    return render(request, 'card/comment.html', context=context_dict)


# The View responsible for allowing users to take a test on a Flash Card Set
def test(request, flash_card_set_slug):

    
    context_dict = {}
    try:
        cardset = FlashCardSet.objects.get(slug=flash_card_set_slug)
        flashcards = FlashCard.objects.filter(flash_card_set=cardset)
    except:
        cardset = None

    if cardset is None:
        return redirect('/card/')
    
    context_dict["flash_card_set"] = cardset
    context_dict["flash_cards"] = flashcards


    return render(request, 'card/test.html',context=context_dict)


# The View responsible for displaying a page of Flash Card Set's that contain questions for a user.
def tests(request):

    context_dict = {}
    try:
        flash_card_sets = FlashCardSet.objects.all()
    except:
        flash_card_sets = None

    flash_card_sets_valid = []
    for flashcardset in flash_card_sets:
        if flashcardset.number_of_questions > 0:
            flash_card_sets_valid.append(flashcardset)


    context_dict["flash_card_sets"] = flash_card_sets_valid

    return render(request, 'card/tests.html',context=context_dict)


# The View responsible with displaying the help page to the user
def help(request):
    return render(request, 'card/help.html')


# The View responsible for allowing a user to edit their Flash Card Sets
def edit(request, flash_card_set_slug):
    context_dict = {}

    try:
        cardset = FlashCardSet.objects.get(slug=flash_card_set_slug)
    except:
        cardset = None

    # You cannot edit a cardset that does not exist
    if cardset is None:
        return redirect('/card/')

    # You cannot edit a cardset that is not yours
    if cardset.user != request.user:
        return redirect('/card/')

    flashcards = FlashCard.objects.filter(flash_card_set=cardset)
    print(flashcards)

    context_dict["flash_card_set"] = cardset
    context_dict["flash_cards"] = flashcards

    form = FlashCardForm()

    if request.method == "POST":
        form = FlashCardForm(request.POST)

        if form.is_valid():
            if cardset:
                flashcard = form.save(commit=False)
                flashcard.flash_card_set = cardset
                flashcard.save()
                cardset.save()
                
                return redirect(reverse('card:card_set',kwargs={'flash_card_set_slug':flash_card_set_slug}))
        
        else:
            print(form.errors)
    
    context_dict["form"] = form

    return render(request, 'card/edit.html', context=context_dict)


# The View responsible for allowing users to search from existing Categories/Card Sets
def search(request):
    context_dict = {}
    context_dict["categories"] = None
    return render(request, 'card/search.html',context=context_dict)


# The View displaying a list of all Card Sets
def view_cardsets(request):
    context_dict = {}
    
    try:
        card_sets = FlashCardSet.objects.all()
        context_dict["flash_card_sets"] = card_sets
        context_dict['user'] = request.user

    except FlashCardSet.DoesNotExist:
        context_dict["flash_card_sets"] = None

    return render(request, 'card/view_cardsets.html',context=context_dict)


# The View displaying a list of all Categories
def view_categories(request):
    context_dict = {}

    try:
        categories = Category.objects.all()
        context_dict["categories"] = categories
    except Category.DoesNotExist:
       context_dict["categories"] = None

    return render(request, 'card/view_categories.html',context=context_dict)



# Function and Class used in the Search page to deal with searches based on category.
def get_category_list(max_results=0, starts_with=''):
    category_list = []
    if starts_with:
        category_list = Category.objects.filter(name__istartswith=starts_with)

    if max_results > 0:
        if len(category_list) > max_results:
            category_list = category_list[:max_results]

    return category_list

class CategorySuggestionView(View):
    def get(self,request):
        if 'suggestion' in request.GET:
            suggestion = request.GET['suggestion']
        else:
            suggestion = ''
        
        category_list = get_category_list(max_results=8,starts_with=suggestion)

        if len(category_list) == 0:
            category_list = Category.objects.order_by('-likes')


        return render(request, 'card/categories.html', {"categories":category_list})
    

# Function and Class used in the Search page to deal with searches based on card set.
def get_cardset_list(max_results=0, starts_with=''):
    cardset_list = []
    if starts_with:
        cardset_list = FlashCardSet.objects.filter(name__istartswith=starts_with)

    if max_results > 0:
        if len(cardset_list) > max_results:
            cardset_list = cardset_list[:max_results]

    return cardset_list

class CardSetSuggestionView(View):
    def get(self,request):
        if 'suggestion' in request.GET:
            suggestion = request.GET['suggestion']
        else:
            suggestion = ''
        
        cardset_list = get_cardset_list(max_results=8,starts_with=suggestion)

        if len(cardset_list) == 0:
            cardset_list = FlashCardSet.objects.order_by('-likes')

        return render(request, 'card/cardsets.html', {"cardsets":cardset_list})


# Not to be confused with show_category, this View is to incremment the view count on a category
class ViewCategoryView(View):

    def get(self, request):
        category_name = request.GET['name']
        try:
            category = Category.objects.get(name=category_name)
        except Category.DoesNotExist:
            return HttpResponse(-1)
        except ValueError:
            return HttpResponse(-1)
        
        category.views = category.views + 1
        category.save()
        return HttpResponse(category.views)
    

# View For liking a Category
class LikeCategoryView(View):

    @method_decorator(login_required)
    def get(self, request):
        cat_name = request.GET['name']
        try:
            category = Category.objects.get(name=cat_name)
        except Category.DoesNotExist:
            return HttpResponse(-1)
        except ValueError:
            return HttpResponse(-1)
        
        category.likes = category.likes + 1
        category.save()
        return HttpResponse(category.likes)