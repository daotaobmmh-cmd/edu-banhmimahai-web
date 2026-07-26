(() => {
  const prompts = Array.isArray(window.PROMPTS) ? window.PROMPTS : [];
  const config = window.SITE_CONFIG || {};
  const grid = document.querySelector('#prompt-grid');
  const search = document.querySelector('#search-input');
  const emptyState = document.querySelector('#empty-state');
  const visibleCount = document.querySelector('#visible-count');
  const categoryNav = document.querySelector('#category-nav');
  const mobileCategoryNav = document.querySelector('#mobile-category-nav');
  const toast = document.querySelector('#toast');
  let activeCategory = 'Tất cả';
  let query = '';

  const categoryOrder = ['Tất cả', 'Hệ thống', 'Lõi', 'Tình huống'];
  const normalize = (value = '') => value.toLocaleLowerCase('vi').normalize('NFD').replace(/[\u0300-\u036f]/g, '');
  const escapeHtml = (value = '') => value.replace(/[&<>'"]/g, char => ({'&':'&amp;','<':'&lt;','>':'&gt;',"'":'&#39;','"':'&quot;'}[char]));

  function showToast(message) {
    toast.textContent = message;
    toast.classList.add('show');
    clearTimeout(showToast.timer);
    showToast.timer = setTimeout(() => toast.classList.remove('show'), 1800);
  }

  function countFor(category) {
    return category === 'Tất cả' ? prompts.length : prompts.filter(p => p.category === category).length;
  }

  function filterButton(category) {
    const pressed = activeCategory === category;
    return `<button class="filter-button" type="button" data-category="${category}" aria-pressed="${pressed}"><span>${category}</span><span class="filter-count">${countFor(category)}</span></button>`;
  }

  function renderFilters() {
    const html = categoryOrder.map(filterButton).join('');
    categoryNav.innerHTML = html;
    mobileCategoryNav.innerHTML = html;
    document.querySelectorAll('[data-category]').forEach(button => {
      button.addEventListener('click', () => {
        activeCategory = button.dataset.category;
        renderFilters();
        applyFilters();
      });
    });
  }

  function cardTemplate(prompt) {
    const notWhen = prompt.notWhen ? `<p class="not-when"><strong>Không dùng khi:</strong> ${escapeHtml(prompt.notWhen)}</p>` : '';
    const searchable = normalize([prompt.id, prompt.title, prompt.category, prompt.usedWhen, prompt.input, prompt.prompt].join(' '));
    return `<article class="prompt-card reveal" data-id="${escapeHtml(prompt.id)}" data-category="${escapeHtml(prompt.category)}" data-search="${escapeHtml(searchable)}">
      <div class="card-body">
        <div class="card-topline"><span class="prompt-id">PROMPT ${escapeHtml(prompt.id)}</span><span class="category-badge">${escapeHtml(prompt.category)}</span></div>
        <h2 class="prompt-title">${escapeHtml(prompt.title)}</h2>
        <div class="info-block"><span class="info-label">Dùng khi</span><p>${escapeHtml(prompt.usedWhen)}</p></div>
        <div class="info-block"><span class="info-label">Input</span><p>${escapeHtml(prompt.input)}</p>${notWhen}</div>
      </div>
      <div class="prompt-panel">
        <div class="prompt-toolbar"><strong>Prompt để sao chép</strong><div class="tool-actions"><button class="tool-button expand-button" type="button" aria-expanded="false">Mở rộng</button><button class="tool-button primary copy-button" type="button">Sao chép</button></div></div>
        <pre class="prompt-code"><code>${escapeHtml(prompt.prompt)}</code></pre>
      </div>
      <form class="feedback" data-feedback-form>
        <label for="feedback-${escapeHtml(prompt.id)}">Góp ý để prompt tốt hơn</label>
        <textarea id="feedback-${escapeHtml(prompt.id)}" name="feedback" maxlength="1500" placeholder="Ví dụ: thiếu tình huống…, output nên ngắn hơn…"></textarea>
        <div class="feedback-row"><span class="feedback-status" aria-live="polite"></span><button class="submit-feedback" type="submit">Gửi góp ý</button></div>
      </form>
    </article>`;
  }

  function renderCards() {
    grid.innerHTML = prompts.map(cardTemplate).join('');
    grid.querySelectorAll('.prompt-card').forEach(card => {
      const prompt = prompts.find(item => item.id === card.dataset.id);
      card.querySelector('.copy-button').addEventListener('click', async event => {
        try {
          await navigator.clipboard.writeText(prompt.prompt);
          const button = event.currentTarget;
          const previous = button.textContent;
          button.textContent = 'Đã chép';
          showToast(`Đã sao chép Prompt ${prompt.id}`);
          setTimeout(() => button.textContent = previous, 1400);
        } catch {
          const range = document.createRange();
          range.selectNodeContents(card.querySelector('.prompt-code'));
          const selection = window.getSelection();
          selection.removeAllRanges();
          selection.addRange(range);
          showToast('Đã chọn prompt — nhấn Ctrl/Cmd + C');
        }
      });
      card.querySelector('.expand-button').addEventListener('click', event => {
        const expanded = card.classList.toggle('expanded');
        event.currentTarget.textContent = expanded ? 'Thu gọn' : 'Mở rộng';
        event.currentTarget.setAttribute('aria-expanded', String(expanded));
      });
      card.querySelector('[data-feedback-form]').addEventListener('submit', event => submitFeedback(event, prompt));
    });

    if ('IntersectionObserver' in window && !matchMedia('(prefers-reduced-motion: reduce)').matches) {
      const observer = new IntersectionObserver(entries => entries.forEach(entry => {
        if (entry.isIntersecting) { entry.target.classList.add('visible'); observer.unobserve(entry.target); }
      }), { threshold: .08 });
      document.querySelectorAll('.reveal').forEach(card => observer.observe(card));
    } else {
      document.querySelectorAll('.reveal').forEach(card => card.classList.add('visible'));
    }
  }

  async function submitFeedback(event, prompt) {
    event.preventDefault();
    const form = event.currentTarget;
    const textarea = form.elements.feedback;
    const status = form.querySelector('.feedback-status');
    const button = form.querySelector('.submit-feedback');
    const feedback = textarea.value.trim();
    if (feedback.length < 5) {
      status.textContent = 'Viết ít nhất 5 ký tự.';
      textarea.focus();
      return;
    }
    button.disabled = true;
    status.textContent = 'Đang gửi…';
    const payload = {
      promptId: prompt.id,
      promptTitle: prompt.title,
      category: prompt.category,
      feedback,
      source: config.sourceUrl || location.href
    };
    try {
      if (!config.feedbackEnabled || !config.feedbackEndpoint) throw new Error('NOT_CONFIGURED');
      const response = await fetch(config.feedbackEndpoint, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });
      if (!response.ok) throw new Error(`HTTP_${response.status}`);
      textarea.value = '';
      status.textContent = 'Đã gửi. Cảm ơn bạn!';
      showToast('Đã gửi góp ý');
    } catch (error) {
      const drafts = JSON.parse(localStorage.getItem('prompt-feedback-drafts') || '[]');
      drafts.push({ ...payload, savedAt: new Date().toISOString() });
      localStorage.setItem('prompt-feedback-drafts', JSON.stringify(drafts.slice(-50)));
      status.textContent = 'Chưa gửi được; đã lưu nháp trên máy.';
    } finally {
      button.disabled = false;
    }
  }

  function applyFilters() {
    const cards = [...document.querySelectorAll('.prompt-card')];
    let count = 0;
    cards.forEach(card => {
      const categoryMatch = activeCategory === 'Tất cả' || card.dataset.category === activeCategory;
      const queryMatch = !query || card.dataset.search.includes(normalize(query));
      const visible = categoryMatch && queryMatch;
      card.classList.toggle('is-hidden', !visible);
      if (visible) count += 1;
    });
    visibleCount.textContent = count;
    emptyState.hidden = count > 0;
  }

  search.addEventListener('input', event => { query = event.target.value.trim(); applyFilters(); });
  renderFilters();
  renderCards();
  applyFilters();
})();
