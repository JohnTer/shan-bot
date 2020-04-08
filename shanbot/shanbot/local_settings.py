import orjson

SERVICE_CONFIG_PATH = "/etc/shan-bot/config.json"

config = None
with open(SERVICE_CONFIG_PATH, "r") as f:
    config = orjson.loads(f.read())

VK_API_TOKEN = config["vk_token"]
VK_CONFIRMATION_CODE = config["vk_confirmation_code"]
VK_SECRET_KEY = config["vk_secret_key"]
