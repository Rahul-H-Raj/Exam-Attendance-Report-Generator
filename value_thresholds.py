def set_threshold(data):
    data_dict = {index: value[1] for index, value in data.items()}
    threshold_dict = {}
    keys = list(data_dict.keys())

    increment = 5

    for i in range(0, len(keys), 4):
        chunk_keys = keys[i:i + 4]
        chunk_values = [data_dict[key] for key in chunk_keys]
        max_value = max(chunk_values)
        rounded_max = (int(max_value / 10) + 1) * 10
        
        # Adjust the rounded_max by the increment based on the chunk's position
        rounded_max += (i // 4) * increment

        for key in chunk_keys:
            threshold_dict[key] = rounded_max

    return threshold_dict