import os
import requests
import time
from lumaai import LumaAI
client = LumaAI(
        auth_token="luma-f4f9d1b4-6f53-488e-8e77-e035cdb9f68e-075748c4-1cfa-4e19-8625-26ff67066c53",
    )


def generate_video(prompt):
    generation = client.generations.create(
        prompt=prompt,
    )
    print(generation)
    return generation['id']

def check_status(id):
    generation = client.generations.get(id)
    print(generation)
    return generation['status']

def download_video(id, save_path="./"):
    # Download from Luma API
    response = requests.get(url, stream=True)

    file_name = os.path.join(save_path, 'video.mp4')
    with open(file_name, 'wb') as file:
        file.write(response.content)
    print(f"File downloaded as {file_name}")

if __name__ == "__main__":
    
    generation_id = generate_video("a beautiful landscape with a river and mountains")
    print("Generated ID:", generation_id)

    while check_status(generation_id) is None:
        print("Waiting for video to be generated...")
        time.sleep(1)
    print("Video generated!")

    url = check_status(id)
    download_video(url, "video.mp4")