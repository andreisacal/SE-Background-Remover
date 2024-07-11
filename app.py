from flask import Flask, render_template, request, send_file
import requests
from PIL import Image
from io import BytesIO

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return 'No file uploaded', 400
        file = request.files['file']
        if file.filename == '':
            return 'No file selected', 400
        if file:
            # Open the uploaded image file
            input_image = Image.open(file.stream)
            
            # Save the image to a temporary BytesIO object
            img_io = BytesIO()
            input_image.save(img_io, format='PNG')
            img_io.seek(0)
            
            # Call the remove.bg API
            api_key = 'YOUR_API'
            response = requests.post(
                'https://api.remove.bg/v1.0/removebg',
                files={'image_file': img_io},
                data={'size': 'auto'},
                headers={'X-Api-Key': api_key},
            )
            
            if response.status_code == requests.codes.ok:
                output_img_io = BytesIO(response.content)
                output_img_io.seek(0)
                return send_file(output_img_io, mimetype='image/png', as_attachment=True, download_name='no_bg.png')
            else:
                return f"Error: {response.status_code} - {response.text}", 500

    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5100)
