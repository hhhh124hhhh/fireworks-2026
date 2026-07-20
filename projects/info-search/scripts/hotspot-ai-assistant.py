#!/usr/bin/env python3
"""
AI 摘要和热度评估助手
使用 Claude API 生成摘要和创作建议（优化版）
"""

import sys
import json
import urllib.request
import urllib.error
import subprocess
import re
from typing import Dict, Optional, List

# Claude API 配置（需要配置）
ANTHROPIC_API_KEY = ""  # 在这里配置 API Key，或者从环境变量读取

# 如果没有配置，尝试从环境变量读取
if not ANTHROPIC_API_KEY:
    import os
    ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")

def fetch_url_content(url: str, max_chars: int = 5000) -> str:
    """获取 URL 内容（使用 BeautifulSoup 清理 HTML）"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=15) as response:
            content = response.read().decode('utf-8', errors='ignore')
            
            # 尝试使用 BeautifulSoup 清理 HTML
            try:
                from bs4 import BeautifulSoup
                
                soup = BeautifulSoup(content, 'html.parser')
                
                # 移除不需要的标签
                for tag in soup(['script', 'style', 'nav', 'header', 'footer', 'aside', 'noscript']):
                    tag.decompose()
                
                # 移除带有特定 class 的元素
                for tag in soup.find_all(class_=re.compile(r'(nav|menu|sidebar|footer|header|cookie|ad|advertisement)', re.I)):
                    tag.decompose()
                
                # 提取主要文本
                main_content = soup.get_text(separator=' ', strip=True)
                
                # 清理多余的空白
                main_content = re.sub(r'\s+', ' ', main_content).strip()
                
                return main_content[:max_chars]
                
            except ImportError:
                # 如果没有 BeautifulSoup，使用简单清理
                content = re.sub(r'<script[^>]*>.*?</script>', '', content, flags=re.DOTALL)
                content = re.sub(r'<style[^>]*>.*?</style>', '', content, flags=re.DOTALL)
                content = re.sub(r'<(script|style|nav|header|footer|aside)[^>]*>.*?</\1>', '', content, flags=re.DOTALL)
                content = re.sub(r'<[^>]+>', ' ', content)
                content = content.strip()
                content = re.sub(r'\s+', ' ', content)
                return content[:max_chars]
            
    except Exception as e:
        return ""

def analyze_content_direction(title: str, score: int) -> str:
    """基于标题和分数分析内容方向"""
    title_lower = title.lower()
    
    # 关键词匹配（按优先级排序）
    
    # 1. 趋势分析（最高优先级）
    trend_keywords = [
        'trend', 'future', 'prediction', 'forecast', 'outlook',
        'impact', 'effect', 'influence', 'shift', 'revolution',
        'shortage', 'crisis', 'boom', 'surge', 'wave',
        'programming language', 'high level language', 'evolution', 'paradigm'
    ]
    if any(k in title_lower for k in trend_keywords):
        return "AI 行业趋势分析"
    
    # 2. 开源项目
    if 'show hn:' in title_lower or 'show hn ：' in title_lower:
        return "开源 AI 项目深度解析"
    
    # 3. AI 工具使用技巧与攻略（新增）
    trick_keywords = [
        'fast mode', 'speed up', 'optimize', 'improve', 'boost',
        'hack', 'trick', 'tip', 'guide', 'how to', 'best practice',
        'tutorial', 'learn', 'master', 'mastering', 'effective'
    ]
    if any(k in title_lower for k in trick_keywords):
        return "AI 工具使用技巧与攻略"
    
    # 4. AI 产品/平台介绍（新增）
    product_keywords = [
        'software factory', 'platform', 'service', 'tool', 'app', 'application',
        'assistant', 'agent', 'bot', 'automation', 'workflow',
        'release', 'launch', 'announce', 'update', 'new'
    ]
    if any(k in title_lower for k in product_keywords):
        if score > 100:
            return "AI 产品/平台深度评测"
        else:
            return "AI 产品/功能介绍"
    
    # 5. AI 编程/开发实战（新增）
    dev_keywords = [
        'api', 'integration', 'development', 'programming', 'coding',
        'code', 'implementation', 'architecture', 'engineer',
        'build', 'create', 'deploy'
    ]
    if any(k in title_lower for k in dev_keywords):
        return "AI 编程/开发实战"
    
    # 6. 教程
    elif any(k in title_lower for k in ['tutorial', 'guide', 'how to', 'learn', 'beginner']):
        return "AI 技术教程"
    
    # 7. 对比
    elif any(k in title_lower for k in ['compare', 'vs', 'versus', 'difference', 'better']):
        return "AI 工具横向对比"
    
    # 8. 工具合集
    elif any(k in title_lower for k in ['best', 'top', 'list', 'collection', 'awesome']):
        return "AI 工具合集推荐"
    
    # 9. 其他开源项目
    elif any(k in title_lower for k in ['open source', 'github', 'source code']):
        return "开源 AI 项目深度解析"
    
    # 10. 默认
    else:
        return "AI 相关内容创作"

def extract_product_name(title: str) -> str:
    """从标题中提取产品名称"""
    title_lower = title.lower()
    
    # 尝试从不同位置提取产品名称
    
    # 1. 查找 "Show HN:" 或 "Show HN ：" 之后的内容
    if 'show hn:' in title_lower or 'show hn ：' in title_lower:
        parts = re.split(r'[：:]', title, 1)
        if len(parts) > 1:
            return parts[1].strip()
    
    # 2. 查找 "-" 分隔的产品名称
    if '-' in title:
        # 取第一部分（更可能是产品名称）
        return title.split('-')[0].strip()
    
    # 3. 查找冒号后的内容
    if '：' in title or ':' in title:
        parts = re.split(r'[：:]', title, 1)
        if len(parts) > 1:
            name_part = parts[1].strip()
            # 移除前缀（如 "Rust中"）
            name_part = re.sub(r'^(本地|第一个|具有|等)\s*', '', name_part)
            if name_part:
                return name_part
    
    # 4. 返回原始标题作为回退
    return title

def generate_suggestions(title: str, content_direction: str) -> List[str]:
    """基于标题和内容方向生成具体的创作建议（使用中文标题）"""
    title_lower = title.lower()
    keywords = re.findall(r'\b[a-zA-Z]{4,}\b', title)
    
    # 提取产品名称
    product_name = extract_product_name(title)
    
    suggestions = []
    
    # 根据内容方向生成不同类型的建议
    if content_direction == "开源 AI 项目深度解析":
        # 开源项目：技术深度、实战教程、应用场景
        product_name = title.split('-')[-1].strip() if '-' in title else "这个项目"
        
        suggestions.append(
            f"技术深度：{product_name} vs 竞品对比分析（性能、功能、易用性、生态支持）"
        )
        suggestions.append(
            f"实战教程：使用 {product_name} 搭建个人 AI 系统（环境配置、核心功能、常见问题）"
        )
        suggestions.append(
            f"应用场景：{product_name} 在 3 个实际场景中的应用（笔记整理、代码助手、知识问答）"
        )
        
    elif content_direction == "新发布 AI 工具评测与试用":
        # 新工具：完整测评、对比分析、试用报告
        product_name = title.split('-')[-1].strip() if '-' in title else "这个工具"
        
        suggestions.append(
            f"深度评测：{product_name} 完整测评报告（核心功能、优缺点、适用场景、价格）"
        )
        suggestions.append(
            f"对比分析：{product_name} vs 同类工具的详细对比（5 个维度、推荐场景）"
        )
        suggestions.append(
            f"试用报告：使用 {product_name} 7 天的真实体验（上手难度、实际效果、值得付费吗）"
        )
        
    elif content_direction == "AI 技术教程":
        # 教程：入门教程、进阶技巧、最佳实践
        topic = title.split('-')[-1].strip() if '-' in title else "这个技术"
        
        suggestions.append(
            f"入门教程：{topic} 新手完全指南（零基础到第一篇作品，附代码示例）"
        )
        suggestions.append(
            f"进阶技巧：{topic} 10 个高级技巧（提升效率、优化性能、避免坑）"
        )
        suggestions.append(
            f"最佳实践：{topic} 项目最佳实践（架构设计、代码规范、性能优化）"
        )
        
    elif content_direction == "AI 工具横向对比":
        # 对比：功能对比、性能测试、选择指南
        topic = title.split('-')[-1].strip() if '-' in title else "这些工具"
        
        suggestions.append(
            f"功能对比：{topic} 功能详细对比（功能清单、差异化亮点、适用场景）"
        )
        suggestions.append(
            f"性能测试：{topic} 性能横向评测（速度、准确性、资源占用、稳定性）"
        )
        suggestions.append(
            f"选择指南：如何选择合适的 {topic}（决策矩阵、使用场景、成本分析）"
        )
        
    elif content_direction == "AI 行业趋势分析":
        # 趋势：数据解读、行业影响、未来预测
        topic = title.split('-')[-1].strip() if '-' in title else "这个趋势"
        
        suggestions.append(
            f"数据解读：{topic} 背后的数据支撑（市场规模、增长趋势、关键指标）"
        )
        suggestions.append(
            f"行业影响：{topic} 对 3 个行业的具体影响（变革点、机遇、挑战）"
        )
        suggestions.append(
            f"未来预测：{topic} 未来 3 年发展趋势（技术演进、市场格局、投资机会）"
        )
        
    elif content_direction == "AI 工具合集推荐":
        # 合集：精选推荐、分类整理、使用场景
        topic = title.split('-')[-1].strip() if '-' in title else "这些工具"
        
        suggestions.append(
            f"精选推荐：2024 年 {topic} 工具 Top 10（功能亮点、适用人群、下载链接）"
        )
        suggestions.append(
            f"分类整理：{topic} 工具按场景分类（开发、设计、测试、部署）"
        )
        suggestions.append(
            f"使用场景：{topic} 工具在不同项目中的应用（案例、效果、成本）"
        )
        
    elif content_direction == "AI 使用技巧与优化":
        # 技巧：技巧总结、性能优化、常见问题
        topic = title.split('-')[-1].strip() if '-' in title else "这些技巧"
        
        suggestions.append(
            f"技巧总结：{topic} 20 个实用技巧（提高效率、节省时间、避免坑）"
        )
        suggestions.append(
            f"性能优化：{topic} 性能优化指南（瓶颈分析、优化方法、效果对比）"
        )
        suggestions.append(
            f"常见问题：{topic} 10 个常见问题及解决方案（错误分析、修复方法、预防措施）"
        )
        
    elif content_direction == "AI 开发实战":
        # 开发：实战教程、代码示例、最佳实践
        topic = title.split('-')[-1].strip() if '-' in title else "这个技术"
        
        suggestions.append(
            f"实战教程：从 0 到 1 构建 {topic} 应用（架构设计、代码实现、部署上线）"
        )
        suggestions.append(
            f"代码示例：{topic} 开发代码示例大全（常见功能、最佳实践、坑点提示）"
        )
        suggestions.append(
            f"最佳实践：{topic} 开发最佳实践（代码规范、架构设计、性能优化）"
        )
        
    elif content_direction == "新产品/功能介绍":
        # 产品：功能介绍、使用指南、应用场景
        product_name = title.split('-')[-1].strip() if '-' in title else "这个产品"
        
        suggestions.append(
            f"功能介绍：{product_name} 核心功能详解（功能清单、使用场景、价值点）"
        )
        suggestions.append(
            f"使用指南：{product_name} 使用完全指南（注册、配置、使用、技巧）"
        )
        suggestions.append(
            f"应用场景：{product_name} 在实际工作中的应用（案例、效果、ROI）"
        )
        
    elif content_direction == "AI 工具使用技巧与攻略":
        # 技巧：使用技巧、优化方法、实战攻略
        tool_name = title.split('-')[-1].strip() if '-' in title else "这个工具"
        
        suggestions.append(
            f"使用技巧：{tool_name} 的 10 个实用技巧（提高效率、节省时间、避免坑）"
        )
        suggestions.append(
            f"优化方法：{tool_name} 性能优化全攻略（设置优化、工作流优化、高级技巧）"
        )
        suggestions.append(
            f"实战攻略：{tool_name} 实战应用攻略（新手到高手，附案例和模板）"
        )
        
    elif content_direction == "AI 产品/平台深度评测":
        # 产品评测：完整评测、对比分析、试用报告
        product_name = title.split('-')[-1].strip() if '-' in title else "这个产品"
        
        suggestions.append(
            f"深度评测：{product_name} 完整测评报告（核心功能、优缺点、适用场景、价格）"
        )
        suggestions.append(
            f"对比分析：{product_name} vs 同类产品的详细对比（5 个维度、推荐场景）"
        )
        suggestions.append(
            f"试用报告：使用 {product_name} 的真实体验（上手难度、实际效果、值得付费吗）"
        )
        
    elif content_direction == "AI 编程/开发实战":
        # 开发：实战教程、代码示例、最佳实践
        topic = title.split('-')[-1].strip() if '-' in title else "这个技术"
        
        suggestions.append(
            f"实战教程：从 0 到 1 构建 {topic} 应用（架构设计、代码实现、部署上线）"
        )
        suggestions.append(
            f"代码示例：{topic} 开发代码示例大全（常见功能、最佳实践、坑点提示）"
        )
        suggestions.append(
            f"最佳实践：{topic} 开发最佳实践（代码规范、架构设计、性能优化）"
        )
        
    else:
        # 通用建议
        suggestions.append(f"{title} 深度解读（背景、技术、影响）")
        suggestions.append(f"{title} 实战应用（场景、方法、效果）")
        suggestions.append(f"{title} 未来展望（趋势、机会、挑战）")
    
    return suggestions[:3]  # 返回前 3 个建议

def evaluate_difficulty(title: str, score: int) -> str:
    """评估创作难度"""
    # 基于分数和关键词
    if any(k in title.lower() for k in ['api', 'code', 'programming', 'development', 'software factory', 'architecture']):
        return "⭐⭐⭐"
    elif any(k in title.lower() for k in ['fast mode', 'optimize', 'improve', 'boost', 'hack', 'trick']):
        return "⭐"
    elif score > 150:
        return "⭐⭐"
    elif any(k in title.lower() for k in ['tutorial', 'guide', 'beginner']):
        return "⭐"
    else:
        return "⭐⭐"

def determine_target_audience(title: str) -> str:
    """确定目标受众"""
    title_lower = title.lower()
    
    if any(k in title_lower for k in ['api', 'code', 'programming', 'development', 'software factory', 'architecture', 'rust', 'python', 'go']):
        return "AI 开发者和工程师"
    elif any(k in title_lower for k in ['business', 'enterprise', 'company', 'startup', 'platform', 'service']):
        return "企业决策者和产品经理"
    elif any(k in title_lower for k in ['tutorial', 'guide', 'beginner', 'learn', 'how to', 'fast mode', 'optimize', 'improve']):
        return "AI 初学者和爱好者"
    else:
        return "AI 爱好者和从业者"

def generate_summary_and_suggestions(
    title: str,
    url: str,
    score: int,
    content: Optional[str] = None,
    translated_title: Optional[str] = None
) -> Dict:
    """
    生成摘要和创作建议（优化版）
    
    Args:
        title: 热点标题
        url: 热点链接
        score: Hacker News 分数
        content: 可选的网页内容
        translated_title: 翻译后的中文标题
    
    Returns:
        包含摘要和创作建议的字典
    """
    
    # 如果没有提供内容，尝试获取
    if content is None or content.startswith("无法获取") or content == "":
        content = fetch_url_content(url)
    
    # 评估热度等级
    heat_level = "一般热度"
    if score >= 200:
        heat_level = "超级热门"
    elif score >= 100:
        heat_level = "非常热门"
    elif score >= 50:
        heat_level = "热门"
    
    # 使用中文标题（如果有）
    display_title = translated_title if translated_title else title
    
    # 分析内容方向
    content_direction = analyze_content_direction(title, score)
    
    # 生成创作建议（使用中文标题）
    suggestions = generate_suggestions(display_title, content_direction)
    
    # 评估难度
    difficulty = evaluate_difficulty(title, score)
    
    # 确定目标受众
    target_audience = determine_target_audience(title)
    
    # 生成摘要
    if content and len(content) > 100:
        # 提取前 200 个字符作为摘要
        summary = content[:200] + "..." if len(content) > 200 else content
    else:
        summary = f"这是一个关于{content_direction}的热点话题，访问链接查看详情。"
    
    # 如果没有配置 API Key，返回基于模板的建议
    if not ANTHROPIC_API_KEY:
        return {
            "summary": summary,
            "content_direction": content_direction,
            "suggestions": suggestions,
            "target_audience": target_audience,
            "difficulty": difficulty
        }

    try:
        # 调用 Claude API
        import http.client
        import ssl
        
        headers = {
            'x-api-key': ANTHROPIC_API_KEY,
            'Content-Type': 'application/json',
            'anthropic-version': '2023-06-01'
        }
        
        # 清理内容（移除多余的空白）
        if content:
            content = ' '.join(content.split())
        
        prompt = f"""你是一个自媒体内容创作助手。请基于以下信息生成内容摘要和创作建议。

