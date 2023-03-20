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


class FlashCardSetForm(forms.ModelForm):
    # Foreign keys not required here
    name = forms.CharField(max_length=FlashCardSet.NAME_MAX_LENGTH, help_text="Please enter the title.")
    subject = forms.ChoiceField(choices = FlashCardSet.SUBJECT_CHOICES)
    likes = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    slug = forms.CharField(widget=forms.HiddenInput(), required=False)

    class Meta:
        # Provide an association between the ModelForm and a model
        model = FlashCardSet
        exclude = ['User']
        fields = ('name', 'subject')
        
"""
FlashCardForm should take question text and answer text
Foreign keys not needed
"""
class FlashCardForm(forms.ModelForm):
    question_text = forms.CharField(max_length=FlashCard.QUESTION_MAX_LENGTH, help_text="Please enter the question.")
    answer_text = forms.CharField(max_length=FlashCard.ANSWER_MAX_LENGTH, help_text="Please enter the answer.")

    class Meta:
        model = FlashCard
        fields = ('question_text', 'answer_text')


"""
CommentForm should simply take comment text
Again no foreign keys needed
"""
class CommentForm(forms.ModelForm):
    pass

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password',)


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('website', 'picture',)

