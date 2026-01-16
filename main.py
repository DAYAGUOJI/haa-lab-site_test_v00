import os
import webbrowser
from pathlib import Path

# =================配置区域=================
BASE_DIR = Path(__file__).parent
ASSETS_DIR = BASE_DIR / "assets" / "icons"
H_REEL_DIR = ASSETS_DIR / "h_reel"
A_REEL_DIR = ASSETS_DIR / "a_reel"
OUTPUT_HTML = BASE_DIR / "haa_logo_final_v19.html"

# == 视觉配置 ==
LOGO_SIZE = "80px"       
GAP_SIZE = "3px"         
BG_COLOR = "#f4f4f4"     
ICON_COLOR = "#000000"   
HEART_COLOR = "#D32F2F"  
APPLE_COLOR = "#000000"
ANCHOR_WATER_COLOR = "#000000" 

# =================逻辑区域=================

def get_svg_content(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            if '<svg' in content: return content
    except Exception: return None

def load_icons(directory):
    icons = []
    if not directory.exists(): return []
    for file in sorted(directory.glob("*.svg")):
        content = get_svg_content(file)
        if content: 
            # 1. 外星人特效
            if file.stem == 'alien':
                eye_covers = """
                    <circle class="eye-cover left-eye" cx="29.5%" cy="60.5%" r="18%" fill="white" transform="scale(0)" />
                    <circle class="eye-cover right-eye" cx="70.5%" cy="60.5%" r="18%" fill="white" transform="scale(0)" />
                """
                content = content.replace('</svg>', f'{eye_covers}</svg>')
            
            # 2. 维特鲁威人特效 [更新为你指定的参数]
            if file.stem == 'human':
                v_shapes = """
                    <circle class="v-shape v-circle" cx="50%" cy="50.5%" r="55%" />
                    <rect class="v-shape v-rect" x="2%" y="8%" width="100.5%" height="92%" />
                """
                content = content.replace('</svg>', f'{v_shapes}</svg>')

            icons.append({"name": file.stem, "content": content})
    return icons

def generate_html():
    h_icons = load_icons(H_REEL_DIR)
    a_icons = load_icons(A_REEL_DIR)
    
    if not h_icons or not a_icons:
        print("错误：未找到图标")
        return

    h_render_list = h_icons * 3
    a_render_list = a_icons * 3

    html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <style>
        :root {{
            --size: {LOGO_SIZE};
            --gap: {GAP_SIZE};
            --bg-color: {BG_COLOR};
            --icon-color: {ICON_COLOR};
            --heart-color: {HEART_COLOR};
            --water-color: {ANCHOR_WATER_COLOR};
            --anchor-hover-y: -6px; 
        }}

        body {{
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
            background-color: var(--bg-color);
            font-family: sans-serif;
            overflow: hidden;
        }}

        /* === Logo 容器 === */
        .haa-logo {{
            display: flex;
            gap: var(--gap);
            position: relative;
        }}

        /* 遮罩 */
        .haa-logo::before, .haa-logo::after {{
            content: "";
            position: absolute;
            left: 0; right: 0;
            height: 25%; 
            z-index: 10; 
            pointer-events: none;
        }}
        .haa-logo::before {{ top: 0; background: linear-gradient(to bottom, var(--bg-color) 0%, transparent 100%); }}
        .haa-logo::after {{ bottom: 0; background: linear-gradient(to top, var(--bg-color) 0%, transparent 100%); }}

        .reel {{
            width: var(--size);
            height: var(--size);
            overflow: hidden; 
            position: relative;
            z-index: 1; 
        }}
        
        .reel.pop-out {{
            overflow: visible !important; 
            z-index: 20; 
        }}

        .reel.pop-out .strip .icon-box {{ opacity: 0; transition: opacity 0s; }}
        .reel.pop-out .strip .icon-box.active-overlay {{ opacity: 1; }}

        .strip {{
            display: flex;
            flex-direction: column;
            will-change: transform;
        }}

        .icon-box {{
            width: var(--size);
            height: var(--size);
            display: flex;
            justify-content: center;
            align-items: center;
            flex-shrink: 0;
            position: relative;
        }}

        svg {{
            width: 70%; 
            height: 70%;
            fill: var(--icon-color);
            transition: fill 0.3s ease;
            transform-origin: center center;
            /* 允许内容溢出画布 */
            overflow: visible !important; 
        }}

        /* === 模糊旋转 === */
        .blur-spin {{
            filter: blur(2px);
            animation: infinite-spin 0.4s linear infinite;
        }}

        @keyframes infinite-spin {{
            0% {{ transform: translateY(0); }}
            100% {{ transform: translateY(-33.33%); }}
        }}

        /* === 粒子系统 === */
        .particle-wrapper {{
            position: absolute;
            /* 强制层级最高，确保粒子在 Frame 和 Mask 之上 */
            z-index: 100; 
            opacity: 0;
            pointer-events: none;
            /* 开启 GPU 加速 */
            transform: translateZ(1px); 
            animation: fly-x 0.4s linear forwards;
        }}

        .particle-inner {{
            width: 100%;
            height: 100%;
            animation: fly-y 0.4s cubic-bezier(0.25, 1, 0.5, 1) forwards;
        }}
        
        .p-crumb .particle-inner {{
            width: 0; height: 0; 
            border-left: 2px solid transparent; 
            border-right: 2px solid transparent; 
            border-bottom: 4px solid var(--icon-color);
        }}

        .p-water .particle-inner {{
            background-color: var(--water-color); 
            border-radius: 50%;
        }}

        @keyframes fly-x {{
            0% {{ transform: translateX(0); opacity: 1; }}
            100% {{ transform: translateX(var(--tx)); opacity: 0; }}
        }}

        @keyframes fly-y {{
            0% {{ transform: translateY(0) scale(1); }}
            100% {{ transform: translateY(var(--ty)) scale(0.5); }}
        }}

        /* === 特效定义 === */
        
        /* Anchor */
        .anchor-hover-high svg {{ transform: translateY(var(--anchor-hover-y)) !important; }}
        .anchor-drop svg {{ animation: high-drop 0.2s cubic-bezier(0.5, 0, 0.75, 0) forwards; }}
        @keyframes high-drop {{ 0% {{ transform: translateY(var(--anchor-hover-y)); opacity: 1; }} 100% {{ transform: translateY(0); opacity: 1; }} }}

        /* Hammer */
        .hammer-action svg {{ transform-origin: 80% 80%; animation: hammer-smash 0.4s cubic-bezier(0.25, 1, 0.5, 1) forwards; }}
        @keyframes hammer-smash {{ 0% {{ transform: rotate(0deg); }} 40% {{ transform: rotate(60deg); }} 100% {{ transform: rotate(0deg); }} }}

        /* Heart */
        .heartbeat svg {{ 
            fill: var(--heart-color) !important; 
            animation: heart-pulse 1.2s infinite ease-in-out;
        }}
        @keyframes heart-pulse {{
             0% {{ transform: scale(1); }}
             15% {{ transform: scale(1.25); }}
             30% {{ transform: scale(1); }}
             45% {{ transform: scale(1.15); }}
             60% {{ transform: scale(1); }}
             100% {{ transform: scale(1); }}
        }}

        /* Apple */
        .bite-mark {{ position: absolute; background-color: var(--bg-color); border-radius: 50%; width: 32%; height: 32%; opacity: 0; z-index: 10; }}
        .bite-1 {{ top: 25%; right: 1%; }} 
        .bite-2 {{ top: 50%; right: -3%; }}   
        .bite-anim {{ animation: bite-snap 0.05s linear forwards; }}
        @keyframes bite-snap {{ from {{ opacity: 0; transform: scale(0.8); }} to {{ opacity: 1; transform: scale(1); }} }}

        /* Alien */
        .eye-cover {{ transform: scale(0); transform-origin: center; transition: transform 0.1s cubic-bezier(0, 0, 0.2, 1); }}
        .alien-action .eye-cover {{ transform: scale(1) !important; }}

        /* Human (Vitruvian) */
        .v-shape {{
            fill: none; stroke: var(--icon-color); stroke-width: 2px;
            /* [修改] 粗细改为 2px */
            stroke-width: 2px; 
            stroke-dasharray: 400; stroke-dashoffset: 400; opacity: 1; vector-effect: non-scaling-stroke; stroke-linecap: round;
        }}
        .v-circle {{ transform-origin: center; transform: rotate(-135deg); }}

        .draw-circle .v-circle {{ animation: draw-stroke 1.6s linear forwards; }}
        .draw-square .v-rect {{ animation: draw-stroke 1.6s linear forwards; }}
        @keyframes draw-stroke {{ to {{ stroke-dashoffset: 0; }} }}

    </style>
</head>
<body>

    <div class="haa-logo">
        <div class="reel"><div class="strip">{_build_strip(h_render_list)}</div></div>
        <div class="reel"><div class="strip">{_build_strip(a_render_list)}</div></div>
        <div class="reel"><div class="strip">{_build_strip(a_render_list)}</div></div>
    </div>

    <script>
        const WAIT_TIME = 3500;
        const SPIN_DURATION_BASE = 1000; 
        const SPIN_DELAY = 400; 
        const START_DELAY = 150;
        
        const reelCounts = [{len(h_icons)}, {len(a_icons)}, {len(a_icons)}];
        const strips = document.querySelectorAll('.strip');
        const iconHeight = document.querySelector('.icon-box').offsetHeight;

        async function sleep(ms) {{ return new Promise(r => setTimeout(r, ms)); }}

        function spawnParticles(container, startX, startY, type, dirY, spreadX = 15) {{
            let count = (type === 'water') ? (20 + Math.floor(Math.random() * 10)) : (3 + Math.floor(Math.random() * 3));
            for (let k = 0; k < count; k++) {{
                const wrapper = document.createElement('div');
                wrapper.className = `particle-wrapper p-${{type}}`;
                
                const inner = document.createElement('div');
                inner.className = 'particle-inner';
                wrapper.appendChild(inner);

                const safeY = type === 'water' ? (60 + Math.random() * 30) : (startY + (Math.random()-0.5)*5);
                wrapper.style.top = safeY + '%';
                wrapper.style.left = (startX + (Math.random()-0.5)*10) + '%'; 
                
                let tx, ty;
                if (type === 'water') {{
                    const angle = (Math.random() - 0.5) * 2.5; 
                    tx = angle * spreadX * 1.3; 
                    ty = -(11 + Math.random() * 4); 
                    const size = 2 + Math.random() * 5; 
                    wrapper.style.width = size + 'px';
                    wrapper.style.height = size + 'px';
                }} else {{
                    tx = (Math.random() - 0.5) * spreadX * 2;
                    ty = (10 + Math.random() * 20) * dirY;
                }}
                
                wrapper.style.setProperty('--tx', `${{tx}}px`);
                wrapper.style.setProperty('--ty', `${{ty}}px`);
                container.appendChild(wrapper);
            }}
        }}

        async function runAnimationLoop() {{
            while (true) {{
                // 1. 依次启动
                for (let i = 0; i < 3; i++) {{
                    const strip = strips[i];
                    strip.parentElement.classList.remove('pop-out');
                    const icons = strip.querySelectorAll('.icon-box');
                    icons.forEach(el => {{
                        el.classList.remove('heartbeat', 'hammer-action', 'alien-action', 'anchor-drop', 'anchor-hover-high', 'active-overlay', 'draw-circle', 'draw-square');
                        el.querySelectorAll('.bite-mark, .particle-wrapper').forEach(n => n.remove());
                        el.style.opacity = ''; 
                    }});

                    strip.style.transition = 'none';
                    strip.style.transform = 'translateY(0)';
                    strip.classList.add('blur-spin');
                    await sleep(START_DELAY);
                }}

                await sleep(SPIN_DURATION_BASE);

                // 2. 依次停止
                for (let i = 0; i < 3; i++) {{
                    const strip = strips[i];
                    const count = reelCounts[i];
                    const targetIndex = Math.floor(Math.random() * count); 
                    const finalPos = -(targetIndex + count) * iconHeight;

                    const targetEl = strip.children[targetIndex + count];
                    const name = targetEl.getAttribute('data-name');
                    const parentReel = strip.parentElement;

                    strip.classList.remove('blur-spin');
                    strip.style.transition = 'transform 0.6s cubic-bezier(0.15, 1, 0.3, 1)';
                    strip.style.transform = `translateY(${{finalPos}}px)`;

                    // === 溢出控制 ===
                    if (['anchor', 'hammer', 'human', 'heart'].some(n => name.includes(n))) {{
                        targetEl.classList.add('active-overlay'); 
                        parentReel.classList.add('pop-out');      
                    }}
                    
                    if (name.includes('anchor')) {{
                        targetEl.classList.add('anchor-hover-high');
                    }}

                    // === 动画触发 ===
                    if (name.includes('anchor')) {{
                        setTimeout(() => {{
                            targetEl.classList.remove('anchor-hover-high');
                            targetEl.classList.add('anchor-drop');
                            setTimeout(() => {{
                                spawnParticles(targetEl, 50, 90, 'water', -1, 40); 
                            }}, 200);
                        }}, 600); 
                    }}

                    if (name.includes('heart')) setTimeout(() => targetEl.classList.add('heartbeat'), 600);

                    if (name.includes('hammer')) {{
                        setTimeout(() => {{
                            targetEl.classList.add('hammer-action');
                            // 锤子粒子范围 spreadX = 30
                            setTimeout(() => spawnParticles(targetEl, 92, 45, 'crumb', 1, 30), 150);
                        }}, 600);
                    }}

                    if (name.includes('apple')) {{
                        setTimeout(() => {{
                            const b1 = document.createElement('div');
                            b1.className = 'bite-mark bite-1 bite-anim';
                            targetEl.appendChild(b1);
                            spawnParticles(targetEl, 75, 25, 'crumb', -1); 
                            setTimeout(() => {{
                                const b2 = document.createElement('div');
                                b2.className = 'bite-mark bite-2 bite-anim';
                                targetEl.appendChild(b2);
                                spawnParticles(targetEl, 78, 50, 'crumb', 1);
                            }}, 250); 
                        }}, 600);
                    }}
                    
                    if (name.includes('alien')) {{
                        const totalTimeLeft = ((3 - i) * SPIN_DELAY) + WAIT_TIME;
                        const triggerTime = totalTimeLeft - 100;
                        setTimeout(() => targetEl.classList.add('alien-action'), triggerTime);
                    }}

                    if (name.includes('human')) {{
                        setTimeout(() => {{
                            targetEl.classList.add('draw-square');
                            setTimeout(() => {{
                                targetEl.classList.add('draw-circle');
                            }}, 1600);
                        }}, 600);
                    }}

                    await sleep(SPIN_DELAY);
                }}

                await sleep(WAIT_TIME);
            }}
        }}

        window.onload = runAnimationLoop;
    </script>
</body>
</html>
    """
    
    with open(OUTPUT_HTML, 'w', encoding='utf-8') as f:
        f.write(html_content)
    print(f"最终优化版 v19 生成: {OUTPUT_HTML}")
    webbrowser.open(f'file://{OUTPUT_HTML.resolve()}')

def _build_strip(icons):
    html = ""
    for icon in icons:
        html += f'<div class="icon-box" data-name="{icon["name"]}">{icon["content"]}</div>'
    return html

if __name__ == "__main__":
    generate_html()