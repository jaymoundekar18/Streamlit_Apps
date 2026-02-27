import requests
from core.config import API_BASE_URL


class APIClient:

    TIMEOUT = 15 
    headers = {
        "Content-Type": "application/json"
    }

    @staticmethod
    def _handle_response(response):
        if response.status_code in (200, 201):
            return response.json()

        if response.status_code == 422:
            return {"error": f"Validation Error: {response.json()}"}

        if response.status_code == 401:
            return {"error": response.text}

        return {"error": f"Error {response.status_code}: {response.text}"}

    @staticmethod
    def _safe_request(method, url, **kwargs):
        try:
            response = requests.request(
                method=method,
                url=url,
                timeout=APIClient.TIMEOUT,
                headers=APIClient.headers,
                **kwargs
            )
            return APIClient._handle_response(response)

        except requests.exceptions.ReadTimeout:
            return {"error": "Server is waking up. Please try again in a few seconds."}

        except requests.exceptions.ConnectionError:
            return {"error": "Unable to connect to server. Please check your connection."}

        except requests.exceptions.RequestException as e:
            return {"error": f"Network error: {str(e)}"}

    @staticmethod
    def create_user(data: dict):
        return APIClient._safe_request(
            "POST",
            f"{API_BASE_URL}/users",
            json=data
        )

    @staticmethod
    def update_user(user_id: str, data: dict):
        return APIClient._safe_request(
            "PATCH",
            f"{API_BASE_URL}/users/{user_id}",
            json=data
        )

    @staticmethod
    def get_user(user_id: str):
        return APIClient._safe_request(
            "GET",
            f"{API_BASE_URL}/users/id{user_id}" 
        )

    @staticmethod
    def get_byusername(username: str):
        return APIClient._safe_request(
            "GET",
            f"{API_BASE_URL}/users/username{username}"  
        )

    @staticmethod
    def delete_user_account(user_id: str):
        return APIClient._safe_request(
            "DELETE",
            f"{API_BASE_URL}/users/{user_id}"
        )

    @staticmethod
    def authenticate_user(username: str, password: str):
        return APIClient._safe_request(
            "POST",
            f"{API_BASE_URL}/login",
            json={"username": username, "password": password}
        )

    @staticmethod
    def add_book(user_id: str, data: dict):
        return APIClient._safe_request(
            "POST",
            f"{API_BASE_URL}/users/{user_id}/books",
            json=data
        )

    @staticmethod
    def get_userBookData(user_id: str):
        return APIClient._safe_request(
            "GET",
            f"{API_BASE_URL}/users/{user_id}/books"
        )

    @staticmethod
    def get_userBookDataByIndex(user_id: str, bookIndex: int):
        return APIClient._safe_request(
            "GET",
            f"{API_BASE_URL}/users/{user_id}/books/{bookIndex}"
        )

    @staticmethod
    def get_userBookNames(user_id: str):
        return APIClient._safe_request(
            "GET",
            f"{API_BASE_URL}/users/{user_id}/booknames"
        )

    @staticmethod
    def update_userBookData(user_id: str, bookIndex: int, data: dict):
        return APIClient._safe_request(
            "PUT",
            f"{API_BASE_URL}/users/{user_id}/books/{bookIndex}",
            json=data
        )