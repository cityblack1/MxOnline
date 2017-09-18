# _*_ coding: utf-8 _*_
# __author__ = 'syss'
# __date__ = '2017/5/31 0031 下午 2:19'
import re


FILENAME = 'usercenter-message.html'
FILENAME2 = 'usercenter-message.html'
with open(FILENAME, 'r') as f:
    html = f.read()
    pattern = re.compile('"../.*?"')
    strs = re.findall(pattern, html)
    for str1 in strs:
        str3 = re.sub('\.\./', '', str1)
        str2 = '\"{' + '% static {0}'.format(str3) + ' %}\"'
        str2 = re.sub('"', '\'', str2)
        html = re.sub(str1, str2, html)
with open(FILENAME2, 'w') as f:
    f.write(html)

