import os
import webbrowser
from pathlib import Path
import time

# ================= 调试参数配置区域 (修改这里) =================

# 1. 圆形参数 (Circle)
# cx: 水平中心 (50%是正中，>50%向右，<50%向左)
# cy: 垂直中心 (50%是正中，>50%向下，<50%向上)
CIRCLE_CX = "50%"      
CIRCLE_CY = "47.5%"    
CIRCLE_R  = "56%"      

# 2. 方形参数 (Rectangle)
RECT_X = "-0.5%"       
RECT_Y = "23.25%"      
RECT_W = "101%"        
RECT_H = "76.5%"       

# ==========================================================

BASE_DIR = Path(__file__).parent
ASSETS_DIR = BASE_DIR / "assets" / "icons"
# 优先查找 h_reel，没有再找 a_reel
HUMAN_PATH = ASSETS_DIR / "h_reel" / "human.svg"
if not HUMAN_PATH.exists():
    HUMAN_PATH = ASSETS_DIR / "a_reel" / "human.svg"

OUTPUT_HTML = BASE_DIR / "debug_human_only.html"

def get_human_svg():
    if not HUMAN_PATH.exists():
        return "Error: human.svg not found"
    try:
        with open(HUMAN_PATH, 'r', encoding='utf-8') as f:
            content = f.read()
            # 注入参数
            v_shapes = f"""
                <circle class="v-shape v-circle" cx="{CIRCLE_CX}" cy="{CIRCLE_CY}" r="{CIRCLE_R}" />
                <rect class="v-shape v-rect" x="{RECT_X}" y="{RECT_Y}" width="{RECT_W}" height="{RECT_H}" />
            """
            # 替换闭合标签前的内容
            content = content.replace('</svg>', f'{v_shapes}</svg>')
            return content
    except Exception as e:
        return f"Error: {e}"

def generate_debug_page():
    svg_content = get_human_svg()
    
    html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <style>
        body {{
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
            background-color: #f4f4f4; /* 保持项目背景色 */
            font-family: monospace;
        }}

        .debug-container {{
            position: relative;
            width: 300px;  /* 放大一点方便看细节 */
            height: 300px;
            border: 1px dashed #ccc; /* 容器边界 */
        }}

        /* 十字辅助线 (红色) - 标示绝对中心 */
        .guide-x {{ position: absolute; top: 50%; left: 0; right: 0; height: 1px; background: rgba(255,0,0,0.3); z-index: 0; }}
        .guide-y {{ position: absolute; left: 50%; top: 0; bottom: 0; width: 1px; background: rgba(255,0,0,0.3); z-index: 0; }}

        .icon-box {{
            width: 100%;
            height: 100%;
            display: flex;
            justify-content: center;
            align-items: center;
            position: relative;
            z-index: 1;
        }}

        svg {{
            width: 70%; 
            height: 70%; /* 保持项目中的比例 */
            fill: #000;
            overflow: visible !important; /* 关键：允许溢出 */
        }}

        /* === 动画定义 === */
        .v-shape {{
            fill: none; 
            stroke: #000; 
            stroke-width: 2px;
            stroke-dasharray: 400; 
            stroke-dashoffset: 400; 
            opacity: 1; 
            vector-effect: non-scaling-stroke; 
            stroke-linecap: round;
        }}
        
        .v-circle {{ transform-origin: center; transform: rotate(-135deg); }}

        /* 激活时的类 */
        .draw-circle .v-circle {{ animation: draw-stroke 1.6s linear forwards; }}
        .draw-square .v-rect {{ animation: draw-stroke 1.6s linear forwards; }}
        
        @keyframes draw-stroke {{ to {{ stroke-dashoffset: 0; }} }}

    </style>
</head>
<body>

    <div class="debug-container">
        <div class="guide-x"></div>
        <div class="guide-y"></div>
        <div class="icon-box" id="target">
            {svg_content}
        </div>
    </div>

    <script>
        const el = document.getElementById('target');
        
        function playAnimation() {{
            // 重置
            el.classList.remove('draw-circle', 'draw-square');
            void el.offsetWidth; // 强制重绘
            
            // 播放
            el.classList.add('draw-square');
            setTimeout(() => {{
                el.classList.add('draw-circle');
            }}, 1000); // 方框画完后画圆
        }}

        // 初始播放
        setTimeout(playAnimation, 500);

        // 循环播放方便调试
        setInterval(playAnimation, 4000);
    </script>
</body>
</html>
    """
    
    with open(OUTPUT_HTML, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f"Debug file generated: {OUTPUT_HTML}")
    webbrowser.open(f'file://{OUTPUT_HTML.resolve()}')

if __name__ == "__main__":
    generate_debug_page()