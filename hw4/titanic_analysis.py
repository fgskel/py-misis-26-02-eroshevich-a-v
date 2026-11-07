import sys
from pathlib import Path

import numpy as np
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR / "data" / "tested.csv"
PROCESSED_PATH = BASE_DIR / "titanic_processed.csv"
STATS_PATH = BASE_DIR / "titanic_statistics.csv"

pd.set_option("display.width", 200)
pd.set_option("display.max_columns", 20)


def section(title):
    print("\n" + "=" * 70)
    print(title)
    print("=" * 70)


def ask_rows_count(max_rows):
    while True:
        raw = input(f"Сколько первых строк вывести? (целое число от 1 до {max_rows}): ").strip()
        try:
            n = int(raw)
        except ValueError:
            print("Нужно ввести целое число, например 5. Попробуйте ещё раз.")
            continue
        if n < 1:
            print("Число должно быть больше нуля.")
            continue
        if n > max_rows:
            print(f"В таблице всего {max_rows} строк, будут показаны все.")
            return max_rows
        return n


def age_stats(series):
    return pd.Series({
        "Среднее арифметическое": series.mean(),
        "Медиана": series.median(),
        "Минимальный возраст": series.min(),
        "Максимальный возраст": series.max(),
        "Стандартное отклонение": series.std(),
        "Количество известных значений": series.count(),
    })


def mean_or_nan(values):
    values = values[~np.isnan(values)]
    return values.mean() if values.size else np.nan


