import time
import threading
import mmap
from queue import Queue


class AccumulatorMultithreaded:

    def __init__(self, file_name):
        self.file_name = file_name
        self.num_threads = 12

    def sum_numbers_in_mm(self, mm, thread_number):
        print(f'Thread {thread_number} begins computations')
        res = 0
        for file_pos in range(thread_number * 4, len(mm), 4 * self.num_threads):
            number = int.from_bytes(mm[file_pos: file_pos + 4], byteorder='little')
            res += number
        return res

    def file_to_mm(self):
        with open(self.file_name, "r+b") as f:
            return mmap.mmap(f.fileno(), 0)

    def get_numbers_sum(self):
        mm = self.file_to_mm()

        threads = []
        queue = Queue()
        for thread_number in range(self.num_threads):
            new_thread = threading.Thread(
                target=lambda sum_func, q, thread_num: q.put(sum_func(mm, thread_num)),
                args=(self.sum_numbers_in_mm, queue, thread_number)
            )
            threads.append(new_thread)

        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()

        numbers_sum = 0
        while not queue.empty():
            numbers_sum += queue.get()

        return numbers_sum

    def write_number_sum_to_file(self):
        start = time.time()
        numbers_sum = self.get_numbers_sum()
        end = time.time()
        with open('numbers_sum_parallel.txt', encoding='utf8', mode='w+') as f:
            f.write(f'Потрачено времени: {end - start}\nСумма чисел: {numbers_sum}')


def main():
    accumulator = AccumulatorMultithreaded('numbers.bin')
    accumulator.write_number_sum_to_file()


if __name__ == '__main__':
    main()
