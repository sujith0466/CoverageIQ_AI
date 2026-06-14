class LegacyProcessor:
    def process_data(self, data):
        if not data:
            return None
        return [d * 2 for d in data]
        
    def complex_transform(self, x, y):
        if x > y:
            return x - y
        elif x < y:
            return y - x
        else:
            return 0

def old_utility_function():
    print("This has never been tested")
    return True
