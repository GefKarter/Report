from django import forms
from django.core.exceptions import ValidationError
from django.core.files.images import get_image_dimensions
from django_summernote.fields import SummernoteTextField
from django_summernote.widgets import SummernoteWidget

from .models import Notification, Responses
from Board.russian_ban_words import unwanteded_words


class NotificationForm(forms.ModelForm):
    title = forms.CharField(max_length=128)
    text = SummernoteTextField()

    class Meta:
        model = Notification
        fields = [
            'photo',
            'title',
            'text',
            'notification_category',

        ]
        widgets = {
            'text': SummernoteWidget()
        }

    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data.get("title")
        text = cleaned_data.get("text")

        if text == title:
            raise ValidationError(
                "The description should not be identical to the name."
            )

        for word in unwanteded_words:
            if word in text:
                raise forms.ValidationError("Your text contains obscene language, correct it and try again.")

        photo = cleaned_data.get("photo")
        if not photo:
            raise forms.ValidationError("No image!")
        else:
            w, h = get_image_dimensions(photo)
            if w > 850:
                raise forms.ValidationError("The width of the image is %i pixel. It is assumed that it should be "
                                            "larger than 850 pixels" % w)
            if h > 350:
                raise forms.ValidationError("The width of the image is %i pixel. It is assumed that it should be more "
                                            "than 350 pixels" % h)

        return cleaned_data


class ResponsesForm(forms.ModelForm):
    text = forms.CharField(max_length=512)

    class Meta:
        model = Responses
        fields = ['text']

    def clean(self):
        cleaned_data = super().clean()
        text = cleaned_data.get("text")

        for word in unwanteded_words:
            if word in text:
                raise forms.ValidationError("Your text contains obscene language, correct it and try again.")

        return cleaned_data
