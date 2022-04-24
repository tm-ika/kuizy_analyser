# kuizy_analyser
数問の選択肢を選んで診断結果を表示するサイトkuizy。希望する診断結果が出るようにするための解析ツール  

# 必要なもの
- 診断したいkuizyのURL　（例 https://kuizy.net/analysis/4034/6 ）  
- python 実行環境  

# ざっくりした処理  
- 選択肢ごとに各診断結果に近づくための配点※が決められている　※[ ]の内部
- 全設問が終了するまで選択を繰り返し、配点の総和をとり、最大値となるインデックスが診断結果となる
- 本ツールはこれらの選択肢をitertoolを使って総当たりし、全パターンの計算を行っている
```
<li id="li4-1" onclick="selected(4, 1, [0, 0, 0, 0, 2, 0, 1, 1, 1, 2], 322476)">
           自分が連キルをすること
</li> 
```

# 実行結果
![image](https://user-images.githubusercontent.com/102900238/164967347-27b7c0b3-3042-4842-8d16-b4a0ae35a11d.png)
