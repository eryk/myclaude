---
name: x-thread-reader
description: 读取 X/Twitter 推文及作者跟帖(thread)，生成中文摘要。当用户提供 x.com 或 twitter.com 链接并请求分析、总结、阅读时自动触发。适用于"总结这条推文"、"分析这个 thread"、"读一下这条推"等请求。
allowed-tools: [WebFetch]
---

# X/Twitter Thread Reader

读取指定推文及作者跟帖，提取核心观点，生成结构化中文摘要。

## 使用方法

用户提供推文链接并请求分析即可：

```
"总结这条推文：https://x.com/用户名/status/推文ID"
"分析一下这个 thread：[URL]"
"帮我读一下这条推：[URL]"
"这条推文说了什么：[URL]"
```

## 工作流程

### 第一步：解析 URL

从用户提供的链接中提取用户名和推文 ID。

支持的 URL 格式：
- `https://x.com/用户名/status/推文ID`
- `https://twitter.com/用户名/status/推文ID`
- `https://mobile.twitter.com/用户名/status/推文ID`

URL 可能带有查询参数（如 `?s=20`），需要忽略这些参数，只提取核心部分。

### 第二步：调用 FxTwitter API

使用 WebFetch 工具请求：

```
https://api.fxtwitter.com/用户名/status/推文ID
```

Prompt 使用："Extract the complete JSON response"

### 第三步：解析返回数据

API 返回 JSON 格式数据，关键字段：

```json
{
  "tweet": {
    "author": {
      "name": "显示名称",
      "screen_name": "用户名"
    },
    "text": "推文正文内容",
    "created_at": "发布时间",
    "replies": 回复数,
    "retweets": 转发数,
    "likes": 点赞数,
    "thread": [
      { "text": "跟帖1内容" },
      { "text": "跟帖2内容" }
    ]
  }
}
```

注意：
- `thread` 字段可能不存在（单条推文无跟帖）
- 需要将主推文和所有 thread 内容合并分析

### 第四步：生成中文摘要

按以下格式输出：

```markdown
## 📌 推文信息
- **作者**：[显示名] (@[用户名])
- **发布时间**：[格式化的时间]
- **互动数据**：❤️ [点赞数] | 🔁 [转发数] | 💬 [回复数]

## 📝 内容摘要
[1-2 句话概括整个 thread 的核心主题]

## 🔑 核心观点
1. [要点一]
2. [要点二]
3. [要点三]
...

## 📄 原文概览
> [主推文原文摘录]
> [如有 thread 标注：含 N 条跟帖]
```

### 摘要原则

1. **简洁优先**：突出核心信息，去除冗余内容
2. **Thread 整合**：将多条跟帖作为一个完整论述分析
3. **中文输出**：无论原文是什么语言，摘要均使用中文
4. **观点提炼**：提取作者的核心主张和关键论据

## 错误处理

- **URL 格式无效**：提示用户提供正确的 x.com 或 twitter.com 链接
- **API 请求失败**：提示推文可能是私密的、已删除、或暂时无法访问
- **无法解析内容**：显示原始返回信息供用户参考

## 示例

**输入：**
```
总结这条推文：https://x.com/elonmusk/status/1234567890
```

**输出：**
```markdown
## 📌 推文信息
- **作者**：Elon Musk (@elonmusk)
- **发布时间**：2024-01-15 10:30
- **互动数据**：❤️ 125.3K | 🔁 23.1K | 💬 8.2K

## 📝 内容摘要
马斯克分享了关于 AI 发展的最新思考，强调了开源模型的重要性以及对 AGI 时间线的预测。

## 🔑 核心观点
1. 开源 AI 模型对于技术民主化至关重要
2. AGI 可能在未来 3-5 年内实现
3. 需要建立全球性的 AI 安全框架

## 📄 原文概览
> "AI development is accelerating faster than most people realize..."
> 含 4 条跟帖
```
