function app() {
    return {
        // App State
        currentView: 'gate', // 'gate', 'study', 'test', 'result'
        showGuide: false,
        showConfirmSubmit: false,
        
        // Learner State
        learnerName: '',
        learnerDept: '',
        
        // Questions Data
        allQuestions: [],
        sections: [], // { no, title, total, answered, progress, questions }
        
        // Study Mode State
        activeSectionIndex: 0,
        studyIndex: 0,
        studyProgress: {}, // maps question ID to selected answer key
        
        // Test Mode State
        testQuestions: [], // 30 selected questions
        testAnswers: {}, // maps question ID to selected answer key
        testCurrentIndex: 0,
        testTimer: 1800, // 30 minutes in seconds
        testTimerInterval: null,
        testStartTime: null,
        
        // Result State
        resultScore: 0,
        resultPassed: false,
        resultTimeSpent: '',
        resultWrongQuestions: [], // questions answered incorrectly in test
        
        // Init
        init() {
            // Load questions from window.HOINHAP_QUESTIONS
            this.allQuestions = window.HOINHAP_QUESTIONS || [];
            
            // Load learner info from localStorage
            this.learnerName = localStorage.getItem('hoinhap:learnerName') || '';
            this.learnerDept = localStorage.getItem('hoinhap:learnerDept') || '';
            
            // Load study progress from localStorage
            try {
                const savedProgress = localStorage.getItem('hoinhap:studyProgress');
                if (savedProgress) {
                    this.studyProgress = JSON.parse(savedProgress);
                }
            } catch (e) {
                console.error('Failed to parse study progress', e);
            }
            
            // Initialize sections list
            this.updateSections();
            
            // Auto-select first section if available
            if (this.sections.length > 0) {
                this.activeSectionIndex = 0;
            }
        },

        // Helper: Shuffle array
        shuffle(arr) {
            return [...arr].sort(() => Math.random() - 0.5);
        },

        // Update Sections list progress
        updateSections() {
            const map = new Map();
            this.allQuestions.forEach(q => {
                if (!map.has(q.sectionNo)) {
                    map.set(q.sectionNo, {
                        no: q.sectionNo,
                        title: q.sectionName,
                        questions: []
                    });
                }
                map.get(q.sectionNo).questions.push(q);
            });
            
            this.sections = [...map.values()]
                .sort((a, b) => a.no - b.no)
                .map(sec => {
                    const total = sec.questions.length;
                    const answered = sec.questions.filter(q => this.studyProgress[q.id] !== undefined).length;
                    const progress = total > 0 ? Math.round((answered / total) * 100) : 0;
                    return {
                        ...sec,
                        total,
                        answered,
                        progress
                    };
                });
        },

        // Study Mode: select section
        selectSection(index) {
            this.activeSectionIndex = index;
            this.studyIndex = 0;
        },

        // Study Mode: get current question
        get currentStudyQuestion() {
            const sec = this.sections[this.activeSectionIndex];
            if (!sec || !sec.questions) return null;
            return sec.questions[this.studyIndex];
        },

        // Study Mode: select answer
        selectStudyAnswer(optionKey) {
            const q = this.currentStudyQuestion;
            if (!q || this.studyProgress[q.id] !== undefined) return;
            
            // Save answer
            this.studyProgress[q.id] = optionKey;
            localStorage.setItem('hoinhap:studyProgress', JSON.stringify(this.studyProgress));
            
            // Update sections progress
            this.updateSections();
        },

        // Study Mode: navigation
        prevStudyQuestion() {
            this.studyIndex = Math.max(0, this.studyIndex - 1);
        },
        nextStudyQuestion() {
            const sec = this.sections[this.activeSectionIndex];
            if (sec && this.studyIndex < sec.questions.length - 1) {
                this.studyIndex++;
            }
        },

        // Study Mode: Styling helpers
        getStudyOptionClass(option) {
            const q = this.currentStudyQuestion;
            if (!q) return '';
            const answeredKey = this.studyProgress[q.id];
            if (answeredKey === undefined) {
                return 'border-slate-100 bg-white hover:border-secondary/30 hover:bg-slate-50';
            }
            if (option.key === q.correctAnswer) {
                return 'border-primary/20 bg-primary/10 text-slate-800 border-2';
            }
            if (option.key === answeredKey) {
                return 'border-error/20 bg-error/10 text-error border-2';
            }
            return 'border-slate-200 bg-white text-slate-500';
        },
        getStudyLetterClass(option) {
            const q = this.currentStudyQuestion;
            if (!q) return '';
            const answeredKey = this.studyProgress[q.id];
            if (answeredKey === undefined) {
                return 'bg-slate-50 text-slate-400 group-hover:bg-secondary group-hover:text-white';
            }
            if (option.key === q.correctAnswer) {
                return 'bg-primary text-white';
            }
            if (option.key === answeredKey) {
                return 'bg-error text-white';
            }
            return 'bg-slate-100 text-slate-400';
        },

        // Study Mode stats helper
        get currentSectionProgress() {
            const sec = this.sections[this.activeSectionIndex];
            return sec ? sec.progress : 0;
        },
        get currentSectionRemaining() {
            const sec = this.sections[this.activeSectionIndex];
            return sec ? (sec.total - sec.answered) : 0;
        },
        get roadProgress() {
            const total = this.allQuestions.length;
            const answered = Object.keys(this.studyProgress).length;
            return total > 0 ? Math.round((answered / total) * 100) : 0;
        },
        get roadCompletedSections() {
            return this.sections.filter(sec => sec.progress === 100).length;
        },

        // Dynamic helper to find the first section with progress < 100
        get shouldContinueSectionIndex() {
            return this.sections.findIndex(sec => sec.progress < 100);
        },

        // Evaluates the CSS classes of a section card dynamically
        getSectionCardClass(idx, activeSectionIndex) {
            const sec = this.sections[idx];
            if (!sec) return '';
            
            let base = 'relative p-4 rounded-2xl cursor-pointer transition-all focus-visible:ring-2 focus-visible:ring-secondary focus-visible:outline-none border-2 ';
            
            if (activeSectionIndex === idx) {
                // Active Card: Blue border #00ADEF, light blue tint
                base += 'border-secondary bg-secondary/5 ring-1 ring-secondary/35 ';
            } else {
                // Learning Status Card
                if (sec.progress === 100) {
                    // Đã học xong: Green border #39B54A, light green tint
                    base += 'border-primary/20 bg-primary/5 text-slate-800';
                } else if (idx === this.shouldContinueSectionIndex || sec.progress > 0) {
                    // Đang học / nên tiếp tục: Warning border #F4CC34, white bg
                    base += 'border-warning bg-white text-slate-800';
                } else {
                    // Chưa học: Gray border, white background
                    base += 'border-slate-100 bg-white text-slate-500 hover:border-slate-200';
                }
            }
            return base;
        },

        // Test Mode: Pick 30 random questions (10 from 1.3, 10 from 1.4, 10 from 65)
        pickTest() {
            const q13 = this.allQuestions.filter(q => q.source === '1.3' && q.active !== false);
            const q14 = this.allQuestions.filter(q => q.source === '1.4' && q.active !== false);
            const q65 = this.allQuestions.filter(q => q.source === '65' && q.active !== false);
            
            const selected13 = this.shuffle(q13).slice(0, 10);
            const selected14 = this.shuffle(q14).slice(0, 10);
            const selected65 = this.shuffle(q65).slice(0, 10);
            
            let finalSet = [...selected13, ...selected14, ...selected65];
            
            if (finalSet.length < 30) {
                const fallback = this.allQuestions.filter(q => !finalSet.includes(q) && q.active !== false);
                finalSet = [...finalSet, ...this.shuffle(fallback).slice(0, 30 - finalSet.length)];
            }
            
            return this.shuffle(finalSet.map(q => ({
                ...q,
                options: q.options // Keep options in A/B/C/D order
            })));
        },

        // Test Mode: Start test
        startTest() {
            if (!this.learnerName.trim()) {
                alert('Vui lòng nhập họ tên trước khi bắt đầu bài thi.');
                return;
            }
            
            // Save info
            localStorage.setItem('hoinhap:learnerName', this.learnerName.trim());
            localStorage.setItem('hoinhap:learnerDept', this.learnerDept.trim());
            
            // Initialize test state
            this.testQuestions = this.pickTest();
            this.testAnswers = {};
            this.testCurrentIndex = 0;
            this.testTimer = 1800; // 30 minutes
            this.testStartTime = new Date();
            
            // Launch timer
            if (this.testTimerInterval) clearInterval(this.testTimerInterval);
            this.testTimerInterval = setInterval(() => {
                if (this.currentView === 'test' && this.testTimer > 0) {
                    this.testTimer--;
                    if (this.testTimer === 0) {
                        this.submitTest(true);
                    }
                }
            }, 1000);
            
            this.currentView = 'test';
        },

        // Test Mode: get current question
        get currentTestQuestion() {
            return this.testQuestions[this.testCurrentIndex];
        },

        // Test Mode: select option
        selectTestAnswer(optionKey) {
            const q = this.currentTestQuestion;
            if (!q) return;
            this.testAnswers[q.id] = optionKey;
        },

        // Test Mode: navigation
        prevTestQuestion() {
            this.testCurrentIndex = Math.max(0, this.testCurrentIndex - 1);
        },
        nextTestQuestion() {
            if (this.testCurrentIndex < 29) {
                this.testCurrentIndex++;
            } else {
                this.showConfirmSubmit = true;
            }
        },
        jumpToTestQuestion(index) {
            this.testCurrentIndex = index;
        },

        // Helper to format seconds to mm:ss
        formatTime(sec) {
            const m = Math.floor(sec / 60);
            const s = sec % 60;
            return `${m.toString().padStart(2, '0')}:${s.toString().padStart(2, '0')}`;
        },

        // Test Mode: Submit test
        submitTest(auto = false) {
            if (!auto) {
                const unansweredCount = 30 - Object.keys(this.testAnswers).length;
                if (unansweredCount > 0 && !confirm(`Bạn còn ${unansweredCount} câu chưa trả lời. Vẫn nộp bài?`)) {
                    this.showConfirmSubmit = false;
                    return;
                }
            }
            
            this.showConfirmSubmit = false;
            if (this.testTimerInterval) clearInterval(this.testTimerInterval);
            
            // Calculate score
            let correct = 0;
            const wrong = [];
            this.testQuestions.forEach((q, idx) => {
                const ans = this.testAnswers[q.id];
                if (ans === undefined || ans === null) {
                    // Unanswered: marked as wrong
                    wrong.push({
                        question: q,
                        index: idx,
                        selectedAnswer: null
                    });
                } else if (ans === q.correctAnswer) {
                    correct++;
                } else {
                    wrong.push({
                        question: q,
                        index: idx,
                        selectedAnswer: ans
                    });
                }
            });
            
            this.resultScore = correct;
            this.resultPassed = correct >= 24; // 80% correct (24/30)
            
            // Calculate time spent
            const endTime = new Date();
            const diffMs = endTime - this.testStartTime;
            const diffSecs = Math.floor(diffMs / 1000);
            const m = Math.floor(diffSecs / 60);
            const s = diffSecs % 60;
            this.resultTimeSpent = `${m.toString().padStart(2, '0')}:${s.toString().padStart(2, '0')}`;
            
            this.resultWrongQuestions = wrong;
            
            // Save last result
            localStorage.setItem('hoinhap:lastResult', JSON.stringify({
                name: this.learnerName.trim(),
                dept: this.learnerDept.trim(),
                correct,
                pass: this.resultPassed,
                at: new Date().toISOString()
            }));
            
            this.currentView = 'result';
        },

        // Study Mode: Enter study view
        startStudy() {
            if (!this.learnerName.trim()) {
                alert('Vui lòng nhập họ tên trước khi bắt đầu.');
                return;
            }
            
            // Save info
            localStorage.setItem('hoinhap:learnerName', this.learnerName.trim());
            localStorage.setItem('hoinhap:learnerDept', this.learnerDept.trim());
            
            this.currentView = 'study';
        }
    }
}
