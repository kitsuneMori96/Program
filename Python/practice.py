def f(x,y):
    return x**2-y

def df(x):
    return 2*x

def nt(x,y):
    while abs(f(x,y))>1e-5:
        x = x-f(x,y)/df(x)
    return x

if __name__ == '__main__':
    print (nt(2,5))
