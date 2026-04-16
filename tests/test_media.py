def test_get_media_items(client):
    """测试获取媒体文件列表"""
    response = client.get("/api/media")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_create_media_item(client):
    """测试创建媒体文件"""
    media_data = {
        "filename": "test.mp4",
        "path": "/media/test.mp4",
        "tags": ["action", "2023"],
        "year": 2023,
        "resolution": "1080p"
    }
    
    response = client.post("/api/media", json=media_data)
    assert response.status_code == 200
    data = response.json()
    assert data["filename"] == "test.mp4"
    assert "action" in data["tags"]
    assert "2023" in data["tags"]
    assert data["year"] == 2023
    assert data["resolution"] == "1080p"


def test_get_media_item(client):
    """测试获取单个媒体文件"""
    # 先创建一个媒体文件
    media_data = {
        "filename": "test2.mp4",
        "path": "/media/test2.mp4",
        "tags": ["drama"]
    }
    response = client.post("/api/media", json=media_data)
    media_id = response.json()["id"]
    
    # 获取该媒体文件
    response = client.get(f"/api/media/{media_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == media_id
    assert data["filename"] == "test2.mp4"


def test_update_media_item(client):
    """测试更新媒体文件"""
    # 先创建一个媒体文件
    media_data = {
        "filename": "test3.mp4",
        "path": "/media/test3.mp4",
        "tags": ["action"]
    }
    response = client.post("/api/media", json=media_data)
    media_id = response.json()["id"]
    
    # 更新该媒体文件
    update_data = {
        "filename": "updated.mp4",
        "tags": ["action", "sci-fi"]
    }
    response = client.put(f"/api/media/{media_id}", json=update_data)
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == media_id
    assert data["filename"] == "updated.mp4"
    assert "sci-fi" in data["tags"]


def test_delete_media_item(client):
    """测试删除媒体文件"""
    # 先创建一个媒体文件
    media_data = {
        "filename": "test4.mp4",
        "path": "/media/test4.mp4",
        "tags": ["comedy"]
    }
    response = client.post("/api/media", json=media_data)
    media_id = response.json()["id"]
    
    # 删除该媒体文件
    response = client.delete(f"/api/media/{media_id}")
    assert response.status_code == 200
    assert response.json()["success"] == True
    
    # 验证删除成功
    response = client.get(f"/api/media/{media_id}")
    assert response.status_code == 404


def test_bulk_create_media_items(client):
    """测试批量创建媒体文件"""
    bulk_data = {
        "items": [
            {
                "filename": "batch1.mp4",
                "path": "/media/batch1.mp4",
                "tags": ["action"]
            },
            {
                "filename": "batch2.mp4",
                "path": "/media/batch2.mp4",
                "tags": ["drama"]
            }
        ]
    }
    
    response = client.post("/api/media/bulk", json=bulk_data)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] == True
    assert data["count"] == 2


def test_bulk_delete_media_items(client):
    """测试批量删除媒体文件"""
    # 先创建两个媒体文件
    media1 = {
        "filename": "bulk1.mp4",
        "path": "/media/bulk1.mp4",
        "tags": ["action"]
    }
    response1 = client.post("/api/media", json=media1)
    id1 = response1.json()["id"]
    
    media2 = {
        "filename": "bulk2.mp4",
        "path": "/media/bulk2.mp4",
        "tags": ["drama"]
    }
    response2 = client.post("/api/media", json=media2)
    id2 = response2.json()["id"]
    
    # 批量删除
    bulk_delete_data = {
        "ids": [id1, id2]
    }
    response = client.post("/api/media/bulk-delete", json=bulk_delete_data)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] == True
    assert data["count"] == 2


def test_add_tag_to_items(client):
    """测试为媒体文件添加标签"""
    # 先创建一个媒体文件
    media_data = {
        "filename": "tagtest.mp4",
        "path": "/media/tagtest.mp4",
        "tags": ["action"]
    }
    response = client.post("/api/media", json=media_data)
    media_id = response.json()["id"]
    
    # 添加标签
    add_tag_data = {
        "media_ids": [media_id],
        "tag_name": "sci-fi",
        "category": "genre"
    }
    response = client.post("/api/media/add-tag", json=add_tag_data)
    assert response.status_code == 200
    assert response.json()["success"] == True


def test_remove_tag_from_items(client):
    """测试从媒体文件移除标签"""
    # 先创建一个媒体文件
    media_data = {
        "filename": "removetag.mp4",
        "path": "/media/removetag.mp4",
        "tags": ["action", "sci-fi"]
    }
    response = client.post("/api/media", json=media_data)
    media_id = response.json()["id"]
    
    # 移除标签
    remove_tag_data = {
        "media_ids": [media_id],
        "tag_name": "sci-fi"
    }
    response = client.post("/api/media/remove-tag", json=remove_tag_data)
    assert response.status_code == 200
    assert response.json()["success"] == True
