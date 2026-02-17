from frameQueue import FrameQueue, NULL_FRAME
import time

class FrameDispatcher:
    def __init__(self, queue: FrameQueue) -> None:
        self.queue = queue
        self.frame_count = 0

    def processFrames(self) -> bool:
        try:
            while True:
                frame = self.queue.get_frame(timeout=2.0)
                if frame is NULL_FRAME:
                    print(f"[frameDispacher] Queue closed. Processed {self.frame_count} frames. Finishing...")
                    break
                self.processFrame(frame)
                self.frame_count += 1
            return True
        except Exception as e:
            print(f"[frameDispacher] Exception processing frames: {e}")
            return False

    def processFrame(self, frame: object) -> bool:
        try:
            # TODO: detección de vehículo, tracking y cálculo de velocidad
            print(f"[frameDispacher] Processing frame {self.frame_count}...")
            return True
        except Exception as e:
            print(f"[frameDispacher] Error processing frame: {e}")
            return False