import os
import shutil
from typing import Optional, Tuple
from pathlib import Path

from app.config import settings


class StorageService:
    @staticmethod
    def get_absolute_media_dir() -> str:
        """获取媒体目录的绝对路径"""
        # 确保使用绝对路径
        if not os.path.isabs(settings.MEDIA_DIR):
            # 获取当前文件的目录，然后向上两级到backend目录
            current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            return os.path.join(current_dir, settings.MEDIA_DIR)
        return settings.MEDIA_DIR

    @staticmethod
    def ensure_directories() -> None:
        """确保存储目录存在"""
        media_dir = StorageService.get_absolute_media_dir()
        os.makedirs(media_dir, exist_ok=True)

    @staticmethod
    def save_uploaded_file(file, filename: str) -> Tuple[str, str]:
        """保存上传的文件
        
        Args:
            file: 上传的文件对象
            filename: 文件名（可能包含路径，如 "folder/subfolder/file.mp4"）
            
        Returns:
            Tuple[str, str]: (文件路径, 文件名)
        """
        StorageService.ensure_directories()
        
        # 提取纯文件名，去掉路径（处理文件夹上传的情况）
        # 例如："Movies/2023/film.mp4" -> "film.mp4"
        # 例如："Movies\\2023\\film.mp4" -> "film.mp4"
        pure_filename = Path(filename).name
        
        # 生成唯一文件名，保留原始文件名的主体部分
        import uuid
        unique_id = str(uuid.uuid4())
        name, ext = os.path.splitext(pure_filename)
        # 构建新文件名：原始文件名 + _ + UUID + 扩展名
        unique_filename = f"{name}_{unique_id[:8]}{ext}"
        
        # 保存文件
        media_dir = StorageService.get_absolute_media_dir()
        file_path = os.path.join(media_dir, unique_filename)
        
        try:
            # 尝试使用 shutil 复制文件对象
            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
        except Exception as e:
            # 尝试另一种方式，直接读取文件内容
            try:
                content = file.file.read()
                with open(file_path, "wb") as buffer:
                    buffer.write(content)
            except Exception as e2:
                raise Exception(f"文件保存失败: {str(e2)}")
        
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
            media_dir = StorageService.get_absolute_media_dir()
            full_path = os.path.join(media_dir, filename)
            
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
        media_dir = StorageService.get_absolute_media_dir()
        full_path = os.path.join(media_dir, filename)
        if os.path.exists(full_path):
            return full_path
        return None