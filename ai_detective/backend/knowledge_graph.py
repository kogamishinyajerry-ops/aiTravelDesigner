"""
知识图谱构建和可视化模块
Knowledge Graph Builder and Visualizer
构建案件知识图谱并生成可视化数据
"""

from typing import List, Dict, Any, Optional, Set, Tuple
from dataclasses import dataclass
from datetime import datetime
import json

from entity_extractor import Entity, EntityExtractor
from relation_extractor import Relation, RelationExtractor


@dataclass
class Node:
    """图谱节点"""
    id: str  # 节点ID
    type: str  # 节点类型
    text: str  # 节点文本
    confidence: float  # 置信度
    attributes: Dict[str, Any]  # 额外属性
    importance: float = 0.0  # 重要性评分


@dataclass
class Edge:
    """图谱边"""
    id: str  # 边ID
    source: str  # 源节点ID
    target: str  # 目标节点ID
    relation: str  # 关系类型
    confidence: float  # 置信度
    weight: float = 1.0  # 权重


@dataclass
class KnowledgeGraph:
    """知识图谱"""
    timestamp: datetime
    nodes: List[Node]  # 节点列表
    edges: List[Edge]  # 边列表
    key_nodes: List[str]  # 关键节点ID
    key_edges: List[str]  # 关键边ID
    stats: Dict[str, Any]  # 统计信息


