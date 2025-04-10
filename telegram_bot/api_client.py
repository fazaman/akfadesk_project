import os
import json
import httpx
from dotenv import load_dotenv

# Загрузка переменных окружения
load_dotenv()

# Получение базового URL API из переменных окружения
API_URL = os.getenv('API_URL', 'http://localhost:8000/api/')

class ApiClient:
    """Клиент для взаимодействия с API бэкенда."""
    
    def __init__(self):
        self.base_url = API_URL
    
    async def get_tasks(self):
        """Получить список всех задач."""
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(f"{self.base_url}tasks/")
                if response.status_code == 200:
                    return response.json()
                return []
            except Exception as e:
                print(f"Ошибка при получении задач: {e}")
                return []
    
    async def get_task(self, task_id):
        """Получить задачу по ID."""
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(f"{self.base_url}tasks/{task_id}/")
                if response.status_code == 200:
                    return response.json()
                return None
            except Exception as e:
                print(f"Ошибка при получении задачи {task_id}: {e}")
                return None
    
    async def create_task(self, title, description=None):
        """Создать новую задачу."""
        data = {
            "title": title,
            "description": description
        }
        
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(
                    f"{self.base_url}tasks/",
                    json=data
                )
                if response.status_code in (201, 200):
                    return response.json()
                return None
            except Exception as e:
                print(f"Ошибка при создании задачи: {e}")
                return None
    
    async def update_task(self, task_id, data):
        """Обновить существующую задачу."""
        async with httpx.AsyncClient() as client:
            try:
                response = await client.patch(
                    f"{self.base_url}tasks/{task_id}/",
                    json=data
                )
                if response.status_code == 200:
                    return response.json()
                return None
            except Exception as e:
                print(f"Ошибка при обновлении задачи {task_id}: {e}")
                return None
    
    async def delete_task(self, task_id):
        """Удалить задачу."""
        async with httpx.AsyncClient() as client:
            try:
                response = await client.delete(f"{self.base_url}tasks/{task_id}/")
                return response.status_code in (204, 200)
            except Exception as e:
                print(f"Ошибка при удалении задачи {task_id}: {e}")
                return False 