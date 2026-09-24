<style>
  .profile-shell {
    max-width: 1200px;
    margin: 20px auto 30px;
    font-family: "Segoe UI", Arial, sans-serif;
    color: #e5edf8;
  }

  .section-panel {
    background: linear-gradient(180deg, rgba(11,19,32,0.95), rgba(8,17,28,0.98));
    border: 1px solid #223a4d;
    border-radius: 18px;
    box-shadow: 0 0 0 1px rgba(41,73,96,0.4), 0 18px 34px rgba(2,8,16,0.35);
    margin: 24px auto;
    overflow: hidden;
  }

  .panel-header {
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 16px 20px;
    background: rgba(12,21,31,0.9);
    border-bottom: 1px solid rgba(75,104,128,0.45);
  }

  .traffic-dot {
    width: 12px;
    height: 12px;
    border-radius: 50%;
    display: inline-block;
  }

  .traffic-dot.red { background: #f87171; }
  .traffic-dot.yellow { background: #fbbf24; }
  .traffic-dot.green { background: #4ade80; }

  .panel-title {
    font-family: "SFMono-Regular", Consolas, monospace;
    color: #9db0c6;
    font-size: 15px;
    letter-spacing: 0.03em;
  }

  .hero-body {
    padding: 32px 34px 26px;
    background:
      linear-gradient(180deg, rgba(9,20,30,0.7), rgba(8,17,27,0.78)),
      linear-gradient(90deg, rgba(59,130,246,0.08), rgba(45,212,191,0.04));
    border-top: 1px solid rgba(92,135,165,0.3);
  }

  .hero-grid {
    display: grid;
    grid-template-columns: 1.2fr 0.5fr;
    gap: 22px;
    align-items: center;
  }

  .eyebrow {
    margin: 0 0 18px;
    font-family: "SFMono-Regular", Consolas, monospace;
    font-size: 14px;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: #5de7c9;
  }

  .hero-title {
    margin: 0;
    font-size: 56px;
    line-height: 1.04;
    font-weight: 800;
    letter-spacing: -0.04em;
    color: #f6f7fb;
  }

  .hero-title .accent {
    color: #7dd3fc;
    display: inline-block;
    font-size: 18px;
    letter-spacing: 0.18em;
    margin-bottom: 12px;
    text-transform: uppercase;
    font-weight: 700;
    font-family: "SFMono-Regular", Consolas, monospace;
  }

  .hero-badge {
    display: inline-flex;
    align-items: center;
    gap: 10px;
    margin-top: 28px;
    padding: 8px 14px 8px 10px;
    border: 1px solid rgba(52,211,153,0.45);
    border-radius: 10px;
    background: rgba(16,33,31,0.75);
    color: #9ae6b4;
    font-family: "SFMono-Regular", Consolas, monospace;
    font-size: 13px;
    letter-spacing: 0.08em;
    text-transform: uppercase;
  }

  .hero-badge::before {
    content: "";
    width: 10px;
    height: 10px;
    border-radius: 50%;
    background: #34d399;
    box-shadow: 0 0 12px rgba(52,211,153,0.9);
  }

  .status-ring {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 160px;
    height: 160px;
    border-radius: 50%;
    margin: auto;
    border: 2px solid rgba(94,167,255,0.85);
    background: radial-gradient(circle at center, rgba(7,20,31,0.8), rgba(8,16,26,0.6));
    box-shadow: inset 0 0 20px rgba(86,200,255,0.12), 0 0 0 1px rgba(125,211,252,0.2);
    position: relative;
  }

  .status-ring::before {
    content: "";
    position: absolute;
    inset: 12px;
    border: 1px solid rgba(125,211,252,0.6);
    border-radius: 50%;
  }

  .status-ring::after {
    content: "";
    width: 34px;
    height: 34px;
    border-left: 3px solid #dfeaf5;
    border-bottom: 3px solid #dfeaf5;
    transform: rotate(45deg) translateY(-2px);
    display: block;
    opacity: 0.9;
  }

  .section-title {
    margin: 0 0 14px;
    font-family: "SFMono-Regular", Consolas, monospace;
    font-size: 15px;
    letter-spacing: 0.12em;
    text-transform: lowercase;
    color: #dfeaf5;
  }

  .section-subtitle {
    margin: 0 0 18px;
    color: #8aa5bb;
    font-family: "SFMono-Regular", Consolas, monospace;
    font-size: 12px;
  }

  .stack-grid,
  .project-grid,
  .focus-grid,
  .connect-grid {
    display: grid;
    gap: 18px;
  }

  .stack-grid {
    grid-template-columns: repeat(3, minmax(0, 1fr));
  }

  .stack-card,
  .focus-card,
  .project-card,
  .info-card {
    background: rgba(10,18,29,0.9);
    border: 1px solid #233a4c;
    border-radius: 16px;
    padding: 18px 18px 16px;
    box-shadow: inset 0 1px 0 rgba(157,177,196,0.08);
  }

  .stack-card {
    min-height: 170px;
  }

  .card-label {
    margin: 0 0 10px;
    font-family: "SFMono-Regular", Consolas, monospace;
    font-size: 12px;
    letter-spacing: 0.14em;
    text-transform: uppercase;
  }

  .stack-card .card-label {
    padding-bottom: 8px;
    border-bottom: 1px solid rgba(110,145,170,0.2);
  }

  .stack-list {
    margin: 10px 0 0;
    padding: 0;
    list-style: none;
    font-family: "SFMono-Regular", Consolas, monospace;
    color: #dfeaf5;
    font-size: 13px;
    line-height: 1.9;
  }

  .project-grid {
    grid-template-columns: repeat(3, minmax(0, 1fr));
  }

  .project-card {
    min-height: 210px;
    position: relative;
    overflow: hidden;
    padding-top: 20px;
  }

  .project-card::before {
    content: "";
    position: absolute;
    left: 18px;
    top: 18px;
    width: 54px;
    height: 2px;
    background: currentColor;
    opacity: 0.9;
  }

  .project-card .title {
    margin: 18px 0 14px;
    font-size: 28px;
    font-weight: 800;
    line-height: 1.15;
    color: #f8fafc;
  }

  .project-card .meta {
    margin: 0;
    color: #d4ddea;
    font-family: "SFMono-Regular", Consolas, monospace;
    font-size: 12px;
    line-height: 1.75;
  }

  .project-card .link {
    display: inline-block;
    margin-top: 18px;
    font-family: "SFMono-Regular", Consolas, monospace;
    color: currentColor;
    text-decoration: none;
    font-size: 13px;
    letter-spacing: 0.08em;
    text-transform: uppercase;
  }

  .focus-grid {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }

  .focus-card {
    padding: 20px 18px 18px;
  }

  .focus-card .title {
    margin: 0 0 14px;
    font-family: "SFMono-Regular", Consolas, monospace;
    font-size: 12px;
    letter-spacing: 0.12em;
    text-transform: uppercase;
  }

  .focus-list {
    margin: 0;
    padding: 0 0 0 18px;
    color: #dfeaf5;
    font-family: "SFMono-Regular", Consolas, monospace;
    line-height: 1.8;
    font-size: 13px;
  }

  .connect-grid {
    grid-template-columns: repeat(2, minmax(0, 1fr));
    align-items: center;
  }

  .info-card img {
    width: 100%;
    display: block;
    border-radius: 12px;
  }

  .profile-note {
    margin: 0;
    text-align: center;
    color: #a9bfd0;
    font-family: "SFMono-Regular", Consolas, monospace;
    font-size: 12px;
    letter-spacing: 0.12em;
    text-transform: uppercase;
  }

  @media (max-width: 980px) {
    .hero-grid,
    .stack-grid,
    .project-grid,
    .focus-grid,
    .connect-grid {
      grid-template-columns: 1fr;
    }

    .hero-title {
      font-size: 42px;
    }
  }
</style>

<div class="profile-shell">
  <div class="section-panel">
    <div class="panel-header">
      <span class="traffic-dot red"></span>
      <span class="traffic-dot yellow"></span>
      <span class="traffic-dot green"></span>
      <span class="panel-title">simon@github ~/profile --build</span>
    </div>

    <div class="hero-body">
      <div class="hero-grid">
        <div>
          <p class="eyebrow">SIMON LEO ALEXANDER</p>
          <h1 class="hero-title"><span class="accent">AI ×</span><br>FULL STACK DEVELOPER</h1>

          <div class="hero-badge">Available for software development opportunities</div>
        </div>

        <div class="status-ring" aria-label="status active"></div>
      </div>
    </div>
  </div>

  <div class="section-panel">
    <div class="panel-header">
      <span class="traffic-dot red"></span>
      <span class="traffic-dot yellow"></span>
      <span class="traffic-dot green"></span>
      <span class="panel-title">whoami</span>
    </div>

    <div class="hero-body" style="padding-top: 18px; padding-bottom: 20px;">
      <div class="connect-grid">
        <div class="info-card">
          <img src="./assets/info-card.svg" alt="Simon profile information card" />
        </div>
        <div class="stack-card" style="min-height: auto;">
          <p class="card-label" style="color:#7dd3fc;">PROFILE</p>
          <p style="margin:0 0 10px; font-size:18px; font-weight:700; color:#f8fafc;">AI &amp; Full Stack Developer</p>
          <p style="margin:0; color:#dfeaf5; line-height:1.7;">
            Building practical systems that connect intelligent models, scalable web platforms, and real-time vision workflows.
          </p>
          <p style="margin:12px 0 0; color:#cddbf0; line-height:1.7;">
            Final-year Information Science &amp; Engineering student focused on AI-powered software, full-stack engineering, and automation.
          </p>
        </div>
      </div>
    </div>
  </div>

  <div class="section-panel">
    <div class="panel-header">
      <span class="traffic-dot red"></span>
      <span class="traffic-dot yellow"></span>
      <span class="traffic-dot green"></span>
      <span class="panel-title">tech --stack</span>
    </div>

    <div class="hero-body" style="padding-top: 24px;">
      <div class="stack-grid">
        <div class="stack-card" style="border-color: rgba(94,167,255,0.8);">
          <p class="card-label" style="color:#7dd3fc;">01 / FRONTEND</p>
          <ul class="stack-list">
            <li>React</li>
            <li>Next.js</li>
            <li>JavaScript</li>
            <li>Tailwind CSS</li>
          </ul>
        </div>

        <div class="stack-card" style="border-color: rgba(192,132,252,0.8);">
          <p class="card-label" style="color:#c084fc;">02 / BACKEND</p>
          <ul class="stack-list">
            <li>Node.js</li>
            <li>Express</li>
            <li>REST APIs</li>
            <li>Python</li>
          </ul>
        </div>

        <div class="stack-card" style="border-color: rgba(52,211,153,0.8);">
          <p class="card-label" style="color:#34d399;">03 / AI / ML</p>
          <ul class="stack-list">
            <li>Python</li>
            <li>TensorFlow</li>
            <li>PyTorch</li>
            <li>YOLO · OpenCV</li>
          </ul>
        </div>

        <div class="stack-card" style="border-color: rgba(251,191,36,0.8);">
          <p class="card-label" style="color:#fbbf24;">04 / DATABASE</p>
          <ul class="stack-list">
            <li>MongoDB</li>
            <li>PostgreSQL</li>
            <li>SQL</li>
          </ul>
        </div>

        <div class="stack-card" style="border-color: rgba(244,114,182,0.8);">
          <p class="card-label" style="color:#f472b6;">05 / DEVOPS</p>
          <ul class="stack-list">
            <li>Git</li>
            <li>GitHub</li>
            <li>AWS</li>
            <li>Linux · Docker</li>
          </ul>
        </div>

        <div class="stack-card" style="border-color: rgba(45,212,191,0.8);">
          <p class="card-label" style="color:#2dd4bf;">06 / VISION</p>
          <ul class="stack-list">
            <li>YOLO</li>
            <li>OpenCV</li>
            <li>PyAV</li>
            <li>TensorRT</li>
          </ul>
        </div>
      </div>
    </div>
  </div>

  <div class="section-panel">
    <div class="panel-header">
      <span class="traffic-dot red"></span>
      <span class="traffic-dot yellow"></span>
      <span class="traffic-dot green"></span>
      <span class="panel-title">what_i_build</span>
    </div>

    <div class="hero-body" style="padding-top: 24px;">
      <div class="project-grid">
        <div class="project-card" style="border-color: rgba(125,211,252,0.9); color: #7dd3fc;">
          <div class="title">AI / Machine Learning</div>
          <p class="meta">Python • TensorFlow • PyTorch • YOLO • Agentic AI</p>
          <a class="link" href="https://github.com/SimonLeo28" target="_blank" rel="noreferrer">View</a>
        </div>

        <div class="project-card" style="border-color: rgba(192,132,252,0.9); color: #c084fc;">
          <div class="title">Full Stack Systems</div>
          <p class="meta">React • Next.js • Node.js • Express • MongoDB</p>
          <a class="link" href="https://github.com/SimonLeo28" target="_blank" rel="noreferrer">View</a>
        </div>

        <div class="project-card" style="border-color: rgba(52,211,153,0.9); color: #34d399;">
          <div class="title">Computer Vision</div>
          <p class="meta">YOLO • OpenCV • PyAV • TensorRT • Flask • Electron</p>
          <a class="link" href="https://github.com/SimonLeo28" target="_blank" rel="noreferrer">View</a>
        </div>
      </div>
    </div>
  </div>

  <div class="section-panel">
    <div class="panel-header">
      <span class="traffic-dot red"></span>
      <span class="traffic-dot yellow"></span>
      <span class="traffic-dot green"></span>
      <span class="panel-title">featured_projects</span>
    </div>

    <div class="hero-body" style="padding-top: 22px;">
      <img src="./assets/projects-showcase.svg" alt="Featured project showcase" style="width:100%; display:block; border-radius: 14px; border: 1px solid rgba(80,116,146,0.35);" />
    </div>
  </div>

  <div class="section-panel">
    <div class="panel-header">
      <span class="traffic-dot red"></span>
      <span class="traffic-dot yellow"></span>
      <span class="traffic-dot green"></span>
      <span class="panel-title">architecture</span>
    </div>

    <div class="hero-body" style="padding-top: 20px;">
      <img src="./assets/stack-architecture.svg" alt="AI to frontend architecture diagram" style="width:100%; display:block; border-radius: 14px; border: 1px solid rgba(80,116,146,0.35);" />
    </div>
  </div>

  <div class="section-panel">
    <div class="panel-header">
      <span class="traffic-dot red"></span>
      <span class="traffic-dot yellow"></span>
      <span class="traffic-dot green"></span>
      <span class="panel-title">current_focus</span>
    </div>

    <div class="hero-body" style="padding-top: 20px; padding-bottom: 22px;">
      <div class="focus-grid">
        <div class="focus-card">
          <p class="title" style="color:#7dd3fc;">Currently Building</p>
          <ul class="focus-list">
            <li>AI-powered applications</li>
            <li>Full-stack web platforms</li>
            <li>Computer vision systems</li>
            <li>Real-time data systems</li>
            <li>Automation workflows</li>
          </ul>
        </div>
        <div class="focus-card">
          <p class="title" style="color:#34d399;">Currently Learning</p>
          <ul class="focus-list">
            <li>Advanced AI/ML</li>
            <li>Agentic AI</li>
            <li>Cloud deployment</li>
            <li>Scalable backend architecture</li>
          </ul>
        </div>
      </div>
    </div>
  </div>

  <div class="section-panel">
    <div class="panel-header">
      <span class="traffic-dot red"></span>
      <span class="traffic-dot yellow"></span>
      <span class="traffic-dot green"></span>
      <span class="panel-title">system_activity</span>
    </div>

    <div class="hero-body" style="padding-top: 20px;">
      <img src="./assets/contrib-heatmap.svg" alt="Contribution activity heatmap" style="width:100%; display:block; border-radius: 14px; border: 1px solid rgba(80,116,146,0.35);" />
    </div>
  </div>

  <div class="section-panel">
    <div class="panel-header">
      <span class="traffic-dot red"></span>
      <span class="traffic-dot yellow"></span>
      <span class="traffic-dot green"></span>
      <span class="panel-title">connect</span>
    </div>

    <div class="hero-body" style="padding-top: 20px; padding-bottom: 24px;">
      <div style="display:flex; justify-content:center; flex-wrap:wrap; gap:16px; margin-bottom:18px; font-family:'SFMono-Regular', Consolas, monospace; font-size:13px;">
        <a href="https://github.com/SimonLeo28" style="color:#7dd3fc; text-decoration:none;">GitHub</a>
        <span style="color:#7c8fa5;">•</span>
        <a href="https://github.com/SimonLeo28/SimonLeo28" style="color:#7dd3fc; text-decoration:none;">Portfolio</a>
        <span style="color:#7c8fa5;">•</span>
        <span style="color:#dfeaf5;">LinkedIn: not shared publicly</span>
        <span style="color:#7c8fa5;">•</span>
        <span style="color:#dfeaf5;">Email: not shared publicly</span>
      </div>

      <p class="profile-note" style="color:#7dd3fc; margin-bottom: 10px;">Let's build something</p>
      <p class="profile-note">AI • Full Stack Development • Computer Vision • Software Engineering</p>
    </div>
  </div>

  <p class="profile-note" style="margin-top: 14px;">Bengaluru, Karnataka, India</p>
</div>
