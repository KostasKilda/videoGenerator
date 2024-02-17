from moviepy.audio.io.AudioFileClip import AudioFileClip
from moviepy.editor import ImageClip, concatenate_videoclips

from openai import OpenAI
import requests
from bs4 import BeautifulSoup
import os

# Importing environmental variables
import enviroment


client = OpenAI()

completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=enviroment.WhisperPrompt
)

# Splitting the response from Whisper as prompted
fact = completion.choices[0].message.content.split('|')


# Adding silence to the start and the end of the sentence
fact[2] = '--'+  fact[2] + '--'


CHUNK_SIZE = 1024



# Eleven labs endpoint
elevenLabsURL = "https://api.elevenlabs.io/v1/text-to-speech/" + enviroment.elevenLabsVoice

headers = {
    "Accept": "audio/mpeg",
    "Content-Type": "application/json",
    "xi-api-key": enviroment.elevenLabsKey
}

data = {
    "text": fact[2],
    "model_id": "eleven_monolingual_v1",
    "voice_settings": {
        "stability": 0.5,
        "similarity_boost": 0.5
    }
}

response = requests.post(elevenLabsURL, json=data, headers=headers)


# Saving the audio file
with open('output.mp3', 'wb') as f:
    for chunk in response.iter_content(chunk_size=CHUNK_SIZE):
        if chunk:
            f.write(chunk)



# Using beautiful soup to download images from unsplash.com
HTML = requests.get('https://unsplash.com/s/photos/' +
                    fact[0] + '?orientation=portrait')


soup = BeautifulSoup(HTML.text, 'html.parser')



photos = soup.find_all("a", class_="rEAWd")

i = 0
for photoHTML in photos:

    try:
        # Acquires the HTML of the individual photo page
        photoPage = requests.get(
            'https://unsplash.com' + photoHTML.get('href'))

        # Parses the HTML to beautiful soup format
        photoSoup = BeautifulSoup(photoPage.text, 'html.parser')

        # Find the image elements with a predifined class
        photoElement = photoSoup.find_all("div", class_="sBV1O")

        # Acquires the URL of the image download button
        photoDownloadUrl = photoElement[0]('a')[0].get('href')

        # Sends a GET request to the image URL
        imageDownload = requests.get(photoDownloadUrl)

        # If the status code returns 200, saves the image
        if imageDownload.status_code == 200:
            imageData = imageDownload.content
            filePath = "images/videoImage" + str(i) + ".jpg"
            with open(filePath, "wb") as file:
                file.write(imageData)

        i += 1

    except:
        pass

    # Stops the for loop after 3 images were saved
    if i >= 3:
        break


# Paths to audio and image files
image_paths = ["images/videoImage0.jpg",
               "images/videoImage1.jpg", "images/videoImage2.jpg"]
audio_path = "output.mp3"

audio_clip = AudioFileClip(audio_path)
audio_duration = audio_clip.duration

# Dynamically acquiring the image duration based on 1/3rd of audio length
image_duration = audio_duration / 3

# Resizing the images
resized_image_clips = []
for path in image_paths:
    image = ImageClip(path)
    resized_image = image.resize(newsize=(400, 600))
    resized_image_clip = resized_image.set_duration(image_duration)
    resized_image_clips.append(resized_image_clip)


# Concatenating the images
colleague_clip = concatenate_videoclips(resized_image_clips, method="compose")


audio_clip = audio_clip.set_duration(colleague_clip.duration)

# Attaching the audio to the video file
video_with_audio = colleague_clip.set_audio(audio_clip)

# Saving the video
video_with_audio.write_videofile('video.mp4', fps=24)



# Clean up files
os.remove("output.mp3")
for image in image_paths:
    os.remove(image)