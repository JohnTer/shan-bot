import vk_api as vk_api_lib
import orjson
from vk_api.utils import get_random_id


class TextMessange(object):
    def __init__(self, vk, text, attachments=None, incoming_message=None,
                 to_id=None, keyboard=None):

        if incoming_message is None and to_id is None:
            raise Exception("incoming_message and to_id are None")
        if text == "":
            raise Exception("text field is empty")
        self.vk_api = vk
        self.text = text
        self.attachments = attachments
        self.incoming_message = incoming_message
        self.to_id = to_id
        self.keyboard = None if keyboard is None else keyboard.get_keyboard()

    def send_message(self):
        peer_id = self.to_id if self.to_id is not None else self.incoming_message.from_id
        attachments = self._prepare_attachments(orjson.loads(
            self.attachments)["photo"]) if self.attachments is not None else None

        self.vk_api.messages.send(
            peer_id=peer_id,
            attachment=attachments,
            random_id=get_random_id(),
            message=self.text,
            keyboard=self.keyboard
        )

    def execute(self):
        self.send_message()

    def _prepare_attachments(self, attachment_dict):
        attachments = []
        upload = vk_api_lib.VkUpload(self.vk_api)
        for pht in attachment_dict:
            photo = upload.photo_messages(photos=pht)[0]
            attachments.append(
                'photo{}_{}'.format(photo['owner_id'], photo['id'])
            )
        return attachments
