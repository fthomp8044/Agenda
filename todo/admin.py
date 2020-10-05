from django.contrib import admin
from .models import Todo
# this lets you customize in model field
class TodoAdmin(admin.ModelAdmin):
    readonly_fields = ('created',)

admin.site.register(Todo, TodoAdmin)
