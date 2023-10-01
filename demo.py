import gradio as gr

from accentor.stressifier import StressifierRunner, default_unstressed_text


def accentor(ukrainian_text: str, stressifier_model_name: str) -> str:
    print(ukrainian_text, stressifier_model_name)
    stressifier_runner = StressifierRunner()
    # ["Ukrainian Word Stressifier", "Ukrainian Accentor"]
    stressed_text = stressifier_runner.stressify(ukrainian_text, stressifier_model_name)
    return stressed_text
    

if __name__ == "__main__":
    with gr.Blocks() as demo:
        with gr.Row():
            with gr.Column(scale=2):
                unstressefied_text = gr.Textbox(label="Unstressefied text", value=default_unstressed_text)
                stressifier_models_names = list(StressifierRunner.models.keys())
                stressifier_picker = gr.Dropdown(
                    choices=stressifier_models_names,
                    value=stressifier_models_names[0]
                )
            with gr.Column(scale=2):
                stressefied_text = gr.Textbox(label="Stressefied text")
        with gr.Row():
            btn = gr.Button("Run stressifier")
            btn.click(
                fn=accentor, 
                inputs=[
                    unstressefied_text, 
                    stressifier_picker
                ], 
                outputs=stressefied_text,
            )
    demo.launch()

