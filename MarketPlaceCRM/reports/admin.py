from django.contrib import admin
from .models import Report, Reports


class ReportInline(admin.TabularInline):  # Или admin.StackedInline для более подробного отображения
    model = Report
    extra = 0  # Количество пустых форм для добавления новых объектов

class ReportsAdmin(admin.ModelAdmin):
    inlines = [ReportInline]

# Register your models here.
admin.site.register(Report)
admin.site.register(Reports)

# Register your models here.
