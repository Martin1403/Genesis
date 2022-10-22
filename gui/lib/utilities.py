from deepspeech import Model
import os
import re

import numpy as np
import requests


count = 1
start = True
path_to_meta = "gui/data/metadata.csv"


def text_filter(text: str) -> str:
    """
    Filter text from AI before TTS
    :param: text (str)
    :return: text (str)
    """
    text = text.strip()
    text = re.sub(r"(\w) (\W)", r"\1\2", text)
    text = re.sub(r"(\W) (\W)", r"\1\2", text)
    text = text + "," if text[-1] not in [".", "?", ",", "!"] else text
    return text


def make_request(url: str, data: str) -> requests.post:
    """
    Returns complete POST request between services.
    :param url: (str) path etc.
    :param data: (str) data to post
    :return: request.post (object)
    """
    return requests.post(url=url, json={"data": data}, headers={"Content-Type": "application/json"})


def make_audio(data: bytes) -> str:
    """
    Make audio (WAV) from AI text to TTS
    :param data: bytes
    :return str: sample path
    """
    path = f"audio.wav"
    if os.path.isfile(path):
        os.remove(path)
    with open(path, mode="bx") as f:
        f.write(data)
    return path


def counter(num=1, length=3):
    """Counter etc. 0001, 0002
    Attributes:
    num (int) integer etc. 1 ==> 0001
        length (int) length of counter etc. 3 ==> 001
    Return:
        (str) etc. 0001
    """
    number = '0' * length + str(num)
    number = number[len(number)-length:]
    return number


def resolve_count() -> None:
    global count, start
    """
    Check metadata.csv and make count the last number
    :return: None
    """
    if start:
        try:
            with open(path_to_meta, "r", encoding="utf-8") as file:
                last_line = file.read().strip().splitlines()[-1]
                last_number = last_line.split("|")[0].split("-")[-1]
                count = int(last_number)
        except IndexError:
            pass
    else:
        start = False


def make_record(number, text):
    """
    MAke record to metadata.csv
    :return:
    """
    if not os.path.exists(path_to_meta):
        with open(path_to_meta, "w", encoding="utf-8"):
            pass
    resolve_count()
    with open(path_to_meta, "a", encoding="utf-8") as file:
        file.writelines(f"{number}|{text}\n")


def save_audio(vad_audio, wav_data: bytearray, user_text: str) -> None:
    global count
    """
    Save recorded audio.
    :param: vad_audio: VAD AUDIO (instance)
    :param: wav_data: wav bytearray from vad audio
    :param: user_text: text from STT service to save into metadata.csv
    :return: None
    """
    audio_folder = "gui/data/wavs"
    os.makedirs(audio_folder, exist_ok=True)
    audio_name = f"MV-001-{counter(count, 4)}"
    audio_path = os.path.join(audio_folder, f"{audio_name}.wav")
    # if os.path.exists(path):
    #     os.remove(path)
    vad_audio.write_wav(audio_path, wav_data)
    make_record(audio_name, user_text)
    count += 1


class DeepSpeech(object):
    """
    DeepSpeech tflite for recognizing wake up word.
    """
    def __init__(self, model_path: str, scorer_path: str = None) -> None:
        """
        Load model before recognizing. Load model only once.
        :param: model_path (str) path to model
        :param: scorer_pah (str) enable scorer whe  scorer is presented
        """
        self.model = Model(model_path)
        if scorer_path:
            self.model.enableExternalScorer(scorer_path)

    def transcribe(self, wav_data: bytearray) -> str:
        """
        From VAD (user_input) to Text to recognize wake up word
        Translate wav bytes to numpy int16 then feed deepspeech
        :param wav_data: (bytearray)
        :return: user_text (str)
        """
        return self.model.stt(np.frombuffer(wav_data, dtype=np.int16))
