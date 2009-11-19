from pyparsing import Literal, CaselessKeyword, CaselessLiteral, \
     Word, Optional, OneOrMore, Group, Combine, ZeroOrMore, nums, \
     Forward, StringEnd, restOfLine, alphas, alphanums, CharsNotIn, \
     MatchFirst, And, Or


def as_comma_separated_list(al):

    l = [al[0]]
    comma = Literal(",").suppress()

    for a1 in al[1:]:
        l.append(comma)
        l.append(a1)

    return And(l)


class wcs_shape(object):
    def __init__(self, *kl, **kw):
        self.args_list = kl
        self.args_repeat = kw.get("repeat", None)

    def get_pyparsing(self):
        return [a.parser for a in self.args_list]


def define_shape(name, shape_args, args_repeat=None):
    lparen = Literal("(").suppress()
    rparen = Literal(")").suppress()
    comma = Literal(",").suppress()

    shape_name = CaselessKeyword(name)


    if args_repeat is None:
        shape_with_parens = And([shape_name, lparen,
                                 as_comma_separated_list(shape_args),
                                 rparen])

        shape_with_spaces = shape_name + And(shape_args)

    else:
        n1, n2 = args_repeat
        sl = []

        ss = shape_args[:n1]
        if ss:
            sl.append(as_comma_separated_list(ss))

        ss = shape_args[n1:n2]
        if ss:
            ar = as_comma_separated_list(ss)
            if sl:
                sl.extend([comma+ ar, ZeroOrMore(comma + ar)])
            else:
                sl.extend([ar, ZeroOrMore(comma + ar)])

        ss = shape_args[n2:]
        if ss:
            if sl:
                sl.extend([comma, as_comma_separated_list(ss)])
            else:
                sl.extend([as_comma_separated_list(ss)])

        sl = [shape_name, lparen] + sl + [rparen]

        shape_with_parens = And(sl)

        shape_with_spaces = shape_name + OneOrMore(And(shape_args))


    return (shape_with_parens | shape_with_spaces)


def test_define_shape():
    args = [s.parser for s in [CoordOdd, CoordEven, Distance]]
    circle_parser = define_shape("circle", args, args_repeat=None)

    p = circle_parser.parseString("circle(1:2:3, 2:4:5, 3.)")
    assert p[0] == "circle"
    assert isinstance(p[1], CoordOdd.type)
    assert isinstance(p[2], CoordEven.type)

    args = [s.parser for s in [CoordEven]]
    circle_parser = define_shape("circle", args, args_repeat=None)

    p = circle_parser.parseString("circle(1:2:3)")
    p = circle_parser.parseString("circle(1d2m3s)")
    assert p[0] == "circle"
    assert isinstance(p[1], CoordEven.type)

    args = [s.parser for s in [CoordOdd, CoordEven, Distance, Distance]]
    ell_parser = define_shape("ell", args, args_repeat=(2,4))

    p = ell_parser.parseString("ell(1:2:2, 2:2:2, 3, 4, 5, 6)")
    assert p[0] == "ell"
    assert isinstance(p[1], CoordOdd.type)
    assert isinstance(p[2], CoordEven.type)

    args = [s.parser for s in [CoordOdd, CoordEven]]
    polygon_parser = define_shape("polygon", args, args_repeat=(0,2))
    p = polygon_parser.parseString("polygon(3:2:4.22, 3:3:4., 3:2:3, 3.2)")
    assert p[0] == "polygon"
    assert isinstance(p[-2], CoordOdd.type)
    assert isinstance(p[2], CoordEven.type)
    #assert isinstance(p[-1], float)


def define_shape_helper(shape_defs):
    l = []

    for n, args in shape_defs.items():
        s = define_shape(n,
                         args.get_pyparsing(),
                         args_repeat = args.args_repeat)

        l.append(s)

    return Or(l)



def define_expr(regionShape, negate_func):

    minus = Literal("-").suppress()
    regionExclude = (minus + regionShape).setParseAction(negate_func)
    regionExpr = (regionShape | regionExclude)

    return regionExpr


def define_line(atom,
                separator,
                comment):

    atomSeparator = separator.suppress()

    atomList = atom + ZeroOrMore(atomSeparator + atom)

    line = (atomList + Optional(comment)) | \
           comment

    return line




def comment_shell_like(comment_begin, parseAction=None):

    c = comment_begin + restOfLine
    if parseAction:
        c = c.setParseAction(parseAction)

    return c


def define_simple_literals(literal_list, parseAction=None):

    l = MatchFirst([CaselessKeyword(k) for k in literal_list])

    if parseAction:
        l = l.setParseAction(parseAction)

    return l


class Shape(object):

    def __init__(self, shape_name, shape_params):
        self.name = shape_name
        self.params = shape_params

        self.comment = None
        self.exclude = False
        self.continued = False
        
    def __repr__(self):
        params_string = ",".join(map(repr, self.params))
        if self.exclude:
            return "Shape : -%s ( %s )" %  (self.name, params_string)
        else:
            return "Shape : %s ( %s )" %  (self.name, params_string)

    def set_exclude(self):
        self.exclude = True


class Property(object):
    def __init__(self, text):
        self.text = text

    def __repr__(self):
        return "Property : " + repr(self.text)

class CoordCommand(Property):
    def __repr__(self):
        return "CoordCommand : " + repr(self.text)

class Global(Property):
    def __repr__(self):
        return "Global : " + repr(self.text)

class Comment(Property):
    def __repr__(self):
        return "Comment : " + repr(self.text)


class RegionPusher(object):
    def __init__(self):
        self.flush()

    def flush(self):
        self.stack = []
        self.comment = None
        self.continued = None
        
    def pushAtom(self, s, l, tok):
        self.stack.append(tok[-1])

    def pushComment(self, s, l, tok):
        self.comment  = tok[-1].strip()

    def set_continued(self, s, l, tok):
        self.continued = True

