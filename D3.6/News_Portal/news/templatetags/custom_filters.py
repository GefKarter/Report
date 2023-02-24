from django import template
register = template.Library()

@register.filter()
def censor(text):
    bad_words = ('заявили', 'безопасности', 'США', 'конфликт', 'берегу', 'военнослужащими', 'Федеральным', 'Украине' )

    for word in text.split():
        if word.lower() in bad_words:
            text = text.replace(word, f"{word[0]}{'*' * (len(word) - 1)}")
    return text