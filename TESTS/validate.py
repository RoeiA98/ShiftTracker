def check_name(name):
    words = name.split()
    return len(words) == 2 and all(word.isalpha() for word in words)