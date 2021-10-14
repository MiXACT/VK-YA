import requests
import json
import time
from tqdm import tqdm


vk_token = '958eb5d439726565e9333aa30e50e0f937ee432e927f0dbd541c541887d919a7c56f95c04217915c32008'


def get_pics_from_vk(num=5):
    for i in tqdm(range(num)):
        uploader.upload(max_pics[i]['url'], max_pics[i]['file_name'])
        time.sleep(0.5)
    return f'Фотографии из ВК скачаны в Яндекс.Диск'


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
        f_names = []
        pics = []
        albums = data['response']['items']

        while i < len(albums):
            pics.append({})
            tmp_height = albums[i]['sizes'][0]['height']
            for size in range(len(albums[i]['sizes'])):
                if albums[i]['sizes'][size]['height'] > tmp_height:
                    tmp_height = albums[i]['sizes'][size]['height']
                    pics[i]['size'] = '{}x{}'.format(albums[i]['sizes'][size]['height'],
                                                     albums[i]['sizes'][size]['width'])
                    pics[i]['url'] = albums[i]['sizes'][size]['url']
            pics[i]['file_name'] = f"{albums[i]['likes']['count']}"
            if pics[i]['file_name'] in f_names:
                pics[i]['file_name'] += time.strftime("_%D_%H-%M", time.localtime(albums[i]['date'])).replace('/', '.')
            else:
                f_names.append(pics[i]['file_name'])
            i += 1
        return pics

    def json_dumping(self, data_in):
        with open('output.json', 'w') as f:
            json.dump(data_in, f, indent=4)


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
    ya_token = input('Введите TOKEN для авторизации в Яндекс.Диске: ')

    vk_pics = VKpics(vk_token)
    uploader = YaUploader(ya_token)

    pics_list = vk_pics.get_pics_by_id(int(vk_id))  # 552934290
    max_pics = vk_pics.max_size_pic(pics_list)
    vk_pics.json_dumping(max_pics)

    uploader.make_dir()

    print(get_pics_from_vk())