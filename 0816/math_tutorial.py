# 數學運算解說：小學 / 國中 / 高中 / 大學
# 每個等級都有可直接執行的範例，只需 Python 標準函式庫。

import math
import random
import statistics
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


if __name__ == "__main__":
    primary_school()
    junior_high()
    senior_high()
    university()
