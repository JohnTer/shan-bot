from django.shortcuts import get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.forms.models import model_to_dict
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View
from django.utils.decorators import method_decorator

import vk_api
import orjson
import requests
from vk_api.utils import get_random_id
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from shanbot import settings

vk_session = vk_api.VkApi(
    token=settings.VK_API_TOKEN)
vk = vk_session.get_api()
confirmation_code = settings.VK_CONFIRMATION_CODE
secret_key = settings.VK_SECRET_KEY

# vk_session.auth(token_only=True)


def download_picture():
    path = "https://cataas.com/cat"
    r = requests.get(path, stream=True)
    if r.status_code == 200:
        with open("temp.image", 'wb') as f:
            for chunk in r:
                f.write(chunk)


@method_decorator(csrf_exempt, name='dispatch')
class EchoView(View):

    @csrf_exempt
    def post(self, request, *args, **kwargs):
        body_unicode = request.body
        data = orjson.loads(body_unicode)
        return
        print(data)

        if not data or 'type' not in data:
            return HttpResponse('not ok', status=422)

        if data['type'] == 'confirmation':
            return HttpResponse(confirmation_code, status=200)
        elif data['type'] == 'message_new':
            from_id = data['object']['message']['from_id']

            keyboard = VkKeyboard(one_time=True)

            keyboard.add_button('Лисички!', color=VkKeyboardColor.NEGATIVE)
            keyboard.add_line()  # Переход на вторую строку
            keyboard.add_button('Песики!', color=VkKeyboardColor.PRIMARY)
            keyboard.add_button('Котики!', color=VkKeyboardColor.PRIMARY)

            attachments = []

            mess = data['object']['message']['text']

            if mess == "Котики!!!":
                path = "https://cataas.com/cat"

                upload = vk_api.VkUpload(vk_session)
                image = requests.get(path, stream=True)
                photo = upload.photo_messages(photos=image.raw)[0]
                attachments.append(
                    'photo{}_{}'.format(photo['owner_id'], photo['id'])
                )
                vk.messages.send(
                    peer_id=from_id,
                    attachment=','.join(attachments),
                    random_id=get_random_id(),
                    message='Кися',
                    keyboard=keyboard.get_keyboard()
                )
            elif mess == "Песики!!!":
                jpath = "https://dog.ceo/api/breeds/image/random"
                path = orjson.loads((requests.get(jpath).text))["message"]

                upload = vk_api.VkUpload(vk_session)
                image = requests.get(path, stream=True)
                photo = upload.photo_messages(photos=image.raw)[0]
                attachments.append(
                    'photo{}_{}'.format(photo['owner_id'], photo['id'])
                )
                vk.messages.send(
                    peer_id=from_id,
                    attachment=','.join(attachments),
                    random_id=get_random_id(),
                    message='Песя',
                    keyboard=keyboard.get_keyboard()
                )
            elif mess == "Лисички!!!":
                jpath = "https://randomfox.ca/floof/"
                path = orjson.loads((requests.get(jpath).text))["image"]

                upload = vk_api.VkUpload(vk_session)
                image = requests.get(path, stream=True)
                photo = upload.photo_messages(photos=image.raw)[0]
                attachments.append(
                    'photo{}_{}'.format(photo['owner_id'], photo['id'])
                )
                vk.messages.send(
                    peer_id=from_id,
                    attachment=','.join(attachments),
                    random_id=get_random_id(),
                    message='Лисичка',
                    keyboard=keyboard.get_keyboard()
                )
            elif mess == "":
                pass

            else:

                vk.messages.send(
                    message=mess,
                    random_id=get_random_id(),
                    peer_id=from_id,
                    keyboard=keyboard.get_keyboard()
                )
            return HttpResponse('ok', status=200)
        return HttpResponse('ok', status=200)