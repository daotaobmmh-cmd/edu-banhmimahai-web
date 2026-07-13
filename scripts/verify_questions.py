import re
import json
import random

def run_verification():
    print("=== STARTING QUESTION DATA VALIDATOR ===")
    
    with open("hoinhap/questions.js", "r", encoding="utf-8") as f:
        content = f.read()
        
    # Extract JSON array
    match = re.search(r"window\.HOINHAP_QUESTIONS\s*=\s*(\[[\s\S]*\]);?", content)
    if not match:
        print("FAIL: Could not find window.HOINHAP_QUESTIONS in hoinhap/questions.js")
        return False
        
    questions = json.loads(match.group(1))
    
    # 1. Total questions count
    total_count = len(questions)
    if total_count != 177:
        print(f"FAIL: Total questions count is {total_count}, expected 177")
        return False
    print("PASS: Total questions count is 177")
    
    # 2. Check for unique and stable IDs
    ids = [q["id"] for q in questions]
    if len(ids) != len(set(ids)):
        print("FAIL: Duplicate IDs found in questions database")
        seen = set()
        dups = []
        for x in ids:
            if x in seen:
                dups.append(x)
            else:
                seen.add(x)
        print(f"Duplicates: {dups}")
        return False
    print("PASS: All question IDs are unique")
    
    # Check that q001 to q177 exist
    for i in range(1, 178):
        expected_id = f"q{i:03d}"
        if expected_id not in ids:
            print(f"FAIL: Missing expected ID {expected_id}")
            return False
    print("PASS: IDs q001 through q177 are fully present")
    
    # 3. Check section mapping and counts
    expected_counts = {
        1: 12, 2: 11, 3: 8, 4: 9, 5: 14, 6: 9, 7: 11, 8: 9,
        9: 13, 10: 6, 11: 5, 12: 5, 13: 10, 14: 11, 15: 10,
        16: 12, 17: 11, 18: 11
    }
    
    actual_counts = {}
    for q in questions:
        sec = q.get("sectionNo")
        actual_counts[sec] = actual_counts.get(sec, 0) + 1
        
    if len(actual_counts) != 18:
        print(f"FAIL: Number of sections is {len(actual_counts)}, expected 18")
        return False
    print("PASS: Exactly 18 sections present")
    
    for sec, exp_c in expected_counts.items():
        act_c = actual_counts.get(sec, 0)
        if act_c != exp_c:
            print(f"FAIL: Section {sec} count is {act_c}, expected {exp_c}")
            return False
    print("PASS: All 18 sections have expected question counts")
    
    # 4. Check option and answer formatting
    for q in questions:
        q_id = q["id"]
        # Options check
        opts = q.get("options", [])
        if len(opts) != 4:
            print(f"FAIL: Question {q_id} has {len(opts)} options, expected 4")
            return False
            
        keys = [opt.get("key") for opt in opts]
        if keys != ["A", "B", "C", "D"]:
            print(f"FAIL: Question {q_id} options keys are {keys}, expected ['A', 'B', 'C', 'D']")
            return False
            
        for opt in opts:
            if not opt.get("text"):
                print(f"FAIL: Question {q_id} option {opt.get('key')} has empty text")
                return False
                
        # Correct answer check
        ans = q.get("correctAnswer")
        if ans not in ["A", "B", "C", "D"]:
            print(f"FAIL: Question {q_id} correctAnswer is '{ans}', expected one of A, B, C, D")
            return False
            
        # Explanation check
        exp = q.get("explanation", "").strip()
        if not exp:
            print(f"FAIL: Question {q_id} has empty explanation")
            return False
            
        # Content hygiene checks
        banned_strings = ["**", "<details", "</details", "<summary", "</summary", "<br"]
        fields_to_check = [
            ("question", q.get("question", "")),
            ("explanation", q.get("explanation", ""))
        ]
        for opt in opts:
            fields_to_check.append((f"option {opt.get('key')}", opt.get("text", "")))
            
        for field_name, field_val in fields_to_check:
            for b in banned_strings:
                if b in field_val:
                    print(f"FAIL: Question {q_id} {field_name} contains banned content '{b}': '{field_val}'")
                    return False
            # Check for raw HTML tags
            if re.search(r'</?[a-zA-Z]+[^>]*>', field_val):
                print(f"FAIL: Question {q_id} {field_name} contains raw HTML tag: '{field_val}'")
                return False
            # Check for stray leading punctuation
            if re.match(r'^[,\.\-\s✅]+', field_val) and len(field_val.strip()) > 0:
                print(f"FAIL: Question {q_id} {field_name} has stray leading punctuation: '{field_val}'")
                return False

        # Sequential number checks
        num = q.get("number")
        disp_num = q.get("displayNumber")
        if num != disp_num:
            print(f"FAIL: Question {q_id} has mismatch between number ({num}) and displayNumber ({disp_num})")
            return False
            
    print("PASS: All questions have 4 options, valid correct answers, and non-empty explanations")
    
    # 5. Check sequential display numbers 1 to 177
    nums = [q["number"] for q in questions]
    if nums != list(range(1, 178)):
        print("FAIL: Sequential question numbers are not 1 to 177")
        return False
    print("PASS: Sequential question numbers are exactly 1 to 177")
    
    # 6. Simulate test selection logic to verify balanced test (10/10/10)
    for run in range(100):
        # pickTest logic
        q13 = [q for q in questions if q["source"] == "1.3" and q.get("active") != False]
        q14 = [q for q in questions if q["source"] == "1.4" and q.get("active") != False]
        q65 = [q for q in questions if q["source"] == "65" and q.get("active") != False]
        
        random.shuffle(q13)
        random.shuffle(q14)
        random.shuffle(q65)
        
        selected13 = q13[:10]
        selected14 = q14[:10]
        selected65 = q65[:10]
        
        test_set = selected13 + selected14 + selected65
        
        if len(test_set) != 30:
            print(f"FAIL [Run {run}]: Test set size is {len(test_set)}, expected 30")
            return False
            
        # Check counts per source
        c13 = sum(1 for q in test_set if q["source"] == "1.3")
        c14 = sum(1 for q in test_set if q["source"] == "1.4")
        c65 = sum(1 for q in test_set if q["source"] == "65")
        
        if c13 != 10 or c14 != 10 or c65 != 10:
            print(f"FAIL [Run {run}]: Balance mismatch - 1.3: {c13}, 1.4: {c14}, 65: {c65}")
            return False
            
        # Check option ordering: must not be shuffled (must remain A, B, C, D)
        for q in test_set:
            opt_keys = [opt["key"] for opt in q["options"]]
            if opt_keys != ["A", "B", "C", "D"]:
                print(f"FAIL [Run {run}]: Options key order is {opt_keys}, expected ['A', 'B', 'C', 'D']")
                return False
                
    print("PASS: Balanced test selection simulation (100 runs) is 10/10/10 with strict option order")
    print("=== ALL VALIDATIONS PASSED SUCCESSFULLY ===")
    return True

if __name__ == "__main__":
    import sys
    success = run_verification()
    sys.exit(0 if success else 1)
