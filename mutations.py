def mutate_string(string, position, character):
    str1= string
    lis= list(string)
    lis[position]=character
    str1= ''.join(lis)
    return str1
    