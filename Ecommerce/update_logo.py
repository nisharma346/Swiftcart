from pathlib import Path

svg_path = Path('c:\\Users\\NISHA\\Desktop\\E-commerce\\Ecommerce\\static\\images\\swiftcart-logo.svg')
svg_path.write_text(
'''<svg width="420" height="120" viewBox="0 0 420 120" fill="none" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="logoGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#2563EB"/>
      <stop offset="100%" stop-color="#9333EA"/>
    </linearGradient>
    <linearGradient id="textGrad" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#2563EB"/>
      <stop offset="100%" stop-color="#9333EA"/>
    </linearGradient>
  </defs>

  <rect x="18" y="24" width="74" height="70" rx="22" fill="#EFF6FF"/>
  <path d="M30 36H70L84 70H42L30 36Z" fill="url(#logoGrad)"/>
  <circle cx="42" cy="82" r="6" fill="#2563EB"/>
  <circle cx="70" cy="82" r="6" fill="#2563EB"/>
  <path d="M34 48H80" stroke="#2563EB" stroke-width="6" stroke-linecap="round"/>
  <path d="M42 54H74" stroke="#2563EB" stroke-width="4" stroke-linecap="round" opacity="0.85"/>

  <path d="M116 58H334" stroke="#E0E7FF" stroke-width="18" stroke-linecap="round" opacity="0.85"/>
  <path d="M124 40C158 28 194 34 216 58C238 82 274 92 310 78C346 64 378 50 402 58" stroke="#9333EA" stroke-width="10" stroke-linecap="round" opacity="0.9"/>
  <path d="M132 50C166 40 202 46 224 70C246 94 282 104 318 92" stroke="#2563EB" stroke-width="6" stroke-linecap="round" opacity="0.8"/>

  <text x="118" y="78" fill="url(#textGrad)" font-family="Segoe UI, Arial, sans-serif" font-size="44" font-weight="800" letter-spacing="0.2">Swift</text>
  <text x="244" y="78" fill="#111827" font-family="Segoe UI, Arial, sans-serif" font-size="44" font-weight="800">Cart</text>
</svg>
''', encoding='utf-8')
print('updated')
