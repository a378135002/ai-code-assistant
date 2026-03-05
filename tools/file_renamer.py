#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
文件批量重命名工具
功能：批量重命名文件，支持正则表达式、序列号、时间戳等

作者：AI Code Assistant
GitHub: https://github.com/a378135002/ai-code-assistant
"""

import os
import re
import shutil
from pathlib import Path
from datetime import datetime
from typing import List, Tuple


class FileRenamer:
    """文件批量重命名器"""
    
    def __init__(self, directory: str, file_types: List[str] = None):
        """
        初始化重命名器
        
        Args:
            directory: 目标目录路径
            file_types: 文件类型列表，如 ['.jpg', '.png']（可选，默认处理所有文件）
        """
        self.directory = Path(directory)
        self.file_types = file_types
        
    def get_files(self) -> List[Path]:
        """获取目录中的所有文件"""
        if self.file_types:
            files = []
            for ext in self.file_types:
                files.extend(self.directory.glob(f"*{ext}"))
            return sorted(files)
        else:
            return [f for f in self.directory.iterdir() if f.is_file()]
    
    def preview_rename(self, pattern: str = None, replacement: str = None, 
                       prefix: str = None, suffix: str = None,
                       start_number: int = 1, use_timestamp: bool = False) -> List[Tuple[str, str]]:
        """
        预览重命名结果
        
        Args:
            pattern: 正则表达式模式（可选）
            replacement: 替换文本（可选）
            prefix: 文件名前缀（可选）
            suffix: 文件名后缀（可选）
            start_number: 起始编号（可选）
            use_timestamp: 是否使用时间戳（可选）
            
        Returns:
            [(原文件名，新文件名), ...]
        """
        files = self.get_files()
        rename_list = []
        
        for i, file in enumerate(files, start=start_number):
            old_name = file.name
            name_without_ext = file.stem
            ext = file.suffix
            
            new_name = name_without_ext
            
            # 正则替换
            if pattern and replacement:
                new_name = re.sub(pattern, replacement, new_name)
            
            # 添加前缀
            if prefix:
                new_name = f"{prefix}{new_name}"
            
            # 添加后缀
            if suffix:
                new_name = f"{new_name}{suffix}"
            
            # 添加序列号
            if start_number:
                new_name = f"{i:03d}_{new_name}"
            
            # 使用时间戳
            if use_timestamp:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                new_name = f"{timestamp}_{new_name}"
            
            new_name_with_ext = f"{new_name}{ext}"
            
            # 避免文件名相同
            if new_name_with_ext != old_name:
                rename_list.append((old_name, new_name_with_ext))
        
        return rename_list
    
    def rename(self, pattern: str = None, replacement: str = None,
               prefix: str = None, suffix: str = None,
               start_number: int = 1, use_timestamp: bool = False,
               dry_run: bool = True) -> int:
        """
        批量重命名文件
        
        Args:
            pattern: 正则表达式模式
            replacement: 替换文本
            prefix: 文件名前缀
            suffix: 文件名后缀
            start_number: 起始编号
            use_timestamp: 是否使用时间戳
            dry_run: 是否仅预览（不实际重命名）
            
        Returns:
            重命名的文件数量
        """
        rename_list = self.preview_rename(pattern, replacement, prefix, suffix, start_number, use_timestamp)
        
        if not rename_list:
            print("ℹ️ 没有需要重命名的文件")
            return 0
        
        if dry_run:
            print("📋 预览重命名结果：")
            print("-" * 60)
            for old_name, new_name in rename_list:
                print(f"  {old_name}")
                print(f"    → {new_name}")
            print("-" * 60)
            print(f"共 {len(rename_list)} 个文件")
            print("\n💡 确认无误后，使用 --execute 参数执行重命名")
            return len(rename_list)
        
        # 实际执行重命名
        print("🔄 开始重命名...")
        success_count = 0
        
        for old_name, new_name in rename_list:
            old_path = self.directory / old_name
            new_path = self.directory / new_name
            
            try:
                # 检查新文件名是否已存在
                if new_path.exists():
                    print(f"⚠️ 跳过：{new_name} 已存在")
                    continue
                
                shutil.move(str(old_path), str(new_path))
                print(f"✅ {old_name} → {new_name}")
                success_count += 1
                
            except Exception as e:
                print(f"❌ 重命名失败 {old_name}: {e}")
        
        print(f"\n🎉 重命名完成！成功：{success_count}/{len(rename_list)}")
        return success_count
    
    def add_date_prefix(self, date_format: str = "%Y%m%d") -> int:
        """
        添加文件修改日期作为前缀
        
        Args:
            date_format: 日期格式
            
        Returns:
            重命名的文件数量
        """
        files = self.get_files()
        success_count = 0
        
        print(f"📅 添加日期前缀：{date_format}")
        print("-" * 60)
        
        for file in files:
            try:
                # 获取文件修改时间
                mtime = datetime.fromtimestamp(file.stat().st_mtime)
                date_str = mtime.strftime(date_format)
                
                old_name = file.name
                name_without_ext = file.stem
                ext = file.suffix
                
                new_name = f"{date_str}_{name_without_ext}{ext}"
                new_path = file.parent / new_name
                
                if new_path.exists():
                    print(f"⚠️ 跳过：{new_name} 已存在")
                    continue
                
                shutil.move(str(file), str(new_path))
                print(f"✅ {old_name} → {new_name}")
                success_count += 1
                
            except Exception as e:
                print(f"❌ 失败 {file.name}: {e}")
        
        print("-" * 60)
        print(f"🎉 完成！成功：{success_count}/{len(files)}")
        return success_count
    
    def remove_special_chars(self, replacement: str = "_") -> int:
        """
        移除文件名中的特殊字符
        
        Args:
            replacement: 替换字符
            
        Returns:
            重命名的文件数量
        """
        files = self.get_files()
        success_count = 0
        
        print(f"🧹 移除特殊字符（替换为：{replacement}）")
        print("-" * 60)
        
        # 特殊字符模式
        pattern = r'[<>:"/\\|？*]'
        
        for file in files:
            try:
                old_name = file.name
                name_without_ext = file.stem
                ext = file.suffix
                
                # 移除特殊字符
                new_name = re.sub(pattern, replacement, name_without_ext)
                new_name = f"{new_name}{ext}"
                
                if new_name == old_name:
                    continue
                
                new_path = file.parent / new_name
                
                if new_path.exists():
                    print(f"⚠️ 跳过：{new_name} 已存在")
                    continue
                
                shutil.move(str(file), str(new_path))
                print(f"✅ {old_name} → {new_name}")
                success_count += 1
                
            except Exception as e:
                print(f"❌ 失败 {file.name}: {e}")
        
        print("-" * 60)
        print(f"🎉 完成！成功：{success_count}/{len(files)}")
        return success_count


def main():
    """主函数 - 命令行界面"""
    import argparse
    
    parser = argparse.ArgumentParser(description="文件批量重命名工具")
    parser.add_argument("directory", help="目标目录路径")
    parser.add_argument("-t", "--types", nargs="+", help="文件类型，如 .jpg .png")
    parser.add_argument("-p", "--pattern", help="正则表达式模式")
    parser.add_argument("-r", "--replace", help="替换文本")
    parser.add_argument("-pre", "--prefix", help="文件名前缀")
    parser.add_argument("-suf", "--suffix", help="文件名后缀")
    parser.add_argument("-n", "--number", type=int, default=1, help="起始编号")
    parser.add_argument("--timestamp", action="store_true", help="使用时间戳")
    parser.add_argument("-e", "--execute", action="store_true", help="执行重命名（默认仅预览）")
    parser.add_argument("--date-prefix", action="store_true", help="添加修改日期前缀")
    parser.add_argument("--clean", action="store_true", help="移除特殊字符")
    
    args = parser.parse_args()
    
    renamer = FileRenamer(args.directory, args.types)
    
    if args.date_prefix:
        renamer.add_date_prefix()
    elif args.clean:
        renamer.remove_special_chars()
    else:
        renamer.rename(
            pattern=args.pattern,
            replacement=args.replace,
            prefix=args.prefix,
            suffix=args.suffix,
            start_number=args.number,
            use_timestamp=args.timestamp,
            dry_run=not args.execute
        )


if __name__ == "__main__":
    main()
