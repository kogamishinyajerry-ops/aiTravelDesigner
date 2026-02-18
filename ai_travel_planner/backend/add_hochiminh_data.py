#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""添加胡志明市景点和餐厅数据"""

from services.planning.professional_itinerary_generator import (
    ProfessionalItineraryGenerator,
    get_professional_generator
)

def add_hochiminh_data():
    """添加胡志明市的景点和餐厅数据"""
    generator = get_professional_generator()
    
    # 胡志明市景点数据
    hochiminh_attractions = [
        {
            "name": "统一宫",
            "name_en": "Independence Palace",
            "tags": ["历史", "文化"],
            "rating": 4.6,
            "duration": 2.0,
            "cost": 150000,  # 越南盾，约40元人民币
            "family_friendly": True,
            "best_time": "上午",
            "opening_hours": "07:30-11:00, 13:00-16:00",
            "description": "南越时期的总统府，见证了1975年越南统一的历史时刻",
            "nearby_restaurants": 8
        },
        {
            "name": "战争遗迹博物馆",
            "name_en": "War Remnants Museum",
            "tags": ["历史", "文化"],
            "rating": 4.7,
            "duration": 2.5,
            "cost": 120000,
            "family_friendly": False,
            "best_time": "上午",
            "opening_hours": "07:30-18:00",
            "description": "展示越南战争历史的博物馆，了解战争的真实情况",
            "nearby_restaurants": 5
        },
        {
            "name": "西贡中央邮局",
            "name_en": "Saigon Central Post Office",
            "tags": ["历史", "文化", "建筑"],
            "rating": 4.5,
            "duration": 0.5,
            "cost": 0,
            "family_friendly": True,
            "best_time": "下午",
            "opening_hours": "08:00-18:00",
            "description": "法国殖民时期的经典建筑，仍在运营的邮局",
            "nearby_restaurants": 12
        },
        {
            "name": "圣母大教堂",
            "name_en": "Notre-Dame Cathedral of Saigon",
            "tags": ["历史", "文化", "建筑", "宗教"],
            "rating": 4.6,
            "duration": 0.5,
            "cost": 0,
            "family_friendly": True,
            "best_time": "上午",
            "opening_hours": "08:00-11:00, 14:00-16:00",
            "description": "法国殖民时期的哥特式教堂，胡志明市标志性建筑",
            "nearby_restaurants": 10
        },
        {
            "name": "范五老街",
            "name_en": "Pham Ngu Lao Street",
            "tags": ["购物", "美食", "夜生活"],
            "rating": 4.3,
            "duration": 2.0,
            "cost": 0,
            "family_friendly": True,
            "best_time": "晚上",
            "opening_hours": "全天",
            "description": "背包客聚集地，充满活力的夜生活和美食街",
            "nearby_restaurants": 50
        },
        {
            "name": "滨城市场",
            "name_en": "Ben Thanh Market",
            "tags": ["购物", "美食"],
            "rating": 4.4,
            "duration": 2.0,
            "cost": 0,
            "family_friendly": True,
            "best_time": "全天",
            "opening_hours": "06:00-22:00",
            "description": "胡志明市最大的传统市场，购买纪念品和品尝当地美食",
            "nearby_restaurants": 30
        },
        {
            "name": "唐人街（堤岸）",
            "name_en": "Chinatown (Cho Lon)",
            "tags": ["文化", "美食", "历史"],
            "rating": 4.2,
            "duration": 3.0,
            "cost": 0,
            "family_friendly": True,
            "best_time": "上午",
            "opening_hours": "06:00-18:00",
            "description": "越南最大的唐人街，有着浓厚的历史文化氛围",
            "nearby_restaurants": 20
        },
        {
            "name": "古芝地道",
            "name_en": "Cu Chi Tunnels",
            "tags": ["历史", "探险"],
            "rating": 4.5,
            "duration": 4.0,
            "cost": 350000,
            "family_friendly": True,
            "best_time": "全天",
            "opening_hours": "07:00-17:00",
            "description": "越南战争时期的地下隧道网络，体验地道战历史",
            "nearby_restaurants": 3
        },
        {
            "name": "耶稣圣心堂",
            "name_en": "Tan Dinh Church",
            "tags": ["宗教", "建筑", "文化"],
            "rating": 4.4,
            "duration": 1.0,
            "cost": 0,
            "family_friendly": True,
            "best_time": "上午",
            "opening_hours": "07:00-11:00, 15:00-17:30",
            "description": "粉色建筑，极具特色的教堂，拍照打卡圣地",
            "nearby_restaurants": 8
        },
        {
            "name": "西贡歌剧院",
            "name_en": "Saigon Opera House",
            "tags": ["文化", "建筑", "艺术"],
            "rating": 4.5,
            "duration": 1.0,
            "cost": 100000,
            "family_friendly": True,
            "best_time": "晚上",
            "opening_hours": "09:00-18:00 (参观)",
            "description": "法国殖民时期的歌剧院，欣赏表演的好地方",
            "nearby_restaurants": 15
        },
        {
            "name": "边青市场",
            "name_en": "Binh Tay Market",
            "tags": ["购物", "美食", "文化"],
            "rating": 4.1,
            "duration": 1.5,
            "cost": 0,
            "family_friendly": True,
            "best_time": "上午",
            "opening_hours": "06:00-18:00",
            "description": "唐人街的主要市场，批发价购物，体验当地生活",
            "nearby_restaurants": 15
        },
        {
            "name": "河畔散步道",
            "name_en": "Saigon Riverwalk",
            "tags": ["休闲", "风景"],
            "rating": 4.3,
            "duration": 1.0,
            "cost": 0,
            "family_friendly": True,
            "best_time": "晚上",
            "opening_hours": "全天",
            "description": "西贡河畔的散步道，享受夜景和河风",
            "nearby_restaurants": 25
        }
    ]
    
    # 胡志明市餐厅数据
    hochiminh_restaurants = [
        {
            "name": "Banh Mi Huynh Hoa",
            "cuisine": "越南菜",
            "specialties": ["越式法棍", "烤肉法棍"],
            "price_range": "经济",
            "rating": 4.7,
            "location": "市中心",
            "best_for": ["午餐", "晚餐"],
            "description": "胡志明市最著名的法棍店，经常排队"
        },
        {
            "name": "Pho Hoa Pasteur",
            "cuisine": "越南菜",
            "specialties": ["牛肉河粉", "鸡汤河粉"],
            "price_range": "经济",
            "rating": 4.5,
            "location": "市中心",
            "best_for": ["早餐", "午餐"],
            "description": "老字号河粉店，味道正宗"
        },
        {
            "name": "Cuc Gach Quan",
            "cuisine": "越南菜",
            "specialties": ["春卷", "烤肉", "越南咖啡"],
            "price_range": "标准",
            "rating": 4.6,
            "location": "市中心",
            "best_for": ["午餐", "晚餐"],
            "description": "传统越南庭院式餐厅，电影《情人》取景地"
        },
        {
            "name": "Secret Garden",
            "cuisine": "越南菜",
            "specialties": ["越南春卷", "烤猪颈肉", "河粉"],
            "price_range": "标准",
            "rating": 4.4,
            "location": "市中心",
            "best_for": ["晚餐"],
            "description": "屋顶花园餐厅，环境优美"
        },
        {
            "name": "Quan Bui",
            "cuisine": "越南菜",
            "specialties": ["越南火锅", "春卷", "烤肉"],
            "price_range": "标准",
            "rating": 4.5,
            "location": "市中心",
            "best_for": ["午餐", "晚餐"],
            "description": "现代越南餐厅，环境时尚"
        },
        {
            "name": "Propeller Skybar",
            "cuisine": "国际美食",
            "specialties": ["西餐", "鸡尾酒", "小吃"],
            "price_range": "高端",
            "rating": 4.3,
            "location": "市中心",
            "best_for": ["晚餐", "夜生活"],
            "description": "屋顶酒吧，俯瞰胡志明市夜景"
        },
        {
            "name": "Com Nieu Saigon",
            "cuisine": "越南菜",
            "specialties": ["越南锅巴", "春卷", "烤鱼"],
            "price_range": "标准",
            "rating": 4.4,
            "location": "市中心",
            "best_for": ["晚餐"],
            "description": "传统越南乡村风格餐厅"
        },
        {
            "name": "Pho Le",
            "cuisine": "越南菜",
            "specialties": ["牛肉河粉", "鸡汤河粉"],
            "price_range": "经济",
            "rating": 4.6,
            "location": "市中心",
            "best_for": ["早餐", "午餐"],
            "description": "老字号河粉店，24小时营业"
        },
        {
            "name": "Pizza 4P's Phan Van Han",
            "cuisine": "意大利菜",
            "specialties": ["手工披萨", "意面", "沙拉"],
            "price_range": "标准",
            "rating": 4.6,
            "location": "市中心",
            "best_for": ["午餐", "晚餐"],
            "description": "越南本土披萨品牌，品质一流"
        },
        {
            "name": "Mia Saigon",
            "cuisine": "越南菜",
            "specialties": ["越南春卷", "烤肉", "河粉", "越南咖啡"],
            "price_range": "高端",
            "rating": 4.7,
            "location": "市中心",
            "best_for": ["晚餐"],
            "description": "米其林推荐餐厅，精致越南料理"
        }
    ]
    
    # 添加到数据库
    generator.attractions_db["越南胡志明市"] = hochiminh_attractions
    generator.restaurants_db["越南胡志明市"] = hochiminh_restaurants
    
    print(f"✅ 已添加 {len(hochiminh_attractions)} 个胡志明市景点")
    print(f"✅ 已添加 {len(hochiminh_restaurants)} 个胡志明市餐厅")

if __name__ == '__main__':
    add_hochiminh_data()
    print("\n数据添加完成！现在可以重新运行行程规划了。")
