import re
import json

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
  uk = df.query("title=='イギリス'")["text"].values[0]
  uk = uk.split("\n")
  ans = list(filter(lambda x: "Category:" in x, uk))
  print(ans)