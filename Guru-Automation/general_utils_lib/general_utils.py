import random, traceback

# remove annoying characters
bad_chars = {
    '\xc2\x82' : ',',        # High code comma
    '\xc2\x84' : ',,',       # High code double comma
    '\xc2\x85' : '...',      # Tripple dot
    '\xc2\x88' : '^',        # High carat
    '\xc2\x91' : '\x27',     # Forward single quote
    '\xc2\x92' : '\x27',     # Reverse single quote
    '\xc2\x93' : '\x22',     # Forward double quote
    '\xc2\x94' : '\x22',     # Reverse double quote
    '\xc2\x95' : ' ',
    '\xc2\x96' : '-',        # High hyphen
    '\xc2\x97' : '--',       # Double hyphen
    '\xc2\x99' : ' ',
    '\xc2\xa0' : ' ',
    '\xc2\xa6' : '|',        # Split vertical bar
    '\xc2\xab' : '<<',       # Double less than
    '\xc2\xbb' : '>>',       # Double greater than
    '\xc2\xbc' : '1/4',      # one quarter
    '\xc2\xbd' : '1/2',      # one half
    '\xc2\xbe' : '3/4',      # three quarters
    '\xca\xbf' : '\x27',     # c-single quote
    '\xcc\xa8' : '',         # modifier - under curve
    '\xcc\xb1' : ''          # modifier - under line
}

def replace_bad_chars(match):
    char = match.group(0)
    return bad_chars[char]

def randomName(capitalize=True):
    bits=[]
    vowels="aeiou"
    letters="abcdefghijklmnopqrstuvwxyz"
    for ch in letters:
        for v in vowels:
            bits.append(ch+v)
    bits.remove("fu")
    bits.remove("hi")
    bits.remove("cu")
    bits.remove("co")
    bits.remove("mo")
    word=""
    rnd=len(bits)-1
    numOfBits=random.randint(2,3)
    for i in range(0,numOfBits):
        word=word+bits[random.randint(1,rnd)]
    word=word+letters[random.randrange(0,25)]
    if (capitalize==True):
        word=word.capitalize()
    return word

