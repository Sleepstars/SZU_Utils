#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
快速网络扫描脚本
专门用于扫描 192.168.3.1/24 网段
"""

from LanScan import LanScanner
import time

def quick_scan():
    """快速扫描 192.168.3.1/24 网段"""
    print("=" * 60)
    print("局域网设备快速扫描工具")
    print("目标网段: 192.168.3.0/24")
    print("=" * 60)
    
    # 创建扫描器，使用较快的设置
    scanner = LanScanner(
        network="192.168.3.0/24",
        timeout=1,
        max_workers=100  # 增加并发数以提高扫描速度
    )
    
    try:
        # 开始扫描
        start_time = time.time()
        alive_hosts = scanner.scan_network(show_progress=True)
        end_time = time.time()
        
        # 显示结果
        scanner.print_results()
        
        print(f"\n扫描耗时: {end_time - start_time:.2f} 秒")
        
        # 自动保存结果
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        filename = f"scan_results_{timestamp}.txt"
        scanner.save_results(filename)
        
        return alive_hosts
        
    except KeyboardInterrupt:
        print("\n\n扫描被用户中断")
        return []
    except Exception as e:
        print(f"扫描过程中发生错误: {e}")
        return []

if __name__ == "__main__":
    quick_scan()
