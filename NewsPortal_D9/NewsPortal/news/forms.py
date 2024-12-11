from django import forms
from django.core.exceptions import ValidationError
from .models import *
from allauth.account.forms import SignupForm
from django.contrib.auth.models import Group

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            #'post_author',
            #'post_type',
            #'post_time',
            'post_category',
            'post_title',
            'post_text',
            #'post_rating',
        ]

    def clean(self):
        cleaned_data = super().clean()
        text = cleaned_data.get("post_text")
        title = cleaned_data.get("post_title")
        if title == text:
            raise ValidationError("Заголовок не должен быть идентичен тексту.")
        return cleaned_data


class BasicSignupForm(SignupForm):

    def save(self, request):
        user = super(BasicSignupForm, self).save(request)
        common_group = Group.objects.get(name='common')
        common_group.user_set.add(user)
        return user