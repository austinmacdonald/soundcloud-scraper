import urllib, json, sys
from collections import Counter
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

def search(s):
    url = 'https://api-v2.soundcloud.com/search/tracks?q=' + s + '&sc_a_id=fec216c5-0208-441b-a0be-487832503519&facet=genre&user_id=788052-567696-631234-153501&client_id=2t9loNQH90kzJcsFCODdigxfp325aq4z&limit=10&offset=0&linked_partitioning=1&app_version=1491553644'
    response = urllib.urlopen(url)
    data = json.loads(response.read())
    search_ids = data['collection'][:5]
    songs = []
    for i in range(5):
        if i >= len(search_ids):
            break
        songs.append({
            'Title': search_ids[i]['title'].encode('utf-8'),
            'User': search_ids[i]['user']['username'].encode('utf-8'),
            'Plays': str(search_ids[i]['playback_count']),
            'ID': search_ids[i]['id']}
        )
    return songs


def get_songs(track_id):
    track_ids = []
    playlist_counter = 0
    for offset in [0, 20, 40, 60, 80, 100, 120, 140, 160, 180]:
        url = 'https://api-v2.soundcloud.com/tracks/' + str(track_id) + '/playlists_without_albums?offset=' + str(
            offset) + '&limit=20&client_id=2t9loNQH90kzJcsFCODdigxfp325aq4z&app_version=1491553644'
        response = urllib.urlopen(url)
        data = json.loads(response.read())
        if 'collection' not in data:
            continue
        for playlist in data['collection']:
            playlist_counter += 1
            for track in playlist['tracks']:
                track_ids.append(track['id'])
        yield str(offset / 2)
    # percent = str(offset / 2) + '%'
    # sys.stdout.write('%s\r' % percent)
    # sys.stdout.flush()
    track_ids_counter = Counter(track_ids)
    track_ids_list = sorted(track_ids_counter, key=track_ids_counter.get, reverse=True)
    # print("Playlists found: " + str(playlistCounter))
    songs = []
    for i in range(1, 11):
        url = 'http://api.soundcloud.com/tracks/' + str(
            track_ids_list[i]) + '.json?client_id=2t9loNQH90kzJcsFCODdigxfp325aq4z'
        try:
            response = urllib.urlopen(url)
            data = json.loads(response.read())
            if 'title' not in data:
                songs.append("Not found")
            else:
                songs.append({
                    'Title': data['title'].encode('utf-8'),
                    'User': data['user']['username'].encode('utf-8'),
                    'Playlists': str(track_ids_counter[track_ids_list[i]]),
                    'Plays': data['playback_count'],
                    'ID': data['id']})
        except ValueError:
            songs.append("Not found")
    yield playlist_counter, songs

