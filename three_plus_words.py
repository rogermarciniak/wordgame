#script to filter out words shorter then 3

with open('dictionary.txt') as f1:
    with open('acceptable_words.txt', 'a') as f2:
        lines = f1.readlines()
        for i, line in enumerate(lines):
            if len(line) > 3:
                f2.write(line)
