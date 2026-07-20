"""
数据存储模块

提供 JSON 文件持久化功能
"""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional
import fcntl


class DataStore:
    """线程安全的数据存储类"""

    def __init__(self, base_dir: Optional[Path] = None):
        """
        初始化数据存储

        Args:
            base_dir: 基础目录，默认为项目目录下的 data
        """
        if base_dir is None:
            base_dir = Path(__file__).parent.parent.parent / "data"

        self.base_dir = Path(base_dir)
        self.base_dir.mkdir(parents=True, exist_ok=True)

        # 数据文件路径
        self.activities_file = self.base_dir / "activities.json"
        self.achievements_file = self.base_dir / "achievements.json"
        self.workflows_file = self.base_dir / "workflows.json"
        self.metrics_file = self.base_dir / "metrics.json"
        self.user_profile_file = self.base_dir / "user_profile.json"

        # 确保数据文件存在
        self._init_files()

    def _init_files(self):
        """初始化所有数据文件"""
        files = [
            self.activities_file,
            self.achievements_file,
            self.workflows_file,
            self.metrics_file,
            self.user_profile_file,
        ]

        for file in files:
            if not file.exists():
                self._write_json(file, {})

    def _read_json(self, file_path: Path) -> Any:
        """安全读取 JSON 文件（带文件锁）"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                fcntl.flock(f, fcntl.LOCK_SH)  # 共享锁
                data = json.load(f)
                fcntl.flock(f, fcntl.LOCK_UN)
                return data
        except (json.JSONDecodeError, FileNotFoundError):
            return {}

    def _write_json(self, file_path: Path, data: Any) -> bool:
        """安全写入 JSON 文件（带文件锁）"""
        try:
            # 创建临时文件
            temp_path = file_path.with_suffix('.tmp')
            with open(temp_path, 'w', encoding='utf-8') as f:
                fcntl.flock(f, fcntl.LOCK_EX)  # 独占锁
                json.dump(data, f, indent=2, ensure_ascii=False)
                fcntl.flock(f, fcntl.LOCK_UN)

            # 原子替换
            temp_path.replace(file_path)
            return True
        except Exception as e:
            print(f"写入文件失败 {file_path}: {e}")
            return False

    # ========== 活动数据 ==========

    def get_activities(self) -> Dict:
        """获取所有活动数据"""
        return self._read_json(self.activities_file)

    def save_activity(self, date: str, activity_data: Dict) -> bool:
        """保存活动数据"""
        activities = self.get_activities()
        if date not in activities:
            activities[date] = {}

        activities[date].update(activity_data)
        return self._write_json(self.activities_file, activities)

    def get_activity_by_date(self, date: str) -> Dict:
        """获取指定日期的活动"""
        activities = self.get_activities()
        return activities.get(date, {})

    def get_activities_in_range(self, start_date: str, end_date: str) -> Dict:
        """获取日期范围内的活动"""
        activities = self.get_activities()
        return {
            date: data for date, data in activities.items()
            if start_date <= date <= end_date
        }

    # ========== 成就数据 ==========

    def get_achievements(self) -> Dict:
        """获取所有成就数据"""
        return self._read_json(self.achievements_file)

    def save_achievement(self, achievement_id: str, data: Dict) -> bool:
        """保存成就数据"""
        achievements = self.get_achievements()
        achievements[achievement_id] = data
        return self._write_json(self.achievements_file, achievements)

    def unlock_achievement(self, achievement_id: str, unlock_time: Optional[str] = None) -> bool:
        """解锁成就"""
        if unlock_time is None:
            unlock_time = datetime.now().isoformat()

        achievements = self.get_achievements()
        if achievement_id not in achievements:
            return False

        if achievements[achievement_id].get('unlocked', False):
            return False  # 已经解锁

        achievements[achievement_id]['unlocked'] = True
        achievements[achievement_id]['unlock_time'] = unlock_time
        achievements[achievement_id]['unlock_count'] = achievements[achievement_id].get('unlock_count', 0) + 1
        return self._write_json(self.achievements_file, achievements)

    def reset_achievements(self) -> bool:
        """重置所有成就"""
        achievements = self.get_achievements()
        for aid in achievements:
            achievements[aid]['unlocked'] = False
            achievements[aid]['unlock_time'] = None
            achievements[aid]['unlock_count'] = 0
        return self._write_json(self.achievements_file, achievements)

    # ========== 工作流数据 ==========

    def get_workflows(self) -> Dict:
        """获取所有工作流数据"""
        return self._read_json(self.workflows_file)

    def save_workflow(self, workflow_id: str, data: Dict) -> bool:
        """保存工作流数据"""
        workflows = self.get_workflows()
        workflows[workflow_id] = data
        return self._write_json(self.workflows_file, workflows)

    # ========== 效率指标数据 ==========

    def get_metrics(self) -> Dict:
        """获取所有效率指标"""
        return self._read_json(self.metrics_file)

    def update_metric(self, metric_name: str, value: Any) -> bool:
        """更新效率指标"""
        metrics = self.get_metrics()
        metrics[metric_name] = value
        return self._write_json(self.metrics_file, metrics)

    def increment_metric(self, metric_name: str, amount: int = 1) -> bool:
        """递增效率指标"""
        metrics = self.get_metrics()
        metrics[metric_name] = metrics.get(metric_name, 0) + amount
        return self._write_json(self.metrics_file, metrics)

    # ========== 用户配置 ==========

    def get_user_profile(self) -> Dict:
        """获取用户配置"""
        return self._read_json(self.user_profile_file)

    def update_user_profile(self, data: Dict) -> bool:
        """更新用户配置"""
        profile = self.get_user_profile()
        profile.update(data)
        return self._write_json(self.user_profile_file, profile)

    def get_streak_info(self) -> Dict:
        """获取连续使用天数信息"""
        profile = self.get_user_profile()
        return profile.get('streak', {
            'current': 0,
            'longest': 0,
            'last_active_date': None
        })

    def update_streak(self, date: str) -> Dict:
        """更新连续使用天数"""
        profile = self.get_user_profile()
        streak = profile.get('streak', {
            'current': 0,
            'longest': 0,
            'last_active_date': None
        })

        from datetime import datetime

        last_date = streak.get('last_active_date')
        today = datetime.strptime(date, "%Y-%m-%d").date()

        if last_date:
            last = datetime.strptime(last_date, "%Y-%m-%d").date()
            delta = (today - last).days

            if delta == 1:
                # 连续使用
                streak['current'] += 1
            elif delta > 1:
                # 中断了
                streak['current'] = 1
            # delta == 0 表示同一天，不更新
        else:
            # 第一次使用
            streak['current'] = 1

        streak['last_active_date'] = date
        streak['longest'] = max(streak['current'], streak['longest'])

        profile['streak'] = streak
        self._write_json(self.user_profile_file, profile)

        return streak

    # ========== 导出功能 ==========

    def export_all_data(self) -> Dict:
        """导出所有数据"""
        return {
            'activities': self.get_activities(),
            'achievements': self.get_achievements(),
            'workflows': self.get_workflows(),
            'metrics': self.get_metrics(),
            'user_profile': self.get_user_profile(),
            'export_time': datetime.now().isoformat()
        }

    def export_csv(self, data_type: str = "activities") -> str:
        """导出 CSV 格式数据"""
        import io
        import csv

        output = io.StringIO()

        if data_type == "activities":
            writer = csv.writer(output)
            writer.writerow(['Date', 'Tool', 'Count', 'Skill', 'Count', 'Messages', 'Platform'])

            activities = self.get_activities()
            for date, data in sorted(activities.items()):
                tools = data.get('tools', {})
                skills = data.get('skills', {})
                messages = data.get('messages', {})

                if tools:
                    for tool, count in tools.items():
                        writer.writerow([date, tool, count, '', '', '', ''])
                elif skills:
                    for skill, count in skills.items():
                        writer.writerow([date, '', '', skill, count, '', ''])
                elif messages:
                    for platform, count in messages.items():
                        writer.writerow([date, '', '', '', '', count, platform])

        return output.getvalue()
