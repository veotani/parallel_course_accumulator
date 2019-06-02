import time
import threading
import mmap
from queue import Queue


def get_start_positions(mm):
	mm_len = len(mm)
	return [pos for pos in range(mm_len) if pos % 4 == 0 and pos < len(mm) - 3]


def sum_numbers_in_mm(mm, start_positions):
	res = 0
	for start_pos in start_positions:
		number = int.from_bytes(mm[start_pos:start_pos+4], byteorder='little')
		res += number
	print(f'Current thread has counted {res} and got {len(start_positions)} numbers')
	return res


class AccumulatorMultithreaded:

	def __init__(self, file_name):
		self.file_name = file_name
		self.num_threads = 4

	def get_positions_for_thread_number(self, thread_number, start_positions):
		res = [pos for pos in start_positions if (pos // 4) % self.num_threads == thread_number]
		return res

	def file_to_mm(self):
		with open(self.file_name, "r+b") as f:
			return mmap.mmap(f.fileno(), 0)

	def get_numbers_sum(self):
		mm = self.file_to_mm()
		start_poss = get_start_positions(mm)
		threads = []
		queue = Queue()
		for thread_number in range(self.num_threads):
			thread_positions = self.get_positions_for_thread_number(thread_number, start_poss)
			new_thread = threading.Thread(
				target=lambda sum_func, q, positions: q.put(sum_func(mm, positions)),
				args=(sum_numbers_in_mm, queue, thread_positions)
			)
			threads.append(new_thread)
		print("Threads:")
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
			f.write(f'Потрачено времени: {end-start}\nСумма чисел: {numbers_sum}')


def main():
	accumulator = AccumulatorMultithreaded('numbers.bin')
	accumulator.write_number_sum_to_file()


if __name__ == '__main__':
	main()
