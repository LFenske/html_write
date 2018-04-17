#!/usr/bin/env python2

class html_write():
    
    HTML_4_01_STRICT = "HTML 4.01 Strict"
    HTML_5_0         = "HTML 5.0"
    XHTML_1_0_STRICT = "XHTML 1.0 Strict"
    XHTML_1_1        = "XHTML 1.1"
    #doctype = HTML_4_01_STRICT
    #doctype = HTML_5_0
    #doctype = XHTML_1_0_STRICT
    #doctype = XHTML_1_1
    
    tags_no_close = {
        HTML_4_01_STRICT: set(("meta",)),
        HTML_5_0        : set(("meta",)),
        XHTML_1_0_STRICT: set(),
        XHTML_1_1       : set(),
        }
    tags_inline = set(("i", "b", "u", "em"))
    self_close_ok = set((
        HTML_5_0        ,
        XHTML_1_0_STRICT,
        XHTML_1_1       ,
        ))
    initial = {
        HTML_4_01_STRICT:
            """<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01//EN">
""",
        HTML_5_0:
            """<!DOCTYPE html>
""",
        XHTML_1_0_STRICT:
            """<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN"
"http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
""",
        XHTML_1_1:
            """<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN"
"http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
""",
        }
    attrs_html = {
        HTML_4_01_STRICT: [],
        HTML_5_0        : [("lang", "EN")],
        XHTML_1_0_STRICT: [("xmlns", "http://www.w3.org/1999/xhtml")],
        XHTML_1_1       : [("xmlns", "http://www.w3.org/1999/xhtml")],
        }
    
    def __init__(self, doctype=XHTML_1_1, indent_size=4):
        self.doctype = doctype
        self.indent_size = indent_size
        
    def make_html(self, page, indent=0):
        res = ""
        indstr = " "*indent
        if type(page) is type(()):
            p = list(page); p.append([]); p.append([])  # Ensure at least 3 items.
            attr = html_write.make_attr(p[2])
            no_end = p[0] in html_write.tags_no_close[self.doctype]
            self_close = not p[1] and self.doctype in html_write.self_close_ok
            if self_close:
                res += indstr+"<"+page[0]+attr+" />\n"
            else:
                res += indstr+"<"+p[0]+attr+">\n"
                res += self.make_html(p[1], indent+self.indent_size)
                if not no_end:
                    res += indstr+"</"+p[0]+">\n"
        elif type(page) is type([]):
            for c in page:
                res += self.make_html(c, indent)
        elif type(page) is type(""):
            res += indstr+page+"\n"
        else:
            error("unhandled type:", type(page))
        return res
    
    @staticmethod
    def make_attr(l):
        res = ""
        for a in l:
            res += ' '+a[0]+'="'+a[1]+'"'
        return res


if __name__ == "__main__":
    hw = html_write()
    page = ("html", [], html_write.attrs_html[hw.doctype])
    head = ("head", [], [])
    head[1].append(("title", "No Title"))
    head[1].append(("meta", [], [("http-equiv","Content-Type"), ("content","text/html; charset=utf-8")]))
    body = ("body", [], [])
    page[1].append(head)
    page[1].append(body)
    
    body[1].append(("h3", ["Hello,", ("i", "World!")]))
    body[1].append(("p", ["Embedded ", ("i", "Italics"), "Test"]))
    
    table = ("table", [])
    tr = ("tr", [])
    tr[1].append(("td", "&nbsp;"))
    tr[1].append(("td", ("b", "head1")))
    tr[1].append(("td", ("b", "head2")))
    table[1].append(tr)
    tr = ("tr", [])
    tr[1].append(("td", "row1"))
    tr[1].append(("td", "value11"))
    tr[1].append(("td", "value12"))
    table[1].append(tr)
    tr = ("tr", [])
    tr[1].append(("td", "row2"))
    tr[1].append(("td", "value21"))
    tr[1].append(("td", "value22"))
    table[1].append(tr)
    
    body[1].append(table)
    
    #print(page)
    html = html_write.initial[hw.doctype] + hw.make_html(page)
    print(html)
