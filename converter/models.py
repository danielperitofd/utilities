from django.db import models
import base64

class ImageUpload(models.Model):
    """Modelo para armazenar imagens carregadas"""
    original_filename = models.CharField(max_length=255)
    custom_name = models.CharField(max_length=255, blank=True, null=True)
    original_image = models.BinaryField()  # Imagem original em bytes
    image_preview_base64 = models.TextField()  # Base64 para preview
    width = models.IntegerField(default=200)
    height = models.IntegerField(default=150)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    converted = models.BooleanField(default=False)
    session_id = models.CharField(max_length=255, blank=True, null=True)  # Para agrupar uploads
    
    class Meta:
        ordering = ['-uploaded_at']
    
    def __str__(self):
        return f"{self.custom_name or self.original_filename}"


class ConvertedImage(models.Model):
    """Modelo para armazenar imagens convertidas em BMP"""
    original_upload = models.OneToOneField(ImageUpload, on_delete=models.CASCADE, related_name='converted_image')
    filename = models.CharField(max_length=255)
    bmp_image = models.BinaryField()  # Imagem BMP em bytes
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.filename
