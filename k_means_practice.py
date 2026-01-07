import random


def initialize_centroids(data, k):
    return random.sample(data, k)


def euclidean_distance(point1, point2):
    return sum((a - b) ** 2 for a, b in zip(point1, point2))


def assign_clusters(data, centroids):
    clusters = [[] for _ in range(len(centroids))]
    for point in data:
        distances = [euclidean_distance(point, centroid) for centroid in centroids]
        closest_centroid_index = distances.index(min(distances))
        clusters[closest_centroid_index].append(point)
    return clusters


def compute_centroid(cluster):
    dimensions = len(cluster[0])
    centroid = []
    for d in range(dimensions):
        dim_sum = sum(point[d] for point in cluster)
        centroid.append(dim_sum / len(cluster))
    return centroid


def update_centroids(clusters):
    return [compute_centroid(cluster) for cluster in clusters]


def kmeans(data, k, max_iters=100, tol=1e-4):
    centroids = initialize_centroids(data, k)
    for _ in range(max_iters):
        clusters = assign_clusters(data, centroids)
        new_centroids = update_centroids(clusters)
        max_shift = max(
            euclidean_distance(old, new) for old, new in zip(centroids, new_centroids)
        )
        centroids = new_centroids
        if max_shift < tol:
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
    centroids, clusters = kmeans(test_data, k)

    print("最终中心点坐标:")
    for i, centroid in enumerate(centroids):
        print(f"中心点 {i}: {centroid}")

    print("\n簇分配结果:")
    for i, cluster in enumerate(clusters):
        print(f"簇 {i} 包含 {len(cluster)} 个点: {cluster}")
