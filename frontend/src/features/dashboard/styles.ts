const css = `
body { margin: 0; min-width: 320px; background: #050505; color: #f5f8fb; font-family: Inter, Arial, sans-serif; }
* { box-sizing: border-box; }
button, input, select, textarea { font: inherit; }
.dashboard-shell { min-height: 100vh; background: radial-gradient(ellipse at 50% -20%, #007ba766, transparent 42%), radial-gradient(ellipse at 100% 45%, #ff2d7533, transparent 34%), #050505; }
.topbar { display:flex; justify-content:space-between; align-items:center; padding:25px 5%; border-bottom:1px solid #08b9ed33; background:#080c16dd; }
.brand { display:inline-flex; align-items:center; gap:10px; color:#edf1fb; font-weight:700; letter-spacing:.19em; }
.brand-mark { display:grid; place-items:center; width:25px; height:25px; border:1px solid currentColor; border-radius:50%; }
.main-nav { display:flex; gap:28px; color:#78869d; font-size:12px; }
.main-nav a { color:inherit; text-decoration:none; transition:color .2s ease; }
.main-nav a:hover { color:#fff; }
.nav-active { color:#fff; }
.account-menu { display:flex; align-items:center; gap:10px; }
.account-email { max-width:180px; overflow:hidden; text-overflow:ellipsis; color:#8c9ab1; font-size:11px; }
.avatar,.application-avatar { display:grid; place-items:center; border-radius:50%; color:#fff; background:linear-gradient(135deg,#007ba7,#ff2d75); font-size:10px; font-weight:700; }
.avatar { width:30px; height:30px; }
.ghost-button,.secondary-button { border:1px solid #ffffff22; border-radius:8px; padding:9px 15px; background:#ffffff0a; color:#d7e2ea; cursor:pointer; }
.dashboard { max-width:1600px; margin:auto; padding:78px 5% 110px; }
.welcome-row { display:flex; justify-content:space-between; align-items:end; gap:30px; margin-bottom:42px; }
.eyebrow { color:#08b9ed; font-size:10px; font-weight:700; letter-spacing:.22em; }
.dashboard h1 { max-width:850px; margin:10px 0 18px; font-size:clamp(56px,7vw,102px); line-height:.91; font-weight:500; letter-spacing:-.075em; }
.dashboard h1 em { color:#ff5c96; font-family:Georgia, serif; font-weight:500; }
.dashboard-copy,.panel-copy,.section-subtitle { color:#9caabd; line-height:1.8; }
.workspace-badge { padding:12px 15px; border:1px solid #ffffff14; border-radius:10px; color:#9aa9bf; background:#ffffff08; font-size:11px; }
.stat-grid { display:grid; grid-template-columns:repeat(4,1fr); gap:12px; }
.stat-card,.marketplace-panel { border:1px solid #08b9ed2b; border-radius:16px; background:linear-gradient(145deg,#111820ee,#08090aec); box-shadow:0 18px 50px #0007,inset 0 1px #ffffff12; }
.stat-card { position:relative; min-height:160px; padding:25px; }
.stat-card span,.stat-card small { display:block; color:#8996ae; font-size:12px; }
.stat-card strong { display:block; margin:19px 0 7px; font-size:30px; }
.metric-icon { position:absolute!important; top:22px; right:24px; color:#ff5c96!important; font-size:18px!important; }
.marketplace-panel { position:relative; overflow:hidden; margin-top:28px; padding:32px; }
.portal-grid { display:grid; grid-template-columns:1.35fr 1fr; gap:14px; }
.portal-grid .marketplace-panel { margin-top:0; }
.panel-heading,.section-heading { display:flex; justify-content:space-between; align-items:end; gap:20px; }
.panel-heading h2,.portal-grid h2,.marketplace-panel>h2 { max-width:580px; margin:0; color:#f1f4fb; font-size:25px; }
.completion-ring { display:grid; place-items:center; width:54px; height:54px; border:3px solid #ff2d75; border-left-color:#ffffff1a; border-radius:50%; font-size:12px; }
.progress-bar { height:5px; margin:25px 0 15px; border-radius:8px; background:#ffffff12; }
.progress-bar span { display:block; width:72%; height:100%; border-radius:8px; background:linear-gradient(90deg,#08b9ed,#ff2d75); }
.profile-checks,.recruiter-actions { display:flex; flex-wrap:wrap; gap:10px; margin:19px 0; color:#89e1bd; font-size:11px; }
.next-panel,.hiring-health { background:linear-gradient(145deg,#1c101b,#0c0e16)!important; }
.mini-feature { display:flex; gap:12px; margin:25px 0; color:#ff5c96; }
.mini-feature strong,.mini-feature small { display:block; }
.section-heading { min-width:0; margin-bottom:22px; }
.search-wrap { display:flex; min-width:0; flex:0 1 340px; align-items:center; gap:10px; color:#9bdff3; }
.search-wrap > span { flex:0 0 auto; font-size:20px; line-height:1; }
.job-search { width:100%; min-width:0; max-width:340px; padding:14px 15px; border:1px solid #ffffff22; border-radius:9px; outline:none; background:#08090a; color:#fff; }
.job-search::placeholder { color:#718097; opacity:1; }
.job-search:focus { border-color:#08b9ed; box-shadow:0 0 0 3px #08b9ed1f; }
.job-grid { display:grid; grid-template-columns:repeat(4,minmax(0,1fr)); gap:14px; }
.job-card { padding:20px; border:1px solid #08b9ed24; border-radius:12px; background:#ffffff08; }
.job-card-top { display:flex; justify-content:space-between; gap:12px; }
.job-company { color:#ff5c96; font-size:12px; font-weight:700; }
.job-type,.status-pill { padding:5px 8px; border-radius:999px; color:#9bdff3; background:#007ba733; font-size:10px; }
.job-card h3 { min-height:48px; margin:14px 0 8px; font-size:20px; }
.job-card p { color:#8996ae; font-size:13px; }
.job-description { display:-webkit-box!important; min-height:42px!important; overflow:hidden; -webkit-box-orient:vertical; -webkit-line-clamp:2; font-size:12px!important; }
.skill-list { display:flex; flex-wrap:wrap; gap:6px; margin-top:18px; }
.skill-list span { padding:5px 8px; border-radius:5px; color:#86dcf8; background:#007ba733; font-size:11px; }
.apply-button { width:100%; margin-top:18px; }
.primary-button { display:inline-flex; justify-content:space-between; align-items:center; gap:20px; border:0; border-radius:9px; padding:15px 18px; color:#fff; background:linear-gradient(110deg,#007ba7,#ff2d75); font-weight:700; cursor:pointer; }
.workflow-message { color:#ff5c96; }
.post-job-form { display:grid; grid-template-columns:repeat(4,1fr); gap:16px; }
.post-job-form label { display:grid; min-width:0; gap:9px; color:#b8c5d2; font-size:11px; font-weight:700; letter-spacing:.04em; }
.post-job-form input,.post-job-form select,.post-job-form textarea { width:100%; min-width:0; border:1px solid #26303b; border-radius:7px; outline:none; padding:14px 15px; color:#f5f8fb; background:#080b0f; transition:border-color .2s,box-shadow .2s; }
.post-job-form input::placeholder,.post-job-form textarea::placeholder { color:#667587; opacity:1; }
.post-job-form input:focus,.post-job-form select:focus,.post-job-form textarea:focus { border-color:#08b9ed; box-shadow:0 0 0 3px #08b9ed1f; }
.post-job-form textarea { min-height:112px; resize:vertical; line-height:1.5; }
.post-job-description { grid-column:span 3; }
.post-job-submit { width:100%; min-height:112px; align-self:end; }
.pipeline-strip { display:grid; grid-template-columns:repeat(5,1fr); gap:1px; overflow:hidden; background:#ffffff12; }
.pipeline-strip div { padding:17px; background:#080d13; }
.pipeline-strip strong,.pipeline-strip span { display:block; }
.pipeline-strip span { margin-top:4px; color:#7f8da4; font-size:10px; }
.application-list { display:grid; gap:10px; margin-top:18px; }
.application-row { display:grid; grid-template-columns:34px 1fr auto auto; align-items:center; gap:14px; padding:16px; border:1px solid #08b9ed24; border-radius:10px; background:#ffffff08; }
.application-avatar { width:34px; height:34px; }
.application-row p { margin:4px 0; color:#8996ae; font-size:12px; }
.application-row small { color:#718097; font-size:10px; }
.pipeline-panel>.applications-panel { margin:28px -32px -32px; border:0; border-top:1px solid #08b9ed22; border-radius:0; }
.health-score { margin:20px 0 8px; color:#54e6a5; font-size:30px; }
@media(max-width:1050px){.job-grid{grid-template-columns:repeat(2,1fr)}}
@media(max-width:900px){.main-nav{display:none}.welcome-row{align-items:flex-start;flex-direction:column}.stat-grid{grid-template-columns:repeat(2,1fr)}.portal-grid{grid-template-columns:1fr}.post-job-form{grid-template-columns:repeat(2,1fr)}.post-job-description{grid-column:span 2}.post-job-submit{min-height:58px}.section-heading{align-items:flex-start;flex-direction:column}.search-wrap{width:100%;flex-basis:auto}.job-search{max-width:none}}
@media(max-width:600px){.account-email{display:none}.topbar{padding:20px 24px}.dashboard{padding:55px 24px 80px}.dashboard h1{font-size:55px}.job-grid{grid-template-columns:1fr}.post-job-form{grid-template-columns:1fr}.post-job-description{grid-column:auto}.application-row{grid-template-columns:34px 1fr}.application-row .status-pill,.application-row select{grid-column:2}.form-row{grid-template-columns:1fr}}
`;
const node = document.createElement("style"); node.textContent = css; document.head.appendChild(node);
