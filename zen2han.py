#!/usr/bin/env python
# -*- coding: utf-8 -*-

FULLWIDTH = (
    '　！”＃＄％＆’（）＊＋，\uff0d\u2212．／０１２３４５６７８９：；＜＝＞？'
    '＠ＡＢＣＤＥＦＧＨＩＪＫＬＭＮＯＰＱＲＳＴＵＶＷＸＹＺ［＼］＾＿'
    '‘ａｂｃｄｅｆｇｈｉｊｋｌｍｎｏｐｑｒｓｔｕｖｗｘｙｚ｛｜｝'
)
HALFWIDTH = (
    ' !\"#$%&\'()*+,--./0123456789:;<=>?'
    '@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_'
    '`abcdefghijklmnopqrstuvwxyz{|}'
)
Z2HMAP = dict( (ord(zc), ord(hc)) for (zc,hc) in zip(FULLWIDTH, HALFWIDTH) )

def zen2han(s):
  return s.translate(Z2HMAP)

assert zen2han('Ｈｉｙa！1') == 'Hiya!1'
