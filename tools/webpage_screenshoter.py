#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
网页批量截图工具
功能：批量网页截图，支持定时、滚动截图、不同分辨率

作者：AI Code Assistant
GitHub: https://github.com/a378135002/ai-code-assistant

安装依赖：
pip install playwright
playwright install
"""

import asyncio
from pathlib import Path
from datetime import datetime
from typing import List, Optional
from playwright.async_api import async_playwright


class WebpageScreenshoter:
    """网页截图工具"""
    
    def __init__(self, output_dir: str = "screenshots"):
        """
        初始化工具
        
        Args:
            output_dir: 截图保存目录
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
    async def screenshot(self, url: str, width: int = 1920, height: int = 1080,
                        full_page: bool = False, wait_time: int = 2000,
                        filename: str = None) -> str:
        """
        截取单个网页
        
        Args:
            url: 网页 URL
            width: 浏览器宽度
            height: 浏览器高度
            full_page: 是否截取整个页面（滚动截图）
            wait_time: 等待时间（毫秒），让页面加载完成
            filename: 输出文件名（可选）
            
        Returns:
            保存的文件路径
        """
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page(viewport={"width": width, "height": height})
            
            try:
                print(f"📸 正在截图：{url}")
                await page.goto(url, wait_until="networkidle", timeout=30000)
                await asyncio.sleep(wait_time / 1000)
                
                # 生成文件名
                if not filename:
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    domain = url.split("//")[-1].split("/")[0].replace(".", "_")
                    filename = f"{timestamp}_{domain}.png"
                
                output_path = self.output_dir / filename
                
                # 截图
                await page.screenshot(
                    path=str(output_path),
                    full_page=full_page
                )
                
                print(f"✅ 截图已保存：{output_path}")
                return str(output_path)
                
            except Exception as e:
                print(f"❌ 截图失败：{e}")
                raise
            finally:
                await browser.close()
    
    async def batch_screenshot(self, urls: List[str], prefix: str = None,
                               full_page: bool = False, wait_time: int = 2000) -> List[str]:
        """
        批量截图
        
        Args:
            urls: URL 列表
            prefix: 文件名前缀（可选）
            full_page: 是否全页截图
            wait_time: 等待时间
            
        Returns:
            保存的文件路径列表
        """
        results = []
        
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            
            for i, url in enumerate(urls, 1):
                print(f"[{i}/{len(urls)}] 处理：{url}")
                
                try:
                    page = await browser.new_page()
                    await page.goto(url, wait_until="networkidle", timeout=30000)
                    await asyncio.sleep(wait_time / 1000)
                    
                    # 生成文件名
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    if prefix:
                        filename = f"{prefix}_{i:03d}.png"
                    else:
                        domain = url.split("//")[-1].split("/")[0].replace(".", "_")
                        filename = f"{timestamp}_{domain}.png"
                    
                    output_path = self.output_dir / filename
                    
                    await page.screenshot(path=str(output_path), full_page=full_page)
                    print(f"✅ 已保存：{filename}")
                    
                    results.append(str(output_path))
                    
                except Exception as e:
                    print(f"❌ 失败 {url}: {e}")
                    results.append(None)
                finally:
                    await page.close()
        
        await browser.close()
        return results
    
    async def screenshot_with_devices(self, url: str, 
                                      devices: List[dict] = None) -> List[str]:
        """
        使用不同设备尺寸截图
        
        Args:
            url: 网页 URL
            devices: 设备列表，如 [{"name": "iPhone", "width": 375, "height": 667}]
            
        Returns:
            保存的文件路径列表
        """
        if devices is None:
            devices = [
                {"name": "Desktop", "width": 1920, "height": 1080},
                {"name": "Laptop", "width": 1366, "height": 768},
                {"name": "Tablet", "width": 768, "height": 1024},
                {"name": "Mobile", "width": 375, "height": 667},
            ]
        
        results = []
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        domain = url.split("//")[-1].split("/")[0].replace(".", "_")
        
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            
            for device in devices:
                print(f"📱 设备：{device['name']} ({device['width']}x{device['height']})")
                
                page = await browser.new_page(
                    viewport={"width": device["width"], "height": device["height"]}
                )
                
                try:
                    await page.goto(url, wait_until="networkidle", timeout=30000)
                    await asyncio.sleep(2)
                    
                    filename = f"{timestamp}_{domain}_{device['name']}.png"
                    output_path = self.output_dir / filename
                    
                    await page.screenshot(path=str(output_path))
                    print(f"✅ 已保存：{filename}")
                    
                    results.append(str(output_path))
                    
                except Exception as e:
                    print(f"❌ 失败 {device['name']}: {e}")
                    results.append(None)
                finally:
                    await page.close()
        
        await browser.close()
        return results


async def main():
    """主函数 - 命令行界面"""
    import argparse
    
    parser = argparse.ArgumentParser(description="网页批量截图工具")
    parser.add_argument("urls", nargs="+", help="网页 URL 列表")
    parser.add_argument("-o", "--output", default="screenshots", help="输出目录")
    parser.add_argument("-f", "--full-page", action="store_true", help="全页截图（滚动）")
    parser.add_argument("-w", "--width", type=int, default=1920, help="浏览器宽度")
    parser.add_argument("-ht", "--height", type=int, default=1080, help="浏览器高度")
    parser.add_argument("-t", "--wait", type=int, default=2000, help="等待时间（毫秒）")
    parser.add_argument("-p", "--prefix", help="文件名前缀")
    parser.add_argument("--devices", action="store_true", help="使用多种设备尺寸截图")
    
    args = parser.parse_args()
    
    screenshoter = WebpageScreenshoter(args.output)
    
    if args.devices:
        # 多设备截图（只处理第一个 URL）
        await screenshoter.screenshot_with_devices(args.urls[0])
    else:
        # 批量截图
        await screenshoter.batch_screenshot(
            args.urls,
            prefix=args.prefix,
            full_page=args.full_page,
            wait_time=args.wait
        )
    
    print(f"\n🎉 截图完成！保存到：{Path(args.output).absolute()}")


if __name__ == "__main__":
    asyncio.run(main())
