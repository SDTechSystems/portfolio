// Step-by-step intake form that submits to the linked Google Form.
const root = document.querySelector<HTMLElement>('[data-intake]');
if (root) initIntake(root);

function initIntake(root: HTMLElement) {
  const form = root.querySelector<HTMLFormElement>('[data-intake-form]')!;
  const steps = [...form.querySelectorAll<HTMLElement>('.intake-step')];
  const questions = steps.filter(s => s.dataset.entry);
  const total = Number(root.dataset.total);
  const slug = root.dataset.slug!;
  const draftKey = `sd-intake-${slug}-v2`;
  const legacyKey = `sd-intake-${slug}-v1`;
  const bar = document.querySelector<HTMLElement>('.intake-progress')!;
  const counter = document.querySelector<HTMLElement>('[data-counter]');
  const nav = root.querySelector<HTMLElement>('[data-nav]')!;
  const reduced = () => matchMedia('(prefers-reduced-motion: reduce)').matches || document.documentElement.hasAttribute('data-motion');
  let current = 0;
  let busy = false;
  let sent = false;
  let resumeAt = 1; // first question, or where a saved draft left off

  document.documentElement.classList.add('intake-js');

  // ----- Draft (per device, optional) -----
  // Answers and the question the person was on, so an accidental reload resumes exactly there.
  type Draft = { answers: Record<string, string[]>; step: number; at: number };
  const readDraft = (): Draft | null => {
    try {
      const raw = localStorage.getItem(draftKey);
      if (raw) {
        const d = JSON.parse(raw);
        if (d && typeof d === 'object' && d.answers && typeof d.answers === 'object') return { answers: d.answers, step: Number(d.step) || 0, at: Number(d.at) || 0 };
      }
      // Drafts saved by the first version only held the answers.
      const old = localStorage.getItem(legacyKey);
      if (old) { const answers = JSON.parse(old); if (answers && typeof answers === 'object') return { answers, step: 0, at: 0 }; }
    } catch {}
    return null;
  };
  const saveDraft = () => {
    if (sent) return;
    const answers = collect();
    if (!Object.keys(answers).length && current === 0) return;
    const step = steps[current]?.dataset.step === 'done' ? 0 : current;
    try { localStorage.setItem(draftKey, JSON.stringify({ answers, step, at: Date.now() })); localStorage.removeItem(legacyKey); } catch {}
  };
  const clearDraft = () => { try { localStorage.removeItem(draftKey); localStorage.removeItem(legacyKey); } catch {} };

  function collect(): Record<string, string[]> {
    const data: Record<string, string[]> = {};
    new FormData(form).forEach((value, key) => {
      const text = String(value).trim();
      if (!text) return;
      (data[key] ||= []).push(text);
    });
    return data;
  }

  function restore(draft: Record<string, string[]>) {
    Object.entries(draft).forEach(([name, values]) => {
      form.querySelectorAll<HTMLInputElement | HTMLTextAreaElement>(`[name="${CSS.escape(name)}"]`).forEach(el => {
        if (el instanceof HTMLInputElement && (el.type === 'radio' || el.type === 'checkbox')) el.checked = values.includes(el.value);
        else el.value = values[0] || '';
      });
    });
    questions.forEach(syncChoices);
  }

  const draft = readDraft();
  const hasDraft = !!draft && Object.keys(draft.answers).length > 0;
  if (hasDraft) restore(draft!.answers);

  function resetAll() {
    clearDraft(); form.reset();
    form.querySelectorAll<HTMLInputElement>('[data-other-text]').forEach(i => { i.hidden = true; });
    questions.forEach(step => { syncChoices(step); showError(step, ''); });
    root.querySelector<HTMLElement>('[data-draft-notice]')!.hidden = true;
    root.querySelector<HTMLElement>('[data-clear-draft]')!.hidden = true;
    root.querySelectorAll('[data-start-label]').forEach(l => { l.textContent = 'Comenzar'; });
    resumeAt = 1;
  }

  // Erasing answers takes two taps, so nobody loses their progress by accident.
  function confirmReset(button: HTMLButtonElement, onReset: () => void) {
    if (button.dataset.armed) { onReset(); return; }
    button.dataset.armed = 'true';
    const label = button.textContent;
    button.textContent = '¿Seguro? Toca de nuevo para borrar todo';
    button.classList.add('is-armed');
    setTimeout(() => { if (button.isConnected) { delete button.dataset.armed; button.textContent = label; button.classList.remove('is-armed'); } }, 4000);
  }

  // ----- Helpers per question -----
  const fieldsOf = (step: HTMLElement) => [...step.querySelectorAll<HTMLInputElement | HTMLTextAreaElement>('input, textarea')];
  function answerOf(step: HTMLElement): string[] {
    const kind = step.dataset.kind;
    if (kind === 'text' || kind === 'long') {
      const v = step.querySelector<HTMLInputElement | HTMLTextAreaElement>('.intake-input')!.value.trim();
      return v ? [v] : [];
    }
    const picked = [...step.querySelectorAll<HTMLInputElement>('.intake-choice input:checked')];
    return picked.map(i => i.dataset.other !== undefined ? (step.querySelector<HTMLInputElement>('[data-other-text]')!.value.trim() || 'Otro') : i.value);
  }

  function syncChoices(step: HTMLElement) {
    const otherBox = step.querySelector<HTMLInputElement>('[data-other]');
    const otherText = step.querySelector<HTMLInputElement>('[data-other-text]');
    if (otherBox && otherText) {
      const show = otherBox.checked;
      if (otherText.hidden === show) {
        otherText.hidden = !show;
        if (show) { otherText.classList.add('is-arriving'); if (!busy) otherText.focus({ preventScroll: true }); }
      }
    }
    const max = Number(step.dataset.max) || 0;
    if (max) {
      const boxes = [...step.querySelectorAll<HTMLInputElement>('.intake-choice input')];
      const count = boxes.filter(b => b.checked).length;
      boxes.forEach(b => { b.disabled = !b.checked && count >= max; b.closest('.intake-choice')!.classList.toggle('is-locked', b.disabled); });
      const picked = step.querySelector('[data-picked]');
      if (picked) picked.textContent = String(count);
    }
    step.classList.toggle('is-answered', answerOf(step).length > 0);
  }

  function validate(step: HTMLElement): string {
    if (!step.dataset.entry) return '';
    const answer = answerOf(step);
    if (step.dataset.required && !answer.length) return step.dataset.kind === 'checkbox' || step.dataset.kind === 'radio' ? 'Elige al menos una opción para continuar.' : 'Esta respuesta es necesaria para preparar tu propuesta.';
    if (step.dataset.input === 'tel' && answer.length && answer[0].replace(/\D/g, '').length < 7) return 'Revisa el número: escríbelo con indicativo, por ejemplo 57 300 000 0000.';
    const other = step.querySelector<HTMLInputElement>('[data-other]');
    if (other?.checked && !step.querySelector<HTMLInputElement>('[data-other-text]')!.value.trim()) return 'Cuéntanos cuál es la otra opción.';
    return '';
  }

  function showError(step: HTMLElement, message: string) {
    const box = step.querySelector<HTMLElement>('[data-error]');
    if (!box) return;
    box.textContent = message;
    step.classList.toggle('has-error', !!message);
    if (message && !reduced()) step.querySelector('.intake-field')?.animate(
      [{ transform: 'translateX(0)' }, { transform: 'translateX(-9px)' }, { transform: 'translateX(7px)' }, { transform: 'translateX(-4px)' }, { transform: 'translateX(0)' }],
      { duration: 380, easing: 'ease-out' });
  }

  // ----- Progress -----
  function updateProgress() {
    const step = steps[current];
    const index = step.dataset.entry ? questions.indexOf(step) + 1 : step.dataset.step === 'intro' ? 0 : total;
    const ratio = step.dataset.step === 'done' ? 1 : index / (total + 1);
    bar.style.setProperty('--progress', String(ratio));
    bar.setAttribute('aria-valuenow', String(Math.min(index, total)));
    root.style.setProperty('--progress', String(ratio));
    if (counter) counter.textContent = String(Math.min(index, total)).padStart(2, '0');
    nav.hidden = !step.dataset.entry;
  }

  // ----- Transitions -----
  async function go(to: number, direction: 1 | -1) {
    if (busy || to < 0 || to >= steps.length || to === current) return;
    busy = true;
    const from = steps[current], next = steps[to];
    const sectionChanged = from.querySelector('[data-section-title]')?.getAttribute('data-section-title') !== next.querySelector('[data-section-title]')?.getAttribute('data-section-title');
    if (!reduced()) {
      // A visual copy of the old question fades out on top while the new one is already live,
      // so keystrokes always land in the current question.
      const ghost = from.cloneNode(true) as HTMLElement;
      const box = from.getBoundingClientRect(), host = form.getBoundingClientRect();
      // Drop names first so the copy never joins the real radio groups or the submitted data.
      ghost.querySelectorAll('input, textarea, button').forEach(el => { el.setAttribute('tabindex', '-1'); el.removeAttribute('name'); });
      const live = fieldsOf(from), copies = fieldsOf(ghost);
      copies.forEach((el, i) => { el.value = live[i].value; if (el instanceof HTMLInputElement) el.checked = (live[i] as HTMLInputElement).checked; });
      ghost.removeAttribute('data-step'); ghost.removeAttribute('data-entry');
      ghost.querySelectorAll('[id]').forEach(el => el.removeAttribute('id'));
      ghost.setAttribute('aria-hidden', 'true'); ghost.classList.remove('is-active', 'section-enter'); ghost.classList.add('intake-ghost');
      Object.assign(ghost.style, { position: 'absolute', left: `${box.left - host.left}px`, top: `${box.top - host.top}px`, width: `${box.width}px`, pointerEvents: 'none' });
      form.append(ghost);
      ghost.animate([
        { opacity: 1, transform: 'translateY(0)', filter: 'blur(0)' },
        { opacity: 0, transform: `translateY(${-36 * direction}px)`, filter: 'blur(6px)' },
      ], { duration: 260, easing: 'cubic-bezier(.4,0,.6,1)', fill: 'forwards' });
      setTimeout(() => ghost.remove(), 300);
    }
    from.hidden = true; from.classList.remove('is-active');
    next.hidden = false; next.classList.add('is-active');
    next.classList.toggle('section-enter', sectionChanged || next.dataset.step === 'review');
    current = to;
    updateProgress();
    if (next.dataset.step === 'review') buildSummary();
    if (!reduced()) {
      next.animate([
        { opacity: 0, transform: `translateY(${44 * direction}px)`, filter: 'blur(6px)' },
        { opacity: 1, transform: 'translateY(0)', filter: 'blur(0)' },
      ], { duration: 520, delay: 120, easing: 'cubic-bezier(.16,1,.3,1)', fill: 'backwards' });
    }
    window.scrollTo({ top: 0, behavior: reduced() ? 'auto' : 'smooth' });
    // Focus right away so fast typists never write into the previous question.
    const focusTarget = next.querySelector<HTMLElement>('.intake-input:not([hidden]), .intake-choice input:checked, .intake-choice input, [data-send], .intake-btn-wa');
    focusTarget?.focus({ preventScroll: true });
    busy = false;
    saveDraft();
  }

  function forward() {
    const step = steps[current];
    if (step.dataset.step === 'done') return;
    const error = validate(step);
    showError(step, error);
    if (error) return;
    saveDraft();
    go(current + 1, 1);
  }
  const back = () => { if (steps[current].dataset.step !== 'done') go(current - 1, -1); };

  // ----- Review -----
  function buildSummary() {
    const list = root.querySelector<HTMLOListElement>('[data-summary]')!;
    list.replaceChildren();
    let answered = 0;
    questions.forEach((step, i) => {
      const answer = answerOf(step);
      if (answer.length) answered++;
      const li = document.createElement('li');
      li.style.setProperty('--i', String(Math.min(i, 20)));
      const btn = document.createElement('button');
      btn.type = 'button';
      const q = document.createElement('span'); q.className = 'intake-summary-q';
      q.textContent = step.querySelector('.intake-question label, .intake-question > span:not(.intake-qnum):not(.intake-req)')?.textContent || '';
      const a = document.createElement('span'); a.className = 'intake-summary-a';
      a.textContent = answer.length ? answer.join(' · ') : 'Sin responder';
      if (!answer.length) li.classList.add('is-empty');
      btn.append(q, a);
      btn.addEventListener('click', () => go(steps.indexOf(step), -1));
      li.append(btn);
      list.append(li);
    });
    root.querySelector('[data-answered]')!.textContent = String(answered);
  }

  // ----- Submit to Google Forms -----
  async function send(event: Event) {
    event.preventDefault();
    if (busy || sent) return;
    const firstInvalid = questions.find(s => validate(s));
    if (firstInvalid) { go(steps.indexOf(firstInvalid), -1); setTimeout(() => showError(firstInvalid, validate(firstInvalid)), 600); return; }
    const button = root.querySelector<HTMLButtonElement>('[data-send]')!;
    const label = root.querySelector<HTMLElement>('[data-send-label]')!;
    const errorBox = root.querySelector<HTMLElement>('[data-send-error]')!;
    button.disabled = true; button.classList.add('is-sending'); label.textContent = 'Enviando…'; errorBox.textContent = '';
    const body = new URLSearchParams();
    questions.forEach(step => fieldsOf(step).forEach(el => {
      if (el instanceof HTMLInputElement && (el.type === 'radio' || el.type === 'checkbox')) { if (el.checked) body.append(el.name, el.value); return; }
      if (el.hidden && el.matches('[data-other-text]')) return;
      const v = el.value.trim();
      if (v) body.append(el.name, v);
    }));
    body.append('fvv', '1'); body.append('pageHistory', '0');
    try {
      // Google Forms does not allow reading the response (opaque); a network error is the only failure we can detect.
      await fetch(`https://docs.google.com/forms/d/e/${root.dataset.formId}/formResponse`, { method: 'POST', mode: 'no-cors', body });
      sent = true;
      clearDraft();
      finish();
    } catch {
      button.disabled = false; button.classList.remove('is-sending'); label.textContent = 'Intentar de nuevo';
      errorBox.textContent = 'No pudimos enviar tus respuestas. Revisa tu conexión e inténtalo de nuevo, o escríbeme por WhatsApp.';
    }
  }

  function finish() {
    const name = (questions[0] && answerOf(questions[0])[0]) || '';
    const business = (questions[1] && answerOf(questions[1])[0]) || '';
    const first = name.split(/\s+/)[0];
    const doneName = root.querySelector<HTMLElement>('[data-done-name]');
    if (doneName && first) doneName.textContent = `, ${first}`;
    const wa = root.querySelector<HTMLAnchorElement>('[data-done-wa]');
    if (wa) {
      const who = name ? ` Soy ${name}${business ? ` de ${business}` : ''}.` : '';
      const text = `Hola Juan, acabo de llenar el formulario de ${root.dataset.label} en sdtechsystems.dev.${who} Quedo atento(a) para revisarlo juntos.`;
      wa.href = `https://wa.me/${root.dataset.wa}?text=${encodeURIComponent(text)}`;
    }
    busy = false;
    go(steps.findIndex(s => s.dataset.step === 'done'), 1);
    nav.hidden = true;
  }

  // ----- Events -----
  root.querySelectorAll('[data-start]').forEach(b => b.addEventListener('click', () => go(resumeAt, 1)));
  root.querySelector<HTMLButtonElement>('[data-clear-draft]')?.addEventListener('click', event => confirmReset(event.currentTarget as HTMLButtonElement, resetAll));
  form.addEventListener('submit', send);
  root.querySelectorAll('[data-next]').forEach(b => b.addEventListener('click', forward));
  root.querySelector('[data-prev]')?.addEventListener('click', back);
  root.querySelector('[data-fwd]')?.addEventListener('click', forward);

  questions.forEach(step => {
    step.addEventListener('input', () => { syncChoices(step); if (step.classList.contains('has-error') && !validate(step)) showError(step, ''); saveDraft(); });
    step.addEventListener('change', event => {
      const target = event.target as HTMLInputElement;
      syncChoices(step);
      if (target.type === 'radio') {
        const choice = target.closest('.intake-choice');
        choice?.classList.add('just-picked');
        setTimeout(() => choice?.classList.remove('just-picked'), 700);
        // Auto-advance after a single choice, unless "Otro" needs text.
        if (target.dataset.other === undefined && steps[current] === step) setTimeout(() => { if (steps[current] === step) forward(); }, 520);
      } else if (target.type === 'checkbox' && target.checked) {
        const choice = target.closest('.intake-choice');
        choice?.classList.add('just-picked');
        setTimeout(() => choice?.classList.remove('just-picked'), 700);
      }
    });
  });

  document.addEventListener('keydown', event => {
    if (event.defaultPrevented || event.altKey) return;
    const step = steps[current];
    const target = event.target as HTMLElement;
    const inText = target.matches('input[type=text], input[type=tel], textarea');
    if (step.dataset.step === 'intro' && event.key === 'Enter' && !target.closest('button, a')) { event.preventDefault(); go(resumeAt, 1); return; }
    if (!step.dataset.entry) return;
    if (event.key === 'Enter') {
      if (target.tagName === 'TEXTAREA' && !(event.ctrlKey || event.metaKey)) return;
      if (target.closest('button, a') && !target.matches('.intake-choice input')) return;
      event.preventDefault(); forward(); return;
    }
    if (inText || event.ctrlKey || event.metaKey || event.key.length !== 1) return;
    const index = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'.indexOf(event.key.toUpperCase());
    const inputs = [...step.querySelectorAll<HTMLInputElement>('.intake-choice input')];
    if (index >= 0 && inputs[index] && !inputs[index].disabled) {
      event.preventDefault();
      const input = inputs[index];
      input.checked = input.type === 'radio' ? true : !input.checked;
      input.focus({ preventScroll: true });
      input.dispatchEvent(new Event('change', { bubbles: true }));
      saveDraft();
    }
  });

  // Phones rarely fire beforeunload; pagehide and hiding the tab cover reloads, app switches and closing.
  window.addEventListener('pagehide', saveDraft);
  document.addEventListener('visibilitychange', () => { if (document.visibilityState === 'hidden') saveDraft(); });

  // ----- Resume a saved draft -----
  const reviewIndex = steps.findIndex(s => s.dataset.step === 'review');
  if (hasDraft) {
    const saved = Math.min(Math.max(draft!.step, 0), reviewIndex);
    // Without a saved position (older drafts), continue at the first unanswered question.
    const firstOpen = questions.findIndex(s => !answerOf(s).length);
    resumeAt = saved > 0 ? saved : firstOpen >= 0 ? steps.indexOf(questions[firstOpen]) : reviewIndex;
    const answered = questions.filter(s => answerOf(s).length).length;
    const notice = root.querySelector<HTMLElement>('[data-draft-notice]');
    if (notice) {
      notice.hidden = false;
      notice.querySelector('[data-draft-count]')!.textContent = `${answered} de ${total}`;
    }
    root.querySelector<HTMLElement>('[data-clear-draft]')!.hidden = false;
    const where = steps[resumeAt].dataset.entry ? `pregunta ${questions.indexOf(steps[resumeAt]) + 1}` : 'revisión final';
    root.querySelectorAll('[data-start-label]').forEach(l => { l.textContent = `Continuar en la ${where}`; });
    if (saved > 0) {
      // An accidental reload goes straight back to the same question.
      steps[0].hidden = true; steps[0].classList.remove('is-active');
      steps[resumeAt].hidden = false; steps[resumeAt].classList.add('is-active');
      current = resumeAt;
      if (steps[resumeAt].dataset.step === 'review') buildSummary();
      steps[resumeAt].querySelector<HTMLElement>('.intake-input:not([hidden]), .intake-choice input:checked, .intake-choice input, [data-send]')?.focus({ preventScroll: true });
      showResumeToast(answered);
    }
  }

  function showResumeToast(answered: number) {
    const toast = document.createElement('div');
    toast.className = 'intake-toast';
    toast.setAttribute('role', 'status');
    const text = document.createElement('p');
    text.innerHTML = `<b>Recuperamos tu avance.</b> ${answered} de ${total} respuestas guardadas en este dispositivo.`;
    const restart = document.createElement('button');
    restart.type = 'button'; restart.textContent = 'Empezar de nuevo';
    const close = document.createElement('button');
    close.type = 'button'; close.className = 'intake-toast-close'; close.setAttribute('aria-label', 'Cerrar aviso'); close.textContent = '✕';
    const dismiss = () => { toast.classList.add('is-leaving'); setTimeout(() => toast.remove(), reduced() ? 0 : 300); };
    restart.addEventListener('click', () => confirmReset(restart, () => { resetAll(); dismiss(); busy = false; go(0, -1); }));
    close.addEventListener('click', dismiss);
    toast.append(text, restart, close);
    document.body.append(toast);
    setTimeout(() => { if (!restart.dataset.armed) dismiss(); }, 9000);
  }

  updateProgress();
}
