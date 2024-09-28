import requests
import json
import time
import os
def post_to_luma(prompt, aspect_ratio, loop):
    # Post to Luma API
    url = "https://api.lumalabs.ai/dream-machine/v1/generations"

    payload = {
        "prompt": prompt,
        "aspect_ratio": aspect_ratio,
        "loop": True
    }
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "authorization": "Bearer luma-f4f9d1b4-6f53-488e-8e77-e035cdb9f68e-075748c4-1cfa-4e19-8625-26ff67066c53"
    }

    response = requests.post(url, json=payload, headers=headers)

    # retrieve id field from returned response.text
    data = json.loads(response.text)
    id = data['id']

    return id

def check_status(id):
    # Get from Luma API
    url = f"https://api.lumalabs.ai/dream-machine/v1/generations/{id}"

    headers = {
        "accept": "application/json",
        "authorization": "Bearer luma-f4f9d1b4-6f53-488e-8e77-e035cdb9f68e-075748c4-1cfa-4e19-8625-26ff67066c53"
    }

    response = requests.get(url, headers=headers)
    data = json.loads(response.text)
    state = data['state']

    # assets is null if state == "queued" else return assets
    return data['assets']["video"] if state == "completed" else None
    

def download_from_luma(url, save_path):
    # Download from Luma API
    response = requests.get(url, stream=True)

    file_name = os.path.join(save_path, 'video.mp4')
    with open(file_name, 'wb') as file:
        file.write(response.content)
    print(f"File downloaded as {file_name}")


if __name__ == "__main__":
    id = post_to_luma("a beautiful landscape with a river and mountains", "16:9", True)
    print("Generated ID:", id)

    while check_status(id) is None:
        print("Waiting for video to be generated...")
        time.sleep(1)
    print("Video generated!")

    url = check_status(id)
    download_from_luma(url, "video.mp4")