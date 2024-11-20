from django.contrib import admin
from .models import Category, SubCategory

class CategoryAdmin(admin.ModelAdmin):
    # Display the category name and its parent category in the list view
    list_display = ('name', 'parent')

    # Enable filtering by parent category (so you can filter subcategories by parent)
    list_filter = ('parent',)

    # Enable search by category name
    search_fields = ('name',)

    # Display the parent field as a dropdown in the admin form
    fieldsets = (
        (None, {
            'fields': ('name', 'parent')
        }),
    )

    # Show the subcategories related to the category in the admin
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.prefetch_related('subcategories')

# Register the Category model with the admin
admin.site.register(Category, CategoryAdmin)
admin.site.register(SubCategory)
