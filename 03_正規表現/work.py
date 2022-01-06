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

def ex27(file_name="jawiki-country.json"):
  """内部リンクの除去

  例)
    [[記事名]]
    [[記事名|表示文字]]
    [[記事名#節名|表示文字]]
  """
  dic = ex26()

  pattern = re.compile(r"\[\[(.+\||)(.+?)\]\]")
  res = {key: pattern.sub(r"\2", value) for key, value in dic.items()}
  return res

def ex28(file_name="jawiki-country.json"):
  """MediaWikiマークアップの除去"""
  dic = ex27()

  def remove_mk(text):
    pattern1 = re.compile(r"\[\[(.+\||)(.+?)\]\]")
    pattern2 = re.compile(r"<\s*?/*?\s*?br\s*?/*?\s*>")
    text = pattern1.sub(r"\2", text)
    text = pattern2.sub("", text)
    return text

  res = {key: remove_mk(value) for key, value in dic.items()}
  return res

def ex25_28(file_name="jawiki-country.json"):
  df = pd.read_json(file_name, lines=True)
  text = df.query("title=='イギリス'")["text"].values[0]

  # 基礎情報が書かれているブロックを抜き出し
  pattern = re.compile(r"\{\{基礎情報.*?\n(.*?)\n\}\}", re.DOTALL)
  text = pattern.search(text)[1]

  # 各フィールドの境目は"\n|"先頭に改行記号を与えれば場合分け不要
  pattern = re.compile(r"\n\|")
  templates = pattern.split("\n"+text)

  # フィールド名と値を抽出
  pattern = re.compile(r"\s+=\s*")
  templates = dict(tuple(pattern.split(template)) for template in templates[1:])

  def remove_mk(text: str) -> str:
    # 強調マークアップを除去
    r1 = re.compile(r"\'{2,5}")
    text = r1.sub("", text)

    # 内部リンクの除去(ゴリ押し)
    r2 = re.compile(r"\[\[([\w\s():,・]+?\||)(.+?)\]\]")
    text = r2.sub(r"\2", text)

    # MediaWikiマークアップの除去Permalink
    r3 = re.compile(r"\{\{(.+\||)(.+?)\}\}")
    text = r3.sub(r"\2", text)
    r4 = re.compile(r"<\s*?/*?\s*?br\s*?/*?\s*>")
    text = r4.sub("", text)
    r5 = re.compile(r"<ref.*((</ref>)|(/>))", re.DOTALL)
    text = r5.sub("", text)
    return text

  templates = {k: remove_mk(v) for k, v in templates.items()}
  return templates

import requests
def ex29(file_name="jawiki-country.json"):
  templates = ex25_28()
  file_url = templates["国旗画像"].replace(" ", "_")
  url = f'https://commons.wikimedia.org/w/api.php?action=query&titles=File:{file_url}&prop=imageinfo&iiprop=url&format=json'
  data = requests.get(url)
  return re.search(r'"url":"(.+?)"', data.text).group(1)