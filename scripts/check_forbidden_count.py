import json
import re

with open('kynangsale/questions.js', 'r', encoding='utf-8') as f:
    text = f.read()

start = text.find('[')
end = text.rfind(']') + 1
questions = json.loads(text[start:end])

print(f"Loaded {len(questions)} questions.")

# Let's inspect how many questions have forbidden words
forbidden = ['tất cả', 'cả a và', 'cả b và', 'cả c và', 'cả 3', 'cả ba', 'các phương án trên', 'không có phương án', 'không có đáp án', 'cả hai']

def has_forbidden(opt_text):
    t = opt_text.lower()
    return any(f in t for f in forbidden)

# Check all
count = 0
for q in questions:
    for opt in q['options']:
        if has_forbidden(opt['text']):
            count += 1
            break

print(f"Questions with forbidden words: {count}")
