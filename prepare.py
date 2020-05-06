import datetime

#### Prepare

def read_token():
    with open('token.md','r') as f:
        return f.readlines()[0]

def get_list():
    re = {'cnt': 0, 'list': ''}

    with open('list.md','r') as f:
        f = f.readlines()
    
        re['cnt'] = len(f)
        for i in f:
            re['list'] += i
    return re

def detect_add(inp):
    re = {'order': 'n', 'content': 'test', 'day': '30/04', 'time': '11:30', 'weekly': '0', 'monthly': '0', 'before': '5', 'note': ''}
    
    tmp = []
    f_half = []

    re['order'] = str(get_list()['cnt'])

    if inp.find('-'):
        tmp = inp.split('-')
        for i in range(1, len(tmp)):
            x = tmp[i][0]
            y = tmp[i][2:].strip()

            if x == 'w' and y.isdecimal():
                re['weekly'] = y
            elif x == 'm' and y.isdecimal():
                re['monthly'] = y
            elif x == 'b' and y.isdecimal():
                re['before'] = y
            elif x == 'n':
                re['note'] = y

    tmp = inp.split('-')[0].split(' ')

    if len(tmp) < 3:
        return re

    re['content'] = tmp[0]
    re['day'] = tmp[1].split('/')[0].zfill(2) + '/' + tmp[1].split('/')[1].zfill(2)
    re['time'] = tmp[2].split(':')[0].zfill(2) + ':' + tmp[2].split(':')[1].zfill(2)

    return re

def add_list(arg):
    s = '{ '
    for key, val in arg.items():
        s += key + ': ' + val + ', '
    s = s[:-2] + ' }\n'

    with open('list.md','a') as f:
        f.write(s)

def del_list(order):
    f = []
    f = open('list.md','r').readlines()
    f.pop(order)

    fo = open('list.md','w')
    for i in range(len(f)):
        tmp = f[i].split(' ')
        tmp[2] = str(i) + ','
        fo.write(' '.join(tmp))

def fix_order(inp):
    re = {'order': 'n', 'content': 'test', 'day': '30/4', 'time': '11:30', 'weekly': '0', 'monthly': '0', 'before': '5', 'note': ''}

    tmp = inp.split('-')

    if tmp[0] == '' or not tmp[0].strip().isdecimal():
        return False

    data = get_list()
    if int(tmp[0].strip()) > data['cnt'] - 1:
        return False

    mau = data['list'].split('\n')[int(tmp[0].strip())].split(' ')
    i = 2
    for key in re:
        re[key] = mau[i][:-1]
        i += 2

    for i in range(1, len(tmp)):
        x = tmp[i][0]
        y = tmp[i][2:].strip()

        if x == 'w' and y.isdecimal():
            re['weekly'] = y
        elif x == 'm' and y.isdecimal():
            re['monthly'] = y
        elif x == 'b' and y.isdecimal():
            re['before'] = y
        else:
            re['note'] = y

    s = '{ '
    for key in re:
        s += key + ': ' + re[key] + ', '
    s = s[:-2] + ' }'

    data = data['list'].split('\n')
    data[int(tmp[0].strip())] = s

    f = open('list.md','w')
    f.write('\n'.join(data))

    return True

def update_schedule(order, last, glotime):
    #{ order: 0, content: test, day: 30/04, time: 11:30, weekly: 990, monthly: 92, before: 93, note: victory }

    save = last.split(' ')
    w, m = save[10][:-1], save[12][:-1]

    if w != '0':
        save[6] = (glotime + datetime.timedelta(days = +7)).strftime("%d/%m") + ','
        save[10] = str(int(w) - 1) + ','
        last = ' '.join(save)
    elif m != '0':
        save[6] = (glotime + datetime.timedelta(months = +1)).strftime("%d/%m") + ','
        save[12] = str(int(m) - 1) + ','
        last = ' '.join(save)
    else:
        del_list(order)
        return

    data = get_list()['list'].split('\n')
    data[order] = last

    f = open('list.md','w')
    f.write('\n'.join(data))  