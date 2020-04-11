import orjson
import vk_api
from .text_message import TextMessange
from .keyboards_preset import NormalKeyboard


class MailingService(object):
    def __init__(self, vk, command_dict):
        self.command = command_dict["type"]
        self.user_list = command_dict["user_list"]
        self.text = command_dict["text"]
        self.attachments = command_dict["attachments"]

        self.vk = vk
        self.keyboard = NormalKeyboard.get_keyboard()

    def _get_active_users(self):
        response = self.vk.groups.get_members(
            group_id=193982859, offset=0, count=150, sort='time_asc')
        users = response['items']
        return users

    def _send_message(self, to_id):
        tm = TextMessange(self.vk, self.text, to_id=to_id,
                          keyboard=self.keyboard, attachments=self.attachments)
        tm.execute()

    def execute(self):
        if not self.user_list:
            self.user_list = self._get_active_users()
        for user in self.user_list:
            try:
                self._send_message(user)
            except Exception as e:
                with open("mailling_exeptions.txt", "a") as f:
                    f.write(str(e) + "\n\n")