**热点信息**:
- 标题: {display_title}
- 链接: {url}
- 热度分数: {score}
- 热度等级: {heat_level}

**网页内容摘要**:
{content[:2000] if len(content) > 2000 else content}

请按以下格式输出（JSON）:
{{
    "summary": "用 2-3 句话总结这个热点的主要内容",
    "content_direction": "{content_direction}",
    "suggestions": {json.dumps(suggestions, ensure_ascii=False)},
    "target_audience": "{target_audience}",
    "difficulty": "{difficulty}"
}}

请只输出 JSON，不要有其他内容。"""
        
        data = {
            "model": "claude-3-haiku-20240307",
            "max_tokens": 1000,
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        }
        
        conn = http.client.HTTPSConnection("api.anthropic.com", context=ssl.create_default_context())
        conn.request("POST", "/v1/messages", json.dumps(data), headers)
        
        response = conn.getresponse()
        response_data = response.read().decode('utf-8')
        result = json.loads(response_data)
        
        if response.status == 200:
            content_text = result['content'][0]['text']
            # 尝试解析 JSON
            try:
                # 提取 JSON 部分（可能在 markdown 代码块中）
                json_match = re.search(r'\{[\s\S]*?\}', content_text)
                if json_match:
                    json_str = json_match.group()
                    suggestions = json.loads(json_str)
                    return suggestions
                else:
                    # 如果没有找到 JSON，返回基于模板的建议
                    return {
                        "summary": content_text[:300],
                        "content_direction": content_direction,
                        "suggestions": suggestions,
                        "target_audience": target_audience,
                        "difficulty": difficulty
                    }
            except json.JSONDecodeError:
                # 如果 JSON 解析失败，返回基于模板的建议
                return {
                    "summary": content_text[:300],
                    "content_direction": content_direction,
                    "suggestions": suggestions,
                    "target_audience": target_audience,
                    "difficulty": difficulty
                }
        else:
            # API 调用失败，返回基于模板的建议
            return {
                "summary": summary,
                "content_direction": content_direction,
                "suggestions": suggestions,
                "target_audience": target_audience,
                "difficulty": difficulty
            }
            
    except Exception as e:
        # 发生错误，返回基于模板的建议
        return {
            "summary": summary,
            "content_direction": content_direction,
            "suggestions": suggestions,
            "target_audience": target_audience,
            "difficulty": difficulty
        }

def main():
    """主函数"""
    if len(sys.argv) < 5:
        print("用法: python3 hotspot-ai-assistant.py <title> <url> <score> <translated_title> [content]")
        print("输出: JSON 格式的摘要和创作建议")
        return

    title = sys.argv[1]
    url = sys.argv[2]
    score = int(sys.argv[3])
    translated_title = sys.argv[4] if len(sys.argv) > 4 else None
    content = sys.argv[5] if len(sys.argv) > 5 else None

    result = generate_summary_and_suggestions(title, url, score, content, translated_title)
    # 输出为单行 JSON，便于 bash 处理
    print(json.dumps(result, ensure_ascii=False, separators=(',', ':')))

if __name__ == "__main__":
    main()
