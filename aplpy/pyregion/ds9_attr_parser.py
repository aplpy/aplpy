import copy

from pyparsing import Literal, CaselessKeyword, CaselessLiteral, \
     Word, Optional, OneOrMore, Group, Combine, ZeroOrMore, nums, \
     Forward, StringEnd, restOfLine, alphas, alphanums, CharsNotIn, \
     MatchFirst, And, Or, quotedString, QuotedString

from region_numbers import CoordOdd, CoordEven, Distance, Angle

from parser_helper import as_comma_separated_list, wcs_shape, \
     define_shape, define_shape_helper, define_expr, define_line, \
     comment_shell_like, define_simple_literals, \
     Shape

def get_ds9_attr_parser():
    lhs = Word(alphas)
    paren = QuotedString("(",endQuoteChar=")")
    rhs = Or([Word(alphas+nums),
              quotedString,
              QuotedString("{",endQuoteChar="}"),
              paren + ZeroOrMore(paren),
              Word(nums+" "),
              Word(nums+".")
              ])
    expr = lhs + Optional(Literal("=").suppress() + rhs)
    expr.setParseAction(lambda s, l, tok: tuple(tok))

    return ZeroOrMore(expr)



class Ds9AttrParser(object):
    def set_continued(self):
        self.continued = True
        
    def __init__(self):
        self.continued = False

        ds9_attr_parser = get_ds9_attr_parser()

        ds9_shape_in_comment_defs = dict(text=wcs_shape(CoordOdd, CoordEven),
                                         vector=wcs_shape(CoordOdd, CoordEven,
                                                          Distance, Angle),
                                         composite=wcs_shape(CoordOdd, CoordEven, Angle),
                                         )
        regionShape = define_shape_helper(ds9_shape_in_comment_defs)
        regionShape = regionShape.setParseAction(lambda s, l, tok: Shape(tok[0], tok[1:]))


        self.parser_default = ds9_attr_parser

        cont = CaselessKeyword("||").setParseAction(self.set_continued).suppress()
        line = Optional(And([regionShape,
                             Optional(cont)])) \
                             + ds9_attr_parser

        self.parser_with_shape = line


    def parse_default(self, s):
        return self.parser_default.parseString(s)

    def parse_check_shape(self, s):
        l = self.parser_with_shape.parseString(s)
        if l and isinstance(l[0], Shape):
            if self.continued:
                l[0].continued = True
            return l[0], l[1:]
        else:
            return None, l



def get_attr(attr_list, global_attrs):
    local_attr = [], {}
    for kv in attr_list:
        if len(kv) == 1:
            local_attr[0].append(kv[0])
        elif len(kv) == 2:
            local_attr[1][kv[0]] = kv[1]
        elif len(kv) > 2:
            local_attr[1][kv[0]] = kv[1:]

    attr0 = copy.copy(global_attrs[0])
    attr1 = copy.copy(global_attrs[1])

    if local_attr[0]:
        attr0.extend(local_attr[0])

    if local_attr[1]:
        attr1.update(local_attr[1])

    return attr0, attr1






def test_attr():

    p = get_ds9_attr_parser()
    assert  p.parseString("color = green")[0] == ("color", "green")
    assert  p.parseString("font=\"123 123\"")[0] == ("font", '"123 123"')
    assert  p.parseString("color")[0] == ("color",)
    assert  p.parseString("tag={group 1}")[0] == ("tag","group 1")

if __name__ == "__main__":
    p = get_ds9_attr_parser()
    s = 'color=green dashlist= 8 4 font="helvetica 10 normal" tag={group 1} select=1 source panda=(1 3 2)(2 3 4)'
    #s = 'dashlist= 8 4 font=1'
    ss = p.parseString(s)
    print ss
