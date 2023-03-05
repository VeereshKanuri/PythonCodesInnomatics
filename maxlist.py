if __name__ == '__main__':
    n = int(input())
    arr = map(int, input().split())
    lis = set(arr)
    lis2= list(lis)
    lis2.sort()
    lis2.pop()
    print(max(lis2))