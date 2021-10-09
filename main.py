import requests

from pprint import pprint


URL = 'https://api.vk.com/method/photos.get'

vk_token = '958eb5d439726565e9333aa30e50e0f937ee432e927f0dbd541c541887d919a7c56f95c04217915c32008'

params = {
    'owner_id': 552934290,
    'access_token': vk_token,
    'v': '5.131',
    'album_id': 'profile',
    'extended': '1',
    'photo_sizes': '1'
}

if __name__ == '__main__':
    r = requests.get(URL, params=params)
    pprint(r.json())
