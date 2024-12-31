# AI小说生成器

一个基于人工智能的小说生成工具，可以帮助作者快速创作小说。

## 功能特点

- 自动生成小说名称和故事梗概
- 生成详细的角色设定
- 生成章节大纲
- 自动扩写章节内容
- 支持多语言翻译
- 支持导出为 TXT 格式
- 现代化的图形界面
- 支持多种写作风格和文化背景

## 系统要求

- Windows 10 或更高版本
- Python 3.9 或更高版本
- OpenAI API 密钥

## 安装说明

1. 克隆仓库：
```bash
git clone https://github.com/yourusername/novel-generator.git
cd novel-generator
```

2. 安装依赖：
```bash
pip install -r requirements.txt
```

3. 配置 API：
   - 复制 `.env.example` 为 `.env`
   - 在 `.env` 文件中填入您的 OpenAI API 密钥

4. 运行程序：
```bash
python novel_generator.py
```

## 使用说明

1. 启动程序后，您可以：
   - 输入小说名称或让 AI 自动生成
   - 选择小说类型和写作风格
   - 设置章节数量和每章字数
   - 配置主要和次要人物数量

2. 点击"生成大纲"按钮，程序会：
   - 生成故事梗概
   - 创建角色设定
   - 生成章节大纲

3. 点击"扩写内容"按钮，程序会：
   - 根据大纲扩写每个章节
   - 自动保存扩写内容
   - 显示写作进度

4. 如需翻译，可以：
   - 勾选"启用翻译"
   - 选择目标语言
   - 点击"翻译内容"按钮

5. 所有生成的内容都会自动保存在以小说名命名的文件夹中。

## 注意事项

- 请确保您有足够的 API 额度
- 建议在扩写前仔细检查大纲和角色设定
- 生成的内容可能需要进一步修改和润色
- 请遵守 OpenAI 的使用条款和政策

## 许可证

本项目采用 MIT 许可证，详见 [LICENSE](LICENSE) 文件。

## 贡献指南

欢迎提交 Issue 和 Pull Request。在提交代码前，请确保：

1. 代码符合 PEP 8 规范
2. 添加了必要的注释和文档
3. 通过了所有测试
4. 更新了 README 和相关文档

## 更新日志

### v1.0.0 (2024-01-20)
- 初始版本发布
- 实现基本的小说生成功能
- 支持多语言翻译
- 添加现代化 UI 界面

## 联系方式

如有问题或建议，请通过以下方式联系：

- 提交 Issue
- 发送邮件至：your.email@example.com

## 致谢

感谢所有为本项目做出贡献的开发者。 