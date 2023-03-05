if __name__ == '__main__':
    n = int(input())
    student_marks = {}
    sum=0
    
    for _ in range(n):
        name, *line = input().split()
        scores = list(map(float, line))
        student_marks[name] = scores
    query_name = input()
    
    for i in range(0,len(student_marks[name])):
        sum= sum+student_marks[query_name][i]
    x=len(student_marks[name])   
    y= sum/x   
    print('%.2f' %(y))