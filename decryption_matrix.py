import numpy as np
import sympy
from sympy import mod_inverse


A =32
n = 127 - A

a=int(input('a='))
b=int(input('b='))
c=int(input('c='))
d=int(input('d='))

det = (a*d - b*c) % n
if(sympy.gcd(det, n) != 1):
    print('error')

indet = mod_inverse(det, n)
a_ans = (d * indet) % n
b_ans = (-b * indet) % n
c_ans = (-c * indet) % n
d_ans = (a * indet) % n
de_key = np.array([[a_ans,b_ans],[c_ans,d_ans]])


c_txt = str(input('Cryptogram?:'))
c_txt_list = list(c_txt)  # 文字列をリストへ変換

c_ascii_list = []
for i in c_txt_list:  # ASCIIコードへ変換
    c_ascii_list.append(ord(i)-A) 

if(c_ascii_list[-1]==0):
    c_ascii_list.pop()

c_arr = np.array(c_ascii_list).reshape(-1, 2)
p_arr_tmp = np.mod(de_key @ c_arr.T, n)
p_arr = p_arr_tmp.T
p_ascii_list = np.ravel(p_arr)
p_ascii_list =map(int, p_ascii_list)

p_txt_list = []
for i in p_ascii_list:  # ASCIIコードを文字へ変換
    p_txt_list.append(chr(i+A))

p_txt = (''.join(p_txt_list))  # リスト内の文字を結合

print('Plaintexst:',p_txt)