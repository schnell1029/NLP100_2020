import collections
from os import sep
import subprocess
import re
from collections import deque

import pandas as pd

def ex10(file_name:str="popular-names.txt")->str:
  """ファイルの行数を表示"""
  res = subprocess.check_output(("wc", "-l", "popular-names.txt")).split()[0]
  line_num_unix = int(res)
  with open(file_name) as file:
    line_num_python = len([1 for _ in file])
    assert line_num_python == line_num_unix
    return line_num_python

def ex11(file_name:str="popular-names.txt"):
  """tabをスペースに置換"""
  # sed "s/\t/ /g" popular-names.txt >> ex11.txt
  with open(file_name) as file, open("ex11.txt", "w") as fout:
    for line in file:
      line = re.sub(r"\t", " ", line)
      fout.write(line)

def ex12(file_name:str="popular-names.txt"):
  """カラムの抜き出し

  Unixコマンドでの処理:
    cut -f 1 popular-names.txt >> col1_cut.txt
    cut -f 2 popular-names.txt >> col2_cut.txt
  """
  # デフォルトだと0行目をheader行として認識するのでNoneを渡して防止する
  df = pd.read_csv(file_name, delimiter="\t", header=None)

  # header行やindex列を書き込まないようにパラメタを渡している
  # columnsに値を渡さなくてもdf[0]とかすればカラムの切り出しができる
  df.to_csv(path_or_buf="col1.txt", sep="\t", columns=[0],
            header=False, index=False)
  df.to_csv(path_or_buf="col2.txt", sep="\t", columns=[1],
            header=False, index=False)

def ex13():
  """カラムの結合

  Unixコマンドでの処理
    paste -d"\t" col1.txt col2.txt > col1-2_paste.txt
  """
  with open("col1.txt") as f1, open("col2.txt") as f2, \
       open("col1-2.txt", "w") as fout:
    for col1, col2 in zip(f1, f2):
      fout.write(col1.strip() + "\t" + col2)

def ex13_pd():
  """ex13のpandasによる実装"""
  df1=pd.read_table("col1.txt", header=None)
  df2=pd.read_table("col2.txt", header=None)
  # df1.shape -> (2780, 1)
  # axis=0なら要素数2780の方の次元で連結する, axis=1なら要素数1の方の次元で連結する(超大切)
  df = pd.concat([df1, df2], axis=1)
  df.to_csv(path_or_buf="col1-2.txt", sep="\t", header=False, index=False)

def ex14(n:int=10, file_name:str="popular-names.txt"):
  """ファイルの先頭N行を表示

  Unixコマンドでの処理
    head -nN popular-names.txt
  """
  with open(file_name) as file:
    for i in range(n):
      print(file.readline().strip())

def ex14_pd(n:int=10, file_name:str="popular-names.txt"):
  """ex14のpandasによる実装"""
  df = pd.read_csv(file_name, delimiter="\t", header=None)
  print(df.head(n))

def ex15(n:int=10, file_name:str="popular-names.txt"):
  """ファイルの末尾N行を出力

  Unixコマンドでの処理
    tail -nN popular-names.txt
  """
  q = deque([], n)
  with open(file_name) as file:
    [q.append(line) for line in file]
    [print(line.strip()) for line in q]

def ex15_pd(n:int=10, file_name:str="popular-names.txt"):
  """ex15のpandasによる実装"""
  df = pd.read_csv(file_name, delimiter="\t", header=None)
  print(df.tail(10))

def ex16(N:int=10, file_name:str="popular-names.txt"):
  """ファイルをN分割

  Unixコマンドによる処理
    N="分割数"
    n=`wc -l popular-names.txt | awk '{print $1}'`
    ln=`expr $n / $N + 1`
    split -l $ln popular-names.txt
  """
  # 行数を取得
  line_count = 0
  with open(file_name) as file:
    line_count = len([1 for _ in file])
  ln = line_count // N + 1

  with open(file_name) as file:
    for prefix in range(N):
      with open(f"{prefix}_splited.txt", "w") as fout:
        for _ in range(ln):
          fout.write(file.readline())
  return

def ex17(file_name:str="popular-names.txt"):
  """1列目の要素集合を求める

  Unixコマンドによる処理
    cut -f 1 popular-names.txt | sort | uniq
  """
  with open(file_name) as file:
    names = set(row.strip().split()[0] for row in file)
    # 目的は上の時点で達成しているがsetは表示順が毎回異なりソート不可なので
    names = sorted(list(names))
    print(*names, sep="\n")
  return

def ex17_pd(file_name:str="popular-names.txt"):
  """ex17のpandasを用いた回答"""
  df = pd.read_csv(file_name, sep="\t", header=None)
  names = sorted(df[0].unique())
  print(*names, sep="\n")
  return

def ex18(file_name:str="popular-names.txt"):
  """ファイルの内容を行単位で並び替え

  Unixコマンドによる処理
    sort -k 3nr popular-names.txt
  """

  data = []
  with open(file_name) as file:
    data = [row.strip().split() for row in file]
  data = sorted(data, key=lambda x: int(x[2]), reverse=True)
  # 表示を合わせるための処理
  data = ["\t".join(row) for row in data]
  print(*data, sep="\n")
  return

def ex18_pd(file_name:str="popular-names.txt"):
  """ex18のpandasを用いた回答"""
  df = pd.read_csv(file_name, sep="\t", header=None)
  print(df.sort_values(2, ascending=False))
  return

def ex19(file_name:str="popular-names.txt"):
  """各行の単語列の出現頻度を求めて頻度の高い順に並びかえ

  Unixコマンドによる処理
    cut -f 1 popular-names.txt | sort | uniq -c | sort -k1rn
  """
  names = []
  with open(file_name) as file:
    names = [row.strip().split()[0] for row in file]
  c = collections.Container(names)
  names = sorted(c.items(), key=lambda x:x[1], reverse=True)
  print(*names, sep="\n")
  return

def ex19_pd(file_name:str="popular-names.txt"):
  """ex19のpandasを用いた回答"""
  df = pd.read_csv(file_name, sep="\t", header=None)
  print(df[0].value_counts())
  return