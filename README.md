# AI 小说生成器

一个基于人工智能的小说生成工具，可以帮助作者快速创作小说。

## 功能特点

- 自动生成小说名称和故事梗概
- 根据设定生成详细的章节大纲
- 自动扩写章节内容
- 支持多种小说类型和写作风格
- 支持多语言翻译
- 可调节章节数量和字数
- 支持导出 Markdown 和 TXT 格式

## 系统要求

- Python 3.8 或更高版本
- PySide6
- OpenAI API 密钥

## 安装步骤

1. 克隆仓库：
```bash
git clone https://github.com/your-username/novel-generator.git
cd novel-generator
```

2. 安装依赖：
```bash
pip install -r requirements.txt
```

3. 配置 API：
创建 `.env` 文件并添加以下内容：
```
OPENAI_API_BASE=your-api-base-url
OPENAI_API_KEY=your-api-key
```

## 使用说明

1. 运行程序：
```bash
python novel_generator.py
```

2. 在界面中设置小说参数：
   - 输入小说名称（可选）
   - 输入故事梗概（可选）
   - 选择小说类型
   - 选择写作风格
   - 调整章节数量和字数
   - 设置人物数量

3. 点击"生成大纲"按钮生成章节大纲
4. 点击"扩写内容"按钮扩写详细内容
5. 如需翻译，勾选"启用翻译"并选择目标语言
6. 使用"转换为txt"按钮可将生成的文件转换为TXT格式

## 许可证

MIT License 