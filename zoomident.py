#!/usr/bin/env python
##
##  Usage:
##    $ ./zoomident.py -i meibo.csv -i extra.txt -p10:10 report.csv
##
##  report.csv:
##    祐介 新山,,2022/01/01 12:34:56,2022/01/01 12:35:00,1,Yes
##    新山 (祐),,2022/01/01 12:34:56,2022/01/01 12:35:00,1,Yes
##    99B99999 新山祐介,,2022/01/01 12:34:56,2022/01/01 12:35:00,1,Yes
##    シンヤマユウスケ,,2022/01/01 12:34:56,2022/01/01 12:35:00,1,Yes
##    Yusuke Shinyama,,2022/01/01 12:34:56,2022/01/01 12:35:00,1,Yes
##
##  meibo.csv:
##    CS2,Dept,99B99999,新山 祐介,シンヤマ ユウスケ,,,2001/1/1,,,yusuke@example.com
##
##  extra.txt:
##    99B99999 新山 祐介 しんやま
##
import sys
import csv
from datetime import datetime, time


##  Mora
##
class Mora:

    def __init__(self, mid, zenk, hank, zenh, *rules):
        self.mid = mid
        self.zenk = zenk
        self.hank = hank
        self.zenh = zenh
        self.roff = []
        self.reng = []
        for rule in rules:
            if rule.startswith('!'):
                self.roff.append(rule[1:])
            elif rule.startswith('+'):
                self.reng.append(rule[1:])
            else:
                self.roff.append(rule)
                self.reng.append(rule)
        #assert self.roff, rules
        #assert self.reng, rules
        return

    def __repr__(self):
        return '<%s>' % self.mid

    def __str__(self):
        return self.zenk


