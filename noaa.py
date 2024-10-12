import os
import requests
from PIL import Image
from io import BytesIO

# URL of the JSON file
json_url = 'https://services.swpc.noaa.gov/products/animations/ovation_north_24h.json'
frames_dir = './frames'
fps = 30  # frames per second
output_video = 'aurora_animation.mp4'
output_gif = 'aurora_animation.gif'

# Create the /frames directory if it doesn't exist
if not os.path.exists(frames_dir):
    os.makedirs(frames_dir)

# Fetch the JSON data from the URL
response = requests.get(json_url)
image_info = response.json()

# Fetch each image and save it in the /frames directory
for i, info in enumerate(image_info):
    img_url = "https://services.swpc.noaa.gov" + info['url']
    img_response = requests.get(img_url)
    img = Image.open(BytesIO(img_response.content))
    img_path = os.path.join(frames_dir, f'frame_{i:04d}.jpg')  # Save as frame_0000.jpg, frame_0001.jpg, etc.
    img.save(img_path)
    print(f"Downloaded {img_path}")

# Now call ffmpeg to generate the video from the frames
# The -r option specifies the frame rate (FPS), and the output file will be aurora_animation.mp4
os.system(f"ffmpeg -r {fps} -i {frames_dir}/frame_%04d.jpg -c:v libx264 -vf fps={fps} -pix_fmt yuv420p {output_video}")
os.system(f"ffmpeg -i {output_video} -vf 'fps={fps},scale=640:-1:flags=lanczos' -gifflags +transdiff -y {output_gif}")

print(f"Video saved as {output_video}")
