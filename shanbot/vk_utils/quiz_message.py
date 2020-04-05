import orjson
import vk_api
from vk_api.utils import get_random_id
from vk_api.keyboard import VkKeyboard, VkKeyboardColor

from .text_message import TextMessange

picture_cache = dict()


class QuizGame(object):
    def __init__(self, vk, quiz, user, attachments=None, to_id=None):
        self.vk = vk
        self.to_id = user.vk_id
        self.quiz = quiz

        answ = orjson.loads(quiz.answers_json)

        self.right_answer = answ['right_answer'].lower()
        self.answers = answ['answers']
        self._create_keyboard()

    def _create_keyboard(self):
        keyboard = VkKeyboard(one_time=False)
        for index, answ in enumerate(self.answers):
            if 0 < index:
                keyboard.add_line()
            keyboard.add_button(answ, color=VkKeyboardColor.DEFAULT)
        self.keyboard = keyboard.get_keyboard()

    def _clear_message(self, message):
        return message.strip().lower()

    def _prepare_attachments(self, attachment_dict):
        attachments = []
        upload = vk_api.VkUpload(self.vk)
        for pht in attachment_dict:
            if pht in picture_cache:
                photo = picture_cache[pht]
            else:
                photo = upload.photo_messages(photos=pht)[0]
                picture_cache[pht] = photo
            attachments.append(
                'photo{}_{}_{}'.format(
                    photo['owner_id'], photo['id'], photo['access_key'])
            )
        return attachments

    def is_answer_right(self, user_answer):
        clean_answer = self._clear_message(user_answer)
        if clean_answer == self.right_answer:
            return True
        return False

    def send_task(self):
        if self.quiz.attachments_json is not None:
            attachments = self._prepare_attachments(
                orjson.loads(self.quiz.attachments_json))
        else:
            attachments = None

        self.vk.messages.send(
            peer_id=self.to_id,
            attachment=attachments,
            random_id=get_random_id(),
            message=self.quiz.text,
            keyboard=self.keyboard
        )