##  Mora Table
##
class MoraTable:

    @classmethod
    def get(klass, k):
        return klass.KEY2MORA.get(k, k)

    MORA_NN = Mora(
        '.n', 'ン', '\uff9d', 'ん', "n'", '+n',
        'n:k', 'n:s', 'n:t', 'n:c', 'n:h', 'n:m', 'n:r', 'n:w',
        'n:g', 'n:z', 'n:d', 'n:j', 'n:b', 'n:f', 'n:p', 'm:p',
        'n:q', 'n:v', 'n:x', 'n:l')

    ALL = (
        # (symbol, zenkaku_kana, hankaku_kana, zenkaku_hira, output, input)
        MORA_NN,

        Mora('.a', 'ア', '\uff71', 'あ', 'a'),
        Mora('.i', 'イ', '\uff72', 'い', 'i', '+y'),
        Mora('.u', 'ウ', '\uff73', 'う', 'u', 'wu', '+w'),
        Mora('.e', 'エ', '\uff74', 'え', 'e'),
        Mora('.o', 'オ', '\uff75', 'お', 'o'),

        Mora('ka', 'カ', '\uff76', 'か', 'ka', '+ca'),
        Mora('ki', 'キ', '\uff77', 'き', 'ki', '+ky'),
        Mora('ku', 'ク', '\uff78', 'く', 'ku', '+k', '+c', '+q'),
        Mora('ke', 'ケ', '\uff79', 'け', 'ke'),
        Mora('ko', 'コ', '\uff7a', 'こ', 'ko'),

        Mora('sa', 'サ', '\uff7b', 'さ', 'sa'),
        Mora('si', 'シ', '\uff7c', 'し', '!si', 'shi', '+si', '+sy'),
        Mora('su', 'ス', '\uff7d', 'す', 'su', '+s'),
        Mora('se', 'セ', '\uff7e', 'せ', 'se'),
        Mora('so', 'ソ', '\uff7f', 'そ', 'so'),

        Mora('ta', 'タ', '\uff80', 'た', 'ta'),
        Mora('ti', 'チ', '\uff81', 'ち', '!ti', 'chi', 'ci', '+ch'),
        Mora('tu', 'ツ', '\uff82', 'つ', '!tu', 'tsu'),
        Mora('te', 'テ', '\uff83', 'て', 'te'),
        Mora('to', 'ト', '\uff84', 'と', 'to', '+t'),

        Mora('na', 'ナ', '\uff85', 'な', 'na'),
        Mora('ni', 'ニ', '\uff86', 'に', 'ni', '+ny'),
        Mora('nu', 'ヌ', '\uff87', 'ぬ', 'nu'),
        Mora('ne', 'ネ', '\uff88', 'ね', 'ne'),
        Mora('no', 'ノ', '\uff89', 'の', 'no'),

        Mora('ha', 'ハ', '\uff8a', 'は', 'ha'),
        Mora('hi', 'ヒ', '\uff8b', 'ひ', 'hi', '+hy'),
        Mora('hu', 'フ', '\uff8c', 'ふ', '!hu', 'fu', '+hu', '+f'),
        Mora('he', 'ヘ', '\uff8d', 'へ', 'he'),
        Mora('ho', 'ホ', '\uff8e', 'ほ', 'ho'),

        Mora('ma', 'マ', '\uff8f', 'ま', 'ma'),
        Mora('mi', 'ミ', '\uff90', 'み', 'mi', '+my'),
        Mora('mu', 'ム', '\uff91', 'む', 'mu', '+m'),
        Mora('me', 'メ', '\uff92', 'め', 'me'),
        Mora('mo', 'モ', '\uff93', 'も', 'mo'),

        Mora('ya', 'ヤ', '\uff94', 'や', 'ya'),
        Mora('yu', 'ユ', '\uff95', 'ゆ', 'yu'),
        Mora('ye', 'イェ', '\uff72\uff6a', 'いぇ', 'ye'),
        Mora('yo', 'ヨ', '\uff96', 'よ', 'yo'),

        Mora('ra', 'ラ', '\uff97', 'ら', 'ra', '+la'),
        Mora('ri', 'リ', '\uff98', 'り', 'ri', '+li', '+ry', '+ly'),
        Mora('ru', 'ル', '\uff99', 'る', 'ru', '+lu', '+r', '+l'),
        Mora('re', 'レ', '\uff9a', 'れ', 're', '+le'),
        Mora('ro', 'ロ', '\uff9b', 'ろ', 'ro', '+lo'),

        Mora('wa', 'ワ', '\uff9c', 'わ', 'wa'),
        Mora('wi', 'ウィ', '\uff73\uff68', 'うぃ', 'whi', '+wi', '+wy', '+why'),
        Mora('we', 'ウェ', '\uff73\uff6a', 'うぇ', 'whe', '+we'),
        Mora('wo', 'ウォ', '\uff73\uff6b', 'うぉ', 'who'),

        Mora('Wi', 'ヰ', None, 'ゐ', '!wi'),
        Mora('We', 'ヱ', None, 'ゑ', '!we'),
        Mora('Wo', 'ヲ', '\uff66', 'を', 'wo'),

        # Special moras: They don't have actual pronunciation,
        #                but we keep them for IMEs.
        Mora('xW', 'ァ', '\uff67', 'ぁ', '!xa', '!la'),
        Mora('xI', 'ィ', '\uff68', 'ぃ', '!xi', '!li'),
        Mora('xV', 'ゥ', '\uff69', 'ぅ', '!xu', '!lu'),
        Mora('xE', 'ェ', '\uff6a', 'ぇ', '!xe', '!le'),
        Mora('xR', 'ォ', '\uff6b', 'ぉ', '!xo', '!lo'),
        Mora('xA', 'ャ', '\uff6c', 'ゃ', '!xya', '!lya'),
        Mora('xU', 'ュ', '\uff6d', 'ゅ', '!xyu', '!lyu'),
        Mora('xO', 'ョ', '\uff6e', 'ょ', '!xyo', '!lyo'),

        # chouon
        Mora('x-', 'ー', '\uff70', 'ー', '!x-', '+h'),

        # choked sound (Sokuon)
        Mora('.t', 'ッ', '\uff6f', 'っ', '!xtu', '!ltu',
             'k:k', 's:s', 't:t', 'h:h', 'f:f', 'm:m', 'r:r',
             'g:g', 'z:z', 'j:j', 'd:d', 'b:b', 'v:v', 'b:c', 't:c'),

        # voiced (Dakuon)
        Mora('ga', 'ガ', '\uff76\uff9e', 'が', 'ga'),
        Mora('gi', 'ギ', '\uff77\uff9e', 'ぎ', 'gi', '+gy'),
        Mora('gu', 'グ', '\uff78\uff9e', 'ぐ', 'gu', '+g'),
        Mora('ge', 'ゲ', '\uff79\uff9e', 'げ', 'ge'),
        Mora('go', 'ゴ', '\uff7a\uff9e', 'ご', 'go'),

        Mora('za', 'ザ', '\uff7b\uff9e', 'ざ', 'za'),
        Mora('zi', 'ジ', '\uff7c\uff9e', 'じ', '!zi', 'ji', '+zi'),
        Mora('zu', 'ズ', '\uff7d\uff9e', 'ず', 'zu', '+z'),
        Mora('ze', 'ゼ', '\uff7e\uff9e', 'ぜ', 'ze'),
        Mora('zo', 'ゾ', '\uff7f\uff9e', 'ぞ', 'zo'),

        Mora('da', 'ダ', '\uff80\uff9e', 'だ', 'da'),
        Mora('di', 'ヂ', '\uff81\uff9e', 'ぢ', '!di', 'dzi'),
        Mora('du', 'ヅ', '\uff82\uff9e', 'づ', '!du', 'dzu'),
        Mora('de', 'デ', '\uff83\uff9e', 'で', 'de'),
        Mora('do', 'ド', '\uff84\uff9e', 'ど', 'do', '+d'),

        Mora('ba', 'バ', '\uff8a\uff9e', 'ば', 'ba'),
        Mora('bi', 'ビ', '\uff8b\uff9e', 'び', 'bi', '+by'),
        Mora('bu', 'ブ', '\uff8c\uff9e', 'ぶ', 'bu', '+b'),
        Mora('be', 'ベ', '\uff8d\uff9e', 'べ', 'be'),
        Mora('bo', 'ボ', '\uff8e\uff9e', 'ぼ', 'bo'),

        # p- sound (Handakuon)
        Mora('pa', 'パ', '\uff8a\uff9f', 'ぱ', 'pa'),
        Mora('pi', 'ピ', '\uff8b\uff9f', 'ぴ', 'pi', '+py'),
        Mora('pu', 'プ', '\uff8c\uff9f', 'ぷ', 'pu', '+p'),
        Mora('pe', 'ペ', '\uff8d\uff9f', 'ぺ', 'pe'),
        Mora('po', 'ポ', '\uff8e\uff9f', 'ぽ', 'po'),

        # double consonants (Youon)
        Mora('KA', 'キャ', '\uff77\uff6c', 'きゃ', 'kya'),
        Mora('KU', 'キュ', '\uff77\uff6d', 'きゅ', 'kyu', '+cu'),
        Mora('KE', 'キェ', '\uff77\uff6a', 'きぇ', 'kye'),
        Mora('KO', 'キョ', '\uff77\uff6e', 'きょ', 'kyo'),

        Mora('kA', 'クァ', '\uff78\uff67', 'くぁ', 'qa'),
        Mora('kI', 'クィ', '\uff78\uff68', 'くぃ', 'qi'),
        Mora('kE', 'クェ', '\uff78\uff6a', 'くぇ', 'qe'),
        Mora('kO', 'クォ', '\uff78\uff6b', 'くぉ', 'qo'),

        Mora('SA', 'シャ', '\uff7c\uff6c', 'しゃ', '!sya', 'sha', '+sya'),
        Mora('SU', 'シュ', '\uff7c\uff6d', 'しゅ', '!syu', 'shu', '+syu', '+sh'),
        Mora('SE', 'シェ', '\uff7c\uff6a', 'しぇ', '!sye', 'she', '+sye'),
        Mora('SO', 'ショ', '\uff7c\uff6e', 'しょ', '!syo', 'sho', '+syo'),

        Mora('CA', 'チャ', '\uff81\uff6c', 'ちゃ', '!tya', '!cya', 'cha'),
        Mora('CU', 'チュ', '\uff81\uff6d', 'ちゅ', '!tyu', '!cyu', 'chu'),
        Mora('CE', 'チェ', '\uff81\uff6a', 'ちぇ', '!tye', '!cye', 'che'),
        Mora('CO', 'チョ', '\uff81\uff6e', 'ちょ', '!tyo', '!cyo', 'cho'),
        Mora('TI', 'ティ', '\uff83\uff68', 'てぃ', '!tyi', '+ti'),
        Mora('TU', 'テュ', '\uff83\uff6d', 'てゅ', '!thu', '+tu'),
        Mora('TO', 'トゥ', '\uff84\uff69', 'とぅ', '!tho', '+two'),

        Mora('NA', 'ニャ', '\uff86\uff6c', 'にゃ', 'nya'),
        Mora('NU', 'ニュ', '\uff86\uff6d', 'にゅ', 'nyu'),
        Mora('NI', 'ニェ', '\uff86\uff6a', 'にぇ', 'nye'),
        Mora('NO', 'ニョ', '\uff86\uff6e', 'にょ', 'nyo'),

        Mora('HA', 'ヒャ', '\uff8b\uff6c', 'ひゃ', 'hya'),
        Mora('HU', 'ヒュ', '\uff8b\uff6d', 'ひゅ', 'hyu'),
        Mora('HE', 'ヒェ', '\uff8b\uff6a', 'ひぇ', 'hye'),
        Mora('HO', 'ヒョ', '\uff8b\uff6e', 'ひょ', 'hyo'),

        Mora('FA', 'ファ', '\uff8c\uff67', 'ふぁ', 'fa'),
        Mora('FI', 'フィ', '\uff8c\uff68', 'ふぃ', 'fi', '+fy'),
        Mora('FE', 'フェ', '\uff8c\uff6a', 'ふぇ', 'fe'),
        Mora('FO', 'フォ', '\uff8c\uff6b', 'ふぉ', 'fo'),
        Mora('FU', 'フュ', '\uff8c\uff6d', 'ふゅ', 'fyu'),
        Mora('Fo', 'フョ', '\uff8c\uff6e', 'ふょ', 'fyo'),

        Mora('MA', 'ミャ', '\uff90\uff6c', 'みゃ', 'mya'),
        Mora('MU', 'ミュ', '\uff90\uff6d', 'みゅ', 'myu'),
        Mora('ME', 'ミェ', '\uff90\uff6a', 'みぇ', 'mye'),
        Mora('MO', 'ミョ', '\uff90\uff6e', 'みょ', 'myo'),

        Mora('RA', 'リャ', '\uff98\uff6c', 'りゃ', 'rya', '+lya'),
        Mora('RU', 'リュ', '\uff98\uff6d', 'りゅ', 'ryu', '+lyu'),
        Mora('RE', 'リェ', '\uff98\uff6a', 'りぇ', 'rye', '+lye'),
        Mora('RO', 'リョ', '\uff98\uff6e', 'りょ', 'ryo', '+lyo'),

        # double consonants + voiced
        Mora('GA', 'ギャ', '\uff77\uff9e\uff6c', 'ぎゃ', 'gya'),
        Mora('GU', 'ギュ', '\uff77\uff9e\uff6d', 'ぎゅ', 'gyu'),
        Mora('GE', 'ギェ', '\uff77\uff9e\uff6a', 'ぎぇ', 'gye'),
        Mora('GO', 'ギョ', '\uff77\uff9e\uff6e', 'ぎょ', 'gyo'),

        Mora('Ja', 'ジャ', '\uff7c\uff9e\uff6c', 'じゃ', 'ja', 'zya'),
        Mora('Ju', 'ジュ', '\uff7c\uff9e\uff6d', 'じゅ', 'ju', 'zyu'),
        Mora('Je', 'ジェ', '\uff7c\uff9e\uff6a', 'じぇ', 'je', 'zye'),
        Mora('Jo', 'ジョ', '\uff7c\uff9e\uff6e', 'じょ', 'jo', 'zyo'),

        Mora('JA', 'ヂャ', '\uff81\uff9e\uff6c', 'ぢゃ', 'zha'),
        Mora('JU', 'ヂュ', '\uff81\uff9e\uff6d', 'ぢゅ', 'zhu'),
        Mora('JE', 'ヂェ', '\uff81\uff9e\uff6a', 'ぢぇ', 'zhe'),
        Mora('JO', 'ヂョ', '\uff81\uff9e\uff6e', 'ぢょ', 'zho'),

        Mora('dI', 'ディ', '\uff83\uff9e\uff68', 'でぃ', '+di', 'dyi'),
        Mora('dU', 'デュ', '\uff83\uff9e\uff6d', 'でゅ', '+du', 'dyu', 'dhu'),
        Mora('dO', 'ドゥ', '\uff84\uff9e\uff69', 'どぅ', 'dho'),

        Mora('BA', 'ビャ', '\uff8b\uff9e\uff6c', 'びゃ', 'bya'),
        Mora('BU', 'ビュ', '\uff8b\uff9e\uff6d', 'びゅ', 'byu'),
        Mora('BE', 'ビェ', '\uff8b\uff9e\uff6a', 'びぇ', 'bye'),
        Mora('BO', 'ビョ', '\uff8b\uff9e\uff6e', 'びょ', 'byo'),

        Mora('va', 'ヴァ', '\uff73\uff9e\uff67', 'う゛ぁ', 'va'),
        Mora('vi', 'ヴィ', '\uff73\uff9e\uff68', 'う゛ぃ', 'vi', '+vy'),
        Mora('vu', 'ヴ',   '\uff73\uff9e',       'う゛', 'vu', '+v'),
        Mora('ve', 'ヴェ', '\uff73\uff9e\uff6a', 'う゛ぇ', 've'),
        Mora('vo', 'ヴォ', '\uff73\uff9e\uff6b', 'う゛ぉ', 'vo'),

        # double consonants + p-sound
        Mora('PA', 'ピャ', '\uff8b\uff9f\uff6c', 'ぴゃ', 'pya'),
        Mora('PU', 'ピュ', '\uff8b\uff9f\uff6d', 'ぴゅ', 'pyu'),
        Mora('PE', 'ピェ', '\uff8b\uff9f\uff6a', 'ぴぇ', 'pye'),
        Mora('PO', 'ピョ', '\uff8b\uff9f\uff6e', 'ぴょ', 'pyo'),
    )

    KEY2MORA = { m.mid:m for m in ALL }


