"""Python API for viewing plex activity."""
import xml.etree.cElementTree as ET
import requests

def get_auth_token(plex_user, plex_password):
    """Get Plex authorization token."""
    auth_url = 'https://my.plexapp.com/users/sign_in.xml'
    auth_params = {'user[login]': plex_user,
                   'user[password]': plex_password}

    headers = {
        'X-Plex-Product': 'Plex API',
        'X-Plex-Version': "2.0",
        'X-Plex-Client-Identifier': '012286'
    }

    response = requests.post(auth_url, data=auth_params, headers=headers)
    auth_tree = ET.fromstring(response.text)
    for auth_elem in auth_tree.getiterator():
        if auth_elem.tag == 'authentication-token':
            return auth_elem.text.strip()

def get_now_playing(auth_token, plex_user, plex_host, plex_port=32400):
    """Get currently watched items."""
    url = 'http://' + plex_host + ':' + str(plex_port) + '/status/sessions'
    plex_response = requests.post(url + '?X-Plex-Token=' + auth_token)
    tree = ET.fromstring(plex_response.text)

    data = {}
    data['movie_title'] = []
    data['movie_year'] = []
    data['user_list'] = []
    data['user_state'] = []

    for elem in tree.getiterator('MediaContainer'):
        for video_elem in elem.iter('Video'):
            if video_elem.attrib['type'] == 'episode':
                data['movie_title'].append(video_elem.attrib['grandparentTitle'] +
                                   ' - ' + video_elem.attrib['title'])
            else:
                data['movie_title'].append(video_elem.attrib['title'])
            data['movie_year'].append(video_elem.attrib['year'])
            for user_elem in video_elem.iter('User'):
                data['user_list'].append(user_elem.attrib['title'])
            for state_elem in video_elem.iter('Player'):
                data['user_state'].append(state_elem.attrib['state'])
    return data
