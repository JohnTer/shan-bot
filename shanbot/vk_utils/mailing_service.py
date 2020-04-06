import orjson
import vk_api
from vk_api.utils import get_random_id

picture_cache = dict()

class TextMessange(object):
    def __init__(self, vk, text, attachments=None, incoming_message=None,
                 to_id=None, keyboard=None):

        if incoming_message is None and to_id is None:
            raise AttributeError("Incoming_message and to_id are None")
        if text == "":
            raise AttributeError("Text field is empty")
        self.vk = vk
        self.text = text
        self.attachments = attachments
        self.incoming_message = incoming_message
        self.to_id = to_id
        self.keyboard = None if keyboard is None else keyboard.get_keyboard()

    def _send_message(self):
        peer_id = self.to_id if self.to_id is not None else self.incoming_message.from_id
        attachments = self._prepare_attachments(orjson.loads(
            self.attachments)["photo"]) if self.attachments is not None else None

        self.vk.messages.send(
            peer_id=peer_id,
            attachment=attachments,
            random_id=get_random_id(),
            message=self.text,
            keyboard=self.keyboard
        )

    def _prepare_attachments(self, attachment_dict):
        attachments = []
        upload = vk_api.VkUpload(self.vk)
        for pht in attachment_dict:
            if pht in picture_cache:
                photo = picture_cache[pht]
                print("KKKKKKK")
            else:
                photo = upload.photo_messages(photos=pht)[0]
                picture_cache[pht] = photo 
            attachments.append(
                'photo{}_{}_{}'.format(
                    photo['owner_id'], photo['id'], photo['access_key'])
            )
        return attachments

    def execute(self):
        self._send_message()
