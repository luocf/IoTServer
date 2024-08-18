import requests
from requests.exceptions import ConnectionError, Timeout, RequestException

BASE_URL = "http://127.0.0.1:8000"

def create_user(username, password, email=None, phone_number=None, is_admin=False):
    user_data = {
        "username": username,
        "password": password,
        "email": email,
        "phone_number": phone_number,
        "is_admin": is_admin
    }
    response = make_post_request("/api/users/", user_data)
    return handle_response(response)

def get_users():
    response = make_get_request("/api/users/")
    return handle_response(response)

def get_user(user_id):
    response = make_get_request(f"/api/users/{user_id}")
    return handle_response(response)

def create_space(name, description=None):
    space_data = {
        "name": name,
        "description": description
    }
    response = make_post_request("/api/spaces/", space_data)
    return handle_response(response)

def get_space(space_id):
    response = make_get_request(f"/api/spaces/{space_id}")
    return handle_response(response)

def create_device(name, eui, device_type, timeout, space_id, online_status=False, power_status=False, set_temperature=None, fan_speed=None, mode=None):
    device_data = {
        "name": name,
        "eui": eui,
        "device_type": device_type,
        "timeout": timeout,
        "space_id": space_id,
        "online_status": online_status,
        "power_status": power_status,
        "set_temperature": set_temperature,
        "fan_speed": fan_speed,
        "mode": mode
    }
    response = make_post_request("/api/devices/", device_data)
    return handle_response(response)

def get_device(device_id):
    response = make_get_request(f"/api/devices/{device_id}")
    return handle_response(response)

def make_post_request(endpoint, json_data, timeout=10):
    try:
        return requests.post(f"{BASE_URL}{endpoint}", json=json_data, timeout=timeout)
    except (ConnectionError, Timeout) as e:
        print(f"Connection error: {e}")
    except RequestException as e:
        print(f"Request error: {e}")
    return None

def make_get_request(endpoint, timeout=10):
    try:
        return requests.get(f"{BASE_URL}{endpoint}", timeout=timeout)
    except (ConnectionError, Timeout) as e:
        print(f"Connection error: {e}")
    except RequestException as e:
        print(f"Request error: {e}")
    return None

def handle_response(response):
    if response is None:
        return None
    print("Status Code:", response.status_code)
    try:
        json_data = response.json()
        print("Response JSON:", json_data)
        return json_data
    except requests.exceptions.JSONDecodeError:
        print("Failed to parse response as JSON. Raw Response Text:", response.text)
        return None

if __name__ == "__main__":
    # user = create_user(username="jaaaa2", password="securepassword2", email="john@example.com2", phone_number="1234567829", is_admin=True)
    # print("Created User:", user)

    # users = get_users()
    # print("All Users:", users)

    # user_details = get_user(user_id=1)
    # print("User Details:", user_details)

    # space = create_space(name="333 Room", description="A room for meetings")
    # print("Created Space:", space)

    # space_details = get_space(space_id=12)
    # print("Space Details:", space_details)

    device = create_device(name="AC Unit 3", eui="323456789ABCDEF", device_type="air_conditioner", timeout=120, space_id=1, online_status=True, power_status=True)
    print("Created Device:", device)

    device_details = get_device(device_id=1)
    print("Device Details:", device_details)
