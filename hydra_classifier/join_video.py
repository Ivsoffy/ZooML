import argparse
import sys
import cv2
import os


def join_video(output_dir, output_video, fps):
    images = [img for img in os.listdir(output_dir) if img.endswith(".jpg") or img.endswith(".png")]
    if not images:
        print("Ошибка: В папке нет фотографий.")
        exit()

    images.sort()
    first_image_path = os.path.join(output_dir, images[0])
    first_image = cv2.imread(first_image_path)
    height, width, layers = first_image.shape

    fourcc = cv2.VideoWriter_fourcc(*"mp4v")  # Кодек для MP4
    video_writer = cv2.VideoWriter(output_video, fourcc, fps, (width, height))

    # Проходим по всем изображениям и добавляем их в видео
    for image_name in images:
        image_path = os.path.join(output_dir, image_name)
        frame = cv2.imread(image_path)
        video_writer.write(frame)  # Добавляем кадр в видео

    # Освобождаем ресурсы
    video_writer.release()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'output_dir',
        help = 'The path to the output image dir')
    parser.add_argument(
        'output_video',
        help = 'The path to the video where framed photos will be saved')
    parser.add_argument(
        'fps',
        help = 'fps for new video')
    if len(sys.argv[1:]) != 3:
        parser.print_help()
        parser.exit()
        
    args = parser.parse_args()
    
    join_video(args.output_dir, args.output_video, int(args.fps))
        
    
if __name__ == '__main__':
    main()