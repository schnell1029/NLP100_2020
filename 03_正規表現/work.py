import re
import json
from typing import List

import pandas as pd

def ex20(file_name="jawiki-country.json"):
  """titleがイギリスのデータの本文を表示"""
  df = pd.read_json(file_name, lines=True)
  uk = df.query("title=='イギリス'")["text"].values[0]
  print(uk)
  return

def ex21(file_name="jawiki-country.json")->List:
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
  return