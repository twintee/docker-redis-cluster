# docker-redis-cluster

## 📚 概要
私用で作ったredis6系のクラスタノード作成用docker-composeとその他諸々  
基本pythonでコンテナの外から制御したい  

## 🌏 動作環境
- ubuntu :16.*, 18.*

## ⚙ 使用法
- ノード生成
    1. 必要モジュール
        - python-dotenv  
        `pip install python-dotenv`
    1. `config.py`を実行。応答で必要情報を.envに書き出したり情報を付与したマウント用ファイルを生成する。  
        - masterを作る場合  
        `python3 config.py master`  
        - slaveを作る場合  
        `python3 config.py slave`  
        - master/slaveを個別設定（１ホストクラスタ等）の場合はmaster・slaveの両方実行
    1. コンテナ生成
        `sudo python3 init.py`  
        - 応答は基本'y'でボリュームやlogの削除は都度判断。dumpはスクリプトから制御しない。
        - nodeの種類を切り替えたい場合config.pyをサイド実施してコンテナ生成スクリプトを再実行。
        - 1ホストでmaster/slave構成したい場合  
        `sudo python3 init.py -n all`  
