# -*- coding: utf-8 -*-

from babel.messages import jslexer


"""
The test below tests the unquote_string function, which should remove quoted
from strings. It tests that the function works for quotes without content '""'.
It also tests that it should work for unicode escaped characters. It does not
test that the function works for regular escaped characters.
"""
def test_unquote():
    assert jslexer.unquote_string('""') == ''
    assert jslexer.unquote_string(r'"h\u00ebllo"') == u"hëllo"

"""
We add a test where we should enter the branch which handles normal escaped 
characters.
"""
def test_unquote_extended():
    assert jslexer.unquote_string('"ja\\bha"') == "ja\bha"


"""
The tests below tests the tokenize function, which given a javaScript code 
snippet should divide it up into tokens. The tests covers a range of cases, but
does not cover any case where the indicates_division property is used.
"""
def test_dollar_in_identifier():
    assert list(jslexer.tokenize('dollar$dollar')) == [('name', 'dollar$dollar', 1)]


def test_dotted_name():
    assert list(jslexer.tokenize("foo.bar(quux)", dotted=True)) == [
        ('name', 'foo.bar', 1),
        ('operator', '(', 1),
        ('name', 'quux', 1),
        ('operator', ')', 1)
    ]


def test_dotted_name_end():
    assert list(jslexer.tokenize("foo.bar", dotted=True)) == [
        ('name', 'foo.bar', 1),
    ]


def test_template_string():
    assert list(jslexer.tokenize("gettext `foo\"bar\"p`", template_string=True)) == [
        ('name', 'gettext', 1),
        ('template_string', '`foo"bar"p`', 1)
    ]


def test_jsx():
    assert list(jslexer.tokenize("""
         <option value="val1">{ i18n._('String1') }</option>
         <option value="val2">{ i18n._('String 2') }</option>
         <option value="val3">{ i18n._('String 3') }</option>
         <component value={i18n._('String 4')} />
         <comp2 prop={<comp3 />} data={{active: true}}>
             <btn text={ i18n._('String 5') } />
         </comp2>
    """, jsx=True)) == [
        ('jsx_tag', '<option', 2),
        ('name', 'value', 2),
        ('operator', '=', 2),
        ('string', '"val1"', 2),
        ('operator', '>', 2),
        ('operator', '{', 2),
        ('name', 'i18n._', 2),
        ('operator', '(', 2),
        ('string', "'String1'", 2),
        ('operator', ')', 2),
        ('operator', '}', 2),
        ('jsx_tag', '</option', 2),
        ('operator', '>', 2),
        ('jsx_tag', '<option', 3),
        ('name', 'value', 3),
        ('operator', '=', 3),
        ('string', '"val2"', 3),
        ('operator', '>', 3),
        ('operator', '{', 3),
        ('name', 'i18n._', 3),
        ('operator', '(', 3),
        ('string', "'String 2'", 3),
        ('operator', ')', 3),
        ('operator', '}', 3),
        ('jsx_tag', '</option', 3),
        ('operator', '>', 3),
        ('jsx_tag', '<option', 4),
        ('name', 'value', 4),
        ('operator', '=', 4),
        ('string', '"val3"', 4),
        ('operator', '>', 4),
        ('operator', '{', 4),
        ('name', 'i18n._', 4),
        ('operator', '(', 4),
        ('string', "'String 3'", 4),
        ('operator', ')', 4),
        ('operator', '}', 4),
        ('jsx_tag', '</option', 4),
        ('operator', '>', 4),
        ('jsx_tag', '<component', 5),
        ('name', 'value', 5),
        ('operator', '=', 5),
        ('operator', '{', 5),
        ('name', 'i18n._', 5),
        ('operator', '(', 5),
        ('string', "'String 4'", 5),
        ('operator', ')', 5),
        ('operator', '}', 5),
        ('jsx_tag', '/>', 5),
        ('jsx_tag', '<comp2', 6),
        ('name', 'prop', 6),
        ('operator', '=', 6),
        ('operator', '{', 6),
        ('jsx_tag', '<comp3', 6),
        ('jsx_tag', '/>', 6),
        ('operator', '}', 6),
        ('name', 'data', 6),
        ('operator', '=', 6),
        ('operator', '{', 6),
        ('operator', '{', 6),
        ('name', 'active', 6),
        ('operator', ':', 6),
        ('name', 'true', 6),
        ('operator', '}', 6),
        ('operator', '}', 6),
        ('operator', '>', 6),
        ('jsx_tag', '<btn', 7),
        ('name', 'text', 7),
        ('operator', '=', 7),
        ('operator', '{', 7),
        ('name', 'i18n._', 7),
        ('operator', '(', 7),
        ('string', "'String 5'", 7),
        ('operator', ')', 7),
        ('operator', '}', 7),
        ('jsx_tag', '/>', 7),
        ('jsx_tag', '</comp2', 8),
        ('operator', '>', 8)
    ]

"""
The test below covers a case where the "indicates_division" property is used.
"""
def test_template_string():
    result = list(jslexer.tokenize("val x = (3+4)/7", template_string=True))
    assert result == [                                                                               
        ('name', 'val', 1),                                       
        ('name', 'x', 1),                                         
        ('operator', '=', 1),                                     
        ('operator', '(', 1),                                     
        ('name', '3', 1),                                         
        ('operator', '+', 1),                                     
        ('name', '4', 1),                                         
        ('operator', ')', 1),                                     
        ('operator', '/', 1),                                     
        ('name', '7', 1)                                          
    ]                    
