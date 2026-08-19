function app() {
    const DATASET_VERSION = '1f1864a2580138c0d22dd3677df5f38e3bf904234b1e5fcf7c31bb999203cc73';
    return {
        // App State
        currentView: 'gate', // 'gate', 'study', 'test', 'result'
        showGuide: false,
        showConfirmSubmit: false,
        
        // Learner State
        learnerName: '',
        learnerDept: '',
        unitAllowlist: [
            "Ban giám đốc",
            "Phòng Kinh doanh",
            "Bộ phận Phát triển Khách hàng hiện hữu",
            "Phòng Marketing",
            "Bộ phận Phát triển nhượng quyền",
            "Phòng Kho vận",
            "Phòng Hành chính - Nhân sự",
            "Phòng Tài chính - Kế toán",
            "Ban Quản lý Quy trình",
            "University"
        ],
        
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
        testAttemptId: '',
        
        // Result State
        resultScore: 0,
        resultPassed: false,
        resultThreshold: 25,
        resultTimeSpent: '',
        resultWrongQuestions: [], // questions answered incorrectly in test
        resultUnansweredCount: 0,
        resultSendingStatus: 'idle', // 'idle', 'sending', 'success', 'error'
        resultErrorMessage: '',
        isSubmittingResult: false,
        
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
        certificateDownloadFailed: false,
        
        // Init
        init() {
            // Load questions from window.HOINHAP_QUESTIONS
            this.allQuestions = window.HOINHAP_QUESTIONS || [];
            
            // Load learner info from localStorage
            this.learnerName = localStorage.getItem('hoinhap:learnerName') || '';
            const savedDept = localStorage.getItem('hoinhap:learnerDept') || '';
            this.learnerDept = this.unitAllowlist.includes(savedDept) ? savedDept : '';
            
            // Check dataset version in localStorage
            const savedVersion = localStorage.getItem('hoinhap:datasetVersion');
            if (savedVersion !== DATASET_VERSION) {
                localStorage.removeItem('hoinhap:studyProgress');
                localStorage.removeItem('hoinhap:lastResult');
                localStorage.setItem('hoinhap:datasetVersion', DATASET_VERSION);
                this.studyProgress = {};
            } else {
                // Load study progress from localStorage
                try {
                    const savedProgress = localStorage.getItem('hoinhap:studyProgress');
                    if (savedProgress) {
                        this.studyProgress = JSON.parse(savedProgress);
                    }
                } catch (e) {
                    console.error('Failed to parse study progress', e);
                }
            }
            
            // Initialize sections list
            this.updateSections();
            
            // Auto-select first section if available
            if (this.sections.length > 0) {
                this.activeSectionIndex = 0;
            }

            // Auto-resend pending quiz result if browser closed/refreshed after error
            try {
                const rawPending = localStorage.getItem('hoinhap:pendingQuizResult');
                if (rawPending) {
                    const pendingPayload = JSON.parse(rawPending);
                    if (pendingPayload && pendingPayload.attemptId) {
                        this.postQuizResult(pendingPayload).catch(() => {});
                    }
                }
            } catch (e) {}
            
            // Set initialization flag and hide fallback UI
            window.alpineInitialized = true;
            document.documentElement.classList.add('alpine-ready');
            const fallbackEl = document.getElementById('app-fallback');
            if (fallbackEl) {
                fallbackEl.style.display = 'none';
            }
            
            // Watch changes to adjust certificate text sizes
            this.$watch('learnerName', () => this.adjustCertLayout());
            this.$watch('learnerDept', () => this.adjustCertLayout());
            this.$watch('currentView', (view) => {
                if (view === 'result') {
                    const delays = [50, 150, 300, 600, 1000, 2000];
                    delays.forEach(delay => {
                        setTimeout(() => this.adjustCertLayout(), delay);
                    });
                    if (document.fonts) {
                        document.fonts.ready.then(() => {
                            this.adjustCertLayout();
                        });
                    }
                }
            });
        },

        // Helper: Shuffle array
        shuffle(arr) {
            return [...arr].sort(() => Math.random() - 0.5);
        },

        // Update Sections list progress
        updateSections() {
            const canonicalTitles = [
                "Hành trình, sản phẩm và địa điểm Má Hải",
                "Hệ giá trị và tư duy làm việc",
                "Hợp đồng lao động và kỷ luật",
                "Nghỉ phép, chấm công và quy trình HR",
                "Phúc lợi, đánh giá và phát triển",
                "Tác phong và giao tiếp khách hàng",
                "Văn hóa nội bộ và tinh thần đồng đội",
                "12 Chữ vàng và phục vụ khách hàng",
                "12 Trái cấm, bảo mật và tài sản",
                "Công cụ, sơ đồ tổ chức và báo cáo",
                "An toàn, PCCC, vệ sinh và môi trường",
                "Má Hải Ways — 5 nguyên lý nền tảng",
                "Làm chủ công việc và dám nhận thử thách",
                "Tập trung, thời gian và nguồn lực",
                "Biết ơn và yêu mến",
                "Làm vì người khác, 5 node và đại sứ thương hiệu",
                "Học hỏi, cải tiến và tiến bộ mỗi ngày",
                "Làm chuẩn, làm thật và kỷ luật vận hành"
            ];
            
            const map = new Map();
            this.allQuestions.forEach(q => {
                if (!map.has(q.sectionNo)) {
                    map.set(q.sectionNo, {
                        no: q.sectionNo,
                        title: canonicalTitles[q.sectionNo - 1] || q.sectionName,
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

        scrollToTopOrActiveQuestion() {
            this.$nextTick(() => {
                requestAnimationFrame(() => {
                    if (this.currentView === 'result' || this.currentView === 'gate') {
                        window.scrollTo({ top: 0, behavior: 'smooth' });
                        return;
                    }

                    let targetEl = null;
                    if (this.currentView === 'study') {
                        targetEl = this.$refs.practiceQuestionCard || document.getElementById('practice-question-card') || this.$refs.practiceQuestionHeading || document.getElementById('practice-question-heading');
                    } else if (this.currentView === 'test') {
                        targetEl = this.$refs.testQuestionCard || document.getElementById('test-question-card') || this.$refs.testQuestionHeading || document.getElementById('test-question-heading');
                    }
                    
                    if (targetEl && typeof targetEl.getBoundingClientRect === 'function') {
                        const rect = targetEl.getBoundingClientRect();
                        const isMobile = window.innerWidth < 640;
                        const headerOffset = isMobile ? 78 : 94;
                        const elementPosition = rect.top + window.pageYOffset;
                        const offsetPosition = Math.max(0, elementPosition - headerOffset);
                        window.scrollTo({
                            top: offsetPosition,
                            behavior: 'smooth'
                        });
                    } else {
                        window.scrollTo({ top: 0, behavior: 'smooth' });
                    }
                });
            });
        },

        focusActiveQuestionTarget() {
            this.scrollToTopOrActiveQuestion();
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
            localStorage.setItem('hoinhap:studyProgress', JSON.stringify(this.studyProgress));
            
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

        // Test Mode: Pick 30 random questions (10 from group 1: HN 1-54, 10 from group 2: HN 55-106, 10 from MHW)
        pickTest() {
            const q13 = this.allQuestions.filter(q => q.stableId && q.stableId.startsWith('HN-') && parseInt(q.stableId.split('-')[1]) <= 54 && q.active !== false);
            const q14 = this.allQuestions.filter(q => q.stableId && q.stableId.startsWith('HN-') && parseInt(q.stableId.split('-')[1]) > 54 && q.active !== false);
            const q65 = this.allQuestions.filter(q => q.stableId && q.stableId.startsWith('MHW-') && q.active !== false);
            
            const selected13 = this.shuffle(q13).slice(0, 10);
            const selected14 = this.shuffle(q14).slice(0, 10);
            const selected65 = this.shuffle(q65).slice(0, 10);
            
            let finalSet = [...selected13, ...selected14, ...selected65];
            
            return this.shuffle(finalSet.map(q => ({
                ...q,
                options: q.options // Keep options in A/B/C/D order
            })));
        },

        // Test Mode: Start test
        startTest() {
            const name = this.learnerName.trim();
            if (!name || name.length > 100) {
                alert('Vui lòng nhập họ tên (từ 1 đến 100 ký tự) trên màn hình chính trước khi bắt đầu bài thi.');
                this.currentView = 'gate';
                return;
            }

            if (!this.learnerDept || !this.unitAllowlist.includes(this.learnerDept)) {
                alert('Vui lòng chọn Đơn vị trên màn hình chính trước khi bắt đầu bài thi.');
                this.currentView = 'gate';
                return;
            }

            // Save info
            localStorage.setItem('hoinhap:learnerName', name);
            localStorage.setItem('hoinhap:learnerDept', this.learnerDept);

            // Generate stable attemptId for this attempt
            if (typeof crypto !== 'undefined' && typeof crypto.randomUUID === 'function') {
                this.testAttemptId = crypto.randomUUID();
            } else {
                this.testAttemptId = 'attempt_' + Date.now() + '_' + Math.random().toString(36).slice(2, 10) + '_' + Math.random().toString(36).slice(2, 10);
            }
            
            // Initialize test state
            this.testQuestions = this.pickTest();
            this.testAnswers = {};
            this.testCurrentIndex = 0;
            this.testTimer = 1800; // 30 minutes
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
                    this.testTimer = 1800 - elapsed;
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
                if (this.testCurrentIndex < 29) {
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
                const unansweredCount = 30 - Object.keys(this.testAnswers).length;
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
            
            const threshold = (this.learnerDept === 'Phòng Kho vận') ? 20 : 25;
            this.resultScore = correct;
            this.resultPassed = correct >= threshold;
            this.resultThreshold = threshold;
            this.resultUnansweredCount = unanswered;
            this.resultWrongQuestions = wrong;
            
            // Calculate time spent & timing contract fields (Fix for browser timer throttling on auto-submit)
            const startMs = this.testStartTime ? this.testStartTime.getTime() : Date.now();
            let elapsedSecs = Math.max(1, Math.round((Date.now() - startMs) / 1000));
            
            let diffSecs = auto ? 1800 : elapsedSecs;
            if (diffSecs > 1800) {
                diffSecs = 1800;
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
                unit: this.learnerDept,
                testAnswers: this.testAnswers,
                testQuestions: this.testQuestions.map(q => q.id),
                pageUrl: window.location.href,
                startedAt: this.testStartedAtISO,
                submittedAt: this.testSubmittedAtISO,
                durationSeconds: this.testDurationSeconds
            };
            
            try {
                localStorage.setItem('hoinhap:pendingQuizResult', JSON.stringify(initialPayload));
            } catch (e) {}
            
            // Save last result
            localStorage.setItem('hoinhap:lastResult', JSON.stringify({
                name: this.learnerName.trim(),
                dept: this.learnerDept,
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
                    const pendingStr = localStorage.getItem('hoinhap:pendingQuizResult');
                    if (pendingStr) payload = JSON.parse(pendingStr);
                } catch (e) {}
            }

            if (!payload) {
                this.isSubmittingResult = false;
                return; // Do NOT generate dummy payload if no pending/override payload exists
            }

            try {
                localStorage.setItem('hoinhap:pendingQuizResult', JSON.stringify(payload));
            } catch (e) {}

            try {
                const controller = new AbortController();
                const timer = setTimeout(() => controller.abort(), 10000);
                const res = await fetch('/api/quiz-result', {
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
                    this.resultAutoRetryAttempt = 0;
                    try {
                        localStorage.removeItem('hoinhap:pendingQuizResult');
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
            if (this.resultAutoRetryAttempt >= 3) return; // Limit background auto-retries while tab open to 3
            this.resultAutoRetryAttempt++;
            const backoffMs = Math.min(5000 * Math.pow(2, this.resultAutoRetryAttempt - 1), 20000);
            setTimeout(() => {
                const rawPending = localStorage.getItem('hoinhap:pendingQuizResult');
                if (rawPending && this.resultSendingStatus === 'error') {
                    this.postQuizResult(payload).catch(() => {});
                }
            }, backoffMs);
        },

        // Study Mode: Enter study view
        startStudy() {
            const name = this.learnerName.trim();
            if (!name) {
                alert('Vui lòng nhập họ tên trước khi bắt đầu.');
                return;
            }
            
            // Save info
            localStorage.setItem('hoinhap:learnerName', name);
            if (this.learnerDept) {
                localStorage.setItem('hoinhap:learnerDept', this.learnerDept);
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
                stableId: q.stableId || q.id,
                displayNumber: q.displayNumber || 0,
                sectionNo: q.sectionNo,
                sectionName: this.sections.find(s => s.no === q.sectionNo)?.title || '',
                questionText: q.question,
                selectedAnswer: mode === 'test' ? this.testAnswers[q.id] : this.studyProgress[q.id],
                correctAnswer: q.correctAnswer,
                mode: mode,
                feedbackText: text,
                pageUrl: window.location.href,
                submittedAt: new Date().toISOString()
            };

            try {
                const res = await fetch('/api/question-feedback', {
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

                    // Trigger Polished Success Moment Overlay (~800ms) with timer safety
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

                        // If submitted from navigation guard, complete pending navigation after success moment
                        if (options.fromGuard && typeof this.pendingNavigationFn === 'function') {
                            const fn = this.pendingNavigationFn;
                            this.pendingNavigationFn = null;
                            this.previouslyFocusedElement = null;
                            fn();
                            this.focusActiveQuestionTarget();
                        } else {
                            // Direct submission: return focus to exact matching textarea for this question
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
                const addrEl = document.getElementById('certificate-address');
                if (nameEl) {
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
                if (addrEl) {
                    addrEl.style.whiteSpace = 'nowrap';
                    addrEl.style.fontSize = '22px';
                    if (addrEl.scrollWidth > 955) {
                        addrEl.style.fontSize = '20px';
                    }
                    if (addrEl.scrollWidth > 955) {
                        addrEl.style.fontSize = '18px';
                        addrEl.style.whiteSpace = 'normal';
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
                
                const originalTransform = scaleWrapper.style.transform;
                const originalMarginBottom = scaleWrapper.style.marginBottom;
                
                scaleWrapper.style.transform = 'none';
                scaleWrapper.style.marginBottom = '0px';
                
                void scaleWrapper.offsetHeight;
                
                const canvas = await html2canvas(element, {
                    scale: 2,
                    useCORS: true,
                    backgroundColor: "#ffffff",
                    logging: false
                });
                
                scaleWrapper.style.transform = originalTransform;
                scaleWrapper.style.marginBottom = originalMarginBottom;
                
                const link = document.createElement('a');
                link.download = `chung-nhan-${this.testAttemptId}.png`;
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
    }
}