class KnowledgeGraphBuilder:
    """知识图谱构建器"""
    
    def __init__(self):
        self.entity_extractor = EntityExtractor()
        self.relation_extractor = RelationExtractor()
    
    def build(self, text: str) -> KnowledgeGraph:
        """
        构建知识图谱
        
        Args:
            text: 案件描述文本
        
        Returns:
            知识图谱
        """
        # 1. 提取实体
        entity_result = self.entity_extractor.extract(text)
        
        # 2. 提取关系
        relation_result = self.relation_extractor.extract(text, entity_result.entities)
        
        # 3. 转换为图谱节点和边
        nodes = self._entities_to_nodes(entity_result.entities)
        edges = self._relations_to_edges(relation_result.relations)
        
        # 4. 计算节点重要性
        self._calculate_node_importance(nodes, edges)
        
        # 5. 确定关键节点
        key_nodes = self._identify_key_nodes(nodes)
        
        # 6. 确定关键边
        key_edges = self._identify_key_edges(edges)
        
        # 7. 计算统计信息
        stats = self._calculate_stats(nodes, edges)
        
        return KnowledgeGraph(
            timestamp=datetime.now(),
            nodes=nodes,
            edges=edges,
            key_nodes=key_nodes,
            key_edges=key_edges,
            stats=stats
        )
    
    def _entities_to_nodes(self, entities: List[Entity]) -> List[Node]:
        """将实体转换为节点"""
        nodes = []
        node_map = {}  # 用于去重
        
        for entity in entities:
            # 去重: 相同文本和类型的实体只保留一个
            key = f"{entity.type}_{entity.text}"
            if key in node_map:
                # 更新现有节点的置信度（取最大值）
                node_map[key].confidence = max(node_map[key].confidence, entity.confidence)
                continue
            
            node = Node(
                id=entity.id,
                type=entity.type,
                text=entity.text,
                confidence=entity.confidence,
                attributes=entity.attributes,
                importance=0.0
            )
            nodes.append(node)
            node_map[key] = node
        
        return nodes
    
    def _relations_to_edges(self, relations: List[Relation]) -> List[Edge]:
        """将关系转换为边"""
        edges = []
        edge_map = {}  # 用于去重
        
        for relation in relations:
            # 去重: 相同源节点、目标节点和关系类型的边只保留一个
            key = f"{relation.source}_{relation.target}_{relation.relation}"
            if key in edge_map:
                # 更新现有边的置信度（取最大值）
                edge_map[key].confidence = max(edge_map[key].confidence, relation.confidence)
                continue
            
            edge = Edge(
                id=relation.id,
                source=relation.source,
                target=relation.target,
                relation=relation.relation,
                confidence=relation.confidence
            )
            edges.append(edge)
            edge_map[key] = edge
        
        return edges
    
    def _calculate_node_importance(self, nodes: List[Node], edges: List[Edge]):
        """计算节点重要性（基于度中心性）"""
        # 统计每个节点的连接数（度）
        node_degree = {}
        for edge in edges:
            node_degree[edge.source] = node_degree.get(edge.source, 0) + 1
            node_degree[edge.target] = node_degree.get(edge.target, 0) + 1
        
        # 归一化并赋值
        if node_degree:
            max_degree = max(node_degree.values())
            for node in nodes:
                degree = node_degree.get(node.id, 0)
                if max_degree > 0:
                    node.importance = degree / max_degree
                else:
                    node.importance = 0.0
        else:
            for node in nodes:
                node.importance = 0.0
    
    def _identify_key_nodes(self, nodes: List[Node]) -> List[str]:
        """识别关键节点"""
        # 按重要性和置信度排序
        sorted_nodes = sorted(
            nodes,
            key=lambda n: (n.importance, n.confidence),
            reverse=True
        )
        
        # 选择重要性>0.3的前5个节点
        key_nodes = [
            n.id for n in sorted_nodes[:5]
            if n.importance > 0.3 or n.confidence > 0.8
        ]
        
        return key_nodes
    
    def _identify_key_edges(self, edges: List[Edge]) -> List[str]:
        """识别关键边"""
        # 按置信度和权重排序
        sorted_edges = sorted(
            edges,
            key=lambda e: (e.confidence, e.weight),
            reverse=True
        )
        
        # 选择置信度>0.7的前5条边
        key_edges = [
            e.id for e in sorted_edges[:5]
            if e.confidence > 0.7
        ]
        
        return key_edges
    
    def _calculate_stats(self, nodes: List[Node], edges: List[Edge]) -> Dict[str, Any]:
        """计算统计信息"""
        stats = {
            "node_count": len(nodes),
            "edge_count": len(edges),
            "density": 0.0,
            "node_types": {},
            "relation_types": {}
        }
        
        # 计算图密度
        if len(nodes) > 1:
            max_edges = len(nodes) * (len(nodes) - 1) / 2
            stats["density"] = len(edges) / max_edges if max_edges > 0 else 0.0
        
        # 统计节点类型
        for node in nodes:
            stats["node_types"][node.type] = stats["node_types"].get(node.type, 0) + 1
        
        # 统计关系类型
        for edge in edges:
            stats["relation_types"][edge.relation] = stats["relation_types"].get(edge.relation, 0) + 1
        
        return stats
    
    def discover_implicit_relations(self, graph: KnowledgeGraph,
                                 max_depth: int = 2) -> List[Dict[str, Any]]:
        """
        发现隐含关系（基于路径分析）
        
        Args:
            graph: 知识图谱
            max_depth: 最大路径深度
        
        Returns:
            隐含关系列表
        """
        implicit_relations = []
        
        # 构建邻接表
        adj_list = {}
        for edge in graph.edges:
            if edge.source not in adj_list:
                adj_list[edge.source] = []
            if edge.target not in adj_list:
                adj_list[edge.target] = []
            
            adj_list[edge.source].append(edge.target)
            adj_list[edge.target].append(edge.source)
        
        # 查找长度为2-3的路径
        for edge1 in graph.edges:
            for edge2 in graph.edges:
                # 跳过自环和重复边
                if edge1 == edge2:
                    continue
                
                # 查找2跳路径: A -> B -> C
                if edge1.target == edge2.source and edge1.source != edge2.target:
                    implicit_relations.append({
                        "path": [edge1.source, edge1.target, edge2.target],
                        "relations": [edge1.relation, edge2.relation],
                        "type": "2_hop",
                        "confidence": min(edge1.confidence, edge2.confidence) * 0.8
                    })
                
                # 查找3跳路径: A -> B -> C -> D
                if max_depth >= 3:
                    for edge3 in graph.edges:
                        if (edge1.target == edge2.source and 
                            edge2.target == edge3.source and 
                            edge1.source != edge3.target):
                            implicit_relations.append({
                                "path": [edge1.source, edge1.target, edge2.target, edge3.target],
                                "relations": [edge1.relation, edge2.relation, edge3.relation],
                                "type": "3_hop",
                                "confidence": min(edge1.confidence, edge2.confidence, edge3.confidence) * 0.6
                            })
        
        # 去重并排序
        unique_relations = {}
        for rel in implicit_relations:
            key = "_".join(rel["path"])
            if key not in unique_relations or rel["confidence"] > unique_relations[key]["confidence"]:
                unique_relations[key] = rel
        
        sorted_relations = sorted(
            unique_relations.values(),
            key=lambda r: r["confidence"],
            reverse=True
        )
        
        return sorted_relations[:10]  # 返回前10个
    
    def find_critical_path(self, graph: KnowledgeGraph) -> Optional[Dict[str, Any]]:
        """
        查找关键路径（基于权重和重要性）
        
        Args:
            graph: 知识图谱
        
        Returns:
            关键路径信息
        """
        if not graph.edges:
            return None
        
        # 构建邻接表
        adj_list = {}
        for edge in graph.edges:
            if edge.source not in adj_list:
                adj_list[edge.source] = []
            adj_list[edge.source].append({
                "target": edge.target,
                "weight": edge.confidence
            })
        
        # 找到重要性最高的节点作为起点
        key_node_id = None
        max_importance = 0
        for node in graph.nodes:
            if node.importance > max_importance:
                max_importance = node.importance
                key_node_id = node.id
        
        if not key_node_id:
            return None
        
        # 使用DFS查找最长路径（基于权重）
        visited = set()
        path = []
        max_path = []
        max_weight = 0
        
        def dfs(current_id: str, current_weight: float, current_path: List[str]):
            nonlocal max_weight, max_path
            
            visited.add(current_id)
            current_path.append(current_id)
            
            # 检查是否需要更新最大路径
            if current_weight > max_weight:
                max_weight = current_weight
                max_path = current_path.copy()
            
            # 继续DFS
            if current_id in adj_list:
                for neighbor in adj_list[current_id]:
                    if neighbor["target"] not in visited:
                        dfs(neighbor["target"],
                             current_weight + neighbor["weight"],
                             current_path)
            
            # 回溯
            current_path.pop()
            visited.remove(current_id)
        
        dfs(key_node_id, 0, path)
        
        if max_path:
            return {
                "path": max_path,
                "total_weight": max_weight,
                "length": len(max_path) - 1
            }
        
        return None


