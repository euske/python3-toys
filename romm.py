#!/usr/bin/env python
# -*- coding: utf-8 -*-

##  romm.py - handles Roma-ji and kana.
##

##  Constants
##
MORA_DATA = [
  # (symbol, zenkaku_kana, hankaku_kana, zenkaku_hira, output, input)
  
  ( '.a', u'ア', u'\uff71', u'あ', 'a', 'a', '3a' ),
  ( '.i', u'イ', u'\uff72', u'い', 'i', 'i', '3i', '2y' ),
  ( '.u', u'ウ', u'\uff73', u'う', 'u', 'u', '3u', '3wu', '2w' ),
  ( '.e', u'エ', u'\uff74', u'え', 'e', 'e', '3e' ),
  ( '.o', u'オ', u'\uff75', u'お', 'o', 'o', '3o' ),
  
  ( 'ka', u'カ', u'\uff76', u'か', 'ka', 'ka', '3ka', '3ca' ),
  ( 'ki', u'キ', u'\uff77', u'き', 'ki', 'ki', '3ki', '2ky' ),
  ( 'ku', u'ク', u'\uff78', u'く', 'ku', 'ku', '3ku', '2k', '2c', '2q' ),
  ( 'ke', u'ケ', u'\uff79', u'け', 'ke', 'ke', '3ke' ),
  ( 'ko', u'コ', u'\uff7a', u'こ', 'ko', 'ko', '3ko' ),
  
  ( 'sa', u'サ', u'\uff7b', u'さ', 'sa', 'sa', '3sa' ),
  ( 'si', u'シ', u'\uff7c', u'し', 'si', 'shi', '3si', '3shi', '2sy' ),
  ( 'su', u'ス', u'\uff7d', u'す', 'su', 'su', '3su', '2s' ),
  ( 'se', u'セ', u'\uff7e', u'せ', 'se', 'se', '3se' ),
  ( 'so', u'ソ', u'\uff7f', u'そ', 'so', 'so', '3so' ),
                               
  ( 'ta', u'タ', u'\uff80', u'た', 'ta', 'ta', '3ta' ),
  ( 'ti', u'チ', u'\uff81', u'ち', 'ti', 'chi', '3chi', '3ci', '1ti', '2chy', '2ch' ),
  ( 'tu', u'ツ', u'\uff82', u'つ', 'tu', 'tsu', '3tsu', '1tu' ),
  ( 'te', u'テ', u'\uff83', u'て', 'te', 'te', '3te' ),
  ( 'to', u'ト', u'\uff84', u'と', 'to', 'to', '3to', '2t' ),
  
  ( 'na', u'ナ', u'\uff85', u'な', 'na', 'na', '3na' ),
  ( 'ni', u'ニ', u'\uff86', u'に', 'ni', 'ni', '3ni', '2ny' ),
  ( 'nu', u'ヌ', u'\uff87', u'ぬ', 'nu', 'nu', '3nu' ),
  ( 'ne', u'ネ', u'\uff88', u'ね', 'ne', 'ne', '3ne' ),
  ( 'no', u'ノ', u'\uff89', u'の', 'no', 'no', '3no' ),
  
  ( 'ha', u'ハ', u'\uff8a', u'は', 'ha', 'ha', '3ha' ),
  ( 'hi', u'ヒ', u'\uff8b', u'ひ', 'hi', 'hi', '3hi', '2hy' ),
  ( 'hu', u'フ', u'\uff8c', u'ふ', 'hu', 'fu', '3hu', '3fu', '2f' ),
  ( 'he', u'ヘ', u'\uff8d', u'へ', 'he', 'he', '3he' ),
  ( 'ho', u'ホ', u'\uff8e', u'ほ', 'ho', 'ho', '3ho' ),
  
  ( 'ma', u'マ', u'\uff8f', u'ま', 'ma', 'ma', '3ma' ),
  ( 'mi', u'ミ', u'\uff90', u'み', 'mi', 'mi', '3mi', '2my' ),
  ( 'mu', u'ム', u'\uff91', u'む', 'mu', 'mu', '3mu', '2m' ),
  ( 'me', u'メ', u'\uff92', u'め', 'me', 'me', '3me' ),
  ( 'mo', u'モ', u'\uff93', u'も', 'mo', 'mo', '3mo' ),
  
  ( 'ya', u'ヤ', u'\uff94', u'や', 'ya', 'ya', '3ya' ),
  ( 'yu', u'ユ', u'\uff95', u'ゆ', 'yu', 'yu', '3yu' ),
  ( 'ye', u'イェ', u'\uff72\uff6a', u'いぇ', 'ye', 'ye', '3ye' ),
  ( 'yo', u'ヨ', u'\uff96', u'よ', 'yo', 'yo', '3yo' ),
  
  ( 'ra', u'ラ', u'\uff97', u'ら', 'ra', 'ra', '3ra', '2la' ),
  ( 'ri', u'リ', u'\uff98', u'り', 'ri', 'ri', '3ri' ,'2li', '2ry', '2ly' ),
  ( 'ru', u'ル', u'\uff99', u'る', 'ru', 'ru', '3ru' ,'2lu', '2r', '2l' ),
  ( 're', u'レ', u'\uff9a', u'れ', 're', 'le', '3re', '2le' ),
  ( 'ro', u'ロ', u'\uff9b', u'ろ', 'ro', 'ro', '3ro', '2lo' ),
  
  ( 'wa', u'ワ', u'\uff9c', u'わ', 'wa', 'wa', '3wa' ),
  ( 'wi', u'ウィ', u'\uff73\uff68', u'うぃ', 'wi', 'wi', '3whi', '3wi', '2wy', '2why' ),
  ( 'we', u'ウェ', u'\uff73\uff6a', u'うぇ', 'we', 'we', '3whe', '3we' ),
  ( 'wo', u'ウォ', u'\uff73\uff6b', u'うぉ', 'wo', 'wo', '1xwo', '2wo' ),
  
  ( 'Wi', u'ヰ', u'', u'ゐ', 'wi', 'i', '1xwi' ),
  ( 'We', u'ヱ', u'', u'ゑ', 'we', 'e', '1xwe' ),
  ( 'Wo', u'ヲ', u'\uff66', u'を', 'wo', 'o', '1wo' ),

  ( '.n', u'ン', u'\uff9d', u'ん', "nn", 'n', '3n', "3n'", '3m:p', '2ng' ),
  
  # Special morae: They don't have actual pronunciation,
  #                but we keep them for IMEs.
  ( 'xW', u'ァ', u'\uff67', u'ぁ', '(a)', '(a)', '1xa', '1la' ),
  ( 'xI', u'ィ', u'\uff68', u'ぃ', '(i)', '(i)', '1xi', '1li' ),
  ( 'xV', u'ゥ', u'\uff69', u'ぅ', '(u)', '(u)', '1xu', '1lu' ),
  ( 'xE', u'ェ', u'\uff6a', u'ぇ', '(e)', '(e)', '1xe', '1le' ),
  ( 'xR', u'ォ', u'\uff6b', u'ぉ', '(o)', '(o)', '1xo', '1lo' ),
  ( 'xA', u'ャ', u'\uff6c', u'ゃ', '(ya)', '(ya)', '1xya', '1lya' ),
  ( 'xU', u'ュ', u'\uff6d', u'ゅ', '(yu)', '(yu)', '1xyu', '1lyu' ),
  ( 'xO', u'ョ', u'\uff6e', u'ょ', '(yo)', '(yo)', '1xyo', '1lyo' ),
  
  ( '!v', u'゛', u'\uff9e', u'゛', '(dakuten)', '(dakuten)' ),
  ( '!p', u'゜', u'\uff9f', u'゜', '(handakuten)', '(handakuten)' ),
  ( '!.', u'。', u'\uff61', u'。', '.', '.', '3.' ),
  ( '!,', u'、', u'\uff64', u'、', ',', ',', '3,' ),
  ( '!_', u'・', u'\uff65', u'・', '(nakaguro)', '(nakaguro)', '1x.' ),
  ( '![', u'「', u'\uff62', u'「', '[', '[', '3[' ),
  ( '!]', u'」', u'\uff63', u'」', ']', ']', '3]' ),
  
  # chouon
  ( '.-', u'ー', u'\uff70', u'ー', 'h', 'h', '1-', '2h' ),
  
  # choked sound (Sokuon)
  ( '.t', u'ッ', u'\uff6f', u'っ', '>', '>', '1xtu', '1ltu',
    '3k:k', '3s:s', '3t:t', '3h:h', '3f:f', '3m:m', '3r:r',
    '3g:g', '3z:z', '3j:j', '3d:d', '3b:b', '3v:v', '3b:c', '3t:c' ),
  
  # voiced (Dakuon)
  ( 'ga', u'ガ', u'\uff76\uff9e', u'が', 'ga', 'ga', '3ga' ),
  ( 'gi', u'ギ', u'\uff77\uff9e', u'ぎ', 'gi', 'gi', '3gi', '2gy' ),
  ( 'gu', u'グ', u'\uff78\uff9e', u'ぐ', 'gu', 'gu', '3gu', '2g'),
  ( 'ge', u'ゲ', u'\uff79\uff9e', u'げ', 'ge', 'ge', '3ge' ),
  ( 'go', u'ゴ', u'\uff7a\uff9e', u'ご', 'go', 'go', '3go' ),
  
  ( 'za', u'ザ', u'\uff7b\uff9e', u'ざ', 'za', 'za', '3za' ),
  ( 'zi', u'ジ', u'\uff7c\uff9e', u'じ', 'zi', 'ji', '3ji', '1zi' ),
  ( 'zu', u'ズ', u'\uff7d\uff9e', u'ず', 'zu', 'zu', '3zu', '2z' ),
  ( 'ze', u'ゼ', u'\uff7e\uff9e', u'ぜ', 'ze', 'ze', '3ze' ),
  ( 'zo', u'ゾ', u'\uff7f\uff9e', u'ぞ', 'zo', 'zo', '3zo' ),
  
  ( 'da', u'ダ', u'\uff80\uff9e', u'だ', 'da', 'da', '3da' ),
  ( 'di', u'ヂ', u'\uff81\uff9e', u'ぢ', 'di', 'dzi', '3dzi', '1di' ),
  ( 'du', u'ヅ', u'\uff82\uff9e', u'づ', 'du', 'dzu', '3dzu', '1du' ),
  ( 'de', u'デ', u'\uff83\uff9e', u'で', 'de', 'de', '3de' ),
  ( 'do', u'ド', u'\uff84\uff9e', u'ど', 'do', 'do', '3do', '2d' ),
  
  ( 'ba', u'バ', u'\uff8a\uff9e', u'ば', 'ba', 'ba', '3ba' ),
  ( 'bi', u'ビ', u'\uff8b\uff9e', u'び', 'bi', 'bi', '3bi', '2by' ),
  ( 'bu', u'ブ', u'\uff8c\uff9e', u'ぶ', 'bu', 'bu', '3bu', '2b' ),
  ( 'be', u'ベ', u'\uff8d\uff9e', u'べ', 'be', 'be', '3be' ),
  ( 'bo', u'ボ', u'\uff8e\uff9e', u'ぼ', 'bo', 'bo', '3bo' ),
  
  # p- sound (Handakuon)
  ( 'pa', u'パ', u'\uff8a\uff9f', u'ぱ', 'pa', 'pa', '3pa' ),
  ( 'pi', u'ピ', u'\uff8b\uff9f', u'ぴ', 'pi', 'pi', '3pi', '2py' ),
  ( 'pu', u'プ', u'\uff8c\uff9f', u'ぷ', 'pu', 'pu', '3pu', '2p' ),
  ( 'pe', u'ペ', u'\uff8d\uff9f', u'ぺ', 'pe', 'pe', '3pe' ),
  ( 'po', u'ポ', u'\uff8e\uff9f', u'ぽ', 'po', 'po', '3po' ),

  # double consonants (Youon)
  ( 'KA', u'キャ', u'\uff77\uff6c', u'きゃ', 'kya', 'kya', '3kya' ),
  ( 'KU', u'キュ', u'\uff77\uff6d', u'きゅ', 'kyu', 'kyu', '3kyu', '2cu' ),
  ( 'KE', u'キェ', u'\uff77\uff6a', u'きぇ', 'kye', 'kye', '3kye' ),
  ( 'KO', u'キョ', u'\uff77\uff6e', u'きょ', 'kyo', 'kyo', '3kyo' ),

  ( 'kA', u'クァ', u'\uff78\uff67', u'くぁ', 'qa', 'qa', '3qa' ),
  ( 'kI', u'クィ', u'\uff78\uff68', u'くぃ', 'qi', 'qi', '3qi' ),
  ( 'kE', u'クェ', u'\uff78\uff6a', u'くぇ', 'qe', 'qe', '3qe' ),
  ( 'kO', u'クォ', u'\uff78\uff6b', u'くぉ', 'qo', 'qo', '3qo' ),
  
  ( 'SA', u'シャ', u'\uff7c\uff6c', u'しゃ', 'sya', 'sha', '3sya', '3sha' ),
  ( 'SU', u'シュ', u'\uff7c\uff6d', u'しゅ', 'syu', 'shu', '3syu', '3shu', '2sh' ),
  ( 'SE', u'シェ', u'\uff7c\uff6a', u'しぇ', 'sye', 'she', '3sye', '3she' ),
  ( 'SO', u'ショ', u'\uff7c\uff6e', u'しょ', 'syo', 'sho', '3syo', '3sho' ),
  
  ( 'CA', u'チャ', u'\uff81\uff6c', u'ちゃ', 'tya', 'cha', '3tya', '1cya', '3cha' ),
  ( 'CU', u'チュ', u'\uff81\uff6d', u'ちゅ', 'tyu', 'chu', '3tyu', '1cyu', '3chu' ),
  ( 'CE', u'チェ', u'\uff81\uff6a', u'ちぇ', 'tye', 'che', '3tye', '1cye', '3che' ),
  ( 'CO', u'チョ', u'\uff81\uff6e', u'ちょ', 'tyo', 'cho', '3tyo', '1cyo', '3cho' ),
  ( 'TI', u'ティ', u'\uff83\uff68', u'てぃ', 'tyi', 'ti', '3tyi', '3thi', '2ti' ),
  ( 'TU', u'テュ', u'\uff83\uff6d', u'てゅ', 'thu', 'tu', '3thu', '2tu' ),
  ( 'TO', u'トゥ', u'\uff84\uff69', u'とぅ', 'to', 'to', '3tho', '2two' ),
  
  ( 'NA', u'ニャ', u'\uff86\uff6c', u'にゃ', 'nya', 'nya', '3nya' ),
  ( 'NU', u'ニュ', u'\uff86\uff6d', u'にゅ', 'nyu', 'nyu', '3nyu' ),
  ( 'NI', u'ニェ', u'\uff86\uff6a', u'にぇ', 'nye', 'nye', '3nye' ),
  ( 'NO', u'ニョ', u'\uff86\uff6e', u'にょ', 'nyo', 'nyo', '3nyo' ),
  
  ( 'HA', u'ヒャ', u'\uff8b\uff6c', u'ひゃ', 'hya', 'hya', '3hya' ),
  ( 'HU', u'ヒュ', u'\uff8b\uff6d', u'ひゅ', 'hyu', 'hyu', '3hyu' ),
  ( 'HE', u'ヒェ', u'\uff8b\uff6a', u'ひぇ', 'hye', 'hye', '3hye' ),
  ( 'HO', u'ヒョ', u'\uff8b\uff6e', u'ひょ', 'hyo', 'hyo', '3hyo' ),
  
  ( 'FA', u'ファ', u'\uff8c\uff67', u'ふぁ', 'fa', 'fa', '3fa' ),
  ( 'FI', u'フィ', u'\uff8c\uff68', u'ふぃ', 'fi', 'fi', '3fi', '2fy' ),
  ( 'FE', u'フェ', u'\uff8c\uff6a', u'ふぇ', 'fe', 'fe', '3fe' ),
  ( 'FO', u'フォ', u'\uff8c\uff6b', u'ふぉ', 'fo', 'fo', '3fo' ),
  ( 'FU', u'フュ', u'\uff8c\uff6d', u'ふゅ', 'fyu', 'fyu', '3fyu' ),
  ( 'Fo', u'フョ', u'\uff8c\uff6e', u'ふょ', 'fyo', 'fyo', '3fyo' ),
  
  ( 'MA', u'ミャ', u'\uff90\uff6c', u'みゃ', 'mya', 'mya', '3mya' ),
  ( 'MU', u'ミュ', u'\uff90\uff6d', u'みゅ', 'myu', 'myu', '3myu' ),
  ( 'ME', u'ミェ', u'\uff90\uff6a', u'みぇ', 'mye', 'mye', '3mye' ),
  ( 'MO', u'ミョ', u'\uff90\uff6e', u'みょ', 'myo', 'myo', '3myo' ),
  
  ( 'RA', u'リャ', u'\uff98\uff6c', u'りゃ', 'rya', 'rya', '3rya', '2lya' ),
  ( 'RU', u'リュ', u'\uff98\uff6d', u'りゅ', 'ryu', 'ryu', '3ryu', '2lyu' ),
  ( 'RE', u'リェ', u'\uff98\uff6a', u'りぇ', 'rye', 'rye', '3rye', '2lye' ),
  ( 'RO', u'リョ', u'\uff98\uff6e', u'りょ', 'ryo', 'ryo', '3ryo', '2lyo' ),
  
  # double consonants + voiced
  ( 'GA', u'ギャ', u'\uff77\uff9e\uff6c', u'ぎゃ', 'gya', 'gya', '3gya' ),
  ( 'GU', u'ギュ', u'\uff77\uff9e\uff6d', u'ぎゅ', 'gyu', 'gyu', '3gyu' ),
  ( 'GE', u'ギェ', u'\uff77\uff9e\uff6a', u'ぎぇ', 'gye', 'gye', '3gye' ),
  ( 'GO', u'ギョ', u'\uff77\uff9e\uff6e', u'ぎょ', 'gyo', 'gyo', '3gyo' ),
  
  ( 'Ja', u'ジャ', u'\uff7c\uff9e\uff6c', u'じゃ', 'zya', 'ja', '3zya', '3ja', '3zha' ),
  ( 'Ju', u'ジュ', u'\uff7c\uff9e\uff6d', u'じゅ', 'zyu', 'ju', '3zyu', '3ju', '3zhu' ),
  ( 'Je', u'ジェ', u'\uff7c\uff9e\uff6a', u'じぇ', 'zye', 'je', '3zye', '3je', '3zhe' ),
  ( 'Jo', u'ジョ', u'\uff7c\uff9e\uff6e', u'じょ', 'zyo', 'jo', '3zyo', '3jo', '3zho' ),
  
  ( 'JA', u'ヂャ', u'\uff81\uff9e\uff6c', u'ぢゃ', 'dya', 'dya', '3dya' ),
  ( 'JU', u'ヂュ', u'\uff81\uff9e\uff6d', u'ぢゅ', 'dyu', 'dyu', '3dyu' ),
  ( 'JE', u'ヂェ', u'\uff81\uff9e\uff6a', u'ぢぇ', 'dye', 'dye', '3dye' ),
  ( 'JO', u'ヂョ', u'\uff81\uff9e\uff6e', u'ぢょ', 'dyo', 'dyo', '3dyo' ),

  ( 'dI', u'ディ', u'\uff83\uff9e\uff68', u'でぃ', 'dyi', 'di', '3dyi', '2di' ),
  ( 'dU', u'デュ', u'\uff83\uff9e\uff6d', u'でゅ', 'dyu', 'du', '3dhu', '2du' ),
  ( 'dO', u'ドゥ', u'\uff84\uff9e\uff69', u'どぅ', 'do', 'do', '3dho' ),
  
  ( 'BA', u'ビャ', u'\uff8b\uff9e\uff6c', u'びゃ', 'bya', 'bya', '3bya' ),
  ( 'BU', u'ビュ', u'\uff8b\uff9e\uff6d', u'びゅ', 'byu', 'byu', '3byu' ),
  ( 'BE', u'ビェ', u'\uff8b\uff9e\uff6a', u'びぇ', 'bye', 'bye', '3bye' ),
  ( 'BO', u'ビョ', u'\uff8b\uff9e\uff6e', u'びょ', 'byo', 'byo', '3byo' ),
  
  ( 'va', u'ヴァ', u'\uff73\uff9e\uff67', u'う゛ぁ', 'va', 'va', '3va' ),
  ( 'vi', u'ヴィ', u'\uff73\uff9e\uff68', u'う゛ぃ', 'vi', 'vi', '3vi', '2vy' ),
  ( 'vu', u'ヴ',   u'\uff73\uff9e',       u'う゛', 'vu', 'vu', '3vu', '2v' ),
  ( 've', u'ヴェ', u'\uff73\uff9e\uff6a', u'う゛ぇ', 've', 've', '3ve' ),
  ( 'vo', u'ヴォ', u'\uff73\uff9e\uff6b', u'う゛ぉ', 'vo', 'vo', '3vo' ),
  
  # double consonants + p-sound
  ( 'PA', u'ピャ', u'\uff8b\uff9f\uff6c', u'ぴゃ', 'pya', 'pya', '3pya' ),
  ( 'PU', u'ピュ', u'\uff8b\uff9f\uff6d', u'ぴゅ', 'pyu', 'pyu', '3pyu' ),
  ( 'PE', u'ピェ', u'\uff8b\uff9f\uff6a', u'ぴぇ', 'pye', 'pye', '3pye' ),
  ( 'PO', u'ピョ', u'\uff8b\uff9f\uff6e', u'ぴょ', 'pyo', 'pyo', '3pyo' ),
]

