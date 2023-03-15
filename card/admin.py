from django.contrib import admin
from card.models import Category, Page, FlashCardSet, FlashCard
from card.models import UserProfile


class PageAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'url', 'views')


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


class FlashCardSetAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


class FlashCardAdmin(admin.ModelAdmin):
    list_display = ('flash_card_set', 'question_text', 'answer_text')


admin.site.register(Category, CategoryAdmin)
admin.site.register(Page, PageAdmin)
admin.site.register(FlashCardSet, FlashCardSetAdmin)
admin.site.register(FlashCard, FlashCardAdmin)
admin.site.register(UserProfile)
