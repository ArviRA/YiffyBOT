//This is The Coding Area
def lcm(a,b):
    while(b!=0):
        temp = a
        a = b
        b = temp % b
    return a
t = int(input())
for _ in range(t):
    n = int(input())
    a = list(map(int,input().split()))
    i = 0
    ans = 1
    c = 0
    while(i<=n-1):
        temp_i = i
        c = 0
        while(a[i]!=0):
            temp = i
            i = a[i] - 1
            a[temp] = 0
            c+=1
        i = temp_i + 1
        if(c!=0):
            ans = ans*c//lcm(ans,c)
    print(ans)