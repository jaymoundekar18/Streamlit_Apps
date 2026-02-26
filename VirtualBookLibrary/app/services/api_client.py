import requests
from core.config import API_BASE_URL

class APIClient:

    TIMEOUT = 10
    headers = {
    "Content-Type": "application/json"
    }

    @staticmethod
    def _handle_response(response):
        if response.status_code in (200, 201):
            return response.json()

        if response.status_code == 422:
            raise Exception(f"Validation Error: {response.json()}")

        if response.status_code == 401:
            return {"error": response.text}
        
        raise Exception(
            f"Error {response.status_code}: {response.text}"
        )

    @staticmethod
    def create_user(data: dict):
        response = requests.post(
            f"{API_BASE_URL}/users",
            json=data,
            timeout=APIClient.TIMEOUT, 
            headers=APIClient.headers
        )
        return APIClient._handle_response(response)

    @staticmethod
    def update_user(user_id: str, data: dict):
        response = requests.patch(
            f"{API_BASE_URL}/users/{user_id}",
            json=data,
            timeout=APIClient.TIMEOUT
        )
        return APIClient._handle_response(response)

    @staticmethod
    def get_user(user_id: str):
        response = requests.get(
            f"{API_BASE_URL}/users/id{user_id}",
            timeout=APIClient.TIMEOUT
        )
        return APIClient._handle_response(response)

    @staticmethod
    def authenticate_user(username: str, password: str):
        response = requests.post(
            f"{API_BASE_URL}/login",
            json={"username": username, "password": password},
            timeout=APIClient.TIMEOUT
        )
        return APIClient._handle_response(response)
    
    @staticmethod
    def get_byusername(username: str):
        response = requests.get(
            f"{API_BASE_URL}/users/username{username}",
            timeout=APIClient.TIMEOUT
        )
        return APIClient._handle_response(response)
    
    @staticmethod
    def delete_user_account(user_id: str):
        response = requests.delete(
            f"{API_BASE_URL}/users/{user_id}",
            timeout=APIClient.TIMEOUT
        )
        return APIClient._handle_response(response)

    @staticmethod
    def add_book(user_id:str, data:dict):
        response = requests.post(
            f"{API_BASE_URL}/users/{user_id}/books",
            json=data,
            timeout=APIClient.TIMEOUT
        )
        return APIClient._handle_response(response)

    @staticmethod
    def get_userBookData(user_id:str):
        response = requests.get(
            f"{API_BASE_URL}/users/{user_id}/books",
            timeout=APIClient.TIMEOUT
        )
        return APIClient._handle_response(response)
    
    @staticmethod
    def get_userBookDataByIndex(user_id:str,bookIndex:int):
        response = requests.get(
            f"{API_BASE_URL}/users/{user_id}/books/{bookIndex}",
            timeout=APIClient.TIMEOUT
        )
        return APIClient._handle_response(response)

    @staticmethod
    def get_userBookNames(user_id:str):
        response = requests.get(
            f"{API_BASE_URL}/users/{user_id}/booknames",
            timeout=APIClient.TIMEOUT
        )
        return APIClient._handle_response(response)

    @staticmethod
    def update_userBookData(user_id:str,bookIndex:int,data:dict):
        response = requests.put(
            f"{API_BASE_URL}/users/{user_id}/books/{bookIndex}",
            json=data,
            timeout=APIClient.TIMEOUT
        )
        return APIClient._handle_response(response)











# import requests
# from requests.exceptions import RequestException
# from core.config import API_BASE_URL


# class APIClient:

#     TIMEOUT = 10
#     headers = {
#         "Content-Type": "application/json"
#     }

#     @staticmethod
#     def _make_request(method, url, **kwargs):
#         try:
#             response = requests.request(
#                 method=method,
#                 url=url,
#                 timeout=APIClient.TIMEOUT,
#                 headers=APIClient.headers,
#                 **kwargs
#             )
#             return APIClient._handle_response(response)

#         except requests.exceptions.Timeout:
#             return {"error": "Request timed out. Server may be down."}

#         except requests.exceptions.ConnectionError:
#             return {"error": "Cannot connect to server. Server may be down."}

#         except RequestException as e:
#             return {"error": f"Network error: {str(e)}"}

#     @staticmethod
#     def _handle_response(response):
#         if response.status_code in (200, 201):
#             return response.json()

#         if response.status_code == 422:
#             raise Exception(f"Validation Error: {response.json()}")

#         if response.status_code == 401:
#             return {"error": response.text}

#         if response.status_code == 404:
#             return {"error": response.text}

#         raise Exception(f"Error {response.status_code}: {response.text}")


#     @staticmethod
#     def create_user(data: dict):
#         return APIClient._make_request(
#             "POST",
#             f"{API_BASE_URL}/users",
#             json=data
#         )

#     @staticmethod
#     def update_user(user_id: str, data: dict):
#         return APIClient._make_request(
#             "PATCH",
#             f"{API_BASE_URL}/users/{user_id}",
#             json=data
#         )

#     @staticmethod
#     def get_user(user_id: str):
#         return APIClient._make_request(
#             "GET",
#             f"{API_BASE_URL}/users/id{user_id}"
#         )
    
#     @staticmethod
#     def authenticate_user(username: str, password: str):
#         return APIClient._make_request(
#             "POST",
#             f"{API_BASE_URL}/login",
#             json={"username": username, "password": password}
#         )
    
#     @staticmethod
#     def get_byusername(username: str):
#         return APIClient._make_request(
#             "GET",
#             f"{API_BASE_URL}/users/username{username}"
#         )
    
#     @staticmethod
#     def delete_user_account(user_id: str):
#         return APIClient._make_request(
#             "DELETE",
#             f"{API_BASE_URL}/users/{user_id}"
#         )

#     @staticmethod
#     def add_book(user_id:str, data:dict):
#         return APIClient._make_request(
#             "POST",
#             f"{API_BASE_URL}/users/{user_id}/books",
#             json=data
#         )

#     @staticmethod
#     def get_userBookData(user_id:str):
#         return APIClient._make_request(
#             "GET",
#             f"{API_BASE_URL}/users/{user_id}/books"
#         )

#     @staticmethod
#     def get_userBookDataByIndex(user_id:str,bookIndex:int):
#         return APIClient._make_request(
#             "GET",
#             f"{API_BASE_URL}/users/{user_id}/books/{bookIndex}"
#         )
    
#     @staticmethod
#     def get_userBookNames(user_id:str):
#         return APIClient._make_request(
#             "GET",
#             f"{API_BASE_URL}/users/{user_id}/booknames"
#         )

#     @staticmethod
#     def update_userBookData(user_id:str,bookIndex:int,data:dict):
#         return APIClient._make_request(
#             "PUT",
#             f"{API_BASE_URL}/users/{user_id}/books/{bookIndex}",
#             json=data
#         )