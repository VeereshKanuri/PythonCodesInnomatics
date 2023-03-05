x= map(int,input().split())
y=  map(int,input().split())
lis= list(y)
p=  map(int,input().split())
w= set(p)
q=  map(int,input().split())
e= set(q)
hapiness=0
for i in lis:
    if i in w:
       hapiness= hapiness+1
    if i in e:
       hapiness= hapiness-1
print(hapiness)