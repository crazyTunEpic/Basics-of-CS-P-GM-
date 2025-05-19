import ctypes
import sys

# библиотека
lib = ctypes.CDLL('./libgoldbach.so')

lib.calculate_primes.argtypes = [
    ctypes.c_int,
    ctypes.POINTER(ctypes.POINTER(ctypes.c_int)),
    ctypes.POINTER(ctypes.c_int)
]
lib.calculate_primes.restype = None

def goldbach_conjecture(n):
    """Проверка гипотезы Гольдбаха для четного числа n."""
    if n % 2 != 0 or n <= 2:
        print("Число должно быть четным и больше 2")
        return
    
    # получение простых чисел до n
    primes_ptr = ctypes.POINTER(ctypes.c_int)()
    primes_count = ctypes.c_int()
    
    lib.calculate_primes(n, ctypes.byref(primes_ptr), ctypes.byref(primes_count))
    
    # преобразование в список
    primes = [primes_ptr[i] for i in range(primes_count.value)]
    
    # проверка гипотезы
    found = False
    for i in range(primes_count.value):
        if primes[i] > n // 2:
            break
        if (n - primes[i]) in primes:
            print(f"{n} = {primes[i]} + {n - primes[i]}")
            found = True
            break
    
    if not found:
        print(f"Для числа {n} не найдено разложение по гипотезе Гольдбаха")
    
    # освобождение памяти
    lib.free(primes_ptr)

def main():
    print("Проверка гипотезы Гольдбаха")
    print("Четное число можно представить в виде суммы двух простых чисел")
    
    try:
        n = int(input("Введите четное число больше 2: "))
        goldbach_conjecture(n)
    except ValueError:
        print("Ошибка: введите целое число")

if __name__ == "__main__":
    main()
