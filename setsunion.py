x=input()
m= map(int,input().split())
z=set(m)
y=input()
n= map(int,input().split())
v=set(n)
q=z.union(v)
print(len(q))