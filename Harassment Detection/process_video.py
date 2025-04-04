import cv2
import os

def extract_frames_every_5_seconds(video_path, output_folder="static/frames"):
    """
    Extracts a frame every 5 seconds from the video and saves them in the specified folder.

    :param video_path: Path to the input video file.
    :param output_folder: Folder where extracted frames will be saved.
    :return: List of paths to the saved frames.
    """
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    cap = cv2.VideoCapture(video_path)

    fps = cap.get(cv2.CAP_PROP_FPS)  # Frames per second
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    duration_sec = int(total_frames / fps)

    frame_paths = []

    for sec in range(0, duration_sec + 1, 5):  # every 5 seconds
        frame_number = int(sec * fps)
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
        ret, frame = cap.read()

        if ret:
            frame_path = os.path.join(output_folder, f"frame_{sec}s.jpg")
            cv2.imwrite(frame_path, frame)
            frame_paths.append(frame_path)
        else:
            print(f"⚠️ Skipped frame at {sec} seconds (frame {frame_number})")

    cap.release()
    return frame_paths


# Example usage
if __name__ == "__main__":
    video_file = "static/test_video.mp4"
    saved_frames = extract_frames_every_5_seconds(video_file)
    print("Frames saved at:")
    for path in saved_frames:
        print(f"  - {path}")
