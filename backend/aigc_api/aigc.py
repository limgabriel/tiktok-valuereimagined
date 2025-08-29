import os
from typing import Optional
from dotenv import load_dotenv
from realitydefender import RealityDefender, RealityDefenderError

load_dotenv()

def format_score(score: Optional[float]) -> str:
    """Helper function to format scores for display"""
    if score is None:
        return "None"
    return f"Score: {score:.4f} ({score * 100:.1f}%)"


async def basic_example(file_path):
    """
    Basic example of uploading a file and getting results
    """
    # Get API key from environment variable
    api_key = os.environ.get("REALITY_DEFENDER_API_KEY")

    if not api_key:
        print("ERROR: Please set REALITY_DEFENDER_API_KEY environment variable")
        return

    client: Optional[RealityDefender] = None

    try:
        # Initialize the SDK
        client = RealityDefender(api_key=api_key)

        # Upload a file for analysis

        if not os.path.exists(file_path):
            print(f"File not found: {file_path}")
            print(
                "Please add a test image named 'test_image.jpg' to the examples/images directory"
            )
            return

        print(f"Uploading file: {file_path}")
        upload_result = await client.upload(file_path=file_path)

        print("Upload successful!")
        print(f"Request ID: {upload_result['request_id']}")
        print(f"Media ID: {upload_result['media_id']}")

        # Poll for results
        print("\nPolling for results...")
        result = await client.get_result(upload_result["request_id"])

        print("\nDetection Results:")
        print(f"Status: {result['status']}")

        # Format score as a percentage if it exists
        if result["score"] is not None:
            print(format_score(result['score']))
        else:
            print("Score: None")

        print("\nModel Results:")
        for model in result["models"]:
            score_display = "None"
            if model["score"] is not None:
                score_display = f"{model['score']:.4f} ({model['score'] * 100:.1f}%)"
            print(f"  - {model['name']}: {model['status']} (Score: {score_display})")
        return result

    except RealityDefenderError as e:
        print(f"Error: {e.message} (Code: {e.code})")
    except Exception as e:
        print(f"Unexpected error: {str(e)}")


# Detection Results:
# Status: AUTHENTIC
# Score: 0.0700 (7.0%)
#
# Model Results:
#   - rd-context-img: AUTHENTIC (Score: 0.0700 (7.0%))
#
# Example complete!

if __name__ == "__main__":
    import asyncio
    file_path = "sampleImages/thumbnail.jpg"
    asyncio.run(basic_example(file_path))
    print("\nExample complete!")