from django import template

register = template.Library()


@register.simple_tag(takes_context=True)
def url_replace(context, **kwargs):
    """Тег, который будет брать текущие параметры запроса и по указанному аргументу производить замену,
    не очищая остальные параметры.
    Параметр декоратора takes_context=True сообщает Django, что для работы тега требуется передать контекст.
    context['request'].GET.copy() нам позволяет скопировать все параметры текущего запроса.
    Далее по указанным полям мы просто устанавливаем новые значения, которые нам передали при использовании тега.
    В конце мы кодируем параметры в формат, который может быть указан в строке браузера.
    """
    d = context['request'].GET.copy()
    for k, v in kwargs.items():
        d[k] = v
    return d.urlencode()
