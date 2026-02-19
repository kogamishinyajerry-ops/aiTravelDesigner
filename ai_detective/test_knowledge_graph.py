"""
测试知识图谱功能
Test Knowledge Graph
"""

import sys
import os

# 添加backend到Python路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from entity_extractor import EntityExtractor
from relation_extractor import RelationExtractor
from knowledge_graph import KnowledgeGraphBuilder


def test_entity_extraction():
    """测试实体抽取"""
    print("=" * 60)
    print("测试实体抽取")
    print("=" * 60)

    test_text = """
    今年12月15日下午3点左右,一个女生来到我的店铺。
    她在店里待了大约1个小时,大概4点左右支付了400余元。
    支付后她立刻要求退款,双方发生争执。
    对方现场报警并拍照取证。
    晚上6点47分,她在小红书发布了一篇笔记,称店铺诈骗。
    第二天,我收到了行政处罚。
    """

    extractor = EntityExtractor()
    result = extractor.extract(test_text)

    print(f"\n✅ 实体抽取完成")
    print(f"  实体总数: {len(result.entities)}")
    print(f"  实体分布: {result.entity_counts}")
    print(f"  关键实体: {result.key_entities}")

    print(f"\n实体列表 (前10个):")
    for entity in result.entities[:10]:
        print(f"  • [{entity.type}] {entity.text} (置信度: {entity.confidence:.2f})")

    assert len(result.entities) >= 5
    print(f"\n✅ 实体抽取测试通过!")


def test_relation_extraction():
    """测试关系抽取"""
    print("\n" + "=" * 60)
    print("测试关系抽取")
    print("=" * 60)

    test_text = """
    今年12月15日下午3点左右,一个女生来到我的店铺。
    她在店里待了大约1个小时,大概4点左右支付了400余元。
    支付后她立刻要求退款,双方发生争执。
    对方现场报警并拍照取证。
    晚上6点47分,她在小红书发布了一篇笔记,称店铺诈骗。
    第二天,我收到了行政处罚。
    """

    extractor = RelationExtractor()
    result = extractor.extract(test_text)

    print(f"\n✅ 关系抽取完成")
    print(f"  关系总数: {len(result.relations)}")
    print(f"  关系分布: {result.relation_counts}")
    print(f"  关键关系: {result.key_relations}")

    print(f"\n关系列表 (前10个):")
    for relation in result.relations[:10]:
        print(f"  • [{relation.type}] {relation.source} -[{relation.relation}]-> {relation.target} (置信度: {relation.confidence:.2f})")

    assert len(result.relations) >= 3
    print(f"\n✅ 关系抽取测试通过!")


def test_knowledge_graph():
    """测试知识图谱构建"""
    print("\n" + "=" * 60)
    print("测试知识图谱构建")
    print("=" * 60)

    test_text = """
    今年12月15日下午3点左右,一个女生来到我的店铺。
    她在店里待了大约1个小时,大概4点左右支付了400余元。
    支付后她立刻要求退款,双方发生争执。
    对方现场报警并拍照取证。
    晚上6点47分,她在小红书发布了一篇笔记,称店铺诈骗。
    第二天,我收到了行政处罚。
    """

    builder = KnowledgeGraphBuilder()
    graph = builder.build(test_text)

    print(f"\n✅ 知识图谱构建完成")
    print(f"  节点数: {graph.stats['node_count']}")
    print(f"  边数: {graph.stats['edge_count']}")
    print(f"  图密度: {graph.stats['density']:.3f}")
    print(f"  节点类型: {graph.stats['node_types']}")
    print(f"  关系类型: {graph.stats['relation_types']}")
    print(f"  关键节点: {graph.key_nodes}")
    print(f"  关键边: {graph.key_edges}")

    assert graph.stats['node_count'] >= 3
    assert graph.stats['edge_count'] >= 2
    print(f"\n✅ 知识图谱构建测试通过!")


