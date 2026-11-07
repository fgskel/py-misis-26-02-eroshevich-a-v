a = str(input())
text_1 = "пРиВет_МИР"
def first_lv(a):
    if a == 'upper': return text_1.upper()
    elif a == 'lower': return text_1.lower()
    elif 'capitalize': return text_1.capitalize()
print(first_lv(a))

b = str(input())
text_2 = "Ботать_это_круто. Очень_круто"
def sec_lv(b):
    if b == 'find':
        for i in range(len(text_2)):
            if text_2[i:i+5] == 'круто':
                return i
    elif b == 'replace':
        for i in range(len(text_2)):
            if text_2[i:i+5] == 'круто':
                return text_2.replace('круто', 'изнурительно')
    elif b == 'count':
        k = 0
        for i in range(len(text_2)):
            if text_2[i] == 'о' or text_2[i] == 'О':
                k += 1
        return k
print(sec_lv(b))


c = str(input())
def third_lv(c):
    t_3 = "1, 2, 3, 4"
    if c == 'split':
        r = str(input())
        t_3 = t_3.split(r)
        return t_3
    elif c == 'split & join':
        r1 = str(input())
        r2 = str(input())
        t_3 = t_3.split(r1)
        t_3 = r2.join(t_3)
        return t_3
    elif c == 'join':
        r = str(input())
        t_3 = r.join(t_3)
        return t_3
print(third_lv(c))

d = str(input())
def fourth_lv(d):
    t_4 = str(input())
    if d == 'isdigit':
        return t_4.isdigit()
    elif d == 'isalpha':
        return t_4.isalpha()
    elif d == 'strip':
        r = str(input())
        return t_4.strip(r)
    elif d == 'format':
        return "{:.2f}".format(float(t_4))
    elif d == 'r':
        return t_4[::-1]
    elif d == 'l':
        return t_4.lower()
    elif d == 'f':
        return t_4.upper()
print(fourth_lv(d))

t_5 = '    pYtHon;is;AWESome    '
def fifth_lv(t_5):
    return t_5.strip().replace(';', ', ').upper().capitalize()
print(fifth_lv(t_5))

