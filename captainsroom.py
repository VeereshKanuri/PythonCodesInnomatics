

x= int(input())
y= list(map(int,input().split()))
z=set(y)
sum=0
count=0
for i in y:
    sum=sum+i

for item in z:
    count=count+item*x

print((count-sum)//(x-1))