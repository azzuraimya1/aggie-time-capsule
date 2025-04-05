from flask import Flask, render_template, request, redirect, send_from_directory
import os
import json
from datetime import datetime

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Create uploads folder if it doesn't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def load_memories():
    try:
        with open('memories.json', 'r') as f:
            return json.load(f)
    except:
        return []

def save_memory(memory):
    memories = load_memories()
    memories.append(memory)
    with open('memories.json', 'w') as f:
        json.dump(memories, f)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form['name']
        year = request.form['year']
        memory = request.form['memory']
        image = request.files['image']

        image_filename = None
        if image and image.filename:
            timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
            image_filename = f"{timestamp}_{image.filename}"
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], image_filename)
            image.save(image_path)

        save_memory({
            'name': name,
            'year': year,
            'memory': memory,
            'image': image_filename
        })

        return redirect('/')

    memories = load_memories()
    return render_template('index.html', memories=memories)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True)
