x= int(input())
for i in range(x):
    y=input()
    a=map(int,input().split())
    s=set(a)
    b=input()
    c=map(int,input().split())
    f=set(c)
    print(s.issubset(f))
    