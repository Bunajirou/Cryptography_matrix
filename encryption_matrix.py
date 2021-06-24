import numpy as np
import sympy

A =32
n = 127 - A

a=int(input('a='))
b=int(input('b='))
c=int(input('c='))
d=int(input('d='))

det = (a*d - b*c) % n
if(sympy.gcd(det, n) != 1):
    print('error')

en_key = np.array([[a,b],[c,d]])

p_txt = str(input('Plaintexst?:'))
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

print('Cryptogram:',c_txt)