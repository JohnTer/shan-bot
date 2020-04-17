from vk_api.keyboard import VkKeyboard, VkKeyboardColor


class RestartKeyboard(object):
    @classmethod
    def get_keyboard(self):
        keyboard = VkKeyboard(one_time=False)
        keyboard.add_button('Начать', color=VkKeyboardColor.PRIMARY)
        return keyboard


class StartKeyboard(object):
    @classmethod
    def get_keyboard(self):
        keyboard = VkKeyboard(one_time=True)

        keyboard.add_button('Нет', color=VkKeyboardColor.NEGATIVE)
        keyboard.add_button('Да', color=VkKeyboardColor.POSITIVE)
        return keyboard


class HelloKeyboard(object):
    @classmethod
    def get_keyboard(self):
        return None


class GreetingKeyboard(object):
    @classmethod
    def get_keyboard(self):
        keyboard = VkKeyboard(one_time=False)
        keyboard.add_button('Крутяк, давай!', color=VkKeyboardColor.PRIMARY)
        return keyboard


class NormalKeyboard(object):
    @classmethod
    def get_keyboard(self):
        keyboard = VkKeyboard(one_time=False)

        keyboard.add_button('Задания\U0001F340', color=VkKeyboardColor.PRIMARY)
        keyboard.add_button('Секретик\U00002728',
                            color=VkKeyboardColor.POSITIVE)
        return keyboard


class QuizKeyboard(object):
    @classmethod
    def get_keyboard(self):
        keyboard = VkKeyboard(one_time=True)

        keyboard.add_button('Назад', color=VkKeyboardColor.DEFAULT)
        keyboard.add_button('Новое задание', color=VkKeyboardColor.PRIMARY)
        return keyboard


class SecretKeyboard(object):
    @classmethod
    def get_keyboard(self):
        keyboard = VkKeyboard(one_time=True)

        keyboard.add_button('Назад', color=VkKeyboardColor.DEFAULT)
        keyboard.add_button('Новый секретик', color=VkKeyboardColor.POSITIVE)
        return keyboard


class BackOnlyKeyboard(object):
    @classmethod
    def get_keyboard(self):
        keyboard = VkKeyboard(one_time=False)

        keyboard.add_button('Назад', color=VkKeyboardColor.DEFAULT)
        return keyboard
