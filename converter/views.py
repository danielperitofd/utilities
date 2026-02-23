"""
Views for BMP Converter application with database storage.
"""
import os
import zipfile
import io
import base64
import uuid
from django.shortcuts import render, redirect, get_object_or_404
from django.http import FileResponse, HttpResponse, JsonResponse
from django.views.decorators.http import require_http_methods
from django.conf import settings
from PIL import Image
from .models import ImageUpload, ConvertedImage


@require_http_methods(["GET", "POST"])
def index(request):
    """Handle image upload and conversion."""
    session_id = request.session.get('session_id')
    if not session_id:
        session_id = str(uuid.uuid4())
        request.session['session_id'] = session_id
    
    if request.method == 'POST':
        # Check if it's a rename submission (has custom_names)
        if 'custom_names' in request.POST:
            return handle_conversion_with_names(request, session_id)
        else:
            return handle_upload(request, session_id)
    
    # Load converted images from database
    converted_images = ConvertedImage.objects.filter(
        original_upload__session_id=session_id
    ).order_by('-created_at')
    
    context = {
        'converted_images': converted_images,
        'show_rename_form': False,
    }
    return render(request, 'index.html', context)


def handle_upload(request, session_id):
    """Handle image upload and prepare for renaming."""
    files = request.FILES.getlist('file')
    width = int(request.POST.get('width', 200))
    height = int(request.POST.get('height', 150))
    
    if not files:
        return HttpResponse("No files uploaded", status=400)
    
    # Save uploaded files to database
    uploaded_files = []
    for file in files:
        if file.name == '':
            continue
        
        # Read file content
        file_content = file.read()
        
        # Create preview (thumbnail as base64)
        try:
            img = Image.open(io.BytesIO(file_content))
            img.thumbnail((150, 150))
            
            # Convert to base64
            img_io = io.BytesIO()
            img.save(img_io, format='PNG')
            img_io.seek(0)
            preview_base64 = base64.b64encode(img_io.getvalue()).decode()
            
        except Exception as e:
            preview_base64 = ''
            print(f"Error creating preview: {str(e)}")
        
        # Save to database
        name_without_ext = os.path.splitext(file.name)[0]
        image_upload = ImageUpload.objects.create(
            original_filename=file.name,
            custom_name=name_without_ext,
            original_image=file_content,
            image_preview_base64=preview_base64,
            width=width,
            height=height,
            session_id=session_id,
        )
        
        uploaded_files.append({
            'id': image_upload.id,
            'original_name': file.name,
            'name_without_ext': name_without_ext,
            'preview_base64': preview_base64,
        })
    
    context = {
        'uploaded_files': uploaded_files,
        'width': width,
        'height': height,
        'converted_images': [],
        'show_rename_form': True,
    }
    return render(request, 'index.html', context)


def handle_conversion_with_names(request, session_id):
    """Convert images with custom names."""
    width = int(request.POST.get('width', 200))
    height = int(request.POST.get('height', 150))
    
    # Get all uploaded images for this session that haven't been converted yet
    image_ids = request.POST.getlist('image_ids')
    custom_names = request.POST.getlist('custom_names')
    
    # Process conversions
    for image_id, custom_name in zip(image_ids, custom_names):
        custom_name = custom_name.strip()
        
        try:
            image_upload = ImageUpload.objects.get(id=image_id, session_id=session_id)
            
            # Open original image from database
            img = Image.open(io.BytesIO(image_upload.original_image))
            img = img.resize((width, height), Image.Resampling.LANCZOS)
            
            # Create BMP filename
            final_name = custom_name if custom_name else os.path.splitext(image_upload.original_filename)[0]
            bmp_filename = final_name + '.bmp'
            
            # Save BMP to bytes
            bmp_io = io.BytesIO()
            img.save(bmp_io, format='BMP')
            bmp_io.seek(0)
            bmp_content = bmp_io.getvalue()
            
            # Save to database
            ConvertedImage.objects.create(
                original_upload=image_upload,
                filename=bmp_filename,
                bmp_image=bmp_content,
            )
            
            # Mark as converted
            image_upload.converted = True
            image_upload.custom_name = custom_name
            image_upload.save()
            
        except ImageUpload.DoesNotExist:
            print(f"Image with id {image_id} not found")
            continue
        except Exception as e:
            print(f"Error converting image {image_id}: {str(e)}")
    
    # Load converted images for gallery
    converted_images = ConvertedImage.objects.filter(
        original_upload__session_id=session_id
    ).order_by('-created_at')
    
    context = {
        'converted_images': converted_images,
        'show_rename_form': False,
    }
    return render(request, 'index.html', context)


@require_http_methods(["GET"])
def download_image(request, image_id):
    """Download a single converted image."""
    converted_image = get_object_or_404(ConvertedImage, id=image_id)
    
    return FileResponse(
        io.BytesIO(converted_image.bmp_image),
        as_attachment=True,
        filename=converted_image.filename
    )


@require_http_methods(["POST"])
def download_selected(request):
    """Download selected images as ZIP."""
    selected_ids = request.POST.getlist('selected_images')
    
    if not selected_ids:
        return HttpResponse("No images selected", status=400)
    
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w') as zip_file:
        for image_id in selected_ids:
            try:
                converted_image = ConvertedImage.objects.get(id=image_id)
                zip_file.writestr(
                    converted_image.filename,
                    converted_image.bmp_image
                )
            except ConvertedImage.DoesNotExist:
                continue
    
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
    session_id = request.session.get('session_id')
    
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w') as zip_file:
        converted_images = ConvertedImage.objects.filter(
            original_upload__session_id=session_id
        )
        for converted_image in converted_images:
            zip_file.writestr(
                converted_image.filename,
                converted_image.bmp_image
            )
    
    zip_buffer.seek(0)
    return FileResponse(
        zip_buffer,
        as_attachment=True,
        filename='all_converted_images.zip',
        content_type='application/zip'
    )


@require_http_methods(["POST"])
def clear_images(request):
    """Clear images for current session."""
    session_id = request.session.get('session_id')
    
    if session_id:
        # Delete converted images first
        ConvertedImage.objects.filter(
            original_upload__session_id=session_id
        ).delete()
        
        # Delete uploaded images
        ImageUpload.objects.filter(session_id=session_id).delete()
    
    return redirect('index')


@require_http_methods(["POST"])
def delete_image(request, image_id):
    """Delete a specific converted image."""
    converted_image = get_object_or_404(ConvertedImage, id=image_id)
    converted_image.delete()
    
    return JsonResponse({'status': 'deleted'})
