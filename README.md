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

4. Install [Selenium](https://selenium.dev), [OpenAI's Whisper model](https://openai.com/index/whisper), and [python-telegram-bot](https://python-telegram-bot.org)
```shell
pip install selenium openai-whisper python-telegram-bot
```

5. Replace `chat_id` value in `env.toml` with your telegram chat ID as in the example below. You can find your chat ID by texting `/start` to `@BotFather` on Telegram.
```toml
bot_token = "0123456789:ZEE5TER5YUnFYreIy1ptnLmenta0a6vQriT"
```

5. Replace `chat_id` value in `env.toml` with your telegram chat ID as in the example below. You can find your chat ID by texting `/start` to `@GetMyIDBot` on Telegram.
```toml
chat_id = "0123456789"
```

6. Run the script
```shell
python bot.py
```
