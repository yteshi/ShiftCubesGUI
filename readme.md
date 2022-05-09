# S(h)ift Cubes GUI

- [S(h)ift Cubes GUI](#shift-cubes-gui)
  - [要約](#要約)
  - [実行の手順](#実行の手順)
  - [準備する Python 環境について](#準備する-python-環境について)
  - [ファイル構成](#ファイル構成)
  - [Mac で実行するときの注意事項](#mac-で実行するときの注意事項)

## 要約

1. Python 　バージョン **3.10** の環境を用意してください．（3.9 等だと，理由は不明ですが，うまく動きません）
2. `pip install numpy pandas pyserial`を実行してください．
3. macOS の場合は，`pip install tkmacosx`を実行してください．
4. `python ShifterGUI.py`を実行してください．

## 実行の手順

1. condaを利用している場合（長谷川）
   1. ターミナルで`conda activate py310`を実行する．
   2. `python ShifterGUI.py`を実行する．
2. pyenvを利用している場合（手嶋）
   1. ターミナルで，`source {path-to-pyenv-dir}/bin/activate`を実行する．
   2. `python ShifterGUI.py`を実行する．

## 準備する Python 環境について

Python はバージョン**3.10.0**で実行してください．
3.9 ではではうまく動作しません．（理由は不明）
バージョンを確かめるためには，ターミナルで，
```
$python -V
Python 3.10.0
```
を実行することで確認できます．

必要な Python のパッケージは以下の表のとおりです．

| パッケージ名    | バージョン | 備考                                 |
| --------------- | ---------- | ------------------------------------ |
| colour          | 0.1.5      | tkmacosx で使用                      |
| numpy           | 1.22.3     | コマンドを計算するために使用         |
| pandas          | 1.4.2      | コマンドを計算するために使用         |
| pyserial        | 3.5        | シリアル通信のために使用             |
| python-dateutil | 2.8.2      |
| pytz            | 2022.1     |
| six             | 1.16.0     |
| tkmacosx        | 1.0.4      | Tkinter の Button など（macOS のみ） |

以上のパッケージは，
```
>pip install -r requirement.txt
```
を実行することでインストールすることができます．

以上のインストールを行った上で，
```
python ShifterGUI.py
```
を実行すれば，GUI が表示されます．

## ファイル構成

-   `/gencode/*`
    -   福井のプログラムの必要な部分のみをコピーしたディレクトリ
-   `Cube.py`
    -   キューブのクラス．
    -   1 つのキューブは表示に使われる 4 色の情報を持つ
-   `CubeColor.py`
    -   キューブに使われる色を定義した列挙体
    -   将来的には，それぞれのキューブで違う色を定義できるようにしたいので作成した．
-   `SarasaButton.py`
    -   GUI に使われるボタン．
    -   `SarasaButton`は，以下のクラスを継承している．
        -   Windows の場合：`tkinter.Button`
        -   macOS の場合：`tkmacosx.Button`
-   `SerialPortSelectDialog.py`
    -   シリアルポート選択画面．
    -   `tkinter.Toplevel`を継承している．
-   `ShifterGUI.py`
    -   メインウィンドウの GUI．このファイルを呼び出すことで，GUI が起動される．

## Mac で実行するときの注意事項

理由は不明だが，GUI の一部パーツ（ボタンやラジオボックス等）が
正しく動作しないバグがある．このバグは，Tkinter という GUI ライブラリによるものであり，
最新版の Python でも解決されていない．

このバグを解決するために，`tkmacosx`パッケージを用いる．
このパッケージは，前述のバグに対応したパーツを提供するパッケージである．

このプログラムでは，`tkinter.Button`の代わりに，`tkmacosx.Button`を用いている．
