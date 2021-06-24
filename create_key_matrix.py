import sympy

n = 95
det = 95

# a,b,c,dの最大値、最小値
max_prime = pow(10, 3)
min_prime = pow(10, 2)

# keyの作成
while(sympy.gcd(det, n) != 1):
    a = sympy.randprime(min_prime, max_prime)
    b = sympy.randprime(min_prime, max_prime)
    c = sympy.randprime(min_prime, max_prime)
    d = sympy.randprime(min_prime, max_prime)

    det = (a*d - b*c) % n

print(a,b,c,d)