SYMBOL = {
  u'　':' ', u'、':',', u'。':'.', u'，':',', u'．':'.',
  u'・':'-', u'：':':', u'；':';', u'？':'?', u'！':'!',
  u'゛':'(dakuten)', u'゜':'(handakuten)', u'´':"'", u'｀':'`',
  u'¨':'"', u'＾':'^', u'￣':'~', u'＿':'_', u'ヽ':'(repeat)',
  u'ヾ':'(repeat-dakuten)', u'ゝ':'(repeat)', u'ゞ':'(repeat-dakuten)',
  u'〃':'"', u'〆':'(shime)', u'〇':'0', u'ー':'-', u'—':'--',
  u'‐':' - ', u'／':'/', u'＼':'\\', u'〜':'-', u'‖':'||',
  u'｜':'|', u'…':'...', u'‥':'..', u'‘':'`', u'’':"'",
  u'“':'"', u'”':'"', u'（':'(', u'）':')', u'〔':'[',
  u'〕':']', u'［':'[', u'］':']', u'｛':'{', u'｝':'}',
  u'〈':'<', u'〉':'>', u'《':'<<', u'》':'>>', u'「':'"',
  u'」':'"', u'『':'[[', u'』':']]', u'【':'{{', u'】':'}}',
  u'＋':'+', u'−':'-', u'±':'+-', u'×':'*', u'÷':'/',
  u'＝':'=', u'≠':'!=', u'＜':'<', u'＞':'>', u'≦':'<=',
  u'≧':'>=', u'∞':'(inf)', u'∴':'(3dot-therefore)', u'♂':'(male)',
  u'♀':'(female)', u'°':'(degree)', u'′':"'", u'″':"''",
  u'℃':'(Celsius)', u'￥':'(Yen)', u'＄':'$', u'¢':'(Cent)',
  u'£':'(Pound)', u'％':'%', u'＃':'#', u'＆':'&', u'＊':'*',
  u'＠':'@', u'§':'(section)', u'☆':'(star)', u'★':'(STAR)',
  u'○':'(circle)', u'●':'(CIRCLE)', u'◎':'(circle2)', u'◇':'(dia)',
  u'◆':'(DIA)', u'□':'(box)', u'■':'(BOX)', u'△':'(triangle)',
  u'▲':'(TRIANGLE)', u'▽':'(tri2)', u'▼':'(TRI2)', u'※':'(*)',
  u'〒':'(Yuubin)', u'→':'(right)', u'←':'(left)', u'↑':'(up)', u'↓':'(down)',
  u'〓':'(geta)', u'∈':'(included)', u'∋':'(including)',
  u'⊆':'(subsumed-equal)', u'⊇':'(subsuming-equal)', u'⊂':'(subsumed)',
  u'⊃':'(subsuming)', u'∪':'(union)', u'∩':'(intersection)',
  u'∧':'(and)', u'∨':'(or)', u'¬':'(not)', u'⇒':'(=>)',
  u'⇔':'(<=>)', u'∀':'(forall)', u'∃':'(exists)', u'∠':'(angle)',
  u'⊥':'(perpendicular)', u'⌒':'(arc)', u'∂':'(partial)',
  u'∇':'(nabra)', u'≡':'(:=)', u'≒':'(nearly=)', u'≪':'(<<)',
  u'≫':'(>>)', u'√':'(sqrt)', u'∽':'(lazy)', u'∝':'(proportional)',
  u'∵':'(3dot-becasue)', u'∫':'(integral)', u'∬':'(integral2)',
  u'Å':'(angstrom)', u'‰':'(permil)', u'♯':'(sharp)', u'♭':'(flat)',
  u'♪':'(note)', u'†':'(dagger)', u'‡':'(ddagger)', u'¶':'(paragraph)',
  u'◯':'(O)',

  u'ヮ':'(small-wa)',
  u'ヵ':'(ka)', u'ヶ':'(ko)', 

  u'Α':'(ALPHA)', u'Β':'(BETA)', u'Γ':'(GAMMA)', u'Δ':'(DELTA)',
  u'Ε':'(EPSILON)', u'Ζ':'(ZETA)', u'Η':'(ETA)', u'Θ':'(THETA)',
  u'Ι':'(IOTA)', u'Κ':'(KAPPA)', u'Λ':'(LAMBDA)', u'Μ':'(MU)',
  u'Ν':'(NU)', u'Ξ':'(XI)', u'Ο':'(OMICRON)', u'Π':'(PI)',
  u'Ρ':'(RHO)', u'Σ':'(SIGMA)', u'Τ':'(TAU)', u'Υ':'(UPSILON)',
  u'Φ':'(PHI)', u'Χ':'(CHI)', u'Ψ':'(PSI)', u'Ω':'(OMEGA)',
  u'α':'(alpha)', u'β':'(beta)', u'γ':'(gamma)', u'δ':'(delta)', 
  u'ε':'(epsilon)', u'ζ':'(zeta)', u'η':'(eta)', u'θ':'(theta)',
  u'ι':'(iota)', u'κ':'(kappa)', u'λ':'(lambda)', u'μ':'(mu)',
  u'ν':'(nu)', u'ξ':'(xi)', u'ο':'(omicron)', u'π':'(pi)',
  u'ρ':'(rho)', u'σ':'(sigma)', u'τ':'(tau)', u'υ':'(upsilon)',
  u'φ':'(phi)', u'χ':'(chi)', u'ψ':'(psi)', u'ω':'(omega)',
  
  u'А':'(C-A)', u'Б':'(C-B")', u'В':'(C-V)', u'Г':'(C-G)',
  u'Д':'(C-D)', u'Е':'(C-YE)', u'Ё':'(C-YO)', u'Ж':'(C-ZH)',
  u'З':'(C-Z)', u'И':'(C-II)', u'Й':'(C-II")', u'К':'(C-K)', 
  u'Л':'(C-L)', u'М':'(C-M)', u'Н':'(C-N)', u'О':'(C-O)', 
  u'П':'(C-P)', u'Р':'(C-R")', u'С':'(C-S)', u'Т':'(C-T)',
  u'У':'(C-U)', u'Ф':'(C-F)', u'Х':'(C-X)', u'Ц':'(C-TS)',
  u'Ч':'(C-CH)', u'Ш':'(C-SH)', u'Щ':'(C-SCH)', u'Ъ':'(C-SOFT)',
  u'Ы':'(C-I)', u'Ь':'(C-SEP)', u'Э':'(C-EH)', u'Ю':'(C-YU)',
  u'Я':'(C-YA)', 
  
  u'а':'(c-a)', u'б':'(c-b)', u'в':'(c-v)', u'г':'(c-g)',
  u'д':'(c-g)', u'е':'(c-ye)', u'ё':'(c-yo)', u'ж':'(c-zh)',
  u'з':'(c-z)', u'и':'(c-ii)', u'й':'(c-ii:)', u'к':'(c-k)',
  u'л':'(c-l)', u'м':'(c-m)', u'н':'(c-n)', u'о':'(c-o)',
  u'п':'(c-p)', u'р':'(c-r)', u'с':'(c-s)', u'т':'(c-t)',
  u'у':'(c-u)', u'ф':'(c-f)', u'х':'(c-x)', u'ц':'(c-ts)',
  u'ч':'(c-ch)', u'ш':'(c-sh)', u'щ':'(c-sch)', u'ъ':'(c-soft)',
  u'ы':'(c-i)', u'ь':'(c-sep)', u'э':'(c-eh)', u'ю':'(c-yu)',
  u'я':'(c-ya)',
  
  u'─':'-', u'│':'|', u'┌':'+', u'┐':'+', u'┘':'+',
  u'└':'+', u'├':'+', u'┬':'+', u'┤':'+', u'┴':'+',
  u'┼':'+', u'━':'=', u'┃':'|', u'┏':'+', u'┓':'+',
  u'┛':'+', u'┗':'+', u'┣':'+', u'┳':'+', u'┫':'+',
  u'┻':'+', u'╋':'+', u'┠':'+', u'┯':'+', u'┨':'+',
  u'┷':'+', u'┿':'+', u'┝':'+', u'┰':'+', u'┥':'+',
  u'┸':'+', u'╂':'+',
  }

