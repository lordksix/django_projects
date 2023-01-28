from django.contrib import admin
from ads.models import Article,Fav

# Register your models here.

admin.site.register(Fav)

@admin.register(Article)
class FilmAdmin(admin.ModelAdmin):
    list_display=['title','price','owner','get_tags']

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('tags')

    def get_tags(self,obj):
        return ", ".join(o.name for o in obj.tags.all())