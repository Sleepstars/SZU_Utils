#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
局域网设备扫描工具
扫描指定网段内所有可ping通的设备
"""

import subprocess
import threading
import time
import ipaddress
import platform
import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
import socket


class LanScanner:
    def __init__(self, network="192.168.3.0/24", timeout=1, max_workers=50):
        """
        初始化局域网扫描器

        Args:
            network (str): 要扫描的网段，默认为 192.168.3.0/24
            timeout (int): ping超时时间（秒），默认1秒
            max_workers (int): 最大并发线程数，默认50
        """
        self.network = ipaddress.IPv4Network(network, strict=False)
        self.timeout = timeout
        self.max_workers = max_workers
        self.alive_hosts = []
        self.lock = threading.Lock()

        # 根据操作系统设置ping命令参数
        self.system = platform.system().lower()
        if self.system == "windows":
            self.ping_cmd = ["ping", "-n", "1", "-w", str(timeout * 1000)]
        else:
            self.ping_cmd = ["ping", "-c", "1", "-W", str(timeout)]

    def ping_host(self, ip):
        """
        ping单个主机

        Args:
            ip (str): 要ping的IP地址

        Returns:
            tuple: (ip, is_alive, response_time)
        """
        try:
            cmd = self.ping_cmd + [str(ip)]
            start_time = time.time()

            result = subprocess.run(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                timeout=self.timeout + 1,
                text=True
            )

            response_time = (time.time() - start_time) * 1000  # 转换为毫秒

            if result.returncode == 0:
                return ip, True, response_time
            else:
                return ip, False, None

        except subprocess.TimeoutExpired:
            return ip, False, None
        except Exception as e:
            print(f"Error ping {ip}: {e}")
            return ip, False, None

    def get_hostname(self, ip):
        """
        获取主机名

        Args:
            ip (str): IP地址

        Returns:
            str: 主机名，如果无法获取则返回 "Unknown"
        """
        try:
            hostname = socket.gethostbyaddr(str(ip))[0]
            return hostname
        except:
            return "Unknown"

    def scan_network(self, show_progress=True):
        """
        扫描整个网段

        Args:
            show_progress (bool): 是否显示进度

        Returns:
            list: 存活主机列表，每个元素为 (ip, hostname, response_time)
        """
        print(f"开始扫描网段: {self.network}")
        print(f"总共需要扫描 {self.network.num_addresses} 个IP地址")
        print("-" * 50)

        hosts = list(self.network.hosts())
        total_hosts = len(hosts)
        completed = 0

        self.alive_hosts = []

        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            # 提交所有ping任务
            future_to_ip = {executor.submit(self.ping_host, ip): ip for ip in hosts}

            for future in as_completed(future_to_ip):
                ip, is_alive, response_time = future.result()
                completed += 1

                if is_alive:
                    hostname = self.get_hostname(ip)
                    with self.lock:
                        self.alive_hosts.append((str(ip), hostname, response_time))

                    print(f"✓ {ip} - {hostname} ({response_time:.1f}ms)")

                if show_progress and completed % 10 == 0:
                    progress = (completed / total_hosts) * 100
                    print(f"进度: {completed}/{total_hosts} ({progress:.1f}%)")

        # 按IP地址排序
        self.alive_hosts.sort(key=lambda x: ipaddress.IPv4Address(x[0]))

        return self.alive_hosts

    def print_results(self):
        """打印扫描结果"""
        print("\n" + "=" * 60)
        print(f"扫描完成！发现 {len(self.alive_hosts)} 个活跃设备:")
        print("=" * 60)

        if not self.alive_hosts:
            print("未发现任何活跃设备")
            return

        print(f"{'IP地址':<15} {'主机名':<25} {'响应时间':<10}")
        print("-" * 60)

        for ip, hostname, response_time in self.alive_hosts:
            print(f"{ip:<15} {hostname:<25} {response_time:.1f}ms")

    def save_results(self, filename="scan_results.txt"):
        """
        保存扫描结果到文件

        Args:
            filename (str): 保存的文件名
        """
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(f"局域网扫描结果 - {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"扫描网段: {self.network}\n")
                f.write(f"发现设备数量: {len(self.alive_hosts)}\n")
                f.write("-" * 60 + "\n")
                f.write(f"{'IP地址':<15} {'主机名':<25} {'响应时间':<10}\n")
                f.write("-" * 60 + "\n")

                for ip, hostname, response_time in self.alive_hosts:
                    f.write(f"{ip:<15} {hostname:<25} {response_time:.1f}ms\n")

            print(f"\n结果已保存到: {filename}")
        except Exception as e:
            print(f"保存文件失败: {e}")


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description="局域网设备扫描工具")
    parser.add_argument(
        "-n", "--network",
        default="192.168.3.0/24",
        help="要扫描的网段 (默认: 192.168.3.0/24)"
    )
    parser.add_argument(
        "-t", "--timeout",
        type=int,
        default=1,
        help="ping超时时间（秒） (默认: 1)"
    )
    parser.add_argument(
        "-w", "--workers",
        type=int,
        default=50,
        help="最大并发线程数 (默认: 50)"
    )
    parser.add_argument(
        "-o", "--output",
        help="保存结果到文件"
    )
    parser.add_argument(
        "--no-progress",
        action="store_true",
        help="不显示扫描进度"
    )

    args = parser.parse_args()

    try:
        # 创建扫描器实例
        scanner = LanScanner(
            network=args.network,
            timeout=args.timeout,
            max_workers=args.workers
        )

        # 开始扫描
        start_time = time.time()
        scanner.scan_network(show_progress=not args.no_progress)
        end_time = time.time()

        # 显示结果
        scanner.print_results()

        print(f"\n扫描耗时: {end_time - start_time:.2f} 秒")

        # 保存结果
        if args.output:
            scanner.save_results(args.output)

    except KeyboardInterrupt:
        print("\n\n扫描被用户中断")
    except Exception as e:
        print(f"扫描过程中发生错误: {e}")


if __name__ == "__main__":
    main()