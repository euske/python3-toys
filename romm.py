#!/usr/bin/env python
# -*- coding: utf-8 -*-

##  romm.py - handles Roma-ji and kana.
##


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


##  Aliases
##
PARSE = MoraParser()
def parse(s): return PARSE.parse(s)

PARSE_OFFICIAL = MoraParserOfficial()
def parse_official(s): return PARSE_OFFICIAL.parse(s)

PARSE_OFFICIAL_ANNA = MoraParserOfficialAnna()
def parse_official_anna(s): return PARSE_OFFICIAL_ANNA(s)

PARSE_ENGLISH = MoraParserEnglish()
def parse_english(s): return PARSE_ENGLISH(s)

GEN = StringGenerator()
def gen(a): return GEN.generate(a)

GEN_OFFICIAL = GeneratorOfficial()
def gen_official(a): return GEN_OFFICIAL.generate(a)

GEN_OFFICIAL_ANNA = GeneratorOfficialAnna()
def gen_official_anna(a): return GEN_OFFICIAL_ANNA.generate(a)

GEN_ENGLISH = GeneratorEnglish()
def gen_english(a): return GEN_ENGLISH.generate(a)


# Test cases
if __name__ == '__main__':
    import unittest

    class TestRoma(unittest.TestCase):

        def checkParse(self, parser, s, moras0):
            moras = [ (isinstance(m,Mora) and m.mid) or c for (c,m) in parser.parse(s) ]
            self.assertEqual(moras0, moras)

        def test_00_parse_basic_official(self):
            self.checkParse(PARSE_OFFICIAL,
                            'akasatana',
                            ['.a','ka','sa','ta','na'])
        def test_01_parse_basic_official_anna(self):
            self.checkParse(PARSE_OFFICIAL_ANNA,
                            'akasatana',
                            ['.a','ka','sa','ta','na'])
        def test_02_parse_basic_english(self):
            self.checkParse(PARSE_ENGLISH,
                            'akasatana',
                            ['.a','ka','sa','ta','na'])
        def test_03_parse_official_ta1(self):
            self.checkParse(PARSE_OFFICIAL,
                            'tatituteto',
                            ['ta','ti','tu','te','to'])
            return
        def test_03_parse_official_ta2(self):
            self.checkParse(PARSE_OFFICIAL,
                            'tachitsuteto',
                            ['ta','ti','tu','te','to'])
            return
        def test_04_parse_official_nn1(self):
            self.checkParse(PARSE_OFFICIAL,
                            'sonna,anna',
                            ['so','.n','.a',',','.a','.n','.a'])
            return
        def test_04_parse_official_nn2(self):
            self.checkParse(PARSE_OFFICIAL,
                            'sonnna,annna',
                            ['so','.n','na',',','.a','.n','na'])
            return
        def test_05_parse_official_anna_nn1(self):
            self.checkParse(PARSE_OFFICIAL_ANNA,
                            'sonna,anna',
                            ['so','.n','na',',','.a','.n','na'])
            return
        def test_05_parse_official_anna_nn2(self):
            self.checkParse(PARSE_OFFICIAL_ANNA,
                            'sonnna,annna',
                            ['so','.n','.n','na',',','.a','.n','.n','na'])
            return
        def test_06_parse_official_youon(self):
            self.checkParse(PARSE_OFFICIAL,
                            'dosyaburi',
                            ['do','SA','bu','ri'])
            return
        def test_06_parse_official_sokuon1(self):
            self.checkParse(PARSE_OFFICIAL,
                            'tyotto',
                            ['CO','.t','to'])
            return
        def test_06_parse_official_sokuon2(self):
            self.checkParse(PARSE_OFFICIAL,
                            'dotchimo',
                            ['do','.t','ti','mo'])
            return
        def test_07_parse_mixed(self):
            self.checkParse(PARSE_OFFICIAL,
                            'aIＵえオ',
                            ['.a','.i','Ｕ','.e','.o'])
            return
        def test_07_parse_ignore(self):
            self.checkParse(PARSE_OFFICIAL,
                            'ai$uεo',
                            ['.a','.i','$','.u','ε','.o'])
            return

        def checkGen(self, generator, moras, s0):
            s = generator.generate( MoraTable.get(x) for x in moras )
            self.assertEqual(s0, s)
        def checkGenRaw(self, generator, moras, s0):
            s = generator.generate(moras)
            self.assertEqual(s0, s)

        def test_10_gen_basic_official(self):
            self.checkGen(GEN_OFFICIAL,
                          ['.a','ka','sa','ta','na','.n'],
                          'akasatanan')
        def test_11_gen_basic_official_anna(self):
            self.checkGen(GEN_OFFICIAL_ANNA,
                          ['.a','ka','sa','ta','na','.n'],
                          'akasatanan')
        def test_12_gen_basic_english(self):
            self.checkGen(GEN_ENGLISH,
                          ['.a','ka','sa','ta','na','.n'],
                          'akasatanan')
        def test_13_gen_official_ta(self):
            self.checkGen(GEN_OFFICIAL,
                          ['ta','ti','tu','te','to'],
                          'tatituteto')
        def test_14_gen_english_ta(self):
            self.checkGen(GEN_ENGLISH,
                          ['ta','ti','tu','te','to'],
                          'tachitsuteto')
        def test_15_gen_official_nn1(self):
            self.checkGen(GEN_OFFICIAL,
                          ['so','.n','.a',',','.a','.n','.a'],
                          "son'a,an'a")
        def test_15_gen_official_nn2(self):
            self.checkGen(GEN_OFFICIAL,
                          ['so','.n','na',',','.a','.n','na'],
                          "son'na,an'na")
        def test_16_gen_official_nn_reduce(self):
            self.checkGen(GEN_OFFICIAL_ANNA,
                          ['so','.n','ka',',','.a','.n','ka'],
                          'sonka,anka')
        def test_17_gen_official_anna_nn1(self):
            self.checkGen(GEN_OFFICIAL_ANNA,
                          ['so','.n','.a',',','.a','.n','.a'],
                          "son'a,an'a")
        def test_17_gen_official_anna_nn2(self):
            self.checkGen(GEN_OFFICIAL_ANNA,
                          ['so','.n','na',',','.a','.n','na'],
                          "sonna,anna")
        def test_18_gen_official_anna_nn_reduce(self):
            self.checkGen(GEN_OFFICIAL_ANNA,
                          ['so','.n','ka',',','.a','.n','ka'],
                          'sonka,anka')
        def test_19_gen_english_rule1(self):
            self.checkGen(GEN_ENGLISH,
                          ['ka','.n','pu'],
                          'kampu')
        def test_19_gen_english_rule2(self):
            self.checkGen(GEN_ENGLISH,
                           ['do','.t','ti','mo'],
                           'dotchimo')

        def test_20_gen_mixed(self):
            self.checkGenRaw(GEN_OFFICIAL,
                             [MoraTable.get('.a'), 'Ｉ', MoraTable.get('.e')],
                             'aＩe')

        def checkKana2Official(self, kana, r0):
            a = ( m or c for (c,m) in parse(kana) )
            roma = gen_official(a)
            self.assertEqual(roma, r0)
        def checkOfficial2Kana(self, roma, k0):
            a = ( (m and m.zenk) or c for (c,m) in parse_official(roma) )
            kana = ''.join(a)
            self.assertEqual(kana, k0)

        def test_30_kana2official_basic1(self):
            self.checkKana2Official('ちょいとあんた,そんなこといってっけどさ',
                                    "tyoitoanta,son'nakotoittekkedosa")
        def test_30_kana2official_basic2(self):
            self.checkKana2Official('にっちもさっちも.',
                                    'nittimosattimo.')
        def test_31_kana2official_mixed(self):
            self.checkKana2Official('ちょいとあんたソンナコトいってっけどサ.',
                                    "tyoitoantason'nakotoittekkedosa.")
        def test_32_kana2official_ignore(self):
            self.checkKana2Official('ちょいとあんた○１２３０そんなこといってっけどさ.',
                                    "tyoitoanta○１２３０son'nakotoittekkedosa.")
        def test_33_official2kana_basic1(self):
            self.checkOfficial2Kana("choitoanta,sonnnakotoittekkedosa",
                                    'チョイトアンタ,ソンナコトイッテッケドサ')
        def test_33_official2kana_basic2(self):
            self.checkOfficial2Kana('nitchimosatchimo.',
                                    'ニッチモサッチモ.')

    unittest.main()
