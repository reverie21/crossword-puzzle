
for i in range(1,int(input())): #More than 2 lines will result in 0 score. Do not leave a blank line also
    print((i*10**0 + i*10**1 + i*10**2 + i*10**3 + i*10**4 + i*10**5 + i*10**6 + i*10**7 + i*10**8 + i*10**9) % 10**i)
