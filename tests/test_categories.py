def test_get_categories(client):
    """测试获取分类列表"""
    response = client.get("/api/categories")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_create_category(client):
    """测试创建分类"""
    category_data = {
        "key": "test-category",
        "label": "测试分类",
        "emoji": "🧪",
        "color": "270 60% 55%"
    }
    
    response = client.post("/api/categories", json=category_data)
    assert response.status_code == 200
    data = response.json()
    assert data["key"] == "test-category"
    assert data["label"] == "测试分类"
    assert data["emoji"] == "🧪"
    assert data["color"] == "270 60% 55%"
    assert data["built_in"] == False


def test_update_category(client):
    """测试更新分类"""
    # 先创建一个分类
    category_data = {
        "key": "update-test",
        "label": "更新测试",
        "emoji": "🔄",
        "color": "270 60% 55%"
    }
    response = client.post("/api/categories", json=category_data)
    category_id = response.json()["id"]
    
    # 更新该分类
    update_data = {
        "label": "已更新分类",
        "emoji": "✅",
        "color": "120 60% 55%"
    }
    response = client.put(f"/api/categories/{category_id}", json=update_data)
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == category_id
    assert data["label"] == "已更新分类"
    assert data["emoji"] == "✅"
    assert data["color"] == "120 60% 55%"


def test_delete_category(client):
    """测试删除分类"""
    # 先创建一个分类
    category_data = {
        "key": "delete-test",
        "label": "删除测试",
        "emoji": "🗑️",
        "color": "270 60% 55%"
    }
    response = client.post("/api/categories", json=category_data)
    category_id = response.json()["id"]
    
    # 删除该分类
    response = client.delete(f"/api/categories/{category_id}")
    assert response.status_code == 200
    assert response.json()["success"] == True


def test_seed_default_data(client):
    """测试初始化默认数据"""
    response = client.post("/api/categories/seed")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] == True
    assert "Default data seeded successfully" in data["message"]
