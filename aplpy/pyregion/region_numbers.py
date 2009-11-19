
import pyparsing

from pyparsing import Literal, CaselessKeyword, CaselessLiteral, \
     Word, Optional, OneOrMore, Group, Combine, ZeroOrMore, nums, \
     Forward, StringEnd, restOfLine, alphas, alphanums, Empty, \
     Or


def _unsigned_simple_number():
    # fnumber : 102.43, 12304.3e10,
    #           .32???
    point = Literal( "." )
    e     = Literal("e") | Literal("E") #CaselessLiteral( "E" )
    fnumber = Combine( Word(nums) +
                       Optional( point + Optional( Word( nums ) ) ) +
                       Optional( e + Word( "+-"+nums, nums ) ) )

    return fnumber #.setParseAction(lambda s,l,t: (float(t[0]), t[0]))
    #return fnumber.leaveWhitespace().setParseAction(lambda s,l,t: [ float(t[0])])



#simple_number = _simple_number()

usn = _unsigned_simple_number()

def getSign(s, l, tok):
    if not tok: return (1, "")
    if tok[0] == "-":
        return -1, "-"
    else:
        return 1, "+"

def get_default(v):
    def _f(s, l, tok):
        if tok:
            return tok
        return v
    return _f

optional_sign = Optional(Literal("+") | Literal("-")).setParseAction(get_default(""))
#optional_sign = Optional(Literal("+") | Literal("-")) #.setParseAction(getSign)


class SimpleNumber(object):
    def __repr__(self):
        return "Number(%s)" % (self.text,)

    def __str__(self):
        return self.__repr__()

    def __init__(self, text):
        self.text = text
        self.v = float(text)



def _simple_number():
    s = Combine(optional_sign + usn)
    s.setParseAction(lambda s, l, tok: SimpleNumber(tok[0]))

    return s

simple_number = _simple_number()

def test_usn():
    for f in ["32.4", "0.23", "0.3e-7", "1.234e+7"]:
        assert usn.parseString(f)[0] == f
        #assert usn.parseString(f)[0][0] == float(f)



class SimpleInteger(object):
    def __repr__(self):
        return "Number(%s)" % (self.text,)

    def __str__(self):
        return self.__repr__()

    def __init__(self, text):
        self.text = text
        self.v = int(text)

def _unsigned_integer():
    s = Combine(Optional("+") + Word(nums))
    s.setParseAction(lambda s, l, tok: SimpleInteger(tok[0]))

    return s


simple_integer = _unsigned_integer()

def test_integer():
    for f in ["32", "+3"]:
        print simple_integer.parseString(f)

        assert usn.parseString(f)[0] == f
        #assert usn.parseString(f)[0][0] == float(f)


def get_degree(s, l, tok):
    pass


class Sixty(object):
    def __init__(self, sn, d, m, s):
        self.v = sn * (d +(m + s/60.)/60.)
        self.degree = self.v

class HMS(object):
    def __repr__(self):
        return "HMS(%s)" % (self.text,)

    def __init__(self, kl):
        self.text = "".join(kl)

        if kl[0] == "-":
            sn = -1
        else:
            sn = +1

        kkl = kl[1::2]
        if len(kkl) == 3:
            d, m, s = float(kl[1]), float(kl[3]), float(kl[5])
        elif len(kkl) == 2:
            d, m, s = float(kl[1]), float(kl[3]), 0.
        else:
            d, m, s = float(kl[1]), 0., 0.


        self.v = sn * (d +(m + s/60.)/60.)
        self.degree = self.v * 15


class DMS(object):
    def __repr__(self):
        return "DMS(%s)" % (self.text,)

    def __init__(self, kl):
        self.text = "".join(kl)

        if kl[0] == "-":
            sn = -1
        else:
            sn = +1

        kkl = kl[1::2]
        if len(kkl) == 3:
            d, m, s = float(kl[1]), float(kl[3]), float(kl[5])
        elif len(kkl) == 2:
            d, m, s = float(kl[1]), float(kl[3]), 0.
        else:
            d, m, s = float(kl[1]), 0., 0.


        self.v = sn * (d +(m + s/60.)/60.)
        self.degree = self.v



class AngularDistance(object):
    def __repr__(self):
        return "Ang(%s)" % (self.text,)

    def __init__(self, kl):
        self.text = "".join(kl)

        m, s = 0, 0
        if kl[1] == "'":
            m = float(kl[0])
            if len(kl) == 4:
                s = float(kl[2])
        else:
            s = float(kl[0])

        self.v = (m + s/60.)/60.
        self.degree = self.v


def _sexadecimal():
    colon = Literal(":")

    s = optional_sign + usn + colon + usn + \
        Optional(colon + usn)

        #Optional(colon + usn).setParseAction(get_default(0))

    #s = s.leaveWhitespace()

    return s

#sexadecimal = _sexadecimal()

sexadecimal60 = _sexadecimal().setParseAction(lambda s, l, tok: DMS(tok))
sexadecimal24 = _sexadecimal().setParseAction(lambda s, l, tok: HMS(tok))


