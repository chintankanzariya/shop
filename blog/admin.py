from django.contrib import admin
from .models import Blogpost


# admin.site.register(Product)
# admin.site.register(Contact)


@admin.register(Blogpost)
class BlogpostAdmin(admin.ModelAdmin):
    list_display = ["post_id", "title","pub_date","head0","chead0","head1","chead1","head2","chead2"]
    search_fields = ('post_id',)

