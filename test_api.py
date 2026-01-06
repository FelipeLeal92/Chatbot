import requests

def test_chat_endpoint():
    url = "http://localhost:8000/chat"
    data = {
        "session_id": "12345",
        "message": "Hello"
    }
    response = requests.post(url, json=data)
    assert response.status_code == 200
    print(response.json())

if __name__ == "__main__":
    test_chat_endpoint()