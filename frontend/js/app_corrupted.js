/* AI Fake News Detector - frontend logic. Talks to the Flask backend via /api/* */
/* ============================= ICONS ============================= */
const ICONS = {
  shield:`<svg width="18" height="18" viewBox="0 0 24 24" fill="none"><path d="M12 2l8 3v6c0 5-3.4 8.9-8 11-4.6-2.1-8-6-8-11V5l8-3z" fill="#fff" opacity=".95"/><path d="M9 12l2 2 4-4" stroke="#5b21b6" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>`,
  home:`<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 11l9-8 9 8"/><path d="M5 10v10h14V10"/></svg>`,
  check:`<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="7"/><path d="M21 21l-4.3-4.3"/></svg>`,
  history:`<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 3"/></svg>`,
  dash:`<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="3" width="7" height="9" rx="1.5"/><rect x="14" y="3" width="7" height="5" rx="1.5"/><rect x="14" y="12" width="7" height="9" rx="1.5"/><rect x="3" y="16" width="7" height="5" rx="1.5"/></svg>`,
  info:`<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="9"/><path d="M12 8h.01M11 12h1v5h1"/></svg>`,
  mail:`<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="5" width="18" height="14" rx="2"/><path d="M3 7l9 6 9-6"/></svg>`,
  logout:`<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M9 21H5a2 2 0 01-2-2V5a2 2 0 012-2h4"/><path d="M16 17l5-5-5-5"/><path d="M21 12H9"/></svg>`,
  globe:`<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3a15 15 0 010 18 15 15 0 010-18z"/></svg>`,
  bolt:`<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M13 2L4 14h6l-1 8 9-12h-6l1-8z"/></svg>`,
  clock:`<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3.5 2"/></svg>`,
  cpu:`<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="7" y="7" width="10" height="10" rx="1.5"/><path d="M12 2v3M12 19v3M2 12h3M19 12h3M5 5l2 2M17 17l2 2M19 5l-2 2M7 17l-2 2"/></svg>`,
  gauge:`<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M4 15a8 8 0 1116 0"/><path d="M12 15l4-5"/></svg>`,
  tag:`<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M20 12l-8 8-9-9V4h7l10 8z"/><circle cx="7.5" cy="7.5" r="1"/></svg>`,
  lamp:`<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M9 18h6M10 21h4M12 3a6 6 0 00-3 11c.6.4 1 1.1 1 2h4c0-.9.4-1.6 1-2a6 6 0 00-3-11z"/></svg>`,
  download:`<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 3v12M7 11l5 5 5-5"/><path d="M5 21h14"/></svg>`,
  refresh:`<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M20 11A8 8 0 105.5 16.5M20 11V5M20 11h-6"/></svg>`,
  share:`<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="18" cy="5" r="2.5"/><circle cx="6" cy="12" r="2.5"/><circle cx="18" cy="19" r="2.5"/><path d="M8.3 10.7l7.4-4.4M8.3 13.3l7.4 4.4"/></svg>`,
  total:`<svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M9 12l2 2 4-4"/><circle cx="12" cy="12" r="9"/></svg>`,
  real:`<svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M20 6L9 17l-5-5"/></svg>`,
  fake:`<svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M18 6L6 18M6 6l12 12"/></svg>`,
  acc:`<svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 17l6-6 4 4 8-8"/><path d="M15 7h6v6"/></svg>`,
  inbox:`<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6"><path d="M4 12h4l2 3h4l2-3h4"/><path d="M5 4h14l2 8v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6l2-8z"/></svg>`,
};


/* ============================= STATE / API ============================= */
let currentView = 'home';
let currentTab = 'text';
let historyPage = 1;
const HISTORY_PAGE_SIZE = 5;
let charts = {};
let modelAccuracy = null;

async function api(path, {method='GET', body}={}){
  const res = await fetch(path, {method, headers: body?{'Content-Type':'application/json'}:undefined, body: body?JSON.stringify(body):undefined});
  let data = null;
  try{ data = await res.json(); }catch(e){}
  if(!res.ok) throw new Error((data && data.error) || `Request failed (${res.status})`);
  return data;
}

