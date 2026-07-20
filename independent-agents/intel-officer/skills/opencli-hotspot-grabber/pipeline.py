#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OpenCLI 情报处理管道 v2.0
整合：热点抓取 → AI 筛选 → 质量评分 → 智能排序 → 选题池生成 → 下游推送

用法:
    # 完整管道（抓取 + 分析 + 写选题池）
    python pipeline.py --full -p zhihu weibo baidu hackernews --output-pool topics-pool-0830.md
    
    # 只抓取
    python pipeline.py --grab -p zhihu weibo baidu hackernews -o tmp
    
    # 只分析（从已有 JSON 文件）
    python pipeline.py --analyze --input tmp/opencli-hotspots-*.json --output-pool topics-pool.md
"""

import subprocess
import json
import sys
import os
import re
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field

# Windows 编码修复
if sys.platform == 'win32':
    os.system('chcp 65001 > nul')
    sys.stdout.reconfigure(encoding='utf-8')

# 引入现有模块
try:
    from hotspot_grabber import OpenCLIGrabber
    GRABBER_AVAILABLE = True
except ImportError:
    GRABBER_AVAILABLE = False
    print("⚠️ hotspot_grabber 模块不可用")

try:
    from ai_scorer import score_ai_relevance, filter_ai_related, enhance_with_ai_score
    AI_SCORER_AVAILABLE = True
except ImportError:
    AI_SCORER_AVAILABLE = False
    print("⚠️ ai_scorer 模块不可用")


# ==================== 质量评分规则（固化 MEMORY.md 规则） ====================

@dataclass
class QualityRule:
    """质量规则定义"""
    keywords: List[str]
    score_delta: int  # 加分/减分
    rule_type: str  # 'positive' or 'negative'
    description: str


# 正面清单（加分项）
POSITIVE_RULES = [
    QualityRule(
        keywords=['步骤', '技巧', '方法', '流程', '指南', '教程'],
        score_delta=10,
        rule_type='positive',
        description='实战教程'
    ),
    QualityRule(
        keywords=['坑', '别', '不要', '避免', '错误', '问题', '解决'],
        score_delta=8,
        rule_type='positive',
        description='踩坑总结'
    ),
    QualityRule(
        keywords=['亲测', '实测', '好用', '效率', '提升', '推荐'],
        score_delta=8,
        rule_type='positive',
        description='工具实测'
    ),
    QualityRule(
        keywords=['省', '节省', '小时', '分钟', '时间', '损失'],
        score_delta=5,
        rule_type='positive',
        description='职场场景'
    ),
]

# 负面清单（减分项）
NEGATIVE_RULES = [
    QualityRule(
        keywords=['战略', '格局', '宏观', '趋势', '展望'],
        score_delta=-20,
        rule_type='negative',
        description='宏观空泛'
    ),
    QualityRule(
        keywords=['报告', '产业', '发展', '白皮书'],
        score_delta=-15,
        rule_type='negative',
        description='宏观报告'
    ),
    QualityRule(
        keywords=['论文', '争议', '学术', '研究'],
        score_delta=-10,
        rule_type='negative',
        description='学术争议'
    ),
]

# AI 话题关键词（从 ai_filter_rules.md 提取）
AI_KEYWORDS = {
    'core': [
        'AI', '人工智能', 'LLM', '大模型', 'GPT', 'Claude', 'Gemini',
        'Agent', '智能体', '多模态', 'AIGC', '生成式 AI',
        'Machine Learning', 'Deep Learning', 'NLP', '强化学习',
        'Transformer', 'Diffusion', 'RAG', '微调'
    ],
    'products': [
        'OpenAI', 'Anthropic', 'Google DeepMind', 'Meta AI', 'Microsoft AI',
        'ChatGPT', 'Copilot', 'Midjourney', 'Stable Diffusion', 'Sora',
        '文心一言', '通义千问', 'Kimi', '智谱 AI', '豆包', 'DeepSeek',
        'Cursor', 'Claude Code', 'GitHub Copilot', 'Perplexity'
    ],
    'tech': [
        'AI 手机', 'AI PC', 'NPU', 'AI 芯片', '半导体', '芯片',
        '自动驾驶', '新能源车', '智能汽车', '特斯拉', '华为', '小米',
        'GitHub', '开源', '程序员', '网络安全', '数据泄露'
    ],
}

# 非 AI 话题排除关键词
NON_AI_KEYWORDS = [
    '油价', '金价', '股市', '大盘', '战争', '政治', '外交',
    '体育', '比赛', '运动员', '娱乐', '明星', '综艺',
    '事故', '犯罪', '纠纷', '食品', '服装', '日用品'
]


# ==================== 核心数据结构 ====================

@dataclass
class TopicItem:
    """选题项"""
    title: str
    platform: str
    rank: int
    hot_score: float = 0.0
    ai_score: float = 0.0
    quality_score: int = 0  # 质量评分
    final_score: float = 0.0  # 综合评分
    priority: str = 'P1'  # P0/P1/P2
    link: str = ''
    description: str = ''
    matched_ai_keywords: List[str] = field(default_factory=list)
    matched_positive_rules: List[str] = field(default_factory=list)
    matched_negative_rules: List[str] = field(default_factory=list)
    is_ai_related: bool = True
    
    def to_dict(self) -> Dict:
        return {
            'title': self.title,
            'platform': self.platform,
            'rank': self.rank,
            'hot_score': self.hot_score,
            'ai_score': self.ai_score,
            'quality_score': self.quality_score,
            'final_score': self.final_score,
            'priority': self.priority,
            'link': self.link,
            'description': self.description,
            'matched_ai_keywords': self.matched_ai_keywords,
            'matched_positive_rules': self.matched_positive_rules,
            'matched_negative_rules': self.matched_negative_rules,
            'is_ai_related': self.is_ai_related,
        }


# ==================== AI 筛选器 ====================

class AIFilter:
    """AI 话题筛选器"""
    
    def __init__(self):
        self.ai_keywords = AI_KEYWORDS
        self.non_ai_keywords = NON_AI_KEYWORDS
    
    def is_ai_related(self, title: str, description: str = '') -> Tuple[bool, List[str]]:
        """
        判断是否为 AI/科技相关话题
        
        Returns:
            (is_ai_related, matched_keywords)
        """
        text = (title + ' ' + description).lower()
        
        # 先检查非 AI 关键词（排除）
        for kw in self.non_ai_keywords:
            if kw.lower() in text:
                return False, []
        
        # 检查 AI 关键词
        matched = []
        for category, keywords in self.ai_keywords.items():
            for kw in keywords:
                if kw.lower() in text:
                    matched.append(kw)
        
        is_ai = len(matched) > 0
        return is_ai, list(set(matched))
    
    def filter_topics(self, items: List[Dict]) -> List[Dict]:
        """筛选 AI 相关话题"""
        filtered = []
        for item in items:
            is_ai, matched = self.is_ai_related(
                item.get('title', ''),
                item.get('description', '')
            )
            if is_ai:
                item['_ai_matched'] = matched
                item['_is_ai_related'] = True
                filtered.append(item)
        return filtered


# ==================== 质量评分器 ====================

class QualityScorer:
    """质量评分器"""
    
    def __init__(self):
        self.positive_rules = POSITIVE_RULES
        self.negative_rules = NEGATIVE_RULES
    
    def score(self, title: str) -> Tuple[int, List[str], List[str]]:
        """
        计算质量评分
        
        Returns:
            (quality_score, matched_positive, matched_negative)
        """
        score = 0
        matched_positive = []
        matched_negative = []
        
        # 检查正面规则（加分）
        for rule in self.positive_rules:
            for kw in rule.keywords:
                if kw in title:
                    score += rule.score_delta
                    matched_positive.append(rule.description)
                    break  # 每个规则只加一次
        
        # 检查负面规则（减分）
        for rule in self.negative_rules:
            for kw in rule.keywords:
                if kw in title:
                    score += rule.score_delta
                    matched_negative.append(rule.description)
                    break  # 每个规则只减一次
        
        # 检查是否有具体数字（加分）
        if re.search(r'\d+', title):
            score += 5
            if '具体数字' not in matched_positive:
                matched_positive.append('具体数字')
        
        return score, matched_positive, matched_negative


# ==================== 排序器 ====================

class TopicRanker:
    """选题排序器"""
    
    def __init__(self, platform_weights: Dict[str, float] = None):
        # 默认权重（MEMORY.md 标准）
        self.platform_weights = platform_weights or {
            'zhihu': 0.50,      # 50%
            'weibo': 0.15,      # 15%
            'baidu': 0.05,      # 5%
            'hackernews': 0.20, # 20%
            'github': 0.10,     # 10%
            'v2ex': 0.10,       # 10%
            'douyin': 0.20,     # 20% (P1)
        }
    
    def calculate_final_score(self, topic: TopicItem) -> float:
        """
        计算综合评分
        
        final_score = ai_score * 0.4 + quality_score/10 * 0.3 + platform_weight * 0.2 + hot_score_norm * 0.1
        """
        # AI 相关性评分（40%）
        ai_component = topic.ai_score * 0.4
        
        # 质量评分（30%）- 归一化到 0-1
        quality_component = (min(topic.quality_score, 30) / 30) * 0.3
        
        # 平台权重（20%）
        platform_weight = self.platform_weights.get(topic.platform, 0.1)
        platform_component = platform_weight * 0.2
        
        # 热度评分（10%）- 归一化
        hot_component = min(topic.hot_score / 100, 1.0) * 0.1 if topic.hot_score else 0.05
        
        final_score = ai_component + quality_component + platform_component + hot_component
        
        # 优先级调整
        if topic.priority == 'P0':
            final_score += 0.1
        elif topic.priority == 'P2':
            final_score -= 0.1
        
        return final_score
    
    def rank(self, topics: List[TopicItem]) -> List[TopicItem]:
        """排序选题"""
        for topic in topics:
            topic.final_score = self.calculate_final_score(topic)
        
        # 按 final_score 降序排序
        return sorted(topics, key=lambda x: x.final_score, reverse=True)


# ==================== 选题池生成器 ====================

class TopicPoolWriter:
    """选题池生成器"""
    
    def __init__(self, output_dir: str = '../workspace-shared/topics'):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def write_markdown(self, topics: List[TopicItem], output_path: str, 
                       timestamp: str = None, mode: str = 'morning') -> str:
        """
        写入 Markdown 选题池
        
        格式：
        # 选题池 - 2026-03-28 08:30
        
        ## P0 选题（TOP 20）
        1. [标题](链接) - 知乎 (AI 评分：0.85, 质量：+15)
        2. ...
        
        ## P1 选题（TOP 30）
        ...
        
        ## 数据汇总
        - 总抓取：140 条
        - AI 相关：85 条
        - P0 选题：20 条
        - P1 选题：30 条
        """
        if not timestamp:
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M')
        
        # 按优先级分组
        p0_topics = [t for t in topics if t.priority == 'P0'][:20]
        p1_topics = [t for t in topics if t.priority == 'P1'][:30]
        p2_topics = [t for t in topics if t.priority == 'P2'][:10]
        
        md_lines = [
            f'# 选题池 - {timestamp}',
            '',
            f'**生成时间**: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}',
            f'**模式**: {mode}',
            '',
            '---',
            '',
        ]
        
        # P0 选题
        if p0_topics:
            md_lines.append('## 🔥 P0 选题（TOP 20）')
            md_lines.append('')
            for i, topic in enumerate(p0_topics, 1):
                link_md = f'[{topic.title}]({topic.link})' if topic.link else topic.title
                ai_score = f'{topic.ai_score:.2f}'
                quality = f'+{topic.quality_score}' if topic.quality_score > 0 else f'{topic.quality_score}'
                md_lines.append(f'{i}. {link_md} - **{topic.platform}** (AI: {ai_score}, 质量：{quality})')
                if topic.matched_positive_rules:
                    md_lines.append(f'   - ✅ {", ".join(topic.matched_positive_rules)}')
                if topic.matched_negative_rules:
                    md_lines.append(f'   - ❌ {", ".join(topic.matched_negative_rules)}')
            md_lines.append('')
        
        # P1 选题
        if p1_topics:
            md_lines.append('## 📌 P1 选题（TOP 30）')
            md_lines.append('')
            for i, topic in enumerate(p1_topics, 1):
                link_md = f'[{topic.title}]({topic.link})' if topic.link else topic.title
                md_lines.append(f'{i}. {link_md} - **{topic.platform}** (AI: {topic.ai_score:.2f}, 质量：{topic.quality_score})')
            md_lines.append('')
        
        # P2 选题（观察）
        if p2_topics:
            md_lines.append('## 👀 P2 选题（观察）')
            md_lines.append('')
            for i, topic in enumerate(p2_topics, 1):
                link_md = f'[{topic.title}]({topic.link})' if topic.link else topic.title
                md_lines.append(f'{i}. {link_md} - **{topic.platform}**')
            md_lines.append('')
        
        # 数据汇总
        md_lines.append('---')
        md_lines.append('')
        md_lines.append('## 📊 数据汇总')
        md_lines.append('')
        md_lines.append(f'- **总抓取**: {len(topics)} 条')
        md_lines.append(f'- **P0 选题**: {len(p0_topics)} 条')
        md_lines.append(f'- **P1 选题**: {len(p1_topics)} 条')
        md_lines.append(f'- **P2 选题**: {len(p2_topics)} 条')
        
        # 平台分布
        platform_dist = {}
        for topic in topics:
            platform_dist[topic.platform] = platform_dist.get(topic.platform, 0) + 1
        
        md_lines.append('')
        md_lines.append('### 平台分布')
        for platform, count in sorted(platform_dist.items(), key=lambda x: x[1], reverse=True):
            md_lines.append(f'- {platform}: {count} 条')
        
        # 写入文件
        content = '\n'.join(md_lines)
        output_path_obj = Path(output_path)
        if output_path_obj.is_absolute():
            output_file = output_path_obj
        else:
            # 相对路径：确保父目录存在
            output_file = Path(output_path).resolve()
        output_file.parent.mkdir(parents=True, exist_ok=True)
        output_file.write_text(content, encoding='utf-8')
        
        return str(output_file)


# ==================== 管道主类 ====================

class IntelligencePipeline:
    """情报处理管道"""
    
    def __init__(self, output_dir: str = 'tmp'):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        self.grabber = OpenCLIGrabber(output_dir=str(self.output_dir)) if GRABBER_AVAILABLE else None
        self.ai_filter = AIFilter()
        self.quality_scorer = QualityScorer()
        self.ranker = TopicRanker()
        self.pool_writer = TopicPoolWriter()
    
    def grab(self, platforms: List[str], quiet: bool = False) -> Dict:
        """步骤 1: 抓取热点"""
        print(f"\n{'='*60}")
        print(f"[PIPELINE] 步骤 1: 抓取热点")
        print(f"{'='*60}")
        
        if not self.grabber:
            print("❌ Grabber 不可用")
            return {}
        
        result = self.grabber.grab_all(platforms=platforms)
        return result
    
    def analyze(self, input_files: List[str], mode: str = 'morning') -> List[TopicItem]:
        """
        步骤 2: 分析（AI 筛选 + 质量评分 + 排序）
        
        input_files: JSON 文件路径列表（支持 glob）
        """
        print(f"\n{'='*60}")
        print(f"[PIPELINE] 步骤 2: 分析")
        print(f"{'='*60}")
        
        # 1. 读取所有 JSON 文件
        all_items = []
        for file_pattern in input_files:
            # 支持 glob
            from glob import glob
            file_paths = sorted(glob(file_pattern), reverse=True)  # 按文件名排序（最新的在前）
            
            for file_path in file_paths[:10]:  # 最多读 10 个文件
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        platforms_data = data.get('platforms', {})
                        for platform, platform_data in platforms_data.items():
                            items = platform_data.get('items', [])
                            for item in items:
                                item['_source_platform'] = platform
                                all_items.append(item)
                    print(f"  📄 读取：{os.path.basename(file_path)}")
                except PermissionError:
                    print(f"  ⚠️  跳过（文件锁定）: {os.path.basename(file_path)}")
                except Exception as e:
                    print(f"  ⚠️  读取失败 {os.path.basename(file_path)}: {e}")
        
        print(f"📥 读取热点总数：{len(all_items)} 条")
        
        # 2. AI 筛选
        print(f"\n🔍 AI 筛选...")
        ai_items = self.ai_filter.filter_topics(all_items)
        print(f"✅ AI 相关：{len(ai_items)} 条（{len(ai_items)/len(all_items)*100:.1f}%）")
        
        # 3. 转换为 TopicItem 并评分
        print(f"\n📊 质量评分...")
        topics = []
        for item in ai_items:
            title = item.get('title', '')
            platform = item.get('_source_platform', item.get('platform', 'unknown'))
            
            # AI 评分
            ai_score = item.get('_ai_score', 0.5)  # 默认 0.5
            
            # 质量评分
            quality_score, matched_pos, matched_neg = self.quality_scorer.score(title)
            
            topic = TopicItem(
                title=title,
                platform=platform,
                rank=item.get('rank', 999),
                hot_score=float(item.get('hot', item.get('score', 0))),
                ai_score=ai_score,
                quality_score=quality_score,
                priority=item.get('priority', 'P1'),
                link=item.get('link', item.get('url', '')),
                description=item.get('description', ''),
                matched_ai_keywords=item.get('_ai_matched', []),
                matched_positive_rules=matched_pos,
                matched_negative_rules=matched_neg,
            )
            topics.append(topic)
        
        # 4. 排序
        print(f"\n📈 排序...")
        ranked_topics = self.ranker.rank(topics)
        
        # 5. 统计
        p0_count = sum(1 for t in ranked_topics if t.priority == 'P0')
        p1_count = sum(1 for t in ranked_topics if t.priority == 'P1')
        p2_count = sum(1 for t in ranked_topics if t.priority == 'P2')
        
        print(f"\n✅ 分析完成:")
        print(f"   P0: {p0_count} 条")
        print(f"   P1: {p1_count} 条")
        print(f"   P2: {p2_count} 条")
        
        return ranked_topics
    
    def write_pool(self, topics: List[TopicItem], output_path: str, 
                   timestamp: str = None, mode: str = 'morning') -> str:
        """步骤 3: 写选题池"""
        print(f"\n{'='*60}")
        print(f"[PIPELINE] 步骤 3: 写选题池")
        print(f"{'='*60}")
        
        output_file = self.pool_writer.write_markdown(
            topics=topics,
            output_path=output_path,
            timestamp=timestamp,
            mode=mode
        )
        
        print(f"✅ 选题池已写入：{output_file}")
        return output_file
    
    def run_full(self, platforms: List[str], output_pool: str, 
                 mode: str = 'morning', quiet: bool = False) -> Dict:
        """
        运行完整管道（抓取 → 分析 → 写选题池）
        """
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M')
        
        # 步骤 1: 抓取
        grab_result = self.grab(platforms=platforms, quiet=quiet)
        
        # 步骤 2: 分析
        topics = self.analyze(
            input_files=[f"{self.output_dir}/opencli-hotspots-*.json"],
            mode=mode
        )
        
        # 步骤 3: 写选题池
        output_file = self.write_pool(
            topics=topics,
            output_path=output_pool,
            timestamp=timestamp,
            mode=mode
        )
        
        # 返回摘要
        return {
            'grab_result': grab_result,
            'topics_count': len(topics),
            'p0_count': sum(1 for t in topics if t.priority == 'P0'),
            'p1_count': sum(1 for t in topics if t.priority == 'P1'),
            'p2_count': sum(1 for t in topics if t.priority == 'P2'),
            'output_file': output_file,
        }


# ==================== 命令行入口 ====================

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='OpenCLI 情报处理管道 v2.0')
    parser.add_argument('--grab', action='store_true', help='只抓取')
    parser.add_argument('--analyze', action='store_true', help='只分析')
    parser.add_argument('--full', action='store_true', help='完整管道（抓取 + 分析 + 写选题池）')
    parser.add_argument('--platforms', '-p', nargs='+', 
                        default=['zhihu', 'weibo', 'baidu', 'hackernews'],
                        help='平台列表')
    parser.add_argument('--output', '-o', default='tmp', help='抓取输出目录')
    parser.add_argument('--output-pool', default='topics-pool.md', help='选题池输出路径')
    parser.add_argument('--input', '-i', nargs='+', help='分析模式的输入文件（JSON）')
    parser.add_argument('--mode', default='morning', choices=['morning', 'afternoon', 'night'],
                        help='分析模式')
    parser.add_argument('--quiet', '-q', action='store_true', help='安静模式')
    
    args = parser.parse_args()
    
    pipeline = IntelligencePipeline(output_dir=args.output)
    
    if args.grab:
        result = pipeline.grab(platforms=args.platforms, quiet=args.quiet)
        print(f"\n抓取完成：{result.get('summary', {}).get('total', 0)} 条")
    
    elif args.analyze:
        if not args.input:
            print("❌ 分析模式需要 --input 参数")
            sys.exit(1)
        topics = pipeline.analyze(input_files=args.input, mode=args.mode)
        output_file = pipeline.write_pool(topics, args.output_pool, mode=args.mode)
        print(f"\n分析完成：输出 {output_file}")
    
    elif args.full:
        result = pipeline.run_full(
            platforms=args.platforms,
            output_pool=args.output_pool,
            mode=args.mode,
            quiet=args.quiet
        )
        print(f"\n完整管道完成:")
        print(f"  抓取：{result['grab_result'].get('summary', {}).get('total', 0)} 条")
        print(f"  选题：{result['topics_count']} 条（P0: {result['p0_count']}, P1: {result['p1_count']}）")
        print(f"  输出：{result['output_file']}")
    
    else:
        parser.print_help()
        sys.exit(1)
    
    return 0


if __name__ == '__main__':
    sys.exit(main())
