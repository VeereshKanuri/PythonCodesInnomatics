y=map(int,input().split())
z=set(y)
x= int(input())
lis=[]
for i in range(x):
    a=map(int,input().split())
    f=set(a)
    lis.append(z.issuperset(f))
if all(lis)==True:
    print('True')
else:
    print('False')