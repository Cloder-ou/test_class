# 數學運算解說：小學 / 國中 / 高中 / 大學
# 每個等級都有可直接執行的範例，只需 Python 標準函式庫。

import math
import random
import statistics
import sys
from fractions import Fraction


def primary_school():
    print("=" * 60)
    print("【小學】四則運算與分數")
    print("=" * 60)
    print("7 + 3 * 4 =", 7 + 3 * 4)
    print("(7 + 3) * 4 =", (7 + 3) * 4)
    print("12 / 4 + 2 =", 12 / 4 + 2)
    print("10 % 3 =", 10 % 3, "（餘數）")
    print("10 ** 2 =", 10**2, "（平方）")

    f1 = Fraction(1, 2)
    f2 = Fraction(2, 3)
    print(f"分數加法 1/2 + 2/3 = {f1 + f2}")

    numbers = [3, 7, 2, 9, 5]
    print("數字:", numbers, "→ 平均 =", sum(numbers) / len(numbers))


def junior_high():
    print("=" * 60)
    print("【國中】代數、一元二次方程式與根號")
    print("=" * 60)

    a, b, c = 1, -5, 6
    d = b * b - 4 * a * c
    x1 = (-b + math.sqrt(d)) / (2 * a)
    x2 = (-b - math.sqrt(d)) / (2 * a)
    print(f"公式解 x² - 5x + 6 = 0 → x = {x1}, {x2}")

    print(f"解一次方程式 3x + 5 = 20 → x = {(20 - 5) / 3}")

    print("√2 ≈", round(math.sqrt(2), 6))
    print("√2 + √8 = √2 + 2√2 ≈", round(math.sqrt(2) + math.sqrt(8), 6))

    a, b = 3, 4
    c = math.hypot(a, b)
    print(f"畢氏定理: 直角邊 {a}、{b} → 斜邊 = {c}")


def senior_high():
    print("=" * 60)
    print("【高中】三角函數、指數對數、微分積分")
    print("=" * 60)

    theta = math.pi / 3
    print(f"sin(π/3) ≈ {math.sin(theta):.4f}, cos(π/3) ≈ {math.cos(theta):.4f}, tan(π/3) ≈ {math.tan(theta):.4f}")

    print(f"e² ≈ {math.exp(2):.4f}，ln(e²) = {math.log(math.exp(2)):.4f}")
    print(f"log₁₀(1000) = {math.log10(1000)}")

    h = 1e-7
    def f(x):
        return x**3 + 2 * x**2 + x
    derivative = (f(2 + h) - f(2)) / h
    print(f"d/dx (x³ + 2x² + x) 在 x=2 處 ≈ {derivative:.6f}（理論值 {3*4+4*2+1}）")

    n = 100000
    integral = sum((i / n) ** 2 for i in range(n)) / n
    print(f"∫₀¹ x² dx ≈ {integral:.6f}（理論值 1/3 ≈ {1/3:.6f}）")

    v = random.sample(range(1, 7), 6)
    print(f"擲骰子 6 次結果 {v} → 平均 {statistics.mean(v)}，樣本標準差 {statistics.stdev(v):.2f}")


def university():
    print("=" * 60)
    print("【大學】線性代數、機率、數值分析")
    print("=" * 60)

    def mat_mul(A, B):
        return [[sum(A[i][k] * B[k][j] for k in range(len(B))) for j in range(len(B[0]))] for i in range(len(A))]

    A = [[4.0, 2.0], [1.0, 3.0]]
    I = [[1.0, 0.0], [0.0, 1.0]]
    print("矩陣乘法 A·I:")
    for row in mat_mul(A, I):
        print(" ", row)

    det = A[0][0] * A[1][1] - A[0][1] * A[1][0]
    inv = [[A[1][1] / det, -A[0][1] / det], [-A[1][0] / det, A[0][0] / det]]
    print(f"A 的行列式 det = {det}")
    print("A 的反矩陣:")
    for row in inv:
        print(" ", row)

    trace = A[0][0] + A[1][1]
    disc = math.sqrt(trace * trace - 4 * det)
    print(f"A 的特徵值 λ = {(trace + disc) / 2:.3f}, {(trace - disc) / 2:.3f}")

    rng = random.Random(42)
    samples = [rng.gauss(0.0, 1.0) for _ in range(1000)]
    print(f"常態分布 N(0,1) 抽樣 1000 筆 → 平均 {statistics.mean(samples):.3f}，標準差 {statistics.stdev(samples):.3f}")

    inside = sum(rng.random() ** 2 + rng.random() ** 2 <= 1 for _ in range(100000))
    print(f"蒙地卡羅估計 π ≈ {4 * inside / 100000:.4f}")

    def taylor_exp(x, terms=20):
        total, term = 0.0, 1.0
        for n in range(terms):
            total += term
            term *= x / (n + 1)
        return total
    print(f"泰勒級數 Σ xⁿ/n! 估計 e² ≈ {taylor_exp(2):.6f}（實際 {math.exp(2):.6f}）")

    h = 1e-7
    limit = (math.sin(h) / h + math.sin(-h) / -h) / 2
    print(f"極限 lim(x→0) sin(x)/x ≈ {limit:.6f}")


