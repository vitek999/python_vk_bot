import requests
import json
import bot_config

def getMessages():
	response = requests.get('http://{}?act=a_check&key={}&ts={}&wait=25&mode=1'.format(server, key, ts))
	#print(response.json())
	res = response.json()
	try:
		b = {'mid': res['updates'][0][1], 'msg': res['updates'][0][6]}
		if 2E9 < res['updates'][0][3]:
		 	b.update({'cid': int(res['updates'][0][3] - 2E9)})
		else:
		 	b.update({'uid': res['updates'][0][3]})
		print(b)
		global ts
		ts = res['ts']
	except IndexError:
		print('ParsingError')
	finally:
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
	print(ts)
	getMessages()




getLongPollServer()
