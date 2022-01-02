import re
import random
from typing import Any, List

def ex00(s: str) -> str:
  """入力単語を逆順に"""
  return s[::-1]

def ex01(s: str) -> str:
  """奇数文字目を抜き出し(0-indexとする)"""
  return s[1::2]

def ex02(s1: str, s2: str) -> str:
  """二つの引数を交互に連結"""
  return "".join([f+s for f, s in zip(s1, s2)])

def ex03(s: str) -> str:
  """英文を単語に分解し各単語の文字数を先頭から出現順に並べたリストを作成"""
  word_list = re.sub(r"[.,]", "", s.strip()).split(" ")
  return list(map(len, word_list))

def ex04(s:str)->str:
  """元素記号をこねくり回す"""
  s = s.strip().split(" ")
  one = [1, 5, 6, 7, 8, 9, 15, 16, 19]
  key = [v[:1] if i+1 in one else v[:2] for i,v in enumerate(s)]
  return {k: v+1 for k,v in zip(key, range(len(key)))}

def ex05(s:str, n:int=2)->List:
  """一要素ずつずらしてタプルを作成するという方針で"""
  return list(zip(*[s[i:] for i in range(2)]))

def ex06(s1:str, s2:str):
  """集合演算"""
  X = set(ex05(s1))
  Y = set(ex05(s2))
  print(f"和集合: {X|Y}")
  print(f"積集合: {X&Y}")
  print(f"差集合: {X-Y}")
  print('Xにseが含まれるか:', {('s', 'e')} <= X)
  print('Yにseが含まれるか:', {('s', 'e')} <= Y)

def ex07(x,y,z)->str:
  return f"{x}時の{y}は{z}"

def ex08(s:str)->str:
  """英小文字をUnicodeの整数値によって置換
  英小文字はUnicodeにおいて[97, 122]なのでex08を2回通せば元の文に戻る"""
  s = [chr(219-ord(v)) if v.islower() else v for v in s]
  return "".join(s)

def ex09(words: str) -> str:
  """先頭末尾以外の文字をシャッフル"""
  def shuffle(word: str) -> str:
    if len(word) > 4:
      res = word[0] + "".join(random.sample(word[1:-1], len(word)-2)) \
                    + word[len(word)-1]
    else:
      res = word
    return res
  return " ".join(map(shuffle, words.split()))