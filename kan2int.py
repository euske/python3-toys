#!/usr/bin/env python
# -*- coding: utf-8 -*-

KANDIGIT = {
    '〇':0, '一':1, '二':2, '三':3, '四':4,
    '五':5, '六':6, '七':7, '八':8, '九':9,
    '零':0, '壱':1, '弍':2, '弐':2, '参':3, '伍':5,
}
KANEXP1 = {
    '十':10, '拾':10, '百':100, '千':1000
}
KANEXP2 = {
    '万':1e4, '萬':1e4, '億':1e8, '兆':1e12, '京':1e16
}

def kan2int(s):
    n = d1 = d2 = 0
    for c in s:
        if c in KANDIGIT:
            d1 = d1*10+KANDIGIT[c]
        elif c in KANEXP1:
            if d1 == 0:
                d1 = 1
            d2 += d1*KANEXP1[c]
            d1 = 0
        elif c in KANEXP2:
            n += (d1+d2)*KANEXP2[c]
            d1 = d2 = 0
    return n+d1+d2

assert kan2int('十三') == 13
assert kan2int('四三') == 43
assert kan2int('四十三') == 43
assert kan2int('四百三') == 403
assert kan2int('四百三十二') == 432
assert kan2int('一万四百三十二') == 10432
assert kan2int('一万五千四百三十二') == 15432
