<template>
  <div class="app">
    <!-- BG -->
    <div class="bg-glow"></div>

    <!-- NAV -->
    <nav class="nav">
      <div class="nav-inner">
        <div class="nav-brand">
          <img src="https://cdnbbsr.s3waas.gov.in/s3dcf6070a4ab7f3afbfd2809173e0824b/uploads/2024/10/20241009217618493.svg" alt="MoRTH" />
          <img src="https://cdnbbsr.s3waas.gov.in/s3dcf6070a4ab7f3afbfd2809173e0824b/uploads/2024/12/202412061445137587.svg" alt="NIC" />
          <span class="brand-name">mParivahan</span>
        </div>
        <span class="gov-tag">Govt. of India</span>
      </div>
    </nav>

    <!-- HERO -->
    <section class="hero">
      <div class="hero-inner">
        <div class="hero-badge">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>
          Official Government Application
        </div>
        <h1>mParivahan App</h1>
        <p>Access vehicle details, driving licence services, challan records and more — right from your Android device.</p>
        <a :href="shortLink" class="btn-hero">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
            <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>
            <polyline points="7 10 12 15 17 10"/>
            <line x1="12" y1="15" x2="12" y2="3"/>
          </svg>
          Download Now — Free
        </a>
        <p class="hero-note">Android 5.0+ &nbsp;·&nbsp; 100% Free &nbsp;·&nbsp; No account needed</p>
      </div>

      <!-- Phone mockup -->
      <div class="phone-wrap">
        <div class="phone">
          <div class="phone-screen">
            <img src="https://play-lh.googleusercontent.com/7Ddr_L-nxrzbMjoXVhGpO9MMdImXfvg5UAjZv_9VjjZZ4L9qdMzwXZZbwbfan-WUWD0=w5120-h2880-rw" alt="App" />
          </div>
        </div>
      </div>
    </section>

    <!-- FEATURES -->
    <section class="features">
      <div class="container">
        <h2 class="section-title">Everything in one app</h2>
        <div class="features-grid">
          <div v-for="f in features" :key="f.title" class="feature-card">
            <div class="f-icon">{{ f.icon }}</div>
            <h3>{{ f.title }}</h3>
            <p>{{ f.desc }}</p>
          </div>
        </div>
      </div>
    </section>

    <!-- DOWNLOAD CTA -->
    <section class="cta">
      <div class="container cta-inner">
        <div>
          <h2>Ready to get started?</h2>
          <p>Download the mParivahan app and manage your vehicle documents digitally.</p>
        </div>
        <a :href="shortLink" class="btn-cta">
          Download APK
        </a>
      </div>
    </section>

    <!-- FOOTER -->
    <footer class="footer">
      <div class="container">
        <p>© 2026 mParivahan · Ministry of Road Transport & Highways, Govt. of India</p>
        <p class="footer-sub">Android users only &nbsp;·&nbsp; Secure download</p>
      </div>
    </footer>
  </div>
</template>

<script setup>
const shortLink = 'https://mparivahaan.s.gy/grqHZR'

const features = [
  { icon: '🚗', title: 'Vehicle Information', desc: 'View RC, registration details, insurance validity and more for any vehicle.' },
  { icon: '📋', title: 'Challan Records', desc: 'Track pending challans with photographic evidence, pay online and download receipts.' },
  { icon: '🪪', title: 'Driving Licence', desc: 'Apply for learner and driving licences online directly from your mobile.' },
  { icon: '⚖️', title: 'Dispute Violations', desc: 'Raise appeals against incorrect challans directly through the app.' },
  { icon: '🔒', title: 'DigiLocker Integration', desc: 'Access DL & RC documents securely linked with your DigiLocker account.' },
  { icon: '📍', title: 'Real-time Updates', desc: 'Get instant notifications on challan status and vehicle-related alerts.' },
]
</script>