# 0x20-0x7e:  !"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefghijklmnopqrstuvwxyz{|}~
ZENKAKU = (
  u'　！”＃＄％＆’（）＊＋，−．／０１２３４５６７８９：；＜＝＞？'
  u'＠ＡＢＣＤＥＦＧＨＩＪＫＬＭＮＯＰＱＲＳＴＵＶＷＸＹＺ［＼］＾＿'
  u'‘ａｂｃｄｅｆｇｈｉｊｋｌｍｎｏｐｑｒｓｔｕｖｗｘｙｚ｛｜｝〜'
  )

HANKAKU = (
  ' !"#'
  "$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]"
  '^_`abcdefghijklmnopqrstuvwxyz{|}~'
  )

z2hmap = dict(zip(ZENKAKU, HANKAKU))
h2zmap = dict(zip(ZENKAKU, HANKAKU))

def zen2han(z):
  return ''.join( z2hmap.get(c,c) for c in z )

# Mora Object
class Mora:
  
  def __init__(self, mid, zenk, hank, zenh):
    self.mid = mid
    self.zenk = zenk
    self.hank = hank
    self.zenh = zenh
    return

  def __repr__(self):
    return '<%s>' % self.mid

  def __str__(self):
    return self.zenk
  

##  Translation Table
##