def build_knowledge_graph(text: str) -> Dict[str, Any]:
    """
    便捷函数: 构建知识图谱
    
    Args:
        text: 案件描述文本
    
    Returns:
        知识图谱字典
    """
    builder = KnowledgeGraphBuilder()
    graph = builder.build(text)
    
    return {
        "nodes": [
            {
                "id": n.id,
                "type": n.type,
                "text": n.text,
                "confidence": n.confidence,
                "importance": n.importance,
                "is_key": n.id in graph.key_nodes
            }
            for n in graph.nodes
        ],
        "edges": [
            {
                "id": e.id,
                "source": e.source,
                "target": e.target,
                "relation": e.relation,
                "confidence": e.confidence,
                "weight": e.weight,
                "is_key": e.id in graph.key_edges
            }
            for e in graph.edges
        ],
        "key_nodes": graph.key_nodes,
        "key_edges": graph.key_edges,
        "stats": graph.stats,
        "timestamp": graph.timestamp.isoformat()
    }


if __name__ == "__main__":
    # 测试
    test_text = """
    今年12月15日下午3点左右,一个女生来到我的店铺。
    她在店里待了大约1个小时,大概4点左右支付了400余元。
    支付后她立刻要求退款,双方发生争执。
    对方现场报警并拍照取证。
    晚上6点47分,她在小红书发布了一篇笔记,称店铺诈骗。
    第二天,我收到了行政处罚。
    """
    
    graph = build_knowledge_graph(test_text)
    print("知识图谱构建结果:")
    print(f"  节点数: {graph['stats']['node_count']}")
    print(f"  边数: {graph['stats']['edge_count']}")
    print(f"  图密度: {graph['stats']['density']:.3f}")
    print(f"  节点类型: {graph['stats']['node_types']}")
    print(f"  关系类型: {graph['stats']['relation_types']}")
    print(f"  关键节点: {graph['key_nodes']}")
    print(f"  关键边: {graph['key_edges']}")
    
    builder = KnowledgeGraphBuilder()
    from dataclasses import dataclass
    # 重新构建图谱对象
    graph_obj = builder.build(test_text)
    
    print("\n隐含关系:")
    implicit_relations = builder.discover_implicit_relations(graph_obj)
    for rel in implicit_relations[:5]:
        print(f"  • {' -> '.join(rel['path'])} (置信度: {rel['confidence']:.2f})")
    
    print("\n关键路径:")
    critical_path = builder.find_critical_path(graph_obj)
    if critical_path:
        print(f"  • 路径: {' -> '.join(critical_path['path'])}")
        print(f"  • 权重: {critical_path['total_weight']:.2f}")
        print(f"  • 长度: {critical_path['length']}")
