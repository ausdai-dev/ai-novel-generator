import sys
import json
import os
import re
from pathlib import Path
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                           QHBoxLayout, QPushButton, QTextEdit, QLabel, QComboBox,
                           QSpinBox, QGroupBox, QMessageBox, QProgressDialog,
                           QLineEdit, QCheckBox, QListWidget, QSlider, QScrollArea)
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
        self.setGeometry(100, 100, 1400, 900)
        
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
        
        # 小说名称输入（可选）
        name_layout = QHBoxLayout()
        self.name_edit = QLineEdit()
        self.name_edit.setPlaceholderText("（可选）请输入小说名称，留空则由AI生成")
        name_layout.addWidget(QLabel("小说名称："))
        name_layout.addWidget(self.name_edit)
        basic_layout.addLayout(name_layout)
        
        # 故事梗概输入（可选）
        self.synopsis_edit = QTextEdit()
        self.synopsis_edit.setPlaceholderText("（可选）请输入故事梗概，约200字，留空则由AI生成")
        self.synopsis_edit.setMaximumHeight(100)
        basic_layout.addWidget(QLabel("故事梗概："))
        basic_layout.addWidget(self.synopsis_edit)
        
        # 类型选择
        self.genre_combo = QComboBox()
        self.genre_combo.addItems(["穿越", "都市", "修仙", "玄幻", "科幻"])
        basic_layout.addWidget(QLabel("选择类型："))
        basic_layout.addWidget(self.genre_combo)
        
        # 字数设置（使用滑块）
        word_count_layout = QVBoxLayout()
        self.word_count_slider = QSlider(Qt.Horizontal)
        self.word_count_slider.setRange(1000, 100000)
        self.word_count_slider.setSingleStep(1000)
        self.word_count_slider.setValue(5000)
        self.word_count_label = QLabel(f"目标字数：{self.word_count_slider.value()}字")
        self.word_count_slider.valueChanged.connect(
            lambda v: self.word_count_label.setText(f"目标字数：{v}字")
        )
        word_count_layout.addWidget(self.word_count_label)
        word_count_layout.addWidget(self.word_count_slider)
        basic_layout.addLayout(word_count_layout)
        
        # 主要人物数量设置（使用滑块）
        character_count_layout = QVBoxLayout()
        self.character_count_slider = QSlider(Qt.Horizontal)
        self.character_count_slider.setRange(1, 10)
        self.character_count_slider.setSingleStep(1)
        self.character_count_slider.setValue(3)
        self.character_count_label = QLabel(f"主要人物数量：{self.character_count_slider.value()}人")
        self.character_count_slider.valueChanged.connect(
            lambda v: self.character_count_label.setText(f"主要人物数量：{v}人")
        )
        character_count_layout.addWidget(self.character_count_label)
        character_count_layout.addWidget(self.character_count_slider)
        basic_layout.addLayout(character_count_layout)
        
        # 写作风格选择
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
        
        # 添加翻译设置组
        translation_group = QGroupBox("翻译设置")
        translation_layout = QVBoxLayout()
        
        # 是否启用翻译
        self.enable_translation = QCheckBox("启用翻译和文化适应")
        translation_layout.addWidget(self.enable_translation)
        
        # 创建滚动区域用于语言选择
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_widget = QWidget()
        scroll_layout = QVBoxLayout()
        scroll_widget.setLayout(scroll_layout)
        
        # 目标语言复选框组
        self.target_languages = {
            "英语 (English)": {
                "code": "en",
                "culture": "英美文化",
                "format": "英语写作风格",
                "taboos": "避免文化冲突、种族歧视等敏感话题"
            },
            "日语 (日本語)": {
                "code": "ja",
                "culture": "日本文化",
                "format": "日式写作风格，注重含蓄和意境",
                "taboos": "注意避免涉及敏感历史话题"
            },
            "法语 (Français)": {
                "code": "fr",
                "culture": "法国文化",
                "format": "法语文学传统",
                "taboos": "尊重法国文化传统和价值观"
            },
            "西班牙语 (Español)": {
                "code": "es",
                "culture": "西班牙及拉美文化",
                "format": "西班牙语文学风格",
                "taboos": "注意不同地区文化差异"
            },
            "俄语 (Русский)": {
                "code": "ru",
                "culture": "俄罗斯文化",
                "format": "俄罗斯文学传统",
                "taboos": "注意政治敏感性"
            },
            "阿拉伯语 (العربية)": {
                "code": "ar",
                "culture": "阿拉伯文化",
                "format": "阿拉伯文学传统",
                "taboos": "尊重伊斯兰文化传统和禁忌"
            },
            "葡萄牙语 (Português)": {
                "code": "pt",
                "culture": "葡萄牙及巴西文化",
                "format": "葡萄牙语文学风格",
                "taboos": "注意不同地区文化差异"
            }
        }
        
        # 创建语言复选框字典
        self.language_checkboxes = {}
        
        # 添加语言复选框
        scroll_layout.addWidget(QLabel("目标语言（可多选）："))
        for lang_name in self.target_languages.keys():
            checkbox = QCheckBox(lang_name)
            checkbox.setEnabled(False)  # 初始状态设为禁用
            self.language_checkboxes[lang_name] = checkbox
            scroll_layout.addWidget(checkbox)
        
        scroll_layout.addStretch()
        scroll_area.setWidget(scroll_widget)
        translation_layout.addWidget(scroll_area)
        
        # 连接翻译启用状态变化
        self.enable_translation.stateChanged.connect(
            lambda state: self._update_language_checkboxes(state)
        )
        
        translation_group.setLayout(translation_layout)
        left_layout.addWidget(translation_group)
        
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

        # 存储扩写后的章节内容
        self.expanded_chapters = []

    def generate_outline(self):
        if not self._check_api_key():
            return
            
        style_prompt = ""
        if self.style_combo.currentText() != "默认风格":
            style_prompt = f"请模仿{self.style_combo.currentText().split(' - ')[0]}的写作风格，"
            
        synopsis = self.synopsis_edit.toPlainText().strip()
        synopsis_prompt = f"\n已有故事梗概：\n{synopsis}\n请基于此梗概进行扩展。" if synopsis else ""
            
        prompt = f"""{style_prompt}作为一个小说大纲生成专家，请为我生成一个{self.genre_combo.currentText()}类型的小说大纲。{synopsis_prompt}

要求：
1. 包含新颖的故事情节
2. 设计{self.character_count_slider.value()}个性格鲜明的主要人物
3. 有吸引人的冲突
4. 列出5-8个主要章节梗概
5. 考虑总字数约{self.word_count_slider.value()}字的内容规划，每个章节字数可以灵活分配
6. 明确标注每个章节的预计字数和章节名称
"""
        
        response = self._call_api(prompt)
        if response:
            self.text_edit.setText(response)
            self.expanded_chapters = []  # 清空之前的章节内容

    def expand_content(self):
        if not self._check_api_key():
            return
            
        if not self._check_novel_name():
            return
            
        current_text = self.text_edit.toPlainText()
        if not current_text:
            return

        # 创建进度对话框
        progress = QProgressDialog("正在扩写内容...", "取消", 0, 100, self)
        progress.setWindowModality(Qt.WindowModal)
        progress.setWindowTitle("扩写进度")
        progress.show()

        try:
            # 分析大纲，获取章节列表
            chapters = self._split_into_chapters(current_text)
            total_chapters = len(chapters)
            target_words_per_chapter = self.word_count_slider.value() // total_chapters

            # 存储所有扩写后的内容
            self.expanded_chapters = []
            
            # 逐章扩写
            for i, chapter in enumerate(chapters):
                progress.setValue(int((i / total_chapters) * 100))
                if progress.wasCanceled():
                    break

                style_prompt = ""
                if self.style_combo.currentText() != "默认风格":
                    style_prompt = f"请模仿{self.style_combo.currentText().split(' - ')[0]}的写作风格，"
                
                prompt = f"""{style_prompt}作为一个专业的小说扩写专家，请对以下章节进行详细扩写：
                {chapter}
                
                要求：
                1. 保持情节连贯性
                2. 添加生动的细节描写
                3. 增加人物对话
                4. 丰富环境描写
                5. 严格控制扩写后的内容在{target_words_per_chapter}字左右
                6. 注意与其他章节的连贯性
                7. 请在扩写时精确计算字数，确保不超出限制
                8. 在章节开始处标注章节标题
                """
                
                response = self._call_api(prompt)
                if response:
                    self.expanded_chapters.append(response)

            # 合并所有章节
            if self.expanded_chapters:
                final_content = "\n\n".join(self.expanded_chapters)
                self.text_edit.setText(final_content)

        finally:
            progress.close()

    def _split_into_chapters(self, text):
        """将大纲文本割成章节列表"""
        chapters = []
        current_chapter = []
        
        for line in text.split('\n'):
            if line.strip().startswith(('第', '章', '1.', '2.', '3.', '4.', '5.', '6.', '7.', '8.', '9.')):
                if current_chapter:
                    chapters.append('\n'.join(current_chapter))
                current_chapter = [line]
            else:
                current_chapter.append(line)
        
        if current_chapter:
            chapters.append('\n'.join(current_chapter))
        
        return chapters

    def _extract_chapter_title(self, chapter_text):
        """从章节内容中取标题"""
        lines = chapter_text.split('\n')
        for line in lines[:3]:  # 只检查前三行
            line = line.strip()
            if line.startswith(('第', '章')) or re.match(r'^[1-9]\.', line):
                return line
        return "未命名章节"

    def review_content(self):
        if not self._check_api_key():
            return
            
        if not self._check_novel_name():
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
        4. 确保人物��象统一
        5. 严格确保总字数在{self.word_count_slider.value()}字左右，当前内容如果超出或不足目标字数，请适当调整
        6. 请在优化时精确计算字数
        7. 在保持故事完整性的前提下，确保字数符合要求
        8. 保持章节标题格式统一
        """
        
        response = self._call_api(prompt)
        if response:
            self.text_edit.setText(response)
            # 更新expanded_chapters，如果之前有扩写内容的话
            if self.expanded_chapters:
                self.expanded_chapters = self._split_into_chapters(response)

    def _update_language_checkboxes(self, state):
        """更新语言复选框的启用状态"""
        enabled = bool(state)  # 将Qt.Checked转换为布尔值
        for checkbox in self.language_checkboxes.values():
            checkbox.setEnabled(enabled)
            if not enabled:
                checkbox.setChecked(False)

    def _get_selected_languages(self):
        """获取所有选中的语言信息"""
        selected_languages = []
        for lang_name, checkbox in self.language_checkboxes.items():
            if checkbox.isChecked() and lang_name in self.target_languages:
                selected_languages.append((lang_name, self.target_languages[lang_name]))
        return selected_languages

    def _translate_and_adapt(self, text):
        """翻译并进行文化适应"""
        if not self.enable_translation.isChecked():
            return {}
            
        translations = {}
        selected_languages = self._get_selected_languages()
        
        if not selected_languages:
            return {}
            
        progress = QProgressDialog("正在进行翻译...", "取消", 0, len(selected_languages), self)
        progress.setWindowModality(Qt.WindowModal)
        progress.setWindowTitle("翻译进度")
        progress.show()
        
        try:
            for i, (lang_name, lang_info) in enumerate(selected_languages):
                progress.setValue(i)
                if progress.wasCanceled():
                    break
                    
                prompt = f"""请将以下中文小说翻译成{lang_info['code']}，并进行文化适应改写：

