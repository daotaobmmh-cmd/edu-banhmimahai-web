function app() {
    const DATASET_VERSION = 'kynangsale-v2.0';
    return {
        // App State
        currentView: 'gate', // 'gate', 'study', 'test', 'result'
        showGuide: false,
        lightboxImage: null,
        showConfirmSubmit: false,
        
        // Learner State
        learnerName: '',
        phoneNumber: '', // Số điện thoại học viên
        
        // Questions Data
        allQuestions: [],
        sections: [], // { no, title, total, answered, progress, questions }
        
        // Study Mode State
        activeSectionIndex: 0,
        studyIndex: 0,
        studyProgress: {}, // maps question ID to selected answer key
        
        // Test Mode State
        testQuestions: [], // 60 selected questions from 8 sections
        testAnswers: {}, // maps question ID to selected answer key
        testCurrentIndex: 0,
        testTimer: 2700, // 45 minutes in seconds
        testTimerInterval: null,
        testStartTime: null,
        testAttemptId: '',
        testStartedAtISO: '',
        testSubmittedAtISO: '',
        testDurationSeconds: 0,
        
        // Result State
        resultScore: 0,
        resultPassed: false,
        resultThreshold: 48, // 48/60 (80%) correct answers to pass
        resultTimeSpent: '',
        resultWrongQuestions: [], // questions answered incorrectly in test
        resultUnansweredCount: 0,
        resultSendingStatus: 'idle', // 'idle', 'sending', 'success', 'error'
        resultErrorMessage: '',
        isSubmittingResult: false,
        resultAutoRetryAttempt: 0,
        
        // Feedback State & Micro-interactions
        feedbackTexts: {}, // maps question ID to text
        feedbackStatuses: {}, // maps question ID to 'idle', 'sending', 'success', 'error'
        showUnsentGuard: false,
        pendingNavigationFn: null,
        showSuccessOverlay: false,
        isGuardSubmitting: false,
        guardErrorText: '',
        previouslyFocusedElement: null,
        successOverlayTimer: null,
        downloadingCertificate: false,
        resultSaved: false,
        certificateDownloadFailed: false,
        
        // Init
        init() {
            // Load questions from window.KYNANGSALE_QUESTIONS or fallback window.HOINHAP_QUESTIONS
            const rawQuestions = (typeof window !== 'undefined' ? (window.KYNANGSALE_QUESTIONS || window.HOINHAP_QUESTIONS) : (global.KYNANGSALE_QUESTIONS || global.HOINHAP_QUESTIONS)) || [];
            
            // Map questions to 8 standardized sections (25 questions each)
            this.allQuestions = rawQuestions.map((q, index) => {
                let sectionNo = q.sectionNo;
                let sectionName = q.sectionName || "";
                
                if (!sectionNo) {
                    const calculatedNo = Math.floor(index / 25) + 1;
                    sectionNo = calculatedNo <= 8 ? calculatedNo : 8;
                }
                
                return {
                    ...q,
                    sectionNo,
                    sectionName
                };
            });

            // Preload question images in the background for instant rendering
            if (typeof Image !== 'undefined') {
                this.allQuestions.forEach(q => {
                    if (q.image) {
                        const img = new Image();
                        img.src = q.image;
                    }
                });
            }
            
            // Load learner info from localStorage
            if (typeof localStorage !== 'undefined') {
                this.learnerName = localStorage.getItem('kynangsale:learnerName') || '';
                this.phoneNumber = localStorage.getItem('kynangsale:phoneNumber') || '';
                
                // Check dataset version in localStorage
                const savedVersion = localStorage.getItem('kynangsale:datasetVersion');
                if (savedVersion !== DATASET_VERSION) {
                    localStorage.removeItem('kynangsale:studyProgress');
                    localStorage.removeItem('kynangsale:lastResult');
                    localStorage.setItem('kynangsale:datasetVersion', DATASET_VERSION);
                    this.studyProgress = {};
                } else {
                    // Load study progress from localStorage
                    try {
                        const savedProgress = localStorage.getItem('kynangsale:studyProgress');
                        if (savedProgress) {
                            this.studyProgress = JSON.parse(savedProgress);
                        }
                    } catch (e) {
                        console.error('Failed to parse study progress', e);
                    }
                }
            }
            
            // Initialize sections list
            this.updateSections();
            
            // Auto-select first section if available
            if (this.sections.length > 0) {
                this.activeSectionIndex = 0;
            }

            // Auto-resend pending quiz result if browser closed/refreshed after error
            if (typeof localStorage !== 'undefined') {
                try {
                    const rawPending = localStorage.getItem('kynangsale:pendingQuizResult');
                    if (rawPending) {
                        const pendingPayload = JSON.parse(rawPending);
                        if (pendingPayload && pendingPayload.attemptId) {
                            this.postQuizResult(pendingPayload).catch(() => {});
                        }
                    }
                } catch (e) {}
            }
            
            // Watch changes to adjust certificate text sizes
            if (typeof this.$watch === 'function') {
                this.$watch('learnerName', () => this.adjustCertLayout());
                this.$watch('phoneNumber', () => this.adjustCertLayout());
                this.$watch('currentView', (view) => {
                    if (view === 'result') {
                        const delays = [50, 150, 300, 600, 1000, 2000];
                        delays.forEach(delay => {
                            setTimeout(() => this.adjustCertLayout(), delay);
                        });
                        if (typeof document !== 'undefined' && document.fonts) {
                            document.fonts.ready.then(() => {
                                this.adjustCertLayout();
                            });
                        }
                    }
                });
            }

            // Set initialization flag and hide fallback UI
            if (typeof window !== 'undefined') {
                window.alpineInitialized = true;
            }
            if (typeof document !== 'undefined') {
                document.documentElement.classList.add('alpine-ready');
                const fallbackEl = document.getElementById('app-fallback');
                if (fallbackEl) {
                    fallbackEl.style.display = 'none';
                }
            }
        },

        // Helper: Shuffle array
        shuffle(arr) {
            return [...arr].sort(() => Math.random() - 0.5);
        },

        // Update Sections list progress
        updateSections() {
            const canonicalTitles = [
                "Phần 1: Nhập môn Nhượng quyền & Lợi thế Mô hình",
                "Phần 2: Phân loại Khách hàng & Kỹ năng Tư vấn",
                "Phần 3: Khảo sát Vị trí, Mặt bằng & Khung giờ Bán hàng",
                "Phần 4: Kỹ thuật Chiên chả, Làm bánh & An toàn Vệ sinh",
                "Phần 5: Xử lý Từ chối & Giải tỏa Rào cản Đối tác",
                "Phần 6: Kỹ năng Vận hành Ca sáng & Xử lý Sự cố Điểm bán",
                "Phần 7: Pháp lý, Quan hệ Cộng đồng & Phát triển Bền vững",
                "Phần 8: Chốt Deal Thực chiến, Tối ưu Lợi nhuận & Văn hóa Phụng sự"
            ];
            
            const map = new Map();
            this.allQuestions.forEach(q => {
                const sNo = q.sectionNo || 1;
                if (!map.has(sNo)) {
                    map.set(sNo, {
                        no: sNo,
                        title: canonicalTitles[sNo - 1] || q.sectionName || `Phần ${sNo}`,
                        questions: []
                    });
                }
                map.get(sNo).questions.push(q);
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

        // Helper: Check if question has unsent non-empty feedback
        hasUnsentFeedback(qId) {
            if (!qId) return false;
            const currentText = (this.feedbackTexts[qId] || '').trim();
            return currentText.length > 0;
        },

        getCurrentActiveQuestion() {
            if (this.currentView === 'study') return this.currentStudyQuestion;
            if (this.currentView === 'test') return this.currentTestQuestion;
            return null;
        },

        guardNavigation(targetFn) {
            const currentQ = this.getCurrentActiveQuestion();
            if (currentQ && this.hasUnsentFeedback(currentQ.id)) {
                this.previouslyFocusedElement = document.activeElement;
                this.pendingNavigationFn = targetFn;
                this.guardErrorText = '';
                this.showUnsentGuard = true;
                return;
            }
            if (typeof targetFn === 'function') {
                targetFn();
            }
        },

        cancelGuard() {
            if (this.isGuardSubmitting || this.showSuccessOverlay) return;
            this.showUnsentGuard = false;
            this.guardErrorText = '';
            this.pendingNavigationFn = null;
            if (this.previouslyFocusedElement && typeof this.previouslyFocusedElement.focus === 'function' && document.body.contains(this.previouslyFocusedElement)) {
                this.previouslyFocusedElement.focus();
            }
            this.previouslyFocusedElement = null;
        },

        confirmDiscardGuard() {
            if (this.isGuardSubmitting || this.showSuccessOverlay) return;
            const fn = this.pendingNavigationFn;
            this.showUnsentGuard = false;
            this.guardErrorText = '';
            this.pendingNavigationFn = null;
            this.previouslyFocusedElement = null;
            if (typeof fn === 'function') {
                fn();
                this.focusActiveQuestionTarget();
            }
        },

        async confirmSendGuard() {
            if (this.isGuardSubmitting) return;
            const currentQ = this.getCurrentActiveQuestion();
            if (!currentQ) return;

            this.isGuardSubmitting = true;
            this.guardErrorText = '';
            const mode = this.currentView === 'test' ? 'test' : 'practice';

            try {
                await this.submitFeedback(currentQ, mode, { fromGuard: true });
            } finally {
                this.isGuardSubmitting = false;
            }
        },

        handleGuardTab(e) {
            if (!this.showUnsentGuard) return;
            const focusables = [this.$refs.guardDiscardBtn, this.$refs.guardSendBtn].filter(Boolean);
            if (focusables.length === 0) return;
            const first = focusables[0];
            const last = focusables[focusables.length - 1];

            if (e.shiftKey) {
                if (document.activeElement === first || !focusables.includes(document.activeElement)) {
                    e.preventDefault();
                    last.focus();
                }
            } else {
                if (document.activeElement === last || !focusables.includes(document.activeElement)) {
                    e.preventDefault();
                    first.focus();
                }
            }
        },

        focusActiveQuestionTarget() {
            this.$nextTick(() => {
                if (this.currentView === 'study') {
                    if (this.$refs.practiceQuestionHeading && typeof this.$refs.practiceQuestionHeading.focus === 'function') {
                        this.$refs.practiceQuestionHeading.focus();
                        return;
                    }
                    if (this.$refs.practiceQuestionCard && typeof this.$refs.practiceQuestionCard.focus === 'function') {
                        this.$refs.practiceQuestionCard.focus();
                        return;
                    }
                } else if (this.currentView === 'test') {
                    if (this.$refs.testQuestionHeading && typeof this.$refs.testQuestionHeading.focus === 'function') {
                        this.$refs.testQuestionHeading.focus();
                        return;
                    }
                    if (this.$refs.testQuestionCard && typeof this.$refs.testQuestionCard.focus === 'function') {
                        this.$refs.testQuestionCard.focus();
                        return;
                    }
                }
                const fallbackTarget = document.getElementById('practice-question-heading') ||
                                       document.getElementById('practice-question-card') ||
                                       document.getElementById('test-question-heading') ||
                                       document.getElementById('test-question-card') ||
                                       document.getElementById('result-card');
                if (fallbackTarget && typeof fallbackTarget.focus === 'function') {
                    fallbackTarget.focus();
                }
            });
        },

        scrollToTopOrActiveQuestion() {
            this.$nextTick(() => {
                const targetElement = document.getElementById('practice-question-card') || 
                                      document.getElementById('test-question-card') || 
                                      document.getElementById('result-card');
                
                if (targetElement) {
                    const rect = targetElement.getBoundingClientRect();
                    const absoluteTop = window.pageYOffset + rect.top;
                    const offset = 80;
                    window.scrollTo({
                        top: Math.max(0, absoluteTop - offset),
                        behavior: 'smooth'
                    });
                } else {
                    window.scrollTo({
                        top: 0,
                        behavior: 'smooth'
                    });
                }
                this.focusActiveQuestionTarget();
            });
        },

        // Study Mode: select section
        selectSection(index) {
            this.guardNavigation(() => {
                this.activeSectionIndex = index;
                this.studyIndex = 0;
                this.scrollToTopOrActiveQuestion();
            });
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
            localStorage.setItem('kynangsale:studyProgress', JSON.stringify(this.studyProgress));
            
            // Update sections progress
            this.updateSections();
        },

        // Study Mode: navigation
        prevStudyQuestion() {
            this.guardNavigation(() => {
                this.studyIndex = Math.max(0, this.studyIndex - 1);
                this.scrollToTopOrActiveQuestion();
            });
        },
        nextStudyQuestion() {
            this.guardNavigation(() => {
                const sec = this.sections[this.activeSectionIndex];
                if (sec && this.studyIndex < sec.questions.length - 1) {
                    this.studyIndex++;
                    this.scrollToTopOrActiveQuestion();
                }
            });
        },

        // Study Mode: Styling helpers
        getStudyOptionClass(option) {
            const q = this.currentStudyQuestion;
            if (!q) return '';
            const answeredKey = this.studyProgress[q.id];
            if (answeredKey === undefined) {
                return 'border-slate-100 bg-white hover:border-primary/30 hover:bg-slate-50';
            }
            if (option.key === q.correctAnswer) {
                return 'border-emerald-200 bg-emerald-50 text-emerald-900 border-2';
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
                return 'bg-slate-50 text-slate-400 group-hover:bg-primary group-hover:text-white';
            }
            if (option.key === q.correctAnswer) {
                return 'bg-emerald-600 text-white';
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
            
            let base = 'relative p-4 rounded-2xl cursor-pointer transition-all focus-visible:ring-2 focus-visible:ring-primary focus-visible:outline-none border-2 ';
            
            if (activeSectionIndex === idx) {
                // Active Card: Orange border, light orange tint
                base += 'border-primary bg-primary/5 ring-1 ring-primary/35 ';
            } else {
                // Learning Status Card
                if (sec.progress === 100) {
                    // Đã học xong: Emerald border, light emerald tint
                    base += 'border-emerald-200 bg-emerald-50/50 text-slate-800';
                } else if (idx === this.shouldContinueSectionIndex || sec.progress > 0) {
                    // Đang học / nên tiếp tục: Primary border (orange), white bg
                    base += 'border-primary/40 bg-white text-slate-800';
                } else {
                    // Chưa học: Gray border, white background
                    base += 'border-slate-100 bg-white text-slate-500 hover:border-slate-200';
                }
            }
            return base;
        },

        // Test Mode: Pick 60 random questions (8 from sec 1,3,5,7 and 7 from sec 2,4,6,8)
        pickTest() {
            const sec1 = this.shuffle(this.allQuestions.filter(q => q.sectionNo === 1)).slice(0, 8);
            const sec2 = this.shuffle(this.allQuestions.filter(q => q.sectionNo === 2)).slice(0, 7);
            const sec3 = this.shuffle(this.allQuestions.filter(q => q.sectionNo === 3)).slice(0, 8);
            const sec4 = this.shuffle(this.allQuestions.filter(q => q.sectionNo === 4)).slice(0, 7);
            const sec5 = this.shuffle(this.allQuestions.filter(q => q.sectionNo === 5)).slice(0, 8);
            const sec6 = this.shuffle(this.allQuestions.filter(q => q.sectionNo === 6)).slice(0, 7);
            const sec7 = this.shuffle(this.allQuestions.filter(q => q.sectionNo === 7)).slice(0, 8);
            const sec8 = this.shuffle(this.allQuestions.filter(q => q.sectionNo === 8)).slice(0, 7);
            
            const finalSet = [...sec1, ...sec2, ...sec3, ...sec4, ...sec5, ...sec6, ...sec7, ...sec8];
            return this.shuffle(finalSet);
        },

        // Test Mode: Start test
        startTest() {
            const name = this.learnerName.trim();
            const phone = this.phoneNumber.trim();

            if (!name || name.length > 100) {
                alert('Vui lòng nhập họ và tên học viên (từ 1 đến 100 ký tự) trên màn hình chính trước khi bắt đầu bài thi.');
                this.currentView = 'gate';
                return;
            }

            const phoneRegex = /^(03|05|07|08|09)\d{8}$/;
            if (!phone || !phoneRegex.test(phone)) {
                alert('Vui lòng nhập số điện thoại hợp lệ (10 chữ số, ví dụ 0901234567) trên màn hình chính trước khi bắt đầu bài thi.');
                this.currentView = 'gate';
                return;
            }

            // Save info
            localStorage.setItem('kynangsale:learnerName', name);
            localStorage.setItem('kynangsale:phoneNumber', phone);

            // Generate stable attemptId for this attempt
            if (typeof crypto !== 'undefined' && typeof crypto.randomUUID === 'function') {
                this.testAttemptId = crypto.randomUUID();
            } else {
                this.testAttemptId = 'attempt_kns_' + Date.now() + '_' + Math.random().toString(36).slice(2, 10);
            }
            
            this.resultSaved = false;
            this.certificateDownloadFailed = false;
            
            // Initialize test state
            this.testQuestions = this.pickTest();
            this.testAnswers = {};
            this.testCurrentIndex = 0;
            this.testTimer = 2700; // 45 minutes
            const now = new Date();
            this.testStartTime = now;
            this.testStartedAtISO = now.toISOString();
            this.resultSendingStatus = 'idle';
            this.resultErrorMessage = '';
            
            // Launch timer
            if (this.testTimerInterval) clearInterval(this.testTimerInterval);
            this.testTimerInterval = setInterval(() => {
                if (this.currentView === 'test') {
                    const elapsed = Math.floor((Date.now() - this.testStartTime.getTime()) / 1000);
                    this.testTimer = 2700 - elapsed;
                    if (this.testTimer <= 0) {
                        this.testTimer = 0;
                        clearInterval(this.testTimerInterval);
                        this.submitTest(true);
                    }
                }
            }, 1000);
            
            this.currentView = 'test';
            this.scrollToTopOrActiveQuestion();
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
            this.guardNavigation(() => {
                this.testCurrentIndex = Math.max(0, this.testCurrentIndex - 1);
                this.scrollToTopOrActiveQuestion();
            });
        },
        nextTestQuestion() {
            this.guardNavigation(() => {
                if (this.testCurrentIndex < 59) {
                    this.testCurrentIndex++;
                    this.scrollToTopOrActiveQuestion();
                } else {
                    this.showConfirmSubmit = true;
                }
            });
        },
        jumpToTestQuestion(index) {
            this.guardNavigation(() => {
                this.testCurrentIndex = index;
                this.scrollToTopOrActiveQuestion();
            });
        },

        // Helper to format seconds to mm:ss
        formatTime(sec) {
            const m = Math.floor(sec / 60);
            const s = sec % 60;
            return `${m.toString().padStart(2, '0')}:${s.toString().padStart(2, '0')}`;
        },

        // Test Mode: Submit test
        async submitTest(auto = false) {
            if (!auto) {
                const unansweredCount = 60 - Object.keys(this.testAnswers).length;
                if (unansweredCount > 0 && !confirm(`Bạn còn ${unansweredCount} câu chưa trả lời. Vẫn nộp bài?`)) {
                    this.showConfirmSubmit = false;
                    return;
                }
            }
            
            this.showConfirmSubmit = false;
            if (this.testTimerInterval) clearInterval(this.testTimerInterval);
            
            // Pre-calculate score
            let correct = 0;
            let unanswered = 0;
            const wrong = [];
            this.testQuestions.forEach((q, idx) => {
                const ans = this.testAnswers[q.id];
                if (ans === undefined || ans === null || ans === '') {
                    unanswered++;
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
            
            const threshold = 48; // Ngưỡng đạt 48/60 (80%)
            this.resultScore = correct;
            this.resultPassed = correct >= threshold;
            this.resultThreshold = threshold;
            this.resultUnansweredCount = unanswered;
            this.resultWrongQuestions = wrong;
            
            // Calculate time spent & timing contract fields
            const startMs = this.testStartTime ? this.testStartTime.getTime() : Date.now();
            let elapsedSecs = Math.max(1, Math.round((Date.now() - startMs) / 1000));
            
            let diffSecs = auto ? 2700 : elapsedSecs;
            if (diffSecs > 2700) {
                diffSecs = 2700;
                auto = true;
            }
            
            const submittedAtDate = new Date(startMs + diffSecs * 1000);
            const submittedAtISO = submittedAtDate.toISOString();
            const startedAtISO = new Date(startMs).toISOString();
            
            this.resultTimeSpent = this.formatTime(diffSecs);
            this.testStartedAtISO = startedAtISO;
            this.testSubmittedAtISO = submittedAtISO;
            this.testDurationSeconds = diffSecs;

            // Build initial payload with timing contract fields
            const initialPayload = {
                attemptId: this.testAttemptId,
                learnerName: this.learnerName.trim(),
                phoneNumber: this.phoneNumber.trim(),
                testAnswers: this.testAnswers,
                testQuestions: this.testQuestions.map(q => q.id),
                pageUrl: window.location.href,
                startedAt: this.testStartedAtISO,
                submittedAt: this.testSubmittedAtISO,
                durationSeconds: this.testDurationSeconds
            };
            
            try {
                localStorage.setItem('kynangsale:pendingQuizResult', JSON.stringify(initialPayload));
            } catch (e) {}
            
            // Save last result
            localStorage.setItem('kynangsale:lastResult', JSON.stringify({
                name: this.learnerName.trim(),
                phoneNumber: this.phoneNumber.trim(),
                correct,
                pass: this.resultPassed,
                threshold,
                at: new Date().toISOString()
            }));
            
            this.currentView = 'result';
            this.scrollToTopOrActiveQuestion();

            // Post result to server
            await this.postQuizResult(initialPayload);
        },

        async postQuizResult(overridePayload = null) {
            if (this.isSubmittingResult) return;
            this.isSubmittingResult = true;

            let payload = overridePayload;
            if (!payload) {
                try {
                    const pendingStr = localStorage.getItem('kynangsale:pendingQuizResult');
                    if (pendingStr) payload = JSON.parse(pendingStr);
                } catch (e) {}
            }

            if (!payload) {
                this.isSubmittingResult = false;
                return;
            }

            try {
                localStorage.setItem('kynangsale:pendingQuizResult', JSON.stringify(payload));
            } catch (e) {}

            try {
                const controller = new AbortController();
                const timer = setTimeout(() => controller.abort(), 10000);
                const res = await fetch('/api/kynangsale-quiz-result', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(payload),
                    signal: controller.signal
                });
                clearTimeout(timer);
                const data = await res.json();
                if (data.ok) {
                    if (typeof data.score === 'number') this.resultScore = data.score;
                    if (typeof data.passed === 'boolean') this.resultPassed = data.passed;
                    if (typeof data.threshold === 'number') this.resultThreshold = data.threshold;
                    this.resultSendingStatus = 'success';
                    this.resultSaved = true;
                    this.resultAutoRetryAttempt = 0;
                    try {
                        localStorage.removeItem('kynangsale:pendingQuizResult');
                    } catch (e) {}
                } else {
                    this.resultSendingStatus = 'error';
                    this.resultErrorMessage = data.error || 'Không thể lưu kết quả thi.';
                    this.scheduleClientAutoRetry(payload);
                }
            } catch (err) {
                this.resultSendingStatus = 'error';
                this.resultErrorMessage = 'Không thể kết nối đến máy chủ.';
                this.scheduleClientAutoRetry(payload);
            } finally {
                this.isSubmittingResult = false;
            }
        },

        scheduleClientAutoRetry(payload) {
            if (!this.resultAutoRetryAttempt) this.resultAutoRetryAttempt = 0;
            if (this.resultAutoRetryAttempt >= 3) return;
            this.resultAutoRetryAttempt++;
            const backoffMs = Math.min(5000 * Math.pow(2, this.resultAutoRetryAttempt - 1), 20000);
            setTimeout(() => {
                const rawPending = localStorage.getItem('kynangsale:pendingQuizResult');
                if (rawPending && this.resultSendingStatus === 'error') {
                    this.postQuizResult(payload).catch(() => {});
                }
            }, backoffMs);
        },

        openImageLightbox(src) {
            this.lightboxImage = src;
        },

        closeImageLightbox() {
            this.lightboxImage = null;
        },

        handleImageError(e) {
            if (e && e.target) {
                e.target.style.display = 'none';
                if (e.target.parentElement) {
                    e.target.parentElement.style.display = 'none';
                }
            }
        },

        // Study Mode: Enter study view
        startStudy() {
            const name = this.learnerName.trim();
            const phone = this.phoneNumber.trim();
            if (!name) {
                alert('Vui lòng nhập họ và tên học viên trước khi bắt đầu.');
                return;
            }
            
            // Save info
            localStorage.setItem('kynangsale:learnerName', name);
            if (phone) {
                localStorage.setItem('kynangsale:phoneNumber', phone);
            }
            
            this.currentView = 'study';
            this.scrollToTopOrActiveQuestion();
        },

        async submitFeedback(q, mode, options = {}) {
            const text = (this.feedbackTexts[q.id] || '').trim();
            if (!text || text.length > 1000) return;
            if (this.feedbackStatuses[q.id] === 'sending') return;

            this.feedbackStatuses[q.id] = 'sending';
            if (options.fromGuard) {
                this.guardErrorText = '';
            }

            const payload = {
                learnerName: this.learnerName,
                phoneNumber: this.phoneNumber,
                stableId: q.stableId || q.id,
                displayNumber: q.displayNumber || 0,
                sectionNo: q.sectionNo,
                sectionName: this.sections.find(s => s.no === q.sectionNo)?.title || q.sectionName || '',
                questionText: q.question,
                selectedAnswer: mode === 'test' ? this.testAnswers[q.id] : this.studyProgress[q.id],
                correctAnswer: q.correctAnswer,
                mode: mode,
                feedbackText: text,
                pageUrl: window.location.href,
                submittedAt: new Date().toISOString()
            };

            try {
                const res = await fetch('/api/kynangsale-question-feedback', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(payload)
                });
                const data = await res.json();
                if (data.ok) {
                    this.feedbackStatuses[q.id] = 'success';
                    this.feedbackTexts[q.id] = '';
                    this.showUnsentGuard = false;
                    this.guardErrorText = '';

                    if (this.successOverlayTimer) {
                        clearTimeout(this.successOverlayTimer);
                        this.successOverlayTimer = null;
                    }

                    this.showSuccessOverlay = true;
                    this.$nextTick(() => {
                        if (this.$refs.successOverlayBox) {
                            this.$refs.successOverlayBox.focus();
                        }
                    });

                    this.successOverlayTimer = setTimeout(() => {
                        this.showSuccessOverlay = false;
                        this.successOverlayTimer = null;
                        this.feedbackStatuses[q.id] = 'idle';

                        if (options.fromGuard && typeof this.pendingNavigationFn === 'function') {
                            const fn = this.pendingNavigationFn;
                            this.pendingNavigationFn = null;
                            this.previouslyFocusedElement = null;
                            fn();
                            this.focusActiveQuestionTarget();
                        } else {
                            this.$nextTick(() => {
                                const textareas = Array.from(document.querySelectorAll('textarea[data-feedback-qid]'));
                                const target = textareas.find(el => el.dataset.feedbackQid === q.id && el.offsetParent !== null && !el.disabled);
                                if (target && typeof target.focus === 'function') {
                                    target.focus();
                                } else {
                                    this.focusActiveQuestionTarget();
                                }
                            });
                        }
                    }, 800);
                } else {
                    this.feedbackStatuses[q.id] = 'error';
                    if (options.fromGuard) {
                        this.guardErrorText = 'Gửi thất bại, vui lòng thử lại';
                    }
                    setTimeout(() => {
                        if (this.feedbackStatuses[q.id] === 'error') this.feedbackStatuses[q.id] = 'idle';
                    }, 4000);
                }
            } catch (err) {
                this.feedbackStatuses[q.id] = 'error';
                if (options.fromGuard) {
                    this.guardErrorText = 'Gửi thất bại, vui lòng thử lại';
                }
                setTimeout(() => {
                    if (this.feedbackStatuses[q.id] === 'error') this.feedbackStatuses[q.id] = 'idle';
                }, 4000);
            }
        },

        adjustCertLayout(retryCount = 0) {
            this.$nextTick(() => {
                const nameEl = document.getElementById('certificate-name');
                const phoneEl = document.getElementById('certificate-phone') || document.getElementById('certificate-address');
                if (nameEl) {
                    // Retry layout computation if element has 0 width (not rendered yet)
                    if (nameEl.scrollWidth === 0 && retryCount < 10) {
                        setTimeout(() => this.adjustCertLayout(retryCount + 1), 50);
                        return;
                    }
                    nameEl.style.whiteSpace = 'nowrap';
                    nameEl.style.fontSize = '64px';
                    if (nameEl.scrollWidth > 955) {
                        nameEl.style.fontSize = '52px';
                    }
                    if (nameEl.scrollWidth > 955) {
                        nameEl.style.fontSize = '40px';
                    }
                    if (nameEl.scrollWidth > 955) {
                        nameEl.style.fontSize = '32px';
                        nameEl.style.whiteSpace = 'normal';
                    }
                }
                if (phoneEl) {
                    phoneEl.style.whiteSpace = 'nowrap';
                    phoneEl.style.fontSize = '22px';
                    if (phoneEl.scrollWidth > 955) {
                        phoneEl.style.fontSize = '20px';
                    }
                    if (phoneEl.scrollWidth > 955) {
                        phoneEl.style.fontSize = '18px';
                        phoneEl.style.whiteSpace = 'normal';
                    }
                }
            });
        },

        async downloadCertificate() {
            if (this.downloadingCertificate) return;
            this.downloadingCertificate = true;
            this.certificateDownloadFailed = false;
            
            try {
                if (typeof html2canvas === 'undefined') {
                    throw new Error('html2canvas is not loaded');
                }
                
                const element = document.getElementById('certificate-print-area');
                const scaleWrapper = document.getElementById('certificate-scale-wrapper');
                if (!element || !scaleWrapper) {
                    throw new Error('Certificate elements not found');
                }
                
                // Save original styles to disable scale transform temporarily during capture
                const originalTransform = scaleWrapper.style.transform;
                const originalMarginBottom = scaleWrapper.style.marginBottom;
                
                scaleWrapper.style.transform = 'none';
                scaleWrapper.style.marginBottom = '0px';
                
                // Force browser reflow to settle layout at 1:1 scale
                void scaleWrapper.offsetHeight;
                
                const canvas = await html2canvas(element, {
                    scale: 2,
                    useCORS: true,
                    backgroundColor: "#ffffff",
                    logging: false
                });
                
                // Restore scale transform immediately
                scaleWrapper.style.transform = originalTransform;
                scaleWrapper.style.marginBottom = originalMarginBottom;
                
                const link = document.createElement('a');
                link.download = `chung-nhan-sale-${this.testAttemptId}.png`;
                link.href = canvas.toDataURL('image/png');
                link.click();
            } catch (err) {
                console.error('Error generating certificate image:', err);
                this.certificateDownloadFailed = true;
                alert('Có lỗi xảy ra khi tạo ảnh chứng nhận. Kết quả thi đã được lưu thành công trên hệ thống. Chúng tôi sẽ chuyển sang chế độ In dự phòng để thay thế.');
                window.print();
            } finally {
                this.downloadingCertificate = false;
            }
        }
    };
}

if (typeof module !== 'undefined' && module.exports) {
    module.exports = app;
}
