def test_get_tags(client):
    """测试获取标签列表"""
    response = client.get("/api/tags")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_create_tag(client):
    """测试创建标签"""
    tag_data = {
        "name": "test-tag",
        "category": "genre",
        "color": "270 60% 55%"
    }
    
    response = client.post("/api/tags", json=tag_data)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "test-tag"
    assert data["category"] == "genre"
    assert data["color"] == "270 60% 55%"


def test_update_tag(client):
    """测试更新标签"""
    # 先创建一个标签
    tag_data = {
        "name": "update-test",
        "category": "genre",
        "color": "270 60% 55%"
    }
    response = client.post("/api/tags", json=tag_data)
    tag_id = response.json()["id"]
    
    # 更新该标签
    update_data = {
        "name": "updated-tag",
        "color": "120 60% 55%"
    }
    response = client.put(f"/api/tags/{tag_id}", json=update_data)
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == tag_id
    assert data["name"] == "updated-tag"
    assert data["color"] == "120 60% 55%"


def test_delete_tag(client):
    """测试删除标签"""
    # 先创建一个标签
    tag_data = {
        "name": "delete-test",
        "category": "genre",
        "color": "270 60% 55%"
    }
    response = client.post("/api/tags", json=tag_data)
    tag_id = response.json()["id"]
    
    # 删除该标签
    response = client.delete(f"/api/tags/{tag_id}")
    assert response.status_code == 200
    assert response.json()["success"] == True


def test_rename_tag(client):
    """测试重命名标签"""
    # 先创建一个标签
    tag_data = {
        "name": "old-name",
        "category": "genre",
        "color": "270 60% 55%"
    }
    response = client.post("/api/tags", json=tag_data)
    
    # 重命名标签
    rename_data = {
        "old_name": "old-name",
        "new_name": "new-name"
    }
    response = client.post("/api/tags/rename", json=rename_data)
    assert response.status_code == 200
    assert response.json()["success"] == True


def test_merge_tags(client):
    """测试合并标签"""
    # 先创建两个标签
    tag1 = {
        "name": "tag1",
        "category": "genre",
        "color": "270 60% 55%"
    }
    client.post("/api/tags", json=tag1)
    
    tag2 = {
        "name": "tag2",
        "category": "genre",
        "color": "120 60% 55%"
    }
    client.post("/api/tags", json=tag2)
    
    # 合并标签
    merge_data = {
        "source_names": ["tag1", "tag2"],
        "target_name": "merged-tag"
    }
    response = client.post("/api/tags/merge", json=merge_data)
    assert response.status_code == 200
    assert response.json()["success"] == True


def test_bulk_delete_tags(client):
    """测试批量删除标签"""
    # 先创建两个标签
    tag1 = {
        "name": "bulk1",
        "category": "genre",
        "color": "270 60% 55%"
    }
    client.post("/api/tags", json=tag1)
    
    tag2 = {
        "name": "bulk2",
        "category": "genre",
        "color": "120 60% 55%"
    }
    client.post("/api/tags", json=tag2)
    
    # 批量删除
    bulk_delete_data = {
        "names": ["bulk1", "bulk2"]
    }
    response = client.post("/api/tags/bulk-delete", json=bulk_delete_data)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] == True
    assert data["count"] == 2


def test_change_tag_category(client):
    """测试更改标签分类"""
    # 先创建一个标签
    tag_data = {
        "name": "category-test",
        "category": "genre",
        "color": "270 60% 55%"
    }
    client.post("/api/tags", json=tag_data)
    
    # 更改分类
    change_data = {
        "tag_name": "category-test",
        "new_category": "quality"
    }
    response = client.post("/api/tags/change-category", json=change_data)
    assert response.status_code == 200
    assert response.json()["success"] == True
