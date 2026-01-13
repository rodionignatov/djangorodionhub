for A in range(1, 500):
    f = True
    for x in range(1, 250):
        for y in range(1, 200):
            Z = ((x <= 9) <= (x * x <= A)) and ((y * y <= A) <= (y <= 9))
            if Z == 0:
                f = False
                break
    if f == True:
        print(A)
        