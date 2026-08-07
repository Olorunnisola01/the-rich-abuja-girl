#!/usr/bin/env python3
"""Build self-contained storyboard gallery for 'The rich Abuja girl'

Features:
- Character References section (Tiwa, Tunde, Chief Adebayo Adenuga, Bisi, Segun Lawson)
- 5 Acts with scene headers, location tags, and voiceover text blocks
- Responsive 16:9 thumbnail grid with hover elevation
- Click-to-popup full resolution lightbox modal
- Collapsible navigation drawer sidebar
- All images Base64-inlined for complete offline portability
"""

import base64
import io
from pathlib import Path
from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "storyboard_gallery.html"
IMAGE_EXT = {".png", ".jpg", ".jpeg", ".webp"}

SCENES = [
    ("S01", "The Heiress of Maitama", "In Maitama, money doesn't speak — it whispers behind high gates and polished marble. But even in luxury, I felt like a bird in a golden cage.", "TIWA_MANSION", 1),
    ("S02", "Broken Down on Shehu Shagari Way", "A flat tire on Abuja's busiest expressway, rain pouring down. My driver was panicked, until a young engineer stopped his pickup truck and stepped out.", "ABUJA_HIGHWAY", 1),
    ("S03", "The First Encounter", "Tunde didn't care about my designer shoes or famous surname. He wiped grease off his hands, smiled, and fixed the engine in ten minutes.", "ABUJA_HIGHWAY", 1),
    ("S04", "Coffee in Wuse II", "I offered to pay him. He refused the cash and asked for coffee instead. That single cup in Wuse II turned into two hours of laughter.", "WUSE_CAFE", 1),
    ("S05", "Chief Adenuga's Warning", "Father saw Tunde drop me off. His words were cold as steel: 'An Adenuga does not mingle with mechanics, Tiwa. Remember who you are.'", "TIWA_MANSION", 1),
    ("S06", "Sunset at Jabi Lake", "We met at Jabi Lake boardwalk as the sun dipped behind the water. For the first time in my life, someone listened to my dreams, not my pedigree.", "JABI_LAKE", 2),
    ("S07", "Tunde's Solar Workshop", "He showed me his prototype solar grid for rural villages. Tunde wasn't just a mechanic — he was building light for millions.", "TUNDE_WORKSHOP", 2),
    ("S08", "Bisi's Advice", "Bisi laughed when I told her. 'Tiwa, you are falling for a guy who smells like motor oil and ambition! But your eyes have never shined like this.'", "TIWA_STUDIO", 2),
    ("S09", "The Stolen Moment at Millennium Park", "Under the canopy of green trees, Tunde held my hand. He told me he knew the gap between our worlds, but he would bridge it.", "MILLENNIUM_PARK", 2),
    ("S10", "The First Kiss", "A soft breeze over the lake, warm Abuja night air. When he kissed me, all the high-society expectations dissolved into night.", "JABI_LAKE", 2),
    ("S11", "The Gala Announcement", "The Adenuga Annual Charity Gala in Asokoro. Father stood on stage and announced my prospective alliance with Segun Lawson.", "ASOKORO_BALLROOM", 3),
    ("S12", "Segun's Arrogance", "Segun took my hand with possessive confidence. 'We are the power couple of Abuja, Tiwa. Don't waste your time with small-town dreamers.'", "ASOKORO_BALLROOM", 3),
    ("S13", "Tunde Gatecrashes", "Tunde arrived in a tailored dark suit to deliver solar plans to a state governor. Our eyes met across the glittering room.", "ASOKORO_BALLROOM", 3),
    ("S14", "Chief Adenuga's Confrontation", "Father confronted Tunde in the private study. 'Stay away from my daughter. I will buy out your small workshop before you can take another step.'", "TIWA_MANSION_STUDY", 3),
    ("S15", "The Ultimatum", "Tunde stood tall before Chief Adebayo Adenuga. 'You can buy buildings, Chief, but you cannot buy Tiwa's heart or my self-respect.'", "TIWA_MANSION", 3),
    ("S16", "Segun's Sabotage", "Segun pulled strings with bank directors to freeze Tunde's startup loan. The workshop was locked, the power cut off.", "TUNDE_WORKSHOP", 4),
    ("S17", "Tiwa Stands Her Ground", "I confronted Segun in front of my father. I threw his engagement ring on the glass table. 'I will never belong to a man who uses deceit.'", "TIWA_MANSION", 4),
    ("S18", "Rain at the National Mosque Vista", "I found Tunde standing in the rain overlooking the cityscape. He asked if I was ready to face the storm that was coming.", "ABUJA_VISTA", 4),
    ("S19", "The Green Energy Pitch", "With Tiwa's support and Bisi's media backing, Tunde pitched directly to the Federal Energy Board. His passion captivated the entire room.", "MINISTRY_HALL", 4),
    ("S20", "Chief Adenuga Watches", "Father sat in the back of the auditorium, watching Tunde command the stage. For the first time, I saw doubt in my father's eyes.", "MINISTRY_HALL", 4),
    ("S21", "The Federal Contract Won", "The Board awarded Tunde the nationwide rural electrification contract. Segun walked out in disgrace.", "MINISTRY_HALL", 5),
    ("S22", "Chief Adenuga's Blessing", "Father invited Tunde to our estate in Maitama. He bowed his head and offered his hand. 'You are a real man, Tunde. Take care of my daughter.'", "TIWA_MANSION_GARDEN", 5),
    ("S23", "The Traditional Yoruba Igbeyawo", "Dressed in matching regal royal blue Aso-Oke, surrounded by family, drumming, and vibrant Yoruba culture, Tunde prostrated before my parents.", "MAITAMA_GARDENS", 5),
    ("S24", "The Church & White Wedding", "In the cathedral under stained glass, we took our vows. From a broken-down car on Shehu Shagari Way to forever.", "ABUJA_CATHEDRAL", 5),
    ("S25", "The Rich Abuja Girl's True Wealth", "Years later at Jabi Lake, watching our child laugh under the sun. I realized true wealth wasn't in Father's bank accounts — it was in the love we built together.", "JABI_LAKE", 5),
]

