x= input()
y= map(int,input().split())
s= set(y)
z=input()
c= map(int,input().split())
w= set(c)
q=s.symmetric_difference(w)
print(len(q))