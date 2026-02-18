#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
互动式旅行规划师 - 深度定制版
通过对话深入了解用户需求，生成真正个性化的旅行方案
"""

import asyncio
import json
from datetime import datetime
from typing import Dict, List, Any, Optional


class InteractiveTravelPlanner:
    """互动式旅行规划师"""
    
    def __init__(self):
        self.user_profile = {
            'team_info': {},
            'preferences': {},
            'expectations': {},
            'constraints': {},
            'special_requests': []
        }
        self.conversation_history = []
        self.stage = 0
        
    async def start_consultation(self):
        """开始规划咨询"""
        print("""
╔══════════════════════════════════════════════════════════════════╗
║        🌍 AI专业旅行规划师 - 深度定制咨询服务                    ║
╠══════════════════════════════════════════════════════════════════╣
║                                                                  ║
║  欢迎使用我们的私人定制旅行规划服务！                           ║
║                                                                  ║
║  不同于普通的行程生成器，我们会通过深度对话了解您的：           ║
║  • 团队成员特点和需求                                             ║
║  • 真正感兴趣的旅行体验                                           ║
║  • 过去旅行的偏好和避坑经验                                       ║
║  • 特殊需求和个性化要求                                           ║
║                                                                  ║
║  让我们开始吧！                                                  ║
╚══════════════════════════════════════════════════════════════════╝
""")
        
        await self.collect_basic_info()
        await self.deep_dive_preferences()
        await self.collect_special_requirements()
        await self.finalize_expectations()
        
        return self.generate_personalized_plan()
    
    async def collect_basic_info(self):
        """收集基本信息"""
        print("\n" + "=" * 70)
        print("📝 第一部分：了解你们团队")
        print("=" * 70)
        
        # 目的地
        dest = input("\n📍 你们想去哪里旅行？（如果已确定胡志明市，请直接确认）\n> ")
        self.user_profile['team_info']['destination'] = dest or "越南胡志明市"
        
        # 日期
        date_input = input("\n📅 旅行日期是？\n> ")
        if date_input:
            self.user_profile['team_info']['dates'] = date_input
        else:
            self.user_profile['team_info']['dates'] = "2026年3月6日-9日"
        
        # 人员构成
        print("\n👥 请介绍一下你们的团队（很重要，会影响行程设计）：")
        print("  - 大家的年龄范围？")
        print("  - 有什么特别的性格特点？")
        print("  - 谁是组织者，决策风格如何？")
        team_desc = input("> ")
        self.user_profile['team_info']['team_description'] = team_desc
        
        # 旅行经历
        print("\n✈️ 之前的旅行经历？")
        print("  - 去过哪些地方？")
        print("  - 最喜欢的旅行体验是什么？")
        print("  - 最不喜欢的经历是什么？")
        travel_history = input("> ")
        self.user_profile['team_info']['travel_history'] = travel_history
        
        # 预算
        budget_input = input("\n💰 预算是多少？\n> ")
        if budget_input:
            self.user_profile['team_info']['budget'] = budget_input
        else:
            self.user_profile['team_info']['budget'] = "¥6,500/人"
        
        self.conversation_history.append({"stage": "basic_info", "data": self.user_profile['team_info']})
        
    async def deep_dive_preferences(self):
        """深度了解偏好"""
        print("\n" + "=" * 70)
        print("🎯 第二部分：了解你们的真实需求")
        print("=" * 70)
        
        # 旅行目的
        print("\n🎯 这次旅行的主要目的是什么？")
        print("  A. 放松度假，逃离工作压力")
        print("  B. 深度体验当地文化和历史")
        print("  C. 美食探索，品尝各种地道美食")
        print("  D. 购物血拼")
        print("  E. 探险体验")
        print("  F. 拍照打卡，社交媒体分享")
        print("  G. 团队 bonding，增进感情")
        print("  H. 其他（请说明）")
        purpose = input("> ")
        self.user_profile['preferences']['purpose'] = purpose
        
        # 活动偏好
        print("\n🏃 活动偏好（多选）：")
        print("  1. 历史景点参观")
        print("  2. 美食探店")
        print("  3. 购物逛街")
        print("  4. 夜生活体验")
        print("  5. 户外活动")
        print("  6. 拍照打卡")
        print("  7. 当地体验（如cooking class）")
        print("  8. 娱乐活动（如表演、酒吧）")
        print("  请输入感兴趣的编号，用空格分隔：")
        activities = input("> ")
        self.user_profile['preferences']['activities'] = activities
        
        # 节奏偏好
        print("\n⏰ 旅行节奏偏好：")
        print("  1. 轻松悠闲，每天2-3个景点")
        print("  2. 适中平衡，每天3-4个景点")
        print("  3. 紧凑充实，每天5+个景点")
        pace = input("> ")
        self.user_profile['preferences']['pace'] = pace
        
        # 住宿偏好
        print("\n🏨 住宿偏好：")
        print("  1. 经济实惠")
        print("  2. 性价比高的中档酒店")
        print("  3. 舒适高档")
        print("  4. 特色民宿")
        print("  5. 奢华酒店")
        accommodation = input("> ")
        self.user_profile['preferences']['accommodation'] = accommodation
        
        # 饮食偏好
        print("\n🍜 饮食偏好：")
        print("  - 有什么忌口或过敏吗？")
        print("  - 更喜欢当地特色还是国际美食？")
        print("  - 对街头美食接受度如何？")
        food_prefs = input("> ")
        self.user_profile['preferences']['food'] = food_prefs
        
        self.conversation_history.append({"stage": "preferences", "data": self.user_profile['preferences']})
    
    async def collect_special_requirements(self):
        """收集特殊需求"""
        print("\n" + "=" * 70)
        print("⚠️ 第三部分：特殊需求和限制")
        print("=" * 70)
        
        # 禁忌
        print("\n❌ 有什么绝对不想做的吗？")
        print("  - 不想去的景点/区域")
        print("  - 不想吃的食物")
        print("  - 不想住的地方")
        print("  - 其他任何"绝对不要"的要求")
        no_go = input("> ")
        self.user_profile['constraints']['avoid'] = no_go
        
        # 必须体验
        print("\n✅ 有什么一定要体验的吗？")
        print("  - 必须去的景点")
        print("  - 必须吃的美食")
        print("  - 必须做的事情")
        must_do = input("> ")
        self.user_profile['constraints']['must_do'] = must_do
        
        # 特殊需求
        print("\n⭐ 特殊需求：")
        print("  - 无障碍需求")
        print("  - 特殊场合（生日、纪念日等）")
        print("  - 商务需求（需要安静空间等）")
        print("  - 其他任何特殊要求")
        special = input("> ")
        self.user_profile['special_requests'].append(special)
        
        self.conversation_history.append({"stage": "constraints", "data": self.user_profile['constraints']})
    
    async def finalize_expectations(self):
        """确认期望"""
        print("\n" + "=" * 70)
        print("✨ 第四部分：确认期望")
        print("=" * 70)
        
        print("\n🎨 如果用几个词形容你理想中的旅行，会是什么？")
        keywords = input("> ")
        self.user_profile['expectations']['keywords'] = keywords
        
        print("\n📸 回来后，你希望最满意的旅行记忆是什么？")
        best_memory = input("> ")
        self.user_profile['expectations']['best_memory'] = best_memory
        
        print("\n💬 还有其他任何想告诉我的吗？")
        additional = input("> ")
        self.user_profile['expectations']['additional'] = additional
        
        self.conversation_history.append({"stage": "expectations", "data": self.user_profile['expectations']})
        
        # 总结
        print("\n" + "=" * 70)
        print("📊 信息收集完成！让我总结一下你们的档案：")
        print("=" * 70)
        self.print_summary()
        
        confirm = input("\n以上信息是否正确？（y/n）\n> ")
        if confirm.lower() != 'y':
            print("好的，我们可以调整。请告诉我需要修改什么：")
            adjustments = input("> ")
            self.user_profile['adjustments'] = adjustments
    
    def print_summary(self):
        """打印用户档案总结"""
        print(f"\n📍 目的地: {self.user_profile['team_info'].get('destination', '未确定')}")
        print(f"📅 日期: {self.user_profile['team_info'].get('dates', '未确定')}")
        print(f"💰 预算: {self.user_profile['team_info'].get('budget', '未确定')}")
        print(f"\n团队特点:")
        print(f"  {self.user_profile['team_info'].get('team_description', '未描述')}")
        print(f"\n旅行目的: {self.user_profile['preferences'].get('purpose', '未明确')}")
        print(f"活动偏好: {self.user_profile['preferences'].get('activities', '未选择')}")
        print(f"节奏: {self.user_profile['preferences'].get('pace', '未选择')}")
        print(f"住宿: {self.user_profile['preferences'].get('accommodation', '未选择')}")
        print(f"\n避免: {self.user_profile['constraints'].get('avoid', '无')}")
        print(f"必须: {self.user_profile['constraints'].get('must_do', '无')}")
        print(f"\n理想旅行关键词: {self.user_profile['expectations'].get('keywords', '未提供')}")
    
    def generate_personalized_plan(self) -> Dict[str, Any]:
        """生成个性化规划"""
        print("\n" + "=" * 70)
        print("🎯 正在为你们生成个性化旅行方案...")
        print("=" * 70)
        
        plan = {
            'user_profile': self.user_profile,
            'personalization_notes': self._create_personalization_notes(),
            'recommendations': self._create_recommendations(),
            'custom_itinerary': self._create_custom_itinerary()
        }
        
        return plan
    
    def _create_personalization_notes(self) -> List[str]:
        """创建个性化备注"""
        notes = []
        
        # 根据旅行目的
        purpose = self.user_profile['preferences'].get('purpose', '')
        if 'A' in purpose:
            notes.append("行程安排较为轻松，避免赶时间")
        if 'B' in purpose:
            notes.append("重点安排历史文化深度讲解，考虑聘请专业导游")
        if 'C' in purpose:
            notes.append("美食是重点，每餐都精心挑选特色餐厅")
        if 'D' in purpose:
            notes.append("安排充足的购物时间，推荐当地特色商品")
        
        # 根据节奏偏好
        pace = self.user_profile['preferences'].get('pace', '')
        if pace == '1':
            notes.append("每天安排2-3个主要活动，留出自由时间")
        elif pace == '2':
            notes.append("每天安排3-4个活动，平衡充实和休息")
        elif pace == '3':
            notes.append("行程较为紧凑，适合精力充沛的团队")
        
        # 根据特殊需求
        avoid = self.user_profile['constraints'].get('avoid', '')
        if avoid:
            notes.append(f"特别注意避开：{avoid}")
        
        must_do = self.user_profile['constraints'].get('must_do', '')
        if must_do:
            notes.append(f"必须体验：{must_do}")
        
        return notes
    
    def _create_recommendations(self) -> Dict[str, Any]:
        """创建个性化推荐"""
        recommendations = {
            'general': [],
            'specific': {}
        }
        
        # 基于关键词的推荐
        keywords = self.user_profile['expectations'].get('keywords', '')
        if '浪漫' in keywords or '情侣' in keywords:
            recommendations['specific'].update({
                'romantic_spots': ['西贡河畔晚餐', '屋顶酒吧夜景'],
                'accommodation': '建议选择有景观的酒店'
            })
        
        if '刺激' in keywords or '冒险' in keywords:
            recommendations['specific'].update({
                'adventure_activities': ['古芝地道探索', '西贡河游船'],
                'nightlife': ['范五老街夜生活', '屋顶酒吧']
            })
        
        if '文化' in keywords:
            recommendations['specific'].update({
                'cultural_experiences': ['聘请历史导游', '博物馆深度游', '唐人街探索'],
                'tips': '建议提前学习越南历史，体验会更深入'
            })
        
        if '美食' in keywords:
            recommendations['specific'].update({
                'food_experiences': ['街头美食巡礼', '特色餐厅预约', 'cooking class'],
                'must_try': ['越南河粉', '越式法棍', '越南咖啡', '越南春卷']
            })
        
        return recommendations
    
    def _create_custom_itinerary(self) -> Dict[str, Any]:
        """创建定制行程框架"""
        # 这里会基于收集的信息生成真正的定制行程
        # 简化版本，实际应该调用专业规划系统
        
        itinerary = {
            'note': '此为框架示例，实际会基于你们的回答深度定制',
            'daily_structure': self._suggest_daily_structure()
        }
        
        return itinerary
    
    def _suggest_daily_structure(self) -> List[Dict[str, str]]:
        """建议的每日行程结构"""
        pace = self.user_profile['preferences'].get('pace', '2')
        
        if pace == '1':
            return [
                {'time': '09:00-12:00', 'type': '主要活动', 'note': '轻松游览'},
                {'time': '12:00-14:00', 'type': '午餐', 'note': '品尝当地美食'},
                {'time': '14:00-17:00', 'type': '主要活动', 'note': '深度体验'},
                {'time': '17:00-19:00', 'type': '休息/自由活动', 'note': '酒店休息或逛街'},
                {'time': '19:00-21:00', 'type': '晚餐', 'note': '特色餐厅'},
                {'time': '21:00-...', 'type': '夜间活动', 'note': '自由选择'}
            ]
        elif pace == '2':
            return [
                {'time': '08:30-11:30', 'type': '主要活动1', 'note': '晨间游览'},
                {'time': '11:30-13:00', 'type': '午餐', 'note': '快速午餐'},
                {'time': '13:00-16:30', 'type': '主要活动2', 'note': '午后深度游'},
                {'time': '16:30-18:00', 'type': '轻量活动', 'note': '景点或购物'},
                {'time': '18:00-20:00', 'type': '晚餐', 'note': '特色餐厅'},
                {'time': '20:00-22:00', 'type': '夜生活', 'note': '探索当地夜生活'}
            ]
        else:  # pace == '3'
            return [
                {'time': '08:00-10:00', 'type': '主要活动1', 'note': '早间景点'},
                {'time': '10:00-12:00', 'type': '主要活动2', 'note': '上午景点'},
                {'time': '12:00-13:00', 'type': '午餐', 'note': '简餐'},
                {'time': '13:00-15:00', 'type': '主要活动3', 'note': '午后景点'},
                {'time': '15:00-17:00', 'type': '主要活动4', 'note': '下午景点'},
                {'time': '17:00-18:30', 'type': '快速活动', 'note': '最后一个景点'},
                {'time': '18:30-20:00', 'type': '晚餐', 'note': '特色晚餐'},
                {'time': '20:00-22:00', 'type': '夜生活', 'note': '夜市或酒吧'}
            ]
    
    def save_profile(self, filename: str = None):
        """保存用户档案"""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"user_profile_{timestamp}.json"
        
        data = {
            'user_profile': self.user_profile,
            'conversation_history': self.conversation_history,
            'created_at': datetime.now().isoformat()
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print(f"\n✅ 用户档案已保存到: {filename}")
        return filename


async def main():
    """主函数"""
    planner = InteractiveTravelPlanner()
    
    # 开始咨询
    plan = await planner.start_consultation()
    
    # 保存档案
    profile_file = planner.save_profile()
    
    # 保存方案
    plan_file = profile_file.replace('user_profile', 'travel_plan')
    with open(plan_file, 'w', encoding='utf-8') as f:
        json.dump(plan, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ 个性化方案已保存到: {plan_file}")
    
    print("\n" + "=" * 70)
    print("🎉 规划完成！")
    print("=" * 70)
    print("\n下一步：")
    print("1. 我会基于你们的深度回答，调用专业规划系统")
    print("2. 生成真正个性化的每日行程")
    print("3. 针对你们的偏好和需求定制每个细节")
    print("\n这个系统会记住你们的所有回答，确保方案是真正的私人订制！")


if __name__ == '__main__':
    print("""
╔══════════════════════════════════════════════════════════════════╗
║  💡 使用说明                                                    ║
╠══════════════════════════════════════════════════════════════════╣
║  这是一个互动式旅行规划系统，会通过对话深入了解：                ║
║  - 你们团队的特点和需求                                         ║
║  - 真正感兴趣的旅行体验                                         ║
║  - 特殊要求和限制条件                                           ║
║  - 理想中的旅行记忆                                             ║
║                                                                  ║
║  请诚实地回答每个问题，答案越详细，方案就越个性化！             ║
╚══════════════════════════════════════════════════════════════════╝
""")
    
    asyncio.run(main())
