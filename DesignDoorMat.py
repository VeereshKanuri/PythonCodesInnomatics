x=list(map(int,input().split()))
str1='.|.'
str2='WELCOME'
lis=list(range(x[0]//2))
for i in range(x[0]//2):
    print((str1*(i*2+1)).center(x[1],'-'))
print(str2.center(x[1],'-'))
for i in lis[::-1]:
    print((str1*(i*2+1)).center(x[1],'-'))
