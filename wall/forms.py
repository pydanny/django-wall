"""
Here we define forms that are specific to WallItems.
"""

from django import forms
from wall.models import Wall, WallItem
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ugettext_noop

class WallItemForm(forms.Form):
    """
    This form collects a new post.
    """
    posting = forms.CharField(label=_(u"Item"),
        widget=forms.Textarea(attrs={'rows': '5', 'cols':'50'}))

    def __init__(self, *args, **kwargs):
        help_text = kwargs.pop('help_text', "")
        super(WallItemForm, self).__init__(*args, **kwargs)
        self.fields['posting'].help_text = help_text

    def save(self, user=None):
        posting = self.cleaned_data['posting']
        return posting

