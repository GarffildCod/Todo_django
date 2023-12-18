from django.contrib import admin
from .models import ToDo

class ToDoController (admin.ModelAdmin):
    readonly_fields = ('created', )

admin.site.register(ToDo, ToDoController)

