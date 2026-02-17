from queue import Queue, Full
import threading

NULL_FRAME: object = object()

class FrameQueue(Queue):
    def __init__(self, max_size: int) -> None:
        self.max_size = max_size
        self.closed = False
        self._close_lock = threading.Lock()
        super().__init__(maxsize=max_size)

    def add_frame(self, frame: object) -> bool:
        if self.closed:
            print("[frameQueue] Error: Cannot add frame to closed queue.")
            return False
        
        try:
            # Usa put() bloqueante para evitar race conditions. Si cola llena, descarta el mas antiguo.
            self.put(frame, block=True, timeout=0.5)
            print(f"[frameQueue] Frame added to queue. Current size: {self.qsize()}/{self.max_size}")
            return True
        except Full:
            # Queue llena: descarta el frame mas antiguo y agrega el nuevo
            try:
                discarded = self.get_nowait()
                print(f"[frameQueue] Warning: Queue full. Discarding oldest frame. Queue size: {self.qsize()}/{self.max_size}")
                self.put_nowait(frame)
                return True
            except Exception as e:
                print(f"[frameQueue] Error adding frame after discard: {e}")
                return False

    def close(self) -> None:
        with self._close_lock:
            if not self.closed:
                self.closed = True
                try:
                    # put() bloqueante con timeout para garantizar que el sentinel se encole
                    self.put(NULL_FRAME, block=True, timeout=1.0)
                except Full:
                    print("[frameQueue] Warning: Could not enqueue sentinel (queue full). Using put_nowait.")
                    try:
                        self.get_nowait()
                        self.put_nowait(NULL_FRAME)
                    except Exception as e:
                        print(f"[frameQueue] Error enqueueing sentinel: {e}")

    def get_frame(self, timeout: float = 1.0) -> object:
        try:
            return self.get(block=True, timeout=timeout)
        except Exception as e:
            print(f"[frameQueue] Error retrieving frame: {e}")
            return NULL_FRAME