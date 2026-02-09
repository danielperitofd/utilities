"""
Views for BMP Converter application.
"""
import os
import zipfile
import io
from django.shortcuts import render, redirect
from django.http import FileResponse, HttpResponse
from django.views.decorators.http import require_http_methods
from django.conf import settings
from PIL import Image


UPLOAD_FOLDER = settings.MEDIA_ROOT / 'uploads'
OUTPUT_FOLDER = settings.MEDIA_ROOT / 'converted'

# Ensure folders exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)


@require_http_methods(["GET", "POST"])
def index(request):
    """Handle image upload and conversion."""
    if request.method == 'POST':
        files = request.FILES.getlist('file')
        width = int(request.POST.get('width', 200))
        height = int(request.POST.get('height', 150))
        
        if not files:
            return HttpResponse("No files uploaded", status=400)
        
        for file in files:
            if file.name == '':
                continue
            
            # Save uploaded file
            filepath = UPLOAD_FOLDER / file.name
            with open(filepath, 'wb+') as f:
                for chunk in file.chunks():
                    f.write(chunk)
            
            # Convert to BMP
            img = Image.open(filepath)
            img = img.resize((width, height), Image.Resampling.LANCZOS)
            bmp_filename = os.path.splitext(file.name)[0] + '.bmp'
            bmp_filepath = OUTPUT_FOLDER / bmp_filename
            img.save(bmp_filepath)
    
    # Load converted images for gallery
    images = []
    if os.path.exists(OUTPUT_FOLDER):
        images = sorted(os.listdir(OUTPUT_FOLDER))
    
    context = {
        'images': images,
    }
    return render(request, 'index.html', context)


@require_http_methods(["GET"])
def download_image(request, filename):
    """Download a single converted image."""
    filepath = OUTPUT_FOLDER / filename
    
    if not filepath.exists():
        return HttpResponse("File not found", status=404)
    
    return FileResponse(
        open(filepath, 'rb'),
        as_attachment=True,
        filename=filename
    )


@require_http_methods(["POST"])
def download_selected(request):
    """Download selected images as ZIP."""
    selected_images = request.POST.getlist('selected_images')
    
    if not selected_images:
        return HttpResponse("No images selected", status=400)
    
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w') as zip_file:
        for image in selected_images:
            image_path = OUTPUT_FOLDER / image
            if image_path.exists():
                zip_file.write(image_path, image)
    
    zip_buffer.seek(0)
    return FileResponse(
        zip_buffer,
        as_attachment=True,
        filename='selected_images.zip',
        content_type='application/zip'
    )


@require_http_methods(["POST"])
def download_all(request):
    """Download all converted images as ZIP."""
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w') as zip_file:
        if os.path.exists(OUTPUT_FOLDER):
            for bmp_file in os.listdir(OUTPUT_FOLDER):
                bmp_path = OUTPUT_FOLDER / bmp_file
                zip_file.write(bmp_path, bmp_file)
    
    zip_buffer.seek(0)
    return FileResponse(
        zip_buffer,
        as_attachment=True,
        filename='all_converted_images.zip',
        content_type='application/zip'
    )


@require_http_methods(["POST"])
def clear_images(request):
    """Clear uploaded and converted images."""
    folders_to_clear = [UPLOAD_FOLDER, OUTPUT_FOLDER]
    
    for folder in folders_to_clear:
        if os.path.exists(folder):
            for filename in os.listdir(folder):
                file_path = os.path.join(folder, filename)
                if os.path.isfile(file_path):
                    os.remove(file_path)
    
    return redirect('index')
