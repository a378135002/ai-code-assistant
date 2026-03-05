#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Excel 批量处理工具
功能：批量合并、转换、清洗 Excel 文件

作者：AI Code Assistant
GitHub: https://github.com/a378135002/ai-code-assistant
"""

import os
import sys
import pandas as pd
from pathlib import Path
from datetime import datetime

class ExcelBatchProcessor:
    """Excel 批量处理器"""
    
    def __init__(self, input_dir: str, output_dir: str = None):
        """
        初始化处理器
        
        Args:
            input_dir: 输入目录路径
            output_dir: 输出目录路径（可选，默认为 input_dir/output）
        """
        self.input_dir = Path(input_dir)
        self.output_dir = Path(output_dir) if output_dir else self.input_dir / "output"
        self.output_dir.mkdir(exist_ok=True)
        
    def merge_excel_files(self, output_filename: str = "merged.xlsx", sheet_name: str = "合并数据"):
        """
        合并多个 Excel 文件为一个
        
        Args:
            output_filename: 输出文件名
            sheet_name: 工作表名称
        """
        print(f"🔍 正在搜索 Excel 文件：{self.input_dir}")
        
        excel_files = list(self.input_dir.glob("*.xlsx")) + list(self.input_dir.glob("*.xls"))
        # 排除输出目录的文件
        excel_files = [f for f in excel_files if "output" not in str(f)]
        
        if not excel_files:
            print("❌ 未找到 Excel 文件")
            return
        
        print(f"✅ 找到 {len(excel_files)} 个 Excel 文件")
        
        all_data = []
        for file in excel_files:
            try:
                print(f"📊 读取：{file.name}")
                df = pd.read_excel(file)
                df['源文件'] = file.name
                all_data.append(df)
            except Exception as e:
                print(f"⚠️ 读取失败 {file.name}: {e}")
        
        if all_data:
            merged_df = pd.concat(all_data, ignore_index=True)
            output_path = self.output_dir / output_filename
            
            merged_df.to_excel(output_path, sheet_name=sheet_name, index=False)
            print(f"✅ 合并完成！输出：{output_path}")
            print(f"📈 总行数：{len(merged_df)}")
        else:
            print("❌ 没有成功读取任何文件")
    
    def convert_format(self, target_format: str = "csv"):
        """
        批量转换 Excel 文件格式
        
        Args:
            target_format: 目标格式 (csv, xlsx)
        """
        print(f"🔄 正在转换格式：{target_format}")
        
        if target_format == "csv":
            excel_files = list(self.input_dir.glob("*.xlsx")) + list(self.input_dir.glob("*.xls"))
            excel_files = [f for f in excel_files if "output" not in str(f)]
            
            for file in excel_files:
                try:
                    print(f"📄 转换：{file.name}")
                    df = pd.read_excel(file)
                    output_path = self.output_dir / f"{file.stem}.csv"
                    df.to_csv(output_path, index=False, encoding='utf-8-sig')
                    print(f"✅ 已保存：{output_path.name}")
                except Exception as e:
                    print(f"⚠️ 转换失败 {file.name}: {e}")
        
        elif target_format == "xlsx":
            csv_files = list(self.input_dir.glob("*.csv"))
            
            for file in csv_files:
                try:
                    print(f"📄 转换：{file.name}")
                    df = pd.read_csv(file, encoding='utf-8-sig')
                    output_path = self.output_dir / f"{file.stem}.xlsx"
                    df.to_excel(output_path, index=False)
                    print(f"✅ 已保存：{output_path.name}")
                except Exception as e:
                    print(f"⚠️ 转换失败 {file.name}: {e}")
        
        print("🎉 批量转换完成！")
    
    def clean_data(self, output_filename: str = "cleaned.xlsx"):
        """
        清洗 Excel 数据（去重、删除空行等）
        
        Args:
            output_filename: 输出文件名
        """
        print("🧹 正在清洗数据...")
        
        excel_files = list(self.input_dir.glob("*.xlsx")) + list(self.input_dir.glob("*.xls"))
        excel_files = [f for f in excel_files if "output" not in str(f)]
        
        if not excel_files:
            print("❌ 未找到 Excel 文件")
            return
        
        for file in excel_files:
            try:
                print(f"📊 清洗：{file.name}")
                df = pd.read_excel(file)
                
                original_rows = len(df)
                
                # 删除全空行
                df = df.dropna(how='all')
                
                # 删除完全重复的行
                df = df.drop_duplicates()
                
                cleaned_rows = len(df)
                removed_rows = original_rows - cleaned_rows
                
                output_path = self.output_dir / f"cleaned_{file.name}"
                df.to_excel(output_path, index=False)
                
                print(f"✅ 清洗完成：{output_path.name}")
                print(f"   原始行数：{original_rows}, 清洗后：{cleaned_rows}, 删除：{removed_rows}")
                
            except Exception as e:
                print(f"⚠️ 清洗失败 {file.name}: {e}")
        
        print("🎉 批量清洗完成！")
    
    def add_watermark(self, text: str = "AI 处理", output_suffix: str = "_watermarked"):
        """
        批量添加水印（在 sheet 名中添加）
        
        Args:
            text: 水印文本
            output_suffix: 输出文件后缀
        """
        print(f"💧 添加水印：{text}")
        
        excel_files = list(self.input_dir.glob("*.xlsx")) + list(self.input_dir.glob("*.xls"))
        excel_files = [f for f in excel_files if "output" not in str(f)]
        
        for file in excel_files:
            try:
                print(f"📄 处理：{file.name}")
                
                with pd.ExcelWriter(file, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
                    # 读取所有 sheet
                    xl = pd.ExcelFile(file)
                    for sheet_name in xl.sheet_names:
                        df = pd.read_excel(file, sheet_name=sheet_name)
                        # 添加水印列
                        df['处理标记'] = f"{text} {datetime.now().strftime('%Y-%m-%d')}"
                        df.to_excel(writer, sheet_name=sheet_name, index=False)
                
                print(f"✅ 已添加水印")
                
            except Exception as e:
                print(f"⚠️ 处理失败 {file.name}: {e}")
        
        print("🎉 批量添加水印完成！")


def main():
    """主函数 - 命令行界面"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Excel 批量处理工具")
    parser.add_argument("input_dir", help="输入目录路径")
    parser.add_argument("-o", "--output", help="输出目录路径（可选）")
    parser.add_argument("-m", "--merge", action="store_true", help="合并 Excel 文件")
    parser.add_argument("-c", "--convert", choices=["csv", "xlsx"], help="转换格式")
    parser.add_argument("-l", "--clean", action="store_true", help="清洗数据")
    parser.add_argument("-w", "--watermark", type=str, help="添加水印文本")
    
    args = parser.parse_args()
    
    processor = ExcelBatchProcessor(args.input_dir, args.output)
    
    if args.merge:
        processor.merge_excel_files()
    elif args.convert:
        processor.convert_format(args.convert)
    elif args.clean:
        processor.clean_data()
    elif args.watermark:
        processor.add_watermark(args.watermark)
    else:
        print("📖 使用方法:")
        print("  python excel_batch_processor.py <输入目录> -m          # 合并文件")
        print("  python excel_batch_processor.py <输入目录> -c csv     # 转换为 CSV")
        print("  python excel_batch_processor.py <输入目录> -l         # 清洗数据")
        print("  python excel_batch_processor.py <输入目录> -w '水印'  # 添加水印")


if __name__ == "__main__":
    main()
