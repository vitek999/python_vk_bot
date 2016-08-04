import requests
import json
import bot_config


def getMessages():
	response = requests.get('http://{}?act=a_check&key={}&ts={}&wait=50&mode=1'.format(server, key, ts))
	res = response.json()
	global ts
	ts = res['ts']
	result = list(filter(lambda x: 4 == x[0], res['updates']))
	for a in result:
		b = {'mid': a[1], 'msg': a[6]}
		if a[3] > 2E9:
		 	b.update({'cid': int(a[3] - 2E9)})
		else:
			b.update({'uid': a[3]})
		print(b)
	getMessages()



def getLongPollServer():
	response = requests.get('https://api.vk.com/method/messages.getLongPollServer?access_token=' + bot_config.vk_token)
	parsed_string = response.json()
	global key
	global server
	global ts
	key = parsed_string['response']['key']
	server = parsed_string['response']['server']
	ts = parsed_string['response']['ts']
	getMessages()




getLongPollServer()
