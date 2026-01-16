import os
import webbrowser
from pathlib import Path

# ================= 配置 =================
BASE_DIR = Path(__file__).parent
ASSETS_DIR = BASE_DIR / "assets" / "icons"
HUMAN_PATH = ASSETS_DIR / "h_reel" / "human.svg" 
OUTPUT_HTML = BASE_DIR / "human_geometry_tuner_v3.html"

def get_human_content():
    target_path = HUMAN_PATH
    if not target_path.exists():
        target_path = ASSETS_DIR / "a_reel" / "human.svg"
    
    if not target_path.exists():
        print(f"❌ 错误：找不到 human.svg，请检查 assets 文件夹")
        return None

    try:
        with open(target_path, 'r', encoding='utf-8') as f:
            content = f.read()
            content = content.replace('</svg>', '') 
            return content
    except Exception as e:
        print(f"❌ 读取错误: {e}")
        return None

def generate_test_bench():
    human_svg_body = get_human_content()
    if not human_svg_body: return

    html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Vitruvian Tuner V3 (Fully Unlocked)</title>
    <style>
        body {{
            background-color: #1e1e1e;
            color: #eee;
            font-family: 'Segoe UI', sans-serif;
            display: flex;
            height: 100vh;
            margin: 0;
            overflow: hidden;
        }}
        
        .preview-area {{
            flex: 2;
            display: flex;
            justify-content: center;
            align-items: center;
            background-image: 
                linear-gradient(#333 1px, transparent 1px), 
                linear-gradient(90deg, #333 1px, transparent 1px);
            background-size: 20px 20px;
            position: relative;
        }}

        .crosshair-x, .crosshair-y {{
            position: absolute;
            background: rgba(255, 0, 0, 0.3);
            pointer-events: none;
            z-index: 0;
        }}
        .crosshair-x {{ width: 100%; height: 1px; top: 50%; }}
        .crosshair-y {{ height: 100%; width: 1px; left: 50%; }}

        .icon-container {{
            width: 500px;
            height: 500px;
            border: 1px dashed #666;
            display: flex;
            justify-content: center;
            align-items: center;
            position: relative;
            background: #000; 
        }}

        svg {{ width: 100%; height: 100%; }}

        svg > :not(.v-shape) {{
            filter: invert(1);
            opacity: 0.4;
        }}

        .v-shape {{
            fill: none !important;
            stroke-width: 2; 
            vector-effect: non-scaling-stroke;
            opacity: 1 !important;
        }}
        #v-circle {{ stroke: #00ffcc; }} 
        #v-rect {{ stroke: #ff00ff; }}   

        .controls {{
            flex: 1;
            padding: 20px;
            background: #252526;
            box-shadow: -5px 0 15px rgba(0,0,0,0.5);
            display: flex;
            flex-direction: column;
            gap: 12px;
            overflow-y: auto;
            min-width: 300px;
        }}

        h2 {{ margin-top: 0; color: #00ffcc; font-size: 16px; border-bottom: 1px solid #444; padding-bottom: 10px; }}
        h3 {{ margin: 5px 0 5px 0; color: #ff00ff; font-size: 14px; }}
        
        .control-group {{
            background: #333;
            padding: 10px;
            border-radius: 6px;
        }}

        label {{ display: flex; justify-content: space-between; margin-bottom: 2px; font-size: 12px; color: #ccc; }}
        input[type=range] {{ width: 100%; cursor: pointer; }}
        
        .code-output {{
            background: #111;
            color: #a6e3a1;
            padding: 10px;
            border-radius: 5px;
            font-family: monospace;
            font-size: 11px;
            word-break: break-all;
            user-select: text;
            border: 1px solid #444;
        }}
        
        .val {{ color: #fff; font-weight: bold; }}
    </style>
</head>
<body>

    <div class="preview-area">
        <div class="crosshair-x"></div>
        <div class="crosshair-y"></div>
        <div class="icon-container">
            {human_svg_body}
            <circle id="v-circle" class="v-shape" cx="50%" cy="50%" r="35%" />
            <rect id="v-rect" class="v-shape v-rect" x="15%" y="15%" width="70%" height="70%" />
            </svg>
        </div>
    </div>

    <div class="controls">
        <h2>📐 Vitruvian Lab V3 (Full Manual)</h2>
        
        <div class="control-group" style="border-left: 3px solid #00ffcc;">
            <h3 style="color: #00ffcc;">⚪ 圆形 (Circle)</h3>
            
            <label>水平位置 (Center X) <span id="val-cx" class="val">55%</span></label>
            <input type="range" id="inp-cx" min="0" max="100" step="0.5" value="55">

            <label>垂直位置 (Center Y) <span id="val-cy" class="val">46.5%</span></label>
            <input type="range" id="inp-cy" min="0" max="100" step="0.5" value="46.5">

            <label>半径 (Radius) <span id="val-r" class="val">57.5%</span></label>
            <input type="range" id="inp-r" min="0" max="100" step="0.5" value="57.5">
        </div>

        <div class="control-group" style="border-left: 3px solid #ff00ff;">
            <h3 style="color: #ff00ff;">⬜ 矩形 (Rectangle)</h3>
            
            <label>左侧位置 (X) <span id="val-rx" class="val">2%</span></label>
            <input type="range" id="inp-rx" min="-50" max="50" step="0.25" value="2">
            
            <label>顶部位置 (Y) <span id="val-ry" class="val">8%</span></label>
            <input type="range" id="inp-ry" min="-50" max="50" step="0.25" value="8">

            <label>宽度 (Width) <span id="val-rw" class="val">100.5%</span></label>
            <input type="range" id="inp-rw" min="0" max="200" step="0.5" value="100.5">
            
            <label>高度 (Height) <span id="val-rh" class="val">92%</span></label>
            <input type="range" id="inp-rh" min="0" max="200" step="0.5" value="92">
        </div>
        
        <div class="code-output" id="result-code">...</div>
    </div>

    <script>
        const els = {{
            cx: document.getElementById('inp-cx'),
            cy: document.getElementById('inp-cy'),
            r: document.getElementById('inp-r'),
            
            rx: document.getElementById('inp-rx'),
            ry: document.getElementById('inp-ry'),
            rw: document.getElementById('inp-rw'),
            rh: document.getElementById('inp-rh'),
            
            circle: document.getElementById('v-circle'),
            rect: document.getElementById('v-rect'),
            
            output: document.getElementById('result-code')
        }};

        function update() {{
            // 1. 获取数值 (现在全部是手动值，没有自动计算了)
            const cx = parseFloat(els.cx.value);
            const cy = parseFloat(els.cy.value);
            const r = parseFloat(els.r.value);
            
            const rx = parseFloat(els.rx.value);
            const ry = parseFloat(els.ry.value);
            const rw = parseFloat(els.rw.value);
            const rh = parseFloat(els.rh.value);
            
            // 2. UI 更新
            document.getElementById('val-cx').innerText = cx + '%';
            document.getElementById('val-cy').innerText = cy + '%';
            document.getElementById('val-r').innerText = r + '%';
            
            document.getElementById('val-rx').innerText = rx + '%';
            document.getElementById('val-ry').innerText = ry + '%';
            document.getElementById('val-rw').innerText = rw + '%';
            document.getElementById('val-rh').innerText = rh + '%';

            // 3. SVG 更新
            els.circle.setAttribute('cx', cx + '%');
            els.circle.setAttribute('cy', cy + '%');
            els.circle.setAttribute('r', r + '%');
            
            els.rect.setAttribute('x', rx + '%');
            els.rect.setAttribute('y', ry + '%');
            els.rect.setAttribute('width', rw + '%');
            els.rect.setAttribute('height', rh + '%');

            // 4. 代码生成
            const code = `
                v_shapes = \"\"\"
                    <circle class="v-shape v-circle" cx="${{cx}}%" cy="${{cy}}%" r="${{r}}%" />
                    <rect class="v-shape v-rect" x="${{rx}}%" y="${{ry}}%" width="${{rw}}%" height="${{rh}}%" />
                \"\"\"`.trim();
            
            els.output.innerText = code;
        }}

        Object.values(els).forEach(el => {{
            if(el && el.tagName === 'INPUT') {{
                el.addEventListener('input', update);
            }}
        }});
        
        update();
    </script>
</body>
</html>
    """
    
    with open(OUTPUT_HTML, 'w', encoding='utf-8') as f:
        f.write(html_content)
    print(f"✅ V3 全手动调试台已生成: {OUTPUT_HTML}")
    webbrowser.open(f'file://{OUTPUT_HTML.resolve()}')

if __name__ == "__main__":
    generate_test_bench()