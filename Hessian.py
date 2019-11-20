def H(x,y):
    """
    Takes two x, y coordinates and returns the Hessian determinant
    of the function, the value of the first partial derivative
    evaluated at the point inputted, and the function value
    at the point.

    It also classifies the critical point, assuming that the
    points inputted are indeed critical points

    Author: Jasper Yun
    Date:   November 18, 2019
    """
    # change as required
    Fx = x*x + y*y - 8*x
    f11 = -2
    f12 = 0
    f22 = 2

    # don't change any of this
    Hess = f12*f12 - (f11*f22)
    
    print("Hess: %s  f11: %s  Fx: %s" %(Hess, f11, Fx))
    if (Hess > 0):
        print("saddle point")
    elif (Hess < 0):
        if (f11 < 0):
            print("local MAX")
        elif (f11 > 0):
            print("local min")
    elif (Hess == 0):
        print("no information")
    
# runs the program continuously until you break
print("End the while loop by inputting XX (program will crash)")
while(True):
    x=int(input("X: "))
    y=int(input("Y: "))
    H(x,y)
    print('')
