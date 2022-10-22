import base64
from concurrent.futures import ThreadPoolExecutor
import io
from typing import Optional, Dict, Any

from quart import Blueprint, render_template, redirect
from quart_schema import hide_route, validate_request, validate_response
from pydantic.dataclasses import dataclass

from tts.api.lib import TTS
from tts.api.lib import InferenceBackend
from tts.api.lib.wavfile import write

blueprint = Blueprint("blueprint", __name__)


max_thread_workers: Optional[int] = None
tts_settings: Dict[str, Any] = {"noise_scale": 0.667, "length_scale": 1.0}
vocoder_settings: Dict[str, Any] = {"denoiser_strength": 0.005}

backend = InferenceBackend("pytorch")
executor = ThreadPoolExecutor(max_workers=max_thread_workers)
tts = TTS(voice_or_lang="kathleen-glow_tts",
          vocoder_or_quality="low",  # "high", "medium", "low"
          backend="pytorch",
          tts_settings=tts_settings,
          vocoder_settings=vocoder_settings,
          executor=executor,
          denoiser_strength=vocoder_settings["denoiser_strength"],
          custom_voices_dir="tts/voices",
          )


@blueprint.route("/")
@hide_route
async def index():
    return redirect("/docs")


@dataclass
class TextSchema:
    """Text data."""
    data: str


@dataclass
class DataSchema(TextSchema):
    """Speech data."""
    pass


@blueprint.route("/tts", methods=["POST"])
@validate_request(TextSchema)
@validate_response(DataSchema)
async def post(data: TextSchema):
    """Text to speech.
    The function returns list of floating point numbers representing wav.
    """
    tts_results = tts.text_to_speech(text=data.data)
    for result_idx, result in enumerate(tts_results):
        with io.BytesIO() as wav_io:
            write(wav_io, result.sample_rate, result.audio)
            wav_data = wav_io.getvalue()
            data = base64.encodebytes(wav_data).decode('ascii')

    return {"data": data}
