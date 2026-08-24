# scripts/validate_kynangsale.py
"""
Validates the /kynangsale/ question dataset and runtime integrity.
"""
import os
import sys
import json

if sys.platform.startswith('win'):
    sys.stdout.reconfigure(encoding='utf-8')

def validate_kynangsale():
    root = os.path.dirname(os.path.dirname(__file__))
    questions_file = os.path.join(root, "kynangsale", "questions.js")
    
    with open(questions_file, "r", encoding="utf-8") as f:
        content = f.read()
    
    # Extract json
    start = content.find("[")
    end = content.rfind("]") + 1
    questions = json.loads(content[start:end])
    
    print(f"Total Questions: {len(questions)}")
    assert len(questions) == 200, f"Expected 200 questions, got {len(questions)}"
    
    # 8 sections x 25
    sections = {}
    ans_counts = {}
    forbidden = ['tất cả', 'cả a và', 'cả b và', 'cả c và', 'cả 3', 'cả ba', 'các phương án trên', 'không có phương án', 'không có đáp án', 'cả hai']
    
    errors = []
    
    for i, q in enumerate(questions):
        sec = q.get('sectionNo')
        sections[sec] = sections.get(sec, 0) + 1
        ans = q.get('correctAnswer')
        ans_counts[ans] = ans_counts.get(ans, 0) + 1
        
        # Check options
        opts = q.get('options', [])
        if len(opts) != 4:
            errors.append(f"Question {q['id']} does not have 4 options")
        
        for opt in opts:
            for f_word in forbidden:
                if f_word in opt['text'].lower():
                    errors.append(f"Question {q['id']} opt {opt['key']} has forbidden phrase: '{f_word}'")
    
    print(f"Section distribution: {sections}")
    for s in range(1, 9):
        assert sections.get(s) == 25, f"Section {s} has {sections.get(s)} questions, expected 25"
    
    print(f"Answer distribution: {ans_counts}")
    for k in ['a', 'b', 'c', 'd']:
        assert ans_counts.get(k) == 50, f"Key {k} has {ans_counts.get(k)}, expected 50"
    
    if errors:
        print("ERRORS FOUND:")
        for err in errors:
            print(" -", err)
        sys.exit(1)
    
    print("ALL VALIDATION CHECKS PASSED PERFECTLY!")

if __name__ == "__main__":
    validate_kynangsale()
