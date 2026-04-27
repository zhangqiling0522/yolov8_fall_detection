import requests
import time
import statistics
import json
from datetime import datetime
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

class APITester:
    def __init__(self, base_url="http://localhost:8000"):
        self.base_url = base_url
        self.test_results = {}
    
    def test_health_check(self, iterations=50):
        """测试健康检查接口"""
        endpoint = "/health"
        times = []
        
        print(f"\n测试健康检查接口 ({iterations}次):")
        print("=" * 60)
        
        for i in range(iterations):
            start_time = time.time()
            try:
                response = requests.get(f"{self.base_url}{endpoint}")
                end_time = time.time()
                response_time = (end_time - start_time) * 1000  # 转换为毫秒
                times.append(response_time)
                
                if i < 5 or i == iterations - 1:
                    print(f"请求 {i+1}: {response_time:.2f}ms, 状态码: {response.status_code}")
            except Exception as e:
                print(f"请求 {i+1}: 错误 - {str(e)}")
        
        if times:
            self._print_statistics(times)
            self.test_results[endpoint] = {
                "times": times,
                "average": statistics.mean(times),
                "min": min(times),
                "max": max(times),
                "std_dev": statistics.stdev(times) if len(times) > 1 else 0
            }
    
    def test_get_old_persons(self, iterations=50):
        """测试获取老人列表接口"""
        endpoint = "/old-persons"
        times = []
        
        print(f"\n测试获取老人列表接口 ({iterations}次):")
        print("=" * 60)
        
        for i in range(iterations):
            start_time = time.time()
            try:
                response = requests.get(f"{self.base_url}{endpoint}")
                end_time = time.time()
                response_time = (end_time - start_time) * 1000
                times.append(response_time)
                
                if i < 5 or i == iterations - 1:
                    print(f"请求 {i+1}: {response_time:.2f}ms, 状态码: {response.status_code}")
            except Exception as e:
                print(f"请求 {i+1}: 错误 - {str(e)}")
        
        if times:
            self._print_statistics(times)
            self.test_results[endpoint] = {
                "times": times,
                "average": statistics.mean(times),
                "min": min(times),
                "max": max(times),
                "std_dev": statistics.stdev(times) if len(times) > 1 else 0
            }
    
    def test_login(self, iterations=50):
        """测试登录接口"""
        endpoint = "/login"
        times = []
        login_data = {
            "name": "小张",
            "phone": "13800138004",
            "password": "123456"
        }
        
        print(f"\n测试登录接口 ({iterations}次):")
        print("=" * 60)
        
        for i in range(iterations):
            start_time = time.time()
            try:
                response = requests.post(f"{self.base_url}{endpoint}", json=login_data)
                end_time = time.time()
                response_time = (end_time - start_time) * 1000
                times.append(response_time)
                
                if i < 5 or i == iterations - 1:
                    print(f"请求 {i+1}: {response_time:.2f}ms, 状态码: {response.status_code}")
            except Exception as e:
                print(f"请求 {i+1}: 错误 - {str(e)}")
        
        if times:
            self._print_statistics(times)
            self.test_results[endpoint] = {
                "times": times,
                "average": statistics.mean(times),
                "min": min(times),
                "max": max(times),
                "std_dev": statistics.stdev(times) if len(times) > 1 else 0
            }
    
    def test_detect_fall(self, iterations=50):
        """测试摔倒检测接口"""
        endpoint = "/detect/fall"
        times = []
        
        # 准备测试图像（使用一个简单的测试图像）
        # 这里使用一个空的图像数据，实际测试时应该使用真实的图像文件
        # 注意：实际测试时需要替换为真实的图像文件路径
        import base64
        import io
        from PIL import Image
        
        # 创建一个简单的测试图像
        img = Image.new('RGB', (640, 480), color='white')
        img_byte_arr = io.BytesIO()
        img.save(img_byte_arr, format='JPEG')
        img_byte_arr.seek(0)
        
        print(f"\n测试摔倒检测接口 ({iterations}次):")
        print("=" * 60)
        
        for i in range(iterations):
            start_time = time.time()
            try:
                files = {'file': ('test.jpg', img_byte_arr.getvalue(), 'image/jpeg')}
                response = requests.post(f"{self.base_url}{endpoint}", files=files)
                end_time = time.time()
                response_time = (end_time - start_time) * 1000
                times.append(response_time)
                
                if i < 5 or i == iterations - 1:
                    print(f"请求 {i+1}: {response_time:.2f}ms, 状态码: {response.status_code}")
            except Exception as e:
                print(f"请求 {i+1}: 错误 - {str(e)}")
        
        if times:
            self._print_statistics(times)
            self.test_results[endpoint] = {
                "times": times,
                "average": statistics.mean(times),
                "min": min(times),
                "max": max(times),
                "std_dev": statistics.stdev(times) if len(times) > 1 else 0
            }
    
    def test_alarm_stop(self, iterations=50):
        """测试停止报警接口"""
        endpoint = "/alarm/stop"
        times = []
        
        print(f"\n测试停止报警接口 ({iterations}次):")
        print("=" * 60)
        
        for i in range(iterations):
            start_time = time.time()
            try:
                response = requests.post(f"{self.base_url}{endpoint}")
                end_time = time.time()
                response_time = (end_time - start_time) * 1000
                times.append(response_time)
                
                if i < 5 or i == iterations - 1:
                    print(f"请求 {i+1}: {response_time:.2f}ms, 状态码: {response.status_code}")
            except Exception as e:
                print(f"请求 {i+1}: 错误 - {str(e)}")
        
        if times:
            self._print_statistics(times)
            self.test_results[endpoint] = {
                "times": times,
                "average": statistics.mean(times),
                "min": min(times),
                "max": max(times),
                "std_dev": statistics.stdev(times) if len(times) > 1 else 0
            }
    
    def _print_statistics(self, times):
        """打印统计信息"""
        if not times:
            return
        
        avg_time = statistics.mean(times)
        min_time = min(times)
        max_time = max(times)
        std_dev = statistics.stdev(times) if len(times) > 1 else 0
        
        print("\n统计信息:")
        print(f"平均响应时间: {avg_time:.2f}ms")
        print(f"最小响应时间: {min_time:.2f}ms")
        print(f"最大响应时间: {max_time:.2f}ms")
        print(f"标准差: {std_dev:.2f}ms")
    
    def run_all_tests(self, iterations=50):
        """运行所有测试"""
        print(f"开始API性能测试 - 时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 80)
        print(f"测试服务器: {self.base_url}")
        print(f"测试次数: {iterations}")
        print("=" * 80)
        
        # 运行各个测试
        self.test_health_check(iterations)
        self.test_get_old_persons(iterations)
        self.test_login(iterations)
        self.test_alarm_stop(iterations)
        self.test_detect_fall(50)  # 摔倒检测测试次数较少，因为耗时较长
        
        # 保存测试结果
        self.save_results()
        
        # 生成可视化图表
        self.visualize_results()
        
        print("\n" + "=" * 80)
        print("测试完成!")
        print(f"测试结果已保存到: api_test_results.json")
    
    def save_results(self):
        """保存测试结果到JSON文件"""
        results = {
            "timestamp": datetime.now().isoformat(),
            "base_url": self.base_url,
            "results": self.test_results
        }
        
        with open("api_test_results.json", "w", encoding="utf-8") as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
    
    def plot_response_times(self):
        """绘制响应时间折线图"""
        if not self.test_results:
            print("没有测试结果可绘制")
            return
        
        plt.figure(figsize=(12, 8))
        
        for endpoint, data in self.test_results.items():
            times = data['times']
            plt.plot(range(1, len(times) + 1), times, label=endpoint, marker='o', markersize=3)
            
            # 标注关键数据点（首尾和最大值）
            if times:
                # 标注第一个点
                plt.annotate(f'{times[0]:.1f}', (1, times[0]), 
                            textcoords="offset points", xytext=(0,10), ha='center')
                # 标注最后一个点
                plt.annotate(f'{times[-1]:.1f}', (len(times), times[-1]), 
                            textcoords="offset points", xytext=(0,10), ha='center')
                # 标注最大值点
                max_idx = times.index(max(times)) + 1
                plt.annotate(f'{max(times):.1f}', (max_idx, max(times)), 
                            textcoords="offset points", xytext=(0,10), ha='center', color='red')
        
        plt.title('API响应时间趋势', fontsize=16)
        plt.xlabel('请求次数', fontsize=12)
        plt.ylabel('响应时间 (ms)', fontsize=12)
        plt.grid(True, alpha=0.3)
        plt.legend()
        plt.tight_layout()
        plt.savefig('api_response_times.png', dpi=150)
        print("响应时间折线图已保存到: api_response_times.png")
    
    def plot_boxplot(self):
        """绘制响应时间箱线图"""
        if not self.test_results:
            print("没有测试结果可绘制")
            return
        
        plt.figure(figsize=(12, 8))
        
        data = []
        labels = []
        stats = []
        
        for endpoint, result in self.test_results.items():
            data.append(result['times'])
            labels.append(endpoint)
            # 计算统计数据
            times = result['times']
            q1 = np.percentile(times, 25)
            q3 = np.percentile(times, 75)
            median = np.median(times)
            stats.append({"q1": q1, "median": median, "q3": q3})
        
        # 绘制箱线图
        box = plt.boxplot(data, labels=labels, patch_artist=True)
        
        # 美化箱线图
        colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd']
        for patch, color in zip(box['boxes'], colors):
            patch.set_facecolor(color)
        
        # 添加数据标注
        for i, (stat, times) in enumerate(zip(stats, data)):
            # 标注中位数
            plt.annotate(f'{stat["median"]:.1f}', (i+1, stat["median"]),
                        textcoords="offset points", xytext=(0,10), ha='center', fontweight='bold')
            # 标注四分位数
            plt.annotate(f'Q1:{stat["q1"]:.1f}', (i+1, stat["q1"]),
                        textcoords="offset points", xytext=(-30,-10), ha='center', fontsize=9)
            plt.annotate(f'Q3:{stat["q3"]:.1f}', (i+1, stat["q3"]),
                        textcoords="offset points", xytext=(30,-10), ha='center', fontsize=9)
            # 标注最大值和最小值
            plt.annotate(f'Max:{max(times):.1f}', (i+1, max(times)),
                        textcoords="offset points", xytext=(0,10), ha='center', color='red', fontsize=9)
            plt.annotate(f'Min:{min(times):.1f}', (i+1, min(times)),
                        textcoords="offset points", xytext=(0,-15), ha='center', color='green', fontsize=9)
        
        plt.xticks(rotation=45, ha='right')
        plt.title('API响应时间分布', fontsize=16)
        plt.ylabel('响应时间 (ms)', fontsize=12)
        plt.grid(True, alpha=0.3, axis='y')
        plt.tight_layout()
        plt.savefig('api_response_boxplot.png', dpi=150)
        print("响应时间箱线图已保存到: api_response_boxplot.png")
    
    def plot_bar_chart(self):
        """绘制平均响应时间柱状图"""
        if not self.test_results:
            print("没有测试结果可绘制")
            return
        
        plt.figure(figsize=(12, 8))
        
        endpoints = []
        avg_times = []
        min_times = []
        max_times = []
        
        for endpoint, result in self.test_results.items():
            endpoints.append(endpoint)
            avg_times.append(result['average'])
            min_times.append(result['min'])
            max_times.append(result['max'])
        
        x = np.arange(len(endpoints))
        width = 0.25
        
        # 绘制柱状图
        bars_min = plt.bar(x - width, min_times, width, label='最小响应时间', color='#98df8a')
        bars_avg = plt.bar(x, avg_times, width, label='平均响应时间', color='#1f77b4')
        bars_max = plt.bar(x + width, max_times, width, label='最大响应时间', color='#ff7f0e')
        
        # 添加数据标注
        for bar in bars_min:
            height = bar.get_height()
            plt.annotate(f'{height:.1f}',
                        xy=(bar.get_x() + bar.get_width() / 2, height),
                        xytext=(0, 3),  # 3 points vertical offset
                        textcoords="offset points",
                        ha='center', va='bottom', fontsize=9)
        
        for bar in bars_avg:
            height = bar.get_height()
            plt.annotate(f'{height:.1f}',
                        xy=(bar.get_x() + bar.get_width() / 2, height),
                        xytext=(0, 3),
                        textcoords="offset points",
                        ha='center', va='bottom', fontsize=9, fontweight='bold')
        
        for bar in bars_max:
            height = bar.get_height()
            plt.annotate(f'{height:.1f}',
                        xy=(bar.get_x() + bar.get_width() / 2, height),
                        xytext=(0, 3),
                        textcoords="offset points",
                        ha='center', va='bottom', fontsize=9)
        
        plt.xticks(x, endpoints, rotation=45, ha='right')
        plt.title('API响应时间对比', fontsize=16)
        plt.ylabel('响应时间 (ms)', fontsize=12)
        plt.legend()
        plt.grid(True, alpha=0.3, axis='y')
        plt.tight_layout()
        plt.savefig('api_response_bar.png', dpi=150)
        print("平均响应时间柱状图已保存到: api_response_bar.png")
    
    def plot_combined_chart(self):
        """将响应时间趋势和柱状图绘制到同一张图上"""
        if not self.test_results:
            print("没有测试结果可绘制")
            return
        
        # 创建一个2x1的子图
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 12))
        
        # 绘制响应时间趋势图（上半部分）
        ax1.set_title('API响应时间趋势', fontsize=16)
        ax1.set_xlabel('请求次数', fontsize=12)
        ax1.set_ylabel('响应时间 (ms)', fontsize=12)
        ax1.grid(True, alpha=0.3)
        
        for endpoint, data in self.test_results.items():
            times = data['times']
            ax1.plot(range(1, len(times) + 1), times, label=endpoint, marker='o', markersize=3)
            
            # 标注关键数据点
            if times:
                # 标注第一个点
                ax1.annotate(f'{times[0]:.1f}', (1, times[0]), 
                            textcoords="offset points", xytext=(0,10), ha='center')
                # 标注最后一个点
                ax1.annotate(f'{times[-1]:.1f}', (len(times), times[-1]), 
                            textcoords="offset points", xytext=(0,10), ha='center')
                # 标注最大值点
                max_idx = times.index(max(times)) + 1
                ax1.annotate(f'{max(times):.1f}', (max_idx, max(times)), 
                            textcoords="offset points", xytext=(0,10), ha='center', color='red')
        
        ax1.legend()
        
        # 绘制平均响应时间柱状图（下半部分）
        endpoints = []
        avg_times = []
        min_times = []
        max_times = []
        
        for endpoint, result in self.test_results.items():
            endpoints.append(endpoint)
            avg_times.append(result['average'])
            min_times.append(result['min'])
            max_times.append(result['max'])
        
        x = np.arange(len(endpoints))
        width = 0.25
        
        # 绘制柱状图
        bars_min = ax2.bar(x - width, min_times, width, label='最小响应时间', color='#98df8a')
        bars_avg = ax2.bar(x, avg_times, width, label='平均响应时间', color='#1f77b4')
        bars_max = ax2.bar(x + width, max_times, width, label='最大响应时间', color='#ff7f0e')
        
        # 添加数据标注
        for bar in bars_min:
            height = bar.get_height()
            ax2.annotate(f'{height:.1f}',
                        xy=(bar.get_x() + bar.get_width() / 2, height),
                        xytext=(0, 3),
                        textcoords="offset points",
                        ha='center', va='bottom', fontsize=9)
        
        for bar in bars_avg:
            height = bar.get_height()
            ax2.annotate(f'{height:.1f}',
                        xy=(bar.get_x() + bar.get_width() / 2, height),
                        xytext=(0, 3),
                        textcoords="offset points",
                        ha='center', va='bottom', fontsize=9, fontweight='bold')
        
        for bar in bars_max:
            height = bar.get_height()
            ax2.annotate(f'{height:.1f}',
                        xy=(bar.get_x() + bar.get_width() / 2, height),
                        xytext=(0, 3),
                        textcoords="offset points",
                        ha='center', va='bottom', fontsize=9)
        
        ax2.set_title('API响应时间对比', fontsize=16)
        ax2.set_xlabel('API端点', fontsize=12)
        ax2.set_ylabel('响应时间 (ms)', fontsize=12)
        ax2.set_xticks(x)
        ax2.set_xticklabels(endpoints, rotation=45, ha='right')
        ax2.legend()
        ax2.grid(True, alpha=0.3, axis='y')
        
        plt.tight_layout()
        plt.savefig('api_combined_chart.png', dpi=150)
        print("组合图表已保存到: api_combined_chart.png")
    
    def visualize_results(self):
        """可视化所有测试结果"""
        print("\n生成测试结果可视化...")
        self.plot_response_times()
        self.plot_boxplot()
        self.plot_bar_chart()
        self.plot_combined_chart()  # 添加组合图表
        print("可视化完成!")

if __name__ == "__main__":
    tester = APITester()
    tester.run_all_tests(iterations=50)
