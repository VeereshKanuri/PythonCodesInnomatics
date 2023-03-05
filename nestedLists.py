if __name__ == '__main__':
    lis1=[]
    scor=[]
    name1=[]
    a= int(input())
    for _ in range(a):
        name = input()
        score = float(input())
        lis1.append([name,score])
        scor.append(score)
    set_1= set(scor)
    lis2= sorted(list(set_1))
    for i in reversed(range(a)) :
        if lis2[1] == lis1[i][1]:
            name1.append(lis1[i][0])
            sorted_list= sorted(name1)
    for j in range(len(sorted_list)):
        print(sorted_list[j])