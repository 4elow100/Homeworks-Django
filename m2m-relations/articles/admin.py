from django.contrib import admin
from django.core.exceptions import ValidationError
from django.forms import BaseInlineFormSet
from .models import Article, Scope, Tag


class ArticleAdminInlineFormset(BaseInlineFormSet):
    def clean(self):
        main_count = 0
        tags_list = []
        for form in self.forms:
            if form.cleaned_data:
                if form.cleaned_data['tag'] in tags_list:
                    raise ValidationError(f'Раздел "{form.cleaned_data["tag"]}" повторяется больше 1 раза')
                tags_list.append(form.cleaned_data['tag'])
                if form.cleaned_data['is_main']:
                    main_count += 1
        if main_count == 0:
            raise ValidationError('Не выбрано ни одного основного раздела')
        if main_count > 1:
            raise ValidationError('Выбрано больше 1 основного раздела')
        return super().clean()


class ArticleAdminInline(admin.TabularInline):
    model = Scope
    formset = ArticleAdminInlineFormset


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    inlines = [ArticleAdminInline]


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name']


@admin.register(Scope)
class ScopeAdmin(admin.ModelAdmin):
    list_display = ['id', 'tag', 'article']
