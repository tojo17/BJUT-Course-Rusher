# coding=utf-8
import requests
import re
import sys
import userinfo
import course

timeout = 1
base_url = 'gdjwgl.bjut.edu.cn'


def retry_post(retry, session, h_url, **kwargs):
    ctTry = 0
    while 1:
        try:
            res = session.post(h_url, **kwargs)
        except:
            if ctTry < retry:
                ctTry += 1
                print('Error: Retrying...', ctTry)
                sys.stdout.flush()
            else:
                print("Failed to get page. Exiting.")
                sys.exit()
        else:
            break
    return res


def retry_get(retry, session, h_url, **kwargs):
    ctTry = 0
    while 1:
        try:
            res = session.get(h_url, **kwargs)
        except:
            if ctTry < retry:
                ctTry += 1
                print('Error: Retrying...', ctTry)
                sys.stdout.flush()
            else:
                print("Failed to get page. Exiting.")
                sys.exit()
        else:
            break
    return res


def login(username, password):
    session = requests.Session()
    h_url = 'http://' + base_url + '/default_vsso.aspx'
    h_head = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    h_data = {
        'TextBox1': username,
        'TextBox2': password,
        'RadioButtonList1_2': '学生'.encode('gb2312'),
        'Button1': ''
    }
    res = retry_post(30, session, h_url, data=h_data, headers=h_head, timeout=timeout, allow_redirects=False)

    if res.headers["Location"] == '/xs_main.aspx?xh=' + username:
        print("Login success.")
    else:
        print("Login failed, check password.")
        sys.exit()
    return session


def get_name(session, username):
    h_url = 'http://' + base_url + '/xs_main.aspx?xh=' + username
    r = retry_get(30, session, h_url)
    p = re.compile(r'<span id="xhxm">.+?</span></em>')
    rp = p.findall(r.text)
    return rp[0][16:-14]


def get_viewstate(session, username, name):
    h_url = 'http://' + base_url + '/xf_xsqxxxk.aspx'
    h_params = {
        'xh': username,
        'xm': name.encode('gb18030'),
        'gnmkdm': 'N121101'
    }
    r = retry_get(30, session, h_url, params=h_params)
    p = re.compile(r'<input type=\"hidden\" name=\"__VIEWSTATE\" value=\".+?\" />')
    rp = p.findall(r.text)
    return rp[0][47:-4]


def sel_course(session, course_name, course_number, viewstate, username, name):
    h_url = 'http://' + base_url + '/xf_xsqxxxk.aspx'
    h_params = {
        'xh': username,
        'xm': name.encode('gb18030'),
        'gnmkdm': 'N121101'
    }
    h_head = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    # refresh viewstate
    h_data = {
        '__EVENTTARGET': '',
        '__EVENTARGUMENT': '',
        '__VIEWSTATE': viewstate,
        'ddl_kcxz': '',
        'ddl_ywyl': '',
        'ddl_kcgs': '',
        'ddl_xqbs': '1',
        'ddl_sksj': '',
        'TextBox1': course_name.encode('gb2312'),
        'Button2': '确定'.encode('gb2312'),
        'dpkcmcGrid:txtChoosePage': '1',
        'dpkcmcGrid:txtPageSize': '200',
    }
    r = retry_post(3, session, h_url, params=h_params, data=h_data, headers=h_head)
    p = re.compile(r'<input type=\"hidden\" name=\"__VIEWSTATE\" value=\".+?\" />')
    rp = p.findall(r.text)
    viewstate = rp[0][47:-4]
    # get course
    h_data = {
        '__EVENTTARGET': '',
        '__EVENTARGUMENT': '',
        '__VIEWSTATE': viewstate,
        'ddl_kcxz': '',
        'ddl_ywyl': '',
        'ddl_kcgs': '',
        'ddl_xqbs': '1',
        'ddl_sksj': '',
        'TextBox1': course_name.encode('gb2312'),
        'Button1': '  提交  '.encode('gb2312'),
        'dpkcmcGrid:txtChoosePage': '1',
        'dpkcmcGrid:txtPageSize': '200',
        'kcmcGrid:_ctl' + str(course_number + 1) + ':xk': 'on'
    }
    r = retry_post(3, s, h_url, params=h_params, data=h_data, headers=h_head)
    p = re.compile(r"<script language=\'javascript\'>alert\(\'.+?\'\);</script>")
    rp = p.findall(r.text)
    if len(rp):
        return 'Failed, ' + rp[0][37:-12]
    else:
        return 'Successfully selected!'


if __name__ == '__main__':
    s = login(userinfo.usr, userinfo.pwd)
    name = get_name(s, userinfo.usr)
    try:
    	print(userinfo.usr, name)
    except:
    	# if name contains chars beyond gbk, just won't display
    	print(userinfo.usr, name.encode('utf-8'))
    sys.stdout.flush()
    viewstate = get_viewstate(s, userinfo.usr, name)
    todo_course = course.course
    count = 0
    while 1:
        count += 1
        print('-------------Loop', count)
        for cur_course in todo_course:
            print('Trying to get', cur_course[0], cur_course[1])
            result = sel_course(s, cur_course[0], cur_course[1], viewstate, userinfo.usr, name)
            print(result)
            if result == 'Successfully selected!':
                todo_course.remove(cur_course)
