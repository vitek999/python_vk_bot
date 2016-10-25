import requests
import urllib.parse
import bot_logger
import bot_config


def getMessages():
    while 1:
        response = requests.get('http://{}?act=a_check&key={}&ts={}&wait=25&mode=1'.format(server, key, ts))
        res = response.json()
        global ts
        ts = res['ts']
        result = list(filter(lambda x: 4 == x[0], res['updates']))
        for a in result:
            b = {'mid': a[1], 'msg': a[6]}
            if a[2]&int('0b10',2) == 2: #Ignore bot own messages
                continue;
            if a[3] > 2E9:
                b.update({'cid': int(a[3] - 2E9)})
                log_msg = '\x1b[33mChat ID:\x1b[0m {} \x1b[33mmessage ID:\x1b[0m {} \x1b[33mmessage:\x1b[0m {}'.format(
                    b['cid'], b['mid'], b['msg'])
            else:
                b.update({'uid': a[3]})
                log_msg = '\x1b[33mUser ID:\x1b[0m {} \x1b[33mmessage ID:\x1b[0m {} \x1b[33mmessage:\x1b[0m {}'.format(
                    b['mid'], b['mid'], b['msg'])
            answerOn(b)
            bot_logger.printLog('getMessages', log_msg)


def getLongPollServer():
    #TODO: Build request from object
    response = requests.get('https://api.vk.com/method/messages.getLongPollServer?access_token=' + bot_config.vk_token)
    parsed_string = response.json()
    global key
    global server
    global ts
    #TODO: Use destructors?
    key = parsed_string['response']['key']
    server = parsed_string['response']['server']
    ts = parsed_string['response']['ts']
    bot_logger.printLog('getLongPollServer', '\x1b[33mSUCCESS!!!\x1b[0m')
    getMessages()


def answerOn(msg):
    def answer(answer):
        #TODO: Refactor to universal answer function
        answer = urllib.parse.quote(answer, safe='~()*!.\'')
        if 'cid' in msg:
            bot_logger.printLog('answering in Chat', answer)
            response = requests.get(
                'https://api.vk.com/method/messages.send?chat_id={}&message={}&access_token={}'.format(msg['cid'],
                                                                                                       answer,
                                                                                                       bot_config.vk_token))
        else:
            bot_logger.printLog('answering to User', answer)
            response = requests.get(
                'https://api.vk.com/method/messages.send?user_id={}&message={}&access_token={}'.format(msg['uid'],
                                                                                                       answer,
                                                                                                       bot_config.vk_token))

    getAnswer(msg['msg'], answer)


def getAnswer(msg, answer):
    if msg == 'test':
        answer('test success!')


getLongPollServer()
