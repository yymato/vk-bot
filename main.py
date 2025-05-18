from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import random, vk_api

vk_session = vk_api.VkApi('LOGIN', 'PASSWORD')
try:
    vk_session.auth(token_only=True)
except vk_api.AuthError as error_msg:
    print(f'Ошибка авторизации: {error_msg}')
    quit()

vk_session_bot = vk_api.VkApi(
    token='TOKEN')
vk_bot = vk_session_bot.get_api()
longpoll = VkBotLongPoll(vk_session_bot, 12345)

photo_ids = [f"photo{i['owner_id']}_{i['id']}" for i
             in vk_session.get_api().photos.get(group_id=12345, album_id=12345)['items']]
for event in longpoll.listen():
    if event.type == VkBotEventType.MESSAGE_NEW:
        user_info = vk_bot.users.get(user_ids=event.object.message['from_id'], fields='first_name')[0]

        vk_bot.messages.send(user_id=event.object.message['from_id'],
                             message=f"Привет, {user_info['first_name']}!",
                             attachment=random.choice(photo_ids),
                             random_id=0)
