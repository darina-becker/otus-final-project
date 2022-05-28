from django.contrib import admin

from app.models import App, AppKind, AppAgeLimit, AppCategory, Comment, Rating

admin.site.register(App)
admin.site.register(AppKind)
admin.site.register(AppAgeLimit)
admin.site.register(AppCategory)


class CommentInline(admin.StackedInline):
    model = Comment
    extra = 0


class AppAdmin(admin.ModelAdmin):
    inlines = [
        CommentInline,
    ]


admin.site.register(Comment)
admin.site.register(Rating)
