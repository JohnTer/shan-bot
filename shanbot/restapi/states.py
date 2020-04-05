from vk_utils import text_message, quiz_message
from .models import USER_STATES, Message, User, IncomingMessage, Quiz, Award
from vk_utils import keyboards_preset


class BeginStateProcessor(object):
    def __init__(self, vk_api):
        self.vk_api = vk_api
        self.accept_choice = set(["начать"])
        self.next_state = USER_STATES[1]

    def _clean_message(self, text):
        return text.strip().lower()

    def _validate_text(self, text):
        return True if text in self.accept_choice else False

    def process(self, user, incoming_message):
        text = self._clean_message(incoming_message.text)
        if not self._validate_text(text):
            self.stay_current(user)
        else:
            self.to_next_state(user)
            user.save()

    def stay_current(self, user):
        message_type = "restart_message"
        message_to_send = Message.objects.get(message_type=message_type)
        tm = text_message.TextMessange(
            self.vk_api, message_to_send.text, to_id=user.vk_id, keyboard=keyboards_preset.RestartKeyboard.get_keyboard())
        tm.execute()
        user.state = self.next_state

    def to_next_state(self, user):
        message_type = "start_message"
        message_to_send = Message.objects.get(message_type=message_type)
        tm = text_message.TextMessange(
            self.vk_api, message_to_send.text, to_id=user.vk_id, keyboard=keyboards_preset.StartKeyboard.get_keyboard())
        tm.execute()
        user.state = self.next_state


class StartStateProcessor(object):
    def __init__(self, vk_api):
        self.vk_api = vk_api
        self.accept_choice = set(["да", "yes", "y"])
        self.refuse_choice = set(["нет", "no", "n"])
        self.next_state = USER_STATES[2]

    def _clean_message(self, text):
        return text.strip().lower()

    def process(self, user, incoming_message):
        text = self._clean_message(incoming_message.text)
        if text in self.accept_choice:
            self.to_next_state(user)
            user.save()
        elif text in self.refuse_choice:
            self.stay_current(user)
            user.save()
        else:
            self.repeat_message(user)

    def repeat_message(self, user):
        message_type = "start_message"
        message_to_send = Message.objects.get(message_type=message_type)
        tm = text_message.TextMessange(
            self.vk_api, message_to_send.text, to_id=user.vk_id, keyboard=keyboards_preset.StartKeyboard.get_keyboard())
        tm.execute()

    def stay_current(self, user):
        message_type = "refuse_message"
        message_to_send = Message.objects.get(message_type=message_type)
        tm = text_message.TextMessange(
            self.vk_api, message_to_send.text, to_id=user.vk_id, keyboard=keyboards_preset.RestartKeyboard.get_keyboard())
        tm.execute()
        user.state = USER_STATES[0]

    def to_next_state(self, user):
        message_type = "hello_message"
        message_to_send = Message.objects.get(message_type=message_type)
        tm = text_message.TextMessange(
            self.vk_api, message_to_send.text, to_id=user.vk_id, keyboard=keyboards_preset.HelloKeyboard.get_keyboard())
        tm.execute()
        user.state = self.next_state


class HelloStateProcessor(object):
    def __init__(self, vk_api):
        self.vk_api = vk_api
        self.next_state = USER_STATES[3]

    def _clean_message(self, text):
        return text.strip()

    def _validate_text(self, text):
        return True if len(text.split()) == 1 else False

    def process(self, user, incoming_message):
        text = self._clean_message(incoming_message.text)
        if not self._validate_text(text):
            self.stay_current(user)
        else:
            user.first_name = incoming_message.text
            self.to_next_state(user)
            user.save()

    def repeat_message(self, user):
        message_type = "hello_message"
        message_to_send = Message.objects.get(message_type=message_type)
        tm = text_message.TextMessange(
            self.vk_api, message_to_send.text, to_id=user.vk_id, keyboard=keyboards_preset.HelloKeyboard.get_keyboard())
        tm.execute()

    def stay_current(self, user):
        message_type = "invalid_message"
        message_to_send = Message.objects.get(message_type=message_type)
        tm = text_message.TextMessange(
            self.vk_api, message_to_send.text, to_id=user.vk_id, keyboard=keyboards_preset.HelloKeyboard.get_keyboard())
        tm.execute()

    def to_next_state(self, user):
        message_type = "greeting_message"
        message_to_send = Message.objects.get(message_type=message_type)
        tm = text_message.TextMessange(
            self.vk_api, message_to_send.text.format(user.first_name), to_id=user.vk_id, keyboard=keyboards_preset.GreetingKeyboard.get_keyboard())
        tm.execute()
        user.state = self.next_state


