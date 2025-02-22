import logging
import os
import requests

log = logging.getLogger(__name__)

MODEL_DIR = os.path.expanduser("~/ai/piper/model/")

piper_models = {
    "ar_JO-kareem-low": "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/ar/ar_JO/kareem/low/ar_JO-kareem-low.onnx",
    "ar_JO-kareem-medium": "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/ar/ar_JO/kareem/medium/ar_JO-kareem-medium.onnx",
    "ca_ES-upc_ona-x_low": "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/ca/ca_ES/upc_ona/x_low/ca_ES-upc_ona-x_low.onnx",
    "ca_ES-upc_ona-medium": "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/ca/ca_ES/upc_ona/medium/ca_ES-upc_ona-medium.onnx",
    "ca_ES-upc_pau-x_low": "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/ca/ca_ES/upc_pau/x_low/ca_ES-upc_pau-x_low.onnx",
    "cs_CZ-jirka-low": "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/cs/cs_CZ/jirka/low/cs_CZ-jirka-low.onnx",
    "cs_CZ-jirka-medium": "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/cs/cs_CZ/jirka/medium/cs_CZ-jirka-medium.onnx",
    "cy_GB-gwryw_gogleddol-medium": "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/cy/cy_GB/gwryw_gogleddol/medium/cy_GB-gwryw_gogleddol-medium.onnx",
    "da_DK-talesyntese-medium": "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/da/da_DK/talesyntese/medium/da_DK-talesyntese-medium.onnx",
    "de_DE-eva_k-x_low": "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/de/de_DE/eva_k/x_low/de_DE-eva_k-x_low.onnx",
    "de_DE-karlsson-low": "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/de/de_DE/karlsson/low/de_DE-karlsson-low.onnx",
    "de_DE-kerstin-low": "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/de/de_DE/kerstin/low/de_DE-kerstin-low.onnx",
    "de_DE-mls-medium": "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/de/de_DE/mls/medium/de_DE-mls-medium.onnx",
    "de_DE-pavoque-low": "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/de/de_DE/pavoque/low/de_DE-pavoque-low.onnx",
    "de_DE-ramona-low": "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/de/de_DE/ramona/low/de_DE-ramona-low.onnx",
    "de_DE-thorsten-low": "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/de/de_DE/thorsten/low/de_DE-thorsten-low.onnx",
    "de_DE-thorsten-medium": "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/de/de_DE/thorsten/medium/de_DE-thorsten-medium.onnx",
    "de_DE-thorsten-high": "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/de/de_DE/thorsten/high/de_DE-thorsten-high.onnx",
    "de_DE-thorsten_emotional-medium": "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/de/de_DE/thorsten_emotional/medium/de_DE-thorsten_emotional-medium.onnx",
    "el_GR-rapunzelina-low": "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/el/el_GR/rapunzelina/low/el_GR-rapunzelina-low.onnx",
    "en_GB-alan-low": "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/en/en_GB/alan/low/en_GB-alan-low.onnx",
    "en_GB-alan-medium": "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/en/en_GB/alan/medium/en_GB-alan-medium.onnx",
    "en_GB-alba-medium": "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/en/en_GB/alba/medium/en_GB-alba-medium.onnx",
    "en_GB-aru-medium": "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/en/en_GB/aru/medium/en_GB-aru-medium.onnx",
    "en_GB-cori-medium": "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/en/en_GB/cori/medium/en_GB-cori-medium.onnx",
    "en_GB-cori-high": "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/en/en_GB/cori/high/en_GB-cori-high.onnx",
    "en_GB-jenny_dioco-medium": "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/en/en_GB/jenny_dioco/medium/en_GB-jenny_dioco-medium.onnx",
    "en_GB-northern_english_male-medium": "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/en/en_GB/northern_english_male/medium/en_GB-northern_english_male-medium.onnx"
}


def get_model(model_name):
    if model_name not in piper_models:
        log.error(f"Model '{model_name}' not found in the dictionary.")
        return None

    onnx_filename = f"{model_name}.onnx"
    json_filename = f"{model_name}.onnx.json"
    onnx_file_path = os.path.join(MODEL_DIR, onnx_filename)
    json_file_path = os.path.join(MODEL_DIR, json_filename)

    if not os.path.exists(onnx_file_path):
        url = piper_models[model_name]
        log.info(f"Downloading {model_name} (.onnx) to {onnx_file_path}...")
        try:
            response = requests.get(url, stream=True)
            response.raise_for_status()

            with open(onnx_file_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
            log.info(f"Download complete: {onnx_file_path}")

        except requests.exceptions.RequestException as e:
            log.error(f"Error downloading {model_name} (.onnx): {e}")
            return None
    else:
        log.info(f"Model (.onnx) already exists at {onnx_file_path}")

    if not os.path.exists(json_file_path):
        json_url = f"{piper_models[model_name]}.json"
        log.info(f"Downloading {model_name} (.onnx.json) to {json_file_path}...")
        try:
            response = requests.get(json_url, stream=True)
            response.raise_for_status()

            with open(json_file_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
            log.info(f"Download complete: {json_file_path}")

        except requests.exceptions.RequestException as e:
            log.error(f"Error downloading {model_name} (.onnx.json): {e}")
            return None
    else:
        log.info(f"Model config (.onnx.json) already exists at {json_file_path}")

    return onnx_file_path

def get_voices():
    return [k for k in piper_models.keys()]