# ParseTable
class ParseTable:
  
  def __init__(self):
    self.tbl = {}
    return

  def __contains__(self, k):
    # Different from (self.tbl in k) --
    # even if self.tbl[k] exists, it might be None.
    return self.tbl.get(k)

  def update(self, src):
    self.tbl.update(src.tbl)
    return

  def add(self, s, mora, allowconflict=False):
    if self.tbl.get(s) and not allowconflict:
      raise ValueError('%r (%r) is already defined: %r' %
                       (s, mora, self.tbl[s]))
    if ':' in s:
      (parselen, s) = (s.index(':'), s.replace(':',''))
    else:
      parselen = len(s)
    for i in range(len(s)):
      w = s[:i+1]
      if w == s:
        self.tbl[w] = (parselen, mora)
      elif w not in self.tbl:
        self.tbl[w] = None
    return
  
  def parse(self, s, i=0):
    while i < len(s):
      n = 1
      r = (1, s[i])
      while i+n <= len(s):
        w = zen2han(s[i:i+n]).lower()
        if w not in self.tbl: break
        x = self.tbl[w]
        if x:
          r = x
        n += 1
      (n, m) = r
      yield m
      i += n
    return

# GenTable
class GenTable(dict):

  def add(self, mora, s):
    if mora in self:
      raise ValueError('%r (%r) is already defined: %r' %
                       (mora, s, self[mora]))
    self[mora] = s
    return
    
  def generate(self, morae, addrule=False, nreduce=False):
    (m0,s0) = (None,'')
    for x in morae:
      if isinstance(x, Mora):
        assert x in self, 'Invalid mora: %r' % x
        (m1,s1) = (x, self[x])
      else:
        (m1,s1) = (None, x)
      if m0:
        if m0.mid == '.t':
          if addrule and s1[0] == 'c':
            s0 = 't'  # qT+"c" -> "tc"
          else:
            s0 = s1[0]
        elif m0.mid == '.n':
          if addrule and s1[0] == 'p':
            s0 = 'm'  # NN+"p" -> "mp"
          elif nreduce and (s1[0] not in 'auieon'):
            s0 = 'n'  # NN+C -> "n"+C
      yield s0
      (m0,s0) = (m1,s1)
    yield s0
    return


