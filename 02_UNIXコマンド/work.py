import subprocess

def ex10(file_name:str="popular-names.txt")->str:
  """ファイルの行数を表示"""
  res = subprocess.check_output(("wc", "-l", "popular-names.txt")).split()[0]
  line_num_unix = int(res)
  with open(file_name) as file:
    line_num_python = len([1 for _ in file])
    assert line_num_python == line_num_unix
    return line_num_python