from tqdm import tqdm
import time



pbar = tqdm(total=512*1024*1024) # Создаём шкалу прогресса
numbers_sum = 0

start = time.time()
with open('numbers.bin', mode='rb') as f:
    a = True # инициализируем переменную, в которую будут считываться числа. 
             # цикл работает пока в этой переменной что-то есть
    while a:
        a = f.read(4) # считываем 4 байта, в которых хранится наше число
		
        # if a: # вариант, при котором мы проверяем, не закончились ли числа ещё и внутри, 
                # но для ускорения работы мы такую проверку делать не будем, т.к.
                # в конце мы просто считаем и распакуем значение 0, что не изменит сумму
				
        #     print(int.from_bytes(a, byteorder='little')) # do smth with number
		
        pbar.update(1) # сообщаем шкале прогресса, 
					   # что одна итерация прошла
        numbers_sum += int.from_bytes(a, byteorder='little')

end = time.time()
pbar.close()

with open('numbers_sum_casual.txt', mode='w+') as f:
    f.write('Результат получен. Сумма чисел: {}\nПотрачено времени: {}'.format(str(numbers_sum), str(end-start)))