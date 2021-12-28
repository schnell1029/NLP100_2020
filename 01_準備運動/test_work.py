import sys
sys.path.append('.')

from work import *

def test_ex00():
  arg = "stressed"
  expected = "desserts"
  assert ex00(arg) == expected

def test_ex01():
  arg = "パタトクカシーー"
  expected = "タクシー"
  assert ex01(arg) == expected

def test_ex02():
  arg1 = "パトカー"
  arg2 = "タクシー"
  expected = "パタトクカシーー"
  assert ex02(arg1, arg2) == expected

def test_ex03():
  arg = """
Now I need a drink, alcoholic of course, \
after the heavy lectures involving quantum mechanics.
"""
  expected = list(map(lambda x: int(x), "314159265358979"))
  assert ex03(arg) == expected

def test_ex04():
  arg = """
Hi He Lied Because Boron Could Not Oxidize Fluorine. \
New Nations Might Also Sign Peace Security Clause. Arthur King Can.
""".strip()
  expected = {'H': 1, 'He': 2, 'Li': 3, 'Be': 4, 'B': 5, 'C': 6, 'N': 7,
    'O': 8, 'F': 9, 'Ne': 10, 'Na': 11, 'Mi': 12, 'Al': 13, 'Si': 14, 'P': 15,
    'S': 16, 'Cl': 17, 'Ar': 18, 'K': 19, 'Ca': 20}
  assert ex04(arg) == expected

def test_ex05():
  arg = "I am an NLPer"
  expected = [('I', ' '), (' ', 'a'), ('a', 'm'), ('m', ' '), (' ', 'a'),
              ('a', 'n'), ('n', ' '), (' ', 'N'), ('N', 'L'), ('L', 'P'),
              ('P', 'e'), ('e', 'r')]
  assert ex05(arg) == expected
  expected = [('I', 'am'), ('am', 'an'), ('an', 'NLPer')]
  assert ex05(arg.split()) == expected