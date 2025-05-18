from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import vk_api, requests, json

vk_session = vk_api.VkApi(
    token='TOKEN')
longpoll = VkBotLongPoll(vk_session, 230403835)
vk = vk_session.get_api()
upload = vk_api.VkUpload(vk_session)

kb = {
    "one_time": False,
    "buttons": [[{"action": {"type": "text", "label": "map"}, "color": "primary"}],
                [{"action": {"type": "text", "label": "sat"}, "color": "primary"}]]
}
users_data = {}

kb = json.dumps(kb, ensure_ascii=False)

for event in longpoll.listen():
    if event.type == VkBotEventType.MESSAGE_NEW:
        if event.obj.message['text'] in ['map', 'sat']:
            if event.obj.message['from_id'] not in users_data:
                vk.messages.send(user_id=event.obj.message['from_id'], random_id=0,
                                 message=f"Сначала напишите, что хотите увидеть")
            else:
                response = requests.get(
                    f'http://static-maps.yandex.ru/1.x/?ll={users_data[event.obj.message['from_id']]
                    ['geo']}&z=10&l={event.obj.message['text']}')
                with open(f'{event.obj.message['from_id']}.png', 'wb') as f:
                    f.write(response.content)
                photo = upload.photo_messages(f'{event.obj.message['from_id']}.png')[0]
                vk.messages.send(user_id=event.obj.message['from_id'], random_id=0,
                                 attachment=f"photo{photo['owner_id']}_{photo['id']}",
                                 message=f"Это {users_data[event.obj.message['from_id']]['name']}. Что вы хотите увидеть?")
        else:
            response = requests.get('https://geocode-maps.yandex.ru/v1',
                               params={'apikey': '62621221-4d79-48d0-83e1-f7b8aa92eca3',
                                       'geocode': event.obj.message['text'],
                                       'lang': 'ru_RU',
                                       'format': 'json'})
            if response:
                geo_pos = response.json()['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['Point'][
                    'pos'].replace(' ', ',')

                if event.obj.message['from_id'] not in users_data:
                    users_data[event.obj.message['from_id']] = {'geo': geo_pos, 'name': event.obj.message['text']}
                else:
                    users_data[event.obj.message['from_id']]['geo'] = geo_pos
                    users_data[event.obj.message['from_id']]['name'] = event.obj.message['text']

                vk.messages.send(user_id=event.obj.message['from_id'], random_id=0, keyboard=kb,
                                 message=f"Отлично, теперь выберите на клавиатуре какой в каком типе карты показать")
            else:
                vk.messages.send(user_id=event.obj.message['from_id'], random_id=0,
                                 message=f"Ошибка геокодирования. Возможно такого места не существует")
