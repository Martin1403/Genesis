from halo import Halo
import base64
import os

from pydub import AudioSegment
from pydub.playback import play
from PyQt5.QtCore import QThread

from .utilities import DeepSpeech, make_request, save_audio, make_audio, text_filter
from .vad import VADAudio

text: str = ""


# Url for all endpoints:
url_service = []
for port, service in enumerate(["stt", "ai", "tts"], 1):
    url_service.append(f"http://{service}-service-c:500{port}/{service}"
                       if os.environ.get("DOCKER") else
                       f"http://127.0.0.1:500{port}/{service}")


# Headers:
# headers = {'accept': 'application/json'}
# content_headers = {'accept': 'application/json', 'Content-Type': 'application/json'}


def get_text():
    global text
    return text


class VadManager(QThread):
    def __init__(self, model_path):
        super().__init__()
        self.model_path = model_path

    def run(self):
        global text
        # VAD AUDIO SETTINGS
        vad_audio = VADAudio(aggressiveness=2,
                             device=None,
                             input_rate=44100 if os.environ.get("Docker") else 16000,
                             file=None)
        # DeepSpeech
        model = DeepSpeech(model_path=self.model_path)
        frames = vad_audio.vad_collector()
        spinner = Halo(spinner='dots')
        wav_data = bytearray()
        for frame in frames:
            if frame is not None:
                spinner.start()
                wav_data.extend(frame)
            elif "genesis" in model.transcribe(wav_data):
                spinner.stop()
                # SENDiNG DATA
                data = base64.encodebytes(wav_data).decode('ascii')                         # BYTES => STR
                response = make_request(url=url_service[0], data=data)                      # STR => STT
                user_text = response.json().get("data")                                     # STT => TEXT
                # Save audio
                save_audio(vad_audio, wav_data, user_text)
                response = make_request(url=url_service[1], data=user_text)                 # TEXT => AI
                ai_text = response.json().get("data")[:-1]                                  # AI => TEXT
                ai_text = text_filter(ai_text)
                response = make_request(url=url_service[2], data=ai_text)                   # TEXT => TTS
                data = response.json().get("data")                                          # TTS => STR
                data = base64.decodebytes(data.encode('ascii'))                             # STR => BYTES
                tts_path = make_audio(data)                                                            # BYTES => WAV
                audio_segment = AudioSegment.from_wav(tts_path)
                play(audio_segment)
                os.remove(tts_path)
                wav_data = bytearray()
                text = f"USER: {user_text}\nAI: {ai_text}"
            else:
                spinner.stop()
                wav_data = bytearray()
