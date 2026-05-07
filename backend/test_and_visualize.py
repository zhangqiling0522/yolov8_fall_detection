import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import requests
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei']  # 使用黑体
plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题

BASE_URL = "http://localhost:8000"

def test_api_connection():
    """测试API连接"""
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            print("✓ API连接成功")
            return True
    except Exception as e:
        print(f"✗ API连接失败: {e}")
        return False

def get_statistics():
    """获取统计数据"""
    try:
        response = requests.get(f"{BASE_URL}/statistics/accuracy")
        if response.status_code == 200:
            print("✓ 获取统计数据成功")
            return response.json()
        else:
            print(f"✗ 获取统计数据失败: {response.status_code}")
            return None
    except Exception as e:
        print(f"✗ 获取统计数据异常: {e}")
        return None

def get_scene_statistics():
    """获取按场景分组的统计数据"""
    try:
        response = requests.get(f"{BASE_URL}/statistics/by-scene")
        if response.status_code == 200:
            print("✓ 获取场景统计数据成功")
            return response.json()
        else:
            print(f"✗ 获取场景统计数据失败: {response.status_code}")
            return None
    except Exception as e:
        print(f"✗ 获取场景统计数据异常: {e}")
        return None

def get_comparison_data():
    """获取对比数据"""
    try:
        response = requests.get(f"{BASE_URL}/statistics/comparison")
        if response.status_code == 200:
            print("✓ 获取对比数据成功")
            return response.json()
        else:
            print(f"✗ 获取对比数据失败: {response.status_code}")
            return None
    except Exception as e:
        print(f"✗ 获取对比数据异常: {e}")
        return None

def plot_overall_metrics(stats):
    """绘制总体指标图表"""
    fig, ax = plt.subplots(figsize=(10, 6))
    
    metrics = ['精确率', '召回率', '准确率', 'F1分数']
    values = [
        stats['precision'],
        stats['recall'],
        stats['accuracy'],
        stats['f1_score']
    ]
    
    # 绘制柱状图
    bars = ax.bar(metrics, values, color=['#4CAF50', '#2196F3', '#FF9800', '#9C27B0'])
    
    # 在柱子上添加数值标签
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.3f}',
                ha='center', va='bottom')
    
    ax.set_ylim(0, 1.1)
    ax.set_title(f'系统总体指标（总样本数: {stats["total_samples"]}）', fontsize=14, fontweight='bold')
    ax.set_ylabel('值')
    ax.grid(axis='y', alpha=0.3)
    
    # 添加表格信息
    table_data = [
        ['指标', '数值'],
        ['总样本数', str(stats['total_samples'])],
        ['真阳性', str(stats['true_positive'])],
        ['假阳性', str(stats['false_positive'])],
        ['假阴性', str(stats['false_negative'])],
        ['真阴性', str(stats['true_negative'])]
    ]
    
    # 在图表下方添加表格
    ax_table = fig.add_axes([0.15, -0.25, 0.7, 0.15])
    ax_table.axis('off')
    table = ax_table.table(cellText=table_data, loc='center', cellLoc='center')
    table.auto_set_font_size(False)
    table.set_fontsize(11)
    table.scale(1, 1.5)
    
    plt.tight_layout()
    plt.savefig('overall_metrics.png', dpi=300, bbox_inches='tight')
    print("✓ 总体指标图表已保存: overall_metrics.png")

