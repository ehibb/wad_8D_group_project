from django.contrib import admin
from card.models import Category, FlashCardSet, FlashCard, Comment
from card.models import UserProfile


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


class FlashCardSetAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


class FlashCardAdmin(admin.ModelAdmin):
    list_display = ('flash_card_set', 'question_text', 'answer_text')


class CommentAdmin(admin.ModelAdmin):
    list_display = ('flash_card_set', 'user', 'comment_text')


admin.site.register(Category, CategoryAdmin)
admin.site.register(FlashCardSet, FlashCardSetAdmin)
admin.site.register(FlashCard, FlashCardAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(UserProfile)
