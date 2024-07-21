def binary_search(arr, value):
    low = 0
    high = len(arr) - 1
    iterations = 0
    upper_bound = None
    
    while low <= high:
        iterations += 1
        mid = (low + high) // 2
        if arr[mid] < value:
            low = mid + 1
        elif arr[mid] > value:
            high = mid - 1
            # Оновлюємо верхню межу
            upper_bound = arr[mid]  
        else:
             # Знайдено точне значення
            upper_bound = arr[mid]
            break 
    if upper_bound is None and low < len(arr):
         # Якщо значення більше за всі елементи
        upper_bound = arr[low] 
    
    return (iterations, upper_bound)

sorted_array = [2.5, 3.2, 4.8, 5.4, 6.1, 7.7, 9.9]
value = 5.0
result = binary_search(sorted_array, value)
print(result) 