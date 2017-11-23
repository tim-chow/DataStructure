def _string_reverse(chars, from_index=None, end_index=None):
    if from_index is None:
        from_index = 0
    if end_index is None:
        end_index = len(chars) - 1

    if from_index > end_index:
        return chars

    middle = (from_index + end_index) / 2
    for i in range(from_index, middle + 1):
        j = end_index + from_index - i
        chars[i], chars[j] = chars[j], chars[i]

    return chars

def string_reverse(string):
    chars = list(string)
    chars = _string_reverse(chars)
    start = 0
    index = 0
    while index < len(chars):
        if chars[index] == " ":
            _string_reverse(chars, start, index-1)
            start = index + 1
        index = index + 1

    return "".join(chars)

if __name__ == "__main__":
    assert string_reverse("I am a student") == "student a am I"

