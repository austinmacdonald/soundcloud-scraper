import urllib, json, sys
from collections import Counter
search = raw_input("Song title and/or Artist: ")
url = 'https://api-v2.soundcloud.com/search/tracks?q=' + search + '&sc_a_id=fec216c5-0208-441b-a0be-487832503519&facet=genre&user_id=788052-567696-631234-153501&client_id=2t9loNQH90kzJcsFCODdigxfp325aq4z&limit=10&offset=0&linked_partitioning=1&app_version=1491553644'
response = urllib.urlopen(url)
data = json.loads(response.read())
searchIDs = data['collection'][:5]
for i in range(5):
	print(str(i + 1) + ") Title: " + searchIDs[i]['title'].encode('utf-8'))
	print("   User: " + searchIDs[i]['user']['username'].encode('utf-8'))
	print("   Plays: " + str(searchIDs[i]['playback_count']))
index = raw_input("Enter number: ")
trackID = searchIDs[int(index)-1]['id']
trackIDs = []
playlistCounter = 0
for offset in [0,20,40,60,80,100,120,140,160,180]:
	url = 'https://api-v2.soundcloud.com/tracks/' + str(trackID) + '/playlists_without_albums?offset=' + str(offset) + '&limit=20&client_id=2t9loNQH90kzJcsFCODdigxfp325aq4z&app_version=1491553644'
	response = urllib.urlopen(url)
	data = json.loads(response.read())
	if 'collection' not in data:
		continue
	for playlist in data['collection']:
		playlistCounter += 1
		for track in playlist['tracks']:
			trackIDs.append(track['id'])
	percent = str(offset / 2) + '%'
	sys.stdout.write('%s\r' % percent)
	sys.stdout.flush()
trackIDsCounter = Counter(trackIDs)
trackIDsList = sorted(trackIDsCounter, key=trackIDsCounter.get, reverse=True)
print("Playlists found: " + str(playlistCounter))
for i in range(1,11):
	url = 'http://api.soundcloud.com/tracks/' + str(trackIDsList[i]) + '.json?client_id=2t9loNQH90kzJcsFCODdigxfp325aq4z'
	try:
		response = urllib.urlopen(url)
		data = json.loads(response.read())
		if 'title' not in data:
			print("Not found")
		else:
			print(str(i) + ") Title: " + data['title'].encode('utf-8'))
			print("   User: " + data['user']['username'].encode('utf-8'))
			print("   Playlists: " + str(trackIDsCounter[trackIDsList[i]]))
	except ValueError:
		print("Not found")