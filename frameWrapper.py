import cv2
from frameQueue import FrameQueue

class FrameWrapper:
    def __init__(self, video_path: str, queue: FrameQueue) -> None:
        self.video_path = video_path
        self.queue = queue
        
    def readVideo(self) -> bool:
        cap = None
        try:
            cap = cv2.VideoCapture(self.video_path)
            if not cap.isOpened():
                print("[frameWrapper] Error: Could not open video.")
                return False
            
            cap.read()  # Skip the first frame
            frame_count = 0
            
            while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    print(f"[frameWrapper] End of video. Processed {frame_count} frames.")
                    break
                result = self.queueFrame(frame)
                if not result:
                    print(f"[frameWrapper] Error queuing frame {frame_count}. Stopping video processing.")
                    continue
                print(f"[frameWrapper] Queued frame {frame_count}.")
                frame_count += 1
            
            return True
        except Exception as e:
            print(f"[frameWrapper] Exception reading video: {e}")
            return False
        finally:
            if cap is not None:
                cap.release()
            self.queue.close()
            
    def queueFrame(self, frame: object) -> bool:
        result = self.queue.add_frame(frame)
        return result