class GreetingStateProcessor(object):
    def __init__(self, vk_api):
        self.vk_api = vk_api
        self.accept_choice = set(["крутяк, давай!"])
        self.next_state = USER_STATES[4]

    def _clean_message(self, text):
        return text.strip().lower()

    def _validate_text(self, text):
        text = self._clean_message(text)
        return True if text in self.accept_choice else False

    def process(self, user, incoming_message):
        if not self._validate_text(incoming_message.text):
            self.stay_current(user)
        else:
            self.to_next_state(user)
            user.save()

    def stay_current(self, user):
        message_type = "invalid_message"
        message_to_send = Message.objects.get(message_type=message_type)
        tm = text_message.TextMessange(
            self.vk_api, message_to_send.text, to_id=user.vk_id, keyboard=keyboards_preset.GreetingKeyboard.get_keyboard())
        tm.execute()

    def to_next_state(self, user):
        message_type = "normal_message"
        message_to_send = Message.objects.get(message_type=message_type)
        tm = text_message.TextMessange(
            self.vk_api, message_to_send.text, to_id=user.vk_id, keyboard=keyboards_preset.NormalKeyboard.get_keyboard())
        tm.execute()
        user.state = self.next_state


class NormalStateProcessor(object):
    def __init__(self, vk_api):
        self.vk_api = vk_api
        self.quiz_choice = set(["задания"])
        self.secret_mode = set(["секретик"])
        self.quiz_state = USER_STATES[5]
        self.secret_state = USER_STATES[6]

    def _clean_message(self, text):
        return text.strip().lower()

    def process(self, user, incoming_message):
        text = self._clean_message(incoming_message.text)
        if text in self.quiz_choice:
            self.to_quiz_state(user)
            user.save()
        else:
            self.stay_current(user)

    def to_quiz_state(self, user):
        message_type = "from_normal_to_choice"
        message_to_send = Message.objects.get(message_type=message_type)
        tm = text_message.TextMessange(
            self.vk_api, message_to_send.text, to_id=user.vk_id, keyboard=keyboards_preset.QuizKeyboard.get_keyboard())
        tm.execute()
        user.state = USER_STATES[5]

    def to_secret_state(self, user):
        self.stay_current(user)

    def stay_current(self, user):
        message_type = "invalid_message"
        message_to_send = Message.objects.get(message_type=message_type)
        tm = text_message.TextMessange(
            self.vk_api, message_to_send.text, to_id=user.vk_id, keyboard=keyboards_preset.NormalKeyboard.get_keyboard())
        tm.execute()


