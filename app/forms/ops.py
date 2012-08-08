__author__ = 'yousuf'

from django.forms import ModelForm
from app.models import OpLink, Op, Comment

class OpLinkForm(ModelForm):
    class Meta:
        model = OpLink
        exclude = ('user')

class OpForm(ModelForm):
    class Meta:
        model = Op
        exclude = ('user', 'added', 'updated', 'tag', 'tag_groups', 'links', 'comments')

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        exclude = ('user', 'updated', 'added')