##  Mora Parser
##
class MoraParser:

    def __init__(self):
        self._tree = {}
        for m in MoraTable.ALL:
            for k in (m.zenk, m.hank, m.zenh):
                if k is None: continue
                self.add(k, m, allowConflict=True)
        return

    def add(self, s, m, allowConflict=False):
        #print('add:', s, m)
        t0 = self._tree
        (s0,_,s1) = s.partition(':')
        for c in (s0+s1)[:-1]:
            if c in t0:
                (_,_,t1) = t0[c]
            else:
                t1 = {}
                t0[c] = (None, None, t1)
            t0 = t1
        c = (s0+s1)[-1]
        if c in t0:
            (obj,_,t1) = t0[c]
            if obj is not None and not allowConflict:
                raise ValueError('already defined: %r' % s)
        else:
            t1 = {}
        t0[c] = (m, s0, t1)
        return

    def parse(self, s, i0=0):
        i1 = i0
        t0 = self._tree
        m = s0 = None
        while i1 < len(s):
            c = s[i1].lower()
            if c in t0:
                (m,s0,t1) = t0[c]
                i1 += 1
                t0 = t1
            elif m is not None:
                yield (s[i0:i1], m)
                i0 = i1 = i0+len(s0)
                t0 = self._tree
                m = s0 = None
            else:
                yield (s[i1], None)
                i0 = i1 = i1+1
                t0 = self._tree
        if m is not None:
            yield (s[i0:], m)
        return

