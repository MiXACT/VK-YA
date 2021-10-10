import requests
import json

from pprint import pprint

vk_token = '958eb5d439726565e9333aa30e50e0f937ee432e927f0dbd541c541887d919a7c56f95c04217915c32008'
ya_token = ''


class VKpics:
    def __init__(self, token: str):
        self.token = token

    def get_pics_by_id(self, id):
        vk_url = 'https://api.vk.com/method/photos.get'
        params = {
            'owner_id': id,
            'access_token': self.token,
            'v': '5.131',
            'album_id': 'profile',
            'extended': '1',
            'photo_sizes': '1'
        }
        return requests.get(vk_url, params=params).json()

    def max_size_pic(self, data):
        """Метод принимает на вход json объект стриницы ВКонтакте
        и возвращает информацию о фотографиях в виде списка словарей с ключами 'file_name', 'size', 'url'"""
        i = 0
        pics = []
        albums = data['response']['items']
        for n in range(len(albums)):
            pics.append({'file_name': '', 'size': '', 'url': ''})

        while i < len(albums):
            tmp_height = albums[i]['sizes'][0]['height']
            for size in range(len(albums[i]['sizes'])):
                if albums[i]['sizes'][size]['height'] > tmp_height:
                    tmp_height = albums[i]['sizes'][size]['height']
                    pics[i]['file_name'] = '{}.jpg'.format(albums[i]['likes']['count'])
                    pics[i]['size'] = '{}x{}'.format(albums[i]['sizes'][size]['height'],
                                                     albums[i]['sizes'][size]['width'])
                    pics[i]['url'] = albums[i]['sizes'][size]['url']
            i += 1
        return pics

    def json_dumping(self, data_in):
        with open('output.json', 'w') as f:
            json.dump(data_in, f)

        # with open('output.json') as f:
        #     data_out = json.load(f)
        #     pprint(data_out)

class YaUploader:
    def __init__(self, token: str):
        self.token = token

    def get_headers(self):
        return {
            'Content-Type': 'application/json',
            'Authorization': f'OAuth {self.token}'
        }

    def make_dir(self):
        """Метод создаёт директорию VK в Яндекс диске"""
        ya_url = 'https://cloud-api.yandex.net/v1/disk/resources'
        headers = self.get_headers()
        requests.put(url=ya_url, params={'path': 'VK'}, headers=headers)

    def upload(self, file_path: str, fname):
        """Метод загружает файлы c именами fname из Интернет по ссылкам из file_path
        в директорию VK Яндекс диска"""
        ya_url = 'https://cloud-api.yandex.net/v1/disk/resources/upload'
        headers = self.get_headers()
        params = {'url': file_path, 'path': f'VK/{fname}'}
        requests.post(url=ya_url, params=params, headers=headers)


if __name__ == '__main__':
    vk_id = input('Введите ID пользователя ВКонтакте (числовое значение): ')
    vk_pics = VKpics(vk_token)
    pics_list = vk_pics.get_pics_by_id(int(vk_id))    # 552934290
    max_pics = vk_pics.max_size_pic(pics_list)
    vk_pics.json_dumping(max_pics)

    uploader = YaUploader(ya_token)
    uploader.make_dir()

    for i in range(len(max_pics)):
        uploader.upload(max_pics[i]['url'], max_pics[i]['file_name'])