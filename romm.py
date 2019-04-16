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
        u'.n', u'ン', u'\uff9d', u'ん', u"n'", u'+n',
        u'n:k', u'n:s', u'n:t', u'n:c', u'n:h', u'n:m', u'n:r', u'n:w',
        u'n:g', u'n:z', u'n:d', u'n:j', u'n:b', u'n:f', u'n:p', u'm:p',
        u'n:q', u'n:v', u'n:x', u'n:l')

    ALL = (
        # (symbol, zenkaku_kana, hankaku_kana, zenkaku_hira, output, input)
        MORA_NN,

        Mora(u'.a', u'ア', u'\uff71', u'あ', u'a'),
        Mora(u'.i', u'イ', u'\uff72', u'い', u'i', u'+y'),
        Mora(u'.u', u'ウ', u'\uff73', u'う', u'u', u'wu', u'+w'),
        Mora(u'.e', u'エ', u'\uff74', u'え', u'e'),
        Mora(u'.o', u'オ', u'\uff75', u'お', u'o'),

        Mora(u'ka', u'カ', u'\uff76', u'か', u'ka', u'+ca'),
        Mora(u'ki', u'キ', u'\uff77', u'き', u'ki', u'+ky'),
        Mora(u'ku', u'ク', u'\uff78', u'く', u'ku', u'+k', u'+c', u'+q'),
        Mora(u'ke', u'ケ', u'\uff79', u'け', u'ke'),
        Mora(u'ko', u'コ', u'\uff7a', u'こ', u'ko'),

        Mora(u'sa', u'サ', u'\uff7b', u'さ', u'sa'),
        Mora(u'si', u'シ', u'\uff7c', u'し', u'!si', u'shi', u'+si', u'+sy'),
        Mora(u'su', u'ス', u'\uff7d', u'す', u'su', u'+s'),
        Mora(u'se', u'セ', u'\uff7e', u'せ', u'se'),
        Mora(u'so', u'ソ', u'\uff7f', u'そ', u'so'),

        Mora(u'ta', u'タ', u'\uff80', u'た', u'ta'),
        Mora(u'ti', u'チ', u'\uff81', u'ち', u'!ti', u'chi', u'ci', u'+ch'),
        Mora(u'tu', u'ツ', u'\uff82', u'つ', u'!tu', u'tsu'),
        Mora(u'te', u'テ', u'\uff83', u'て', u'te'),
        Mora(u'to', u'ト', u'\uff84', u'と', u'to', u'+t'),

        Mora(u'na', u'ナ', u'\uff85', u'な', u'na'),
        Mora(u'ni', u'ニ', u'\uff86', u'に', u'ni', u'+ny'),
        Mora(u'nu', u'ヌ', u'\uff87', u'ぬ', u'nu'),
        Mora(u'ne', u'ネ', u'\uff88', u'ね', u'ne'),
        Mora(u'no', u'ノ', u'\uff89', u'の', u'no'),

        Mora(u'ha', u'ハ', u'\uff8a', u'は', u'ha'),
        Mora(u'hi', u'ヒ', u'\uff8b', u'ひ', u'hi', u'+hy'),
        Mora(u'hu', u'フ', u'\uff8c', u'ふ', u'!hu', u'fu', u'+hu', u'+f'),
        Mora(u'he', u'ヘ', u'\uff8d', u'へ', u'he'),
        Mora(u'ho', u'ホ', u'\uff8e', u'ほ', u'ho'),

        Mora(u'ma', u'マ', u'\uff8f', u'ま', u'ma'),
        Mora(u'mi', u'ミ', u'\uff90', u'み', u'mi', u'+my'),
        Mora(u'mu', u'ム', u'\uff91', u'む', u'mu', u'+m'),
        Mora(u'me', u'メ', u'\uff92', u'め', u'me'),
        Mora(u'mo', u'モ', u'\uff93', u'も', u'mo'),

        Mora(u'ya', u'ヤ', u'\uff94', u'や', u'ya'),
        Mora(u'yu', u'ユ', u'\uff95', u'ゆ', u'yu'),
        Mora(u'ye', u'イェ', u'\uff72\uff6a', u'いぇ', u'ye'),
        Mora(u'yo', u'ヨ', u'\uff96', u'よ', u'yo'),

        Mora(u'ra', u'ラ', u'\uff97', u'ら', u'ra', u'+la'),
        Mora(u'ri', u'リ', u'\uff98', u'り', u'ri', u'+li', u'+ry', u'+ly'),
        Mora(u'ru', u'ル', u'\uff99', u'る', u'ru', u'+lu', u'+r', u'+l'),
        Mora(u're', u'レ', u'\uff9a', u'れ', u're', u'+le'),
        Mora(u'ro', u'ロ', u'\uff9b', u'ろ', u'ro', u'+lo'),

        Mora(u'wa', u'ワ', u'\uff9c', u'わ', u'wa'),
        Mora(u'wi', u'ウィ', u'\uff73\uff68', u'うぃ', u'whi', u'+wi', u'+wy', u'+why'),
        Mora(u'we', u'ウェ', u'\uff73\uff6a', u'うぇ', u'whe', u'+we'),
        Mora(u'wo', u'ウォ', u'\uff73\uff6b', u'うぉ', u'who'),

        Mora(u'Wi', u'ヰ', None, u'ゐ', u'!wi'),
        Mora(u'We', u'ヱ', None, u'ゑ', u'!we'),
        Mora(u'Wo', u'ヲ', u'\uff66', u'を', u'wo'),

        # Special moras: They don't have actual pronunciation,
        #                but we keep them for IMEs.
        Mora(u'xW', u'ァ', u'\uff67', u'ぁ', u'!xa', u'!la'),
        Mora(u'xI', u'ィ', u'\uff68', u'ぃ', u'!xi', u'!li'),
        Mora(u'xV', u'ゥ', u'\uff69', u'ぅ', u'!xu', u'!lu'),
        Mora(u'xE', u'ェ', u'\uff6a', u'ぇ', u'!xe', u'!le'),
        Mora(u'xR', u'ォ', u'\uff6b', u'ぉ', u'!xo', u'!lo'),
        Mora(u'xA', u'ャ', u'\uff6c', u'ゃ', u'!xya', u'!lya'),
        Mora(u'xU', u'ュ', u'\uff6d', u'ゅ', u'!xyu', u'!lyu'),
        Mora(u'xO', u'ョ', u'\uff6e', u'ょ', u'!xyo', u'!lyo'),

        # chouon
        Mora(u'x-', u'ー', u'\uff70', u'ー', u'!x-', u'+h'),

        # choked sound (Sokuon)
        Mora(u'.t', u'ッ', u'\uff6f', u'っ', u'!xtu', u'!ltu',
             u'k:k', u's:s', u't:t', u'h:h', u'f:f', u'm:m', u'r:r',
             u'g:g', u'z:z', u'j:j', u'd:d', u'b:b', u'v:v', u'b:c', u't:c'),

        # voiced (Dakuon)
        Mora(u'ga', u'ガ', u'\uff76\uff9e', u'が', u'ga'),
        Mora(u'gi', u'ギ', u'\uff77\uff9e', u'ぎ', u'gi', u'+gy'),
        Mora(u'gu', u'グ', u'\uff78\uff9e', u'ぐ', u'gu', u'+g'),
        Mora(u'ge', u'ゲ', u'\uff79\uff9e', u'げ', u'ge'),
        Mora(u'go', u'ゴ', u'\uff7a\uff9e', u'ご', u'go'),

        Mora(u'za', u'ザ', u'\uff7b\uff9e', u'ざ', u'za'),
        Mora(u'zi', u'ジ', u'\uff7c\uff9e', u'じ', u'!zi', u'ji', u'+zi'),
        Mora(u'zu', u'ズ', u'\uff7d\uff9e', u'ず', u'zu', u'+z'),
        Mora(u'ze', u'ゼ', u'\uff7e\uff9e', u'ぜ', u'ze'),
        Mora(u'zo', u'ゾ', u'\uff7f\uff9e', u'ぞ', u'zo'),

        Mora(u'da', u'ダ', u'\uff80\uff9e', u'だ', u'da'),
        Mora(u'di', u'ヂ', u'\uff81\uff9e', u'ぢ', u'!di', u'dzi'),
        Mora(u'du', u'ヅ', u'\uff82\uff9e', u'づ', u'!du', u'dzu'),
        Mora(u'de', u'デ', u'\uff83\uff9e', u'で', u'de'),
        Mora(u'do', u'ド', u'\uff84\uff9e', u'ど', u'do', u'+d'),

        Mora(u'ba', u'バ', u'\uff8a\uff9e', u'ば', u'ba'),
        Mora(u'bi', u'ビ', u'\uff8b\uff9e', u'び', u'bi', u'+by'),
        Mora(u'bu', u'ブ', u'\uff8c\uff9e', u'ぶ', u'bu', u'+b'),
        Mora(u'be', u'ベ', u'\uff8d\uff9e', u'べ', u'be'),
        Mora(u'bo', u'ボ', u'\uff8e\uff9e', u'ぼ', u'bo'),

        # p- sound (Handakuon)
        Mora(u'pa', u'パ', u'\uff8a\uff9f', u'ぱ', u'pa'),
        Mora(u'pi', u'ピ', u'\uff8b\uff9f', u'ぴ', u'pi', u'+py'),
        Mora(u'pu', u'プ', u'\uff8c\uff9f', u'ぷ', u'pu', u'+p'),
        Mora(u'pe', u'ペ', u'\uff8d\uff9f', u'ぺ', u'pe'),
        Mora(u'po', u'ポ', u'\uff8e\uff9f', u'ぽ', u'po'),

        # double consonants (Youon)
        Mora(U'KA', u'キャ', u'\uff77\uff6c', u'きゃ', u'kya'),
        Mora(U'KU', u'キュ', u'\uff77\uff6d', u'きゅ', u'kyu', u'+cu'),
        Mora(U'KE', u'キェ', u'\uff77\uff6a', u'きぇ', u'kye'),
        Mora(U'KO', u'キョ', u'\uff77\uff6e', u'きょ', u'kyo'),

        Mora(u'kA', u'クァ', u'\uff78\uff67', u'くぁ', u'qa'),
        Mora(u'kI', u'クィ', u'\uff78\uff68', u'くぃ', u'qi'),
        Mora(u'kE', u'クェ', u'\uff78\uff6a', u'くぇ', u'qe'),
        Mora(u'kO', u'クォ', u'\uff78\uff6b', u'くぉ', u'qo'),

        Mora(U'SA', u'シャ', u'\uff7c\uff6c', u'しゃ', u'!sya', u'sha', u'+sya'),
        Mora(U'SU', u'シュ', u'\uff7c\uff6d', u'しゅ', u'!syu', u'shu', u'+syu', u'+sh'),
        Mora(U'SE', u'シェ', u'\uff7c\uff6a', u'しぇ', u'!sye', u'she', u'+sye'),
        Mora(U'SO', u'ショ', u'\uff7c\uff6e', u'しょ', u'!syo', u'sho', u'+syo'),

        Mora(U'CA', u'チャ', u'\uff81\uff6c', u'ちゃ', u'!tya', u'!cya', u'cha'),
        Mora(U'CU', u'チュ', u'\uff81\uff6d', u'ちゅ', u'!tyu', u'!cyu', u'chu'),
        Mora(U'CE', u'チェ', u'\uff81\uff6a', u'ちぇ', u'!tye', u'!cye', u'che'),
        Mora(U'CO', u'チョ', u'\uff81\uff6e', u'ちょ', u'!tyo', u'!cyo', u'cho'),
        Mora(U'TI', u'ティ', u'\uff83\uff68', u'てぃ', u'!tyi', u'+ti'),
        Mora(U'TU', u'テュ', u'\uff83\uff6d', u'てゅ', u'!thu', u'+tu'),
        Mora(U'TO', u'トゥ', u'\uff84\uff69', u'とぅ', u'!tho', u'+two'),

        Mora(U'NA', u'ニャ', u'\uff86\uff6c', u'にゃ', u'nya'),
        Mora(U'NU', u'ニュ', u'\uff86\uff6d', u'にゅ', u'nyu'),
        Mora(U'NI', u'ニェ', u'\uff86\uff6a', u'にぇ', u'nye'),
        Mora(U'NO', u'ニョ', u'\uff86\uff6e', u'にょ', u'nyo'),

        Mora(U'HA', u'ヒャ', u'\uff8b\uff6c', u'ひゃ', u'hya'),
        Mora(U'HU', u'ヒュ', u'\uff8b\uff6d', u'ひゅ', u'hyu'),
        Mora(U'HE', u'ヒェ', u'\uff8b\uff6a', u'ひぇ', u'hye'),
        Mora(U'HO', u'ヒョ', u'\uff8b\uff6e', u'ひょ', u'hyo'),

        Mora(U'FA', u'ファ', u'\uff8c\uff67', u'ふぁ', u'fa'),
        Mora(U'FI', u'フィ', u'\uff8c\uff68', u'ふぃ', u'fi', u'+fy'),
        Mora(U'FE', u'フェ', u'\uff8c\uff6a', u'ふぇ', u'fe'),
        Mora(U'FO', u'フォ', u'\uff8c\uff6b', u'ふぉ', u'fo'),
        Mora(U'FU', u'フュ', u'\uff8c\uff6d', u'ふゅ', u'fyu'),
        Mora(u'Fo', u'フョ', u'\uff8c\uff6e', u'ふょ', u'fyo'),

        Mora(U'MA', u'ミャ', u'\uff90\uff6c', u'みゃ', u'mya'),
        Mora(U'MU', u'ミュ', u'\uff90\uff6d', u'みゅ', u'myu'),
        Mora(U'ME', u'ミェ', u'\uff90\uff6a', u'みぇ', u'mye'),
        Mora(U'MO', u'ミョ', u'\uff90\uff6e', u'みょ', u'myo'),

        Mora(U'RA', u'リャ', u'\uff98\uff6c', u'りゃ', u'rya', u'+lya'),
        Mora(U'RU', u'リュ', u'\uff98\uff6d', u'りゅ', u'ryu', u'+lyu'),
        Mora(U'RE', u'リェ', u'\uff98\uff6a', u'りぇ', u'rye', u'+lye'),
        Mora(U'RO', u'リョ', u'\uff98\uff6e', u'りょ', u'ryo', u'+lyo'),

        # double consonants + voiced
        Mora(U'GA', u'ギャ', u'\uff77\uff9e\uff6c', u'ぎゃ', u'gya'),
        Mora(U'GU', u'ギュ', u'\uff77\uff9e\uff6d', u'ぎゅ', u'gyu'),
        Mora(U'GE', u'ギェ', u'\uff77\uff9e\uff6a', u'ぎぇ', u'gye'),
        Mora(U'GO', u'ギョ', u'\uff77\uff9e\uff6e', u'ぎょ', u'gyo'),

        Mora(u'Ja', u'ジャ', u'\uff7c\uff9e\uff6c', u'じゃ', u'ja', u'zya'),
        Mora(u'Ju', u'ジュ', u'\uff7c\uff9e\uff6d', u'じゅ', u'ju', u'zyu'),
        Mora(u'Je', u'ジェ', u'\uff7c\uff9e\uff6a', u'じぇ', u'je', u'zye'),
        Mora(u'Jo', u'ジョ', u'\uff7c\uff9e\uff6e', u'じょ', u'jo', u'zyo'),

        Mora(U'JA', u'ヂャ', u'\uff81\uff9e\uff6c', u'ぢゃ', u'zha'),
        Mora(U'JU', u'ヂュ', u'\uff81\uff9e\uff6d', u'ぢゅ', u'zhu'),
        Mora(U'JE', u'ヂェ', u'\uff81\uff9e\uff6a', u'ぢぇ', u'zhe'),
        Mora(U'JO', u'ヂョ', u'\uff81\uff9e\uff6e', u'ぢょ', u'zho'),

        Mora(u'dI', u'ディ', u'\uff83\uff9e\uff68', u'でぃ', u'+di', u'dyi'),
        Mora(u'dU', u'デュ', u'\uff83\uff9e\uff6d', u'でゅ', u'+du', u'dyu', u'dhu'),
        Mora(u'dO', u'ドゥ', u'\uff84\uff9e\uff69', u'どぅ', u'dho'),

        Mora(U'BA', u'ビャ', u'\uff8b\uff9e\uff6c', u'びゃ', u'bya'),
        Mora(U'BU', u'ビュ', u'\uff8b\uff9e\uff6d', u'びゅ', u'byu'),
        Mora(U'BE', u'ビェ', u'\uff8b\uff9e\uff6a', u'びぇ', u'bye'),
        Mora(U'BO', u'ビョ', u'\uff8b\uff9e\uff6e', u'びょ', u'byo'),

        Mora(u'va', u'ヴァ', u'\uff73\uff9e\uff67', u'う゛ぁ', u'va'),
        Mora(u'vi', u'ヴィ', u'\uff73\uff9e\uff68', u'う゛ぃ', u'vi', u'+vy'),
        Mora(u'vu', u'ヴ',   u'\uff73\uff9e',       u'う゛', u'vu', u'+v'),
        Mora(u've', u'ヴェ', u'\uff73\uff9e\uff6a', u'う゛ぇ', u've'),
        Mora(u'vo', u'ヴォ', u'\uff73\uff9e\uff6b', u'う゛ぉ', u'vo'),

        # double consonants + p-sound
        Mora(U'PA', u'ピャ', u'\uff8b\uff9f\uff6c', u'ぴゃ', u'pya'),
        Mora(U'PU', u'ピュ', u'\uff8b\uff9f\uff6d', u'ぴゅ', u'pyu'),
        Mora(U'PE', u'ピェ', u'\uff8b\uff9f\uff6a', u'ぴぇ', u'pye'),
        Mora(U'PO', u'ピョ', u'\uff8b\uff9f\uff6e', u'ぴょ', u'pyo'),
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
        s = u''
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
                            u'aIＵえオ',
                            [u'.a',u'.i',u'Ｕ',u'.e',u'.o'])
            return
        def test_07_parse_ignore(self):
            self.checkParse(PARSE_OFFICIAL,
                            u'ai$uεo',
                            [u'.a',u'.i',u'$',u'.u',u'ε',u'.o'])
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
                             [MoraTable.get('.a'), u'Ｉ', MoraTable.get('.e')],
                             u'aＩe')

        def checkKana2Official(self, kana, r0):
            a = ( m or c for (c,m) in parse(kana) )
            roma = gen_official(a)
            self.assertEqual(roma, r0)
        def checkOfficial2Kana(self, roma, k0):
            a = ( (m and m.zenk) or c for (c,m) in parse_official(roma) )
            kana = u''.join(a)
            self.assertEqual(kana, k0)

        def test_30_kana2official_basic1(self):
            self.checkKana2Official(u'ちょいとあんた,そんなこといってっけどさ',
                                    u"tyoitoanta,son'nakotoittekkedosa")
        def test_30_kana2official_basic2(self):
            self.checkKana2Official(u'にっちもさっちも.',
                                    u'nittimosattimo.')
        def test_31_kana2official_mixed(self):
            self.checkKana2Official(u'ちょいとあんたソンナコトいってっけどサ.',
                                    u"tyoitoantason'nakotoittekkedosa.")
        def test_32_kana2official_ignore(self):
            self.checkKana2Official(u'ちょいとあんた○１２３０そんなこといってっけどさ.',
                                    u"tyoitoanta○１２３０son'nakotoittekkedosa.")
        def test_33_official2kana_basic1(self):
            self.checkOfficial2Kana(u"choitoanta,sonnnakotoittekkedosa",
                                    u'チョイトアンタ,ソンナコトイッテッケドサ')
        def test_33_official2kana_basic2(self):
            self.checkOfficial2Kana(u'nitchimosatchimo.',
                                    u'ニッチモサッチモ.')

    unittest.main()
