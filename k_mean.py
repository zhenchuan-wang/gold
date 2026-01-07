# k-means聚类算法实现，不使用numpy
import random
import math


def euclidean_distance(point1, point2):
    """计算两个点之间的欧氏距离。"""
    return math.sqrt(sum((a - b) ** 2 for a, b in zip(point1, point2)))


def initialize_centroids(data, k):
    """从数据中随机选择k个点作为初始中心点。"""
    return random.sample(data, k)


def assign_clusters(data, centroids):
    """将每个数据点分配到最近的中心点，返回簇列表。"""
    clusters = [[] for _ in range(len(centroids))]
    for point in data:
        # 计算点到每个中心点的距离
        distances = [euclidean_distance(point, centroid) for centroid in centroids]
        closest_centroid_index = distances.index(min(distances))
        clusters[closest_centroid_index].append(point)
    return clusters


def compute_centroid(cluster):
    """计算一个簇的中心点（均值）。"""
    if not cluster:  # 处理空簇，返回None
        return None
    # 对每个维度计算平均值
    dimensions = len(cluster[0])
    centroid = []
    for d in range(dimensions):
        dim_sum = sum(point[d] for point in cluster)
        centroid.append(dim_sum / len(cluster))
    return centroid


def update_centroids(clusters):
    """根据簇重新计算所有中心点，处理空簇。"""
    new_centroids = []
    for cluster in clusters:
        centroid = compute_centroid(cluster)
        if centroid is None:  # 空簇时，随机初始化一个中心点（简单处理）
            centroid = (
                [random.random() * 10 for _ in range(len(clusters[0][0]))]
                if clusters[0]
                else [0, 0]
            )
        new_centroids.append(centroid)
    return new_centroids


def kmeans(data, k, max_iters=100, tol=1e-4):
    """k-means主算法，不使用显式深拷贝的版本"""
    centroids = initialize_centroids(data, k)

    for iteration in range(max_iters):
        # 分配簇
        clusters = assign_clusters(data, centroids)

        # 计算新中心点
        new_centroids = update_centroids(clusters)

        # 检查是否收敛
        max_shift = 0
        for old, new in zip(centroids, new_centroids):
            shift = euclidean_distance(old, new)
            max_shift = max(max_shift, shift)

        centroids = new_centroids

        if max_shift < tol:
            print(f"在第 {iteration+1} 次迭代后收敛，最大移动距离: {max_shift:.6f}")
            break

    return centroids, clusters


# 测试用例
if __name__ == "__main__":
    # 示例数据：简单的二维点列表
    test_data = [
        [1, 2],
        [1, 4],
        [1, 0],
        [4, 2],
        [4, 4],
        [4, 0],
        [10, 10],
        [10, 12],  # 添加更多点以增加测试多样性
    ]
    k = 3
    centroids, clusters = kmeans(test_data, 2)

    print("最终中心点坐标:")
    for i, centroid in enumerate(centroids):
        print(f"中心点 {i}: {centroid}")

    print("\n簇分配结果:")
    for i, cluster in enumerate(clusters):
        print(f"簇 {i} 包含 {len(cluster)} 个点: {cluster}")
