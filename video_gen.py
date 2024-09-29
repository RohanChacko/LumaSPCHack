import time
from lumaai import LumaAI
from helper import check_status, download_video, delete_all_videos

client = LumaAI(
        auth_token="luma-f4f9d1b4-6f53-488e-8e77-e035cdb9f68e-075748c4-1cfa-4e19-8625-26ff67066c53",
    )

def text2video(prompt):
    generation = client.generations.create(
        prompt=prompt,
    )
    return generation.id


def img2video(image_url_start, prompt, image_url_end=None, loop=False):

    keyframes = {
      "frame0": {
        "type": "image",
        "url": image_url_start
      }
    }

    if image_url_end is not None:
        keyframes["frame1"] = {
        "type": "image",
        "url": image_url_end
      }
    generation = client.generations.create(
    prompt=prompt,
    loop=loop,
    aspect_ratio="3:4",
    keyframes=keyframes
    )
    return generation.id

if __name__ == "__main__":
    
    # text2video
    #generation_id = text2video("a photoshoot of a product handbag against a white background. 4k photorealistic handbag material. good spot lighting, camera motion orbit left")
    
    # img2video
    save_path = "./video.mp4"
    image_url_start = "https://i.ibb.co/X5xXnqD/image-2024-03-26-T145127-347.png"
    image_url_end = None #"https://i.ibb.co/XFvKq9P/plhrazbmh-P.png"
    loop = False if image_url_end is None else False
    prompt = f"[motion=4] Camera zoom in slowly with man standing still and posing"
    generation_id = img2video(image_url_start=image_url_start, prompt=prompt, image_url_end=image_url_end, loop=loop)
    print("Generated ID:", generation_id)
    
    while check_status(client, generation_id) is None:
        print("Waiting for video to be generated...")
        time.sleep(1)

    status = check_status(client, generation_id)
    if status is not None and status is not False:
        print("Video generated!")
        download_video(client, generation_id, save_path)
    elif status is False:
        print("Video generation failed!")



        
        
        
        