#script to filter out words shorter then 7

with open('words.txt') as f1:
    with open('source_words.txt', 'a') as f2:
        lines = f1.readlines()
        for i, line in enumerate(lines):
            if len(line) > 7:
                f2.write(line)
