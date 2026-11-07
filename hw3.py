import random

SIZE = 5
ROOM_TYPES = ["пусто", "сундук", "монстр", "ловушка", "портал"]
LOOT = ["золото", "зелье", "меч", "щит", "карта"]
ICONS = {"пусто": "⬜️", "сундук": "🎁", "монстр": "☠️", "ловушка": "⚠️",
         "портал": "🌀", "ключ": "🔑", "старт": "🏁", "выход": "🚪"}


def gen_maze(size):
    maze = [[{"type": random.choice(ROOM_TYPES), "visited": False}
             for i in range(size)] for i in range(size)]
    maze[0][0]["type"] = "старт"
    maze[size - 1][size - 1]["type"] = "выход"
    # ключ гарантированно кладём в случайную комнату
    free = [(i, j) for i in range(size) for j in range(size)
            if (i, j) not in [(0, 0), (size - 1, size - 1)]]
    kx, ky = random.choice(free)
    maze[kx][ky]["type"] = "ключ"
    return maze


def show_map(maze, pos):
    for i, row in enumerate(maze):
        line = ""
        for j, room in enumerate(row):
            if [i, j] == pos:
                line += "🧍"
            elif room["visited"]:
                line += ICONS[room["type"]]
            else:
                line += "❓"
        print(line)


def fight(state):
    monster_hp = random.randint(20, 40)
    print(f"Монстр! У него {monster_hp} HP")
    while monster_hp > 0 and state["hp"] > 0:
        print(f"Монстр: {monster_hp} HP | Вы: {state['hp']} HP")
        action = input("1 - атака, 2 - зелье, 3 - бежать: ")
        if action == "1":
            dmg = random.randint(5, 15) + (5 if "меч" in state["inv"] else 0)
            monster_hp -= dmg
            print(f"Вы нанесли {dmg} урона")
        elif action == "2":
            if "зелье" in state["inv"]:
                state["inv"].remove("зелье")
                state["hp"] = min(100, state["hp"] + 30)
                print("+30 HP")
            else:
                print("Нет зелья!")
        elif action == "3":
            if random.random() < 0.5:
                print("Вы сбежали!")
                return
            print("Не удалось сбежать!")
        else:
            continue
        if monster_hp > 0:
            hit = random.randint(5, 12)
            state["hp"] -= hit
            print(f"Монстр бьёт на {hit}")
    if state["hp"] > 0:
        print("Монстр побеждён! Выпало: золото")
        state["inv"].append("золото")


def enter_room(maze, state):
    x, y = state["pos"]
    room = maze[x][y]
    if room["visited"]:
        return
    room["visited"] = True
    kind = room["type"]
    print(f"\n>>> Комната: {kind}")

    if kind == "сундук":
        items = random.sample(LOOT, random.randint(1, 3))
        print(f"В сундуке: {items}")
        state["inv"].extend(items)
    elif kind == "ключ":
        print("Вы нашли ключ!")
        state["inv"].append("ключ")
    elif kind == "ловушка":
        dmg = random.randint(10, 25)
        if "щит" in state["inv"]:
            dmg //= 2
            print("Щит смягчил удар!")
        state["hp"] -= dmg
        print(f"Ловушка! -{dmg} HP")
    elif kind == "монстр":
        fight(state)
    elif kind == "портал":
        state["pos"] = [random.randrange(SIZE), random.randrange(SIZE)]
        print("Портал телепортировал вас!")
        enter_room(maze, state)


def inventory_menu(state):
    inv = state["inv"]
    while True:
        print(f"\nИнвентарь: {inv}")
        c = input("1 - сортировать, 2 - выбросить, 3 - выпить зелье, 0 - назад: ")
        if c == "1":
            inv.sort()
        elif c == "2":
            name = input("Что выбросить? ")
            if name in inv:
                inv.remove(name)
            else:
                print("Нет такого предмета")
        elif c == "3":
            if "зелье" in inv:
                inv.remove("зелье")
                state["hp"] = min(100, state["hp"] + 30)
                print("+30 HP")
            else:
                print("Нет зелья")
        elif c == "0":
            return


def main():
    global maze
    maze = gen_maze(SIZE)
    state = {"hp": 100, "inv": [], "pos": [0, 0]}
    maze[0][0]["visited"] = True
    moves = {"w": (-1, 0), "s": (1, 0), "a": (0, -1), "d": (0, 1)}
    while state["hp"] > 0:
        show_map(maze, state["pos"])
        print(f"HP: {state['hp']} | Инвентарь: {state['inv']}")
        enter_room(maze, state)
        if state["hp"] <= 0:
            break
        if state["pos"] == [SIZE - 1, SIZE - 1]:
            if "ключ" in state["inv"]:
                print("🎉 Вы открыли выход и победили!")
                return
            print("Выход заперт, нужен ключ.")

        cmd = input("w/a/s/d - идти, i - инвентарь, q - выход: ").lower()
        if cmd == "q":
            return
        elif cmd == "i":
            inventory_menu(state)
        elif cmd in moves:
            nx = state["pos"][0] + moves[cmd][0]
            ny = state["pos"][1] + moves[cmd][1]
            if 0 <= nx < SIZE and 0 <= ny < SIZE:
                state["pos"] = [nx, ny]
            else:
                print("Там стена!")
    print("💀 Вы проиграли")


if __name__ == "__main__":
    main()
    