# Linuxコマンドの紹介

* Linuxのbashファイルでログを解析を行うことが多いので共有。
* bashファイルはWindowsで言うところのbatファイルだが、数多くのLinuxコマンドを利用することで解析スクリプトとして扱える。
* WindowsでもWSLがあるし、一部はgit bashでも動くので活用できる。
* bashはLinuxの標準で入っていてpythonみたいに環境構築しなくていいので楽。

---

## 目次

* cat
* grep
* cut
* sed
* sort
* uniq
* xargs
* awk

---

## cat

* テキストファイルを一行ずつ取り出して標準出力するコマンド

```sh
cat test.log
```

```
2022-07-24 19:10:05,169 thread-26288 __main__:28 main [INFO]: START
2022-07-24 19:10:05,169 thread-6652 __main__:18 work [INFO]: Received
2022-07-24 19:10:05,170 thread-27628 __main__:18 work [INFO]: Received
2022-07-24 19:10:05,170 thread-20256 __main__:18 work [INFO]: Received
2022-07-24 19:10:05,787 thread-27628 __main__:20 work [INFO]: Calculate START
2022-07-24 19:10:05,927 thread-6652 __main__:20 work [INFO]: Calculate START
2022-07-24 19:10:05,942 thread-20256 __main__:20 work [INFO]: Calculate START
2022-07-24 19:10:08,471 thread-27628 __main__:22 work [INFO]: Calculate END
（中略）
2022-07-24 19:10:18,081 thread-27628 __main__:24 work [INFO]: Replied
2022-07-24 19:10:19,328 thread-20256 __main__:22 work [INFO]: Calculate END
2022-07-24 19:10:19,636 thread-20256 __main__:24 work [INFO]: Replied
2022-07-24 19:10:19,637 thread-26288 __main__:36 main [INFO]: END
```


```
# 日付　スレッドID　モジュール名:行数　関数　ログレベル: メッセージ
2022-07-24 19:02:09,048 2876 __main__:28 main [INFO]: START
```

---

## grep

* 入力から特定のワードを含んでいる行だけを出力する。
  * 複数条件を指定したり、正規表現を使ったり、ワードが含まない行を出力することもできる。

```sh
cat test.log | grep "Calculate START"
```

"Calculate START"を抜き出す
```
2022-07-24 19:10:05,787 thread-27628 __main__:20 work [INFO]: Calculate START
2022-07-24 19:10:05,927 thread-6652 __main__:20 work [INFO]: Calculate START
2022-07-24 19:10:05,942 thread-20256 __main__:20 work [INFO]: Calculate START
2022-07-24 19:10:09,585 thread-27628 __main__:20 work [INFO]: Calculate START
2022-07-24 19:10:09,939 thread-6652 __main__:20 work [INFO]: Calculate START
2022-07-24 19:10:11,301 thread-20256 __main__:20 work [INFO]: Calculate START
2022-07-24 19:10:12,029 thread-6652 __main__:20 work [INFO]: Calculate START
2022-07-24 19:10:13,735 thread-27628 __main__:20 work [INFO]: Calculate START
2022-07-24 19:10:16,661 thread-20256 __main__:20 work [INFO]: Calculate START
```

---

## cut

* 行を一定のルールで分割するコマンド
  * 固定幅 OR 区切り文字分割

```sh
cat test.log | grep "Calculate START" | cut -d " " -f 3   
```

スレッドIDの列を抜き出す
```
thread-27628
thread-6652
thread-20256
thread-27628
thread-6652
thread-20256
thread-6652
thread-27628
thread-20256
```

---

## sed

* 入力した行の文字列の置換を行うコマンド
  * 特定の文字列や正規表現にマッチした部分を置き換える。削除するときに使うことが多い。
  * `'s/abc/ABC/g'` の形式で指定する。（sは置換コマンド、gは繰り返し実行のオプション）


```sh
cat test.log | grep "Calculate START" | cut -d " " -f 3 | sed 's/thread-//g'
```

スレッドIDの数値だけを取得

```
27628
6652
20256
27628
6652
20256
6652
27628
20256
```

---

## sort

* ソートするコマンド。文字列としても数値としてもソートできる。


```sh
cat test.log | grep "Calculate START" | cut -d " " -f 3 | sed 's/thread-//g' | sort -n
```

```
6652
6652
6652
20256
20256
20256
27628
27628
27628
```

---

## uniq

* 重複を削除するコマンド。隣り合うものしか比較しないのでsortしてから実行する。


```sh
cat test.log | grep "Calculate START" | cut -d " " -f 3 | sed 's/thread-//g' | sort -n | uniq
```

```
6652
20256
27628
```

---

## date

* 日付・時刻を取得するコマンド。経過秒への変換もできる。

```sh
date -d '2022-07-24 19:10:05,927' '+%s'
```

```
1658657405
```

---

## xargs

* 標準入力からの入力ではない場合 "|"（パイプ）は使えない。
  * cat, dateなどでは標準入力は受け付けない。
* xargsで標準入力された1行に対して任意の処理を実行できる。


```sh
cat test.log | grep "Calculate START" | cut -d " " -f 1,2 | xargs -I DATE sh -c "date -d 'DATE' '+%s'"
```

```出力
1658657405
1658657405
1658657405
1658657409
1658657409
1658657411
1658657412
1658657413
1658657416
```

---

## head

* 先頭のN行を取り出すコマンド

## tail

* 末尾のN行を取り出すコマンド

---

## awk

* 列ごとの計算などができるコマンド。cutコマンドの高機能版。

```sh
# 一番最初の時刻を取り出す
start_time=`cat test.log | cut -d " " -f 1,2 | xargs -I DATE sh -c "date -d 'DATE' '+%s'" | head -n 1`
# awkで時刻差を取得
cat test.log | grep "Calculate START" | cut -d " " -f 1,2 | xargs -I DATE sh -c "date -d 'DATE' '+%s'" | awk -v start_time=${start_time} '{print $1 - start_time}'
```

実行開始からの経過時間だけを取得
```
0
0
0
4
4
6
7
8
11
```

---

## まとめてみる

```sh
# thread_idの一覧
thread_ids=`cat test.log | grep "Calculate START" | cut -d " " -f 3 | sed 's/thread-//g' | sort -n | uniq`
# thrad_idごとに処理時間の平均値を出す
echo "thread_id:time"
for thread_id in $thread_ids; do
    echo -n"" $thread_id":"
    cat test.log | grep thread-$thread_id | grep -e "Calculate START" -e "Calculate END" | \
    cut -d " " -f 1,2 | xargs -I DATE sh -c "date -d 'DATE' '+%s'" | \
    awk 'BEGIN{mean=0}
        {
            if (NR%2!=0){ start_time=$1;} \
            else {mean = mean + $1 - start_time}
        } \
        END{print mean}'
done
```

出力
```
thread_id:time
6652:7
20256:11
27628:11
```