class QuizStateProcessor(object):
    def __init__(self, vk_api):
        self.vk_api = vk_api
        self.back_choice = set(["назад"])
        self.new_task_mode = set(["новое задание"])
        self.normal_state = USER_STATES[4]

    def _clean_message(self, text):
        return text.strip().lower()

    def process(self, user, incoming_message):
        text = self._clean_message(incoming_message.text)
        if text in self.back_choice:
            self.to_normal_state(user)
            user.save()
        elif text in self.new_task_mode or user.solving_mode:
            last_quiz_solve = user.last_quiz_solve
            try:
                quiz = Quiz.objects.get(order=last_quiz_solve + 1)
            except Quiz.DoesNotExist:
                self.no_task_message(user)
            else:
                self.play(user, quiz, incoming_message)
                user.save()
        else:
            self.stay_current(user)

    def stay_current(self, user):
        message_type = "invalid_message"
        message_to_send = Message.objects.get(message_type=message_type)
        tm = text_message.TextMessange(
            self.vk_api, message_to_send.text, to_id=user.vk_id, keyboard=keyboards_preset.QuizKeyboard.get_keyboard())
        tm.execute()

    def to_normal_state(self, user):
        message_type = "normal_message_from_quiz"
        message_to_send = Message.objects.get(message_type=message_type)
        tm = text_message.TextMessange(
            self.vk_api, message_to_send.text, to_id=user.vk_id, keyboard=keyboards_preset.NormalKeyboard.get_keyboard())
        tm.execute()
        user.state = self.normal_state
        user.solving_mode = False

    def no_task_message(self, user):
        message_type = "quiz_no_task"
        message_to_send = Message.objects.get(message_type=message_type)
        tm = text_message.TextMessange(
            self.vk_api, message_to_send.text, to_id=user.vk_id, keyboard=keyboards_preset.QuizKeyboard.get_keyboard())
        tm.execute()

    def wrong_answer_message(self, user):
        message_type = "wrong_answer"
        message_to_send = Message.objects.get(message_type=message_type)
        tm = text_message.TextMessange(
            self.vk_api, message_to_send.text, to_id=user.vk_id)
        tm.execute()

    def right_answer_message(self, user):
        message_type = "right_answer"
        message_to_send = Message.objects.get(message_type=message_type)
        tm = text_message.TextMessange(
            self.vk_api, message_to_send.text, to_id=user.vk_id, keyboard=keyboards_preset.QuizKeyboard.get_keyboard())
        tm.execute()

    def play(self, user, quiz, incoming_message):
        quiz_game = quiz_message.QuizGame(self.vk_api, quiz, user)
        if user.solving_mode == False:
            user.solving_mode = True
            user.save()
            quiz_game.send_task()
        else:
            if not quiz_game.is_answer_right(incoming_message.text):
                self.wrong_answer_message(user)
                quiz_game.send_task()
            else:
                self.right_answer_message(user)
                self.check_award(quiz, user)
                user.solving_mode = False
                user.last_quiz_solve += 1

    def check_award(self, quiz, user):
        if quiz.award_id is None:
            return
        award = quiz.award_id
        tm = text_message.TextMessange(
            self.vk_api, award.text, to_id=user.vk_id, attachments=award.attachments_json)
        tm.execute()


class StateEngine():
    def __init__(self, vk_api):
        self.user_cache = set()
        self.vk_api = vk_api

    def _check_new_person(self, incoming_message):
        user_id = incoming_message.from_id
        try:
            User.objects.get(vk_id=user_id)
        except User.DoesNotExist:
            user = User.objects.create(vk_id=user_id)
            user.save()
            self.user_cache.add(user_id)
            return user
        else:
            return None

    def _pipeline(self, user, incoming_message):
        state = user.state
        if state == USER_STATES[0]:  # start
            BeginStateProcessor(self.vk_api).process(user, incoming_message)
        elif state == USER_STATES[1]:  # hello
            StartStateProcessor(self.vk_api).process(user, incoming_message)
        elif state == USER_STATES[2]:
            HelloStateProcessor(self.vk_api).process(user, incoming_message)
        elif state == USER_STATES[3]:
            GreetingStateProcessor(self.vk_api).process(user, incoming_message)
        elif state == USER_STATES[4]:
            NormalStateProcessor(self.vk_api).process(user, incoming_message)
        elif state == USER_STATES[5]:
            QuizStateProcessor(self.vk_api).process(user, incoming_message)

    def execute(self, incoming_message):
        user = self._check_new_person(incoming_message)
        if user is None:
            user = User.objects.get(vk_id=incoming_message.from_id)
        self._pipeline(user, incoming_message)
