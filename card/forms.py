from django import forms
from card.models import Category, UserProfile, FlashCardSet, FlashCard
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


class FlashCardSetForm(forms.ModelForm):  # Which is PageFrom before
    # Foreign keys not required here
    name = forms.CharField(max_length=FlashCardSet.NAME_MAX_LENGTH, help_text="Please enter the title.")
    subject = forms.CharField(max_length=FlashCardSet.SUBJECT_MAX_LENGTH, help_text="Please enter the subject")
    likes = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    slug = forms.CharField(widget=forms.HiddenInput(), required=False)

    class Meta:
        # Provide an association between the ModelForm and a model
        model = FlashCardSet
        fields = ('name', 'subject')


class FlashCardForm(forms.ModelForm):  # Modify here
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