/* ============================= UTIL ============================= */
function toast(msg, ms=2600){
  const t=document.getElementById('toast'); t.textContent=msg; t.classList.add('show');
  clearTimeout(t._h); t._h=setTimeout(()=>t.classList.remove('show'), ms);
}
function esc(s){ return (s||'').replace(/[&<>"']/g, c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c])); }
function fmtDate(d){
  const dt = new Date(d);
  return dt.toLocaleDateString('en-GB',{day:'2-digit',month:'short',year:'numeric'}) + ', ' +
         dt.toLocaleTimeString('en-US',{hour:'numeric',minute:'2-digit',hour12:true});
}
function fmtDateShort(d){ return new Date(d).toLocaleDateString('en-GB',{day:'2-digit',month:'short'}); }

const UI_STR = {
  whyFake:{English:'Why this news is Fake?', Hindi:'à¤¯à¤¹ à¤¨à¥à¤¯à¥‚à¤œà¤¼ à¤«à¥‡à¤• à¤•à¥à¤¯à¥‹à¤‚ à¤¹à¥ˆ?', Marathi:'à¤¹à¥€ à¤¬à¤¾à¤¤à¤®à¥€ à¤¬à¤¨à¤¾à¤µà¤Ÿ à¤•à¤¾ à¤†à¤¹à¥‡?'},
  whyReal:{English:'Why this news looks Real?', Hindi:'à¤¯à¤¹ à¤¨à¥à¤¯à¥‚à¤œà¤¼ à¤…à¤¸à¤²à¥€ à¤•à¥à¤¯à¥‹à¤‚ à¤²à¤—à¤¤à¥€ à¤¹à¥ˆ?', Marathi:'à¤¹à¥€ à¤¬à¤¾à¤¤à¤®à¥€ à¤–à¤°à¥€ à¤•à¤¾ à¤µà¤¾à¤Ÿà¤¤à¥‡?'},
};

/* ============================= NAV / ROUTER ============================= */
const NAV_ITEMS = [
  {id:'home', label:'Home', icon:'home'},
  {id:'check', label:'Check News', icon:'check'},
  {id:'history', label:'History', icon:'history'},
  {id:'dashboard', label:'Dashboard', icon:'dash'},
  {id:'about', label:'About', icon:'info'},
  {id:'contact', label:'Contact', icon:'mail'},
];
const SIDEBAR_ITEMS = [
  {id:'dashboard', label:'Dashboard', icon:'dash'},
  {id:'check', label:'Check News', icon:'check'},
  {id:'history', label:'History', icon:'history'},
];
function renderNav(){
  const nav = document.getElementById('navlinks');
  nav.innerHTML = NAV_ITEMS.map(n=>`<button data-nav="${n.id}" class="${(currentView===n.id||(n.id==='check'&&currentView==='home'&&false))?'active':''}">${n.label}</button>`).join('');
  nav.querySelectorAll('button').forEach(b=>b.addEventListener('click', ()=>go(b.dataset.nav)));
  const lb = document.getElementById('logoutBtn');
  lb.innerHTML = ICONS.logout + '<span>Logout</span>';
  lb.onclick = ()=> toast('Demo workspace — logout is disabled here.');

  const sidebar = document.getElementById('sidebar');
  sidebar.innerHTML = SIDEBAR_ITEMS.map(n=>`<button data-nav="${n.id}" class="${currentView===n.id?'active':''}">${ICONS[n.icon]}<span>${n.label}</span></button>`).join('<hr>');
  sidebar.querySelectorAll('button').forEach(b=>b.addEventListener('click', ()=>go(b.dataset.nav)));

  document.getElementById('shell').classList.toggle('with-sidebar', currentView==='dashboard' || currentView==='history');
  nav.querySelectorAll('button').forEach(b=>{
    let active = b.dataset.nav===currentView || (b.dataset.nav==='check' && currentView==='result');
    b.classList.toggle('active', active);
  });
}
function go(view){
  currentView = view;
  ['home','result','dashboard','history','about','contact'].forEach(v=>{
    document.getElementById('view-'+v).hidden = (v!==view) && !(view==='check' && v==='home');
  });
  if(view==='check') { currentView='home'; document.getElementById('view-home').hidden=false; }
  renderNav();
  if(view==='dashboard') renderDashboard();
  if(view==='history') renderHistory();
  window.scrollTo({top:0, behavior:'instant'});
}


/* ============================= HOME VIEW ============================= */
function renderHome(){
  const el = document.getElementById('view-home');
  el.innerHTML = `
  <div class="hero">
    <h1>AI-Powered Fake News Detection</h1>
    <p>Detect fake news in English, Hindi and Marathi using an AI-powered machine learning model.</p>
    <div class="panel">
      <div class="tabs">
        <button data-tab="text" class="${currentTab==='text'?'active':''}">Text</button>
        <button data-tab="url" class="${currentTab==='url'?'active':''}">URL</button>
      </div>
      <div id="tabpane"></div>
    </div>
    <div class="features">
      <div class="f"><span class="icon-badge">${ICONS.globe}</span><div><b>Multi-Language Support</b>English, Hindi, Marathi</div></div>
      <div class="f"><span class="icon-badge">${ICONS.cpu}</span><div><b>AI-Powered Analysis</b>Machine Learning Models</div></div>
      <div class="f"><span class="icon-badge">${ICONS.bolt}</span><div><b>Real-time Results</b>Instant detection &amp; score</div></div>
    </div>
  </div>`;
  el.querySelectorAll('[data-tab]').forEach(b=>b.addEventListener('click', ()=>{ currentTab=b.dataset.tab; renderTabPane(); el.querySelectorAll('[data-tab]').forEach(x=>x.classList.toggle('active', x.dataset.tab===currentTab)); }));
  renderTabPane();
}
function renderTabPane(){
  const pane = document.getElementById('tabpane');
  if(currentTab==='text'){
    pane.innerHTML = `
      <label class="field-label">Enter News Content</label>
      <textarea id="newsText" rows="5" maxlength="2000" placeholder="Paste or type a news article, headline or forwarded message here...">à¤¸à¤°à¤•à¤¾à¤° à¤¨à¥‡ à¤˜à¥‹à¤·à¤£à¤¾ à¤•à¥€ à¤¹à¥ˆ à¤•à¤¿ à¤ªà¥à¤°à¤¤à¥à¤¯à¥‡à¤• à¤¨à¤¾à¤—à¤°à¤¿à¤• à¤•à¥‹ â‚¹5 à¤²à¤¾à¤– à¤°à¥à¤ªà¤ à¤®à¥à¤«à¥à¤¤ à¤¦à¤¿à¤ à¤œà¤¾à¤à¤‚à¤—à¥‡à¥¤</textarea>
      <div class="counter"><span id="charCount">0</span> / 2000</div>
      <div class="row-between">
        <select id="langSelect">
          <option value="auto">Auto Detect Language</option>
          <option value="English">English</option>
          <option value="Hindi">Hindi</option>
          <option value="Marathi">Marathi</option>
        </select>
        <button class="btn btn-primary" id="checkBtn">${ICONS.check}<span>Check News</span></button>
      </div>
      <div class="aidisc">${ICONS.info}<span>Results are a statistical estimate, always verify important claims with an official source.</span></div>`;
    const ta = pane.querySelector('#newsText');
    const cc = pane.querySelector('#charCount');
    const upd=()=>{ cc.textContent = ta.value.length; };
    ta.addEventListener('input', upd); upd();
    pane.querySelector('#checkBtn').addEventListener('click', ()=>submitCheck());
  } else {
    pane.innerHTML = `
      <label class="field-label">Paste News URL</label>
      <input type="text" id="newsUrl" placeholder="https://example.com/news/article">
      <label class="field-label" style="margin-top:14px;">Headline / Snippet (optional)</label>
      <textarea id="newsUrlText" rows="3" maxlength="2000" placeholder="Paste the headline or a short snippet if you have it — improves accuracy"></textarea>
      <div class="row-between">
        <select id="langSelect">
          <option value="auto">Auto Detect Language</option>
          <option value="English">English</option>
          <option value="Hindi">Hindi</option>
          <option value="Marathi">Marathi</option>
        </select>
        <button class="btn btn-primary" id="checkBtn">${ICONS.check}<span>Check News</span></button>
      </div>
      <div class="aidisc">${ICONS.info}<span>The server downloads the article text from the link (public pages only). Adding a headline/snippet is optional.</span></div>`;
    pane.querySelector('#checkBtn').addEventListener('click', ()=>submitCheck());
  }
}
async function submitCheck(){
  const btn = document.querySelector('#checkBtn');
  let text='', url='';
  if(currentTab==='text'){
    text = document.getElementById('newsText').value.trim();
    if(!text){ toast('Please enter some news text first.'); return; }
      if(text.length < 80){ toast('This is a very short claim. The AI prediction may be less reliable. For better results, paste the full news text or use the article URL.', 5500); }
  } else {
    url = document.getElementById('newsUrl').value.trim();
    text = document.getElementById('newsUrlText').value.trim();
    if(!url){ toast('Please paste a news URL first.'); return; }
  }
  const language = document.getElementById('langSelect').value;
  btn.disabled = true; btn.innerHTML = `<span class="spinner"></span><span>Analyzing...</span>`;
  try{
    const record = await api('/api/analyze', {method:'POST', body:{text, url, language}});
    renderResult(record);
    go('result');
  } catch(e){
    toast(e.message || 'Something went wrong. Please try again.', 4200);
  } finally {
    btn.disabled = false; btn.innerHTML = `${ICONS.check}<span>Check News</span>`;
  }
}


/* ============================= RESULT VIEW ============================= */
function ringSvg(pct, color){
  const r=58, c=2*Math.PI*r;
  const dash = c*(pct/100);
  return `<svg width="150" height="150" viewBox="0 0 150 150">
    <circle cx="75" cy="75" r="${r}" fill="none" stroke="var(--border)" stroke-width="13"/>
    <circle cx="75" cy="75" r="${r}" fill="none" stroke="${color}" stroke-width="13" stroke-linecap="round"
      stroke-dasharray="${dash} ${c-dash}"/>
  </svg>`;
}
function renderResult(record){
const el = document.getElementById('view-result');

const assessment = record.assessment || record.final_assessment || {};
const finalPrediction =
    record.final_prediction ||
    record.prediction ||
    record.baseline_prediction ||
    {};

const rawVerdict = finalPrediction.verdict || 'UNKNOWN';

// Convert knowledge-rule results into our simple FAKE/REAL system.
let verdict = rawVerdict;

if (rawVerdict === 'SUPPORTS') {
    verdict = 'REAL';
} else if (rawVerdict === 'REFUTES') {
    verdict = 'FAKE';
}

const prediction = {
    ...finalPrediction,
    verdict: verdict
};

const signals = assessment.signals || {};

const confidence = finalPrediction.confidence
    ? (finalPrediction.confidence <= 1
        ? finalPrediction.confidence * 100
        : finalPrediction.confidence)
    : 0;

const confidenceSource =
    finalPrediction.source || 'AI model probability — not a factual guarantee';

const factChecks = assessment.fact_checks || record.fact_checks || [];
const newsSources = assessment.news_sources || record.news_sources || [];
const summary = assessment.fact_check_summary || {};

let verdictClass = 'real';
if (verdict === 'FAKE') {
  verdictClass = 'fake';
}

let verdictIcon = 'âš ';
if (verdict === 'REAL') verdictIcon = 'âœ“';
if (verdict === 'UNKNOWN') verdictIcon = '?';

const language = record.language || 'Unknown';

const sourceInfo = record.source || {};
const sourceDomain = sourceInfo.domain || 'Unknown';
const sourceStatus = sourceInfo.assessment || 'UNKNOWN';
const sourceSignals = sourceInfo.signals || [];

const factCheckHTML = factChecks.length
    ? factChecks.map(item => `
        <div class="card" style="margin-top:10px;">
          <div style="display:flex;justify-content:space-between;gap:10px;align-items:center;">
            <strong>${esc(item.publisher || 'Unknown publisher')}</strong>
            <span class="badge ${
              item.normalized_rating === 'REFUTED' ? 'fake' :
              item.normalized_rating === 'SUPPORTED' ? 'real' : ''
            }">
              ${esc(item.normalized_rating || 'UNKNOWN')}
            </span>
          </div>

          <div class="small muted" style="margin-top:6px;">
            Rating: ${esc(item.rating || 'Not specified')}
          </div>

          ${
            item.url
              ? `<div style="margin-top:8px;">
                   <a href="${esc(item.url)}" target="_blank" rel="noopener noreferrer">
                     View fact-check source â†’
                   </a>
                 </div>`
              : ''
          }
        </div>
      `).join('')
    : `
      <div class="muted small">
        No external fact-check results were found for this claim.
      </div>
    `;
    const newsSourceHTML = '';
      const sourceHTML = `
       <div class="card" style="margin-top:10px;">
         <div style="display:flex;justify-content:space-between;gap:10px;align-items:center;">
           <strong>News Source</strong>
           <span class="badge">
             ${esc(sourceStatus)}
           </span>
        </div>

        <div style="margin-top:10px;">
          <strong>Domain:</strong> ${esc(sourceDomain)}
        </div>

        ${
          sourceSignals.length
            ? `<div style="margin-top:8px;">
                 ${sourceSignals.map(signal => `<div class="small muted">${esc(signal)}</div>`).join('')}
              </div>`
            : ''
        }
       </div>
      `;

  const reasons = [];

  if (signals.fact_check_refuted > 0) {
    reasons.push(
      `${signals.fact_check_refuted} external fact-check result(s) contradict this claim.`
    );
  }

  if (signals.fact_check_misleading > 0) {
    reasons.push(
      `${signals.fact_check_misleading} result(s) were rated misleading or missing context.`
    );
  }

  if (signals.fact_check_supported > 0) {
    reasons.push(
      `${signals.fact_check_supported} external fact-check result(s) support this claim.`
    );
  }

  if (prediction.verdict) {
    reasons.push(
      `AI fake-news model result: ${prediction.verdict}.`
    );
  }
  if (signals.news_sources > 0) {
    reasons.push(
      `${signals.news_sources} current news source(s) were found for this claim.`
    );
  }

  if (!reasons.length) {
    reasons.push(
      'There was not enough external evidence to produce a stronger conclusion.'
    );
  }

  el.innerHTML = `
    <div class="wrap">

      <div class="result-head">
        <h2>Analysis Result</h2>
      </div>

      <div class="grid3" style="align-items:stretch;">

        <!-- VERDICT -->
        <div class="card verdict-card">

          <span class="verdict-pill ${verdictClass}">
            ${verdictIcon} ${esc(verdict)}
          </span>

          <div style="margin-top:25px;text-align:center;">
            <div style="font-size:42px;font-weight:800;">
              ${confidence}%
          </div>

          <div class="muted small">
            Confidence
          </div>

          <div class="small muted" style="margin-top:8px;">
             Based on ${esc(confidenceSource)}
          </div>

          <div style="margin-top:20px;font-size:13px;">
           ${summary.total || 0} external fact-check result(s)
          </div>

          <div class="muted small" style="margin-top:20px;text-align:center;">
            Final assessment based on available evidence.
          </div>

        </div>

        <!-- MODEL -->
        <div class="card">

          <h3>AI Verification</h3>

          <div class="meta-list">

            <div class="meta-item">
              <span class="ic">${ICONS.cpu}</span>
              <div>
                <div class="lab">Model</div>
                <div class="val">Fake News Classifier</div>
              </div>
            </div>

            <div class="meta-item">
              <span class="ic">${ICONS.tag}</span>
              <div>
                <div class="lab">Model Verdict</div>
                <div class="val">
                  ${esc(prediction.verdict || 'Not available')}
                </div>
              </div>
            </div>

            <div class="meta-item">
              <span class="ic">${ICONS.globe}</span>
              <div>
                <div class="lab">Language</div>
                <div class="val">${esc(language)}</div>
              </div>
            </div>

          </div>

        </div>

        <!-- FACT CHECK SUMMARY -->
        <div class="card">

          <h3>Fact-Check Summary</h3>

          <div class="meta-list">

            <div class="meta-item">
              <span class="ic">${ICONS.fake}</span>
              <div>
                <div class="lab">Refuted</div>
                <div class="val">${summary.refuted || 0}</div>
              </div>
            </div>

            <div class="meta-item">
              <span class="ic">${ICONS.real}</span>
              <div>
                <div class="lab">Supported</div>
                <div class="val">${summary.supported || 0}</div>
              </div>
            </div>

            <div class="meta-item">
              <span class="ic">${ICONS.tag}</span>
              <div>
                <div class="lab">Misleading</div>
                <div class="val">${summary.misleading || 0}</div>
              </div>
            </div>

          </div>

        </div>

      </div>

      <!-- REASONS -->

      <div class="card" style="margin-top:16px;">

        <h3>Why this result was produced</h3>

        <ul class="reasons" style="list-style:none;padding:0;margin:0;">
          ${reasons.map(r => `
            <li>
              <span class="x">â€¢</span>
              <span>${esc(r)}</span>
            </li>
          `).join('')}
        </ul>

      </div>

      <!-- FACT CHECK SOURCES -->

      <div class="card" style="margin-top:16px;">

        <h3>External Fact-Check Sources</h3>

        <div style="margin-top:12px;">
          ${factCheckHTML}
        </div>

      </div>
      <!-- NEWS SOURCE -->

      <div class="card" style="margin-top:16px;">

        <h3>News Source</h3>

        <div style="margin-top:12px;">
         ${sourceHTML}
        </div>

      </div>      

      <!-- NEWS TEXT -->

      <div class="grid2" style="margin-top:16px;">

        <div class="card">
          <h3>News / Claim</h3>

          <div class="newstext">
            ${esc(record.text || record.input?.text || record.claims?.[0] || record.url || '')}
          </div>
        </div>

        <div class="card">

          <h3>${ICONS.lamp} Recommendation</h3>

          <p style="font-size:13.5px;line-height:1.6;margin:0;">
            ${
              verdict === 'FAKE'
              ? 'The AI fake-news model classified this news as FAKE. Review the source and supporting information before sharing.'
              : verdict === 'REAL'
              ? 'The AI fake-news model classified this news as REAL. The source should still be checked before relying on the information.'
              : 'The system could not determine whether this news is FAKE or REAL.' 
            }
          </p>

        </div>

      </div>

      <!-- ACTIONS -->

      <div class="result-actions">

        <button class="btn btn-primary" id="dlPdfBtn">
          ${ICONS.download}
          <span>Download Report (PDF)</span>
        </button>

        <button class="btn btn-blue" id="anotherBtn">
          ${ICONS.refresh}
          <span>Check Another News</span>
        </button>

        <button class="btn btn-outline" id="shareBtn">
          ${ICONS.share}
          <span>Share Result</span>
        </button>

      </div>

    </div>
  `;

  el.querySelector('#anotherBtn')
    .addEventListener('click', () => go('home'));

  el.querySelector('#shareBtn')
    .addEventListener('click', () => shareResult(record));

  el.querySelector('#dlPdfBtn')
    .addEventListener('click', (e) =>
      downloadReport(record, e.target.closest('button'))
    );
}
async function shareResult(record){
  const summary = `AI Fake News Detector — ${record.id}\nVerdict: ${record.verdict} (${record.score}% ${record.verdict==='FAKE'?'fake':'real'} probability)\nCategory: ${record.category}\n${record.text ? 'Text: '+record.text.slice(0,140) : ''}`;
  if(navigator.share){
    try{ await navigator.share({title:'Fake News Detection Result', text:summary}); return; }catch(e){ /* fallthrough */ }
  }
  try{ await navigator.clipboard.writeText(summary); toast('Result copied to clipboard.'); }
  catch(e){ toast('Could not share automatically — copy the result manually.'); }
}

/* ---------- PDF report ---------- */
function buildReportHTML(record){
  const isFake = record.verdict==='FAKE';
  return `
  <div style="padding:34px;">
    <div style="display:flex;align-items:center;gap:12px;border-bottom:3px solid #5b21b6;padding-bottom:16px;margin-bottom:22px;">
      <div style="width:40px;height:40px;border-radius:10px;background:linear-gradient(120deg,#5b21b6,#2f6bff);display:flex;align-items:center;justify-content:center;">${ICONS.shield}</div>
      <div>
        <div style="font-size:19px;font-weight:800;color:#111;">AI-Powered Fake News Detection Report</div>
        <div style="font-size:11.5px;color:#777;">Generated by AI Fake News Detector</div>
      </div>
    </div>
    <div style="font-size:17px;font-weight:800;color:${isFake?'#dc2626':'#16a34a'};margin-bottom:16px;">RESULT: ${isFake?'FAKE NEWS':'REAL NEWS'} &nbsp;(${record.score}% ${isFake?'Fake':'Real'} Probability)</div>
    <table style="font-size:13px;line-height:1.9;color:#222;margin-bottom:18px;">
      <tr><td style="padding-right:14px;color:#666;">News ID</td><td>: ${record.id}</td></tr>
      <tr><td style="padding-right:14px;color:#666;">Checked At</td><td>: ${fmtDate(record.createdAt)}</td></tr>
      <tr><td style="padding-right:14px;color:#666;">Language</td><td>: ${record.lang}</td></tr>
      <tr><td style="padding-right:14px;color:#666;">Model Used</td><td>: ${esc(record.model)}</td></tr>
      <tr><td style="padding-right:14px;color:#666;">Confidence Score</td><td>: ${record.score}%</td></tr>
      <tr><td style="padding-right:14px;color:#666;">Category</td><td>: ${esc(record.category)}${isFake?' / Misleading':''}</td></tr>
    </table>
    <div style="font-weight:700;font-size:13.5px;margin-bottom:6px;color:#111;">News Text:</div>
    <div style="font-size:13px;background:#f5f6fb;border:1px solid #e4e8f3;border-radius:8px;padding:12px 14px;margin-bottom:18px;line-height:1.7;">${esc(record.text||record.url||'')}</div>
    <div style="font-weight:700;font-size:13.5px;margin-bottom:8px;color:#111;">Analysis Summary:</div>
    <ul style="margin:0 0 18px;padding-left:20px;font-size:13px;line-height:1.9;">${record.reasons.map(r=>`<li>${esc(r)}</li>`).join('')}</ul>
    <div style="font-weight:700;font-size:13.5px;margin-bottom:6px;color:#111;">Recommendation:</div>
    <div style="font-size:13px;margin-bottom:34px;">${esc(record.recommendation)}</div>
    <div style="text-align:right;font-size:12px;color:#666;font-style:italic;">AI Fake News Detector System</div>
  </div>`;
}
async function downloadReport(record, btn){
  const orig = btn.innerHTML;
  btn.disabled = true; btn.innerHTML = `<span class="spinner"></span><span>Preparing...</span>`;
  try{
    const holder = document.getElementById('reportTemplate');
    holder.innerHTML = buildReportHTML(record);
    await new Promise(r=>setTimeout(r,50));
    const canvas = await html2canvas(holder, {scale:2, backgroundColor:'#ffffff', width:760});
    const imgData = canvas.toDataURL('image/png');
    const { jsPDF } = window.jspdf;
    const pdf = new jsPDF({unit:'pt', format:'a4'});
    const pageW = pdf.internal.pageSize.getWidth();
    const pageH = pdf.internal.pageSize.getHeight();
    const imgW = pageW;
    const imgH = canvas.height * (imgW / canvas.width);
    if(imgH <= pageH){
      pdf.addImage(imgData,'PNG',0,0,imgW,imgH);
    } else {
      let remaining = canvas.height, y = 0;
      const pageCanvasH = Math.floor(pageH * (canvas.width / pageW));
      while(remaining > 0){
        const sliceH = Math.min(pageCanvasH, remaining);
        const sliceCanvas = document.createElement('canvas');
        sliceCanvas.width = canvas.width; sliceCanvas.height = sliceH;
        sliceCanvas.getContext('2d').drawImage(canvas, 0, y, canvas.width, sliceH, 0, 0, canvas.width, sliceH);
        const sliceImg = sliceCanvas.toDataURL('image/png');
        if(y>0) pdf.addPage();
        pdf.addImage(sliceImg,'PNG',0,0,imgW, sliceH*(imgW/canvas.width));
        y += sliceH; remaining -= sliceH;
      }
    }
    const blob = pdf.output('blob');
    const a = document.createElement('a');
    a.href = URL.createObjectURL(blob); a.download = `${record.id}-fake-news-report.pdf`; a.click();
  } catch(e){
    toast('Could not generate the PDF report.');
  } finally {
    btn.disabled=false; btn.innerHTML = orig;
  }
}


/* ============================= DASHBOARD ============================= */
async function renderDashboard(){
  const el = document.getElementById('view-dashboard');
  let s;
  try{ s = await api('/api/stats'); }
  catch(e){ el.innerHTML = `<div class="wrap"><div class="card empty">Could not load statistics. Is the backend running?</div></div>`; return; }
  modelAccuracy = s.modelAccuracy;

  if(!s.total){
    el.innerHTML = `<div class="wrap"><h1 class="page-title">Dashboard</h1><p class="page-sub">Overview of every news check you've run.</p>
      <div class="card empty"><div class="ic">${ICONS.inbox}</div><b>No checks yet</b><div class="small" style="margin-top:6px;">Run your first check to populate the dashboard.</div>
      <div style="margin-top:16px;"><button class="btn btn-primary" id="goCheck">${ICONS.check}<span>Check News</span></button></div></div></div>`;
    el.querySelector('#goCheck').addEventListener('click', ()=>go('home'));
    return;
  }
  el.innerHTML = `
    <div class="wrap">
      <div class="toolbar"><div><h1 class="page-title">Dashboard</h1><p class="page-sub" style="margin:0;">Overview of every news check stored on the server.</p></div></div>
      <div class="grid3" style="grid-template-columns:repeat(4,1fr);">
        <div class="card stat-card"><div class="stat-top"><span class="stat-lab">Total Checked</span><span class="ic" style="background:#eef0ff;color:#4338ca;">${ICONS.total}</span></div><div class="stat-num">${s.total}</div></div>
        <div class="card stat-card"><div class="stat-top"><span class="stat-lab">Real News</span><span class="ic" style="background:var(--green-bg);color:var(--green);">${ICONS.real}</span></div><div class="stat-num" style="color:var(--green);">${s.real}</div></div>
        <div class="card stat-card"><div class="stat-top"><span class="stat-lab">Fake News</span><span class="ic" style="background:var(--red-bg);color:var(--red);">${ICONS.fake}</span></div><div class="stat-num" style="color:var(--red);">${s.fake}</div></div>
        <div class="card stat-card"><div class="stat-top"><span class="stat-lab">Model Accuracy</span><span class="ic" style="background:#eaf1ff;color:#2563eb;">${ICONS.acc}</span></div><div class="stat-num" style="color:#2563eb;">${s.modelAccuracy!=null ? s.modelAccuracy+'%' : '—'}</div><div class="small muted">Held-out test split Â· avg. confidence ${s.avgConfidence}%</div></div>
      </div>
      <div class="grid2" style="margin-top:16px;">
        <div class="card"><h3>Statistics Overview</h3><div style="height:260px;"><canvas id="lineChart"></canvas></div></div>
        <div class="card"><h3>News by Language</h3><div style="height:260px;"><canvas id="langChart"></canvas></div></div>
      </div>
    </div>`;
  if(charts.line) charts.line.destroy();
  if(charts.lang) charts.lang.destroy();
  const styles = getComputedStyle(document.documentElement);
  const gridColor = styles.getPropertyValue('--border').trim();
  const textColor = styles.getPropertyValue('--muted').trim();
  const labels = s.byDate.map(d=>fmtDateShort(d.date+'T12:00:00'));
  charts.line = new Chart(document.getElementById('lineChart'), {
    type:'line',
    data:{ labels, datasets:[
      {label:'Real News', data:s.byDate.map(d=>d.real), borderColor:'#16a34a', tension:.35, fill:false, pointRadius:3},
      {label:'Fake News', data:s.byDate.map(d=>d.fake), borderColor:'#dc2626', tension:.35, fill:false, pointRadius:3},
    ]},
    options:{ responsive:true, maintainAspectRatio:false,
      plugins:{legend:{position:'top', labels:{color:textColor, boxWidth:10, usePointStyle:true}}},
      scales:{ x:{grid:{color:gridColor}, ticks:{color:textColor}}, y:{beginAtZero:true, grid:{color:gridColor}, ticks:{color:textColor, precision:0}} } }
  });
  const langLabels = Object.keys(s.byLang);
  charts.lang = new Chart(document.getElementById('langChart'), {
    type:'doughnut',
    data:{ labels:langLabels, datasets:[{ data:langLabels.map(l=>s.byLang[l]), backgroundColor:['#f59e0b','#2563eb','#16a34a','#7c3aed'], borderWidth:0 }] },
    options:{ responsive:true, maintainAspectRatio:false, cutout:'62%',
      plugins:{ legend:{position:'bottom', labels:{color:textColor, boxWidth:10, usePointStyle:true}} } }
  });
}

/* ============================= HISTORY ============================= */
async function renderHistory(){
  const el = document.getElementById('view-history');
  let h;
  try{ h = await api(`/api/history?page=${historyPage}&per_page=${HISTORY_PAGE_SIZE}`); }
  catch(e){ el.innerHTML = `<div class="wrap"><div class="card empty">Could not load history. Is the backend running?</div></div>`; return; }
  if(!h.total){
    el.innerHTML = `<div class="wrap"><h1 class="page-title">History</h1><p class="page-sub">Every news item you've checked shows up here.</p>
      <div class="card empty"><div class="ic">${ICONS.inbox}</div><b>Nothing checked yet</b>
      <div style="margin-top:16px;"><button class="btn btn-primary" id="goCheck2">${ICONS.check}<span>Check News</span></button></div></div></div>`;
    el.querySelector('#goCheck2').addEventListener('click', ()=>go('home'));
    return;
  }
  if(historyPage > h.pages){ historyPage = h.pages; return renderHistory(); }
  let pagerBtns = '';
  for(let p=1;p<=h.pages;p++){ pagerBtns += `<button data-p="${p}" class="${p===h.page?'active':''}">${p}</button>`; }
  el.innerHTML = `
    <div class="wrap">
      <div class="toolbar"><div><h1 class="page-title">History</h1><p class="page-sub" style="margin:0;">${h.total} news item${h.total===1?'':'s'} checked so far.</p></div>
        <button class="btn btn-danger-outline" id="clearBtn">Clear history</button></div>
      <div class="card" style="padding:0;overflow:hidden;">
        <div class="tablewrap">
        <table>
          <thead><tr><th>ID</th><th>News</th><th>Language</th><th>Result</th><th>Score</th><th>Date</th></tr></thead>
          <tbody>
            ${h.items.map(c=>`
              <tr class="rowlink" data-id="${c.id}">
                <td class="mono small">${c.id}</td>
                <td>${esc((c.text||c.url||'').slice(0,60))}${(c.text||c.url||'').length>60?'â€¦':''}</td>
                <td>${c.lang}</td>
                <td><span class="badge ${c.verdict==='FAKE'?'fake':'real'}">${c.verdict==='FAKE'?'Fake':'Real'}</span></td>
                <td>${c.score}%</td>
                <td class="small muted">${fmtDateShort(c.createdAt)}</td>
              </tr>`).join('')}
          </tbody>
        </table>
        </div>
        <div style="padding:14px 20px;">
          <div class="pager">
            <button data-p="prev" ${h.page===1?'disabled':''}>&lt; Previous</button>
            ${pagerBtns}
            <button data-p="next" ${h.page===h.pages?'disabled':''}>Next &gt;</button>
          </div>
        </div>
      </div>
    </div>`;
  const items = h.items;
  el.querySelectorAll('tr.rowlink').forEach(tr=>tr.addEventListener('click', ()=>{
    const rec = items.find(c=>c.id===tr.dataset.id);
    if(rec){ renderResult(rec); go('result'); }
  }));
  el.querySelectorAll('.pager button').forEach(b=>b.addEventListener('click', ()=>{
    if(b.dataset.p==='prev') historyPage--; else if(b.dataset.p==='next') historyPage++; else historyPage=parseInt(b.dataset.p,10);
    renderHistory();
  }));
  el.querySelector('#clearBtn').addEventListener('click', async ()=>{
    if(!confirm('Delete all saved checks? This cannot be undone.')) return;
    try{ await api('/api/history',{method:'DELETE'}); historyPage=1; toast('History cleared.'); renderHistory(); }
    catch(e){ toast('Could not clear history.'); }
  });
}

/* ============================= ABOUT / CONTACT ============================= */
function renderAbout(){
  document.getElementById('view-about').innerHTML = `
    <div class="wrap" style="max-width:760px;">
      <h1 class="page-title">About this tool</h1>
      <p class="page-sub">How the detection works, in plain terms.</p>
      <div class="card static-card">
        <p>AI Fake News Detector analyzes news text or a news link in English, Hindi and Marathi and provides a FAKE or REAL prediction using a trained machine learning model.</p>

      <p><b>1. News Classification</b> The system analyzes the submitted news content and predicts whether it is likely to be FAKE or REAL, along with a confidence score.</p>

      <p><b>2. Source Analysis</b> When a news URL is provided, the system identifies the source domain and checks whether it is present in the project's recognized-source list. A source can be recognized, unassessed, or unknown when no URL is provided.</p>

      <p><b>3. Additional Verification</b> The system can also check available external fact-check results and applies built-in knowledge rules for selected well-known factual claims.</p>
        <p>Results are informational and meant to support your own judgement, not replace it — always verify anything important against an official or well-known source before acting on it or sharing it further.</p>
      </div>
    </div>`;
}
function renderContact(){
  document.getElementById('view-contact').innerHTML = `
    <div class="wrap" style="max-width:760px;">
      <h1 class="page-title">Contact</h1>
      <p class="page-sub">Questions, feedback, or a news item you want double-checked manually.</p>
      <div class="contact-grid">
        <div class="card"><h3>${ICONS.mail} Email</h3><p class="muted small" style="margin:0;">support@aifakenewsdetector.example</p></div>
        <div class="card"><h3>${ICONS.info} Report a mistake</h3><p class="muted small" style="margin:0;">Found a wrong verdict? Use Share Result on that check and send it our way.</p></div>
      </div>
    </div>`;
}


/* ============================= INIT ============================= */
document.getElementById('ic-shield-slot').innerHTML = ICONS.shield;
renderAbout(); renderContact(); renderHome();
renderNav();
go('home');


