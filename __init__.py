import requests
import json
import os
import time
import logging
import torchaudio
logging.basicConfig()
logging.root.setLevel(logging.NOTSET)

# add work dir
dir_current = os.getcwd()

def load_audio_comfy_format(path_data):
    waveform, sample_rate = torchaudio.load(path_data)
    audio = {"waveform": waveform.unsqueeze(0), "sample_rate": sample_rate}
    return audio
def write_data_from_url(url, object_path):
    object_data = requests.get(url).content
    with open(object_path, "wb") as handler:
        handler.write(object_data)
def json_read_update_write(filename_input, filename_output, content):
    f = open(filename_input)
    data = json.load(f)
    data.update(content)
    logging.info("file_output {}".format(data),)
    with open(filename_output, 'w') as f:
        json.dump(data, f, indent=4)
def jen_process_check(id):
    url = "https://jen.futureverseai.com/api/v1/public/generation_status/{}".format(id)
    headers = {'accept': 'application/json', 'Authorization': 'Bearer {}'.format(jen_api_key)}

    response = requests.request("GET", url, headers=headers)
    download_url = None
    if response.json()["data"]["status"] != "validated":
        return False, download_url
    else:
        download_url = response.json()["data"]["url"]
        if download_url != None:
            response = requests.get(download_url)
            status_code = response.status_code
            if status_code == 200:
                return True, download_url
            else:
                return False, download_url
        else:
            return True, download_url
def jen_get_api_key_from_config():
    p = os.path.dirname(os.path.realpath(__file__))
    path_config = os.path.join(p, "config.json")
    f = open(path_config)
    data = json.load(f)
    jen_api_key = data["JEN_API_KEY"]
    return jen_api_key

jen_api_key = jen_get_api_key_from_config()

class JEN_download:
    def __init__(self):
        pass
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "id": ("STRING", {"default": "123-123-123"}),
                "format": ("STRING", {"default": "mp3"}),
                "dest_dir": ("STRING", {"default": "output/JEN"}),
                "local_test": ("BOOLEAN", {"default": False},),
            }
        }

    # define output
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("id",)
    FUNCTION = "run"
    OUTPUT_NODE = True
    CATEGORY = "JEN"

    def run(self, id, format, dest_dir, local_test):
        assert format in ["wav", "mp3"]
        os.makedirs(os.path.join(dir_current, dest_dir), exist_ok=True)
        dest_dir = os.path.join(dir_current, dest_dir)
        path_generate = os.path.join(dest_dir, "download." + format)
        logging.info("path_generate {}".format(path_generate))
        if not local_test:
            validated, download_url = jen_process_check(id)
            if validated:
                data_genearte = requests.get(download_url).content
                with open(path_generate, "wb") as handler:
                    handler.write(data_genearte)
        return str(id)

class JEN_generate:
    def __init__(self):
        pass
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "prompt": ("STRING", {"default": "party edm"}),
                "format": ("STRING", {"default": "mp3"}),
                "fadeOutLength": ("INT", {"default": 0}),
                "duration": ("INT", {"default": 10}),
                "dest_dir": ("STRING", {"default": "output/JEN"}),
                "local_test": ("BOOLEAN", {"default": False},),
            }
        }

    # define output
    RETURN_TYPES = ("AUDIO", "STRING", "STRING",)
    RETURN_NAMES = ("audio", "id", "creditBalance",)
    FUNCTION = "run"
    OUTPUT_NODE = True
    CATEGORY = "JEN"

    def run(self, prompt, format, fadeOutLength, duration, dest_dir, local_test):
        assert format in ["wav", "mp3"]
        assert duration in [10, 45]
        os.makedirs(os.path.join(dir_current, dest_dir), exist_ok=True)
        dest_dir = os.path.join(dir_current, dest_dir)
        path_generate = os.path.join(dest_dir, "generate." + format)
        logging.info("path_generate {}".format(path_generate))
        id = ""; creditBalance = "/"
        if not local_test:
            url = "https://jen.futureverseai.com/api/v1/public/track/generate"
            payload = {'prompt': prompt, "format": format, "fadeOutLength": fadeOutLength, "duration": duration}
            # payload = json.dumps(payload)
            # payload = {'prompt': prompt, "format": format, "fadeOutLength": fadeOutLength, "duration": duration}
            logging.info("payload {}".format(payload))
            headers = {'accept': 'application/json', 'Authorization': 'Bearer {}'.format(jen_api_key)}
            response = requests.request("POST", url, headers=headers, json=payload)

            response = response.json()
            logging.info("response {}".format(response))

            data = response["data"][0]
            id = data["id"]; status = data["status"]; creditBalance = response["creditBalance"]
            count = 0
            while (True):
                try:
                    logging.info("checking progress")
                    validated, download_url = jen_process_check(id)
                    if validated:
                        data_genearte = requests.get(download_url).content
                        with open(path_generate, "wb") as handler:
                            handler.write(data_genearte)
                        break

                except Exception as e:
                    logging.info(str(e))
                time.sleep(5)
                count += 1
                if count > 15:
                    logging.info("timeout waiting for geneartion, you can still check your results by id")
                    break


        audio = load_audio_comfy_format(path_generate)
        return audio, str(id), str(creditBalance)

