/**
 * PURE & OLIVE - Skin Routine Quiz Engine
 * Interactive diagnostic matching user's skin type & concerns to tailored clean beauty routines
 */

let quizState = {
  skin_type: 'combination',
  concern: 'acne',
  style: 'complete',
  step: 1
};

let currentBundle = [];

function setQuizStep(stepNumber) {
  quizState.step = stepNumber;

  // Update step indicator
  document.querySelectorAll('.quiz-step-dot').forEach((dot, idx) => {
    if (idx + 1 === stepNumber) {
      dot.classList.add('active');
    } else if (idx + 1 < stepNumber) {
      dot.classList.add('completed');
    } else {
      dot.classList.remove('active', 'completed');
    }
  });

  // Show/Hide steps
  document.querySelectorAll('.quiz-step-pane').forEach((pane, idx) => {
    pane.style.display = (idx + 1 === stepNumber) ? 'block' : 'none';
  });

  // Scroll to quiz container
  const container = document.getElementById('quiz-card-container');
  if (container) {
    container.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
  }
}

function selectSkinType(val) {
  quizState.skin_type = val;
  highlightSelection('skin-type-option', val);
  setTimeout(() => setQuizStep(2), 300);
}

function selectConcern(val) {
  quizState.concern = val;
  highlightSelection('concern-option', val);
  setTimeout(() => setQuizStep(3), 300);
}

function selectStyle(val) {
  quizState.style = val;
  highlightSelection('style-option', val);
  submitQuiz();
}

function highlightSelection(className, value) {
  document.querySelectorAll(`.${className}`).forEach(btn => {
    if (btn.dataset.value === value) {
      btn.classList.add('selected');
    } else {
      btn.classList.remove('selected');
    }
  });
}

async function submitQuiz() {
  const loadingEl = document.getElementById('quiz-loading');
  const resultEl = document.getElementById('quiz-result-pane');
  const stepPanes = document.querySelectorAll('.quiz-step-pane');

  stepPanes.forEach(pane => pane.style.display = 'none');
  if (loadingEl) loadingEl.style.display = 'block';

  try {
    const res = await fetch('/api/quiz-recommend', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(quizState)
    });

    const data = await res.json();
    if (loadingEl) loadingEl.style.display = 'none';

    if (data.status === 'success') {
      renderQuizResults(data);
      if (resultEl) resultEl.style.display = 'block';
    } else {
      alert('เกิดข้อผิดพลาดในการประมวลผล กรุณาลองใหม่อีกครั้ง');
      setQuizStep(1);
    }
  } catch (err) {
    console.error(err);
    if (loadingEl) loadingEl.style.display = 'none';
    alert('ไม่สามารถเชื่อมต่อระบบได้ กรุณาลองใหม่อีกครั้ง');
    setQuizStep(1);
  }
}

function renderQuizResults(data) {
  currentBundle = data.bundle_items || [];

  // Update Header Labels
  document.getElementById('result-skin-type').textContent = data.skin_type_label;
  document.getElementById('result-concern').textContent = data.concern_label;
  document.getElementById('result-advice').textContent = data.advice;

  // Render Morning Routine
  const morningContainer = document.getElementById('morning-routine-list');
  morningContainer.innerHTML = data.morning_routine.map((p, idx) => `
    <div class="routine-item-card">
      <div class="routine-step-num">Step ${idx + 1}</div>
      <img src="${p.image_url}" alt="${p.name}" class="routine-item-img">
      <div class="routine-item-info">
        <span class="routine-badge">${p.subcategory.toUpperCase()}</span>
        <h5>${p.name}</h5>
        <div class="routine-price">฿${p.price.toLocaleString()}</div>
      </div>
      <button class="btn btn-secondary" onclick="addToCart({id: ${p.id}, name: '${p.name.replace(/'/g, "\\'")}', price: ${p.price}, image_url: '${p.image_url}', volume: '${p.volume}'})" style="padding: 6px 14px; font-size: 0.8rem; margin-left: auto;">
        + ชิ้นนี้
      </button>
    </div>
  `).join('');

  // Render Night Routine
  const nightContainer = document.getElementById('night-routine-list');
  nightContainer.innerHTML = data.night_routine.map((p, idx) => `
    <div class="routine-item-card">
      <div class="routine-step-num">Step ${idx + 1}</div>
      <img src="${p.image_url}" alt="${p.name}" class="routine-item-img">
      <div class="routine-item-info">
        <span class="routine-badge">${p.subcategory.toUpperCase()}</span>
        <h5>${p.name}</h5>
        <div class="routine-price">฿${p.price.toLocaleString()}</div>
      </div>
      <button class="btn btn-secondary" onclick="addToCart({id: ${p.id}, name: '${p.name.replace(/'/g, "\\'")}', price: ${p.price}, image_url: '${p.image_url}', volume: '${p.volume}'})" style="padding: 6px 14px; font-size: 0.8rem; margin-left: auto;">
        + ชิ้นนี้
      </button>
    </div>
  `).join('');

  // Bundle Summary
  document.getElementById('bundle-original-price').textContent = `฿${data.subtotal.toLocaleString('th-TH', { minimumFractionDigits: 2 })}`;
  document.getElementById('bundle-discount').textContent = `- ฿${data.discount.toLocaleString('th-TH', { minimumFractionDigits: 2 })}`;
  document.getElementById('bundle-final-price').textContent = `฿${data.bundle_price.toLocaleString('th-TH', { minimumFractionDigits: 2 })}`;
  document.getElementById('bundle-count').textContent = `${data.bundle_items.length} ชิ้น`;
}

function addFullBundleToCart() {
  if (currentBundle && currentBundle.length > 0) {
    addBundleToCart(currentBundle);
  }
}

function restartQuiz() {
  document.getElementById('quiz-result-pane').style.display = 'none';
  setQuizStep(1);
}
