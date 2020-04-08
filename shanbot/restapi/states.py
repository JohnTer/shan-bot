import random
import time
from vk_utils import text_message, quiz_message
from .models import USER_STATES, Message, User, IncomingMessage, Quiz, Award, Secret
from vk_utils import keyboards_preset


class BaseStateProcess(object):
    def __init__(self, vk_api):
        self.vk_api = vk_api

    def _clean_message(self, text):
        return text.strip().lower()

    def _validate_text(self, text):
        pass

    def send_message(self, message_type, keyboard, to_id, text=None):
        message_to_send = Message.objects.get(
            message_type=message_type)
        tm = text_message.TextMessange(
            self.vk_api, message_to_send.text, to_id=to_id, keyboard=keyboard)
        tm.execute()

    def process(self):
        raise NotImplementedError


class BeginStateProcessor(BaseStateProcess):
    def __init__(self, vk_api):
        BaseStateProcess.__init__(self, vk_api)
        self.accept_choice = set(["начать"])
        self.next_state = USER_STATES[1]

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
        keyboard = keyboards_preset.RestartKeyboard.get_keyboard()
        to_id = user.vk_id
        self.send_message(message_type, keyboard, to_id)
        user.state = self.next_state

    def to_next_state(self, user):
        message_type = "start_message"
        keyboard = keyboards_preset.StartKeyboard.get_keyboard()
        to_id = user.vk_id
        self.send_message(message_type, keyboard, to_id)
        user.state = self.next_state


class StartStateProcessor(BaseStateProcess):
    def __init__(self, vk_api):
        BaseStateProcess.__init__(self, vk_api)
        self.accept_choice = set(["да", "yes", "y"])
        self.refuse_choice = set(["нет", "no", "n"])
        self.next_state = USER_STATES[2]

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
        keyboard = keyboards_preset.StartKeyboard.get_keyboard()
        to_id = user.vk_id
        self.send_message(message_type, keyboard, to_id)

    def stay_current(self, user):
        message_type = "refuse_message"
        keyboard = keyboards_preset.RestartKeyboard.get_keyboard()
        to_id = user.vk_id
        self.send_message(message_type, keyboard, to_id)
        user.state = USER_STATES[0]

    def to_next_state(self, user):
        message_type = "hello_message"
        keyboard = keyboards_preset.HelloKeyboard.get_keyboard()
        to_id = user.vk_id
        self.send_message(message_type, keyboard, to_id)
        user.state = self.next_state


class HelloStateProcessor(BaseStateProcess):
    def __init__(self, vk_api):
        BaseStateProcess.__init__(self, vk_api)
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
        keyboard = keyboards_preset.HelloKeyboard.get_keyboard()
        to_id = user.vk_id
        self.send_message(message_type, keyboard, to_id)

    def stay_current(self, user):
        message_type = "invalid_message"
        keyboard = keyboards_preset.HelloKeyboard.get_keyboard()
        to_id = user.vk_id
        self.send_message(message_type, keyboard, to_id)

    def to_next_state(self, user):
        message_type = "greeting_message"
        keyboard = keyboards_preset.GreetingKeyboard.get_keyboard()
        to_id = user.vk_id
        message_to_send = Message.objects.get(message_type=message_type)
        tm = text_message.TextMessange(
            self.vk_api, message_to_send.text.format(user.first_name), to_id=to_id, keyboard=keyboard)
        tm.execute()
        user.state = self.next_state


class GreetingStateProcessor(BaseStateProcess):
    def __init__(self, vk_api):
        BaseStateProcess.__init__(self, vk_api)
        self.accept_choice = set(["крутяк, давай!"])
        self.next_state = USER_STATES[4]

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
        keyboard = keyboards_preset.GreetingKeyboard.get_keyboard()
        to_id = user.vk_id
        self.send_message(message_type, keyboard, to_id)

    def to_next_state(self, user):
        message_type = "greeting_video_link"
        
        keyboard = keyboards_preset.NormalKeyboard.get_keyboard()
        to_id = user.vk_id
        self.send_message(message_type, keyboard, to_id)
        
        message_type = "normal_message"
        self.send_message(message_type, keyboard, to_id)
        user.state = self.next_state


class NormalStateProcessor(BaseStateProcess):
    def __init__(self, vk_api):
        BaseStateProcess.__init__(self, vk_api)
        self.quiz_choice = set(["задания"])
        self.secret_mode = set(["секретик"])
        self.quiz_state = USER_STATES[5]
        self.secret_state = USER_STATES[6]

    def process(self, user, incoming_message):
        text = self._clean_message(incoming_message.text)
        if text in self.quiz_choice:
            self.to_quiz_state(user)
            user.save()
        elif text in self.secret_mode:
            self.to_secret_state(user)
            user.save()
        else:
            self.stay_current(user)

    def to_quiz_state(self, user):
        message_type = "from_normal_to_choice"
        keyboard = keyboards_preset.QuizKeyboard.get_keyboard()
        to_id = user.vk_id
        self.send_message(message_type, keyboard, to_id)
        user.state = USER_STATES[5]

    def to_secret_state(self, user):
        message_type = "from_normal_to_secret"
        keyboard = keyboards_preset.SecretKeyboard.get_keyboard()
        to_id = user.vk_id
        self.send_message(message_type, keyboard, to_id)
        user.state = USER_STATES[6]

    def stay_current(self, user):
        message_type = "invalid_message"
        keyboard = keyboards_preset.NormalKeyboard.get_keyboard()
        to_id = user.vk_id
        self.send_message(message_type, keyboard, to_id)