<style scoped>
.app { min-height: 100vh; background: #060c1a; color: #fff; }

.bg-glow {
  position: fixed; inset: 0; z-index: 0; pointer-events: none;
  background:
    radial-gradient(ellipse 70% 50% at 10% 5%, rgba(11,79,163,0.4) 0%, transparent 55%),
    radial-gradient(ellipse 50% 40% at 90% 90%, rgba(6,182,212,0.18) 0%, transparent 50%);
}

/* NAV */
.nav {
  position: relative; z-index: 10;
  border-bottom: 1px solid rgba(255,255,255,0.07);
  backdrop-filter: blur(20px);
  background: rgba(6,12,26,0.7);
  padding: 14px 0;
  position: sticky; top: 0;
}
.nav-inner {
  max-width: 1100px; margin: 0 auto; padding: 0 20px;
  display: flex; align-items: center; justify-content: space-between;
}
.nav-brand { display: flex; align-items: center; gap: 12px; }
.nav-brand img { height: 26px; filter: brightness(0) invert(1); opacity: 0.9; }
.brand-name { font-weight: 700; font-size: 17px; letter-spacing: -0.3px; }
.gov-tag {
  font-size: 11px; color: rgba(255,255,255,0.45);
  border: 1px solid rgba(255,255,255,0.12); padding: 4px 10px; border-radius: 99px;
}

/* HERO */
.hero {
  position: relative; z-index: 1;
  max-width: 1100px; margin: 0 auto; padding: 70px 20px 60px;
  display: flex; align-items: center; gap: 60px; flex-wrap: wrap;
}
.hero-inner { flex: 1; min-width: 280px; }
.hero-badge {
  display: inline-flex; align-items: center; gap: 6px;
  background: rgba(16,185,129,0.1); border: 1px solid rgba(16,185,129,0.22);
  border-radius: 99px; padding: 5px 14px;
  font-size: 12px; color: #6ee7b7; font-weight: 600;
  margin-bottom: 20px;
}
.hero h1 {
  font-size: clamp(36px, 6vw, 58px); font-weight: 800;
  letter-spacing: -1.5px; line-height: 1.08; margin-bottom: 18px;
  background: linear-gradient(135deg, #fff 30%, #93c5fd);
  -webkit-background-clip: text; -webkit-text-fill-color: transparent;
}
.hero p {
  font-size: 17px; color: rgba(255,255,255,0.6); line-height: 1.65;
  margin-bottom: 32px; max-width: 460px;
}
.btn-hero {
  display: inline-flex; align-items: center; gap: 10px;
  padding: 16px 30px;
  background: linear-gradient(135deg, #1d4ed8, #0ea5e9);
  color: #fff; border-radius: 14px; text-decoration: none;
  font-weight: 700; font-size: 16px;
  box-shadow: 0 8px 32px rgba(29,78,216,0.55), 0 0 0 1px rgba(255,255,255,0.08) inset;
  transition: transform 0.18s, box-shadow 0.18s;
  margin-bottom: 14px;
}
.btn-hero:hover { transform: translateY(-2px); box-shadow: 0 14px 44px rgba(29,78,216,0.7); }
.hero-note { font-size: 12px; color: rgba(255,255,255,0.35); }

/* PHONE MOCKUP */
.phone-wrap { flex: 0 0 auto; }
.phone {
  width: 200px; height: 400px; border-radius: 32px;
  border: 2px solid rgba(255,255,255,0.12);
  background: #111827; overflow: hidden;
  box-shadow: 0 30px 60px rgba(0,0,0,0.5), 0 0 0 1px rgba(255,255,255,0.04);
}
.phone-screen { width: 100%; height: 100%; overflow: hidden; }
.phone-screen img { width: 100%; height: 100%; object-fit: cover; opacity: 0.9; }

/* FEATURES */
.features { position: relative; z-index: 1; padding: 60px 0; }
.container { max-width: 1100px; margin: 0 auto; padding: 0 20px; }
.section-title {
  text-align: center; font-size: 32px; font-weight: 800;
  letter-spacing: -0.8px; margin-bottom: 40px;
}
.features-grid {
  display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 18px;
}
.feature-card {
  background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.07);
  border-radius: 18px; padding: 24px;
  transition: background 0.2s, border-color 0.2s;
}
.feature-card:hover { background: rgba(255,255,255,0.055); border-color: rgba(255,255,255,0.12); }
.f-icon { font-size: 28px; margin-bottom: 12px; }
.feature-card h3 { font-size: 16px; font-weight: 700; margin-bottom: 8px; }
.feature-card p { font-size: 13.5px; color: rgba(255,255,255,0.5); line-height: 1.6; }

/* CTA */
.cta { position: relative; z-index: 1; padding: 50px 0; }
.cta-inner {
  display: flex; align-items: center; justify-content: space-between;
  gap: 24px; flex-wrap: wrap;
  background: rgba(29,78,216,0.12); border: 1px solid rgba(29,78,216,0.25);
  border-radius: 22px; padding: 36px;
}
.cta h2 { font-size: 26px; font-weight: 800; margin-bottom: 8px; }
.cta p { font-size: 15px; color: rgba(255,255,255,0.6); }
.btn-cta {
  flex-shrink: 0; padding: 14px 28px;
  background: linear-gradient(135deg, #1d4ed8, #0ea5e9);
  color: #fff; border-radius: 12px; text-decoration: none;
  font-weight: 700; font-size: 15px;
  box-shadow: 0 6px 24px rgba(29,78,216,0.5);
  white-space: nowrap; transition: transform 0.15s;
}
.btn-cta:hover { transform: translateY(-2px); }

/* FOOTER */
.footer { position: relative; z-index: 1; padding: 32px 0; text-align: center; }
.footer p { font-size: 13px; color: rgba(255,255,255,0.35); }
.footer-sub { margin-top: 6px; font-size: 12px; }
</style>
