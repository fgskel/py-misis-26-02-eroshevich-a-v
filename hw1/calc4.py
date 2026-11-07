class daily_energy:
    def __init__(self, weight, height, age, gender, activity):
        self.weight = weight
        self.height = height
        self.age = age
        self.gender = gender
        self.activity = activity
    def BMR(self):
        if self.gender == 'female': return 10 * self.weight + 6.25 * self.height - 5 * self.age - 161
        elif self.gender == 'male': return 10 * self.weight + 6.25 * self.height - 5 * self.age + 5
    def TDEE(self):
        if self.activity == 'zero': return self.BMR() * 1.2
        elif self.activity == 'light': return self.BMR() * 1.375
        elif self.activity == 'medium': return self.BMR() * 1.55
        elif self.activity == 'high': return self.BMR() * 1.725

me = daily_energy(44, 164, 17, 'female', 'light')
print('Ваша норма базового метаболизма:', me.BMR())
print('Ваш суточный расход энергии:', me.TDEE())

