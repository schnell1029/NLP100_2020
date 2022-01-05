import re

import pandas as pd

def ex20(file_name="jawiki-country.json"):
  """titleがイギリスのデータの本文を表示"""
  df = pd.read_json(file_name, lines=True)
  uk = df.query("title=='イギリス'")["text"].values[0]
  print(uk)
  return

def ex21(file_name="jawiki-country.json"):
  """カテゴリ名を宣言している行を抽出"""
  df = pd.read_json(file_name, lines=True)
  uk_text = df.query("title=='イギリス'")["text"].values[0]

  pattern = re.compile(r"^.*\[Category.*$", re.MULTILINE)
  res = pattern.findall(uk_text)
  [print(m) for m in res]
  return

def ex22(file_name="jawiki-country.json"):
  """カテゴリ名を抽出"""
  df = pd.read_json(file_name, lines=True)
  text = df.query("title=='イギリス'")["text"].values[0]
  # グループ1にカテゴリ、グループ2にNoneまたは"|.*"をマッチさせるという方針で
  pattern = re.compile(r"\[\[Category:(.*?)(|\|.*)\]\]")
  res = pattern.findall(text)
  [print(g[0]) for g in res]
  return

def ex23(file_name="jawiki-country.json"):
  """セクション名とそのレベルを表示

  例) レベル1
    ==セクション名==
  例) レベル2
    ===セクション名===
  """
  df = pd.read_json(file_name, lines=True)
  text = df.query("title=='イギリス'")["text"].values[0]

  pattern = re.compile(r"(={2,})\s*(.+?)\s*(\1)")
  res = pattern.findall(text)
  for match in res:
    level = len(match[0]) - 1
    prefix = "  "*level + str(level)
    print(prefix + match[1])
  return

def ex24(file_name="jawiki-country.json"):
  """記事から参照されているメディアファイルを全て抜き出す

  例)
    [[ファイル:Royal Coat of Arms of the United Kingdom.svg|85px|イギリスの国章]]
  """
  df = pd.read_json(file_name, lines=True)
  text = df.query("title=='イギリス'")["text"].values[0]

  pattern = re.compile(r"\[\[ファイル:(.+?)\|")
  res = pattern.findall(text)
  [print(item) for item in res]
  return

def ex25(file_name="jawiki-country.json"):
  """基礎情報テンプレートのフィールド名と値を抽出し、辞書オブジェクトとして格納

  例)
    [[ファイル:Royal Coat of Arms of the United Kingdom.svg|85px|イギリスの国章]]
  """
  df = pd.read_json(file_name, lines=True)
  text = df.query("title=='イギリス'")["text"].values[0]

  pattern = re.compile(r"\{\{基礎情報.*?\n(.*?)\n\}\}", re.DOTALL)
  res = pattern.findall(text)

  pattern = re.compile(r"\|(.+)\s=(.+)\n")
  res = pattern.findall(res[0])
  res = {key: value for key, value in res}
  return res

def ex26(file_name="jawiki-country.json"):
  """強調マークアップの除去

  例)
    ''弱い強調''
    '''強調'''
    '''''強い強調'''''
  """
  dic = ex25()

  pattern = re.compile(r"\'{2,5}")
  res = {key: pattern.sub("", value) for key, value in dic.items()}
  return res