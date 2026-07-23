---
title: 网络编程与JSON（AI增强版）
date:
study_time:
review_version: v3.6
publish: true
category: Python基础
difficulty: 🔸核心
tags:
  - 学习笔记
  - Python基础
  - 网络编程
  - JSON
status: 完善
---
# [day09] 学习笔记｜网络编程与 JSON（AI 增强版）

## 📌 核心速览

- **字符集与编码**：ASCII（128 字符）、Unicode（全球字符统一编号）、UTF-8（Unicode 的变长编码实现）。Python 3 字符串默认使用 Unicode，网络传输需编码为字节（`encode()`）/解码为字符串（`decode()`）。
- **JSON（JavaScript Object Notation）**：轻量级数据交换格式，与 Python 字典高度对应。核心方法：`json.dumps()`（序列化）、`json.loads()`（反序列化）、`json.dump()`/`json.load()`（文件操作）。
- **Socket 网络编程**：基于 TCP/UDP 协议实现进程间通信。TCP 面向连接、可靠传输；UDP 无连接、效率高。关键概念：IP 地址、端口号、三次握手、四次挥手。
- **TCP 服务端/客户端模型**：服务端 `bind()`→`listen()`→`accept()`→`send()`/`recv()`；客户端 `connect()`→`send()`/`recv()`。

---

## 1️⃣ 完整知识库

### 字符集与编码 🔹 基础

#### 定义与本质

- **ASCII**：美国信息交换标准代码，使用 7 位二进制表示 128 个字符（英文字母、数字、符号）。
- **Unicode**：为世界上所有字符分配唯一的数字编号（码点，Code Point），如 `U+4E2D` = "中"。
- **UTF-8**：Unicode 的一种实现方式，使用 1~4 个字节变长编码，兼容 ASCII，是互联网的事实标准。

```python
# Python 字符串是 Unicode
s = "Hello 世界"

# 编码：字符串 → 字节
b = s.encode("utf-8")
print(b)  # b'Hello \xe4\xb8\x96\xe7\x95\x8c'

# 解码：字节 → 字符串
s2 = b.decode("utf-8")
print(s2)  # "Hello 世界"
```

#### 避坑与局限

- **编码不一致是乱码的根源**：文件保存为 GBK，但用 UTF-8 读取，就会乱码。
- **始终指定编码**：打开文件时显式写 `encoding="utf-8"`，避免依赖系统默认编码。

---

### JSON 数据处理 🔸 核心

#### 定义与本质

JSON 是一种纯文本数据格式，与 Python 类型映射关系：

| Python | JSON |
| :--- | :--- |
| `dict` | `object` |
| `list`、`tuple` | `array` |
| `str` | `string` |
| `int`、`float` | `number` |
| `True`/`False` | `true`/`false` |
| `None` | `null` |

#### 基础用法

```python
import json

data = {"name": "张三", "age": 30, "city": "北京"}

# 序列化：Python 对象 → JSON 字符串
json_str = json.dumps(data, ensure_ascii=False, indent=2)
print(json_str)

# 反序列化：JSON 字符串 → Python 对象
obj = json.loads(json_str)
print(obj["name"])

# 写入文件
with open("data.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

# 从文件读取
with open("data.json", "r", encoding="utf-8") as f:
    loaded = json.load(f)
```

**常用参数**

| 参数 | 作用 |
| :--- | :--- |
| `ensure_ascii=False` | 保留中文，不转义为 `\uXXXX` |
| `indent=2` | 格式化缩进，便于阅读 |
| `sort_keys=True` | 按键名排序 |
| `separators=(",", ":")` | 压缩，去掉空格（用于网络传输节省带宽） |

#### 进阶用法与原理

**自定义编码（处理 datetime 等不可序列化类型）**

```python
from datetime import datetime
import json

def custom_encoder(obj):
    if isinstance(obj, datetime):
        return obj.isoformat()
    raise TypeError(f"Object {obj} is not JSON serializable")

now = {"time": datetime.now()}
json_str = json.dumps(now, default=custom_encoder)
print(json_str)  # {"time": "2024-01-15T10:30:00"}

# 自定义解码
def custom_decoder(dct):
    if "time" in dct:
        dct["time"] = datetime.fromisoformat(dct["time"])
    return dct

original = json.loads(json_str, object_hook=custom_decoder)
```

---

### Socket 网络编程 🔸 核心

#### 定义与本质

**网络通信三要素**

