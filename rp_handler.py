import json
import base64
from PIL import Image
import io
import time
from huggingface_hub import InferenceClient
import runpod

# Initialize the Hugging Face Inference Client
client = InferenceClient(token="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")

def generate_image(prompt, model_name="black-forest-labs/FLUX.1-dev", max_retries=3, delay=10):
    """Generate an image from text using the Hugging Face Inference API."""
    for attempt in range(max_retries):
        try:
            print(f"Attempt {attempt + 1}/{max_retries}: Generating image...")
            image = client.text_to_image(prompt, model=model_name)
            return image
        except Exception as e:
            print(f"Error during inference: {e}")
            if attempt < max_retries - 1:
                print(f"Retrying in {delay} seconds...")
                time.sleep(delay)
            else:
                raise
    return None

def handler(event):
    """RunPod handler function."""
    input_data = event.get("input", {})
    prompt = input_data.get("instruction")
    seconds = input_data.get("seconds", 0)

    if not prompt:
        return json.dumps({"error": "Prompt is required"})

    try:
        time.sleep(seconds)  # Simulate delay if specified

        # Generate the image
        image = generate_image(prompt)

        if isinstance(image, Image.Image):
            # Convert image to base64
            img_bytes = io.BytesIO()
            image.save(img_bytes, format="PNG")
            img_bytes.seek(0)
            base64_image = base64.b64encode(img_bytes.getvalue()).decode("utf-8")

            # Return the result as JSON string
            result = {
                "message": "Image generation successful",
                "image": base64_image
            }
            return json.dumps(result)

        else:
            return json.dumps({"error": "Failed to generate image"})
    except Exception as e:
        return json.dumps({"error": str(e)})

if __name__ == '__main__':
    runpod.serverless.start({'handler': handler})