ACTS = {
    1: ("TWO DIFFERENT WORLDS", ["S01", "S02", "S03", "S04", "S05"]),
    2: ("SPARKS & SECRET ENCOUNTERS", ["S06", "S07", "S08", "S09", "S10"]),
    3: ("THE CLASH OF STATUS", ["S11", "S12", "S13", "S14", "S15"]),
    4: ("THE TEST OF LOVE", ["S16", "S17", "S18", "S19", "S20"]),
    5: ("TRIUMPH & DEVOTION", ["S21", "S22", "S23", "S24", "S25"]),
}

def inline_images(path, thumb_size=520, full_size=1200):
    """Inline thumbnail and full-resolution images as base64 JPEG strings."""
    with Image.open(path) as raw:
        image = ImageOps.exif_transpose(raw).convert("RGB")
        
        # Thumbnail (card grid)
        thumb_h = int(thumb_size * 9 / 16)
        thumb_img = image.copy()
        thumb_img.thumbnail((thumb_size, thumb_h), Image.Resampling.LANCZOS)
        thumb_canvas = Image.new('RGB', (thumb_size, thumb_h), (10, 30, 22))
        thumb_canvas.paste(thumb_img, ((thumb_size - thumb_img.width) // 2, (thumb_h - thumb_img.height) // 2))
        thumb_buffer = io.BytesIO()
        thumb_canvas.save(thumb_buffer, format="JPEG", quality=75, optimize=True)
        thumb_b64 = base64.b64encode(thumb_buffer.getvalue()).decode("ascii")
        
        # Full resolution (lightbox)
        full_h = int(full_size * 9 / 16)
        full_img = image.copy()
        full_img.thumbnail((full_size, full_h), Image.Resampling.LANCZOS)
        full_canvas = Image.new('RGB', (full_size, full_h), (10, 30, 22))
        full_canvas.paste(full_img, ((full_size - full_img.width) // 2, (full_h - full_img.height) // 2))
        full_buffer = io.BytesIO()
        full_canvas.save(full_buffer, format="JPEG", quality=92, optimize=True)
        full_b64 = base64.b64encode(full_buffer.getvalue()).decode("ascii")
        
        return thumb_b64, full_b64

def image_files(folder):
    if not folder.exists(): return []
    return sorted((p for p in folder.iterdir() if p.is_file() and p.suffix.lower() in IMAGE_EXT), key=lambda p: p.name)

def label_for(path):
    stem = path.stem
    if stem.endswith("_ref"):
        name_part = stem[:-4].replace("_", " ").title()
        return f"{name_part} — CHARACTER REFERENCE"
    parts = stem.split("_")
    if len(parts) >= 2 and parts[0].startswith("S") and parts[1].startswith("Step"):
        return f"{parts[0]} — " + " ".join(parts[2:]).replace("_", " ").title()
    return stem.replace("_", " ").title()

def build_gallery():
    print("=" * 60)
    print("THE RICH ABUJA GIRL — Gallery Builder")
    print("=" * 60)
    
    scene_map = {s[0]: {"title": s[1], "voiceover": s[2], "location": s[3], "act": s[4]} for s in SCENES}
    refs = image_files(ROOT / "images" / "refs")
    acts = {a: image_files(ROOT / "images" / f"act{a}") for a in (1, 2, 3, 4, 5)}
    total = len(refs) + sum(len(f) for f in acts.values())
    print(f"\nImages: {total} total, {len(refs)} character references")
    
    html = ['<!doctype html><html><head><meta charset="utf-8">']
    html.append('<title>The Rich Abuja Girl — Storyboard Gallery</title>')
    html.append('<style>')
    html.append('*{margin:0;padding:0;box-sizing:border-box;}')
    html.append('body{font-family:"Segoe UI",Tahoma,Geneva,Verdana,sans-serif;background:#0d1b15;color:#e2ece7;line-height:1.6;}')
    html.append('header{background:linear-gradient(135deg,#0a231c 0%,#154336 50%,#d4af37 100%);color:#fff;padding:3.5rem 2rem;text-align:center;box-shadow:0 4px 20px rgba(0,0,0,0.4);border-bottom:3px solid #d4af37;}')
    html.append('h1{font-size:2.8rem;margin-bottom:0.5rem;font-weight:300;letter-spacing:1px;color:#f9f6e8;}')
    html.append('.subtitle{font-size:1.2rem;color:#d4af37;margin-bottom:1rem;font-weight:400;text-transform:uppercase;letter-spacing:2px;}')
    html.append('.description{max-width:850px;margin:1rem auto;font-size:1.05rem;opacity:0.95;line-height:1.7;color:#e8f0eb;}')
    html.append('.badge{display:inline-block;padding:0.6rem 1.8rem;background:rgba(212,175,55,0.15);border:1px solid #d4af37;border-radius:25px;margin-top:1rem;font-size:0.95rem;color:#d4af37;}')
    html.append('.sidebar-toggle{position:fixed;top:1.5rem;left:1.5rem;z-index:9999;background:#154336;color:#d4af37;border:1px solid #d4af37;padding:0.75rem 1.25rem;font-size:1rem;cursor:pointer;border-radius:25px;box-shadow:0 2px 10px rgba(0,0,0,0.3);font-family:inherit;transition:all 0.3s;}')
    html.append('.sidebar-toggle:hover{background:#d4af37;color:#0a231c;transform:translateY(-2px);}')
    html.append('.sidebar{position:fixed;top:0;left:-380px;width:380px;height:100vh;background:#0a231c;border-right:1px solid #d4af37;z-index:9998;transition:left 0.3s ease;overflow-y:auto;padding:5rem 1.5rem 2rem;box-shadow:4px 0 20px rgba(0,0,0,0.5);}')
    html.append('.sidebar.open{left:0;}')
    html.append('.sidebar-overlay{display:none;position:fixed;inset:0;background:rgba(0,0,0,0.7);z-index:9997;}')
    html.append('.sidebar-overlay.active{display:block;}')
    html.append('.sidebar-close{position:absolute;top:1rem;right:1rem;font-size:1.5rem;color:#d4af37;background:none;border:none;cursor:pointer;width:32px;height:32px;border-radius:50%;}')
    html.append('.sidebar nav{display:flex;flex-direction:column;gap:0.3rem;}')
    html.append('.sidebar nav a{color:#c5d8cf;text-decoration:none;padding:0.6rem 0.75rem;border-radius:6px;transition:all 0.2s;font-size:0.95rem;}')
    html.append('.sidebar nav a:hover{background:rgba(212,175,55,0.15);color:#d4af37;}')
    html.append('.sidebar nav a.act-link{font-weight:600;color:#d4af37;margin-top:0.75rem;padding:0.75rem;background:#154336;border-radius:8px;border-left:3px solid #d4af37;}')
    html.append('.sidebar nav a.scene-link{padding-left:1.75rem;font-size:0.9rem;color:#9ab5a8;}')
    html.append('.container{max-width:1400px;margin:0 auto;padding:2rem;}')
    html.append('.act{margin:3.5rem 0;}')
    html.append('.act h2{color:#d4af37;font-size:2.2rem;margin-bottom:1.5rem;padding-bottom:0.75rem;border-bottom:2px solid #154336;font-weight:300;letter-spacing:1px;}')
    html.append('.scene{margin:2rem 0;padding:2rem;background:#122820;border-radius:12px;box-shadow:0 4px 15px rgba(0,0,0,0.3);border-left:4px solid #d4af37;}')
    html.append('.scene h3{color:#f9f6e8;font-size:1.5rem;margin-bottom:0.5rem;font-weight:500;}')
    html.append('.scene .location{color:#d4af37;font-size:0.9rem;margin-bottom:1rem;text-transform:uppercase;letter-spacing:1px;font-weight:600;}')
    html.append('.voiceover{font-style:italic;color:#e2ece7;margin:1.5rem 0;padding:1.5rem;background:#173329;border-left:3px solid #d4af37;border-radius:6px;line-height:1.8;font-size:1.05rem;}')
    html.append('.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));gap:1.5rem;margin-top:1.5rem;}')
    html.append('.card{cursor:pointer;transition:all 0.3s;background:#173329;border-radius:8px;overflow:hidden;box-shadow:0 3px 10px rgba(0,0,0,0.3);border:1px solid rgba(212,175,55,0.2);}')
    html.append('.card:hover{transform:translateY(-5px);box-shadow:0 8px 25px rgba(212,175,55,0.3);border-color:#d4af37;}')
    html.append('.card img{width:100%;height:auto;display:block;}')
    html.append('.card .label{padding:1rem;text-align:center;font-size:0.9rem;color:#c5d8cf;font-weight:500;}')
    html.append('.lightbox{display:none;position:fixed;top:0;left:0;width:100%;height:100%;background:rgba(0,0,0,0.92);z-index:10000;justify-content:center;align-items:center;}')
    html.append('.lightbox.active{display:flex;}')
    html.append('.lightbox img{max-width:95%;max-height:95%;object-fit:contain;border-radius:6px;border:2px solid #d4af37;}')
    html.append('.lightbox-close{position:absolute;top:20px;right:30px;font-size:2.5rem;color:#d4af37;cursor:pointer;background:rgba(0,0,0,0.5);border:1px solid #d4af37;width:50px;height:50px;border-radius:50%;transition:background 0.2s;}')
    html.append('.lightbox-close:hover{background:#d4af37;color:#0a231c;}')
    html.append('@media (max-width:768px){.container{padding:1rem;}.act{margin:2rem 0;}.scene{padding:1.2rem;}.grid{grid-template-columns:repeat(auto-fill,minmax(200px,1fr));gap:1rem;}}')
    html.append('</style></head><body>')
    
    html.append('<button class="sidebar-toggle" onclick="toggleSidebar()">☰ Navigate Story</button>')
    html.append('<div class="sidebar-overlay" id="sidebar-overlay" onclick="toggleSidebar()"></div>')
    html.append('<aside class="sidebar" id="sidebar">')
    html.append('<button class="sidebar-close" onclick="toggleSidebar()">✕</button>')
    html.append('<nav>')
    html.append('<a href="#character-refs" style="font-weight:600;color:#d4af37;">Character References</a>')
    for act_num in range(1, 6):
        act_name, scene_ids = ACTS[act_num]
        html.append(f'<a href="#act-{act_num}" class="act-link">Act {act_num} — {act_name}</a>')
        for scene_id in scene_ids:
            info = scene_map[scene_id]
            html.append(f'<a href="#{scene_id}" class="scene-link">{scene_id} — {info["title"]}</a>')
    html.append('</nav></aside>')
    
    html.append('<header>')
    html.append('<h1>The Rich Abuja Girl</h1>')
    html.append('<div class="subtitle">A Nigerian High-Society Romance Story</div>')
    html.append('<p class="description">When Tiwa Adenuga, heiress to one of Abuja\'s wealthiest Yoruba empires, breaks down on Shehu Shagari Way, she meets Tunde Bakare — a brilliant tech engineer from humble roots. As their bond deepens amidst the luxury of Maitama and sunset walks at Jabi Lake, class divides, family expectations, and an arrogant rival suitor threaten to tear them apart.</p>')
    html.append(f'<div class="badge">{total} Storyboard Keyframes & Character References • Click thumbnails for full resolution</div>')
    html.append('</header>')
    
    html.append('<div class="container">')
    
    # Character References Section
    html.append('<div class="act" id="character-refs"><h2>Character References</h2><div class="grid">')
    for img_path in refs:
        thumb_b64, full_b64 = inline_images(img_path)
        label = label_for(img_path)
        html.append(f'<div class="card" onclick="openLightbox(\'data:image/jpeg;base64,{full_b64}\')">')
        html.append(f'<img src="data:image/jpeg;base64,{thumb_b64}" alt="{label}">')
        html.append(f'<div class="label">{label}</div>')
        html.append('</div>')
    html.append('</div></div>')
    
    # Act Sections & Scenes
    for act_num in range(1, 6):
        act_name, scene_ids = ACTS[act_num]
        html.append(f'<div class="act" id="act-{act_num}"><h2>Act {act_num} — {act_name}</h2>')
        
        for scene_id in scene_ids:
            info = scene_map[scene_id]
            html.append(f'<div class="scene" id="{scene_id}">')
            html.append(f'<h3>{scene_id} — {info["title"]}</h3>')
            html.append(f'<div class="location">LOCATION: {info["location"]}</div>')
            vo_html = info["voiceover"].replace('\n', '<br>')
            html.append(f'<div class="voiceover">"{vo_html}"</div>')
            html.append('<div class="grid">')
            
            scene_imgs = [p for p in acts[act_num] if p.name.startswith(f"{scene_id}_")]
            for img_path in scene_imgs:
                thumb_b64, full_b64 = inline_images(img_path)
                label = label_for(img_path)
                html.append(f'<div class="card" onclick="openLightbox(\'data:image/jpeg;base64,{full_b64}\')">')
                html.append(f'<img src="data:image/jpeg;base64,{thumb_b64}" alt="{label}">')
                html.append(f'<div class="label">{label}</div>')
                html.append('</div>')
            
            html.append('</div></div>')
        
        html.append('</div>')
    
    html.append('</div>')  # Close container
    
    # Lightbox Modal
    html.append('<div class="lightbox" id="lightbox" onclick="closeLightbox()">')
    html.append('<button class="lightbox-close" onclick="closeLightbox()">&times;</button>')
    html.append('<img id="lightbox-img" src="" alt="Full resolution keyframe">')
    html.append('</div>')
    
    # JavaScript
    html.append('<script>')
    html.append('function openLightbox(src){document.getElementById("lightbox-img").src=src;document.getElementById("lightbox").classList.add("active");}')
    html.append('function closeLightbox(){document.getElementById("lightbox").classList.remove("active");}')
    html.append('function toggleSidebar(){document.getElementById("sidebar").classList.toggle("open");document.getElementById("sidebar-overlay").classList.toggle("active");}')
    html.append('document.addEventListener("keydown",function(e){if(e.key==="Escape"){closeLightbox();if(document.getElementById("sidebar").classList.contains("open"))toggleSidebar();}});')
    html.append('</script>')
    
    html.append('</body></html>')
    
    OUT.write_text('\n'.join(html), encoding='utf-8')
    size_mb = OUT.stat().st_size / (1024 * 1024)
    print(f"\n[OK] Wrote {OUT.name}")
    print(f"  Total images embedded: {total}")
    print(f"  File size: {size_mb:.2f} MB")
    print("=" * 60)

if __name__ == "__main__":
    build_gallery()
