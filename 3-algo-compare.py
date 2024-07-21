import timeit
from collections import defaultdict

# Функція для обчислення префіксної функції (LPS)
def compute_lps(pattern):
    lps = [0] * len(pattern)
    length = 0
    i = 1

    while i < len(pattern):
        if pattern[i] == pattern[length]:
            length += 1
            lps[i] = length
            i += 1
        else:
            if length != 0:
                length = lps[length - 1]
            else:
                lps[i] = 0
                i += 1

    return lps

# Алгоритм Кнута-Морріса-Пратта
def kmp_search(main_string, pattern):
    M = len(pattern)
    N = len(main_string)

    lps = compute_lps(pattern)

    i = j = 0

    while i < N:
        if pattern[j] == main_string[i]:
            i += 1
            j += 1
        elif j != 0:
            j = lps[j - 1]
        else:
            i += 1

        if j == M:
            return i - j

    return -1  # якщо підрядок не знайдено

# Алгоритм Боєра-Мура
def boyer_moore(text, pattern):
    m, n = len(pattern), len(text)
    if m > n:
        return -1
    skip = defaultdict(lambda: m)
    for i in range(m - 1):
        skip[pattern[i]] = m - i - 1
    s = 0
    while s <= n - m:
        j = m - 1
        while j >= 0 and pattern[j] == text[s + j]:
            j -= 1
        if j < 0:
            return s
        s += skip[text[s + m - 1]]
    return -1

# Алгоритм Рабіна-Карпа
def rabin_karp(text, pattern, d=256, q=101):
    m, n = len(pattern), len(text)
    h, p, t = pow(d, m-1) % q, 0, 0
    for i in range(m):
        p = (d * p + ord(pattern[i])) % q
        t = (d * t + ord(text[i])) % q
    for s in range(n - m + 1):
        if p == t and text[s:s+m] == pattern:
            return s
        if s < n - m:
            t = (t - ord(text[s]) * h) % q
            t = (t * d + ord(text[s + m])) % q
            t = (t + q) % q
    return -1

# Читання текстів із файлів
def read_file(file_path):
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
        return file.read()

article1 = read_file('стаття1.txt')
article2 = read_file('стаття2.txt')

# Підрядки для пошуку
existing_substring = "алгоритм"
fake_substring = "неіснуючийпідрядок"

# Вимірювання часу виконання
algorithms = [boyer_moore, kmp_search, rabin_karp]
results = {algo.__name__: {} for algo in algorithms}

for algo in algorithms:
    for art, art_name in [(article1, 'стаття 1'), (article2, 'стаття 2')]:
        try:
            real_time = timeit.timeit(lambda: algo(art, existing_substring), number=10)
            fake_time = timeit.timeit(lambda: algo(art, fake_substring), number=10)
            results[algo.__name__][f'{art_name} з існуючим'] = real_time
            results[algo.__name__][f'{art_name} з вигаданим'] = fake_time
        except Exception as e:
            print(f"Помилка при виконанні {algo.__name__} з {art_name}: {e}")

# Вивід результатів
fastest_algo = {}
for name, times in results.items():
    print(f"\nАлгоритм: {name}")
    for test, time in times.items():
        print(f"{test}: {time:.6f} секунд")
        if test not in fastest_algo or time < fastest_algo[test][1]:
            fastest_algo[test] = (name, time)

# Висновки
print("\nВисновки:")
for test, (name, time) in fastest_algo.items():
    print(f"Для {test}, найшвидший алгоритм: {name} з часом: {time:.6f} секунд")

# Висновки у форматі markdown
markdown_output = "# Висновки\n"
for test, (name, time) in fastest_algo.items():
    markdown_output += f"Для **{test}**, найшвидший алгоритм: **{name}** з часом: **{time:.6f} секунд**\n"

with open('results.md', 'w', encoding='utf-8') as f:
    f.write(markdown_output)