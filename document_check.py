import collections
import re

test = collections.namedtuple('Regular', ['regular', 'desc','repaire_func'])
# 中文与（数字或英文）之间没有加空格，错误
repaire_func1 = lambda w: w.groupdict()['chi1'] + ' ' + w.groupdict()['english'] + ' ' + w.groupdict()['chi2']
RE_EG1 = test(re.compile(r'(?P<chi1>[^\x00-\xff]+?)(?P<english>[a-zA-Z0-9|_]+)(?P<chi2>[^\x00-\xff])'),'中文与（数字或英文）之间没有加空格，错误',repaire_func1)

# 数字与英文单位之间没有加空格，错误
repaire_func2 = lambda w: w.groupdict()['num'] + ' ' + w.groupdict()['english']
RE_EG2 = test(re.compile(r'(?P<num>[0-9]+?)(?P<english>[a-zA-Z]+)'),'数字与英文单位之间没有加空格，错误',repaire_func2)

# 中文后跟英文标点，错误
def repaire_func5(w):
    if w.groupdict()['point'] == ',':
        return w.groupdict()['chi1'] + '，'
    elif w.groupdict()['point'] == '!':
        return w.groupdict()['chi1'] + '！'
    elif w.groupdict()['point'] == '.':
        return w.groupdict()['chi1'] + '。'
    else:
        return w.groupdict()['chi1'] + w.groupdict()['point']

RE_EG5 = test(re.compile(r'(?P<chi1>[^\x00-\xff]+?)(?P<point>[,|.|!])'),'中文后跟英文标点，错误',repaire_func5)


# 英文中间跟全角标点，错误
def repaire_func6(w):
    if w.groupdict()['point'] == '，':
        return w.groupdict()['english1'] + ',' + w.groupdict()['english2']
    elif w.groupdict()['point'] == '！':
        return w.groupdict()['english1'] + '!'+ w.groupdict()['english2']
    elif w.groupdict()['point'] == '。':
        return w.groupdict()['english1'] + '.'+ w.groupdict()['english2']
    else:
        return w.groupdict()['english1'] + w.groupdict()['point'] + w.groupdict()['english2']

RE_EG6 = test(re.compile(r'(?P<english1>[a-zA-Z]+?)(?P<point>[，|。|！])(?P<span>[\s]*?)(?P<english2>[a-zA-Z]+?)'),'英文中间跟全角标点，错误',repaire_func6)

re_list = [globals()[name] for name in globals()
           if name.startswith('RE_')]

def check(file):
    '''file:文件的路径'''
    with open(file, encoding='utf-8') as fp:
        for line_no,line in enumerate(fp, 1):
            # print(line)
            for RE in re_list:
                for match in RE.regular.finditer(line):
                    word = match.groupdict()
                    print(RE.desc,": 第" + str(line_no) +"行:",line)
                    print(word)
                    repaired_line = RE.regular.sub(RE.repaire_func,line)
                    print("repaired_line:",repaired_line)

check('text.txt')

