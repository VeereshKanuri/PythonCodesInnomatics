if __name__ == '__main__':
    N = int(input())
    list1=[]
    for i in range(N):
        y=list(input().split())
        if y[0]=='insert':
            list1.insert(int(y[1]),int(y[2]))
        if y[0]=='remove':
            list1.remove(int(y[1]))
        if y[0]=='append':
            list1.append(int(y[1]))
        if y[0]=='print':
            print(list1)
        if y[0]=='sort':
            list1.sort()
        if y[0]=='pop':
            list1.pop()
        if y[0]=='reverse':
            list1.reverse()