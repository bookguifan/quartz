# [day07] 学习笔记｜面向对象编程（AI 增强版）

**📅 日期**：未提供 **⏱ 学习时长**：未提供 **🔧 AI 审核版本**：v3.6

## 📌 核心速览

- **面向对象（OOP）**：以"对象"为核心组织代码，三大特征：封装（隐藏实现细节）、继承（代码复用）、多态（同一接口不同实现）。
- **`self` 关键字**：类方法的第一个参数，代表实例自身。通过 `self.属性` 访问实例属性，通过 `self.方法()` 调用其他方法。
- **魔术方法**：以双下划线包围的特殊方法，如 `__init__`（构造）、`__str__`（字符串表示）、`__del__`（析构）、`__len__`（长度）、`__call__`（可调用）。
- **继承与 MRO**：子类继承父类的属性和方法；`super()` 调用父类方法；MRO（方法解析顺序）由 C3 线性化算法决定。
- **类属性 vs 实例属性**：类属性属于类（所有实例共享），实例属性属于实例（各自独立）。
- **类方法（`@classmethod`）与静态方法（`@staticmethod`）**：类方法接收 `cls` 参数，可访问类属性；静态方法不接收 `self`/`cls`，与普通函数无异但归属于类。
- **私有属性**：以双下划线 `__` 开头的属性，名称会被改写（name mangling）为 `_类名__属性名`，实现伪私有。

---

## 1️⃣ 完整知识库

### 面向对象基础 🔸 核心

#### 定义与本质

**面向过程 vs 面向对象**

| 维度 | 面向过程 | 面向对象 |
| :--- | :--- | :--- |
| **核心** | 步骤和函数 | 对象和数据 |
| **思维方式** | 怎么做（How） | 谁来做（Who） |
| **代码组织** | 按功能划分函数 | 按实体划分类 |
| **复用方式** | 函数调用 | 继承、组合 |
| **适用场景** | 小型脚本、算法 | 大型系统、GUI、游戏 |

**OOP 三大特征**

- **封装**：将数据和操作数据的方法绑定在一起，隐藏内部实现，对外暴露接口。
- **继承**：子类继承父类的特征，可以扩展或重写。
- **多态**：同一操作作用于不同对象，产生不同行为。

#### 基础用法

```python
class Dog:
    # 类属性（所有实例共享）
    species = "Canis familiaris"
    
    def __init__(self, name, age):
        # 实例属性（每个实例独立）
        self.name = name
        self.age = age
    
    def bark(self):
        return f"{self.name} says: Woof!"
    
    def __str__(self):
        return f"{self.name} is {self.age} years old"

# 创建实例
my_dog = Dog("Buddy", 3)
print(my_dog)           # Buddy is 3 years old
print(my_dog.bark())    # Buddy says: Woof!
print(Dog.species)      # Canis familiaris
```

**命名规范与类型注解**

| 类别 | 规范 | 示例 |
| :--- | :--- | :--- |
| 变量 / 函数 / 文件名 | **蛇形命名法（snake_case）**：全小写，下划线分隔 | `user_name`、`get_info()` |
| 类名 | **大驼峰（PascalCase）**：每个单词首字母大写，无下划线 | `ClassName` |
| 常量 | 全大写，下划线分隔 | `MAX_SIZE`、`PI` |
| 私有变量 / 方法（约定） | 单下划线 `_xxx`：模块/类内私有 | `_internal_val` |
| 强私有（名称改写） | 双下划线 `__xxx`：触发 name mangling | `__private_attr` |
| 避免关键字冲突 | 末尾单下划线 `xxx_` | `class_`、`type_` |

```python
# 类型注解：标注参数和返回值的预期类型（非强制，零开销）
def add(a: int, b: int) -> int:
    return a + b

name: str = "张三"
age: int = 18

# 类型注解不会阻止传入错误类型，只是提示
add("hello", "world")  # 运行时正常，返回 "helloworld"
```

---

### 魔术方法 🔸 核心

