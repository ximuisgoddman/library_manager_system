from django.test import TestCase


# Create your tests here.
def check_if_ok(n):
    flag = 0
    for m in range(2, n):
        x = n / m - (m - 1) / 2
        print(m, x)
        if str(x).split(".")[-1] == "0":
            flag = 1
    return True if flag else False


print(check_if_ok(10))
