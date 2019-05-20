def generate_2gigs_numbers():
    with open('numbers.bin', mode='wb+') as f:
        for i in tqdm(range(512*1024*1024)):
            n = generate_32bit_number()
            f.write(n)

def generate_32bit_number():
    return np.random.randint(2**32, dtype='uint')

def main():
	generate_2gigs_numbers()
	
if __name__ = '__main__':
	main()