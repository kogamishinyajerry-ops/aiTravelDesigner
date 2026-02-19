"""
测试外部数据获取模块
Test External Data Fetching Modules
"""

import sys
sys.path.insert(0, 'backend')

from social_media_fetcher import SocialMediaFetcher, Platform
from legal_database_fetcher import LegalDatabaseFetcher, CaseType
from multimedia_analyzer import MultimediaAnalyzer


def test_social_media_fetcher():
    """测试社交媒体数据获取"""
    print("=" * 60)
    print("1️⃣ 社交媒体数据获取测试")
    print("=" * 60)
    
    fetcher = SocialMediaFetcher()
    
    # 测试1: 根据用户名获取
    print("\n📱 测试: 获取用户数据")
    result = fetcher.fetch_by_username("testuser", Platform.XIAOHONGSHU, days_back=30)
    print(f"✅ 获取到 {result.total_results} 条帖子")
    print(f"   用户名: {result.user_profile.username}")
    print(f"   粉丝数: {result.user_profile.followers_count}")
    
    # 测试2: 根据关键词搜索
    print("\n🔍 测试: 关键词搜索")
    result = fetcher.fetch_by_keyword("诈骗", Platform.XIAOHONGSHU, max_results=5)
    print(f"✅ 搜索到 {result.total_results} 条结果")
    
    # 测试3: 用户行为分析
    print("\n📊 测试: 用户行为分析")
    user_result = fetcher.fetch_by_username("testuser", Platform.XIAOHONGSHU)
    behavior = fetcher.analyze_user_behavior(user_result)
    print(f"✅ 发帖频率: {behavior['posting_frequency']:.2f} 条/天")
    print(f"   平均互动: {behavior['avg_engagement']:.1f}")
    print(f"   可疑模式: {behavior['suspicious_patterns']}")
    
    # 测试4: 跨平台追踪
    print("\n🌐 测试: 跨平台追踪")
    traces = fetcher.track_network_traces("testuser", Platform.XIAOHONGSHU)
    print(f"✅ 跨平台账户: {traces['accounts_found']} 个")
    print(f"   跨平台活跃: {traces['cross_platform_activity']}")


def test_legal_database_fetcher():
    """测试法律数据库查询"""
    print("\n" + "=" * 60)
    print("2️⃣ 法律数据库查询测试")
    print("=" * 60)
    
    fetcher = LegalDatabaseFetcher()
    
    # 测试1: 搜索相似案例
    print("\n📚 测试: 搜索相似案例")
    description = "对方在小红书发布虚假信息，称我店铺诈骗，损害我的名誉。"
    result = fetcher.search_similar_cases(description, CaseType.DEFAMATION, max_results=3)
    print(f"✅ 找到 {result.total_cases} 个相似案例")
    for i, case in enumerate(result.cases[:3], 1):
        print(f"   {i}. {case.case_name} (相似度: {case.similarity_score:.2f})")
    
    # 测试2: 查询法律条文
    print("\n📖 测试: 查询法律条文")
    result = fetcher.query_legal_provisions(["名誉", "侵权", "赔偿"], max_results=5)
    print(f"✅ 找到 {result.total_provisions} 条相关法律")
    for i, provision in enumerate(result.provisions[:3], 1):
        print(f"   {i}. {provision.law_name} {provision.article}")
    
    # 测试3: 获取统计数据
    print("\n📊 测试: 获取案件统计")
    result = fetcher.get_case_statistics(CaseType.DEFAMATION)
    if result.statistics:
        stats = result.statistics
        print(f"✅ 总案例数: {stats.total_cases}")
        print(f"   原告胜率: {stats.plaintiff_win_rate * 100:.1f}%")
        print(f"   平均赔偿: {stats.avg_compensation:.0f}元")
    
    # 测试4: 预测结果
    print("\n🎯 测试: 预测案件结果")
    prediction = fetcher.predict_outcome(description, CaseType.DEFAMATION)
    print(f"✅ 胜诉概率: {prediction['win_probability']}%")
    print(f"   预期结果: {prediction['expected_outcome']}")
    print(f"   预估赔偿: {prediction['estimated_compensation']:.0f}元")
    print(f"   置信度: {prediction['confidence']}%")


