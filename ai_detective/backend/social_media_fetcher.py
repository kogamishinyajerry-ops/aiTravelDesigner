"""
社交媒体数据获取模块
Social Media Data Fetcher

功能:
- 模拟社交媒体数据获取（实际使用需要API密钥）
- 支持小红书、微博、抖音等平台
- 用户历史行为分析
- 网络痕迹追踪
"""

from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field
from datetime import datetime, timedelta
import re
import hashlib
from enum import Enum


class Platform(Enum):
    """支持的平台"""
    XIAOHONGSHU = "小红书"
    WEIBO = "微博"
    DOUYIN = "抖音"
    BILIBILI = "B站"
    ZHIHU = "知乎"


@dataclass
class SocialMediaPost:
    """社交媒体帖子"""
    post_id: str
    platform: Platform
    user_id: str
    username: str
    content: str
    timestamp: datetime
    likes: int
    comments: int
    shares: int
    images: List[str] = field(default_factory=list)
    tags: List[str] = field(default_factory=list)
    raw_data: Dict[str, Any] = field(default_factory=dict)


@dataclass
class UserProfile:
    """用户档案"""
    user_id: str
    platform: Platform
    username: str
    avatar: str
    bio: str
    followers_count: int
    following_count: int
    posts_count: int
    verified: bool
    registration_date: datetime
    last_active: datetime
    suspicious_indicators: List[str] = field(default_factory=list)
    behavior_patterns: Dict[str, Any] = field(default_factory=dict)


@dataclass
class FetchResult:
    """数据获取结果"""
    timestamp: datetime
    query: str
    platform: Platform
    posts: List[SocialMediaPost] = field(default_factory=list)
    user_profile: Optional[UserProfile] = None
    total_results: int = 0
    search_metadata: Dict[str, Any] = field(default_factory=dict)
    confidence: float = 0.0
    error_message: str = ""


