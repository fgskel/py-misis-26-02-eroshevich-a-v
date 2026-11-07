print('Введите первое число:')
n1 = int(input())
print('Введите второе число:')
n2 = int(input())
print('Введите знак:')
op = str(input())
if op == '+':
    print('Результат:', n1 + n2)
elif op == '-':
    print('Результат:', n1 - n2)
elif op == '*':
    print('Результат:', n1 * n2)
elif op == '/':
    print('Результат:', n1 / n2)
elif op == '%':
    print('Результат:', n1 % n2)
else:
    print('Результат:', n1 // n2)

