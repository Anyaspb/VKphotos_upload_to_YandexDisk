import requests
import time
import json

class VK:

    def __init__(self, access_token, user_id, version='5.131'):
        self.token = access_token
        self.id = user_id
        self.version = version
        self.params = {'access_token': self.token, 'v': self.version}


    def photo_from_profile(self):
        url = 'https://api.vk.com/method/photos.get'
        params2 = {'owner_id': profile_number, 'album_id': 'profile', 'extended': 1}
        res = requests.get(url, params={**self.params, **params2}).json()
        return res

    def get_photos(self):
        data = vk.photo_from_profile()
        count_foto = int(data['response']['count'])
        i = 0
        fotos = []
        links = {}
        like_check = []
        for i in range(count_foto):
            file_url = data['response']['items'][i]['sizes'][-1]['url']
            date = int(data['response']['items'][i]['date'])
            likes = data['response']['items'][i]['likes']['count']
            if likes in like_check:
                filename = str(date)
            else:
                filename = str(likes)
            like_check.append(likes)
            fotos.append({'filename': ('%s.jpg' % filename), 'size': 'z'})
            links[filename] = file_url
            time.sleep(0.1)
        with open('info.json', 'w') as f:
            json.dump(fotos, f)
        return links


class YandexDisk:

    def __init__(self, token):
        self.token = token

    def get_headers(self):
        return {
            'Content-Type': 'application/json',
            'Authorization': 'OAuth {}'.format(self.token)
        }

    def create_folder(self):
        folder_url = 'https://cloud-api.yandex.net/v1/disk/resources?path=%2Fimages'
        headers = self.get_headers()
        response = requests.put(folder_url, headers=headers)
        response.raise_for_status()
        if response.status_code == 201:
            print("Success")

    def save_file_to_disk(self, file_url, filename):
        upload_url = 'https://cloud-api.yandex.net/v1/disk/resources/upload'
        headers = self.get_headers()
        params = {"url": file_url, "path": 'images/%s' % filename}
        response = requests.post(upload_url, headers=headers, params=params)
        return response

    def uploading_photos(self, links_list):
        log = []
        for name, url in links_list.items():
            self.save_file_to_disk(url, name)
            log.append(f'Файл {name}.jpg загружен')
        with open('log.txt', 'w') as f:
            for line in log:
                f.write(line + '\n')
            f.write(f'Всего загружено {len(log)} файл(ов)')





if __name__ == '__main__':

    # ввести свой токен и id VK
    access_token = '...'
    user_id = '...'
    vk = VK(access_token, user_id)
    # запрос входных данных
    profile_number = input('Введите id пользователя vk для сохранения фото профиля: ')
    token = input('Введите токен с Полигона Яндекс.Диска, куда сохраним фото: ')
    # получения списка ссылок на фото
    links = vk.get_photos()

    uploader = YandexDisk(token)
    # создание папки images на Яндекс.Диск
    folder = uploader.create_folder()
    # сохранение фото на Яндекс.Диск
    res = uploader.uploading_photos(links)