class SocialMediaFetcher:
    """社交媒体数据获取器"""
    
    def __init__(self):
        self._initialize_patterns()
        
    def _initialize_patterns(self):
        """初始化正则模式"""
        # 小红书用户ID模式
        self.xiaohongshu_user_pattern = re.compile(r'用户[ID]?[:：]\s*([a-zA-Z0-9]+)')
        
        # 小红书帖子ID模式
        self.xiaohongshu_post_pattern = re.compile(r'笔记[ID]?[:：]\s*([a-zA-Z0-9]+)')
        
        # 微博用户模式
        self.weibo_user_pattern = re.compile(r'@([a-zA-Z0-9_\u4e00-\u9fa5]+)')
        
        # 抖音用户模式
        self.douyin_user_pattern = re.compile(r'抖音[号]?[:：]\s*([a-zA-Z0-9]+)')
    
    def fetch_by_username(
        self, 
        username: str, 
        platform: Platform = Platform.XIAOHONGSHU,
        days_back: int = 30
    ) -> FetchResult:
        """根据用户名获取数据"""
        timestamp = datetime.now()
        
        # 实际使用时需要调用各平台API
        # 这里使用模拟数据
        
        # 生成模拟用户档案
        user_profile = self._generate_mock_user_profile(username, platform)
        
        # 生成模拟帖子
        posts = self._generate_mock_posts(username, platform, days_back)
        
        return FetchResult(
            timestamp=timestamp,
            query=username,
            platform=platform,
            posts=posts,
            user_profile=user_profile,
            total_results=len(posts),
            search_metadata={
                "search_type": "username",
                "days_back": days_back,
                "platform": platform.value
            },
            confidence=0.85,
            error_message=""
        )
    
    def fetch_by_keyword(
        self,
        keyword: str,
        platform: Platform = Platform.XIAOHONGSHU,
        max_results: int = 20
    ) -> FetchResult:
        """根据关键词搜索"""
        timestamp = datetime.now()
        
        # 生成模拟搜索结果
        posts = self._generate_mock_search_posts(keyword, platform, max_results)
        
        return FetchResult(
            timestamp=timestamp,
            query=keyword,
            platform=platform,
            posts=posts,
            user_profile=None,
            total_results=len(posts),
            search_metadata={
                "search_type": "keyword",
                "max_results": max_results,
                "platform": platform.value
            },
            confidence=0.75,
            error_message=""
        )
    
    def fetch_by_post_id(
        self,
        post_id: str,
        platform: Platform = Platform.XIAOHONGSHU
    ) -> FetchResult:
        """根据帖子ID获取数据"""
        timestamp = datetime.now()
        
        # 生成模拟帖子数据
        post = self._generate_mock_post_by_id(post_id, platform)
        
        return FetchResult(
            timestamp=timestamp,
            query=post_id,
            platform=platform,
            posts=[post] if post else [],
            user_profile=None,
            total_results=1 if post else 0,
            search_metadata={
                "search_type": "post_id",
                "platform": platform.value
            },
            confidence=0.95,
            error_message=""
        )
    
    def analyze_user_behavior(self, result: FetchResult) -> Dict[str, Any]:
        """分析用户行为模式"""
        if not result.user_profile or not result.posts:
            return {}
        
        behavior_patterns = {
            "posting_frequency": 0.0,
            "avg_engagement": 0.0,
            "peak_hours": [],
            "content_themes": [],
            "suspicious_patterns": []
        }
        
        if result.posts:
            # 发帖频率（每天平均发帖数）
            time_span_days = (result.posts[0].timestamp - result.posts[-1].timestamp).days
            if time_span_days > 0:
                behavior_patterns["posting_frequency"] = len(result.posts) / time_span_days
            
            # 平均互动量
            total_engagement = sum(p.likes + p.comments + p.shares for p in result.posts)
            behavior_patterns["avg_engagement"] = total_engagement / len(result.posts)
            
            # 发帖高峰时段
            hour_counts = {}
            for post in result.posts:
                hour = post.timestamp.hour
                hour_counts[hour] = hour_counts.get(hour, 0) + 1
            if hour_counts:
                peak_hour = max(hour_counts.items(), key=lambda x: x[1])
                behavior_patterns["peak_hours"] = [peak_hour[0]]
            
            # 内容主题
            all_tags = []
            for post in result.posts:
                all_tags.extend(post.tags)
            tag_counts = {}
            for tag in all_tags:
                tag_counts[tag] = tag_counts.get(tag, 0) + 1
            if tag_counts:
                top_tags = sorted(tag_counts.items(), key=lambda x: x[1], reverse=True)[:5]
                behavior_patterns["content_themes"] = [tag[0] for tag in top_tags]
        
        # 可疑模式检测
        suspicious_patterns = []
        if result.user_profile:
            # 新注册且高活跃
            days_since_reg = (datetime.now() - result.user_profile.registration_date).days
            if days_since_reg < 30 and result.user_profile.posts_count > 50:
                suspicious_patterns.append("新注册用户高活跃")
            
            # 无认证但高关注
            if not result.user_profile.verified and result.user_profile.followers_count > 10000:
                suspicious_patterns.append("未认证高关注用户")
            
            # 粉丝互动异常
            if behavior_patterns["avg_engagement"] < 10 and result.user_profile.followers_count > 1000:
                suspicious_patterns.append("粉丝互动量异常低")
        
        behavior_patterns["suspicious_patterns"] = suspicious_patterns
        
        return behavior_patterns
    
    def track_network_traces(
        self,
        username: str,
        platform: Platform = Platform.XIAOHONGSHU
    ) -> Dict[str, Any]:
        """追踪网络痕迹"""
        traces = {
            "accounts_found": 0,
            "platforms": {},
            "linked_profiles": [],
            "cross_platform_activity": False
        }
        
        # 模拟跨平台搜索
        platforms_to_search = [p for p in Platform if p != platform]
        
        for p in platforms_to_search:
            # 模拟搜索结果
            found = self._mock_cross_platform_search(username, p)
            if found:
                traces["platforms"][p.value] = {
                    "found": True,
                    "username": username,
                    "similarity": found["similarity"]
                }
                traces["linked_profiles"].append({
                    "platform": p.value,
                    "username": username,
                    "similarity": found["similarity"]
                })
                traces["accounts_found"] += 1
        
        traces["cross_platform_activity"] = traces["accounts_found"] > 1
        
        return traces
    
    # ============ 辅助方法 ============
    
    def _generate_mock_user_profile(self, username: str, platform: Platform) -> UserProfile:
        """生成模拟用户档案"""
        return UserProfile(
            user_id=self._generate_id(),
            platform=platform,
            username=username,
            avatar=f"https://example.com/avatars/{username}.jpg",
            bio=f"{username}的个人简介",
            followers_count=1250,
            following_count=89,
            posts_count=156,
            verified=False,
            registration_date=datetime.now() - timedelta(days=180),
            last_active=datetime.now() - timedelta(hours=3),
            suspicious_indicators=[],
            behavior_patterns={}
        )
    
    def _generate_mock_posts(
        self,
        username: str,
        platform: Platform,
        days_back: int
    ) -> List[SocialMediaPost]:
        """生成模拟帖子列表"""
        posts = []
        now = datetime.now()
        
        # 生成10-20个帖子
        num_posts = min(20, max(10, days_back // 2))
        
        for i in range(num_posts):
            days_ago = i * (days_back / num_posts)
            timestamp = now - timedelta(days=days_ago)
            
            post = SocialMediaPost(
                post_id=self._generate_post_id(platform),
                platform=platform,
                user_id=self._generate_id(),
                username=username,
                content=self._generate_mock_content(i, platform),
                timestamp=timestamp,
                likes=self._random_int(10, 500),
                comments=self._random_int(0, 50),
                shares=self._random_int(0, 30),
                tags=self._generate_mock_tags(platform)
            )
            posts.append(post)
        
        return posts
    
    def _generate_mock_search_posts(
        self,
        keyword: str,
        platform: Platform,
        max_results: int
    ) -> List[SocialMediaPost]:
        """生成模拟搜索结果"""
        posts = []
        now = datetime.now()
        
        num_results = min(max_results, 10)
        
        for i in range(num_results):
            post = SocialMediaPost(
                post_id=self._generate_post_id(platform),
                platform=platform,
                user_id=self._generate_id(),
                username=f"用户{self._random_int(1000, 9999)}",
                content=f"关于'{keyword}'的内容... {self._generate_mock_content(i, platform)}",
                timestamp=now - timedelta(days=self._random_int(1, 30)),
                likes=self._random_int(5, 300),
                comments=self._random_int(0, 20),
                shares=self._random_int(0, 10),
                tags=[keyword]
            )
            posts.append(post)
        
        return posts
    
    def _generate_mock_post_by_id(
        self,
        post_id: str,
        platform: Platform
    ) -> Optional[SocialMediaPost]:
        """生成指定ID的模拟帖子"""
        if not post_id:
            return None
            
        return SocialMediaPost(
            post_id=post_id,
            platform=platform,
            user_id=self._generate_id(),
            username="测试用户",
            content=f"帖子{post_id}的内容...",
            timestamp=datetime.now() - timedelta(days=5),
            likes=self._random_int(50, 200),
            comments=self._random_int(5, 30),
            shares=self._random_int(2, 15),
            tags=self._generate_mock_tags(platform)
        )
    
    def _generate_mock_content(self, index: int, platform: Platform) -> str:
        """生成模拟内容"""
        contents = [
            "今天遇到了很糟糕的事情",
            "分享一下我的经验",
            "这个店太差了，大家避雷",
            "强烈不推荐",
            "维权成功！",
            "希望大家引以为戒",
            "太生气了",
            "终于解决了",
            "谢谢大家的支持",
            "更新一下进展"
        ]
        return contents[index % len(contents)]
    
    def _generate_mock_tags(self, platform: Platform) -> List[str]:
        """生成模拟标签"""
        tags_map = {
            Platform.XIAOHONGSHU: ["避雷", "维权", "消费陷阱", "投诉", "经验分享"],
            Platform.WEIBO: ["曝光", "避雷", "投诉", "求助"],
            Platform.DOUYIN: ["避坑", "真实经历", "消费者"],
            Platform.BILIBILI: ["避坑", "测评", "维权"],
            Platform.ZHIHU: ["法律", "维权", "投诉", "消费者权益"]
        }
        return tags_map.get(platform, ["吐槽", "分享"])
    
    def _mock_cross_platform_search(
        self,
        username: str,
        platform: Platform
    ) -> Optional[Dict[str, Any]]:
        """模拟跨平台搜索"""
        # 模拟30%概率在其他平台找到
        import random
        if random.random() > 0.7:
            return {
                "found": True,
                "username": username,
                "similarity": random.uniform(0.6, 0.95)
            }
        return None
    
    def _generate_id(self) -> str:
        """生成随机ID"""
        import random
        import string
        return ''.join(random.choices(string.ascii_letters + string.digits, k=12))
    
    def _generate_post_id(self, platform: Platform) -> str:
        """生成帖子ID"""
        return f"{platform.value.lower()}_{self._generate_id()}"
    
    def _random_int(self, min_val: int, max_val: int) -> int:
        """生成随机整数"""
        import random
        return random.randint(min_val, max_val)


# ============ 测试代码 ============

if __name__ == "__main__":
    print("=" * 60)
    print("社交媒体数据获取器 - 测试")
    print("=" * 60)
    
    fetcher = SocialMediaFetcher()
    
    # 测试1: 根据用户名获取
    print("\n1️⃣ 测试: 根据用户名获取数据")
    print("-" * 40)
    result1 = fetcher.fetch_by_username("testuser", Platform.XIAOHONGSHU, days_back=30)
    print(f"✅ 获取到 {result1.total_results} 条帖子")
    print(f"   用户: {result1.user_profile.username}")
    print(f"   粉丝数: {result1.user_profile.followers_count}")
    
    # 测试2: 根据关键词搜索
    print("\n2️⃣ 测试: 根据关键词搜索")
    print("-" * 40)
    result2 = fetcher.fetch_by_keyword("诈骗", Platform.XIAOHONGSHU, max_results=10)
    print(f"✅ 搜索到 {result2.total_results} 条结果")
    if result2.posts:
        print(f"   首条内容: {result2.posts[0].content[:50]}...")
    
    # 测试3: 用户行为分析
    print("\n3️⃣ 测试: 用户行为分析")
    print("-" * 40)
    behavior = fetcher.analyze_user_behavior(result1)
    print(f"✅ 发帖频率: {behavior['posting_frequency']:.2f} 条/天")
    print(f"   平均互动: {behavior['avg_engagement']:.1f}")
    print(f"   可疑模式: {behavior['suspicious_patterns']}")
    
    # 测试4: 网络痕迹追踪
    print("\n4️⃣ 测试: 网络痕迹追踪")
    print("-" * 40)
    traces = fetcher.track_network_traces("testuser", Platform.XIAOHONGSHU)
    print(f"✅ 跨平台账户: {traces['accounts_found']} 个")
    print(f"   跨平台活跃: {traces['cross_platform_activity']}")
    for profile in traces['linked_profiles']:
        print(f"   - {profile['platform']}: {profile['username']}")
    
    print("\n" + "=" * 60)
    print("🎉 所有测试完成!")
    print("=" * 60)
