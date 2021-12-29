from os import sep
import subprocess
import re

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

  df1=pd.read_table("col1.txt", header=None)
  df2=pd.read_table("col2.txt", header=None)

  # df1.shape -> (2780, 1)
  # axis=0なら要素数2780の方の次元で連結する
  # axis=1なら要素数1の方の次元で連結する
  df = pd.concat([df1, df2], axis=1)

  df.to_csv(path_or_buf="col1-2.txt", sep="\t", header=False, index=False)