def test_sexadecimal():
    s = sexadecimal60.parseString

    assert s("32:24:32.2")[0].v == Sixty(1, 32, 24, 32.2).v
    assert s("-32:24:32.2")[0].v == Sixty(-1, 32, 24, 32.2).v
    assert s("+32:24:32.2")[0].v == Sixty(1, 32, 24, 32.2).v



def _hms_number():
    _h = (usn + Literal("h")).leaveWhitespace()
    _m = (usn + Literal("m")).leaveWhitespace()
    _s = (usn + Literal("s")).leaveWhitespace()


    hms = optional_sign + _h + Optional(_m + Optional(_s))

    hms = hms.setParseAction(lambda s, l, tok: HMS(tok))

    return hms


def _dms_number():
    _d = (usn + Literal("d")).leaveWhitespace()
    _m = (usn + Literal("m")).leaveWhitespace()
    _s = (usn + Literal("s")).leaveWhitespace()


    dms = optional_sign + _d + Optional(_m + Optional(_s))

    dms = dms.setParseAction(lambda s, l, tok: DMS(tok))

    return dms


    #zzz = Empty().setParseAction(lambda s, l, tok: 0)


    #_hms = optional_sign + Or([_h + Optional(_m).setParseAction(get_default(0)) \
    #                           + Optional(_s).setParseAction(get_default(0)),
    #                           zzz + _m + Optional(_s).setParseAction(get_default(0)),
    #                           zzz + zzz + _s])

    #_hms = _hms.leaveWhitespace()



hms_number = _hms_number()
dms_number = _dms_number()


def test_hms():
    s = hms_number.parseString

    assert s("32h24m32.2s")[0].v == Sixty(1, 32, 24, 32.2).v
    assert s("0h24m32.2s")[0].v == Sixty(1, 0, 24, 32.2).v
    #assert s("32m")[0].v == HMS(1, 0, 32, 0).v
    assert s("32h")[0].v == Sixty(1, 32, 0, 0).v



# def _dms_number():
#     _d = (usn + Literal("d")).leaveWhitespace()
#     _m = (usn + Literal("m")).leaveWhitespace()
#     _s = (usn + Literal("s")).leaveWhitespace()

#     zzz = Empty().setParseAction(lambda s, l, tok: 0)

#     _dms = optional_sign + Or([_d + Optional(_m).setParseAction(get_default(0)) + Optional(_s).setParseAction(get_default(0)),
#                                zzz + _m + Optional(_s).setParseAction(get_default(0)),
#                                zzz + zzz + _s])

#     #_hms = _hms.leaveWhitespace()
#     dms = _dms.setParseAction(lambda s, l, tok: DMS(*tok))

#     return dms



def test_dms():
    s = dms_number.parseString

    assert s("32d24m32.2s")[0].v == Sixty(1, 32, 24, 32.2).v
    assert s("-32d24m32.2s")[0].v == Sixty(-1, 32, 24, 32.2).v
    #assert s("-24m32.2s")[0].v == DMS(-1, 0, 24, 32.2).v
    #assert s("32m")[0].v == DMS(1, 0, 32, 0).v
    assert s("32d")[0].v == Sixty(1, 32, 0, 0).v



def _angular_distance():
    _m = (usn + Literal("\'")).leaveWhitespace()
    _s = (usn + Literal("\"")).leaveWhitespace()

    ms = Or([ _m + Optional(_s),
               _s])

    #_hms = _hms.leaveWhitespace()
    ms = ms.setParseAction(lambda s, l, tok: AngularDistance(tok))

    return ms


angular_distance = _angular_distance()

def test_ang_distance():
    s = angular_distance.parseString

    assert s("32.3'")[0].v == Sixty(1, 0, 32.3, 0.).v
    assert s("32\'24\"")[0].v == Sixty(1, 0, 32, 24).v





class Arg(object):
    def __init__(self, type, parser):
        self.type = type
        self.parser = parser


class CoordOdd:
    parser = (hms_number | sexadecimal24 | simple_number)
    type = HMS

class CoordEven:
    parser = (dms_number | sexadecimal60 | simple_number)
    type = DMS

class Distance:
    parser = (angular_distance | simple_number)
    type = AngularDistance

class Angle:
    parser = (simple_number)
    type = simple_number

class Integer:
    parser = simple_integer
    type = simple_number


# CoordOdd = Arg(type=HMS,
#                parser=(hms_number | sexadecimal24 | simple_number)
#                )

# CoordEven = Arg(type=DMS,
#                 parser=(dms_number | sexadecimal60 | simple_number)
#                 )

# Distance = Arg(type=AngularDistance,
#                parser=(angular_distance | simple_number)
#                )

# Angle = Arg(type=float,
#             parser=(simple_number)
#             )



def test_coord_odd():
    s = CoordOdd.parser.parseString

    assert s("32h24m32.2s")[0].v == HMS(1, 32, 24, 32.2).v
    assert s("32:24:32.2s")[0].v == HMS(1, 32, 24, 32.2).v
    assert s("32.24")[0] == 32.24

    s1 = s("32:24:32.2s")[0]
    assert isinstance(s1, HMS)
