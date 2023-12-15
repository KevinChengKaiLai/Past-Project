from cs50 import get_string

# 0.0588 * L - 0.296 * S - 15.8
# L is the average number of letters per 100 words in the text,
# S is the average number of sentences per 100 words in the text.

text = get_string('Text: ')
letter = 0
sentence = 0

space = 0
for i in text:
    if i in [' ', '\n']:
        space += 1
    elif i in ['!','.','?' ]:
        sentence += 1
    elif i.isalpha() :
        letter += 1
word = space + 1

# print('sentence =',sentence)
# print('letter =',letter)
# print('word =', word)
L = float(letter) / float(word) *100
S = float(sentence) / float(word) *100

grade = 0.0588 * L - 0.296 * S - 15.8

if grade < 1:
    print('Before Grade 1')
elif grade >= 16:
    print('Grade 16+')
else:
    print("Grade",round(grade))

