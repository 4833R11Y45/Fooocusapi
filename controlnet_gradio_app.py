import gradio as gr
import base64
import requests
import os
from PIL import Image
import io

def encode_image_to_base64(image):
    """Convert PIL Image to base64 string"""
    if image is None:
        return None
    buffered = io.BytesIO()
    image.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode()

def generate_images(person_file, pose_file, person_stop, person_weight, 
                   pose_stop, pose_weight):
    try:
        # Extract original filenames 
        person_name = os.path.splitext(person_file.name)[0]
        pose_name = os.path.splitext(pose_file.name)[0]

        # Create output filename
        output_filename = f"{person_name}_{pose_name}.png"

        # Create outputs directory if it doesn't exist
        os.makedirs("outputs", exist_ok=True)
        output_path = os.path.join("outputs", output_filename)

        # Print debug information
        print(f"Person file: {person_file.name}")
        print(f"Pose file: {pose_file.name}")
        print(f"Person name: {person_name}")
        print(f"Pose name: {pose_name}")
        print(f"Output filename: {output_filename}")

        # Load images using PIL
        person_image = Image.open(person_file.name)
        pose_image = Image.open(pose_file.name)

        # Prepare API payload
        payload = {
            "control_inputs": [
                {
                    "cn_img": encode_image_to_base64(person_image),
                    "cn_stop": float(person_stop),
                    "cn_weight": float(person_weight),
                    "cn_type": "ImagePrompt"
                },
                {
                    "cn_img": encode_image_to_base64(pose_image),
                    "cn_stop": float(pose_stop),
                    "cn_weight": float(pose_weight),
                    "cn_type": "CPDS"
                }
            ]
        }

        # Make API request
        response = requests.post(
            "http://localhost:7866/v1/controlnet/generate",
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        response.raise_for_status()

        result = response.json()

        if (isinstance(result, dict) and 
            'result' in result and 
            isinstance(result['result'], list) and 
            len(result['result']) > 0):

            image_url = result['result'][0]

            # Download the image
            image_response = requests.get(image_url)
            image_response.raise_for_status()

            # Save the image
            with open(output_path, 'wb') as f:
                f.write(image_response.content)

            # Load the saved image
            generated_image = Image.open(output_path)

            return (
                generated_image,
                f"Generated and saved as: {output_filename}",
                None,
                output_path
            )
        else:
            return None, "No image generated", f"Invalid response structure: {result}", None

    except Exception as e:
        error_msg = str(e)
        print(f"Error in generate_images: {error_msg}")
        return None, f"Error: {error_msg}", error_msg, None

def create_ui():
    with gr.Blocks(title="ControlNet Image Generator") as app:
        gr.Markdown("# ControlNet Image Generator")

        with gr.Row():
            with gr.Column():
                person_file = gr.File(
                    label="Person Image (ImagePrompt)",
                    file_types=["image"]
                )
                with gr.Row():
                    person_stop = gr.Slider(
                        minimum=0, maximum=1, value=0.6,
                        label="Person Stop Value"
                    )
                    person_weight = gr.Slider(
                        minimum=0, maximum=2, value=0.5,
                        label="Person Weight Value"
                    )

            with gr.Column():
                pose_file = gr.File(
                    label="Pose Image (CPDS)",
                    file_types=["image"]
                )
                with gr.Row():
                    pose_stop = gr.Slider(
                        minimum=0, maximum=1, value=0.6,
                        label="Pose Stop Value"
                    )
                    pose_weight = gr.Slider(
                        minimum=0, maximum=2, value=0.5,
                        label="Pose Weight Value"
                    )

        with gr.Row():
            generate_btn = gr.Button("Generate", variant="primary")
            reset_btn = gr.Button("Reset")

        with gr.Row():
            output_image = gr.Image(
                label="Generated Image",
                type="pil",
                interactive=False
            )

        with gr.Row():
            status_text = gr.Textbox(
                label="Status",
                interactive=False
            )
            error_text = gr.Textbox(
                label="Error",
                visible=True,
                interactive=False
            )

        download_btn = gr.File(
            label="Download Generated Image",
            interactive=True,
            visible=True
        )

        generate_btn.click(
            fn=generate_images,
            inputs=[
                person_file, pose_file,
                person_stop, person_weight,
                pose_stop, pose_weight
            ],
            outputs=[output_image, status_text, error_text, download_btn]
        )

        def reset_interface():
            return {
                person_file: None,
                pose_file: None,
                person_stop: 0.6,
                person_weight: 0.5,
                pose_stop: 0.6,
                pose_weight: 0.5,
                output_image: None,
                status_text: "Interface reset",
                error_text: None,
                download_btn: None
            }

        reset_btn.click(
            fn=reset_interface,
            inputs=[],
            outputs=[
                person_file, pose_file,
                person_stop, person_weight,
                pose_stop, pose_weight,
                output_image, status_text, error_text,
                download_btn
            ]
        )

    return app

if __name__ == "__main__":
    app = create_ui()
    app.launch(server_name="0.0.0.0", server_port=7867)
