from django.contrib import admin


from .models.branch import Branch

@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "name"
    ]