| 要素 | 作用 | 示例 |
| :--- | :--- | :--- |
| **IP 地址** | 设备在网络中的唯一标识 | `192.168.1.1`、`127.0.0.1`（本机） |
| **端口号** | 程序在设备上的唯一标识 | `80`（HTTP）、`443`（HTTPS）、`22`（SSH） |

**端口号分类**

| 类型 | 范围 | 说明 |
| :--- | :--- | :--- |
| **知名端口** | 0 ~ 1023 | 系统保留，分配给常用服务（如 HTTP: 80、HTTPS: 443、SSH: 22） |
| **动态端口** | 1024 ~ 65535 | 程序员开发自定义应用程序时使用，自定义端口时尽量规避 0~1023 |
| **协议** | 数据传输的规则 | TCP（可靠）、UDP（高效） |

**TCP 三次握手**

建立连接时需要三次交互：
1. **SYN**：客户端向服务端发送连接请求。
2. **SYN-ACK**：服务端收到请求，回复确认并同步自己的序列号。
3. **ACK**：客户端再次确认，连接建立成功。

> 三次握手的目的是**同步双方的初始序列号**，并确认双方的发送/接收能力正常。

**TCP 四次挥手**

断开连接时需要四次交互（因为 TCP 是全双工的，双方都要单独关闭）：
1. **FIN**：主机 A 发送结束请求。
2. **ACK**：主机 B 确认 A 的结束请求。
3. **FIN**：主机 B 发送自己的结束请求。
4. **ACK**：主机 A 确认 B 的结束请求，连接彻底关闭。

#### 基础用法

**TCP 服务端**

```python
import socket

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # 端口复用
server.bind(("0.0.0.0", 8888))
server.listen(5)

print("服务端启动，等待连接...")
conn, addr = server.accept()
print(f"客户端 {addr} 已连接")

conn.send("Welcome!".encode("utf-8"))
data = conn.recv(1024).decode("utf-8")
print(f"收到：{data}")

conn.close()
server.close()
```

**TCP 客户端**

```python
import socket

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("127.0.0.1", 8888))

data = client.recv(1024).decode("utf-8")
print(f"服务端：{data}")

client.send("Hello Server!".encode("utf-8"))
client.close()
```

**`__name__` 属性**

`__name__` 是 Python 的内置属性，代表当前模块的名称。
- 如果直接运行当前模块（作为主程序），`__name__` 的值为 `'__main__'`。
- 如果被其他模块导入，`__name__` 的值为模块文件名（不含 `.py`）。
- 常用于编写模块级测试代码或入口判断。

```python
# 推荐写法：只有直接运行该文件时才执行
if __name__ == '__main__':
    # 启动服务端或执行测试代码
    start_server()
```

#### 避坑与局限

| 坑点 | 说明 | 解决 |
| :--- | :--- | :--- |
| **端口占用** | 服务端程序崩溃后，端口不会立即释放（TIME_WAIT 状态） | 设置 `SO_REUSEADDR` |
| **`recv` 返回空** | 客户端关闭连接后，`recv` 返回空字节 `b''` | 用 `if not data: break` 判断断开 |
| **粘包问题** | TCP 是流协议，连续发送的数据可能被合并接收 | 添加消息头（长度）或使用固定分隔符 |
| **阻塞 I/O** | 默认 `recv`/`accept` 会阻塞线程 | 使用多线程、多进程或异步 I/O |
| **被动套接字** | `listen()` 后的套接字只能调用 `accept()`，不能 `send`/`recv` | 用 `accept()` 返回的新套接字进行通信 |
| **客户端下线判断** | 客户端调用 `close()` 后，服务端 `recv` 返回空字节 `b''` | 判断 `if not data: break` 即可知客户端已下线 |
| **服务端关闭逻辑** | 关闭 `accept()` 返回的套接字表示与该客户端通信完毕；关闭监听套接字则停止服务 | 根据业务场景慎重选择关闭对象 |

---

## 4️⃣ 避坑指南 & 易错对比

| 对比组 | 区分要点 |
| :--- | :--- |
| `json.dumps` vs `json.dump` | 前者返回字符串，后者直接写入文件对象 |
| `json.loads` vs `json.load` | 前者解析字符串，后者从文件对象读取 |
| TCP vs UDP | TCP 面向连接、可靠、有序；UDP 无连接、高效、不保证送达 |
| `encode()` vs `decode()` | 字符串→字节 vs 字节→字符串 |
| `SO_REUSEADDR` 作用 | 允许端口复用，解决程序重启时的"Address already in use" |