原文：
{text}

要求：
1. 使用{lang_info['culture']}背景进行改写
2. 调整时间、地点、人物名字等元素以符合目标文化
3. 采用{lang_info['format']}
4. {lang_info['taboos']}
5. 保持故事核心情节不变
6. 确保翻译准确性和文学性
7. 适应目标语言的表达习惯和修辞特点
8. 保持章节结构
"""
                
                response = self._call_api(prompt)
                if response:
                    translations[lang_name] = response
                    
            return translations
            
        except Exception as e:
            self.text_edit.append(f"\n\n翻译失败：{str(e)}")
            return {}
        finally:
            progress.close()

    def _generate_novel_name(self):
        """如果用户未输入小说名称，则由AI生成"""
        if self.name_edit.text().strip():
            return self.name_edit.text().strip()
            
        synopsis = self.synopsis_edit.toPlainText().strip()
        current_text = self.text_edit.toPlainText()
        
        prompt = f"""请为这个小说生成一个吸引人的标题。

类型：{self.genre_combo.currentText()}
写作风格：{self.style_combo.currentText()}
故事梗概：{synopsis if synopsis else '无'}
内容预览：{current_text[:500] if current_text else '无'}

要求：
1. 标题要简洁有力
2. 符合小说内容和风格
3. 具有吸引力和记忆点
4. 不要使用网络小说常见的套路标题
"""
        
        response = self._call_api(prompt)
        if response:
            # 清理可能的多余内容，只保留标题
            title = response.strip().split('\n')[0].strip()
            self.name_edit.setText(title)
            return title
            
        return "未命名小说"

    def export_markdown(self):
        current_text = self.text_edit.toPlainText()
        if not current_text:
            return
            
        try:
            # 确保有小说名称
            novel_name = self._generate_novel_name()
            
            # 创建小说专属文件夹
            folder_path = Path(novel_name)
            folder_path.mkdir(exist_ok=True)
            
            # 获取总字数
            total_words = len(current_text)
            
            # 保存源文件（中文版本）
            self._save_novel_version(folder_path, novel_name, current_text, "源文件", self.expanded_chapters)
            
            # 如果启用了翻译，生成翻译版本
            if self.enable_translation.isChecked():
                translations = self._translate_and_adapt(current_text)
                for lang_name, translated_text in translations.items():
                    lang_code = self.target_languages[lang_name]["code"]
                    translated_chapters = self._split_into_chapters(translated_text) if total_words > 20000 else None
                    self._save_novel_version(folder_path, novel_name, translated_text, lang_code, translated_chapters)
            
            self.text_edit.append(f"\n\n已成功保存所有版本到 {folder_path} 文件夹！")
            self.text_edit.append(f"总字数：{total_words}")
                
        except Exception as e:
            self.text_edit.append(f"\n\n导出失败：{str(e)}")

    def _save_novel_version(self, folder_path, novel_name, content, version_suffix, chapters=None):
        """保存小说的某个版本（源文件或翻译版本）"""
        try:
            # 如果有章节且总字数超过20000，则分章节保存
            if chapters and len(content) > 20000:
                # 保存每个章节
                for i, chapter in enumerate(chapters, 1):
                    chapter_title = self._extract_chapter_title(chapter)
                    filename = f"{novel_name}-第{i}章-{chapter_title}-{version_suffix}.md"
                    filepath = folder_path / filename
                    
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(chapter)
                
                # 同时保存完整版本
                full_filepath = folder_path / f"{novel_name}-完整版-{version_suffix}.md"
                with open(full_filepath, 'w', encoding='utf-8') as f:
                    f.write(content)
                    
            else:
                # 保存为单个文件
                filepath = folder_path / f"{novel_name}-{version_suffix}.md"
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(content)
                    
        except Exception as e:
            self.text_edit.append(f"\n\n保存{version_suffix}版本失败：{str(e)}")

    def _check_api_key(self):
        """检查API密钥是否已配置"""
        if not openai.api_key:
            QMessageBox.warning(self, "配置缺失", "请在.env文件中配置OPENAI_API_KEY")
            return False
        return True

    def _check_novel_name(self):
        """检查小说名称是否已输入"""
        if not self.name_edit.text().strip():
            QMessageBox.warning(self, "名称缺失", "请输入小说名称")
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
                    {"role": "system", "content": "你是一个专业的小说创作助手，擅长故事构思、情节发展和文字优化。在生成内容时，你会严格控制字数限制。"},
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