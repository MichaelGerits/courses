# TODO
alfabet = "abcdefghijklmnopqrstuvwxyz"
text = input("text: ").lower()
letter_amount = 0
word_amount = 1
sentence_amount = 0

for i in range(len(text)):
    if text[i] == " ":
        word_amount += 1
    elif text[i] == "." or text[i] == "!" or text[i] == "?":
        sentence_amount += 1
    elif text[i] in alfabet:
        letter_amount += 1

L = letter_amount / word_amount * 100
S = sentence_amount / word_amount * 100
CL_index = round(0.0588 * L - 0.296 * S - 15.8)

if CL_index >= 16:
    print("Grade 16+")

# set response if index is below 1
elif CL_index < 1:
    print("Before Grade 1")

# output index(grade)
else:
    print(f"Grade {CL_index}")