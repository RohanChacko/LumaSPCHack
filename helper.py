import os
import requests

def check_status(client, id):
    generation = client.generations.get(id)
    return generation.state if generation.state == "completed" else None

def delete_video(client, id):
    client.generations.delete(id)

def delete_all_videos(client):
    generations = client.generations.list(limit=100, offset=0) # default limit is 10

    for generation in generations:
        if generation[0] == "generations":
            for video in generation[1]:
                print(f"Deleting video {video.id}")
                delete_video(client, video.id)

def download_video(client,id, save_path="./"):
    generation = client.generations.get(id)

    url = generation.assets.video
    # Download from Luma API
    response = requests.get(url, stream=True)

    file_name = os.path.join(save_path, 'video.mp4')
    with open(file_name, 'wb') as file:
        file.write(response.content)
    print(f"File downloaded as {file_name}")
