#!/usr/bin/env python
# -*- coding: utf-8 -*-

HIRA2KATA = dict( (c, c+96) for c in range(0x3041,0x3094) )

def hira2kata(s):
    return s.translate(HIRA2KATA)

assert hira2kata('あぎょーasdf3') == 'アギョーasdf3'
