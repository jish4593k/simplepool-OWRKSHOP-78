import ctypes
from typing import Any, Optional

class Chunk(ctypes.Structure):
    _fields_ = [("data", ctypes.c_void_p), ("next", ctypes.POINTER("Chunk"))]

class Cmpool:
    def __init__(self, size: int, length: int):
        # Initialize the pool with given size and length
        self.head: Optional[ctypes.POINTER(Chunk)] = None
        self.tail: Optional[ctypes.POINTER(Chunk)] = None
        self.remain = length
        self.size = size
        self.length = length

        # Create a linked list of chunks
        for i in range(self.length):
            p = ctypes.pointer(Chunk())
            p.contents.data = ctypes.c_void_p(ctypes.create_string_buffer(size))
            
            # Print the pointer value for demonstration
            print(p)

            if i == 0:
                self.head = self.tail = p
                continue

            self.tail.contents.next = p
            self.tail = p

    def __del__(self):
        print("-----------")

        # Cleanup the allocated memory on deletion
        while self.head:
            p = self.head

            print(f"s:{p}")

            self.head = p.contents.next

            if p:
                if p.contents.data:
                    ctypes.c_free(p.contents.data)
                    # Print the freed memory for demonstration
                    # print(f"d:{p.contents.data}")

                ctypes.c_free(p)

    def alloc(self) -> ctypes.POINTER(Chunk):
        # Allocate a chunk from the pool
        p = self.head
        self.head = p.contents.next
        self.remain -= 1

        p.contents.next = None

        return p

    def dealloc(self, p: ctypes.POINTER(Chunk)) -> None:
        # Deallocate a chunk and return it to the pool
        ctypes.memset(p, 0, ctypes.sizeof(Chunk))

        self.tail.contents.next = p
        self.tail = p

        self.remain += 1


def main():
    # Create an instance of Cmpool
    mp = Cmpool(128, 10)

    # Allocate a chunk from the pool
    p = mp.alloc()
    print(" ===== ")
    print(p)

    # Deallocate the chunk and return it to the pool
    mp.dealloc(p)
    # The pool is automatically cleaned up when it goes out of scope


if __name__ == "__main__":
    main()
