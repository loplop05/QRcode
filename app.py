import os
import sys
import base64
import webbrowser
from io import BytesIO
from threading import Timer
from flask import Flask, request, jsonify, render_template
import qrcode

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    try:
        data = request.get_json() or {}
        url = data.get('url', '').strip()
        filename = data.get('filename', '').strip()

        # Fallback to default if empty
        if not filename:
            filename = 'qrcode'

        if not url:
            return jsonify({"success": False, "message": "URL cannot be empty"}), 400

        # Sanitize filename (remove path structures to avoid saving outside the workspace)
        filename = os.path.basename(filename)
        if not filename.lower().endswith('.png'):
            filename += '.png'

        # Create QR code
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=10,
            border=4,
        )
        qr.add_data(url)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")

        # Save to disk
        img.save(filename)

        # Convert to base64 for preview
        buffered = BytesIO()
        img.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode('utf-8')
        img_base64 = f"data:image/png;base64,{img_str}"

        return jsonify({
            "success": True,
            "message": f"QR code saved successfully as {filename}",
            "image_data": img_base64,
            "filename": filename
        })
    except Exception as e:
        return jsonify({"success": False, "message": f"An unexpected error occurred: {str(e)}"}), 500

def open_browser():
    webbrowser.open_new("http://127.0.0.1:5000/")

if __name__ == '__main__':
    # Start the browser helper thread
    Timer(1.5, open_browser).start()
    # Run the server locally
    app.run(host='127.0.0.1', port=5000, debug=False)
