(() => {
  const csrfEl = document.getElementById('csrf');
  const csrf = csrfEl ? csrfEl.value : '';

  async function sessionCheck() {
    // Revalidate auth on BFCache restore or normal load
    try {
      const res = await fetch('/session-check', { credentials: 'same-origin', cache: 'no-store' });
      if (res.status === 403) location.replace('/verify-2fa');
      else if (res.status >= 400) location.replace('/');
    } catch {
      location.replace('/');
    }
  }

  async function revealSecret(id) {
    const form = new FormData();
    form.append('item_id', id);
    form.append('csrf_token', csrf);
    const res = await fetch('/vault/reveal', { method: 'POST', body: form, credentials: 'same-origin', cache: 'no-store' });
    if (!res.ok) throw new Error('Reveal failed');
    return await res.text();
  }

  function onTableClick(e) {
    const btn = e.target.closest('button');
    if (!btn) return;

    const row = btn.closest('tr');
    if (!row) return;
    const id = row.dataset.id;
    const span = row.querySelector('.secret');

    if (btn.classList.contains('reveal')) {
      if (span.dataset.loaded === 'true') {
        span.textContent = '••••••••';
        span.dataset.loaded = 'false';
        btn.textContent = 'Reveal';
        return;
      }
      btn.disabled = true;
      revealSecret(id).then(txt => {
        span.textContent = txt;
        span.dataset.loaded = 'true';
        btn.textContent = 'Hide';
      }).catch(err => {
        alert(err.message || 'Reveal failed');
      }).finally(() => { btn.disabled = false; });
    }

    if (btn.classList.contains('copy')) {
      (async () => {
        try {
          let txt = span.dataset.loaded === 'true' ? span.textContent : await revealSecret(id);
          await navigator.clipboard.writeText(txt);
          const old = btn.textContent;
          btn.textContent = 'Copied';
          setTimeout(() => (btn.textContent = old), 1000);
        } catch {
          alert('Copy failed');
        }
      })();
    }
  }

  // Revalidate when page is shown (handles back/forward cache)
  window.addEventListener('pageshow', sessionCheck);

  // Event delegation: one listener for all rows/buttons
  const tbody = document.querySelector('table tbody');
  if (tbody) tbody.addEventListener('click', onTableClick);
})();
