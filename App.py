import requests
import time
import gradio as gr
import Constants
import Hidden_Constants

#generates an audio fragment of the chosen athlete reading the text
def generate_audio(text, athlete):
    match athlete:
        case 'Michael Jordan':
            voice_id = Constants.MJ_VOICE_ID
        case 'Louis van Gaal':
            voice_id = 2
        case 'Serena Williams':
            voice_id = 3        

    url = f'https://api.elevenlabs.io/v1/text-to-speech/{voice_id}'
    headers = {'xi-api-key' : Hidden_Constants.ELEVENLABS_API_KEY}
    payload = {'text': text, 
               'voice_settings':
                    {'stability': 0.75, 
                     'similarity_boost': 0.75
                    }
                }
    r = requests.post(url, headers=headers, json=payload)
    
    with open('speech.mp3', 'wb') as f:
        f.write(r.content)

    return {audio_output: gr.update(visible=True, value='./speech.mp3'),
            audio_to_video_button: gr.update(visible=True)
            }


#generates a talking head video of the chosen athlete based on the audio file previously generated
def generate_video(athlete):

    #credits check
    url = "https://api.d-id.com/credits"
    headers = {
        "accept": "application/json",
        "authorization": f'Basic {Hidden_Constants.DID_API_KEY}'
    }
    response = requests.get(url, headers=headers)
    print(response.text)

    #get actor image url
    match athlete:
        case 'Michael Jordan':
            image_url = Constants.MJ_IMAGE_URL
        case 'Louis van Gaal':
            image_url = Constants.MJ_IMAGE_URL
        case 'Serena Williams':
            image_url = Constants.MJ_IMAGE_URL     

    #upload audio file to a temp location
    url = 'https://api.d-id.com/audios'
    files = {'audio': ('speech.mp3', open('speech.mp3', 'rb'), 'audio/mpeg')}
    r = requests.post(url, headers=headers, files=files).json()
    audio_url = r['url']
    print(audio_url)

    #generate the talking head video
    url = 'https://api.d-id.com/talks'
    headers = {'accept': 'application/json',
               'content-type': 'application/json',
               'authorization': f'Basic {Hidden_Constants.DID_API_KEY}'
               }
    payload = {
        "script": {
            "type": "audio",
            "ssml": "false",
            "audio_url": audio_url
        },
        "config": {
            "fluent": "false",
            "pad_audio": "0.0"
        },
        "source_url": image_url
        }
    r = requests.post(url, headers=headers, json=payload)
    print(r)
    print(r.text)
    r = r.json()
    id = r['id']
    print(id)

    #the url to the generated video
    url = f'https://api.d-id.com/talks/{id}'
    headers = {'accept': 'application/json',
               'authorization': f'Basic {Hidden_Constants.DID_API_KEY}'
               }
    
    #check if the video is done generating, and get the url if it is
    while True:
        time.sleep(5)
        r = requests.get(url, headers=headers).json()
        print (r)
        status = r['status']
        if status == 'done':
            video_url = r['result_url']
            break    
        elif status == 'error' or 'rejected':
            print('Something went wrong.')
            break

    file = requests.get(video_url)
    with open('video.mp4', 'wb') as f:
        f.write(file.content)   
    
    return {video_output: gr.update(visible=True, value='video.mp4')}

    #upload portrait image to a temp location
    image_filename = f'SportIcons/{athlete}.jpg'
    url = 'https://api.d-id.com/images'
    headers = {'accept': 'application/json',
                'content-type': 'multipart/form-data',
                'authorization': f'Basic {Constants.DID_API_KEY}'
                }
    files = {'image': (image_filename, open(image_filename, 'rb'), 'image/jpeg')}
    r = requests.post(url, headers=headers, files=files)
    print (r)
    print (r.text)
    image_url = r['url']


#creates the Gradio interface
with gr.Blocks() as demo:
    text = gr.Textbox(placeholder='Enter text here', label='Input')
    athlete = gr.Dropdown(choices=['Michael Jordan', 'Louis van Gaal', 'Serena Williams'], value='Michael Jordan', label='Select Athlete')
    text_to_audio_button = gr.Button('Generate Audio')
    audio_output = gr.Audio(label='Audio', visible=False, interactive=False)
    audio_to_video_button = gr.Button('Generate Video Based On This Audio', visible=False)
    video_output = gr.Video(label='Video', visible=False)

    text_to_audio_button.click(generate_audio, inputs=[text, athlete], outputs=[audio_output, audio_to_video_button])
    audio_to_video_button.click(generate_video, inputs=[athlete], outputs=video_output)


if __name__ == "__main__":
    demo.launch()