from flask import Flask, render_template
import vk_api

app = Flask(__name__)
vk_session = vk_api.VkApi('LOGIN', 'PASSWORD')
try:
    vk_session.auth(token_only=True)
except vk_api.AuthError as error_msg:
    print(f'Ошибка авторизации: {error_msg}')
    quit()


@app.route('/vk_stats/<int:group_id>')
def homepage(group_id):
    stats = vk_session.get_api().stats.get(group_id=group_id, fields='reach')[:10]
    total_likes = 0
    total_comments = 0
    total_subscribed = 0
    age_map = {
        '12-18': 0, '18-21': 0, '21-24': 0, '24-27': 0,
        '27-30': 0, '30-35': 0, '35-45': 0, '45-100': 0
    }
    cities = []

    for i in stats:
        total_likes += i.get('likes', 0) or 0
        total_comments += i.get('comments', 0) or 0
        total_subscribed += i.get('subscribed', 0) or 0

        for age in i.get('age_distribution', []):
            age_value = age.get('value')
            if age_value in age_map:
                age_map[age_value] += age.get('count', 0)

        for city in i.get('cities', []):
            city_name = city.get('name')
            if city_name and city_name not in cities:
                cities.append(city_name)

    return render_template('base.html',
                           total_likes=total_likes,
                           total_comments=total_comments,
                           total_subscribed=total_subscribed,
                           age_map=age_map,
                           cities=cities)

if __name__ == '__main__':
    app.run()