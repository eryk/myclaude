---
name: iterm
description: 读取指定 iTerm2 session 的最近输出内容。使用 "/iterm <名称> [行数]" 获取内容，或 "/iterm" 列出所有 session。适用于调试时获取其他终端窗口的日志输出，免去手动复制粘贴。
allowed-tools: [Bash]
---

# iTerm Session Reader

从 iTerm2 的其他窗口/Tab 中读取终端输出，用于调试和日志查看。

## 使用方法

```
/iterm <session名称> [行数]

# 示例
/iterm debug-server        # 获取 debug-server 的最近 50 行
/iterm debug-server 200    # 获取最近 200 行
/iterm                     # 列出所有可用 session
```

## 设置 Session 名称

在目标 iTerm 窗口中执行以下命令设置名称：

```bash
# 设置 Tab/Session 标题
echo -ne "\033]0;debug-server\007"
```

或者：右键点击 Tab → "Edit Session Title..."

## 工作流程

### 第一步：解析参数

从用户输入中提取：
- `session_name`：目标 session 名称（可选）
- `line_count`：获取行数，默认 50

### 第二步：执行对应操作

**情况 A：未指定 session 名称**

列出所有可用的 session：

```bash
osascript -e '
tell application "iTerm2"
    set output to ""
    set winIndex to 1
    repeat with w in windows
        set tabIndex to 1
        repeat with t in tabs of w
            repeat with s in sessions of t
                set sessionName to name of s
                set output to output & winIndex & "\t" & tabIndex & "\t" & sessionName & "\n"
                set tabIndex to tabIndex + 1
            end repeat
        end repeat
        set winIndex to winIndex + 1
    end repeat
    return output
end tell'
```

然后格式化输出为表格，提示用户选择。

**情况 B：指定了 session 名称**

搜索匹配的 session 并**在 AppleScript 内部截取最后 N 行**（避免传输全部内容）：

```bash
osascript -e '
on getLastNLines(theText, n)
    set theLines to paragraphs of theText
    set lineCount to count of theLines
    if lineCount ≤ n then
        return theText
    end if
    set startIndex to lineCount - n + 1
    set resultLines to items startIndex thru -1 of theLines
    set AppleScript'\''s text item delimiters to linefeed
    set resultText to resultLines as text
    set AppleScript'\''s text item delimiters to ""
    return resultText
end getLastNLines

tell application "iTerm2"
    repeat with w in windows
        repeat with t in tabs of w
            repeat with s in sessions of t
                if name of s contains "SESSION_NAME" then
                    set sessionText to contents of s
                    return my getLastNLines(sessionText, LINE_COUNT)
                end if
            end repeat
        end repeat
    end repeat
    return "SESSION_NOT_FOUND"
end tell'
```

将 `SESSION_NAME` 替换为用户指定的名称，`LINE_COUNT` 替换为行数（默认 50）。

### 第三步：处理内容

1. 如果返回 `SESSION_NOT_FOUND`，执行情况 A 列出所有 session
2. 清理输出（去除首尾空行）

### 第四步：智能分析

根据当前对话上下文决定输出方式：

- **正在调试问题**：分析输出内容，关联之前讨论的 bug，给出建议
- **首次获取**：展示内容，简要指出发现的错误、警告或异常
- **纯查看需求**：直接展示内容

## 输出格式

### 成功获取内容

```markdown
## 📺 iTerm Session: {session_name} (最近 {line_count} 行)

```
{输出内容}
```

## 🔍 分析
{根据上下文的智能分析，如果没有明显问题则省略此部分}
```

### 列出所有 session

```markdown
## 📋 可用的 iTerm Sessions

| # | Session 名称 | 窗口 | Tab |
|---|-------------|------|-----|
| 1 | debug-server | 1 | 1 |
| 2 | ssh-prod | 1 | 2 |
| 3 | local-dev | 2 | 1 |

使用方式: `/iterm <session名称> [行数]`
```

### 未找到 session

```markdown
## ⚠️ 未找到 session: {session_name}

## 📋 可用的 iTerm Sessions

{session 列表表格}
```

## 错误处理

| 场景 | 处理方式 |
|------|----------|
| iTerm2 未运行 | 提示 "iTerm2 未运行，请先启动 iTerm2" |
| 没有任何 session | 提示 "当前没有打开的 iTerm session" |
| 未找到指定 session | 显示 "未找到 'xxx'"，并列出所有可用 session |
| AppleScript 执行失败 | 显示错误信息，提示检查系统偏好设置中的自动化权限 |
| 内容为空 | 提示 "该 session 暂无输出内容" |

## 权限说明

首次使用时，macOS 可能会提示授权。需要在：

**系统偏好设置 → 隐私与安全性 → 自动化**

允许终端应用（如 Terminal、iTerm2、或你使用的终端）控制 iTerm2。

## 示例

**输入：**
```
/iterm debug-server 100
```

**输出：**
```markdown
## 📺 iTerm Session: debug-server (最近 100 行)

```
2024-01-15 10:30:15 INFO  Starting server on port 3000
2024-01-15 10:30:16 INFO  Database connected
2024-01-15 10:30:20 ERROR Connection refused: Redis not available
2024-01-15 10:30:21 WARN  Retrying Redis connection...
...
```

## 🔍 分析
发现 1 个错误：
- **Redis 连接失败** (行 3): `Connection refused: Redis not available`

建议：检查 Redis 服务是否已启动，或确认连接配置是否正确。
```
