# Requirements

Assuming that you are running this script on a Debian/Ubuntu Native or WSL environment, these are the steps you need to follow

1. Follow the [instructions](https://developer.nvidia.com/cuda-downloads) to install Install CUDA.
    - [Debian](https://developer.nvidia.com/cuda-downloads?target_os=Linux&target_arch=x86_64&Distribution=Debian&target_version=12&target_type=deb_network)
    - [WUbuntu](https://developer.nvidia.com/cuda-downloads?target_os=Linux&target_arch=x86_64&Distribution=Ubuntu&target_version=24.04&target_type=deb_network)
    - [WSL-Ubuntu](https://developer.nvidia.com/cuda-downloads?target_os=Linux&target_arch=x86_64&Distribution=WSL-Ubuntu&target_version=2.0&target_type=deb_network)

2. Install [`ffmpeg`](https://ffmpeg.org)
```shell
sudo apt install ffmpeg
```

3. **Recommended:** Create a [Conda](https://docs.anaconda.com/miniconda) environment and activate it
```shell
conda create -n isere-rdv-bot
conda activate isere-rdv-bot
```

4. Install [Selenium](https://selenium.dev) and [OpenAI's Whisper](https://openai.com/index/whisper)
```python
pip install selenium openai-whisper
```

5. Run the script
```python
python bot.py
```