def primary_interactive():
    print("=" * 60)
    print("【小學·互動】簡易四則運算器")
    print("=" * 60)
    a = float(input("請輸入第一個數字: "))
    b = float(input("請輸入第二個數字: "))
    op = input("請輸入運算子 (+ - * /): ")

    if op == "+":
        print(f"{a} + {b} = {a + b}")
    elif op == "-":
        print(f"{a} - {b} = {a - b}")
    elif op == "*":
        print(f"{a} * {b} = {a * b}")
    elif op == "/":
        if b == 0:
            print("錯誤: 不能除以 0")
        else:
            print(f"{a} / {b} = {a / b}")
    else:
        print(f"不支援的運算子: {op}")


def junior_interactive():
    print("=" * 60)
    print("【國中·互動】一元二次方程式求解 ax² + bx + c = 0")
    print("=" * 60)
    a = float(input("請輸入 a: "))
    b = float(input("請輸入 b: "))
    c = float(input("請輸入 c: "))

    if a == 0:
        print("這不是二次方程式 (a 不能為 0)")
        return
    d = b * b - 4 * a * c
    print(f"判別式 D = {d}")
    if d > 0:
        x1 = (-b + math.sqrt(d)) / (2 * a)
        x2 = (-b - math.sqrt(d)) / (2 * a)
        print(f"兩相異實根: x = {x1:.4f}, {x2:.4f}")
    elif d == 0:
        x = -b / (2 * a)
        print(f"重根: x = {x:.4f}")
    else:
        print("無實數解（有兩個共軛複數根）")


def senior_interactive():
    print("=" * 60)
    print("【高中·互動】三角函數計算器")
    print("=" * 60)
    deg = float(input("請輸入角度（度）: "))
    func = input("請選擇 sin / cos / tan: ")

    rad = math.radians(deg)
    if func == "sin":
        print(f"sin({deg}°) = {math.sin(rad):.6f}")
    elif func == "cos":
        print(f"cos({deg}°) = {math.cos(rad):.6f}")
    elif func == "tan":
        if math.cos(rad) == 0:
            print("tan 在該角度無定義（cos = 0）")
        else:
            print(f"tan({deg}°) = {math.tan(rad):.6f}")
    else:
        print(f"不支援的函式: {func}")


def university_interactive():
    print("=" * 60)
    print("【大學·互動】2×2 矩陣計算（行列式、反矩陣、特徵值）")
    print("=" * 60)
    A = []
    for i in range(2):
        row = []
        for j in range(2):
            row.append(float(input(f"請輸入 A[{i + 1}][{j + 1}] = ")))
        A.append(row)

    print("您輸入的矩陣 A:")
    for row in A:
        print(" ", row)

    det = A[0][0] * A[1][1] - A[0][1] * A[1][0]
    print(f"行列式 det(A) = {det:.4f}")

    if det == 0:
        print("矩陣不可逆（奇異矩陣），無反矩陣")
    else:
        inv = [[A[1][1] / det, -A[0][1] / det],
               [-A[1][0] / det, A[0][0] / det]]
        print("反矩陣 A⁻¹:")
        for row in inv:
            print(" ", [round(v, 4) for v in row])

    trace = A[0][0] + A[1][1]
    disc = trace * trace - 4 * det
    if disc >= 0:
        s = math.sqrt(disc)
        print(f"特徵值 λ = {(trace + s) / 2:.4f}, {(trace - s) / 2:.4f}")
    else:
        s = math.sqrt(-disc)
        print(f"特徵值 λ = {trace / 2:.4f} ± {s / 2:.4f}i")


def interactive_menu():
    print("選擇互動範例:")
    print("1) 小學：四則運算器")
    print("2) 國中：一元二次方程式求解")
    print("3) 高中：三角函數計算器")
    print("4) 大學：2×2 矩陣計算")
    choice = input("請輸入編號 (1-4): ")
    if choice == "1":
        primary_interactive()
    elif choice == "2":
        junior_interactive()
    elif choice == "3":
        senior_interactive()
    elif choice == "4":
        university_interactive()
    else:
        print("無效的編號")


if __name__ == "__main__":
    if "--interactive" in sys.argv:
        interactive_menu()
    else:
        primary_school()
        junior_high()
        senior_high()
        university()
