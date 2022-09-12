from time import perf_counter
from re import search, sub
from os import get_terminal_size


def runtime_counter(main):
    def wrapper(*args, **kwargs):
        global wasted_time; wasted_time = list()

        start = perf_counter()

        main(*args, **kwargs)

        end = perf_counter()
        print(f"\nEnd in {round((end - start) - sum(wasted_time), 2)}s")
    return wrapper


def wastetime_counter(func):
    def wrapper(*args, **kwargs):
        start = perf_counter()

        res = func(*args, **kwargs)

        end = perf_counter()

        wasted_time.append(end - start)
        return res
    return wrapper


def hash_key(key):
    if key == "":
        return key

    preFix = "#90091"
    add_preFix = True

    if search(rf"^{preFix}", key):
        key = sub(rf"^{preFix}", "", key)
        add_preFix = False

    abc = "ulOXntwCgdiNkMfvhbLKxzWErVFHcDjSyTJPaeUZqosBAIRmpYQG"
    ABC = "KwCWaVlOhTFEHpvfgSeuDcXNqtikzxAbIdGYnLZUrBQojymRMPsJ"
    numbers = "2016574398"
    NUMBERS = "3650198274"
    symbols = "@_!~^|%#-+*=&$"
    SYMBOLS = "^~-_@%|*!$#&=+"

    hashed_key = ""

    for n in key:
        if n in abc:
            for num in range(len(abc)):
                if n == abc[num]:
                    n = ABC[num]
                    hashed_key += n
                    break
        elif n in numbers:
            for num in range(len(numbers)):
                if n == numbers[num]:
                        n = NUMBERS[num]
                        hashed_key += n
                        break
        elif n in symbols:
            for num in range(len(symbols)):
                if n == symbols[num]:
                        n = SYMBOLS[num]
                        hashed_key += n
                        break
        else:
            hashed_key += n
    
    if add_preFix:
        return preFix + hashed_key

    return hashed_key


def log_progress(iteration, total, prefix="", suffix="", decimals=1, length=100, fill="█", print_end="\r", auto_size=False):
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    if auto_size:
        styling = f"{prefix} |{fill}| {percent}% {suffix}"
        terminal_width = get_terminal_size()[0]
        length = terminal_width - len(styling)
    filled_length = int(length * iteration // total)
    bar = fill * filled_length + "-" * (length - filled_length)
    print(f"\r{prefix} |{bar}| {percent}% {suffix}", end=print_end)

    if iteration == total: 
        print()


def log_loading(i, text="", character=".", count=3, prefix=""):
    print(f"{prefix}{text}{i * character}{count * ' '}\r", end="\r")

    if i == count:
        i = 1
    else:
        i += 1

    return i
