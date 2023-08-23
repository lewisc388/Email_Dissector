def join_strings_with_a(lst):
    result = []
    prev_string = ""

    for string in lst:
        if string.startswith("a"):
            prev_string += string
        else:
            if prev_string:
                result.append(prev_string)
            prev_string = string

    if prev_string:
        result.append(prev_string)

    return result

# Example usage
input_list = ["carrot", "apple", "apricot", "ali", "banana", "cherry", "apricot", "apartment", "date"]
output_list = join_strings_with_a(input_list)
print(output_list)