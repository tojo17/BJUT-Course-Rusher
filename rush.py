# coding=utf-8
import requests
import userinfo

# Normally we wait for the server to response, which is halal.
# In rush hours the server doesn't response, we fuck it anyway,
# with out waiting for responses, which is not halal.
# Allahu akbar! Fuck Zheng Fang Soft!
halal=True
# login must be halal
login_timeout=2
# base server is normally 'gdjwgl.bjut.edu.cn' which depends on DNS server
# sometimes you can replace it with ip address for a specific server
base_server='gdjwgl.bjut.edu.cn'
# base_server = '172.21.96.63'
# base_server = '172.21.96.64'

def login(session):
    h_url = 'http://' + base_server + '/default4.aspx'
    h_head = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    h_data = '__VIEWSTATE=dDwxMTE4MjQwNDc1Ozs%2BkCoSUKMXG5ZXBP2D2Ow9ni8sipk%3D&TextBox1=' \
             + userinfo.usr + '&TextBox2=' \
             + userinfo.pwd + '&RadioButtonList1=%D1%A7%C9%FA&Button1=+%B5%C7+%C2%BC+'

    str_success = '<html><head><title>Object moved</title></head><body>'

    try:
        r = session.post(h_url, data=h_data, headers=h_head, timeout=login_timeout)
    except:
        # timeout, login failed.
        return 0
    if r.text[:52] == str_success:
        return 1
    else:
        return 0
    # print(session.cookies.items())

def check_session(session):
    print('Checking session...')
    try:
        r = session.get('http://' + base_server + '/content.aspx', timeout=login_timeout)
    except:
        # timeout, ignore state
        print('Time out, ignore state.')
        return 1
    if r.status_code == 200:
        print('Session valid, continue.')
        return 1
    # if not 200 response, needs login again
    print('Session expired, login again.')
    return 0

def get_pe(session,data):
    h_url

if __name__ == '__main__':
    s = requests.Session()
    # check if session kicked out
    if not check_session(s):
        # start login
        print("Logging in as", userinfo.usr)
        ct=0
        while not login(s):
            ct = ct + 1
            print("Login failed, retrying...\t", ct)
        print("Logged in, cookies:", s.cookies.items())

    # rush for PE courses.


