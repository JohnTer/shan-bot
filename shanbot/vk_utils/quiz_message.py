import orjson
import vk_api as vk_api_lib
from vk_api.utils import get_random_id
from vk_api.keyboard import VkKeyboard, VkKeyboardColor

from .text_message import TextMessange

PICTURE_CACHE = dict()

class QuizGame(object):
    def __init__(self, vk, quiz, user, attachments=None, to_id=None):
        self.vk_api = vk
        self.to_id = user.vk_id
        self.quiz = quiz
        answ = orjson.loads(quiz.answers_json)
        self.right_answer = answ['right_answer'].lower()
        self.answers = answ['answers']
        self._create_keyboard()

    def _create_keyboard(self):
        keyboard = VkKeyboard(one_time=False)
        answers = self.answers
        col_answer_count = 2
        N_ = len(answers) - 1
        for index, answ in enumerate(answers):
            if 0 < index:
                keyboard.add_line()
            keyboard.add_button(answ, color=VkKeyboardColor.DEFAULT)
        self.keyboard = keyboard.get_keyboard()

    def send_task(self):
        attachments = self._prepare_attachments(orjson.loads(self.quiz.attachments_json)[
                                                "photo"]) if self.quiz.attachments_json is not None else None

        self.vk_api.messages.send(
            peer_id=self.to_id,
            attachment=attachments,
            random_id=get_random_id(),
            message=self.quiz.text,
            keyboard=self.keyboard
        )

    def _clear_message(self, message):
        return message.strip().lower()

    def is_answer_right(self, user_answer):
        return True if self._clear_message(user_answer) == self.right_answer else False

    def _prepare_attachments(self, attachment_dict):
        attachments = []
        upload = vk_api_lib.VkUpload(self.vk_api)
        for pht in attachment_dict:
            if pht in PICTURE_CACHE:
                photo = PICTURE_CACHE[pht]
            else:
                photo = upload.photo_messages(photos=pht)[0]
                PICTURE_CACHE[pht] = photo
            attachments.append(
                'photo{}_{}_{}'.format(photo['owner_id'], photo['id'], photo['access_key'])
            )
        return attachments
