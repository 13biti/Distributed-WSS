import multiprocessing

class Calculator:
    def __init__(self):
        manager = multiprocessing.Manager()
        self.last_sum = manager.dict()

    def sum(self, num1, num2):
        while True:
            result = num1 + num2
            self.last_sum.update({1: [{1: ["hello", "bye"]}, ["hello", 2, 3]]})

    def process_sum(self, num1, num2):
        process = multiprocessing.Process(target=self.sum, args=(num1, num2))
        process.start()
        # Do not join the process, let it run indefinitely

# Example usage
if __name__ == '__main__':
    calc = Calculator()
    calc.process_sum(3, 4)
    while True:
        print("Last sum:", calc.last_sum)

