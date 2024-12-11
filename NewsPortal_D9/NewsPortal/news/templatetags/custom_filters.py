from django import template

register = template.Library()

class TypeException(Exception):
    pass

# Регистрируем наш фильтр под именем currency, чтоб Django понимал,
# что это именно фильтр для шаблонов, а не простая функция.
@register.filter()
def censor(text):
    CENS_WORDS = ['подшипник', 'коробка', 'видеорегистратор', 'транспорт', 'безопасность', 'также', 'видео',
                  'отставание', 'место']

    if type(text) != str:
        raise TypeException(f'Недопустимый формат данных (string)!')
    lst = []
    st = ''
    i = 0
    for sym in text:
        i += 1
        if sym.isalpha():
            st += sym
            if i == len(text):
                lst.append(st)
        else:
            if len(st):
                lst.append(st)
            lst.append(sym)
            st = ''

    for i in range(len(lst)):
        if lst[i].lower() in CENS_WORDS:
            lst[i] = lst[i].replace(lst[i], lst[i][:1] + "*" * (len(lst[i]) - 1))

    censored_text = ''
    for word in lst:
        censored_text += word

    return f'{censored_text}'


