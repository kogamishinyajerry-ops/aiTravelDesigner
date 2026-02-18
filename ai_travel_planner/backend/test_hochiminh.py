#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""测试专业规划系统"""

import asyncio
from services.planning import get_professional_planning_service, TravelRequirements
from services.planning.professional_standards import (
    TravelStyle, ActivityIntensity, BudgetLevel, AccommodationType
)

async def main():
    # 初始化专业规划服务
    service = get_professional_planning_service()

    # 构建旅行需求对象
    requirements = TravelRequirements(
        destination='越南胡志明市',
        departure_city='上海',
        start_date='2026-03-06',
        end_date='2026-03-09',
        days=4,
        travelers_adults=6,
        travelers_children=0,
        travelers_infants=0,
        travelers_seniors=0,
        travel_style=TravelStyle.CULTURAL,  # 文化深度游
        activity_intensity=ActivityIntensity.MODERATE,  # 适中强度
        budget_level=BudgetLevel.STANDARD,  # 标准型预算
        budget_limit=6500 * 6,  # 总预算39,000元
        interests=['历史', '文化', '美食', '购物'],
        accommodation_type=AccommodationType.STANDARD_HOTEL,
        accommodation_preferences=['市中心', '交通便利'],
        flight_class='economy',
        transport_preference='混合使用出租车和Grab'
    )

    print('🎯 开始生成专业行程规划...')
    print('=' * 60)

    # 生成行程
    itinerary, session_id = await service.create_itinerary_from_requirements(requirements)

    print('\n✅ 行程生成完成！')
    print(f'会话ID: {session_id}\n')
    print('=' * 60)

    # 打印行程摘要
    print(f"📍 目的地: {itinerary.requirements.destination}")
    print(f"📅 日期: {itinerary.requirements.start_date} 至 {itinerary.requirements.end_date}")
    print(f"👥 人数: {itinerary.requirements.travelers_adults}人")
    print(f"💰 预算: ¥{itinerary.requirements.budget_limit:,} (¥{itinerary.requirements.budget_limit // itinerary.requirements.travelers_adults:,}/人)")
    print(f"🎨 风格: {itinerary.requirements.travel_style.value}")
    print(f"🔥 强度: {itinerary.requirements.activity_intensity.value}")
    print()

    # 打印每日行程
    print('=' * 60)
    print('🗓️ 每日行程安排')
    print('=' * 60)

    for day in itinerary.daily_plans:
        print(f"\n📅 第{day.get('day', '?')}天: {day.get('date', '?')}")
        print(f"   主题: {day.get('theme', '探索')}")

        # 打印活动
        if 'morning' in day and day['morning']:
            print(f"\n   上午:")
            print(f"   {day['morning']}")
        if 'afternoon' in day and day['afternoon']:
            print(f"\n   下午:")
            print(f"   {day['afternoon']}")
        if 'lunch' in day and day['lunch']:
            print(f"\n   午餐:")
            print(f"   {day['lunch']}")
        if 'dinner' in day and day['dinner']:
            print(f"\n   晚餐:")
            print(f"   {day['dinner']}")

    # 打印预算明细
    print('\n' + '=' * 60)
    print('💰 预算明细')
    print('=' * 60)

    budget = itinerary.budget_breakdown
    if budget:
        print(f"\n总预算: ¥{itinerary.requirements.budget_limit:,}")
        print(f"人均: ¥{itinerary.requirements.budget_limit // itinerary.requirements.travelers_adults:,}")
        print()
        print('费用构成:')
        for key, value in budget.items():
            if key != 'total_cost':
                print(f"  {key}: {value}")

    # 规划建议
    if itinerary.recommendations:
        print('\n' + '=' * 60)
        print('💡 规划建议')
        print('=' * 60)
        for rec in itinerary.recommendations:
            print(f"  • {rec}")

    # 保存完整结果到JSON
    import json
    result_dict = {
        'itinerary': {
            'destination': itinerary.requirements.destination,
            'start_date': itinerary.requirements.start_date,
            'end_date': itinerary.requirements.end_date,
            'days': itinerary.daily_plans,
            'total_budget': itinerary.requirements.budget_limit,
            'adults': itinerary.requirements.travelers_adults,
            'style': itinerary.requirements.travel_style.value,
            'intensity': str(itinerary.requirements.activity_intensity.value),
        },
        'budget': {
            'total_budget': itinerary.requirements.budget_limit,
            'per_person': itinerary.requirements.budget_limit // itinerary.requirements.travelers_adults,
            'breakdown': budget
        },
        'recommendations': itinerary.recommendations,
        'session_id': session_id
    }

    with open('/workspace/ai_travel_planner/backend/test_result.json', 'w', encoding='utf-8') as f:
        json.dump(result_dict, f, ensure_ascii=False, indent=2)
    print('\n✅ 完整行程数据已保存到 test_result.json')

if __name__ == '__main__':
    asyncio.run(main())
