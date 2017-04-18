import unittest
import json
from Data.interface import *
from Data.accounts import *
import requests
import time
import uuid


class AccountTest(unittest.TestCase):
    def __init__(self, method_name=config['setting']['method_name'], env=config['setting']['environment'],
                 port=config['setting']['port']):
        super(AccountTest, self).__init__(method_name)
        self.env = env
        self.host = config[env]['base_url'] + ':' + str(port)
        self.url_login = self.host + config['api']['account']['login']
        self.url_logout = self.host + config['api']['account']['logout']
        self.url_oauth = self.host + config['api']['oauth']
        self.url_register = self.host + config['api']['account']['register']
        self.email = accounts[env]['customer'][0]['email']
        self.password = accounts[env]['customer'][0]['password']
        self.headers = {'content-type': "application/json"}

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def get_login_token(self, email, password):
        url = self.url_login
        payload = {'email': email, 'passphrase': password}
        headers = {'content-type': "application/json"}
        response = requests.post(url, data=json.dumps(payload), headers=headers)
        token = response.json()['token']
        return token

    def register_new_user(self):
        mobile = time.strftime('%y%m%d%H%M%S')[-11:]
        nickname = str(uuid.uuid4())[-10:]
        email = 'test.%s@gmail.com' % str(uuid.uuid4())[-8:]
        password = 'Test1234'
        url = self.url_register
        payload = {"mobile": mobile, "nickname": nickname, "email": email, "image_path": "1",
                   "birthday": "1980-01-02", "gender": "M", "passphrase": password}
        requests.post(url, data=json.dumps(payload), headers=self.headers)
        time.sleep(1)
        return {'email': email, 'password': password, 'nickname': nickname}
		
	def get_user_id_by_email(self, email):
        sql = "select id from database_name where database_table.email = '" + email + "'"
        db_helper = DbHelper(self.env)
        result = db_helper.query(sql)
        db_helper.close()
        return result[0][0]

    # =========================================
    # Test Cases
    # =========================================
    def test_register_001_new_user(self):
        # test case description
        case = 'register a new user'
        print('Case ID: %s\n Description: %s' % (unittest.TestCase.id(self), case))
        mobile = time.strftime('%y%m%d%H%M%S')[-11:]
        nickname = str(uuid.uuid4())[-10:]
        email = 'test.%s@gmail.com' % str(uuid.uuid4())[-8:]
        url = self.url_register
        payload = {"mobile": mobile, "nickname": nickname, "email": email, "image_path": "1",
                   "birthday": "1980-01-02", "gender": "M", "passphrase": "Test1234"}
        print("url: %s" % url)
        print("payload: %s" % payload)
        response = requests.post(url, data=json.dumps(payload), headers=self.headers)
        time.sleep(1)
        print("response: status_code is %s , %s\n" % (response.status_code, response.text))
        data = response.json()
        self.assertEqual(200, response.status_code, 'Expected response code = 200. Actual = %s.' % response.status_code)
        self.assertEqual('register ok', data['Msg'],
                         'Expected response: Msg = register ok. Actual = %s.' % data['Msg'])

    def test_register_002_existed_name(self):
        # test case description
        case = 'register a new user using a existed nickname'
        print('Case ID: %s\n Description: %s' % (unittest.TestCase.id(self), case))
        # register a new user and get the new user's nickname
        return_data = self.register_new_user()
        nickname = return_data['nickname']
        # register a new user with the newly created user's nickname
        email = 'test.%s@gmail.com' % str(uuid.uuid4())[-8:]
        mobile = time.strftime('%y%m%d%H%M%S')[-11:]
        payload = {"mobile": mobile, "nickname": nickname, "email": email, "image_path": "1",
                   "birthday": "1980-01-02", "gender": "M", "passphrase": 'Test1234'}
        url = self.url_register
        rp = requests.post(url, data=json.dumps(payload), headers=self.headers)
        time.sleep(1)
        print("response: status_code is %s , %s\n" % (rp.status_code, rp.text))
        data = rp.json()
        self.assertEqual(400, rp.status_code,
                         'Expected response code = 400. Actual = %s.' % rp.status_code)
        self.assertEqual('30004', data['errorCode'],
                         'Expected response: errorCode = 30004. Actual = %s.' % data['errorCode'])
        self.assertEqual('User nickname already exist', data['errorMsg'],
                         'Expected response: errorMsg = User nickname already exist. Actual = %s.' % data['errorMsg'])