| 魔术方法 | 触发时机 | 用途 |
| :--- | :--- | :--- |
| `__init__(self)` | 创建实例后自动调用 | 初始化实例属性 |
| `__str__(self)` | `print()` 或 `str()` 时调用 | 友好的字符串表示 |
| `__repr__(self)` | `repr()` 或交互式输出时调用 | 官方字符串表示（通常可 eval） |
| `__del__(self)` | 实例被垃圾回收前调用 | 资源清理（极少直接使用） |
| `__len__(self)` | `len()` 时调用 | 定义对象长度 |
| `__call__(self)` | 实例像函数一样被调用时 | 让对象可调用 |
| `__eq__(self, other)` | `==` 比较时调用 | 自定义相等判断 |
| `__lt__(self, other)` | `<` 比较时调用 | 自定义排序规则 |

```python
class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def __str__(self):
        return f"Vector({self.x}, {self.y})"
    
    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)
    
    def __len__(self):
        return int((self.x**2 + self.y**2) ** 0.5)

v1 = Vector(2, 3)
v2 = Vector(1, 1)
print(v1 + v2)    # Vector(3, 4)
print(len(v1))    # 3
```

---

### 继承与 MRO 🔸 核心

#### 基础用法

```python
class Animal:
    def __init__(self, name):
        self.name = name
    
    def speak(self):
        raise NotImplementedError("子类必须实现此方法")

class Cat(Animal):
    def __init__(self, name, color):
        super().__init__(name)   # 调用父类构造方法
        self.color = color
    
    def speak(self):
        return f"{self.name} says: Meow!"

class Dog(Animal):
    def speak(self):
        return f"{self.name} says: Woof!"

# 多态
def animal_concert(animals):
    for animal in animals:
        print(animal.speak())

animal_concert([Cat("Kitty", "white"), Dog("Buddy")])
```

#### 进阶用法与原理

**MRO（Method Resolution Order）**

```python
class A:
    def method(self):
        print("A")

class B(A):
    def method(self):
        print("B")

class C(A):
    def method(self):
        print("C")

class D(B, C):  # 多继承
    pass

d = D()
d.method()      # 输出：B（按 MRO 顺序找到第一个）
print(D.__mro__)  # (<class 'D'>, <class 'B'>, <class 'C'>, <class 'A'>, <class 'object'>)
```

> [!note] 💡 AI 扩展（进阶）
> **C3 线性化算法**：Python 使用 C3 线性化算法计算 MRO，保证：
> 1. **子类优先**：子类的方法总是先于父类被调用。
> 2. **单调性**：如果类 A 在类 B 之前，那么 A 的所有子类也在 B 之前。
> 3. **无歧义**：避免菱形继承问题中的歧义。
> **菱形继承问题**：如果 D 继承 B 和 C，而 B 和 C 都继承 A，C3 算法确保 A 只出现一次，且顺序确定。

---

### 类属性、类方法与静态方法 🔸 核心

#### 基础用法

```python
class Circle:
    # 类属性
    pi = 3.14159
    count = 0  # 统计创建了多少个圆
    
    def __init__(self, radius):
        self.radius = radius
        Circle.count += 1
    
    def area(self):
        return self.pi * self.radius ** 2
    
    @classmethod
    def from_diameter(cls, diameter):
        """类方法：用直径创建圆"""
        return cls(diameter / 2)
    
    @staticmethod
    def is_valid_radius(r):
        """静态方法：判断半径是否合法"""
        return r > 0

# 使用
c1 = Circle(5)
c2 = Circle.from_diameter(10)
print(Circle.count)           # 2
print(Circle.is_valid_radius(-1))  # False
```

| 类型 | 装饰器 | 第一个参数 | 可访问 | 用途 |
| :--- | :--- | :--- | :--- | :--- |
| 实例方法 | 无 | `self`（实例） | 实例属性 + 类属性 | 操作实例数据 |
| 类方法 | `@classmethod` | `cls`（类） | 类属性 | 工厂方法、替代构造器 |
| 静态方法 | `@staticmethod` | 无 | 无（通过类名访问） | 与类相关但不需要访问类/实例的工具函数 |

---

### 私有属性与封装 🔹 基础

```python
class BankAccount:
    def __init__(self, owner, balance):
        self.owner = owner
        self.__balance = balance  # 私有属性（name mangling）
    
    def deposit(self, amount):
        if amount > 0:
            self.__balance += amount
        return self.__balance
    
    def get_balance(self):
        return self.__balance

acc = BankAccount("Alice", 1000)
print(acc.get_balance())     # 1000
# print(acc.__balance)       # AttributeError!
print(acc._BankAccount__balance)  # 1000（可以访问但不建议）
```

