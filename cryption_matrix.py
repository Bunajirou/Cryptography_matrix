import tkinter as tk
from tkinter import messagebox
import numpy as np
import sympy
from sympy import mod_inverse

# 鍵の生成
def create_key():
    n = 95
    max_prime = pow(10, 3)
    min_prime = pow(10, 2)

    while(True):
        a = sympy.randprime(min_prime, max_prime)
        b = sympy.randprime(min_prime, max_prime)
        c = sympy.randprime(min_prime, max_prime)
        d = sympy.randprime(min_prime, max_prime)
        det = (a*d - b*c) % n
        if(sympy.gcd(det, n) == 1):break
    
    a_box.delete(0, tk.END)
    b_box.delete(0, tk.END)
    c_box.delete(0, tk.END)
    d_box.delete(0, tk.END)
    a_box.insert(tk.END, a)
    b_box.insert(tk.END, b)
    c_box.insert(tk.END, c)
    d_box.insert(tk.END, d)


# 暗号化
def encryption():
    A = 32
    n = 127-A
    try:
        a = int(a_box.get())
        b = int(b_box.get())
        c = int(c_box.get())
        d = int(d_box.get())
    except:
        messagebox.showwarning('エラー','暗号化鍵が間違っている、もしくは入力されていません。')

    det = (a*d - b*c) % n
    if(sympy.gcd(det, n) != 1):
        messagebox.showwarning('エラー','暗号化鍵が正しくありません')

    en_key = np.array([[a,b],[c,d]])
    p_txt = input_box.get()

    p_txt_list = list(p_txt)  # 文字列をリストへ変換
    p_ascii_list = []

    for i in p_txt_list:  # ASCIIコードへ変換
        p_ascii_list.append(ord(i)-A) 
    p_len = len(p_ascii_list)

    if(p_len % 2 == 1):  # 文字数が奇数だった場合リストの末尾に0(スペース)を挿入
        p_ascii_list.append(0)

    p_arr = np.array(p_ascii_list).reshape(-1, 2)
    c_arr_tmp = np.mod(en_key @ p_arr.T, n)
    c_arr = c_arr_tmp.T
    c_ascii_list = np.ravel(c_arr)

    c_txt_list = []
    for i in c_ascii_list:  # ASCIIコードを文字へ変換
        c_txt_list.append(chr(i+A))

    c_txt = (''.join(c_txt_list))  # リスト内の文字を結合
    output_box.delete(0, tk.END)
    output_box.insert(tk.END, c_txt)


# 復号
def decryption():
    A = 32
    n = 127-A
    try:
        a = int(a_box.get())
        b = int(b_box.get())
        c = int(c_box.get())
        d = int(d_box.get())
    except:
        messagebox.showwarning('エラー','暗号化鍵が間違っている、もしくは入力されていません。')

    det = (a*d - b*c) % n
    if(sympy.gcd(det, n) != 1):
        messagebox.showwarning('エラー','暗号化鍵が正しくありません')

    indet = mod_inverse(det, n)
    a_ans = (d * indet) % n
    b_ans = (-b * indet) % n
    c_ans = (-c * indet) % n
    d_ans = (a * indet) % n
    de_key = np.array([[a_ans,b_ans],[c_ans,d_ans]])

    c_txt = input_box.get()
    c_txt_list = list(c_txt)  # 文字列をリストへ変換

    c_ascii_list = []
    for i in c_txt_list:  # ASCIIコードへ変換
        c_ascii_list.append(ord(i)-A) 

    c_arr = np.array(c_ascii_list).reshape(-1, 2)
    p_arr_tmp = np.mod(de_key @ c_arr.T, n)
    p_arr = p_arr_tmp.T
    p_ascii_list = np.ravel(p_arr)
    p_ascii_list =map(int, p_ascii_list)

    p_txt_list = []
    for i in p_ascii_list:  # ASCIIコードを文字へ変換
        p_txt_list.append(chr(i+A))
    if(p_txt_list[-1]==' '):  # 最後の文字がスペースなら削除
        p_txt_list.pop()

    p_txt = (''.join(p_txt_list))  # リスト内の文字を結合
    output_box.delete(0, tk.END)
    output_box.insert(tk.END, p_txt)


# ラジオボタンに応じて表示の変更
def check_rdo():
    if(mode.get()==0):
        run_button = tk.Button(text='暗号化実行', command=encryption)
        invar.set('<平文を入力>')
        outvar.set('<暗号文')
        keyvar.set('<暗号化鍵を入力>　または　<暗号化鍵を生成>')
        key_button.pack(
            side=tk.RIGHT,
            expand=True,
            anchor=tk.NE,
            pady=80,
            padx=80
        )
    else:
        run_button = tk.Button(text='復号化実行', command=decryption)
        invar.set('<暗号文を入力>')
        outvar.set("<平文>")
        keyvar.set('<暗号化鍵を入力>')
        key_button.pack_forget()
    run_button.place(x=260, y=208)
    input_box.delete(0, tk.END)
    output_box.delete(0, tk.END)


if __name__ == '__main__':
    # ウィンドウの作成
    root = tk.Tk()
    root.title('行列を用いた暗号')
    root.geometry("350x300")

    # 表示変更用制御変数
    invar = tk.StringVar()
    invar.set('')
    outvar = tk.StringVar()
    outvar.set('')
    keyvar = tk.StringVar()
    keyvar.set('')

    # ラベルの作成
    key_label = tk.Label(textvariable=keyvar)
    key_label.place(x=10, y=10)
    bracket_label = tk.Label(text='(     )', font=('MS明朝', '50', 'normal'))
    bracket_label.place(x=8, y=40)
    mode_label = tk.Label(text='<モード選択>')
    mode_label.place(x=10, y=120)
    input_label = tk.Label(textvariable=invar)
    input_label.place(x=10, y=190)
    output_label = tk.Label(textvariable=outvar)
    output_label.place(x=10, y=240)

    # 入出力欄の作成
    a_box = tk.Entry(width=5)
    a_box.place(x=40, y=55)
    b_box = tk.Entry(width=5)
    b_box.place(x=90, y=55)
    c_box = tk.Entry(width=5)
    c_box.place(x=40, y=80)
    d_box = tk.Entry(width=5)
    d_box.place(x=90, y=80)
    input_box = tk.Entry(width=40)
    input_box.place(x=10, y=211)
    output_box = tk.Entry(width=40)
    output_box.place(x=10, y=261)

    # ボタンの作成
    key_button = tk.Button(text='暗号化鍵を生成',command=create_key)

    # ラジオボタンの作成
    mode = tk.IntVar()
    mode.set(0)
    de_rdo = tk.Radiobutton(root, value=0, variable=mode, text='暗号化モード', command=check_rdo)
    de_rdo.place(x=10, y=140)
    en_rdo = tk.Radiobutton(root, value=1, variable=mode, text='復号化モード', command=check_rdo)
    en_rdo.place(x=10, y=160)

    check_rdo()


root.mainloop()