def test_multimedia_analyzer():
    """测试多媒体分析"""
    print("\n" + "=" * 60)
    print("3️⃣ 多媒体分析测试")
    print("=" * 60)
    
    analyzer = MultimediaAnalyzer()
    
    # 测试1: 分析聊天记录截图
    print("\n📸 测试: 分析聊天记录截图")
    result = analyzer.analyze_image(
        image_path="wechat_chat_record.png",
        enable_ocr=True
    )
    print(f"✅ 媒体ID: {result.media_id}")
    print(f"   图片类型: {result.image_type.value}")
    print(f"   OCR文本长度: {len(result.text_content)} 字符")
    print(f"   置信度: {result.confidence}")
    
    # 测试2: 分析交易记录
    print("\n💰 测试: 分析交易记录")
    result = analyzer.analyze_image(
        image_path="payment_record.jpg",
        enable_ocr=True
    )
    print(f"✅ 媒体ID: {result.media_id}")
    print(f"   图片类型: {result.image_type.value}")
    print(f"   置信度: {result.confidence}")
    
    # 测试3: 分析音频
    print("\n🎤 测试: 分析音频")
    result = analyzer.analyze_audio(audio_path="call_recording.mp3")
    print(f"✅ 媒体ID: {result.media_id}")
    print(f"   时长: {result.duration}秒")
    print(f"   说话人数: {result.speaker_count}")
    print(f"   关键短语: {result.key_phrases}")
    
    # 测试4: 批量分析
    print("\n📦 测试: 批量分析")
    files = [
        {"path": "chat.png", "type": "image"},
        {"path": "payment.jpg", "type": "image"},
        {"path": "call.mp3", "type": "audio"}
    ]
    batch_result = analyzer.analyze_batch(files)
    print(f"✅ 批次ID: {batch_result.batch_id}")
    print(f"   处理文件: {batch_result.processed_files}/{batch_result.total_files}")
    print(f"   摘要: {batch_result.summary}")
    
    # 测试5: 提取证据
    print("\n🔍 测试: 从媒体提取证据")
    payment_result = analyzer.analyze_image(image_path="payment_record.jpg")
    evidence = analyzer.extract_evidence_from_media(payment_result)
    print(f"✅ 证据类型: {evidence['evidence_type']}")
    print(f"   提取金额: {evidence['amount']}")
    print(f"   置信度: {evidence['confidence']}")


def test_integration():
    """集成测试 - 模拟完整流程"""
    print("\n" + "=" * 60)
    print("4️⃣ 集成测试")
    print("=" * 60)
    
    print("\n🔗 测试: 完整分析流程")
    
    # 场景: 小红书诽谤案件
    
    # 1. 获取对方社交媒体数据
    print("\n[步骤1] 获取对方社交媒体数据...")
    sm_fetcher = SocialMediaFetcher()
    sm_result = sm_fetcher.fetch_by_username("suspect_user", Platform.XIAOHONGSHU)
    print(f"✅ 获取到 {sm_result.total_results} 条帖子")
    
    # 2. 分析用户行为
    print("\n[步骤2] 分析用户行为模式...")
    behavior = sm_fetcher.analyze_user_behavior(sm_result)
    print(f"✅ 发帖频率: {behavior['posting_frequency']:.2f} 条/天")
    print(f"   可疑模式: {behavior['suspicious_patterns']}")
    
    # 3. 查询相似法律案例
    print("\n[步骤3] 查询相似法律案例...")
    legal_fetcher = LegalDatabaseFetcher()
    description = "对方在小红书发布虚假信息，称我店铺诈骗，损害我的名誉。"
    similar_cases = legal_fetcher.search_similar_cases(description, CaseType.DEFAMATION)
    print(f"✅ 找到 {similar_cases.total_cases} 个相似案例")
    
    # 4. 查询相关法律条文
    print("\n[步骤4] 查询相关法律条文...")
    provisions = legal_fetcher.query_legal_provisions(["名誉", "侵权"])
    print(f"✅ 找到 {provisions.total_provisions} 条相关法律")
    
    # 5. 预测案件结果
    print("\n[步骤5] 预测案件结果...")
    prediction = legal_fetcher.predict_outcome(description, CaseType.DEFAMATION)
    print(f"✅ 胜诉概率: {prediction['win_probability']}%")
    print(f"   预估赔偿: {prediction['estimated_compensation']:.0f}元")
    
    # 6. 分析证据材料
    print("\n[步骤6] 分析证据材料...")
    mm_analyzer = MultimediaAnalyzer()
    files = [
        {"path": "xiaohongshu_post_screenshot.png", "type": "image"},
        {"path": "payment_record.jpg", "type": "image"}
    ]
    batch_result = mm_analyzer.analyze_batch(files)
    print(f"✅ 分析了 {batch_result.processed_files} 个文件")
    
    print("\n✅ 集成测试完成!")


if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("🚀 AI Detective - 外部数据获取模块测试")
    print("=" * 60)
    
    try:
        test_social_media_fetcher()
        test_legal_database_fetcher()
        test_multimedia_analyzer()
        test_integration()
        
        print("\n" + "=" * 60)
        print("🎉 所有测试通过!")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
