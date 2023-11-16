from django.contrib import admin
from .models import Test, Question, Answer, UserProgress


class TestsAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}


admin.site.register(Test, TestsAdmin)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(UserProgress)
