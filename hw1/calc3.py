def f(a, b, c):
    if c == '+': return a + b
    elif c == '-': return a - b
    elif c == '*': return a * b
    elif c == '/': return a / b
    elif c == '%': return a % b
    elif c == '//': return a // b
while True:
    for i in range(1):
        print('Введите первое число:')
        a = int(input())
        print('Введите второе число:')
        b = int(input())
        print('Введите знак:')
        c = str(input())
        print('Результат:', f(a, b, c))
        break

    