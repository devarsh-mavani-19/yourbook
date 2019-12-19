#SuperUser Information
##Username = devarsh
#password = 123hello

from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUserForm, BookModel, SendMessageModel,search, Question, Answer

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUserForm
    list_display = ['enrollment', 'username']

admin.site.register(CustomUserForm, CustomUserAdmin)

admin.site.register(BookModel)
admin.site.register(SendMessageModel)
admin.site.register(search)
admin.site.register(Question)
admin.site.register(Answer)