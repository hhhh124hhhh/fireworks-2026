"""
工作流追踪模块

追踪和记录工作流相关信息
"""

from datetime import datetime
from typing import Dict, List, Optional
from .data_store import DataStore


class WorkflowTracker:
    """工作流追踪器"""

    def __init__(self, data_store: Optional[DataStore] = None):
        """
        初始化工作流追踪器

        Args:
            data_store: 数据存储实例
        """
        self.data_store = data_store or DataStore()
        self._init_workflows()

    def _init_workflows(self):
        """初始化工作流数据"""
        workflows = self.data_store.get_workflows()
        if not workflows:
            # 初始化一些预定义的工作流类型
            predefined = {
                'general': {
                    'name': '通用任务',
                    'description': '常规工作流任务',
                    'completion_count': 0,
                    'cron_runs': 0,
                    'last_used': None
                },
                'automation': {
                    'name': '自动化任务',
                    'description': '自动化脚本执行',
                    'completion_count': 0,
                    'cron_runs': 0,
                    'last_used': None
                },
                'coding': {
                    'name': '编程任务',
                    'description': '编程和代码相关任务',
                    'completion_count': 0,
                    'cron_runs': 0,
                    'last_used': None
                },
                'data_processing': {
                    'name': '数据处理',
                    'description': '数据处理和分析',
                    'completion_count': 0,
                    'cron_runs': 0,
                    'last_used': None
                }
            }

            for wf_id, wf_data in predefined.items():
                self.data_store.save_workflow(wf_id, wf_data)

    def start_workflow(self, workflow_type: str, name: Optional[str] = None) -> str:
        """
        启动一个新的工作流

        Args:
            workflow_type: 工作流类型
            name: 工作流名称（可选）

        Returns:
            工作流实例ID
        """
        workflow_id = f"{workflow_type}_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}"

        workflows = self.data_store.get_workflows()

        if workflow_type not in workflows:
            workflows[workflow_type] = {
                'name': name or workflow_type,
                'description': f'{name or workflow_type} 工作流',
                'completion_count': 0,
                'cron_runs': 0,
                'last_used': None
            }
            self.data_store.save_workflow(workflow_type, workflows[workflow_type])

        return workflow_id

    def complete_workflow(self, workflow_id: str, success: bool = True) -> bool:
        """
        完成工作流

        Args:
            workflow_id: 工作流ID
            success: 是否成功

        Returns:
            是否保存成功
        """
        workflows = self.data_store.get_workflows()

        # 提取工作流类型（去掉时间戳）
        workflow_type = workflow_id.rsplit('_', 2)[0]

        if workflow_type in workflows:
            workflows[workflow_type]['completion_count'] += 1
            workflows[workflow_type]['last_used'] = datetime.now().isoformat()
            return self.data_store.save_workflow(workflow_type, workflows[workflow_type])

        return False

    def track_cron_execution(self, workflow_type: str) -> bool:
        """
        记录 cron 任务执行

        Args:
            workflow_type: 工作流类型

        Returns:
            是否保存成功
        """
        workflows = self.data_store.get_workflows()

        if workflow_type not in workflows:
            workflows[workflow_type] = {
                'name': workflow_type,
                'description': 'Cron 任务',
                'completion_count': 0,
                'cron_runs': 0,
                'last_used': None
            }

        workflows[workflow_type]['cron_runs'] += 1
        workflows[workflow_type]['last_used'] = datetime.now().isoformat()

        return self.data_store.save_workflow(workflow_type, workflows[workflow_type])

    def record_time_saved(self, minutes: int) -> bool:
        """
        记录通过自动化节省的时间

        Args:
            minutes: 节省的分钟数

        Returns:
            是否保存成功
        """
        return self.data_store.increment_metric('time_saved_minutes', minutes)

    def record_problem_solved(self) -> bool:
        """
        记录成功解决的问题

        Returns:
            是否保存成功
        """
        return self.data_store.increment_metric('problems_solved', 1)

    def track_subagent_task(self, created: bool = False, completed: bool = False) -> bool:
        """
        记录子代理任务

        Args:
            created: 是否创建子代理
            completed: 是否完成任务

        Returns:
            是否保存成功
        """
        if created:
            self.data_store.increment_metric('subagent_created', 1)
        if completed:
            self.data_store.increment_metric('subagent_completed', 1)

        return True

    def get_workflow_stats(self) -> Dict:
        """
        获取工作流统计信息

        Returns:
            统计信息字典
        """
        workflows = self.data_store.get_workflows()

        total_completions = sum(w.get('completion_count', 0) for w in workflows.values())
        total_cron_runs = sum(w.get('cron_runs', 0) for w in workflows.values())

        # 按类型统计
        by_type = {}
        for wf_id, data in workflows.items():
            by_type[wf_id] = {
                'name': data.get('name'),
                'completions': data.get('completion_count', 0),
                'cron_runs': data.get('cron_runs', 0),
                'last_used': data.get('last_used')
            }

        # 最常用的工作流
        top_workflows = sorted(
            by_type.items(),
            key=lambda x: x[1]['completions'],
            reverse=True
        )[:5]

        return {
            'total_completions': total_completions,
            'total_cron_runs': total_cron_runs,
            'by_type': by_type,
            'top_workflows': top_workflows
        }

    def get_workflow_history(self, limit: int = 10) -> List[Dict]:
        """
        获取工作流历史记录

        Args:
            limit: 返回数量

        Returns:
            历史记录列表
        """
        workflows = self.data_store.get_workflows()

        # 按最后使用时间排序
        history = []
        for wf_id, data in workflows.items():
            if data.get('last_used'):
                history.append({
                    'id': wf_id,
                    'name': data.get('name'),
                    'completions': data.get('completion_count', 0),
                    'cron_runs': data.get('cron_runs', 0),
                    'last_used': data.get('last_used')
                })

        history.sort(key=lambda x: x['last_used'], reverse=True)
        return history[:limit]
