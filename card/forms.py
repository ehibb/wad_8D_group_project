from django import forms
from card.models import Category, UserProfile, FlashCardSet, FlashCard, Comment
from django.contrib.auth.models import User


class CategoryForm(forms.ModelForm):
    name = forms.CharField(max_length=Category.NAME_MAX_LENGTH, help_text="Please enter the category name.")
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    likes = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    slug = forms.CharField(widget=forms.HiddenInput(), required=False)

    # An inline class to provide additional information on the form.
    class Meta:
        model = Category
        fields = ('name',)

def get_choices():
    choices = []
    for category in Category.objects.all():
        choices.append((str(category), str(category)))
    return choices

class FlashCardSetForm(forms.ModelForm):  # Which is PageFrom before
    # Foreign keys not required here
    
    
    name = forms.CharField(max_length=FlashCardSet.NAME_MAX_LENGTH, help_text="Please enter the title.")
    subject = forms.ChoiceField(choices = FlashCardSet.SUBJECT_CHOICES, required=False)
    likes = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    slug = forms.CharField(widget=forms.HiddenInput(), required=False)

    class Meta:
        # Provide an association between the ModelForm and a model
        model = FlashCardSet
        exclude = ['User']
        fields = ('name', 'subject')

    def __init__(self, *args, **kwargs):
        category_name_slug = kwargs.pop("category_name_slug")
        super().__init__(*args, **kwargs)
        choices = get_choices()
        self.fields['subject'].choices = choices
        # Exclude Category field if we are in a category
        if category_name_slug:
            self.fields['subject'].widget = forms.HiddenInput()
            
"""
FlashCardForm should take question text and answer text
Foreign keys not needed
"""
class FlashCardForm(forms.ModelForm):  # Modify here

    question_text = forms.CharField(max_length=500, help_text="Please enter the Flash Card Question")
    answer_text = forms.CharField(max_length=500, help_text="Please enter the Flash Card Answer")

    class Meta:
        model = FlashCard
        fields = ('question_text','answer_text')
    


"""
CommentForm should simply take comment text
Again no foreign keys needed
"""
class CommentForm(forms.ModelForm):

    comment_text = forms.CharField(max_length=500, help_text="Please leave a comment.")

    class Meta:
        model = Comment
        fields = ('comment_text',)


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password',)


