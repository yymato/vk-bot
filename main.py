from random import random

import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType

import config


def captcha_handler(captcha):
    key = input('Enter captcha code {0}: '.format(captcha.get_url())).strip()
    return captcha.try_again(key)


def auth_handler():
    key = input('Enter authentication code: ')
    remember_device = True
    return key, remember_device


def main():
    login, password = config.LOGPAS
    vk_session = vk_api.VkApi(login, password)
    try:
        vk_session.auth(token_only=True)
    except vk_api.AuthError as error_msg:
        print(error_msg)
        return

    upload = vk_api.VkUpload(vk_session)
    photos = ['static/img/pic_cat.jpg', 'static/img/kitten.jpg']

    for item in photos:
        photo = upload.photo(
            item,
            album_id=config.ALBUM_ID,
            group_id=config.GROUP_ID
        )
        vk_photo_url = 'https://vk.com/photo{}_{}'.format(
            photo[0]['owner_id'], photo[0]['id']
        )
        vk_photo_id = f"photo{photo[0]['owner_id']}_{photo[0]['id']}"

        print(photo, vk_photo_id, vk_photo_url, sep="\n")
        vk = vk_session.get_api()
        vk.wall.post(message="Cats", attachments=[vk_photo_id])


if __name__ == '__main__':
    main()
