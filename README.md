# AI小说生成器

一个基于GPT的小说生成工具，可以自动生成小说大纲、扩写内容，并支持多语言翻译。

## 功能特点

- 自动生成小说名称和故事简介
- 可定制章节数量和每章字数
- 支持多种小说类型和写作风格
- 可设置主要和次要人物数量
- 支持多种文化背景元素
- 自动扩写章节内容
- 支持多语言翻译
- 支持导出为txt格式

## 环境要求

- Python 3.8+
- PySide6
- OpenAI API密钥

## 安装步骤

1. 克隆仓库
```bash
git clone https://github.com/yourusername/novel-generator.git
cd novel-generator
```

2. 安装依赖
```bash
pip install -r requirements.txt
```

3. 配置环境变量
创建`.env`文件并添加以下内容：
```
OPENAI_API_KEY=你的API密钥
OPENAI_API_BASE=https://api.openai.com/v1  # 或其他API地址
```

## 使用说明

1. 运行程序
```bash
python novel_generator.py
```

2. 在界面中设置：
   - 小说类型
   - 写作风格
   - 文化背景
   - 章节数量
   - 每章字数
   - 人物数量

3. 点击"生成大纲"按钮生成小说大纲

4. 点击"扩写内容"按钮将大纲扩写为完整内容

5. 可选：使用翻译功能将内容翻译为其他语言

6. 可选：点击"转换为txt"按钮将所有内容导出为txt格式

## 文件说明

- `novel_generator.py`: 主程序文件
- `novel_generator_ui.py`: UI界面文件
- `novel_generator_ui.ui`: Qt Designer UI设计文件
- `requirements.txt`: 项目依赖文件

## 注意事项

- 请确保有足够的API额度
- 生成的内容会自动保存为markdown格式
- 可以随时将内容导出为txt格式
- 建议在生成前先设置好所有参数

## 许可证

MIT License 