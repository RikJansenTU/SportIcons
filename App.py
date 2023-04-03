import requests
import gradio as gr
import Constants

def generate(text, athlete):
    match athlete:
        case 'Michael Jordan':
            voice_id = 1
        case 'Louis van Gaal':
            voice_id = 2
        case 'Serena Williams':
            voice_id = 3        

    header = {'xi-api-key' : Constants.ELEVENLABS_API_KEY}
    payload = {'text':text, 'voice_settings':{'stability':75, 'similarity_boost':75}}
    r = requests.post(f'api.elevenlabs.iov1/text-to-speech/{voice_id}', headers=header, data=payload)
    with open('speech.mp3', 'wb') as f:
        #not all content
        f.write(r.content)

#creates the Gradio interface
with gr.Blocks() as demo:
    with gr.Tab('Text-to-Audio-to-Video'):
        text = gr.Textbox(placeholder='Enter text here', label='Input')
        athlete = gr.Dropdown(choices=['Michael Jordan', 'Louis van Gaal', 'Serena Williams'], value='Michael Jordan')
        text_to_audio_button = gr.Button('Generate Audio')
        text_to_video_button = gr.Button('Generate Video')
        audio = gr.Audio(label='Audio', interactive=True)
        audio_to_video_button = gr.Button('Generate Video')
        video_output= gr.Video(label='Video')
    with gr.Tab('Text-to-Video'):
        text = gr.Textbox(placeholder='Enter text here', label='Input')
        athlete = gr.Dropdown(choices=['Michael Jordan', 'Louis van Gaal', 'Serena Williams'], value='Michael Jordan')
        text_to_video_button = gr.Button('Generate Video')
        video_output= gr.Video(label='Video')
    text_to_video_button.click(generate, inputs=[text, athlete], outputs=video_output)

if __name__ == "__main__":
    demo.launch()