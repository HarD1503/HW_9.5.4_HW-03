import django_filters as filters
from django_filters import (FilterSet, ModelChoiceFilter,
                            ModelMultipleChoiceFilter, DateFilter, DateTimeFilter,
                            DateFromToRangeFilter, NumberFilter, DateRangeFilter)
from django.contrib.auth.models import User
from .models import Post, Category
from django.forms import SelectDateWidget
from django.utils.translation import gettext_lazy as _


# Создаем свой набор фильтров для модели Post.
# FilterSet, который мы наследуем,
# должен чем-то напомнить знакомые вам Django дженерики.
class PostFilter(FilterSet):
    category = ModelMultipleChoiceFilter(
        field_name='post_category__category_name',
        queryset=Category.objects.all(),
        label='Категории',
        conjoined=True,
    )

    post_time = DateFilter(label='Дата публикации позже: ',
                              lookup_expr='gt',
                              widget=SelectDateWidget())

    class Meta:
        # В Meta классе мы должны указать Django модель,
        # в которой будем фильтровать записи.
        model = Post
        # В fields мы описываем по каким полям модели
        # будет производиться фильтрация.
        fields = {
            # поиск по названию
            'post_title': ['icontains'],
        }