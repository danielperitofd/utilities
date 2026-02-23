from django.contrib import admin
from .models import ImageUpload, ConvertedImage

@admin.register(ImageUpload)
class ImageUploadAdmin(admin.ModelAdmin):
    list_display = ('id', 'original_filename', 'custom_name', 'uploaded_at', 'converted', 'session_id')
    list_filter = ('uploaded_at', 'converted')
    search_fields = ('original_filename', 'custom_name', 'session_id')
    readonly_fields = ('uploaded_at',)


@admin.register(ConvertedImage)
class ConvertedImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'filename', 'created_at', 'original_upload')
    list_filter = ('created_at',)
    search_fields = ('filename',)
    readonly_fields = ('created_at',)
