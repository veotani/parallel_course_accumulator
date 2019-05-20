import time
import threading
import mmap
import math
import queue



def SumNumbersInFile(mm, from_pos, to_pos):
	print('Starting processing file positions from {} to {}'.format(from_pos, to_pos))
	res = 0
	for i in range(from_pos//4, to_pos//4):
		res += int.from_bytes(mm[i*4:(i+1)*4], byteorder='little')
	print('Ended processing file positions from {} to {}'.format(from_pos, to_pos))
	return res


def main():
	
	que = queue.Queue()
	
	threads = []
	num_of_threads = 12
	
	with open("numbers.bin", "r+b") as f:
		mm = mmap.mmap(f.fileno(), 0)
		total_len = len(mm)
		ps = total_len // num_of_threads # piece size
		
		start = time.time()
		
		for i in range(num_of_threads):
			if (i == (total_len - 1)):
				threads.append(threading.Thread(
					target=lambda foo, q, mm, from_p, to_p: q.put(foo(mm, from_p, to_p)), 
					args=(SumNumbersInFile, que, mm, i*ps, total_len)
				))
			else:
				threads.append(threading.Thread(
					target=lambda foo, q, mm, from_p, to_p: q.put(foo(mm, from_p, to_p)), 
					args=(SumNumbersInFile, que, mm, i*ps, (i+1)*ps)
				))
				
		for thread in threads:
			thread.start()
		
		for thread in threads:
			thread.join()
		
		end = time.time()
		
		numbers_sum = 0
		while not que.empty():
			numbers_sum += que.get()
			print(numbers_sum)
		
		print('result is: {}'.format(numbers_sum))
		mm.close()
	
	with open('numbers_sum_parallel.txt', mode='w+') as f:
		f.write('Результат получен. Сумма чисел: {}\nПотрачено времени: {}'.format(str(numbers_sum), str(end-start)))

if __name__ == '__main__':
    main()