def plot_scene_comparison(scene_stats):
    """绘制场景对比图表"""
    if not scene_stats:
        print("✗ 没有场景数据")
        return
    
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    
    scenes = [item['scene'] for item in scene_stats]
    
    # 1. 精确率对比
    ax1 = axes[0, 0]
    precision_values = [item['precision'] for item in scene_stats]
    bars1 = ax1.bar(scenes, precision_values, color='#4CAF50')
    for bar in bars1:
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.3f}',
                ha='center', va='bottom')
    ax1.set_title('不同场景的精确率对比', fontweight='bold')
    ax1.set_ylim(0, 1)
    ax1.grid(axis='y', alpha=0.3)
    
    # 2. 召回率对比
    ax2 = axes[0, 1]
    recall_values = [item['recall'] for item in scene_stats]
    bars2 = ax2.bar(scenes, recall_values, color='#2196F3')
    for bar in bars2:
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.3f}',
                ha='center', va='bottom')
    ax2.set_title('不同场景的召回率对比', fontweight='bold')
    ax2.set_ylim(0, 1)
    ax2.grid(axis='y', alpha=0.3)
    
    # 3. 准确率对比
    ax3 = axes[1, 0]
    accuracy_values = [item['accuracy'] for item in scene_stats]
    bars3 = ax3.bar(scenes, accuracy_values, color='#FF9800')
    for bar in bars3:
        height = bar.get_height()
        ax3.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.3f}',
                ha='center', va='bottom')
    ax3.set_title('不同场景的准确率对比', fontweight='bold')
    ax3.set_ylim(0, 1)
    ax3.grid(axis='y', alpha=0.3)
    
    # 4. F1分数对比
    ax4 = axes[1, 1]
    f1_values = [item['f1_score'] for item in scene_stats]
    bars4 = ax4.bar(scenes, f1_values, color='#9C27B0')
    for bar in bars4:
        height = bar.get_height()
        ax4.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.3f}',
                ha='center', va='bottom')
    ax4.set_title('不同场景的F1分数对比', fontweight='bold')
    ax4.set_ylim(0, 1)
    ax4.grid(axis='y', alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('scene_comparison.png', dpi=300)
    print("✓ 场景对比图表已保存: scene_comparison.png")

def plot_method_comparison(comparison_data):
    """绘制方法对比图表"""
    if not comparison_data or 'comparison' not in comparison_data:
        print("✗ 没有对比数据")
        return
    
    comparison = comparison_data['comparison']
    methods = [item['method'] for item in comparison]
    
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    
    # 1. 精确率对比
    ax1 = axes[0, 0]
    precision_values = [item['precision'] for item in comparison]
    colors = ['#4CAF50' if '本系统' in m else '#757575' for m in methods]
    bars1 = ax1.bar(methods, precision_values, color=colors)
    for bar in bars1:
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.3f}',
                ha='center', va='bottom')
    ax1.set_title('与同类研究的精确率对比', fontweight='bold')
    ax1.set_ylim(0.75, 1)
    ax1.grid(axis='y', alpha=0.3)
    ax1.tick_params(axis='x', rotation=15)
    
    # 2. 召回率对比
    ax2 = axes[0, 1]
    recall_values = [item['recall'] for item in comparison]
    bars2 = ax2.bar(methods, recall_values, color=colors)
    for bar in bars2:
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.3f}',
                ha='center', va='bottom')
    ax2.set_title('与同类研究的召回率对比', fontweight='bold')
    ax2.set_ylim(0.75, 1)
    ax2.grid(axis='y', alpha=0.3)
    ax2.tick_params(axis='x', rotation=15)
    
    # 3. 准确率对比
    ax3 = axes[1, 0]
    accuracy_values = [item['accuracy'] for item in comparison]
    bars3 = ax3.bar(methods, accuracy_values, color=colors)
    for bar in bars3:
        height = bar.get_height()
        ax3.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.3f}',
                ha='center', va='bottom')
    ax3.set_title('与同类研究的准确率对比', fontweight='bold')
    ax3.set_ylim(0.75, 1)
    ax3.grid(axis='y', alpha=0.3)
    ax3.tick_params(axis='x', rotation=15)
    
    # 4. F1分数对比
    ax4 = axes[1, 1]
    f1_values = [item['f1_score'] for item in comparison]
    bars4 = ax4.bar(methods, f1_values, color=colors)
    for bar in bars4:
        height = bar.get_height()
        ax4.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.3f}',
                ha='center', va='bottom')
    ax4.set_title('与同类研究的F1分数对比', fontweight='bold')
    ax4.set_ylim(0.75, 1)
    ax4.grid(axis='y', alpha=0.3)
    ax4.tick_params(axis='x', rotation=15)
    
    plt.tight_layout()
    plt.savefig('method_comparison.png', dpi=300)
    print("✓ 方法对比图表已保存: method_comparison.png")

def plot_radar_chart(comparison_data):
    """绘制雷达图"""
    if not comparison_data or 'comparison' not in comparison_data:
        print("✗ 没有对比数据")
        return
    
    comparison = comparison_data['comparison']
    
    fig = plt.figure(figsize=(10, 10))
    ax = fig.add_subplot(111, projection='polar')
    
    categories = ['精确率', '召回率', '准确率', 'F1分数']
    N = len(categories)
    
    angles = [n / float(N) * 2 * np.pi for n in range(N)]
    angles += angles[:1]
    
    for item in comparison:
        values = [
            item['precision'],
            item['recall'],
            item['accuracy'],
            item['f1_score']
        ]
        values += values[:1]
        
        color = '#4CAF50' if '本系统' in item['method'] else '#757575'
        linewidth = 3 if '本系统' in item['method'] else 2
        ax.plot(angles, values, 'o-', linewidth=linewidth, label=item['method'], color=color)
        ax.fill(angles, values, alpha=0.1, color=color)
    
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(categories, fontsize=12)
    ax.set_ylim(0.7, 1)
    ax.set_title('系统性能雷达图对比', size=14, fontweight='bold', y=1.08)
    ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.0))
    ax.grid(True)
    
    plt.tight_layout()
    plt.savefig('radar_comparison.png', dpi=300)
    print("✓ 雷达图已保存: radar_comparison.png")

def main():
    print("=" * 60)
    print("摔倒检测系统 - 测试与可视化工具")
    print("=" * 60)
    print(f"测试时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # 1. 测试API连接
    if not test_api_connection():
        print("\n请先启动后端服务!")
        return
    
    print()
    
    # 2. 获取统计数据
    stats = get_statistics()
    if stats:
        plot_overall_metrics(stats)
    
    print()
    
    # 3. 获取场景统计
    scene_stats = get_scene_statistics()
    if scene_stats:
        plot_scene_comparison(scene_stats)
    
    print()
    
    # 4. 获取对比数据
    comparison_data = get_comparison_data()
    if comparison_data:
        plot_method_comparison(comparison_data)
        plot_radar_chart(comparison_data)
    
    print()
    print("=" * 60)
    print("测试与可视化完成!")
    print("生成的图表文件:")
    print("  - overall_metrics.png: 总体指标图表")
    print("  - scene_comparison.png: 场景对比图表")
    print("  - method_comparison.png: 方法对比图表")
    print("  - radar_comparison.png: 雷达图对比")
    print("=" * 60)

if __name__ == "__main__":
    main()
