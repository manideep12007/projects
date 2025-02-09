from django.contrib import admin
from .models import Post,Category

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['image','content','author','category']
    list_filter = ['created','category','author__username']
    search_fields = ['content','author__username']
    ordering = ['updated']
    date_hierarchy = 'updated'
    save_on_top = True
    save_as = True 

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = [
        'name'
    ]