---

## 2️⃣ 知识网络

- **课内联动**：编码 → 字符集基础；JSON → 数据序列化；Socket → 网络通信原理。
- **前后衔接**：
  - 前置知识：day06 的 HTTP 协议（建立在 TCP 之上）。
  - 后续延伸：day10 的进程/线程/协程用于实现并发网络服务；所有 Web 框架（Django、Flask）底层都是 Socket。
- **AI/实战落地**：REST API 返回 JSON 数据；模型配置文件、超参数保存常用 JSON；分布式训练中的进程间通信基于 Socket。

---

## 3️⃣ 应用场景与扩展

> [!note] 🛠️ 实战扩展（基础）
> **TCP 粘包问题与解决方案**
> TCP 是流式协议，数据没有明确边界，连续发送多个数据包时可能被合并接收（粘包）。
>
> **解决方案 1：固定消息头（推荐）**
> 在每条消息前附加一个固定长度的头部，标识消息体长度。
> ```python
> def send_msg(sock, msg):
>     data = msg.encode('utf-8')
>     header = len(data).to_bytes(4, 'big')  # 4字节头部
>     sock.sendall(header + data)
>
> def recv_msg(sock):
>     import struct
>     header = sock.recv(4)
>     body_len = struct.unpack('!I', header)[0]
>     body = b''
>     while len(body) < body_len:
>         chunk = sock.recv(body_len - len(body))
>         if not chunk:
>             break
>         body += chunk
>     return body.decode('utf-8')
> ```
>
> **解决方案 2：特殊分隔符**
> 在消息末尾添加特殊标记（如 `\n`），接收端按标记切分。适用于消息内容不含该标记的场景。
>
> **注意事项**：粘包是 TCP 协议特性而非缺陷，UDP 是面向消息的协议，不存在粘包问题。

> **案例：简单的 JSON API 客户端**

```python
import json
import urllib.request

# 获取公开 API 数据
url = "https://api.github.com"
req = urllib.request.Request(url, headers={"User-Agent": "Python"})
with urllib.request.urlopen(req) as response:
    data = json.loads(response.read().decode())
    print(f"GitHub API 当前用户：{data.get('current_user_url')}")
```

> [!note] 🛠️ 实战扩展（进阶）
> **JSON Schema 验证实战**
> JSON Schema 是描述 JSON 数据结构规则的声明式语言，可确保 API 输入/输出的数据格式正确性。
>
> ```python
> import json
> from jsonschema import validate, ValidationError
>
> # 定义 Schema：用户信息必须包含 name、age
> schema = {
>     "type": "object",
>     "required": ["name", "age"],
>     "properties": {
>         "name": {"type": "string", "minLength": 1},
>         "age": {"type": "integer", "minimum": 0, "maximum": 150}
>     }
> }
>
> # 验证数据
> user_data = {"name": "张三", "age": 25}
> try:
>     validate(instance=user_data, schema=schema)
>     print("验证通过")
> except ValidationError as e:
>     print(f"验证失败：{e.message}")
> ```
>
> **原理**：JSON Schema 将数据约束（类型、范围、格式、枚举等）表达为 JSON 字典，验证器按 Schema 规则递归检查数据树的每个节点，发现不匹配即抛出 `ValidationError`。
>
> **常见应用**：API 请求参数校验、配置文件格式检查、微服务间数据契约（Contract Testing）。

---

## 8️⃣ AI 附加说明

- **组织方式**：AI 重排，将原笔记中字符集、JSON、网络编程整合为系统结构，去除绝对路径图片引用（已复制到 asset）。
- **重要性判断摘要**：原笔记中缺少 TCP 三次握手/四次挥手的详细解释和粘包问题说明，已补充；新增端口复用和消息边界处理作为避坑内容。
- **难度标签分布**：🔹 基础 1 处，🔸 核心 2 处。
- **扩展块统计**：基础扩展 1 个（TCP 粘包问题及解决方案），进阶扩展 1 个（JSON Schema 验证实战）。总知识点 N ≈ 3，比例符合规则。
- **代码库使用情况**：未使用。
- **可能遗漏但可补充的主题**：UDP Socket 编程、`socketserver` 模块、`select`/`poll`/`epoll` 多路复用、WebSocket 协议。

- **自检声明**：已按语法验收标准（7项）、笔记逻辑验收标准（11项）、代码块语言标注、版本号一致性逐项自检确认。