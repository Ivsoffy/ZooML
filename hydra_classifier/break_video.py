import argparse
import sys
import cv2
import os

def break_video(video_path, output_dir, desired_fps):
    video_capture = cv2.VideoCapture(video_path)
    fps = video_capture.get(cv2.CAP_PROP_FPS)
    skip_frames = int(fps / desired_fps)
    os.makedirs(output_dir, exist_ok=True)
    frame_count = 0

    if not video_capture.isOpened():
        print("Ошибка: Не удалось открыть видеофайл.")
        exit()

    while True:
        ret, frame = video_capture.read()
        if not ret:
            break

        if frame_count % skip_frames == 0:
          frame_filename = os.path.join(output_dir, f"frame_{frame_count:04d}.jpg")
          cv2.imwrite(frame_filename, frame)

        frame_count += 1
    video_capture.release()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'input_video',
        help = 'The path to the input video')
    parser.add_argument(
        'input_dir',
        help = 'The path to the directory where input photos are stored')
    parser.add_argument(
        'fps',
        help = 'fps new video'
    )
    if len(sys.argv[1:]) != 3:
        parser.print_help()
        parser.exit()

    args = parser.parse_args()

    break_video(args.input_video, args.input_dir, int(args.fps))

if __name__ == '__main__':
    main()