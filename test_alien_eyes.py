import os
import webbrowser
from pathlib import Path

# ================= 配置 =================
BASE_DIR = Path(__file__).parent
ASSETS_DIR = BASE_DIR / "assets" / "icons"
# 注意：这里假设你的图标在 a_reel 文件夹里，如果找不到请检查路径
ALIEN_PATH = ASSETS_DIR / "a_reel" / "alien.svg" 
OUTPUT_HTML = BASE_DIR / "alien_eye_tuner_mirror.html"

def get_alien_content():
    if not ALIEN_PATH.exists():
        # 尝试去 h_reel 找找，防止放错文件夹
        alt_path = ASSETS_DIR / "h_reel" / "alien.svg"
        if alt_path.exists():
            with open(alt_path, 'r', encoding='utf-8') as f:
                return f.read().replace('</svg>', '')
        
        print(f"❌ 错误：找不到外星人图标，请检查路径: {ALIEN_PATH}")
        return None
        
    try:
        with open(ALIEN_PATH, 'r', encoding='utf-8') as f:
            content = f.read()
            content = content.replace('</svg>', '')
            return content
    except Exception as e:
        print(f"❌ 读取错误: {e}")
        return None

def generate_test_bench():
    alien_svg_body = get_alien_content()
    if not alien_svg_body:
        return

    html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Alien Eye Tuner (Mirror Mode)</title>
    <style>
        body {{
            background-color: #222;
            color: #eee;
            font-family: 'Segoe UI', sans-serif;
            display: flex;
            height: 100vh;
            margin: 0;
            overflow: hidden;
        }}
        
        /* === 左侧预览区 === */
        .preview-area {{
            flex: 2;
            display: flex;
            justify-content: center;
            align-items: center;
            background-image: 
                linear-gradient(#333 1px, transparent 1px),
                linear-gradient(90deg, #333 1px, transparent 1px);
            background-size: 20px 20px;
            background-position: center center;
            border-right: 1px solid #444;
            position: relative;
        }}

        /* 中心辅助线 */
        .center-line {{
            position: absolute;
            width: 0;
            height: 100%;
            border-left: 1px dashed #f38ba8;
            opacity: 0.5;
            pointer-events: none;
        }}

        .icon-container {{
            width: 400px;
            height: 400px;
            /* border: 1px dashed #555; */
            display: flex;
            justify-content: center;
            align-items: center;
            position: relative;
        }}

        svg {{
            width: 100%;
            height: 100%;
            fill: #000;
        }}

        .test-eye {{
            fill: #fff;
            transform-box: fill-box;
            transform-origin: center;
            opacity: 0.85; /* 稍微透明，方便对齐边缘 */
        }}

        /* === 右侧控制面板 === */
        .controls {{
            flex: 1;
            padding: 30px;
            background: #181818;
            overflow-y: auto;
            display: flex;
            flex-direction: column;
            gap: 20px;
            box-shadow: -5px 0 15px rgba(0,0,0,0.5);
        }}

        h2 {{ margin: 0 0 10px 0; color: #89b4fa; font-size: 20px; }}
        h3 {{ margin: 0 0 15px 0; color: #f38ba8; font-size: 16px; border-bottom: 1px solid #333; padding-bottom: 5px;}}
        
        .control-group {{
            background: #252525;
            padding: 20px;
            border-radius: 12px;
        }}

        .input-row {{
            margin-bottom: 15px;
        }}

        label {{
            display: flex;
            justify-content: space-between;
            font-size: 13px;
            margin-bottom: 8px;
            color: #ccc;
            font-weight: 500;
        }}

        input[type=range] {{
            width: 100%;
            cursor: pointer;
            accent-color: #f38ba8;
        }}

        .highlight {{ color: #f38ba8; font-weight: bold; }}

        .code-output {{
            background: #111;
            color: #a6e3a1;
            font-family: 'Consolas', monospace;
            padding: 15px;
            border-radius: 8px;
            font-size: 12px;
            word-break: break-all;
            user-select: text;
            border: 1px solid #333;
        }}
        
        .copy-btn {{
            background: #89b4fa;
            border: none;
            color: #000;
            padding: 12px;
            cursor: pointer;
            font-weight: bold;
            margin-top: 10px;
            border-radius: 8px;
            width: 100%;
            transition: opacity 0.2s;
        }}
        .copy-btn:hover {{ opacity: 0.9; }}

    </style>
</head>
<body>

    <div class="preview-area">
        <div class="center-line"></div>
        <div class="icon-container">
            {alien_svg_body}
            <circle id="eye-left" class="test-eye" cx="30%" cy="55%" r="20%" />
            <circle id="eye-right" class="test-eye" cx="70%" cy="55%" r="20%" />
            </svg>
        </div>
    </div>

    <div class="controls">
        <h2>👽 镜像调试模式</h2>
        
        <div class="control-group">
            <h3>👁️ 动画预览</h3>
            <div class="input-row">
                <label>睁眼程度 (Scale 0-1)</label>
                <input type="range" id="anim-scale" min="0" max="1" step="0.01" value="1">
            </div>
        </div>

        <div class="control-group">
            <h3>📐 参数调整 (只需调一边)</h3>
            
            <div class="input-row">
                <label>X 轴位置 (离左边的距离) <span id="val-lx" class="highlight">30%</span></label>
                <input type="range" id="inp-lx" min="0" max="50" step="0.5" value="30">
                <div style="font-size: 11px; color: #666; margin-top: 2px;">右眼自动设为: <span id="val-rx">70%</span></div>
            </div>
            
            <div class="input-row">
                <label>Y 轴位置 (上下高度) <span id="val-ly" class="highlight">55%</span></label>
                <input type="range" id="inp-ly" min="0" max="100" step="0.5" value="55">
            </div>
            
            <div class="input-row">
                <label>R 半径 (圆的大小) <span id="val-lr" class="highlight">20%</span></label>
                <input type="range" id="inp-lr" min="0" max="50" step="0.5" value="20">
            </div>
        </div>

        <div class="control-group">
            <h3>📝 最终代码</h3>
            <div class="code-output" id="result-code">...</div>
            <button class="copy-btn" onclick="copyCode()">复制并粘贴回 Main.py</button>
        </div>
    </div>

    <script>
        const els = {{
            lx: document.getElementById('inp-lx'),
            ly: document.getElementById('inp-ly'),
            lr: document.getElementById('inp-lr'),
            scale: document.getElementById('anim-scale'),
            
            eyeL: document.getElementById('eye-left'),
            eyeR: document.getElementById('eye-right'),
            
            valLx: document.getElementById('val-lx'),
            valRx: document.getElementById('val-rx'),
            valLy: document.getElementById('val-ly'),
            valLr: document.getElementById('val-lr'),
            
            output: document.getElementById('result-code')
        }};

        function update() {{
            // 1. 获取数值
            const lx = parseFloat(els.lx.value);
            const ly = parseFloat(els.ly.value);
            const lr = parseFloat(els.lr.value);
            
            // 2. 自动计算镜像 (右眼 X = 100 - 左眼 X)
            const rx = 100 - lx;

            // 3. 更新界面文字
            els.valLx.innerText = lx + '%';
            els.valRx.innerText = rx + '%'; // 显示计算出的右眼数值
            els.valLy.innerText = ly + '%';
            els.valLr.innerText = lr + '%';

            // 4. 更新 SVG 属性
            els.eyeL.setAttribute('cx', lx + '%');
            els.eyeL.setAttribute('cy', ly + '%');
            els.eyeL.setAttribute('r', lr + '%');
            
            els.eyeR.setAttribute('cx', rx + '%');
            els.eyeR.setAttribute('cy', ly + '%'); // Y轴相同
            els.eyeR.setAttribute('r', lr + '%');  // 半径相同

            // 5. 更新缩放预览
            const s = els.scale.value;
            els.eyeL.style.transform = `scale(${{s}})`;
            els.eyeR.style.transform = `scale(${{s}})`;

            // 6. 生成 Python 字符串 (保持格式化)
            const code = `
                eye_covers = \"\"\"
                    <circle class="eye-cover left-eye" cx="${{lx}}%" cy="${{ly}}%" r="${{lr}}%" fill="white" transform="scale(0)" />
                    <circle class="eye-cover right-eye" cx="${{rx}}%" cy="${{ly}}%" r="${{lr}}%" fill="white" transform="scale(0)" />
                \"\"\"`.trim();
            
            els.output.innerText = code;
        }}

        // 绑定事件
        els.lx.addEventListener('input', update);
        els.ly.addEventListener('input', update);
        els.lr.addEventListener('input', update);
        els.scale.addEventListener('input', update);

        function copyCode() {{
            navigator.clipboard.writeText(els.output.innerText).then(() => {{
                const btn = document.querySelector('.copy-btn');
                const originalText = btn.innerText;
                btn.innerText = '✅ 已复制!';
                btn.style.background = '#a6e3a1';
                setTimeout(() => {{
                    btn.innerText = originalText;
                    btn.style.background = '#89b4fa';
                }}, 1500);
            }});
        }}

        // 初始化
        update();
    </script>
</body>
</html>
    """
    
    with open(OUTPUT_HTML, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"✅ 镜像调试台已生成: {OUTPUT_HTML}")
    webbrowser.open(f'file://{OUTPUT_HTML.resolve()}')

if __name__ == "__main__":
    generate_test_bench()