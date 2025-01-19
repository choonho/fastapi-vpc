import requests
import os

NEUTRON_URL = os.getenv("NEUTRON_URL")
#NEUTRON_URL = "http://127.0.0.1:9696/networking/v2.0/networks"

def create_openstack_network(name: str, project_id: str,  auth_token: str) -> str:
    headers = {
        "Content-Type": "application/json",
        "X-Auth-Token": auth_token
    }
    payload = {
        "network": {
            "name": name,
            "admin_state_up": True,
            "project_id": project_id
        }
    }
    response = requests.post(NEUTRON_URL, json=payload, headers=headers)
    
    if response.status_code == 201:
        network_id = response.json()["network"]["id"]
        return network_id
    else:
        raise Exception(f"Failed to create network: {response.text}")


if __name__ == "__main__":
    vpc_id = create_openstack_network("my-vpc-test-xxxx")
    print(vpc_id)