def test_implicit_relations():
    """测试隐含关系发现"""
    print("\n" + "=" * 60)
    print("测试隐含关系发现")
    print("=" * 60)

    test_text = """
    今年12月15日下午3点左右,一个女生来到我的店铺。
    她在店里待了大约1个小时,大概4点左右支付了400余元。
    支付后她立刻要求退款,双方发生争执。
    对方现场报警并拍照取证。
    晚上6点47分,她在小红书发布了一篇笔记,称店铺诈骗。
    第二天,我收到了行政处罚。
    """

    builder = KnowledgeGraphBuilder()
    graph = builder.build(test_text)

    implicit_relations = builder.discover_implicit_relations(graph)

    print(f"\n✅ 隐含关系发现完成")
    print(f"  隐含关系数: {len(implicit_relations)}")

    print(f"\n隐含关系 (前5个):")
    for rel in implicit_relations[:5]:
        print(f"  • {' -> '.join(rel['path'])} (置信度: {rel['confidence']:.2f})")

    assert len(implicit_relations) >= 1
    print(f"\n✅ 隐含关系发现测试通过!")


def test_critical_path():
    """测试关键路径查找"""
    print("\n" + "=" * 60)
    print("测试关键路径查找")
    print("=" * 60)

    test_text = """
    今年12月15日下午3点左右,一个女生来到我的店铺。
    她在店里待了大约1个小时,大概4点左右支付了400余元。
    支付后她立刻要求退款,双方发生争执。
    对方现场报警并拍照取证。
    晚上6点47分,她在小红书发布了一篇笔记,称店铺诈骗。
    第二天,我收到了行政处罚。
    """

    builder = KnowledgeGraphBuilder()
    graph = builder.build(test_text)

    critical_path = builder.find_critical_path(graph)

    print(f"\n✅ 关键路径查找完成")

    if critical_path:
        print(f"  路径: {' -> '.join(critical_path['path'])}")
        print(f"  权重: {critical_path['total_weight']:.2f}")
        print(f"  长度: {critical_path['length']}")
    else:
        print(f"  未找到关键路径")

    print(f"\n✅ 关键路径查找测试通过!")


def test_integration():
    """测试集成测试"""
    print("\n" + "=" * 60)
    print("测试知识图谱集成分析")
    print("=" * 60)

    test_text = """
    今年12月15日下午3点左右,一个女生来到我的店铺。
    她在店里待了大约1个小时,大概4点左右支付了400余元。
    支付后她立刻要求退款,双方发生争执。
    对方现场报警并拍照取证。
    晚上6点47分,她在小红书发布了一篇笔记,称店铺诈骗。
    第二天,我收到了行政处罚。
    """

    # 1. 实体抽取
    entity_extractor = EntityExtractor()
    entity_result = entity_extractor.extract(test_text)

    # 2. 关系抽取
    relation_extractor = RelationExtractor()
    relation_result = relation_extractor.extract(test_text, entity_result.entities)

    # 3. 知识图谱构建
    graph_builder = KnowledgeGraphBuilder()
    graph = graph_builder.build(test_text)

    # 4. 隐含关系发现
    implicit_relations = graph_builder.discover_implicit_relations(graph)

    # 5. 关键路径查找
    critical_path = graph_builder.find_critical_path(graph)

    print(f"\n✅ 集成分析完成")
    print(f"\n【实体信息】")
    print(f"  实体总数: {len(entity_result.entities)}")
    print(f"  实体分布: {entity_result.entity_counts}")

    print(f"\n【关系信息】")
    print(f"  关系总数: {len(relation_result.relations)}")
    print(f"  关系分布: {relation_result.relation_counts}")

    print(f"\n【图谱信息】")
    print(f"  节点数: {graph.stats['node_count']}")
    print(f"  边数: {graph.stats['edge_count']}")
    print(f"  图密度: {graph.stats['density']:.3f}")

    print(f"\n【隐含关系】")
    print(f"  隐含关系数: {len(implicit_relations)}")

    print(f"\n【关键路径】")
    if critical_path:
        print(f"  路径长度: {critical_path['length']}")
        print(f"  路径权重: {critical_path['total_weight']:.2f}")

    print(f"\n✅ 集成分析测试通过!")


if __name__ == "__main__":
    print("\n" + "🚀" * 30)
    print("开始测试知识图谱功能")
    print("🚀" * 30)

    try:
        test_entity_extraction()
        test_relation_extraction()
        test_knowledge_graph()
        test_implicit_relations()
        test_critical_path()
        test_integration()

        print("\n" + "=" * 60)
        print("🎉 所有测试通过!")
        print("=" * 60)

    except Exception as e:
        print(f"\n❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