class MoraParserOfficial(MoraParser):

    def __init__(self):
        MoraParser.__init__(self)
        for m in MoraTable.ALL:
            for k in m.roff:
                self.add(k, m)
        self.add('nn', MoraTable.MORA_NN)
        return

class MoraParserOfficialAnna(MoraParser):

    def __init__(self):
        MoraParser.__init__(self)
        for m in MoraTable.ALL:
            for k in m.roff:
                self.add(k, m)
        self.add('n', MoraTable.MORA_NN)
        return

class MoraParserEnglish(MoraParser):

    def __init__(self):
        MoraParser.__init__(self)
        for m in MoraTable.ALL:
            for k in m.reng:
                self.add(k, m)
        return


##  String Generator
##
class StringGenerator:

    def generate(self, seq):
        s = ''
        m1 = None
        for m2 in seq:
            if m1 is None:
                pass
            elif isinstance(m1, Mora):
                s += self.convert(m1, m2)
            else:
                s += m1
            m1 = m2
        if m1 is None:
            pass
        elif isinstance(m1, Mora):
            s += self.convert(m1, None)
        else:
            s += m1
        return s

    def convert(self, m1, m2=None):
        return m1.zenk

class GeneratorOfficial(StringGenerator):

    def convert(self, m1, m2=None):
        if m1.mid == '.t':
            if isinstance(m2, Mora):
                k = m2.roff[0]
                return k[0] # double the consonant
            return 't'
        elif m1.mid == '.n':
            if not isinstance(m2, Mora) or m2.mid[0] not in '.ynN':
                return 'n'  # NN+C -> "n"+C
        return m1.roff[0]

