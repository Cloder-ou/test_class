# 數學運算解說

涵蓋 **小學、國中、高中、大學** 四個學習等級，所有範例皆有可執行的 Python 程式碼（見 `math_tutorial.py`）。

## 小學：四則運算與分數

- 先乘除後加減：`7 + 3 * 4 = 19`
- 括號優先：`(7 + 3) * 4 = 40`
- 除法：`12 / 4 + 2 = 5.0`
- 餘數：`10 % 3 = 1`
- 平方：`10 ** 2 = 100`
- 分數加法：`1/2 + 2/3 = 7/6`
- 平均：`(3 + 7 + 2 + 9 + 5) / 5 = 5.2`

```python
from fractions import Fraction   # 引入分數模組，可精確表示分數

f1 = Fraction(1, 2)              # 分數 1/2
f2 = Fraction(2, 3)              # 分數 2/3
print(f1 + f2)                   # 通分後相加 → 7/6
```

## 國中：代數、方程式與根號

- 一次方程式：`3x + 5 = 20 → x = 5`
- 一元二次方程式公式解：
  - `x² - 5x + 6 = 0 → x = 3, 2`
  - 判別式 `D = b² - 4ac`
- 根號運算：`√2 + √8 = √2 + 2√2 ≈ 4.242641`
- 畢氏定理：`3² + 4² = c² → c = 5`

```python
import math                  # 引入 math 模組，提供 sqrt 等數學函式

a, b, c = 1, -5, 6           # 一元二次方程式的三個係數
d = b * b - 4 * a * c        # 判別式 D = b² - 4ac
x1 = (-b + math.sqrt(d)) / (2 * a)   # 公式解的第一個根 → 3.0
x2 = (-b - math.sqrt(d)) / (2 * a)   # 公式解的第二個根 → 2.0
print(x1, x2)                # 輸出兩根：3.0 2.0
```

## 高中：三角函數、指數對數、微積分

- 三角函數：`sin(π/3) ≈ 0.8660`、`cos(π/3) ≈ 0.5000`、`tan(π/3) ≈ 1.7321`
- 指數對數：`e² ≈ 7.3891`、`ln(e²) = 2`、`log₁₀(1000) = 3`
- 微分（數值逼近）：`d/dx (x³ + 2x² + x)` 在 `x = 2` 處 ≈ `21`
- 定積分（黎曼和）：`∫₀¹ x² dx ≈ 0.333328`（理論值 `1/3`）
- 統計：擲骰子 6 次結果的平均與標準差

```python
import math   # 引入 math 模組（三角、指數、對數皆需使用）

# 數值微分：以差分公式近似導數 d/dx f(x) ≈ (f(x+h) - f(x)) / h
h = 1e-7                        # 極小的增量 h
def f(x):                       # 定義多項式函式 f(x)
    return x**3 + 2 * x**2 + x
x = 2
derivative = (f(x + h) - f(x)) / h    # 在 x=2 的導數 → ≈ 21.000001
print(derivative)               # 輸出 ≈ 21.000001（理論值 21）

# 數值積分：以黎曼和近似定積分 ∫₀¹ x² dx
n = 100000                      # 切割段數，愈大愈精確
integral = sum((i / n) ** 2 for i in range(n)) / n   # 每個小長方形相加
print(integral)                 # 輸出 ≈ 0.333328（理論值 1/3）

# 三角函數與對數（單位為弧度）
theta = math.pi / 3             # 60°
print(math.sin(theta))          # ≈ 0.8660
print(math.log10(1000))         # 3.0
```

## 大學：線性代數、機率、數值分析

- 矩陣乘法：`A · I = A`
- 行列式：`det(A) = 10`
- 反矩陣：`A⁻¹ = [[0.3, -0.2], [-0.1, 0.4]]`
- 特徵值：`A` 的 `λ = 5, 2`
- 常態分布：`N(0,1)` 抽樣 1000 筆的平均與標準差
- 蒙地卡羅方法：估算 `π ≈ 3.1372`
- 泰勒級數：`Σ xⁿ/n!` 估計 `e² ≈ 7.389056`
- 極限（數值逼近）：`lim(x→0) sin(x)/x ≈ 1`

```python
import math                      # 引入 math 模組（行列式與特徵值計算用）
import random                    # 引入 random 模組（蒙地卡羅抽樣用）

def mat_mul(A, B):               # 自訂矩陣乘法函式
    """兩矩陣相乘：A(m×k) 與 B(k×n) → C(m×n)"""
    m, k, n = len(A), len(B), len(B[0])
    return [[sum(A[i][t] * B[t][j] for t in range(k)) for j in range(n)] for i in range(m)]

# 定義 2×2 矩陣 A 與單位矩陣 I
A = [[4.0, 2.0], [1.0, 3.0]]
I = [[1.0, 0.0], [0.0, 1.0]]
print(mat_mul(A, I))             # A·I = A → [[4.0, 2.0], [1.0, 3.0]]

# 2×2 行列式 det = ad - bc
det = A[0][0] * A[1][1] - A[0][1] * A[1][0]
print(det)                       # 10.0

# 特徵值：解 det(A - λI) = 0（2×2 手算公式）
trace = A[0][0] + A[1][1]        # 跡 = a + d = 7
disc = math.sqrt(trace * trace - 4 * det)  # √(49 - 40) = 3
lambda1 = (trace + disc) / 2     # 5.0
lambda2 = (trace - disc) / 2     # 2.0
print(lambda1, lambda2)          # 5.0 2.0

# 蒙地卡羅法估算 π：隨機丟點，落在單位圓內的比例 × 4
random.seed(42)                  # 固定隨機種子，結果可重現
inside = sum(random.random() ** 2 + random.random() ** 2 <= 1 for _ in range(100000))
print(4 * inside / 100000)       # ≈ 3.1372
```

## 執行方式

```bash
python 0816/math_tutorial.py
```