def main():
    if not DATA_PATH.exists():
        print(f"Файл {DATA_PATH} не найден. Положите tested.csv в папку data рядом со скриптом.")
        sys.exit(1)

    # Часть II. Загрузка и первичный анализ
    section("ЧАСТЬ II. Загрузка и первичный анализ данных")
    df = pd.read_csv(DATA_PATH, dtype={"Ticket": str})
    rows_before, cols_before = df.shape

    n = ask_rows_count(len(df))
    print(f"\nПервые {n} строк:")
    print(df.head(n))
    print("\nПоследние 5 строк:")
    print(df.tail(5))

    print(f"\nСтрок: {df.shape[0]}, столбцов: {df.shape[1]}")
    print("\nНазвания столбцов:")
    print(list(df.columns))
    print("\nТипы данных:")
    print(df.dtypes)

    numeric_cols = ["Age", "SibSp", "Parch", "Fare"]
    categorical_cols = ["Survived", "Pclass", "Sex", "Embarked", "Name", "Ticket", "Cabin"]
    print("\nЧисловые признаки:", numeric_cols)
    print("Категориальные признаки:", categorical_cols)
    print("PassengerId - просто идентификатор строки, в анализе не участвует.")

    print("\nОсновные статистики числовых признаков:")
    summary = df[numeric_cols].agg(["mean", "median", "min", "max", "std"]).T
    summary.columns = ["среднее", "медиана", "минимум", "максимум", "ст. откл."]
    print(summary.round(2))

    print("\nКоличество пассажиров по классам:")
    print(df["Pclass"].value_counts().sort_index())
    print("\nУникальных значений в Embarked:", df["Embarked"].nunique())
    print("Сами значения:", sorted(df["Embarked"].dropna().unique()))

    # Часть III. Пропуски
    section("ЧАСТЬ III. Обработка пропущенных значений")
    missing = df.isna().sum()
    missing_pct = (missing / len(df) * 100).round(2)
    print(pd.DataFrame({"пропусков": missing, "процент": missing_pct}))
    print("\nСтолбец с наибольшим числом пропусков:", missing.idxmax(),
          f"({missing.max()} шт.)")

    age_known = df["Age"].copy()
    before = age_stats(df["Age"])

    # Медиана считается один раз по исходным данным, до заполнения.
    age_median = df["Age"].median()
    df["Age"] = df["Age"].fillna(age_median)
    after = age_stats(df["Age"])

    comparison = pd.DataFrame({"До обработки": before, "После обработки": after}).round(2)
    print("\nСравнение возраста до и после заполнения медианой "
          f"({age_median}):")
    print(comparison)

    embarked_missing = df["Embarked"].isna().sum()
    df = df.dropna(subset=["Embarked"])
    print(f"\nУдалено строк без Embarked: {embarked_missing}")

    cabin_share = df["Cabin"].isna().mean() * 100
    print(f"Доля пропусков в Cabin: {cabin_share:.1f}%")
    if cabin_share > 50:
        df = df.drop(columns="Cabin")
        print("Столбец Cabin удалён.")

    print("\nОставшиеся пропуски:")
    print(df.isna().sum())
    print(f"\nДо обработки: {rows_before} строк, {cols_before} столбцов")
    print(f"После обработки: {df.shape[0]} строк, {df.shape[1]} столбцов")

    # Для анализа берём только реальные возрасты: подставленная медиана
    # исказила бы средние по группам и сравнение по полу.
    an = df.copy()
    an["Age"] = age_known.loc[an.index]

    # Часть IV. NumPy
    section("ЧАСТЬ IV. Анализ данных с помощью NumPy")
    survived = an["Survived"].to_numpy()
    sex = an["Sex"].to_numpy()
    age = an["Age"].to_numpy(dtype=float)
    fare = an["Fare"].to_numpy(dtype=float)

    male = sex == "male"
    female = sex == "female"
    alive = survived == 1
    dead = survived == 0

    print(f"Выжило всего: {survived.mean() * 100:.2f}%")
    print(f"Среди мужчин: {survived[male].mean() * 100:.2f}%")
    print(f"Среди женщин: {survived[female].mean() * 100:.2f}%")
    print(f"\nСредний возраст мужчин: {mean_or_nan(age[male]):.3f}")
    print(f"Средний возраст женщин: {mean_or_nan(age[female]):.3f}")

    print(f"\nСтоимость билета: min = {np.nanmin(fare):.2f}, "
          f"max = {np.nanmax(fare):.2f}, mean = {np.nanmean(fare):.2f}")
    print(f"Стандартное отклонение возраста (по известным значениям): {np.nanstd(age, ddof=1):.2f}")

    comparison_np = pd.DataFrame({
        "Мужчины": [
            male.sum(),
            survived[male].mean() * 100,
            mean_or_nan(age[male]),
            mean_or_nan(age[male & alive]),
            mean_or_nan(age[male & dead]),
        ],
        "Женщины": [
            female.sum(),
            survived[female].mean() * 100,
            mean_or_nan(age[female]),
            mean_or_nan(age[female & alive]),
            mean_or_nan(age[female & dead]),
        ],
    }, index=[
        "Количество пассажиров",
        "Доля выживших, %",
        "Средний возраст",
        "Средний возраст выживших",
        "Средний возраст погибших",
    ]).round(3)
    print("\nСравнение мужчин и женщин:")
    print(comparison_np)

    # Часть V. Фильтрация
    section("ЧАСТЬ V. Фильтрация данных")
    task1 = an[(an["Sex"] == "male") & (an["Age"] > 30) & (an["Pclass"] == 1)]
    print(f"Задание 1. Мужчины старше 30 лет в первом классе: {len(task1)}")
    print(task1.head(10))

    # "Моложе 18 или женщины, которые выжили": условие выживания относится к женщинам.
    task2 = an[(an["Age"] < 18) | ((an["Sex"] == "female") & (an["Survived"] == 1))]
    print(f"\nЗадание 2. Моложе 18 лет или выжившие женщины: {len(task2)}")

    third = an[an["Pclass"] == 3]
    mean_fare_third = third["Fare"].mean()
    task3 = third[third["Fare"] > mean_fare_third]
    print(f"\nЗадание 3. Средняя стоимость билета в 3 классе: {mean_fare_third:.2f}")
    print(f"Пассажиров дороже среднего: {len(task3)}")
    print(task3.head(10))

    task4 = an[an["Age"].between(20, 40) & (an["Embarked"] == "S")]
    print(f"\nЗадание 4. Возраст 20-40 лет, порт S: {len(task4)}")

    # Часть VI. Группировка
    section("ЧАСТЬ VI. Группировка и агрегирование")
    by_class_sex = an.groupby(["Pclass", "Sex"]).agg(
        passengers=("PassengerId", "count"),
        mean_age=("Age", "mean"),
        survived_pct=("Survived", lambda s: s.mean() * 100),
        mean_fare=("Fare", "mean"),
    ).round(2).reset_index()
    print("По классу и полу:")
    print(by_class_sex)

    by_port = an.groupby("Embarked").agg(
        passengers=("PassengerId", "count"),
        survived_pct=("Survived", lambda s: s.mean() * 100),
    ).round(2)
    print("\nПо порту посадки:")
    print(by_port)

    class_survival = an.groupby("Pclass")["Survived"].mean() * 100
    print("\nДоля выживших по классам, %:")
    print(class_survival.round(2))
    print(f"Наибольшая доля выживших - в классе {class_survival.idxmax()} "
          f"({class_survival.max():.2f}%)")

    # Часть VII. Сохранение
    section("ЧАСТЬ VII. Сохранение результатов")
    df.to_csv(PROCESSED_PATH, index=False)
    by_class_sex.to_csv(STATS_PATH, index=False)
    print(f"Сохранено: {PROCESSED_PATH.name}, {STATS_PATH.name}")

    reloaded = pd.read_csv(PROCESSED_PATH, dtype={"Ticket": str})
    try:
        pd.testing.assert_frame_equal(
            reloaded, df.reset_index(drop=True), check_dtype=False
        )
        print("Проверка пройдена: данные в titanic_processed.csv совпадают с исходным DataFrame.")
    except AssertionError as error:
        print("Данные после перезагрузки отличаются:")
        print(error)
    print("Форма перезагруженной таблицы:", reloaded.shape)


if __name__ == "__main__":
    main()
