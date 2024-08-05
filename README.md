# Comfy-JEN
Comfy UI custom nodes for JEN music generation powered by Futureverse
## Installation
```shell
pip install -r requirements.txt
```
### Optional Dependencies
You may need following nodes to visualise contents:
1. [comfyui-mixlab-nodes](https://github.com/shadowcz007/comfyui-mixlab-nodes) for optional audio visualiser
2. [rgthree-comfy](https://github.com/rgthree/rgthree-comfy) for optional text output viewer
## API Key
You will need API key to run the nodes, no local model required.

### Guides
1. Sign up to JEN from https://app.jenmusic.ai/
2. Request API key from dashboard (feature about to release)
3. Create a config.json file under ComfyUI-JEN, copy and paste your API key in the file and save
4. run example workflow under workflow/
5. results will be automatically stored under dest_dir (default output/JEN)
6. file generate
```json
{
    "JEN_API_KEY": "YOUR_JEN_API_KEY"
}
```
## Example Workflow
### From track generation to track extend
Generate a 10s track, then extend it by 20s. Generated and extended files are saved under output/JEN or other destinations.
![JEN-generate_extend](workflow/JEN-generate_extend.png)
### Download existing track given ID
![JEN-generate_extend](workflow/JEN-download.png)
## License
Apache License Version 2.0

