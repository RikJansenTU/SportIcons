import requests
import gradio as gr
import Constants

def generate_audio(text, athlete):
    match athlete:
        case 'Michael Jordan':
            voice_id = 'pNInz6obpgDQGcFmaJgB'
        case 'Louis van Gaal':
            voice_id = 2
        case 'Serena Williams':
            voice_id = 3        

    url = f'https://api.elevenlabs.io/v1/text-to-speech/{voice_id}'
    headers = {'xi-api-key' : Constants.ELEVENLABS_API_KEY}
    payload = {'text': text, 
               'voice_settings':
                    {'stability': 0.75, 
                     'similarity_boost': 0.75
                     }
                }
    r = requests.post(url, headers=headers, json=payload)
    
    with open('speech.mp3', 'wb') as f:
        f.write(r.content)
    print (r.content)

    return {audio_output: gr.update(visible=True, value='./speech.mp3'),
            audio_to_video_button: gr.update(visible=True)}

def generate_video(audio, athlete):
    url = 'https://api.d-id.com/talks'
    headers = {'accept': 'application/json',
               'content-type': 'application/json',
               'authorization': f'Basic {Constants.DID_API_KEY}'}
    payload = {}
    r = requests.post(url, headers=headers, json=payload)
    return {video_output: gr.update(visible=True)}

#creates the Gradio interface
with gr.Blocks() as demo:
    text = gr.Textbox(placeholder='Enter text here', label='Input')
    athlete = gr.Dropdown(choices=['Michael Jordan', 'Louis van Gaal', 'Serena Williams'], value='Michael Jordan', label='Select Athlete')
    text_to_audio_button = gr.Button('Generate Audio')
    audio_output = gr.Audio(label='Audio', visible=False, interactive=False)
    audio_to_video_button = gr.Button('Generate Video Based On This Audio', visible=False)
    video_output = gr.Video(label='Video', visible=False)

    text_to_audio_button.click(generate_audio, inputs=[text, athlete], outputs=[audio_output, audio_to_video_button])
    audio_to_video_button.click(generate_video, inputs=[audio_output, athlete], outputs=video_output)

if __name__ == "__main__":
    demo.launch()