##  Initialization
##
MORA = {}
PARSE_OFFICIAL = ParseTable()
PARSE_OFFICIAL_ANNA = ParseTable()
PARSE_ENGLISH = ParseTable()
GEN_OFFICIAL = GenTable()
GEN_OFFICIAL_ANNA = GenTable()
GEN_ENGLISH = GenTable()
def initialize():
  NN = None
  for m in MORA_DATA:
    (mid, zenk, hank, zenh, p_off, p_eng) = m[:6]
    assert mid not in MORA
    assert isinstance(zenk, str)
    assert isinstance(hank, str)
    assert isinstance(zenh, str)
    mora = Mora(mid, zenk, hank, zenh)
    MORA[mid] = mora
    PARSE_OFFICIAL.add(zenk, mora, True)
    PARSE_OFFICIAL.add(hank, mora, True)
    PARSE_OFFICIAL.add(zenh, mora, True)
    PARSE_ENGLISH.add(zenk, mora, True)
    PARSE_ENGLISH.add(hank, mora, True)
    PARSE_ENGLISH.add(zenh, mora, True)
    for x in m[6:]:
      (c,k) = (ord(x[0])-48,x[1:])
      if c & 1:
        PARSE_OFFICIAL.add(k, mora)
      if c & 2:
        PARSE_ENGLISH.add(k, mora)
    if mid == '.n':
      NN = mora
    else:
      GEN_OFFICIAL.add(mora, p_off)
    GEN_ENGLISH.add(mora, p_eng)
  PARSE_OFFICIAL_ANNA.update(PARSE_OFFICIAL)
  PARSE_OFFICIAL.add('nn', NN)
  GEN_OFFICIAL_ANNA.update(GEN_OFFICIAL)
  GEN_OFFICIAL_ANNA.add(NN, "n'")
  GEN_OFFICIAL.add(NN, 'nn')
  return
