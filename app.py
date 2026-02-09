from flask import Flask, request, render_template, send_file, url_for, redirect
from PIL import Image
import os
import zipfile
import io

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'static/converted'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        files = request.files.getlist('file')
        width = int(request.form.get('width', 200))
        height = int(request.form.get('height', 150))
        
        if not files:
            return "No files uploaded", 400
        
        for file in files:
            if file.filename == '':
                continue
            filepath = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(filepath)
            img = Image.open(filepath)
            
            # Adiciona rotação de 90 graus para a direita
            img = img.rotate(-360, expand=True)
            
            img = img.resize((width, height), Image.Resampling.LANCZOS)
            bmp_filename = os.path.splitext(file.filename)[0] + '.bmp'
            bmp_filepath = os.path.join(OUTPUT_FOLDER, bmp_filename)
            img.save(bmp_filepath)
        
        # Carregar as imagens convertidas para exibição na galeria
        images = os.listdir(OUTPUT_FOLDER)
        return render_template('index.html', images=images)
    
    # Carregar a página inicial com as imagens já convertidas
    images = os.listdir(OUTPUT_FOLDER)
    return render_template('index.html', images=images)

@app.route('/download-image/<filename>')
def download_image(filename):
    filepath = os.path.join(OUTPUT_FOLDER, filename)
    return send_file(filepath, as_attachment=True, download_name=filename)

@app.route('/download-selected', methods=['POST'])
def download_selected():
    selected_images = request.form.getlist('selected_images')
    if not selected_images:
        return "No images selected", 400
    
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w') as zip_file:
        for image in selected_images:
            image_path = os.path.join(OUTPUT_FOLDER, image)
            zip_file.write(image_path, image)
    
    zip_buffer.seek(0)
    return send_file(zip_buffer, as_attachment=True, download_name='selected_images.zip', mimetype='application/zip')

@app.route('/download-all', methods=['POST'])
def download_all():
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w') as zip_file:
        for bmp_file in os.listdir(OUTPUT_FOLDER):
            zip_file.write(os.path.join(OUTPUT_FOLDER, bmp_file), bmp_file)
    
    zip_buffer.seek(0)
    return send_file(zip_buffer, as_attachment=True, download_name='all_converted_images.zip', mimetype='application/zip')

@app.route('/clear-images', methods=['POST'])
def clear_images():
    folders_to_clear = [UPLOAD_FOLDER, OUTPUT_FOLDER]
    for folder in folders_to_clear:
        for filename in os.listdir(folder):
            file_path = os.path.join(folder, filename)
            if os.path.isfile(file_path):
                os.remove(file_path)
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