class GeneratorOfficialAnna(StringGenerator):

    def convert(self, m1, m2=None):
        if m1.mid == '.t':
            if isinstance(m2, Mora):
                k = m2.roff[0]
                return k[0] # double the consonant
            return 't'
        elif m1.mid == '.n':
            if not isinstance(m2, Mora) or m2.mid[0] not in '.y':
                return 'n'  # NN+C -> "n"+C
        return m1.roff[0]

class GeneratorEnglish(StringGenerator):

    def convert(self, m1, m2=None):
        if m1.mid == '.t':
            if isinstance(m2, Mora):
                k = m2.reng[0]
                if not k.startswith('c'):
                    return k[0] # double the consonant
            return 't'
        elif m1.mid == '.n':
            if isinstance(m2, Mora) and m2.mid[0] in 'pP':
                return 'm'  # NN+"p" -> "mp"
            elif not isinstance(m2, Mora) or m2.mid[0] not in '.y':
                return 'n'  # NN+C -> "n"+C
        return m1.reng[0]


PARSE_ENGLISH = MoraParserEnglish()
GEN = StringGenerator()
GEN_ENGLISH = GeneratorEnglish()

# expand(s): Expand features
def expand(s):
    words = []
    w = ''
    for c in s:
        if c.isalpha():
            w += c
        elif w:
            words.append(w)
            w = ''
    if w:
        words.append(w)
    a = []
    for w in words:
        a.append(w.lower())
        w1 = w2 = ''
        for (s,m) in PARSE_ENGLISH.parse(w):
            if m is not None:
                w1 += m.zenk
                w2 += m.reng[0].lower()
        if w1:
            a.append(w1)
        if w2:
            a.append(w2)
    for w1 in a:
        yield w1
        if "'" in w1:
            yield w1.replace("'",'')
        for w2 in a:
            if w1 != w2:
                w = w1+w2
                yield w
                if "'" in w:
                    yield w.replace("'",'')
    return

