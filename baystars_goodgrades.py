from tkinter import *
from tkinter import  messagebox as mb
import requests
from bs4 import BeautifulSoup

"""
ベイスターズの打者の良い成績だけを公式サイトから持ってくるコード。
サイトを見たところ,成績の情報が<td>というタグにまとめられていることが分かった。
一人の打者につき5つずつのタグがあったのでそれぞれの情報を(5x+n)で表すようにした。
また、ボタンを押された時の処理を見やすくしようと思い、成績の情報を集める関数と、
ボタンを押された時の処理の関数を分けようとしたが、変数の情報を保持できなかったので、
ボタンを押された時の処理で一度に両方行った。
"""

#　メインウィンドウを作り、ボタンを実装する
win = Tk()
mylabel = Label(win,text = "ベイスターズの情報を見ますか？")
mylabel.pack()

def ok_click():
    db_butterlist = ['戸柱','伊藤光','益子','高城','嶺井','山本','東妻','中井','牧','伊藤裕',
    '倉本','森','大和','柴田','田中俊','小深田','宮崎','田部','知野','山下','ソト','デラロサ',
    '宮本','桑原','佐野','神里','オースティン','乙坂','楠本','細川','蛯名','関根']

    # URLからTHMLの情報をテキストとして持ってくる
    url = 'https://www.baystars.co.jp/game/result'
    r = requests.get(url)
    soup = BeautifulSoup(r.text)

    count = 0           # 成績を判別する際に必要な数字
    is_db = False       # ベイスターズの選手かの判別
    action = False      # 良い成績かどうかの判別
    out_count = 'a'
    butter_name = 'a'
    game = True         # 試合が始まっているかの判別

    # 情報を記録するファイルの作成
    with open('test.text', 'w'):
        pass

    # tdタグに挟まれている箇所を抽出
    soup = soup.find_all('td')
    # 抽出した箇所を一つずつ処理する
    for child in soup:
        count += 1

        # 試合の中で打者100人までは判別できるようにした
        for i in range(100):

            # カウントが(5x+1)の時は、アウトカウントの情報
            # 文字列が0アウトか、変化しなかった時、良い成績だとわかる
            if count == i*5+1 and \
            (str(child.contents) == '[<img src="/images/game/out0.png"/>]' or str(child.contents) == out_count):
                action = True
            # 良い成績でなかった時、変化したアウトカウントを変数に入れる
            elif count == i*5+1 and \
            (str(child.contents) != '[<img src="/images/game/out0.png"/>]' or str(child.contents) != out_count):
                out_count = str(child.contents)
                action = False

            # アウトカウントが(5x+3)の時は打者の名前
            # 後でファイルに書き込めるように変数に入れる
            if count == i*5+3 and (str(child.text) in db_butterlist):
                is_db = True
                butter_name = child.text
            elif count == i*5+3 and (str(child.text) not in db_butterlist):
                is_db = False

            # アウトカウントが(5x+5)の時は打者の成績
            # 代打、代走、交代の成績も表示されてしまうので、表示しないようにする
            # ☆で囲まれた箇所は点数を表し、勝ち負けが分かってしまうので、別の処理にする
            if count == (i*5+5) and action == True and\
            '代打' not in str(child) and '代走' not in str(child) and '交代' not in str(child)\
            and is_db == True and '☆' not in str(child):
                text = '{0} {1}{2}'.format(butter_name,child.text,'\n')
                # ファイルに成績を書き込む
                with open('test.text','a') as f:
                    f.write(text)

            # 成績の中に☆があった時、後ろから11文字を削除し、記録する
            # 11文字削除する事で両チームが2桁得点の時も綺麗に記録できる
            if count == (i*5+5) and is_db == True and '☆' in str(child):
                text = '{0} {1}{2}{3}'.format(butter_name,child.text[:-11],'!','\n')
                # ファイルに成績を書き込む
                with open('test.text','a') as f:
                    f.write(text)

            # 処理の最初にカウントを+1しているので、カウントが0の時は試合が始まっていないと分かる
            if count == 0:
                game = False

    # 試合が始まっているとき、ファイルから成績を取ってきて、試合情報というタイトルで成績を表示
    if game == True:
        with open('test.text') as f:
            s = f.read()
            mb.showinfo('試合情報',s)
    # 試合が始まっていないときの処理
    else:
        mb.showinfo('試合情報','まだ試合が始まっていません')

# ボタンの見た目を作って実装
okButton = Button(win,text = "見る",command=ok_click)
okButton.pack()

# Tkinterで必須の処理
win,mainloop()