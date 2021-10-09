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

def max_size_pic(data, pics_num):
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
                pics[i]['size'] = '{}x{}'.format(albums[i]['sizes'][size]['height'], albums[i]['sizes'][size]['width'])
                pics[i]['url'] = albums[i]['sizes'][size]['url']
        print(pics[i])
        i += 1
    #return

if __name__ == '__main__':
    res = requests.get(URL, params=params).json()
    max_size_pic(res, 5)
    pprint(res['response']['items'])