class QuizStateProcessor(BaseStateProcess):
    def __init__(self, vk_api):
        BaseStateProcess.__init__(self, vk_api)
        self.back_choice = set(["назад"])
        self.new_task_mode = set(["новое задание"])
        self.normal_state = USER_STATES[4]

    def process(self, user, incoming_message):
        text = self._clean_message(incoming_message.text)
        if text in self.back_choice:
            self.to_normal_state(user)
            user.save()
        elif text in self.new_task_mode or user.solving_mode:
            last_quiz_solve = user.last_quiz_solve
            try:
                current_time = int(time.time())
                quiz = Quiz.objects.get(order=last_quiz_solve + 1)
                if quiz.available_unixtime > current_time and not user.admin_mode:
                    raise Quiz.DoesNotExist
            except Quiz.DoesNotExist:
                self.no_task_message(user)
            else:
                self.play(user, quiz, incoming_message)
                user.save()
        else:
            self.stay_current(user)

    def stay_current(self, user):
        message_type = "invalid_message"
        keyboard = keyboards_preset.QuizKeyboard.get_keyboard()
        to_id = user.vk_id
        self.send_message(message_type, keyboard, to_id)

    def to_normal_state(self, user):
        message_type = "normal_message_from_quiz"
        keyboard = keyboards_preset.NormalKeyboard.get_keyboard()
        to_id = user.vk_id
        self.send_message(message_type, keyboard, to_id)
        user.state = self.normal_state
        user.solving_mode = False

    def no_task_message(self, user):
        message_type = "quiz_no_task"
        keyboard = keyboards_preset.QuizKeyboard.get_keyboard()
        to_id = user.vk_id
        self.send_message(message_type, keyboard, to_id)

    def wrong_answer_message(self, user):
        message_type = "wrong_answer"
        keyboard = None
        to_id = user.vk_id
        self.send_message(message_type, keyboard, to_id)

    def right_answer_message(self, user):
        message_type = "right_answer"
        keyboard = keyboards_preset.QuizKeyboard.get_keyboard()
        to_id = user.vk_id
        self.send_message(message_type, keyboard, to_id)

    def play(self, user, quiz, incoming_message):
        quiz_game = quiz_message.QuizGame(self.vk_api, quiz, user)
        if user.solving_mode == False:
            self._new_game(user, quiz_game)
        else:
            self._continue_game(user, quiz, quiz_game, incoming_message)

    def _new_game(self, user, quiz_game):
        user.solving_mode = True
        user.save()
        quiz_game.send_task()

    def _continue_game(self, user, quiz, quiz_game, incoming_message):
        if not quiz_game.is_answer_right(incoming_message.text):
            self.wrong_answer_message(user)
            quiz_game.send_task()
        else:
            self.check_award(quiz, user)
            user.solving_mode = False
            user.last_quiz_solve += 1

    def check_award(self, quiz, user):
        if quiz.award_id is None:
            self.right_answer_message(user)
            return
        award = quiz.award_id
        tm = text_message.TextMessange(self.vk_api, award.text, to_id=user.vk_id,
                                       attachments=award.attachments_json, keyboard=keyboards_preset.QuizKeyboard.get_keyboard())
        tm.execute()


class SecretStateProcessor(BaseStateProcess):
    def __init__(self, vk_api):
        BaseStateProcess.__init__(self, vk_api)
        self.back_choice = set(["назад"])
        self.new_secret = set(["новый секретик"])
        self.normal_state = USER_STATES[4]

        self.random_text = ("Ах!", "Ох!", "Ага!", "Ба!", "Ля!")

    def process(self, user, incoming_message):
        text = self._clean_message(incoming_message.text)
        if text in self.back_choice:
            self.to_normal_state(user)
            user.save()
        elif text in self.new_secret:
            self.send_secret(user)
        else:
            self.stay_current(user)

    def send_secret(self, user):
        secrets = Secret.objects.filter(order_type=0)
        secret = random.choice(secrets)
        keyboard = keyboards_preset.SecretKeyboard.get_keyboard()
        to_id = user.vk_id
        text = random.choice(
            self.random_text) if secret.text is None else secret.text

        tm = text_message.TextMessange(
            self.vk_api, text, to_id=to_id, keyboard=keyboard, attachments=secret.attachments_json)
        tm.execute()

    def stay_current(self, user):
        message_type = "invalid_message"
        keyboard = keyboards_preset.SecretKeyboard.get_keyboard()
        to_id = user.vk_id
        self.send_message(message_type, keyboard, to_id)

    def to_normal_state(self, user):
        message_type = "normal_message_from_quiz"
        keyboard = keyboards_preset.NormalKeyboard.get_keyboard()
        to_id = user.vk_id
        self.send_message(message_type, keyboard, to_id)
        user.state = self.normal_state
        user.solving_mode = False


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
        elif state == USER_STATES[6]:
            SecretStateProcessor(self.vk_api).process(user, incoming_message)

    def execute(self, incoming_message):
        user = self._check_new_person(incoming_message)
        if user is None:
            user = User.objects.get(vk_id=incoming_message.from_id)
        self._pipeline(user, incoming_message)