class JEN_extend:
    def __init__(self):
        pass
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "id": ("STRING", {"default": "123-123-123"}),
                "prompt": ("STRING", {"default": "party edm"}),
                "format": ("STRING", {"default": "mp3"}),
                "fadeOutLength": ("INT", {"default": 0}),
                "duration": ("INT", {"default": 20}),
                "dest_dir": ("STRING", {"default": "output/JEN"}),
                "local_test": ("BOOLEAN", {"default": False},),
            }
        }

    # define output
    RETURN_TYPES = ("AUDIO", "STRING", "STRING",)
    RETURN_NAMES = ("audio", "id", "creditBalance",)
    FUNCTION = "run"
    OUTPUT_NODE = True
    CATEGORY = "JEN"

    def run(self, id, prompt, format, fadeOutLength, duration, dest_dir, local_test):
        assert format in ["wav", "mp3"]
        assert duration in [20, 40]
        os.makedirs(os.path.join(dir_current, dest_dir), exist_ok=True)
        dest_dir = os.path.join(dir_current, dest_dir)
        path_extend = os.path.join(dest_dir, "extend." + format)
        logging.info("path_extend {}".format(path_extend))
        creditBalance = "/"
        if not local_test:
            url = "https://jen.futureverseai.com/api/v1/public/track/extend/{}".format(id)
            payload = {'prompt': prompt, "format": format, "fadeOutLength": fadeOutLength, "duration": duration}
            # payload = json.dumps(payload)
            # payload = {'prompt': prompt, "format": format, "fadeOutLength": fadeOutLength, "duration": duration}
            logging.info("payload {}".format(payload))
            headers = {'accept': 'application/json', 'Authorization': 'Bearer {}'.format(jen_api_key)}
            response = requests.request("POST", url, headers=headers, json=payload)

            response = response.json()
            logging.info("response {}".format(response))

            data = response["data"][0]
            id = data["id"]; status = data["status"]; creditBalance = response["creditBalance"]
            count = 0
            while (True):
                try:
                    logging.info("checking progress")
                    validated, download_url = jen_process_check(id)
                    if validated:
                        data_genearte = requests.get(download_url).content
                        with open(path_extend, "wb") as handler:
                            handler.write(data_genearte)
                        break

                except Exception as e:
                    logging.info(str(e))
                time.sleep(5)
                count += 1
                if count > 20:
                    logging.info("timeout waiting for geneartion, you can still check your results by id")
                    break
        audio = load_audio_comfy_format(path_extend)
        return audio, str(id), str(creditBalance)

# export node
NODE_CLASS_MAPPINGS = {
    "JEN_generate": JEN_generate,
    "JEN_download": JEN_download,
    "JEN_extend": JEN_extend
}
NODE_DISPLAY_NAME_MAPPINGS = {
    "JEN_generate": "ComfyUI-JEN-generate",
    "JEN_download": "ComfyUI-JEN-download",
    "JEN_extend": "ComfyUI-JEN-extend"
}

__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS']


if __name__ == '__main__':
    JEN_generate = JEN_generate()
    JEN_extend = JEN_extend()

    # prompt = "party edm"
    # format = "mp3"
    # fadeOutLength = 0
    # duration = 10
    # dest_dir = "."; local_test = False
    # JEN_generate.run(prompt, format, fadeOutLength, duration, dest_dir, local_test)

    # id = "123123"
    # prompt = "party edm"
    # format = "mp3"
    # fadeOutLength = 0
    # duration = 20
    # dest_dir = "."; local_test = False
    # JEN_extend.run(id, prompt, format, fadeOutLength, duration, dest_dir, local_test)

