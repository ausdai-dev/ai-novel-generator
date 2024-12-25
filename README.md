# AI小说生成器

这是一个基于PySide6和GPT模型的AI小说生成器，能够自动生成各种类型的小说内容。

## 功能特点

- 支持多种小说类型（穿越、都市、修仙、玄幻、科幻）
- 智能生成小说大纲
- 自动扩写内容
- 智能校核和优化
- 导出Markdown格式
- 支持多种写作风格模仿
- 可自定义字数

## 安装依赖

```bash
pip install -r requirements.txt
```

## 配置

1. 复制 `.env.example` 文件并重命名为 `.env`
2. 在 `.env` 文件中配置你的 API 信息：
   ```
   OPENAI_API_BASE=你的API地址
   OPENAI_API_KEY=你的API密钥
   ```

## 运行方法

```bash
python novel_generator.py
```

## 使用说明

1. 选择小说类型
2. 设置目标字数
3. 选择写作风格
4. 点击"生成大纲"按钮生成初始大纲
5. 点击"扩写内容"按钮扩充内容
6. 点击"校核优化"按钮优化文本
7. 点击"导出Markdown"保存结果

## 系统要求

- Python 3.8+
- PySide6
- OpenAI API访问权限

## 注意事项

- 请确保在运行程序前正确配置 `.env` 文件
- 生成的小说文件会保存为 `novel.md`
- API调用可能需要付费，请注意使用频率

## 贡献

欢迎提交 Issue 和 Pull Request！ 