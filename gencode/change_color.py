import os
import numpy as np
import pandas as pd


# 0/1でふるいの位置を左側/右側に初期化
direction = 0

# データシートの読み込み
file_dir = os.path.dirname(os.path.abspath(__file__))
df = pd.read_table(os.path.join(file_dir, 'datasheet.tsv'))

# 配列データの読み込みと差分計算
def read_data():
    # before，afterをndarrayとして読み込み
    file_before = os.path.join(file_dir, 'before.txt')
    file_after = os.path.join(file_dir, 'after.txt')
    arr_before = np.loadtxt(file_before, dtype='int', delimiter=',', encoding='utf_8_sig', max_rows=4)
    arr_after = np.loadtxt(file_after, dtype='int', delimiter=',', encoding='utf_8_sig', max_rows=4)

    # 各要素の色の差分を計算
    diff = (arr_after - arr_before) % 4
    
    # 差分有り；0，差分なし：1
    all_zero = 0
    if np.all(diff == 0) == True:
        all_zero = 1
    
    # 差分有りのとき差分を表示
    if all_zero == 0:
        print('difference:\n{}\nfinal state:\n{}' .format(diff, arr_after))
    # 差分無しのとき
    else:
        print('difference: nothing')

    return diff, all_zero


# ふるいが左側から右向きスタート
def right_forward(diff=None):
    # before，afterから差分を計算
    diff = np.array(diff).reshape(4, -1)
    # diff, all_zero = read_data()

    # キューブの行ごとに値をまとめて整列
    num = np.array(range(4))
    num[0] = 1000*diff[3, 0] + 100*diff[3, 1] + 10*diff[3, 2] + 1*diff[3, 3]
    num[1] = 1000*diff[2, 0] + 100*diff[2, 1] + 10*diff[2, 2] + 1*diff[2, 3]
    num[2] = 1000*diff[1, 0] + 100*diff[1, 1] + 10*diff[1, 2] + 1*diff[1, 3]
    num[3] = 1000*diff[0, 0] + 100*diff[0, 1] + 10*diff[0, 2] + 1*diff[0, 3]
    
    # 行ごとにデータシートを参照
    arr = {}
    arr_len = {}
    # 最多手数
    length = 0
    for i in range(4):
        # データシートから該当する行をまとめて抽出
        extract = df.query('diff_fill == @num[@i]')
        # 該当行から必要な列を抽出
        arr[i] = extract['dec'].to_numpy()
        # arrの中身が0なら長さを0とする
        if np.all(arr[i] == 0) == True:
            arr_len[i] = 0
        else:
            arr_len[i] = len(arr[i])
        
        # 抽出した列の長さは手数に相当
        # 最多手数より大きければ更新
        if arr_len[i] > length:
            length = arr_len[i]
    
    # 最多手数がゼロのときふるいは静止
    if length == 0:
        direction = -1
    # 最多手数が偶数のとき色変化後にふるいは左側
    elif length % 2 == 0:
        direction = 0
    # 最多手数が奇数のとき色変化後にふるいは右側
    else:
        direction = 1


    # 命令配列
    command = []
    # 最多手数準拠
    for j in range(length):
        # キューブは全4行
        for i in range(4):
            # '+ (j % 2) * 32' について
            # ここではふるいは左側から右向きスタートなので，jが偶数/奇数のときふるいは右向き/左向きに動く
            # 右向き/左向きを区別するため，左向きのときは32を足した値としている


            # jがあるキューブの行の手数より大きい，つまり，当該行の色変化が完了しているが他の行がまだ完了していないとき

            # かつ，当該行の手数と最大手数との差が偶数，つまり，当該行の色変化が完了したときのふるいの位置と最終的なふるいの位置とが同じ場合
            if j >= arr_len[i] and (length - arr_len[i]) % 2 == 0:
                # 実質0を命令に追記，全下げ
                command.append(0 + (j % 2) * 32)
            # 差が奇数，つまり，ふるいの位置が左右異なる場合
            elif j >= arr_len[i] and (length - arr_len[i]) % 2 == 1:
                # 当該行の最終手のとき
                if j == arr_len[i]:
                    # 実質31を命令に追記，全上げで1回動かす
                    command.append(31 + (j % 2) * 32)
                # それ以降
                else:
                    # 実質0を命令に追記，全下げ
                    command.append(0 + (j % 2) * 32)
            
            # jが当該行の手数以下の場合
            else:
                # データシートから抽出した値を命令に追記
                command.append(arr[i][j])
    
    # 終端記号を命令に追記
    command.append(255)


    # 色の差分が有るとき命令配列とふるいの位置を表示
    # if all_zero == 0:
    if False:
        print('command: {}' .format(command))
        print('sifter moves {} times' .format(int((len(command) - 1) / 4)))

    return(command, direction)


# ふるいが右側から左向きスタート
# 右向きとほぼ同様の手順だが，左右や偶奇が反転していることに注意
def left_forward(diff=None):
    diff = np.array(diff).reshape(4, -1)
    # diff, all_zero = read_data()
    
    # 1と3を入れ替え
    diff = np.where(diff==1, 5, diff)
    diff = np.where(diff==3, 1, diff)
    diff = np.where(diff==5, 3, diff)
    
    # 左向きスタートの場合とは左右反転して整列
    num = np.array(range(4))
    num[0] = 1000*diff[3, 3] + 100*diff[3, 2] + 10*diff[3, 1] + 1*diff[3, 0]
    num[1] = 1000*diff[2, 3] + 100*diff[2, 2] + 10*diff[2, 1] + 1*diff[2, 0]
    num[2] = 1000*diff[1, 3] + 100*diff[1, 2] + 10*diff[1, 1] + 1*diff[1, 0]
    num[3] = 1000*diff[0, 3] + 100*diff[0, 2] + 10*diff[0, 1] + 1*diff[0, 0]
    
    arr = {}
    arr_len = {}
    length = 0
    for i in range(4):
        extract = df.query('diff_fill == @num[@i]')
        arr[i] = extract['dec_reverse'].to_numpy()

        if np.all(arr[i] == 32) == True:
            arr_len[i] = 0
        else:
            arr_len[i] = len(arr[i])
        
        if arr_len[i] > length:
            length = arr_len[i]
    
    if length == 0:
        direction = -1
    elif length % 2 == 0:
        direction = 1
    else:
        direction = 0


    command = []
    for j in range(length):
        for i in range(4):
            if j >= arr_len[i] and (length - arr_len[i]) % 2 == 0:
                    command.append(0 + ((j+1) % 2) * 32)
            elif j >= arr_len[i] and (length - arr_len[i]) % 2 == 1:
                if j == arr_len[i]:
                    command.append(31 + ((j+1) % 2) * 32)
                else:
                    command.append(0 + ((j+1) % 2) * 32)
            
            else:
                command.append(arr[i][j])
    
    command.append(255)

    # if all_zero == 0:
    if True:
        print('command: {}' .format(command))
        print('sifter moves {} times' .format(int((len(command) - 1) / 4)))

    return(command, direction)


if __name__ == '__main__':
    print('')
    if direction == 0:
        command, direction = right_forward()
    else:
        command, direction = left_forward()
    print('\n')
