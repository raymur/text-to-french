from io import BytesIO
from kokoro import KPipeline
from IPython.display import display, Audio
import soundfile as sf
from flask import Flask, jsonify, render_template, request, send_file


pipeline = KPipeline(lang_code='f')
app = Flask(__name__)
app.config['TESTING'] = True
app.config['DEBUG'] = True
app.config['TEMPLATES_AUTO_RELOAD'] = True


@app.route("/", methods=['GET'])
def home():
    return render_template('index.html')

@app.route("/", methods=['POST'])
def get_wavs():
    text = request.json.get('text')
    generator = pipeline(
        text, voice='ff_siwis',
        speed=1, split_pattern=r'\n+'
    )
    for i, (graphemes, phonemes, audio) in enumerate(generator):
        fn = f'{i}.wav'
        sf.write(fn, audio, 24000)
    # TODO: zip files and send multiple over
    return send_file(fn,  mimetype='audio/wav', download_name=fn, as_attachment=True)

if __name__=="__main__":
    app.run()