> ⚠️ **注意**：Python 没有真正的私有，双下划线只是名称改写（name mangling）机制，约定上 `_单下划线` 开头的属性表示"内部使用，不建议外部访问"。

---

## 4️⃣ 避坑指南 & 易错对比

| 对比组 | 区分要点 |
| :--- | :--- |
| `self` vs `cls` | `self` 是实例，`cls` 是类 |
| 实例属性 vs 类属性 | 前者用 `self.xxx` 定义（各实例独立），后者在类体中直接定义（共享） |
| `__init__` vs `__new__` | `__new__` 创建实例（很少重写），`__init__` 初始化实例 |
| `__str__` vs `__repr__` | `__str__` 面向用户（友好），`__repr__` 面向开发者（精确） |
| 继承 vs 组合 | "是一个"用继承（Dog is Animal），"有一个"用组合（Car has Engine） |
| 单继承 vs 多继承 | Python 支持多继承，但需谨慎使用（MRO 复杂、耦合度高） |

---

## 2️⃣ 知识网络

- **课内联动**：`self` → 实例引用；魔术方法 → Python 对象协议；继承 → 代码复用；MRO → 多继承的解析规则。
- **前后衔接**：
  - 前置知识：day03 的可变/不可变、day04 的字典、day05 的函数和作用域。
  - 后续延伸：day08 的闭包和装饰器（函数也是对象）；day10 的上下文管理器（`__enter__`/`__exit__` 也是魔术方法）；所有框架（Django、PyTorch）都重度使用 OOP。
- **AI/实战落地**：PyTorch 的 `nn.Module`、TensorFlow 的 `keras.Model` 都是基于类的框架；数据集的封装、模型的定义都离不开 OOP；`__call__` 让对象可以像函数一样调用，是 PyTorch 层对象的核心设计。

**Python 设计原则**

- **一切皆对象**：数字、字符串、函数、类都是对象。
- **显式优于隐式**：不搞魔术写法，代码意图清晰。
- **约定大于规范**：私有变量用下划线只是约定，不是强制。
- **多用组合，少用继承**：Python 继承尽量浅，优先使用组合。

```python
# 组合示例：Car has a Engine
class Engine:
    def start(self):
        return "发动机启动"

class Car:
    def __init__(self):
        self.engine = Engine()  # 组合

    def drive(self):
        return self.engine.start() + "，汽车行驶"
```

---

## 3️⃣ 应用场景与扩展

> **案例：实现一个简单的深度学习层（模拟 PyTorch 风格）**

```python
class Linear:
    """模拟全连接层"""
    def __init__(self, in_features, out_features):
        self.in_features = in_features
        self.out_features = out_features
        # 随机初始化权重
        import random
        self.weight = [[random.random() for _ in range(in_features)] 
                        for _ in range(out_features)]
        self.bias = [random.random() for _ in range(out_features)]
    
    def __call__(self, x):
        """让层对象可调用"""
        return [
            sum(w * xi for w, xi in zip(self.weight[i], x)) + self.bias[i]
            for i in range(self.out_features)
        ]
    
    def __repr__(self):
        return f"Linear({self.in_features} -> {self.out_features})"

layer = Linear(3, 2)
print(layer)           # Linear(3 -> 2)
output = layer([1.0, 2.0, 3.0])
print(output)          # 前向传播结果
```

---

## 8️⃣ AI 附加说明

- **组织方式**：AI 重排，将原笔记中 OOP 的零散概念整合为"基础→魔术方法→继承→类方法/静态方法→私有属性"的递进结构。
- **重要性判断摘要**：原笔记中缺少 MRO 的深入解释和类方法/静态方法的对比表，已补充；新增模拟 PyTorch 层作为 AI 实战案例。
- **难度标签分布**：🔹 基础 1 处，🔸 核心 4 处。
- **扩展块统计**：基础扩展 1 个（OOP 对比表），进阶扩展 1 个（C3 线性化算法）。总知识点 N ≈ 5，比例符合规则。
- **代码库使用情况**：未使用。
- **可能遗漏但可补充的主题**：元类（metaclass）、描述符（descriptor）、属性装饰器 `@property`（day10 会涉及）、抽象基类（ABC）。

- **自检声明**：已按语法验收标准（7项）、笔记逻辑验收标准（11项）、代码块语言标注、版本号一致性逐项自检确认。