initialize()


##  Aliases
##
def official2kana(s):
  return ''.join( str(m) for m in PARSE_OFFICIAL.parse(s) )
def official_anna2kana(s):
  return ''.join( str(m) for m in PARSE_OFFICIAL_ANNA.parse(s) )
def english2kana(s):
  return ''.join( str(m) for m in PARSE_ENGLISH.parse(s) )

def kana2official(s):
  return ''.join(GEN_OFFICIAL.generate(PARSE_OFFICIAL.parse(s)))
def kana2official_anna(s):
  return ''.join(GEN_OFFICIAL_ANNA.generate(PARSE_OFFICIAL.parse(s)))
def kana2english(s):
  return ''.join(GEN_ENGLISH.generate(PARSE_OFFICIAL.parse(s)))


# Test cases
if __name__ == '__main__':
  import unittest

  class TestRoma(unittest.TestCase):

    def checkParse(self, table, s, morae0):
      morae = [ isinstance(m,Mora) and m.mid for m in table.parse(s) ]
      self.assertEqual(morae0, morae)
      
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
                      ['so','.n','.a','!,','.a','.n','.a'])
      return
    def test_04_parse_official_nn2(self):
      self.checkParse(PARSE_OFFICIAL,
                      'sonnna,annna',
                      ['so','.n','na','!,','.a','.n','na'])
      return
    def test_05_parse_official_anna_nn1(self):
      self.checkParse(PARSE_OFFICIAL_ANNA,
                      'sonna,anna',
                      ['so','.n','na','!,','.a','.n','na'])
      return
    def test_05_parse_official_anna_nn2(self):
      self.checkParse(PARSE_OFFICIAL_ANNA,
                      'sonnna,annna',
                      ['so','.n','.n','na','!,','.a','.n','.n','na'])
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
                      ['.a','.i','.u','.e','.o'])
      return
    def test_07_parse_ignore(self):
      self.checkParse(PARSE_OFFICIAL,
                      u'ai$uεo',
                      ['.a','.i',False,'.u',False,'.o'])
      return

    def checkGen(self, table, morae, s0):
      s = ''.join(table.generate( MORA[x] for x in morae ))
      self.assertEqual(s0, s)
    def checkGenNReduce(self, table, morae, s0):
      s = ''.join(table.generate(( MORA[x] for x in morae ), nreduce=True))
      self.assertEqual(s0, s)
    def checkGenAddRule(self, table, morae, s0):
      s = ''.join(table.generate(( MORA[x] for x in morae ), addrule=True))
      self.assertEqual(s0, s)
    def checkGenRaw(self, table, morae, s0):
      s = ''.join(table.generate(morae))
      self.assertEqual(s0, s)

    def test_10_gen_basic_official(self):
      self.checkGen(GEN_OFFICIAL,
                    ['.a','ka','sa','ta','na'],
                    'akasatana')
    def test_11_gen_basic_official_anna(self):
      self.checkGen(GEN_OFFICIAL_ANNA,
                    ['.a','ka','sa','ta','na'],
                    'akasatana')
    def test_12_gen_basic_english(self):
      self.checkGen(GEN_ENGLISH,
                    ['.a','ka','sa','ta','na'],
                    'akasatana')
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
                    ['so','.n','.a','!,','.a','.n','.a'],
                    'sonna,anna')
    def test_15_gen_official_nn2(self):
      self.checkGen(GEN_OFFICIAL,
                    ['so','.n','na','!,','.a','.n','na'],
                    'sonnna,annna')
    def test_16_gen_official_nn_noreduce(self):
      self.checkGen(GEN_OFFICIAL,
                    ['so','.n','ka','!,','.a','.n','ka'],
                    'sonnka,annka')
    def test_16_gen_official_nn_reduce(self):
      self.checkGenNReduce(GEN_OFFICIAL,
                           ['so','.n','ka','!,','.a','.n','ka'],
                           'sonka,anka')
    def test_17_gen_official_anna_nn1(self):
      self.checkGen(GEN_OFFICIAL_ANNA,
                    ['so','.n','.a','!,','.a','.n','.a'],
                    "son'a,an'a")
    def test_17_gen_official_anna_nn2(self):
      self.checkGen(GEN_OFFICIAL_ANNA,
                    ['so','.n','na','!,','.a','.n','na'],
                    "son'na,an'na")
    def test_18_gen_official_anna_nn_noreduce(self):
      self.checkGen(GEN_OFFICIAL_ANNA,
                    ['so','.n','ka','!,','.a','.n','ka'],
                    "son'ka,an'ka")
    def test_18_gen_official_anna_nn_reduce(self):
      self.checkGenNReduce(GEN_OFFICIAL_ANNA,
                           ['so','.n','ka','!,','.a','.n','ka'],
                           'sonka,anka')
    def test_19_gen_official_addrule(self):
      self.checkGenAddRule(GEN_OFFICIAL,
                           ['ka','.n','pu'],
                           'kampu')
    def test_19_gen_english_addrule(self):
      self.checkGenAddRule(GEN_ENGLISH,
                           ['do','.t','ti','mo'],
                           'dotchimo')

    def test_20_gen_mixed(self):
      self.checkGenRaw(GEN_OFFICIAL,
                       [MORA['.a'], u'Ｉu', MORA['.e']],
                       u'aＩue')
      
    def checkKana2Official(self, kana, r0):
      roma = kana2official(kana)
      self.assertEqual(roma, r0)
    def checkOfficial2Kana(self, roma, k0):
      kana = official2kana(roma)
      self.assertEqual(kana, k0)

    def test_30_kana2official_basic1(self):
      self.checkKana2Official(u'ちょいとあんた、そんなこといってっけどさ',
                              u'tyoitoannta,sonnnakotoittekkedosa')
    def test_30_kana2official_basic2(self):
      self.checkKana2Official(u'にっちもさっちも。',
                              u'nittimosattimo.')
    def test_31_kana2official_mixed(self):
      self.checkKana2Official(u'ちょいとあんたソンナコトいってっけどサ。',
                              u'tyoitoanntasonnnakotoittekkedosa.')
    def test_32_kana2official_ignore(self):
      self.checkKana2Official(u'ちょいとあんた○１２３０そんなこといってっけどさ。',
                              u'tyoitoannta○１２３０sonnnakotoittekkedosa.')
    def test_33_official2kana_basic1(self):
      self.checkOfficial2Kana(u'choitoanta,sonnnakotoittekkedosa',
                              u'チョイトアンタ、ソンナコトイッテッケドサ')
    def test_33_official2kana_basic2(self):
      self.checkOfficial2Kana(u'nitchimosatchimo.',
                              u'ニッチモサッチモ。')
  
  unittest.main()
