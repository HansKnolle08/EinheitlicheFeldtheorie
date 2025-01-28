import time

def timestamp_dec(funktion):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = funktion(*args, **kwargs)
        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"Die Funktion '{funktion.__name__}' dauerte {elapsed_time:.4f} Sekunden.")
    return wrapper