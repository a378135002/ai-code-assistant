# 🛠️ Python 自动化工具集

这里提供实用的 Python 自动化工具，开箱即用！

---

## 📊 Excel 批量处理工具

**功能：**
- ✅ 批量合并多个 Excel 文件
- ✅ 批量转换格式（Excel ↔ CSV）
- ✅ 数据清洗（去重、删除空行）
- ✅ 添加水印标记

**安装：**
```bash
pip install pandas openpyxl xlrd
```

**使用示例：**

```bash
# 合并 Excel 文件
python excel_batch_processor.py ./input_files -m

# 转换为 CSV
python excel_batch_processor.py ./input_files -c csv

# 清洗数据
python excel_batch_processor.py ./input_files -l

# 添加水印
python excel_batch_processor.py ./input_files -w "已处理"
```

**详细文档：** [查看代码](excel_batch_processor.py)

---

## 📁 文件批量重命名工具

**功能：**
- ✅ 批量添加前缀/后缀
- ✅ 正则表达式替换
- ✅ 自动添加序列号
- ✅ 添加时间戳
- ✅ 添加文件日期前缀
- ✅ 移除特殊字符

**使用示例：**

```bash
# 预览重命名（添加前缀和序列号）
python file_renamer.py ./photos --prefix "vacation_" -n 1

# 执行重命名
python file_renamer.py ./photos --prefix "vacation_" -n 1 -e

# 正则替换
python file_renamer.py ./docs -p "旧文字" -r "新文字" -e

# 添加文件日期前缀
python file_renamer.py ./photos --date-prefix

# 移除特殊字符
python file_renamer.py ./files --clean
```

**详细文档：** [查看代码](file_renamer.py)

---

## 📸 网页批量截图工具

**功能：**
- ✅ 批量网页截图
- ✅ 全页滚动截图
- ✅ 多设备尺寸截图（桌面/平板/手机）
- ✅ 自定义分辨率
- ✅ 自动等待页面加载

**安装：**
```bash
pip install playwright
playwright install  # 安装浏览器
```

**使用示例：**

```bash
# 单个网页截图
python webpage_screenshoter.py https://example.com

# 批量截图
python webpage_screenshoter.py https://site1.com https://site2.com -o ./screenshots

# 全页截图（滚动）
python webpage_screenshoter.py https://blog.com -f

# 多设备截图
python webpage_screenshoter.py https://example.com --devices

# 自定义尺寸
python webpage_screenshoter.py https://example.com -w 1366 -ht 768
```

**详细文档：** [查看代码](webpage_screenshoter.py)

---

## 💡 定制需求

这些工具不能满足你的需求？我可以帮你定制！

**提交需求：**
1. 访问 [GitHub Issues](https://github.com/a378135002/ai-code-assistant/issues/new/choose)
2. 选择「💻 代码需求」模板
3. 填写你的需求
4. 我会评估报价并开发

**常见定制：**
- 特定格式的 Excel 处理
- 特殊规则的文件重命名
- 特定网站的截图需求
- 其他 Python 自动化脚本

---

## 📦 获取方式

**方式一：GitHub 下载**
```bash
git clone https://github.com/a378135002/ai-code-assistant.git
cd ai-code-assistant/tools
pip install -r requirements.txt
```

**方式二：面包多购买**（即将上线）
- 单个工具：¥29
- 工具包（全部）：¥99
- 包含使用说明和技术支持

---

## ⭐ 使用提示

1. **先备份** - 批量操作前建议备份原文件
2. **先预览** - 重命名工具默认仅预览，确认无误再加 `-e` 执行
3. **测试运行** - 大规模处理前先小批量测试
4. **查看帮助** - 每个工具都支持 `-h` 查看帮助

```bash
python excel_batch_processor.py -h
python file_renamer.py -h
python webpage_screenshoter.py -h
```

---

**🔥 更多工具开发中... 欢迎提需求！**
