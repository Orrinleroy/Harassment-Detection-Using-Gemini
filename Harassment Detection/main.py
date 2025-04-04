from process_video import extract_frames_every_5_seconds
from analyze_image import analyze_image
import os
import time
import json

def check_suspicious_activity(response_text):
    keywords = ["harassment", "violence", "suspicious", "threat", "abuse"]
    return any(word.lower() in response_text.lower() for word in keywords)

def main():
    video_file = "static/test_video.mp4"
    results = []

    try:
        print("🎞️ Extracting frames every 5 seconds...")
        frame_paths = extract_frames_every_5_seconds(video_file)

        print(f"✅ Extracted {len(frame_paths)} frames:")
        for path in frame_paths:
            print(f"  - {path}")

        print("\n🔍 Analyzing frames using Gemini...\n")

        for frame_path in frame_paths:
            success = False
            retry_attempts = 3
            delay_seconds = 50
            frame_result = {
                "frame": frame_path,
                "status": "Skipped",
                "gemini_response": "",
                "suspicious": False
            }

            for attempt in range(retry_attempts):
                print(f"🖼️ Analyzing {os.path.basename(frame_path)} (Attempt {attempt + 1})...")
                try:
                    result = analyze_image(frame_path)
                    print("Gemini Response:", result)

                    suspicious = check_suspicious_activity(result)

                    frame_result["gemini_response"] = result
                    frame_result["suspicious"] = suspicious
                    frame_result["status"] = "Analyzed"
                    success = True
                    break

                except Exception as e:
                    if "429" in str(e):
                        print("⏳ Rate limit hit. Waiting before retrying...")
                        time.sleep(delay_seconds)
                    else:
                        print(f"❌ Error analyzing {frame_path}: {e}")
                        frame_result["status"] = f"Error: {e}"
                        break

            if not success:
                print(f"⚠️ Skipping {frame_path} after {retry_attempts} failed attempts.\n")

            results.append(frame_result)

        # Save results to JSON
        with open("results.json", "w") as f:
            json.dump(results, f, indent=4)

        print("📁 Analysis results saved to results.json")

    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
