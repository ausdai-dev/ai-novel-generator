import sys
import json
import os
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                           QHBoxLayout, QPushButton, QTextEdit, QLabel, QComboBox,
                           QSpinBox, QGroupBox, QMessageBox)
from PySide6.QtCore import Qt
import openai
import requests
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 配置API
openai.api_base = os.getenv("OPENAI_API_BASE", "https://free.v36.cm/v1")
openai.api_key = os.getenv("OPENAI_API_KEY", "")

class NovelGenerator(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AI小说生成器")
        self.setGeometry(100, 100, 1200, 800)
        
        # 检查API配置
        if not openai.api_key:
            QMessageBox.warning(self, "配置缺失", "请在.env文件中配置OPENAI_API_KEY")
        
        # 创建中心部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 创建布局
        layout = QHBoxLayout()
        central_widget.setLayout(layout)
        
        # 左侧控制面板
        left_panel = QWidget()
        left_layout = QVBoxLayout()
        left_panel.setLayout(left_layout)
        
        # 创建基本设置组
        basic_group = QGroupBox("基本设置")
        basic_layout = QVBoxLayout()
        
        # 类型选择
        self.genre_combo = QComboBox()
        self.genre_combo.addItems(["穿越", "都市", "修仙", "玄幻", "科幻"])
        basic_layout.addWidget(QLabel("选择类型："))
        basic_layout.addWidget(self.genre_combo)
        
        # 字数设置
        word_count_layout = QHBoxLayout()
        self.word_count_spin = QSpinBox()
        self.word_count_spin.setRange(1000, 100000)
        self.word_count_spin.setSingleStep(1000)
        self.word_count_spin.setValue(5000)
        self.word_count_spin.setSuffix(" 字")
        word_count_layout.addWidget(QLabel("目标字数："))
        word_count_layout.addWidget(self.word_count_spin)
        basic_layout.addLayout(word_count_layout)
        
        # 写作���格选择
        self.style_combo = QComboBox()
        self.style_combo.addItems([
            "默认风格",
            "金庸风格 - 武侠文学",
            "莫言风格 - 现实主义",
            "刘慈欣风格 - 科幻硬核",
            "南派三叔风格 - 悬疑探险",
            "天蚕土豆风格 - 玄幻",
            "我吃西红柿风格 - 修真"
        ])
        basic_layout.addWidget(QLabel("写作风格："))
        basic_layout.addWidget(self.style_combo)
        
        basic_group.setLayout(basic_layout)
        left_layout.addWidget(basic_group)
        
        # 操作按钮
        self.generate_btn = QPushButton("生成大纲")
        self.generate_btn.clicked.connect(self.generate_outline)
        left_layout.addWidget(self.generate_btn)
        
        self.expand_btn = QPushButton("扩写内容")
        self.expand_btn.clicked.connect(self.expand_content)
        left_layout.addWidget(self.expand_btn)
        
        self.review_btn = QPushButton("校核优化")
        self.review_btn.clicked.connect(self.review_content)
        left_layout.addWidget(self.review_btn)
        
        self.export_btn = QPushButton("导出Markdown")
        self.export_btn.clicked.connect(self.export_markdown)
        left_layout.addWidget(self.export_btn)
        
        left_layout.addStretch()
        
        # 右侧文本显示区域
        self.text_edit = QTextEdit()
        self.text_edit.setPlaceholderText("这里将显示生成的内容...")
        
        # 添加到主布局
        layout.addWidget(left_panel, 1)
        layout.addWidget(self.text_edit, 4)

    def generate_outline(self):
        if not self._check_api_key():
            return
            
        style_prompt = ""
        if self.style_combo.currentText() != "默认风格":
            style_prompt = f"请模仿{self.style_combo.currentText().split(' - ')[0]}的写作风格，"
            
        prompt = f"""{style_prompt}作为一个小说大纲生成专家，请为我生成一个{self.genre_combo.currentText()}类型的小说大纲。
        要求：
        1. 包含新颖的故事情节
        2. 有明确的人物设定
        3. 有吸引人的冲突
        4. 列出5-8个主要章节梗概
        5. 考虑总字数约{self.word_count_spin.value()}字的内容规划
        """
        
        response = self._call_api(prompt)
        if response:
            self.text_edit.setText(response)

    def expand_content(self):
        if not self._check_api_key():
            return
            
        current_text = self.text_edit.toPlainText()
        if not current_text:
            return
            
        style_prompt = ""
        if self.style_combo.currentText() != "默认风格":
            style_prompt = f"请模仿{self.style_combo.currentText().split(' - ')[0]}的写作风格，"
            
        prompt = f"""{style_prompt}作为一个专业的小说扩写专家，请基于以下大纲进行详细的内容扩写：
        {current_text}
        
        要求：
        1. 保持情节连贯性
        2. 添加生动的细节描写
        3. 增加人物对话
        4. 丰富环境描写
        5. 扩写后的内容总字数控制在{self.word_count_spin.value()}字左右
        """
        
        response = self._call_api(prompt)
        if response:
            self.text_edit.setText(response)

    def review_content(self):
        if not self._check_api_key():
            return
            
        current_text = self.text_edit.toPlainText()
        if not current_text:
            return
            
        style_prompt = ""
        if self.style_combo.currentText() != "默认风格":
            style_prompt = f"请保持{self.style_combo.currentText().split(' - ')[0]}的写作风格，"
            
        prompt = f"""{style_prompt}作为一个专业的文学编辑，请对以下内容进行审核和优化：
        {current_text}
        
        要求：
        1. 检查情节逻辑性
        2. 优化语言表达
        3. 提升文学性
        4. 确保人物形象统一
        5. 确保总字数在{self.word_count_spin.value()}字左右
        """
        
        response = self._call_api(prompt)
        if response:
            self.text_edit.setText(response)

    def export_markdown(self):
        current_text = self.text_edit.toPlainText()
        if not current_text:
            return
            
        try:
            with open('novel.md', 'w', encoding='utf-8') as f:
                f.write(current_text)
            self.text_edit.append("\n\n已成功导出到 novel.md 文件！")
        except Exception as e:
            self.text_edit.append(f"\n\n导出失败：{str(e)}")

    def _check_api_key(self):
        """检查API密钥是否已配置"""
        if not openai.api_key:
            QMessageBox.warning(self, "配置缺失", "请在.env文件中配置OPENAI_API_KEY")
            return False
        return True

    def _call_api(self, prompt):
        try:
            headers = {
                "Authorization": f"Bearer {openai.api_key}",
                "Content-Type": "application/json"
            }
            
            data = {
                "model": "gpt-4o-mini",
                "messages": [
                    {"role": "system", "content": "你是一个专业的小说创作助手，擅长故事构思、情节发展和文字优化。"},
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0.7
            }
            
            response = requests.post(
                f"{openai.api_base}/chat/completions",
                headers=headers,
                json=data
            )
            
            if response.status_code == 200:
                result = response.json()
                if 'choices' in result and len(result['choices']) > 0:
                    return result['choices'][0]['message']['content']
                else:
                    self.text_edit.append("\n\nAPI响应格式错误")
                    return None
            else:
                self.text_edit.append(f"\n\nAPI错误状态码：{response.status_code}")
                self.text_edit.append(f"\n响应内容：{response.text}")
                return None
                
        except Exception as e:
            self.text_edit.append(f"\n\nAPI调用错误：{str(e)}")
            return None

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = NovelGenerator()
    window.show()
    sys.exit(app.exec()) 