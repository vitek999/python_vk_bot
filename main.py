import requests
import json
import urllib.parse
import bot_config

def getMessages():
	response = requests.get('http://{}?act=a_check&key={}&ts={}&wait=25&mode=1'.format(server, key, ts))
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
		answerOn(b)
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

def answerOn(msg):
	def answer(answer):
		answer = urllib.parse.quote(answer, safe='~()*!.\'')
		if 'cid' in msg:
			print('answering in chat:', answer)
			response = requests.get('https://api.vk.com/method/messages.send?chat_id={}&message={}&access_token={}'.format(msg['cid'], answer, bot_config.vk_token))
		else:
			print('answering to user:', answer)
			response = requests.get('https://api.vk.com/method/messages.send?user_id={}&message={}&access_token={}'.format(msg['uid'], answer, bot_config.vk_token))
	getAnswer(msg['msg'], answer)

def getAnswer(msg, answer):
	if msg == 'test':
		answer('test succes!')

getLongPollServer()