class IndexDB:

    def __init__(self):
        self.index = {}
        return

    def add(self, name, uid):
        # name -> {feats} -> uid
        feats = set(expand(name))
        for f in feats:
            self.addraw(f, uid)
        return

    def addraw(self, feat, uid):
        if feat in self.index:
            a = self.index[feat]
        else:
            a = self.index[feat] = set()
        a.add(uid)
        return

    def lookup(self, name):
        # name -> {feats} -> uid
        feats = set(expand(name))
        uids = None
        for f in feats:
            if f not in self.index: continue
            a = self.index[f]
            if uids is None:
                uids = a
            else:
                uids = uids.intersection(a)
        return uids

def main(argv):
    import getopt
    def usage():
        print('usage: %s [-i input] [-p HH:MM[-HH:MM]] [file ...]' % argv[0])
        return 100
    try:
        (opts, args) = getopt.getopt(argv[1:], 'i:p:')
    except getopt.GetoptError:
        return usage()
    db = IndexDB()
    r0 = r1 = None
    for (k, v) in opts:
        if k == '-i':
            path = v
            if path.endswith('.csv'):
                with open(path, encoding='cp932') as fp:
                    table = list(csv.reader(fp))
                    for row in table[1:]:
                        uid = row[2]
                        db.addraw(row[2], uid)
                        db.add(row[3], uid)
                        db.add(row[4], uid)
            else:
                with open(path) as fp:
                    for line in fp:
                        (line,_,_) = line.strip().partition('#')
                        if not line: continue
                        f = line.split()
                        uid = f.pop(0)
                        for w in f:
                            db.add(w, uid)
        elif k == '-p':
            (t1,_,t2) = v.partition('-')
            (h,_,m) = t1.partition(':')
            r1 = r0 = time(int(h), int(m))
            if t2:
                (h,_,m) = t2.partition(':')
                r1 = time(int(h), int(m))
            assert r0 <= r1
    for path in args:
        with open(path) as fp:
            table = list(csv.reader(fp))
        for row in table[1:]:
            name = row[0]
            dt0 = datetime.strptime(row[2], '%Y/%m/%d %H:%M:%S')
            dt1 = datetime.strptime(row[3], '%Y/%m/%d %H:%M:%S')
            t0 = dt0.time()
            t1 = dt1.time()
            if r0 is not None and (t1 < r0 or r1 < t0): continue
            uids = db.lookup(name)
            if uids is None:
                print(f'# notfound: {name}')
            elif 2 < len(uids):
                print(f'# ambiguous: {name} {uids}')
            else:
                uid = list(uids)[0]
                print(f'{uid} # {name}')
    return 0

if __name__ == '__main__': sys.exit(main(sys.argv))
