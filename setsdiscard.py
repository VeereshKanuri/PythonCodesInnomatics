n = int(input())
s = set(map(int, input().split()))
x= int(input())
for i in range(x):
    lis= input().split()
    if lis[0]=='pop':
        s.pop()
    else:
        lis2= list(lis)
        m=str(lis2[0])
        n= int(lis2[1])
        if m=='remove':
            s.remove( n)
        elif m=='discard':
            s.discard(n)
        
print(sum(s))