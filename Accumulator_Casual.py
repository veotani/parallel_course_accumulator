import time


def main():
    numbers_sum = 0

    start = time.time()
    with open('numbers.bin', mode='rb') as f:
        count_numbers = 0
        while True:
            next_bytes = f.read(4) # считываем 4 байта, в которых хранится наше число
            if next_bytes == b'':
                break
            number = int.from_bytes(next_bytes, byteorder='little')
            print(number)
            numbers_sum += number
            count_numbers += 1

    end = time.time()

    with open('numbers_sum_casual.txt', mode='w+') as f:
        f.write('Результат получен. Сумма чисел: {}\nПотрачено времени: {}\nНайдено чисел: {}, равенство 512*1024: {}'
            .format(
                str(numbers_sum),
                str(end-start),
                count_numbers,
                count_numbers == 512*1024
            )
        )


if __name__ == '__main__':
    main()
