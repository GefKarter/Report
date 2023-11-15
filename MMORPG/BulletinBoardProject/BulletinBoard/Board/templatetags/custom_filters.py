from django import template
from Board.russian_ban_words import unwanteded_words

register = template.Library()


@register.filter()
def censor_filter(text):
    unwanted_words = unwanteded_words  # Список нежелательных слов находится в файле russian_ban_words
    for word in unwanted_words:
        text = text.replace(word, '***')  # Заменяем нежелательное слово символами ***
    return text

