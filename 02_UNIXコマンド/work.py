import subprocess
import re

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
  # cat popular-names.txt | sed "s/\t/ /g"
  with open(file_name) as file, open("ex11.txt", "w") as fout:
    for line in file:
      line = re.sub(r"\t", " ", line)
      fout.write(line)

def ex12(file_name:str="popular-names.txt"):
  """カラムの抜き出し"""
  with open(file_name) as file, open("ex12.txt", "w") as fout:
