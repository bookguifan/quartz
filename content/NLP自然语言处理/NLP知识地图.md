---
title: NLP 知识地图
date:
study_time:
review_version: v3.6
publish: true
category: NLP自然语言处理
difficulty: 🔹基础
tags:
  - 学习笔记
  - 自然语言处理
  - 知识地图
status: 完善
---

# NLP 自然语言处理 知识地图

> 本知识地图基于 13 篇增强版笔记聚合生成，涵盖从 NLP 基础到 Transformer 与预训练模型的完整学习路径。
> 第二次更新：整合 2026 最新版 PDF 课件，新增 fasttext/BERT 系列模型/迁移学习扩展案例 3 篇笔记，深入整合 Transformer 笔记。

---

## 一、概念速查索引

### NLP 基础概念

- **自然语言处理（NLP）**：让计算机理解、解释和生成人类语言的技术，涵盖分词、语义理解、机器翻译等任务（来源：[[1.NLP入门与文本预处理（AI增强版）]]）
- **分词（Tokenization）**：将连续文本切分为最小语义单元（词/字）的过程，是 NLP 的第一步（来源：[[1.NLP入门与文本预处理（AI增强版）]]）
- **命名实体识别（NER）**：从文本中识别人名、地名、机构名等专有名词并分类的任务（来源：[[1.NLP入门与文本预处理（AI增强版）]]）
- **词性标注（POS Tagging）**：为每个词标注语法类别（名词/动词/形容词等）的过程（来源：[[1.NLP入门与文本预处理（AI增强版）]]）
- **文本张量表示**：将文本转换为数值向量（张量）的过程，是深度学习处理文本的前提（来源：[[1.NLP入门与文本预处理（AI增强版）]]、[[2.文本张量表示方法（AI增强版）]]）

### 文本表示方法

- **One-Hot 编码**：用维度等于词表大小的稀疏向量表示每个词，仅一位为 1 其余为 0（来源：[[2.文本张量表示方法（AI增强版）]]）
- **Word2Vec**：通过上下文预测训练的稠密词向量模型，包含 CBOW 和 SkipGram 两种架构（来源：[[2.文本张量表示方法（AI增强版）]]）
- **CBOW**：利用上下文词预测中心词的 Word2Vec 架构，适合小数据集和高频词（来源：[[2.文本张量表示方法（AI增强版）]]）
- **SkipGram**：利用中心词预测上下文词的 Word2Vec 架构，适合大数据集和低频词（来源：[[2.文本张量表示方法（AI增强版）]]）
- **FastText（概念）**：Word2Vec 的改进版，引入子词（subword）n-gram 特征，能处理未登录词（来源：[[2.文本张量表示方法（AI增强版）]]）
- **fasttext（工具包）**：Facebook FAIR 开发的 NLP 工具包，支持文本分类和词向量训练，通过层次 softmax 和负采样实现极速训练（来源：[[11.fasttext工具详解与应用（AI增强版）]]）
- **层次 softmax**：基于哈夫曼树的 softmax 加速方法，将多分类复杂度从 O(V) 降到 O(logV)，适合超多类别场景（来源：[[11.fasttext工具详解与应用（AI增强版）]]）
- **负采样（Negative Sampling）**：每次训练仅更新部分权重，降低梯度下降计算量，同时增加噪声样本提升模型鲁棒性（来源：[[11.fasttext工具详解与应用（AI增强版）]]）
- **nn.Embedding**：PyTorch 提供的词嵌入层，将离散词索引映射为稠密向量，可端到端训练（来源：[[2.文本张量表示方法（AI增强版）]]）

### 文本数据分析与特征工程

- **文本数据分析**：通过标签分布、句子长度分布、散点图、词汇统计、词云等手段理解数据特征（来源：[[3.文本数据分析与特征处理（AI增强版）]]）
- **N-gram 特征**：将连续 N 个词作为一个特征单元，捕捉局部词序信息（来源：[[3.文本数据分析与特征处理（AI增强版）]]）
- **文本长度规范**：通过 `pad_sequences` 将变长文本截断/填充为统一长度，满足 batch 训练需求（来源：[[3.文本数据分析与特征处理（AI增强版）]]）
- **回译数据增强**：通过"翻译→回译"生成语义等价但表述不同的增强样本，扩充训练数据（来源：[[3.文本数据分析与特征处理（AI增强版）]]）

### 循环神经网络系列

- **RNN（循环神经网络）**：具有循环连接的网络结构，能处理变长序列数据，按输入输出维度分为 N-to-N、N-to-1、1-to-N、N-to-M 四类（来源：[[4.RNN模型及其变体（AI增强版）]]）
- **传统 RNN 内部结构**：`h_t = tanh(W_xh·x_t + W_hh·h_{t-1} + b_h)`，存在梯度消失/爆炸问题（来源：[[4.RNN模型及其变体（AI增强版）]]）
- **LSTM（长短期记忆网络）**：通过遗忘门、输入门、输出门三个门控机制控制信息流，缓解梯度消失问题（来源：[[4.RNN模型及其变体（AI增强版）]]）
- **GRU（门控循环单元）**：LSTM 的简化版，将遗忘门和输入门合并为更新门，参数更少训练更快（来源：[[4.RNN模型及其变体（AI增强版）]]）
- **Bi-LSTM / Bi-GRU**：双向循环网络，同时利用前向和后向信息，输出拼接两方向隐状态（来源：[[4.RNN模型及其变体（AI增强版）]]）
- **teacher_forcing**：训练时用真实标签而非模型上一步输出作为下一步输入的策略，加速收敛但可能引入暴露偏差（来源：[[5.RNN人名分类器案例（AI增强版）]]、[[7.Seq2Seq英译法案例（AI增强版）]]）

### 注意力机制

- **Attention 机制**：让模型在处理序列时动态关注相关部分，通过 Query-Key-Value 三要素计算加权求和（来源：[[6.注意力机制（AI增强版）]]）
- **Q/K/V 三要素**：Query（查询）与 Key（键）计算相似度，对 Value（值）加权求和得到注意力输出（来源：[[6.注意力机制（AI增强版）]]）
- **注意力三步走**：① Q 与 K 计算相似度 → ② softmax 归一化为权重 → ③ 对 V 加权求和（来源：[[6.注意力机制（AI增强版）]]）
- **Scaled Dot-Product Attention**：`Attention(Q,K,V) = softmax(QK^T/√dk)V`，除以 √dk 防止 softmax 饱和（来源：[[6.注意力机制（AI增强版）]]）
- **自注意力（Self-Attention）**：Q=K=V 均来自同一序列，用于捕捉序列内部的长距离依赖关系（来源：[[6.注意力机制（AI增强版）]]）
- **多头注意力（Multi-Head Attention）**：将 Q/K/V 分成多组并行计算注意力再拼接，捕捉不同子空间的注意力模式（来源：[[8.Transformer模型架构（AI增强版）]]）

### Transformer 架构

- **Transformer**：2017 年提出的完全基于注意力机制的序列模型，摒弃循环结构，支持并行计算（来源：[[8.Transformer模型架构（AI增强版）]]）
- **位置编码（Positional Encoding）**：用正弦/余弦函数为输入注入位置信息，弥补注意力机制无序性的缺陷（来源：[[8.Transformer模型架构（AI增强版）]]）
- **掩码张量（Mask）**：Subsequent Mask 下三角矩阵防止解码器看到未来信息；Padding Mask 忽略填充位置（来源：[[8.Transformer模型架构（AI增强版）]]）
- **前馈全连接层（PositionwiseFeedForward）**：两层线性变换 + ReLU 激活，对每个位置独立进行非线性变换（来源：[[8.Transformer模型架构（AI增强版）]]）
- **规范化层（LayerNorm）**：对每个样本的特征维度做标准化，稳定深层网络训练（来源：[[8.Transformer模型架构（AI增强版）]]）
- **子层连接（SublayerConnection）**：残差连接 + LayerNorm，结构为 `x + Sublayer(LayerNorm(x))`（来源：[[8.Transformer模型架构（AI增强版）]]）
- **编码器层（EncoderLayer）**：由多头注意力子层 + 前馈子层组成，各子层均带残差连接和 LayerNorm（来源：[[8.Transformer模型架构（AI增强版）]]）
- **解码器层（DecoderLayer）**：比编码器层多一个带掩码的交叉注意力子层，用于关注编码器输出（来源：[[8.Transformer模型架构（AI增强版）]]）
- **Seq2Seq**：Encoder-Decoder 架构，编码器将输入序列编码为上下文向量，解码器逐步生成输出序列（来源：[[7.Seq2Seq英译法案例（AI增强版）]]）

### 迁移学习与预训练模型

- **迁移学习**：将预训练模型在大规模语料上学到的知识迁移到下游任务中，通过微调实现高效适配（来源：[[9.迁移学习与预训练模型应用（AI增强版）]]）
- **BERT**：Encoder-Only 架构的预训练模型，通过掩码语言模型（MLM 8-1-1策略）和下一句预测（NSP）训练，三种 Embedding（Token+Segment+Position）求和输入双向 Transformer Encoder（来源：[[12.BERT系列预训练模型详解（AI增强版）]]）
- **ELMo**：2018年华盛顿大学提出的动态词向量模型，通过双向多层 LSTM 加权融合生成上下文相关词向量，是首个支持一词多义的词向量模型（来源：[[12.BERT系列预训练模型详解（AI增强版）]]）
- **GPT**：Decoder-Only 架构的预训练模型，通过 look-ahead mask 实现单向自回归语言建模，12个block堆叠，擅长文本生成任务（来源：[[12.BERT系列预训练模型详解（AI增强版）]]）
- **BERT vs ELMo vs GPT**：BERT（Transformer Encoder+深度融合双向）> ELMo（LSTM+拼接双向）> GPT（Transformer Decoder+单向），特征提取能力和双向建模能力依次递减（来源：[[12.BERT系列预训练模型详解（AI增强版）]]）
- **T5**：Encoder-Decoder 架构的预训练模型，将所有任务统一为"文本到文本"格式（来源：[[9.迁移学习与预训练模型应用（AI增强版）]]）
- **Pipeline**：HuggingFace 提供的高层 API，一行代码完成预训练模型推理，适合快速验证（来源：[[9.迁移学习与预训练模型应用（AI增强版）]]）
- **AutoModel**：自动根据任务类型选择模型类的 API，提供 `AutoTokenizer` + `AutoModelForXXX` 的组合方式（来源：[[9.迁移学习与预训练模型应用（AI增强版）]]）
- **pooler_output vs last_hidden_state**：前者取 `[CLS]` 位置经一层全连接+Tanh 的输出，适合分类；后者是全部位置的隐状态，适合序列标注（来源：[[10.中文文本分类案例（AI增强版）]]）
- **MLM 掩码语言模型**：8-1-1 策略——80%概率替换为 [MASK]、10%替换为随机词、10%保持不变，防止模型只关注 [MASK] 位置（来源：[[12.BERT系列预训练模型详解（AI增强版）]]）
- **中文填空/句子关系任务**：基于 BertModel 特征抽取的下游迁移学习任务，前者预测被遮蔽词，后者判断句子对关系（来源：[[13.迁移学习扩展案例（AI增强版）]]）

---

## 核心流程

### 文本分类完整流程

```text
原始文本 → jieba分词 → 词表映射(Word2Vec/nn.Embedding) → 序列填充(pad_sequences)
  → 模型(RNN/LSTM/GRU/CNN/BERT) → 输出(logits) → 损失函数(CrossEntropyLoss) → 优化器(Adam/AdamW)
```

### Seq2Seq 翻译流程

```text
源语言句子 → Embedding → Encoder(GRU) → 上下文向量 → Decoder(GRU+Attention) → 目标语言句子
  训练策略：teacher_forcing（用真实标签作为下一步输入）
```

### BERT 微调流程

```text
预训练模型(BERT-base) → 加载数据(Dataset+DataLoader) → 冻结/部分冻结参数
  → 替换分类头(nn.Linear) → collate_fn分词padding → AdamW优化 → 评估(pooler_output)
```

---

## 核心矛盾

| 矛盾对 | 核心冲突 | 解决方案 |
|--------|---------|---------|
| **稀疏表示 vs 稠密表示** | One-Hot 维度灾难 vs Word2Vec 语义丢失 | nn.Embedding 端到端训练、FastText 子词特征 |
| **梯度消失 vs 序列记忆** | RNN 长距离梯度衰减 vs 需要长期记忆 | LSTM 三门控、GRU 两门控、残差连接 |
| **局部感受野 vs 长距离依赖** | CNN/RNN 局部窗口有限 vs 语言长距离关联 | Self-Attention 直接建模任意位置关系 |
| **预训练通用性 vs 下游任务特异性** | 通用模型无法适配所有场景 vs 从零训练成本高 | 冻结+微调、Pipeline 快速验证、AutoModel 灵活切换 |
| **生成多样性 vs 生成质量** | 高温度增加创意但降低准确性 vs 低温度确定但刻板 | Temperature 参数调节、Top-p 核采样、自回归生成 |
| **语义检索 vs 关键词检索** | 语义相似但词不同导致召回失败 vs 关键词精确但语义窄 | 混合检索（语义+全文）、Rerank 二次精排 |

---

## 二、学习路径与关联

### 学习路径

```text
第一阶段：NLP 基础与文本预处理
  [[1.NLP入门与文本预处理（AI增强版）]] → [[2.文本张量表示方法（AI增强版）]] → [[3.文本数据分析与特征处理（AI增强版）]]
      │
      ▼
第二阶段：循环神经网络系列
  [[4.RNN模型及其变体（AI增强版）]] → [[5.RNN人名分类器案例（AI增强版）]] → [[6.注意力机制（AI增强版）]]
      │
      ▼
第三阶段：Seq2Seq 与 Transformer
  [[7.Seq2Seq英译法案例（AI增强版）]] → [[8.Transformer模型架构（AI增强版）]]
      │
      ▼
第四阶段：迁移学习与预训练应用
  [[9.迁移学习与预训练模型应用（AI增强版）]] → [[10.中文文本分类案例（AI增强版）]]
      │
      ▼
第五阶段：工具实践与模型详解
  [[11.fasttext工具详解与应用（AI增强版）]] → [[12.BERT系列预训练模型详解（AI增强版）]] → [[13.迁移学习扩展案例（AI增强版）]]
```

### 知识网络

- **课内联动**：
  - [One-Hot] → [Word2Vec] → [nn.Embedding] → [fasttext工具]：文本表示从稀疏到稠密、从概念到工具的演化（笔记1→2→11）
  - [传统RNN] → [LSTM] → [GRU]：门控机制解决梯度消失的递进（笔记4）
  - [RNN人名分类] → [Seq2Seq翻译]：从分类任务到生成任务的扩展（笔记5→7）
  - [注意力机制] → [Transformer]：Attention 从辅助组件到核心架构的跃迁（笔记6→8）
  - [Transformer] → [BERT/GPT/T5] → [ELMo]：从架构到预训练模型的落地，三模型对比（笔记8→9→12）
  - [fasttext工具] → [迁移学习概念] → [中文分类案例] → [扩展案例]：从工具到理论的迁移学习完整链路（笔记11→9→10→13）

- **前后衔接**：
  - 前置知识：[[Python基础知识地图|Python 编程]]、[[深度学习知识地图|PyTorch 基础]]、线性代数（矩阵运算）、概率论（softmax）
  - 当前主题：NLP 从规则到深度学习的完整技术栈
  - 后续延伸：[[基础工作流整合知识地图|Prompt Engineering]]、[[深度学习知识地图|RLHF 微调]]、大语言模型（LLM）、多模态模型
  - **交叉参考**：RNN/LSTM/GRU 详见 [[深度学习知识地图]] 2.13 节；Transformer 架构详见 [[深度学习知识地图]] 2.3 节；文本预处理（jieba）基于 [[Python基础知识地图]] day03 字符串操作

---

## 三、PyTorch / 工具 API 速查

### jieba 分词 API

| 方法 | 签名 | 关键参数 | 适用场景 |
|------|------|---------|---------|
| 精确分词 | `jieba.cut(text, cut_all=False)` | `cut_all=False` 精确模式 | 默认场景，返回生成器 |
| 全模式 | `jieba.cut(text, cut_all=True)` | `cut_all=True` | 扫描所有可能的词 |
| 搜索引擎模式 | `jieba.cut_for_search(text)` | 无 | 搜索引擎索引构建 |
| 加载自定义词典 | `jieba.load_userdict(path)` | `path` 词典文件路径 | 领域专有词汇 |
| 词性标注 | `jieba.posseg.cut(text)` | 无 | 需要词性信息的场景 |

### PyTorch nn 模块 API

| 类/函数 | 签名 | 关键参数 | 适用场景 |
|---------|------|---------|---------|
| 词嵌入层 | `nn.Embedding(num_embeddings, embedding_dim)` | `num_embeddings` 词表大小, `embedding_dim` 向量维度 | 将词索引映射为稠密向量 |
| 标准 RNN | `nn.RNN(input_size, hidden_size, num_layers, batch_first)` | `batch_first=True` 输入为 (batch, seq, feature) | 基础序列建模 |
| LSTM | `nn.LSTM(input_size, hidden_size, num_layers, batch_first)` | 同上 | 长序列建模，缓解梯度消失 |
| GRU | `nn.GRU(input_size, hidden_size, num_layers, batch_first)` | 同上 | LSTM 轻量替代 |
| 线性层 | `nn.Linear(in_features, out_features)` | `in_features`, `out_features` | 分类输出层 |
| LayerNorm | `nn.LayerNorm(features)` | `features` 特征维度 | Transformer 规范化 |
| 负对数似然损失 | `nn.NLLLoss()` | 无 | 配合 LogSoftmax 使用 |
| 交叉熵损失 | `nn.CrossEntropyLoss()` | `ignore_index` 可选 | 多分类任务（内含 LogSoftmax） |
| Adam 优化器 | `optim.Adam(params, lr)` | `lr` 学习率 | 通用优化器 |
| AdamW 优化器 | `optim.AdamW(params, lr)` | `lr`, `weight_decay` | 带权重衰减，适合 Transformer |

### HuggingFace Transformers API

| 类/方法 | 功能 | 关键参数 | 适用场景 |
|---------|------|---------|---------|
| `pipeline(task, model)` | 一行代码推理 | `task` 任务类型, `model` 模型名 | 快速验证预训练模型 |
| `AutoTokenizer.from_pretrained(name)` | 自动加载分词器 | `name` 模型名 | 配合 AutoModel 使用 |
| `AutoModelForSequenceClassification` | 文本分类模型 | `num_labels` 类别数 | 文本分类任务 |
| `AutoModelForTokenClassification` | 序列标注模型 | `num_labels` 类别数 | NER 任务 |
| `AutoModelForMaskedLM` | 完形填空模型 | 无 | 掩码语言模型任务 |
| `AutoModelForQuestionAnswering` | 阅读理解模型 | 无 | 问答任务 |
| `BertModel.from_pretrained(name)` | 加载 BERT 模型 | `name` 模型名 | 具体模型方式 |
| `BertForMaskedLM.from_pretrained(name)` | BERT 完形填空 | `name` 模型名 | BERT MLM 任务 |

---

## 四、FAQ

> **Q1**：Word2Vec 的 CBOW 和 SkipGram 该怎么选？
> **A1**：CBOW 适合小数据集和高频词（训练快），SkipGram 适合大数据集和低频词（效果好但训练慢）。工程实践中数据量大时优先 SkipGram。

> **Q2**：LSTM 和 GRU 该怎么选？
> **A2**：GRU 参数更少（少一个门）、训练更快，性能与 LSTM 接近。数据量小时优先 GRU（防过拟合），数据量大时 LSTM 略优。大多数场景 GRU 是性价比之选。

> **Q3**：为什么 Attention 公式要除以 √dk？
> **A3**：当 dk 较大时，QK^T 的值会很大，导致 softmax 进入饱和区（梯度趋近于 0）。除以 √dk 将方差缩放回 1，保持梯度稳定。

> **Q4**：Transformer 相比 RNN 的核心优势是什么？
> **A4**：① 并行计算（RNN 必须按时间步串行）；② 长距离依赖建模能力更强（自注意力直接连接任意两位置）；③ 可扩展性强（支持大规模预训练）。

> **Q5**：BERT 的 pooler_output 和 last_hidden_state 该用哪个？
> **A5**：分类任务用 `pooler_output`（取 [CLS] 位置经全连接+Tanh）；序列标注/Token 级任务用 `last_hidden_state`（保留全部位置的隐状态）。

> **Q6**：迁移学习中如何冻结预训练模型参数？
> **A6**：两种方式——① `param.requires_grad = False`（推荐，只关闭梯度但仍在计算图中）；② `with torch.no_grad():` 包裹前向传播（完全不在计算图中）。方式①更灵活，允许部分层冻结部分层微调。

> **Q7**：`batch_first=True` 和 `batch_first=False` 有什么区别？
> **A7**：`batch_first=True` 时输入形状为 `(batch, seq, feature)`；`False`（默认）时为 `(seq, batch, feature)`。建议统一使用 `True`，避免维度混淆。注意 RNN 输出的隐状态形状始终是 `(num_layers, batch, hidden)`，不受 batch_first 影响。

> **Q8**：`nn.NLLLoss()` 和 `nn.CrossEntropyLoss()` 有什么区别？
> **A8**：`CrossEntropyLoss` = `LogSoftmax` + `NLLLoss`。如果模型最后一层是 `LogSoftmax`，用 `NLLLoss`；如果是原始 logits，用 `CrossEntropyLoss`。两者数学上等价，但不要重复应用 LogSoftmax。

> **Q9**：fasttext 的层次 softmax 和负采样该选哪个？
> **A9**：类别数少（<10万）时负采样更快更简单；类别数极大（>10万）时层次 softmax 更稳定。fasttext 文本分类推荐 `loss='hs'`（层次 softmax）。

> **Q10**：BERT、ELMo、GPT 的核心区别是什么？
> **A10**：BERT 用 Transformer Encoder 做深度融合双向建模；ELMo 用双层 LSTM 做拼接式双向建模；GPT 用 Transformer Decoder 做单向自回归建模。BERT 在特征提取和双向理解上最强。

> **Q11**：BERT MLM 为什么要用 8-1-1 策略而不是全部替换为 [MASK]？
> **A11**：如果 100% 替换为 [MASK]，模型只会学关注 [MASK] 位置，推理时没有 [MASK] 标记会导致性能下降。保留 10% 原词和 10% 随机词让模型学到原始词信息。

---

## 五、标签云

#NLP #自然语言处理 #深度学习 #PyTorch #Word2Vec #LSTM #GRU #RNN #注意力机制 #Transformer #BERT #ELMo #GPT #迁移学习 #预训练模型 #Seq2Seq #文本分类 #分词 #jieba #HuggingFace #词向量 #Embedding #自注意力 #多头注意力 #位置编码 #LayerNorm #fasttext #层次softmax #负采样 #MLM #NSP #动态词向量

---

## 附录：概念索引完整性自检

| 笔记 | 核心术语数 | 关键流程数 | 核心矛盾数 | 状态 |
|------|-----------|-----------|-----------|------|
| [[1.NLP入门与文本预处理（AI增强版）]] | 5 | 1 | 0 | PASS |
| [[2.文本张量表示方法（AI增强版）]] | 9 | 1 | 1 | PASS |
| [[3.文本数据分析与特征处理（AI增强版）]] | 4 | 1 | 0 | PASS |
| [[4.RNN模型及其变体（AI增强版）]] | 7 | 1 | 1 | PASS |
| [[5.RNN人名分类器案例（AI增强版）]] | 1 | 1 | 0 | PASS |
| [[6.注意力机制（AI增强版）]] | 6 | 1 | 0 | PASS |
| [[7.Seq2Seq英译法案例（AI增强版）]] | 1 | 1 | 0 | PASS |
| [[8.Transformer模型架构（AI增强版）]] | 9 | 1 | 1 | PASS |
| [[9.迁移学习与预训练模型应用（AI增强版）]] | 5 | 1 | 1 | PASS |
| [[10.中文文本分类案例（AI增强版）]] | 2 | 1 | 0 | PASS |
| [[11.fasttext工具详解与应用（AI增强版）]] | 5 | 1 | 1 | PASS |
| [[12.BERT系列预训练模型详解（AI增强版）]] | 7 | 1 | 2 | PASS |
| [[13.迁移学习扩展案例（AI增强版）]] | 2 | 1 | 0 | PASS |
| **合计** | **63** | **13** | **7** | **PASS** |
