# -*- coding: utf-8 -*-
import sys
import json
import os
import re
from pathlib import Path
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QMessageBox, QProgressDialog, 
    QCheckBox, QTextEdit, QComboBox, QVBoxLayout, QWidget, QPushButton, QGroupBox
)
from PySide6.QtCore import Qt, QTimer
import openai
import requests
from dotenv import load_dotenv
from novel_generator_ui import Ui_NovelGeneratorWindow
import time

# 设置默认编码为UTF-8
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')
if sys.stderr.encoding != 'utf-8':
    sys.stderr.reconfigure(encoding='utf-8')

# 加载环境变量
print("正在加载环境变量...")
env_path = Path('.env')
if env_path.exists():
    print(f"找到.env文件：{env_path.absolute()}")
    load_dotenv(encoding='utf-8')
    print("环境变量加载完成")
else:
    print("警告：未找到.env文件")

# 配置API
openai.api_base = os.getenv("OPENAI_API_BASE", "https://free.v36.cm/v1")
openai.api_key = os.getenv("OPENAI_API_KEY", "")
print(f"API基础URL：{openai.api_base}")
print(f"API密钥：{'已配置' if openai.api_key else '未配置'}")

class NovelGenerator(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # 存储扩写后的章节内容
        self.expanded_chapters = []
        
        # 存储当前小说名称
        self.current_novel_name = ""
        
        # 设置UI
        self.ui = Ui_NovelGeneratorWindow()
        self.ui.setupUi(self)
        
        # 检查API配置
        if not openai.api_key:
            QMessageBox.warning(self, "配置缺失", "请在.env文件中配置OPENAI_API_KEY")
        
        # 初始化UI组件
        self._init_ui()
        
        # 连接信号和槽
        self._connect_signals()

    def _show_message(self, title, text, icon=QMessageBox.Information, timeout=3000):
        """显示一个会自动关闭的消息框"""
        msg = QMessageBox(self)  # 设置父窗口
        msg.setIcon(icon)
        msg.setWindowTitle(title)
        msg.setText(text)
        msg.setStandardButtons(QMessageBox.Ok)
        
        # 创建定时器
        timer = QTimer(self)  # 设置父对象
        timer.timeout.connect(msg.close)
        timer.setSingleShot(True)
        timer.start(timeout)  # 3秒后自动关闭
        
        # 显示消息框并等待
        msg.exec()

    def _save_chapter_content(self, chapter_text, chapter_index, chapter_title, content_type, lang_name=None):
        """保存单个章节内容"""
        if not self.current_novel_name:
            return
            
        # 清理小说名称和章节标题
        safe_novel_name = self._sanitize_filename(self.current_novel_name)
        safe_chapter_title = self._sanitize_filename(chapter_title)
            
        # 创建小说主文件夹
        folder_path = Path(safe_novel_name)
        folder_path.mkdir(exist_ok=True)
        
        # 创建章节子文件夹
        chapters_folder = folder_path / "chapters"
        chapters_folder.mkdir(exist_ok=True)
        
        # 确保章节标题使用H3格式
        if not chapter_text.startswith('###'):
            lines = chapter_text.split('\n')
            chapter_text = f"### {lines[0]}" + '\n' + '\n'.join(lines[1:])
        
        # 根据内容类型确定文件名
        if content_type == "扩写":
            filename = f"第{chapter_index + 1:02d}章_{safe_chapter_title.split('_')[-1]}.md"
            chapter_filepath = chapters_folder / filename
            try:
                with open(chapter_filepath, 'w', encoding='utf-8') as f:
                    f.write(chapter_text)
                return chapter_text
            except Exception as e:
                self._show_message("保存失败", f"保存章节文件失败：{str(e)}", QMessageBox.Warning)
                return None
        else:  # 翻译
            safe_lang_name = self._sanitize_filename(lang_name)
            lang_folder = chapters_folder / safe_lang_name
            lang_folder.mkdir(exist_ok=True)
            
            filename = f"第{chapter_index + 1:02d}章_{safe_chapter_title.split('_')[-1]}.md"
            chapter_filepath = lang_folder / filename
            try:
                with open(chapter_filepath, 'w', encoding='utf-8') as f:
                    f.write(chapter_text)
                return chapter_text
            except Exception as e:
                self._show_message("保存失败", f"保存章节文件失败：{str(e)}", QMessageBox.Warning)
                return None

    def expand_content(self):
        """扩写内容"""
        print("开始扩写内容")
        if not self._check_api_key():
            return
            
        # 获取要扩写的内容
        current_text = self.ui.outlineEdit.toPlainText().strip()
        if not current_text:
            self._show_message("输入错误", "请先生成或输入故事大纲", QMessageBox.Warning)
            return

        # 获取小说名称
        novel_name = self.ui.nameEdit.text().strip()
        if not novel_name:
            self._show_message("输入错误", "请先输入或生成小说名称", QMessageBox.Warning)
            return
            
        self.current_novel_name = novel_name
        
        # 创建小说文件夹
        safe_novel_name = self._sanitize_filename(novel_name)
        novel_dir = Path(safe_novel_name)
        novel_dir.mkdir(exist_ok=True)
        
        # 保存故事梗概文件
        synopsis = self.ui.synopsisEdit.toPlainText().strip()
        synopsis_file = novel_dir / f"{safe_novel_name}-故事梗概.md"
        try:
            with open(synopsis_file, 'w', encoding='utf-8') as f:
                f.write(synopsis)
            print(f"故事梗概已保存到：{synopsis_file}")
        except Exception as e:
            print(f"保存故事梗概文件失败：{str(e)}")
            self._show_message("保存失败", f"保存故事梗概文件失败：{str(e)}", QMessageBox.Warning)
            return

        # 创建进度对话框
        progress = QProgressDialog("正在扩写内容...", "取消", 0, 100, self)
        progress.setWindowModality(Qt.WindowModal)
        progress.setWindowTitle("扩写进度")
        progress.show()

        try:
            # 分析大纲，获取章节列表
            chapters = self._split_into_chapters(current_text)
            if not chapters:
                self._show_message("章节识别失败", "无法从大纲中识别出章节，请检查大纲格式", QMessageBox.Warning)
                return
                
            # 处理章节
            total_chapters = len(chapters)
            chapter_count = self.ui.chapterCountSlider.value()
            avg_words = self.ui.avgChapterWordsSlider.value()
            total_words = chapter_count * avg_words

            # 存储所有扩写后的内容
            self.expanded_chapters = []
            all_expanded_content = []
            
            # 创建chapters目录
            chapters_dir = novel_dir / "chapters"
            chapters_dir.mkdir(exist_ok=True)
            
            # 逐章扩写
            for i, chapter in enumerate(chapters):
                progress.setValue(int((i / total_chapters) * 100))
                if progress.wasCanceled():
                    break

                style_prompt = ""
                if self.ui.styleCombo.currentText() != "默认风格":
                    style_prompt = f"请模仿{self.ui.styleCombo.currentText().split(' - ')[0]}的写作风格，"
                
                # 提取章节标题和内容
                chapter_lines = chapter.split('\n')
                chapter_title = chapter_lines[0].strip()
                chapter_content = '\n'.join(chapter_lines[1:]).strip()
                
                # 提取预计字数
                expected_words = None
                for line in chapter_lines:
                    if '预计字数' in line:
                        try:
                            expected_words = int(re.search(r'\d+', line).group())
                            break
                        except:
                            pass
                
                if not expected_words:
                    expected_words = avg_words
                
                # 允许的字数误差范围（15%）
                word_margin = int(expected_words * 0.15)
                min_words = expected_words - word_margin
                max_words = expected_words + word_margin
                
                # 构建扩写提示
                prompt = f"""{style_prompt}作为一个专业的小说扩写专家，请对《{novel_name}》的以下章节进行详细扩写：

章节标题：{chapter_title}
章节梗概：{chapter_content}
目标字数：{expected_words}字（允许范围：{min_words}-{max_words}字）
                
要求：
1. 严格按照章节梗概展开情节
2. 保持与其他章节的情节连贯性
3. 添加生动的细节描写和人物对话
4. 丰富环境描写和人物心理
5. 扩写后的内容必须严格控制在{min_words}-{max_words}字之间
6. 必须保持章节标题格式：{chapter_title}
7. 扩写时注意承上启下，与整体故事线保持一致
8. 不要在文末添加字数统计、优化总结等额外信息
"""
                
                # 尝试扩写，如果字数不对就重试
                max_retries = 3
                expanded_content = None
                success = False
                
                for retry in range(max_retries):
                    response = self._call_api(prompt)
                    if not response:
                        continue
                        
                    # 清理响应内容
                    cleaned_response = self._clean_response(response)
                    
                    # 检查字数
                    content_length = len(cleaned_response.replace('\n', '').replace(' ', ''))
                    if min_words <= content_length <= max_words:
                        # 字数符合要求
                        expanded_content = cleaned_response
                        success = True
                        break
                    else:
                        # 字数不符合要求，添加更严格的提示重试
                        if content_length < min_words:
                            prompt += f"\n\n当前扩写字数为{content_length}字，比目标字数少{min_words - content_length}字，请补充更多细节和对话。"
                        else:
                            prompt += f"\n\n当前扩写字数为{content_length}字，比目标字数多{content_length - max_words}字，请适当精简。"
                        
                        # 最后一次重试，即使字数不符合要求也保存结果
                        if retry == max_retries - 1:
                            expanded_content = cleaned_response
                
                # 保存扩写内容
                if expanded_content:
                    # 保存章节文件
                    chapter_file = chapters_dir / f"第{i+1:02d}章_{self._sanitize_filename(chapter_title.split('：')[-1])}.md"
                    try:
                        with open(chapter_file, 'w', encoding='utf-8') as f:
                            f.write(expanded_content)
                        print(f"已保存章节：{chapter_file}")
                        all_expanded_content.append(expanded_content)
                        self.expanded_chapters.append(expanded_content)
                        
                        if not success:
                            self._show_message("扩写提示", f"第{i+1}章 {chapter_title} 的字数控制未达到预期，建议后续手动调整。", QMessageBox.Warning)
                    except Exception as e:
                        print(f"保存章节文件失败：{str(e)}")
                        self._show_message("保存失败", f"保存章节文件失败：{str(e)}", QMessageBox.Warning)
                else:
                    self._show_message("扩写失败", f"第{i+1}章 {chapter_title} 扩写失败，将使用原始大纲内容。", QMessageBox.Warning)
                    # 使用原始大纲内容作为该章节的内容
                    chapter_file = chapters_dir / f"第{i+1:02d}章_{self._sanitize_filename(chapter_title.split('：')[-1])}.md"
                    try:
                        with open(chapter_file, 'w', encoding='utf-8') as f:
                            f.write(chapter)
                        print(f"已保存原始大纲内容：{chapter_file}")
                        all_expanded_content.append(chapter)
                        self.expanded_chapters.append(chapter)
                    except Exception as e:
                        print(f"保存章节文件失败：{str(e)}")
                        self._show_message("保存失败", f"保存章节文件失败：{str(e)}", QMessageBox.Warning)
                
                # 每章扩写完成后，更新UI显示并保存汇总文件
                final_content = "\n\n".join(all_expanded_content)
                self.ui.expandedEdit.setText(final_content)
                
                # 保存汇总文件
                summary_file = novel_dir / f"{safe_novel_name}-扩写.md"
                try:
                    with open(summary_file, 'w', encoding='utf-8') as f:
                        f.write(final_content)
                    print(f"已更新汇总文件：{summary_file}")
                except Exception as e:
                    print(f"保存汇总文件失败：{str(e)}")
                    self._show_message("保存失败", f"保存汇总文件失败：{str(e)}", QMessageBox.Warning)
            
            # 显示扩写完成的消息
            if all_expanded_content:
                total_expanded_words = sum(len(content.replace('\n', '').replace(' ', '')) for content in all_expanded_content)
                self._show_message("扩写完成", 
                    f"已完成所有章节的扩写，总字数：{total_expanded_words}字\n" +
                    f"目标字数：{total_words}字\n" +
                    f"各章节已分别保存在 {safe_novel_name}/chapters/ 目录下\n" +
                    f"汇总文件已保存为 {safe_novel_name}/{safe_novel_name}-扩写.md")
            else:
                self._show_message("扩写失败", "所有章节扩写均未达到预期，请检查大纲格式或重试。", QMessageBox.Warning)
            
        except Exception as e:
            print(f"扩写过程中发生错误：{str(e)}")
            self._show_message("错误", f"扩写过程中发生错误：{str(e)}", QMessageBox.Critical)
        finally:
            progress.close()

    def _init_ui(self):
        """初始化UI组件"""
        # 设置默认值
        self.ui.chapterCountSlider.setValue(5)
        self.ui.avgChapterWordsSlider.setValue(2000)
        self.ui.mainCharacterCountSlider.setValue(3)
        self.ui.supportCharacterCountSlider.setValue(5)
        
        # 设置输入框提示文本
        self.ui.nameEdit.setPlaceholderText("请输入小说名称，如不输入则由AI自动生成")
        self.ui.synopsisEdit.setPlaceholderText("请输入故事简介，如不输入则由AI自动生成")
        
        # 更新总字数显示
        self._update_total_words()
        
        # 连接滑块值变化信号
        self.ui.chapterCountSlider.valueChanged.connect(self._update_total_words)
        self.ui.avgChapterWordsSlider.valueChanged.connect(self._update_total_words)
        self.ui.mainCharacterCountSlider.valueChanged.connect(self._update_character_count)
        self.ui.supportCharacterCountSlider.valueChanged.connect(self._update_character_count)

        # 初始化小说类型下拉菜单
        self.ui.genreCombo.clear()
        self.ui.genreCombo.addItems([
            "玄幻奇幻",
            "武侠仙侠",
            "都市现实",
            "历史军事",
            "游戏竞技",
            "科幻灵异",
            "言情感情",
            "轻小说",
            "西方奇幻",
            "狼人传说",
            "吸血鬼",
            "龙与地下城",
            "蒸汽朋克",
            "克苏鲁",
            "其他类型"
        ])

        # 初始化写作风格下拉菜单
        self.ui.styleCombo.clear()
        self.ui.styleCombo.addItems([
            "默认风格",
            "金庸 - 武侠风格",
            "古龙 - 武侠风格",
            "莫言 - 现实主义",
            "刘慈欣 - 科幻风格",
            "余华 - 现实主义",
            "南派三叔 - 探险风格",
            "天蚕土豆 - 玄幻风格",
            "猫腻 - 仙侠风格",
            "唐家三少 - 轻小说风格",
            "J.K.罗琳 - 哈利波特风格",
            "乔治·R·R·马丁 - 冰与火之歌风格",
            "托尔金 - 魔戒风格",
            "斯蒂芬·金 - 恐怖风格",
            "安妮·赖斯 - 吸血鬼风格",
            "尼尔·盖曼 - 奇幻风格",
            "菲利普·K·迪克 - 科幻风格"
        ])

        # 设置按钮文本
        self.ui.generateBtn.setText("生成大纲")
        self.ui.expandBtn.setText("扩写内容")
        self.ui.translateBtn.setText("翻译内容")
        self.ui.translateBtn.setEnabled(False)  # 初始状态禁用翻译按钮
        
        # 添加转换为txt按钮到翻译按钮下方
        self.ui.convertToTxtBtn = QPushButton("转换为txt")
        self.ui.convertToTxtBtn.clicked.connect(self.convert_to_txt)
        # 将转换按钮添加到设置布局中，紧跟在翻译按钮后面
        self.ui.settingsLayout.insertWidget(self.ui.settingsLayout.indexOf(self.ui.translateBtn) + 1, self.ui.convertToTxtBtn)
        
        # 创建翻译语言分组
        self.language_group = QGroupBox("翻译语言选项")
        language_layout = QVBoxLayout()
        
        # 创建翻译语言复选框
        self.language_checkboxes = {}
        self.language_tabs = {}
        languages = {
            "english": "英语 (English)",
            "french": "法语 (French)",
            "german": "德语 (German)",
            "russian": "俄语 (Russian)",
            "spanish": "西班牙语 (Spanish)",
            "japanese": "日语 (Japanese)",
            "arabic": "阿拉伯语 (Arabic)",
            "korean": "韩语 (Korean)"
        }
        
        # 创建复选框
        for lang_code, lang_name in languages.items():
            checkbox = QCheckBox(lang_name)
            checkbox.setEnabled(False)  # 初始状态禁用
            # 使用lambda函数时捕获当前值
            checkbox.stateChanged.connect(
                lambda state, code=lang_code, name=lang_name: 
                self._handle_language_toggle(state, code, name)
            )
            self.language_checkboxes[lang_code] = checkbox
            language_layout.addWidget(checkbox)
        
        # 设置语言分组的布局
        self.language_group.setLayout(language_layout)
        self.language_group.setEnabled(False)  # 初始状态禁用整个分组
        
        # 将语言分组添加到设置布局中，紧跟在启用翻译和文化适应复选框后面
        self.ui.settingsLayout.insertWidget(self.ui.settingsLayout.indexOf(self.ui.enableTranslation) + 1, self.language_group)
        
        # 连接启用翻译复选框的信号
        self.ui.enableTranslation.stateChanged.connect(self._handle_translation_enable)
        
        # 更新所有标签
        self._update_total_words()
        self._update_character_count()

    def _handle_language_toggle(self, state, lang_code, lang_name):
        """处理语言复选框状态变化"""
        # 仅处理复选框状态，不再创建标签页
        pass

    def _connect_signals(self):
        """连接信号和槽"""
        try:
            # 确保按钮存在
            if hasattr(self.ui, 'generateBtn'):
                self.ui.generateBtn.clicked.connect(self.generate_outline)
                print("生成大纲按钮连接成功")
            else:
                print("警告：找不到生成大纲按钮")
                
            if hasattr(self.ui, 'expandBtn'):
                self.ui.expandBtn.clicked.connect(self.expand_content)
                print("扩写按钮连接成功")
            else:
                print("警告：找不到扩写按钮")
                
            if hasattr(self.ui, 'translateBtn'):
                self.ui.translateBtn.clicked.connect(self.translate_content)
                print("翻译按钮连接成功")
            else:
                print("警告：找不到翻译按钮")
                
            if hasattr(self.ui, 'convertToTxtBtn'):
                self.ui.convertToTxtBtn.clicked.connect(self.convert_to_txt)
                print("转换按钮连接成功")
            else:
                print("警告：找不到转换按钮")
                
            # 连接文化适应复选框
            if hasattr(self.ui, 'cultureCheckBox'):
                self.ui.cultureCheckBox.stateChanged.connect(self._handle_culture_toggle)
                print("文化适应复选框连接成功")
            else:
                print("警告：找不到文化适应复选框")
                
        except Exception as e:
            print(f"信号连接失败：{str(e)}")
            # 打印更详细的错误信息
            import traceback
            print(traceback.format_exc())

    def _update_total_words(self):
        """更新总字数显示"""
        chapter_count = self.ui.chapterCountSlider.value()
        avg_words = self.ui.avgChapterWordsSlider.value()
        total_words = chapter_count * avg_words
        
        self.ui.chapterCountLabel.setText(f"章节数量：{chapter_count}章")
        self.ui.avgChapterWordsLabel.setText(f"每章平均字数：{avg_words}字")
        self.ui.totalWordsLabel.setText(f"总字数：{total_words}字")

    def _update_character_count(self):
        """更新人物数量显示"""
        main_count = self.ui.mainCharacterCountSlider.value()
        support_count = self.ui.supportCharacterCountSlider.value()
        
        self.ui.mainCharacterCountLabel.setText(f"主要人物数量：{main_count}人")
        self.ui.supportCharacterCountLabel.setText(f"次要人物数量：{support_count}人")

    def _check_api_key(self):
        """检查API密钥是否配置"""
        if not openai.api_key:
            self._show_message("配置缺失", "请在.env文件中配置OPENAI_API_KEY", QMessageBox.Warning)
            print("API密钥未配置")
            return False
        print(f"API密钥已配置：{openai.api_key[:8]}...")
        return True

    def _call_api(self, prompt, model="gpt-4o-mini"):
        """调用API生成内容"""
        try:
            print(f"正在调用API，模型：{model}")
            print(f"API基础URL：{openai.api_base}")
            print("发送的提示：")
            print("=" * 50)
            print(prompt)
            print("=" * 50)
            
            # 设置请求头
            headers = {
                "Authorization": f"Bearer {openai.api_key}",
                "Content-Type": "application/json"
            }
            
            # 构建请求数据
            data = {
                "model": model,
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.7,
                "max_tokens": 4000,
                "top_p": 1,
                "frequency_penalty": 0,
                "presence_penalty": 0
            }
            
            print("正在发送请求...")
            # 直接使用requests发送请求
            response = requests.post(
                f"{openai.api_base}/chat/completions",
                headers=headers,
                json=data,
                timeout=60  # 设置60秒超时
            )
            
            print(f"API响应状态码：{response.status_code}")
            print(f"API响应内容：{response.text}")
            
            if response.status_code == 200:
                result = response.json()
                if "choices" in result and len(result["choices"]) > 0:
                    content = result["choices"][0]["message"]["content"].strip()
                    print("API响应成功，响应长度：", len(content))
                    return content
                else:
                    print("API响应格式错误：", result)
                    self._show_message("API响应错误", "响应格式不正确", QMessageBox.Critical)
                    return None
            else:
                error_msg = f"API响应错误：{response.status_code}"
                if response.text:
                    try:
                        error_data = response.json()
                        if "error" in error_data:
                            error_msg += f"\n{error_data['error'].get('message', '')}"
                    except:
                        error_msg += f"\n{response.text}"
                print(error_msg)
                self._show_message("API响应错误", error_msg, QMessageBox.Critical)
                return None
            
        except requests.exceptions.Timeout:
            error_msg = "API请求超时，请重试"
            print(error_msg)
            self._show_message("API调用失败", error_msg, QMessageBox.Critical)
            return None
        except requests.exceptions.RequestException as e:
            error_msg = f"API请求异常：{str(e)}"
            print(error_msg)
            self._show_message("API调用失败", error_msg, QMessageBox.Critical)
            return None
        except Exception as e:
            error_msg = f"API调用失败：{str(e)}"
            print(error_msg)
            import traceback
            print(traceback.format_exc())
            self._show_message("API调用失败", error_msg, QMessageBox.Critical)
            return None

    def _clean_response(self, response):
        """清理API响应内容"""
        # 移除可能的Markdown标记
        cleaned = re.sub(r'```.*?```', '', response, flags=re.DOTALL)
        # 移除多余的空行
        cleaned = re.sub(r'\n{3,}', '\n\n', cleaned)
        # 移除字数统计等额外信息
        cleaned = re.sub(r'字数[：:]\s*\d+.*$', '', cleaned, flags=re.MULTILINE)
        cleaned = re.sub(r'总字数[：:]\s*\d+.*$', '', cleaned, flags=re.MULTILINE)
        cleaned = re.sub(r'优化总结.*$', '', cleaned, flags=re.DOTALL)
        return cleaned.strip()

    def _sanitize_filename(self, filename):
        """清理文件名，移除非法字符"""
        # 移除文件名中的非法字符
        filename = re.sub(r'[<>:"/\\|?*]', '_', filename)
        # 移除前后的空白字符和点
        filename = filename.strip('. ')
        # 如果文件名为空，使用默认名称
        return filename if filename else 'untitled'

    def _split_into_chapters(self, text):
        """将大纲文本分割为章节列表"""
        # 移除可能的文件标题
        text = re.sub(r'^.*?\.md\s*\n', '', text, flags=re.MULTILINE)
        
        # 按章节分割
        chapters = []
        current_chapter = []
        
        for line in text.split('\n'):
            # 使用H3格式的标题
            if re.match(r'^第.+章[:：]', line.strip()):
                if current_chapter:
                    chapters.append('\n'.join(current_chapter))
                # 将标题转换为H3格式
                title = line.strip()
                current_chapter = [f"### {title}"]
            elif line.strip() and current_chapter:
                current_chapter.append(line.strip())
        
        if current_chapter:
            chapters.append('\n'.join(current_chapter))
        
        return chapters

    def _save_current_content(self, content_type):
        """保存当前内容到文件"""
        if not self.current_novel_name:
            return
            
        safe_novel_name = self._sanitize_filename(self.current_novel_name)
        folder_path = Path(safe_novel_name)
        folder_path.mkdir(exist_ok=True)
        
        if content_type == "大纲":
            filename = f"{safe_novel_name}-大纲.md"
            content = self.ui.outlineEdit.toPlainText()
        elif content_type == "扩写":
            filename = f"{safe_novel_name}-扩写.md"
            content = self.ui.expandedEdit.toPlainText()
        else:  # 翻译
            filename = f"{safe_novel_name}-翻译.md"
            content = self.translatedEdit.toPlainText()
        
        try:
            with open(folder_path / filename, 'w', encoding='utf-8') as f:
                f.write(content)
        except Exception as e:
            self._show_message("保存失败", f"保存文件失败：{str(e)}", QMessageBox.Warning)

    def generate_outline(self):
        """生成小说大纲"""
        print("开始生成大纲")
        if not self._check_api_key():
            return
            
        try:
            # 获取用户输入
            novel_name = self.ui.nameEdit.text().strip()
            synopsis = self.ui.synopsisEdit.toPlainText().strip()
            
            # 如果没有输入小说名称，则自动生成
            if not novel_name:
                print("正在自动生成小说名称...")
                genre = self.ui.genreCombo.currentText()
                style = self.ui.styleCombo.currentText()
                prompt = f"""请为一部{genre}类型的小说生成一个富有创意的名字，要求：
1. 名字要有吸引力和记忆点
2. 符合{genre}的特点
3. 如果写作风格不是默认风格，要符合{style}的风格特点
4. 不要解释，直接给出名字即可"""
                
                response = self._call_api(prompt)
                if not response:
                    self._show_message("生成失败", "无法自动生成小说名称，请手动输入", QMessageBox.Warning)
                    return
                    
                novel_name = self._clean_response(response)
                self.ui.nameEdit.setText(novel_name)
                print(f"自动生成的小说名称：{novel_name}")
                
            # 如果没有输入故事简介，则自动生成
            if not synopsis:
                print("正在自动生成故事简介...")
                genre = self.ui.genreCombo.currentText()
                style = self.ui.styleCombo.currentText()
                cultural_background = self.ui.cultureCombo.currentText()
                main_chars = self.ui.mainCharacterCountSlider.value()
                support_chars = self.ui.supportCharacterCountSlider.value()
                
                prompt = f"""请为小说《{novel_name}》生成一个引人入胜的故事简介，要求：
1. 符合{genre}类型的特点
2. 融入{cultural_background}的元素
3. 包含{main_chars}个主要人物和{support_chars}个次要人物
4. 如果写作风格不是默认风格，要符合{style}的风格特点
5. 简介长度在200-300字之间
6. 不要解释，直接给出简介内容即可"""
                
                response = self._call_api(prompt)
                if not response:
                    self._show_message("生成失败", "无法自动生成故事简介，请手动输入", QMessageBox.Warning)
                    return
                    
                synopsis = self._clean_response(response)
                self.ui.synopsisEdit.setText(synopsis)
                print(f"自动生成的故事简介：{synopsis}")
                
            self.current_novel_name = novel_name
            print(f"小说名称：{novel_name}")
            print(f"故事简介：{synopsis}")
                
            # 获取其他参数
            genre = self.ui.genreCombo.currentText()
            chapter_count = self.ui.chapterCountSlider.value()
            avg_words = self.ui.avgChapterWordsSlider.value()
            total_words = chapter_count * avg_words
            style = self.ui.styleCombo.currentText()
            secondary_chars = self.ui.supportCharacterCountSlider.value()
            cultural_background = self.ui.cultureCombo.currentText()
            
            print(f"类型：{genre}")
            print(f"章节数：{chapter_count}")
            print(f"每章字数：{avg_words}")
            print(f"写作风格：{style}")
            print(f"文化背景：{cultural_background}")
            
            # 构建提示
            prompt = f"""作为一个专业的小说策划专家，请为以下小说生成详细的章节大纲：

小说名称：《{novel_name}》
简介：{synopsis}
文化背景：{cultural_background}
类型：{genre}
章节数量：{chapter_count}章
每章字数：{avg_words}字
总字数：{total_words}字
次要人物数量：{secondary_chars}人
写作风格：{style}

要求：
1. 每章标题格式为"第X章：章节标题"
2. 每章内容包含该章节的主要情节概要
3. 确保故事情节连贯，符合逻辑
4. 根据总字数合理分配每章内容
5. 适当设置故事高潮和转折点
6. 不要包含文件标题或额外的格式说明
7. 确保章节数量严格等于{chapter_count}章
8. 合理安排次要人物的出场和发展

请直接给出大纲内容，无需其他说明。"""

            print("开始调用API生成大纲")

            # 创建进度对话框
            progress = QProgressDialog("正在生成大纲...", "取消", 0, 100, self)
            progress.setWindowModality(Qt.WindowModal)
            progress.setWindowTitle("生成进度")
            progress.show()

            try:
                # 调用API生成大纲
                response = self._call_api(prompt)
                if not response:
                    self._show_message("生成失败", "无法生成大纲，请重试", QMessageBox.Warning)
                    return
                    
                print("API调用成功，开始处理响应")
                # 清理响应内容
                cleaned_response = self._clean_response(response)
                
                # 检查章节数量
                chapters = self._split_into_chapters(cleaned_response)
                if not chapters:
                    self._show_message("生成失败", "无法从生成的内容中识别出章节，请重试", QMessageBox.Warning)
                    return
                
                print(f"识别出{len(chapters)}个章节")
                
                # 更新UI显示
                self.ui.outlineEdit.setText(cleaned_response)
                
                # 保存大纲文件
                self._save_current_content("大纲")
                
                # 显示成功消息
                self._show_message("生成成功", f"已生成{len(chapters)}章大纲")
                
            except Exception as e:
                print(f"生成大纲时发生错误：{str(e)}")
                import traceback
                print(traceback.format_exc())
                self._show_message("错误", f"生成大纲时发生错误：{str(e)}", QMessageBox.Critical)
            finally:
                progress.close()
                
        except Exception as e:
            print(f"生成大纲过程中发生错误：{str(e)}")
            import traceback
            print(traceback.format_exc())
            self._show_message("错误", f"生成大纲过程中发生错误：{str(e)}", QMessageBox.Critical)

    def translate_content(self):
        """翻译小说内容"""
        if not self._check_api_key():
            return
            
        # 获取要翻译的内容
        content = self.ui.expandedEdit.toPlainText().strip()
        if not content:
            self._show_message("输入错误", "请先扩写小说内容", QMessageBox.Warning)
            return
            
        # 获取选中的语言
        selected_languages = {}
        for lang_code, checkbox in self.language_checkboxes.items():
            if checkbox.isChecked():
                if lang_code == "english":
                    selected_languages[lang_code] = "英语"
                elif lang_code == "french":
                    selected_languages[lang_code] = "法语"
                elif lang_code == "german":
                    selected_languages[lang_code] = "德语"
                elif lang_code == "russian":
                    selected_languages[lang_code] = "俄语"
                elif lang_code == "spanish":
                    selected_languages[lang_code] = "西班牙语"
                elif lang_code == "japanese":
                    selected_languages[lang_code] = "日语"
                elif lang_code == "arabic":
                    selected_languages[lang_code] = "阿拉伯语"
                elif lang_code == "korean":
                    selected_languages[lang_code] = "韩语"
        
        if not selected_languages:
            self._show_message("输入错误", "请选择至少一种目标语言", QMessageBox.Warning)
            return
            
        # 获取大纲和故事梗概内容
        outline_content = self.ui.outlineEdit.toPlainText().strip()
        synopsis_content = self.ui.synopsisEdit.toPlainText().strip()
            
        # 创建进度对话框
        progress = QProgressDialog("正在翻译内容...", "取消", 0, 100, self)
        progress.setWindowModality(Qt.WindowModal)
        progress.setWindowTitle("翻译进度")
        progress.show()
        
        try:
            # 分析内容，获取章节列表
            chapters = []
            current_chapter = []
            lines = content.split('\n')
            
            for line in lines:
                if line.strip().startswith('### 第') and '章' in line:
                    if current_chapter:
                        chapters.append('\n'.join(current_chapter))
                    current_chapter = [line.strip()]
                elif line.strip():
                    current_chapter.append(line.strip())
            
            if current_chapter:
                chapters.append('\n'.join(current_chapter))
            
            if not chapters:
                self._show_message("章节识别失败", "无法从内容中识别出章节，请检查格式", QMessageBox.Warning)
                return
                
            total_chapters = len(chapters)
            total_tasks = total_chapters * len(selected_languages)
            completed_tasks = 0
            
            # 为每种语言创建存储翻译内容的列表
            translated_contents = {lang_code: [] for lang_code in selected_languages}
            
            # 翻译大纲和故事梗概
            for lang_code, lang_name in selected_languages.items():
                # 翻译大纲
                if outline_content:
                    outline_prompt = f"""请将以下中文小说大纲翻译成{lang_name}，保持原文的格式和结构：

{outline_content}

要求：
1. 保持章节标题格式
2. 保持段落结构
3. 确保翻译准确流畅
4. 不要添加额外的解释或说明"""

                    outline_response = self._call_api(outline_prompt)
                    if outline_response:
                        outline_translated = self._clean_response(outline_response)
                        # 保存翻译后的大纲
                        safe_novel_name = self._sanitize_filename(self.current_novel_name)
                        outline_file = Path(safe_novel_name) / f"{safe_novel_name}-大纲-{lang_name}.md"
                        with open(outline_file, 'w', encoding='utf-8') as f:
                            f.write(outline_translated)
                
                # 翻译故事梗概
                if synopsis_content:
                    synopsis_prompt = f"""请将以下中文小说梗概翻译成{lang_name}，保持原文的文学性：

{synopsis_content}

要求：
1. 保持段落结构
2. 确保翻译准确流畅
3. 不要添加额外的解释或说明"""

                    synopsis_response = self._call_api(synopsis_prompt)
                    if synopsis_response:
                        synopsis_translated = self._clean_response(synopsis_response)
                        # 保存翻译后的故事梗概
                        safe_novel_name = self._sanitize_filename(self.current_novel_name)
                        synopsis_file = Path(safe_novel_name) / f"{safe_novel_name}-故事梗概-{lang_name}.md"
                        with open(synopsis_file, 'w', encoding='utf-8') as f:
                            f.write(synopsis_translated)
            
            # 逐章翻译
            for i, chapter in enumerate(chapters):
                if progress.wasCanceled():
                    break
                    
                # 对每种选中的语言进行翻译
                for lang_code, lang_name in selected_languages.items():
                    if progress.wasCanceled():
                        break
                        
                    # 更新进度
                    progress.setValue(int((completed_tasks / total_tasks) * 100))
                    progress.setLabelText(f"正在翻译第{i+1}章 ({lang_name})...")
                    
                    # 构建翻译提示
                    prompt = f"""请将以下中文小说内容翻译成{lang_name}，保持原文的文学性和表达方式：

{chapter}

要求：
1. 保持章节标题格式（### 第X章）
2. 保持段落结构
3. 确保翻译准确流畅
4. 保持文学性和表达方式
5. 不要添加额外的解释或说明"""

                    # 调用API进行翻译
                    response = self._call_api(prompt)
                    if response:
                        # 清理响应内容
                        cleaned_response = self._clean_response(response)
                        translated_contents[lang_code].append(cleaned_response)
                        
                        # 保存翻译后的章节
                        chapter_title = chapter.split('\n')[0].replace('### ', '')
                        self._save_chapter_content(
                            cleaned_response,
                            i,
                            chapter_title,
                            "翻译",
                            lang_name
                        )
                    else:
                        self._show_message("翻译失败", f"第{i+1}章 {lang_name}翻译失败", QMessageBox.Warning)
                        translated_contents[lang_code].append(chapter)  # 使用原文
                    
                    completed_tasks += 1
            
            # 为每种语言生成合并后的翻译文件
            for lang_code, contents in translated_contents.items():
                if len(contents) == total_chapters:
                    lang_name = selected_languages[lang_code]
                    merged_content = "\n\n".join(contents)
                    safe_novel_name = self._sanitize_filename(self.current_novel_name)
                    merged_file = Path(safe_novel_name) / f"{safe_novel_name}-扩写-{lang_name}.md"
                    with open(merged_file, 'w', encoding='utf-8') as f:
                        f.write(merged_content)
            
            # 显示翻译完成的消息
            success_languages = [
                selected_languages[lang_code]
                for lang_code, contents in translated_contents.items()
                if len(contents) == total_chapters
            ]
            
            if success_languages:
                message = "翻译完成：\n"
                for lang_name in success_languages:
                    message += f"- {lang_name}\n"
                message += f"\n翻译结果已保存在 {self._sanitize_filename(self.current_novel_name)}/ 目录下"
                self._show_message("翻译完成", message)
            else:
                self._show_message("翻译失败", "所有语言的翻译均未完全成功，请重试", QMessageBox.Warning)
            
        except Exception as e:
            print(f"翻译过程中发生错误：{str(e)}")
            import traceback
            print(traceback.format_exc())
            self._show_message("错误", f"翻译内容时发生错误：{str(e)}", QMessageBox.Critical)
        finally:
            progress.close()

    def convert_to_txt(self):
        """将所有md文件转换为txt格式"""
        if not self.current_novel_name:
            self._show_message("错误", "请先生成或加载小说内容", QMessageBox.Warning)
            return
            
        safe_novel_name = self._sanitize_filename(self.current_novel_name)
        novel_dir = Path(safe_novel_name)
        
        if not novel_dir.exists():
            self._show_message("错误", "找不到小说文件夹", QMessageBox.Warning)
            return
            
        try:
            # 转换所有md文件为txt
            for md_file in novel_dir.glob("*.md"):
                txt_file = md_file.with_suffix('.txt')
                with open(md_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                with open(txt_file, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"已转换文件：{txt_file}")
                
            # 转换chapters目录下的所有文件
            chapters_dir = novel_dir / "chapters"
            if chapters_dir.exists():
                chapters_txt_dir = novel_dir / "chapters_txt"
                chapters_txt_dir.mkdir(exist_ok=True)
                
                # 转换原始章节和翻译章节
                for md_file in chapters_dir.rglob("*.md"):
                    relative_path = md_file.relative_to(chapters_dir)
                    txt_file = chapters_txt_dir / relative_path.with_suffix('.txt')
                    txt_file.parent.mkdir(parents=True, exist_ok=True)
                    with open(md_file, 'r', encoding='utf-8') as f:
                        content = f.read()
                    with open(txt_file, 'w', encoding='utf-8') as f:
                        f.write(content)
                    print(f"已转换章节文件：{txt_file}")
                    
            self._show_message("转换完成", 
                f"已将所有md文件转换为txt格式\n" +
                f"文件保存在：{novel_dir}")
                
        except Exception as e:
            print(f"转换文件时发生错误：{str(e)}")
            self._show_message("错误", f"转换文件时发生错误：{str(e)}", QMessageBox.Critical)

    def _handle_culture_toggle(self, state):
        """处理文化适应复选框状态变化"""
        is_enabled = bool(state)
        self.language_group.setEnabled(is_enabled)
        
        # 如果禁用，取消所有语言的选中状态并移除标签页
        if not is_enabled:
            for checkbox in self.language_checkboxes.values():
                checkbox.setChecked(False)
            # 移除所有翻译标签页
            for tab in self.language_tabs.values():
                index = self.ui.tabWidget.indexOf(tab)
                if index != -1:
                    self.ui.tabWidget.removeTab(index)
            self.language_tabs.clear()

    def _handle_translation_enable(self, state):
        """处理启用翻译复选框的状态变化"""
        is_enabled = bool(state)
        
        # 启用/禁用翻译按钮
        self.ui.translateBtn.setEnabled(is_enabled)
        
        # 启用/禁用语言分组
        self.language_group.setEnabled(is_enabled)
        
        # 启用所有语言复选框
        for checkbox in self.language_checkboxes.values():
            checkbox.setEnabled(is_enabled)
        
        if is_enabled:
            # 默认选中英语
            if "english" in self.language_checkboxes:
                self.language_checkboxes["english"].setChecked(True)
        else:
            # 取消所有选中状态
            for checkbox in self.language_checkboxes.values():
                checkbox.setChecked(False)
            # 移除所有翻译标签页
            for tab in self.language_tabs.values():
                index = self.ui.tabWidget.indexOf(tab)
                if index != -1:
                    self.ui.tabWidget.removeTab(index)
            self.language_tabs.clear()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = NovelGenerator()
    window.show()
    sys.exit(app.exec()) 