import os
import shutil
from typing import Optional, Tuple
from pathlib import Path

from app.config import settings


class StorageService:
    @staticmethod
    def ensure_directories() -> None:
        """确保存储目录存在"""
        os.makedirs(settings.MEDIA_DIR, exist_ok=True)
        os.makedirs(settings.UPLOAD_DIR, exist_ok=True)

    @staticmethod
    def save_uploaded_file(file, filename: str) -> Tuple[str, str]:
        """保存上传的文件
        
        Args:
            file: 上传的文件对象
            filename: 文件名
            
        Returns:
            Tuple[str, str]: (文件路径, 文件名)
        """
        StorageService.ensure_directories()
        
        # 生成唯一文件名
        import uuid
        unique_id = str(uuid.uuid4())
        ext = os.path.splitext(filename)[1]
        unique_filename = f"{unique_id}{ext}"
        
        # 保存文件
        file_path = os.path.join(settings.MEDIA_DIR, unique_filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # 返回相对路径和文件名
        relative_path = f"/media/{unique_filename}"
        return relative_path, unique_filename

    @staticmethod
    def delete_file(file_path: str) -> bool:
        """删除文件
        
        Args:
            file_path: 文件路径
            
        Returns:
            bool: 是否删除成功
        """
        try:
            # 提取文件名
            filename = os.path.basename(file_path)
            full_path = os.path.join(settings.MEDIA_DIR, filename)
            
            if os.path.exists(full_path):
                os.remove(full_path)
                return True
            return False
        except Exception:
            return False

    @staticmethod
    def get_file_path(filename: str) -> Optional[str]:
        """获取文件的完整路径
        
        Args:
            filename: 文件名
            
        Returns:
            Optional[str]: 文件的完整路径
        """
        full_path = os.path.join(settings.MEDIA_DIR, filename)
        if os.path.exists(full_path):
            return full_path
        return None