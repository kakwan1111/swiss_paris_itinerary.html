#!/usr/bin/env python3
"""香港 Apple Store iPhone 庫存提醒工具：本機 Flask 網頁介面版。

安全設計：只讀取頁面並提醒，不會自動加入購物袋、付款、提交訂單、
處理 CAPTCHA、繞過排隊或規避網站的反機器人措施。
"""

from __future__ import annotations

import asyncio
import os
import platform
import shutil
import subprocess
import threading
import time
from pathlib import Path
from typing import Any

from flask import Flask, jsonify, render_template_string, request
from playwright.async_api import BrowserContext, Page, async_playwright

app = Flask(__name__)

DEFAULT_URL = "https://www.apple.com/hk/shop/buy-iphone/iphone-duo"
DEFAULT_MODEL = "iPhone Duo"
DEFAULT_STORAGE = "256GB"
DEFAULT_COLOR = "Night Sky"
DEFAULT_INTERVAL = 30
PROFILE_DIR = Path(os.getenv("APPLE_PROFILE_DIR", str(Path.home() / ".apple-hk-stock-profile"))).expanduser()

IN_STOCK_TERMS = ["加入購物袋", "加到購物袋", "Add to Bag", "Available", "有貨", "立即購買", "購買"]
OUT_OF_STOCK_TERMS = ["暫時無法供應", "目前無法供應", "售罄", "Unavailable", "暫無供應", "Out of stock"]

state_lock = threading.Lock()
monitor_thread: threading.Thread | None = None
stop_event = threading.Event()
state: dict[str, Any] = {
    "running": False,
    "last_check": None,
    "available": False,
    "message": "尚未開始監控。",
    "checks": 0,
    "config": {},
}


def normalize(value: str) -> str:
    return "".join(value.split()).casefold()


def hits(text: str, terms: list[str]) -> list[str]:
    normalized = normalize(text)
    return [term for term in terms if normalize(term) in normalized]


def inspect_text(page_text: str, target_terms: list[str]) -> tuple[bool, str]:
    target_hits = hits(page_text, target_terms)
    if len(target_hits) < len(target_terms):
        return False, f"尚未完整找到目標配置（找到：{', '.join(target_hits) or '無'}）"

    out_hits = hits(page_text, OUT_OF_STOCK_TERMS)
    in_hits = hits(page_text, IN_STOCK_TERMS)
    if out_hits and not in_hits:
        return False, f"偵測到無貨訊號：{', '.join(out_hits)}"
    if in_hits:
        return True, f"目標配置及可購買訊號：{', '.join(in_hits)}"
    return False, "找到目標配置，但未找到明確可購買訊號"


def notify(title: str, message: str) -> None:
    print(f"\a\n{title}: {message}")
    try:
        if platform.system() == "Linux" and shutil.which("notify-send"):
            subprocess.run(["notify-send", title, message], check=False, timeout=5)
        elif platform.system() == "Darwin" and shutil.which("osascript"):
            subprocess.run(
                ["osascript", "-e", f'display notification "{message}" with title "{title}"'],
                check=False,
                timeout=5,
            )
    except Exception:
        pass


def update_state(**values: Any) -> None:
    with state_lock:
        state.update(values)


async def launch_browser(playwright: Any, profile_dir: Path) -> BrowserContext:
    """Prefer the Microsoft Edge already included with Windows.

    This keeps the packaged EXE small and avoids requiring a separate browser
    download. If Edge is unavailable, fall back to bundled/default Chromium.
    """
    common = dict(
        user_data_dir=str(profile_dir),
        headless=False,
        locale="zh-HK",
        timezone_id="Asia/Hong_Kong",
        viewport={"width": 1440, "height": 1000},
    )
    try:
        return await playwright.chromium.launch_persistent_context(channel="msedge", **common)
    except Exception:
        return await playwright.chromium.launch_persistent_context(**common)


async def monitor(config: dict[str, Any]) -> None:
    target_terms = [config["model"], config["storage"], config["color"]]
    interval = max(15, int(config["interval"]))
    profile_dir = Path(config["profile_dir"]).expanduser()
    profile_dir.mkdir(parents=True, exist_ok=True)

    async with async_playwright() as playwright:
        context: BrowserContext = await launch_browser(playwright, profile_dir)

        page: Page = context.pages[0] if context.pages else await context.new_page()
        try:
            await page.goto(config["url"], wait_until="domcontentloaded", timeout=60_000)
            try:
                await page.wait_for_load_state("networkidle", timeout=15_000)
            except Exception:
                pass

            while not stop_event.is_set():
                try:
                    text = await page.locator("body").inner_text(timeout=15_000)
                    available, message = inspect_text(text, target_terms)
                    count = state["checks"] + 1
                    update_state(
                        last_check=time.strftime("%Y-%m-%d %H:%M:%S"),
                        available=available,
                        message=message,
                        checks=count,
                    )
                    if available:
                        notify("Apple 香港庫存提醒", f"{config['model']} / {config['storage']} / {config['color']}：{message}")
                        update_state(message=f"疑似有貨：{message}。請在瀏覽器內手動確認。")
                        # 發現疑似有貨後暫停，避免重複通知和重新整理。
                        break
                except Exception as exc:
                    update_state(last_check=time.strftime("%Y-%m-%d %H:%M:%S"), message=f"讀取頁面失敗：{exc}")

                # 分段等待，令停止按鈕最多約 1 秒內生效。
                for _ in range(interval):
                    if stop_event.is_set():
                        break
                    await asyncio.sleep(1)
                if not stop_event.is_set():
                    try:
                        await page.reload(wait_until="domcontentloaded", timeout=60_000)
                    except Exception as exc:
                        update_state(message=f"重新載入失敗，將重試：{exc}")
        finally:
            await context.close()


def worker(config: dict[str, Any]) -> None:
    update_state(running=True, available=False, checks=0, message="瀏覽器啟動中……", config=config)
    try:
        asyncio.run(monitor(config))
        if stop_event.is_set():
            update_state(message="監控已停止。")
        elif state["available"]:
            update_state(message="已暫停監控；請手動確認瀏覽器內的庫存及配置。")
        else:
            update_state(message="監控已結束。")
    except Exception as exc:
        update_state(message=f"監控錯誤：{exc}")
    finally:
        update_state(running=False)


@app.get("/")
def index():
    return render_template_string(TEMPLATE, state=state_snapshot())


@app.get("/api/status")
def api_status():
    return jsonify(state_snapshot())


@app.post("/api/start")
def api_start():
    global monitor_thread
    with state_lock:
        if state["running"]:
            return jsonify({"ok": False, "error": "監控已在執行。"}), 409

    data = request.get_json(silent=True) or request.form
    try:
        interval = max(15, int(data.get("interval", DEFAULT_INTERVAL)))
    except (TypeError, ValueError):
        return jsonify({"ok": False, "error": "檢查間隔必須是整數。"}), 400

    config = {
        "url": (data.get("url") or DEFAULT_URL).strip(),
        "model": (data.get("model") or DEFAULT_MODEL).strip(),
        "storage": (data.get("storage") or DEFAULT_STORAGE).strip(),
        "color": (data.get("color") or DEFAULT_COLOR).strip(),
        "interval": interval,
        "profile_dir": str(PROFILE_DIR),
    }
    if not config["url"].startswith("https://www.apple.com/"):
        return jsonify({"ok": False, "error": "為安全起見，網址必須是 https://www.apple.com/ 開頭。"}), 400

    stop_event.clear()
    monitor_thread = threading.Thread(target=worker, args=(config,), daemon=True)
    monitor_thread.start()
    return jsonify({"ok": True, "message": "監控已啟動。"})


@app.post("/api/stop")
def api_stop():
    if not state_snapshot()["running"]:
        return jsonify({"ok": False, "error": "目前沒有執行中的監控。"}), 409
    stop_event.set()
    return jsonify({"ok": True, "message": "正在停止監控……"})


def state_snapshot() -> dict[str, Any]:
    with state_lock:
        return dict(state)


TEMPLATE = r"""<!doctype html>
<html lang="zh-HK">
<head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Apple 香港庫存監控</title>
<style>
:root{font-family:system-ui,-apple-system,"Segoe UI",sans-serif;color:#172033;background:#f4f7fb}
body{margin:0}.shell{max-width:980px;margin:0 auto;padding:42px 20px}.eyebrow{color:#58708f;font-size:.78rem;letter-spacing:.14em;text-transform:uppercase;font-weight:700}.hero{display:flex;justify-content:space-between;gap:24px;align-items:end;margin-bottom:28px}h1{font-size:clamp(2rem,5vw,4rem);line-height:.98;margin:10px 0 0;letter-spacing:-.06em}.lead{max-width:560px;color:#58708f;line-height:1.6}.panel{background:#fff;border:1px solid #dce5ef;border-radius:20px;padding:24px;box-shadow:0 14px 40px #28415c12}.form{display:grid;grid-template-columns:repeat(2,1fr);gap:16px}.full{grid-column:1/-1}label{display:grid;gap:7px;font-size:.86rem;font-weight:700;color:#415775}input{width:100%;box-sizing:border-box;border:1px solid #cdd9e6;border-radius:10px;padding:12px 13px;font:inherit;color:#172033;background:#fbfdff}button{border:0;border-radius:10px;padding:12px 17px;font:inherit;font-weight:800;cursor:pointer}.primary{background:#172033;color:#fff}.secondary{background:#e9f0f7;color:#172033}.actions{display:flex;gap:10px;flex-wrap:wrap;margin-top:20px}.notice{margin-top:20px;padding:14px;border-radius:12px;background:#fff7e6;color:#7c5100;line-height:1.5}.status{margin-top:22px;display:grid;grid-template-columns:160px 1fr;gap:15px;align-items:start}.badge{display:inline-block;padding:7px 10px;border-radius:999px;background:#e7edf5;color:#4d6684;font-weight:800;font-size:.85rem}.badge.live{background:#dff7e8;color:#17633b}.badge.alert{background:#fff0c7;color:#7a4d00}.meta{color:#5b718c;font-size:.92rem;line-height:1.7}.log{margin-top:20px;background:#f6f9fc;border-radius:12px;padding:14px;color:#314761;min-height:44px;white-space:pre-wrap}.foot{margin-top:22px;font-size:.85rem;color:#70839a;line-height:1.6}@media(max-width:700px){.hero{display:block}.form{grid-template-columns:1fr}.status{grid-template-columns:1fr}}
</style></head>
<body><main class="shell">
<div class="eyebrow">Local browser assistant · Hong Kong</div>
<div class="hero"><div><h1>Apple 庫存監控</h1><p class="lead">監測指定 iPhone 配置，發現疑似有貨時提醒你。購物袋、付款、驗證碼及提交訂單全部保留由你手動操作。</p></div></div>
<section class="panel"><form id="configForm"><div class="form">
<label class="full">Apple 產品頁面 URL<input name="url" value="{{ state.config.get('url', 'https://www.apple.com/hk/shop/buy-iphone/iphone-duo') }}"></label>
<label>型號<input name="model" value="{{ state.config.get('model', 'iPhone Duo') }}"></label>
<label>容量<input name="storage" value="{{ state.config.get('storage', '256GB') }}"></label>
<label>顏色<input name="color" value="{{ state.config.get('color', 'Night Sky') }}"></label>
<label>檢查間隔（秒，最少 15）<input type="number" min="15" name="interval" value="{{ state.config.get('interval', 30) }}"></label>
</div><div class="actions"><button class="primary" type="submit">啟動監控</button><button class="secondary" type="button" id="stop">停止監控</button></div></form>
<div class="notice">安全提示：此工具不會自動購買、付款、處理 CAPTCHA、繞過排隊或規避 Apple 的反機器人措施。請只在自己的瀏覽器中手動登入和填寫資料。</div>
<div class="status"><div><span id="badge" class="badge">尚未開始</span></div><div class="meta">檢查次數：<b id="checks">0</b><br>最後檢查：<b id="last">—</b><br>目標：<b id="target">—</b></div></div>
<div class="log" id="message">尚未開始監控。</div><p class="foot">瀏覽器會使用本機資料夾 <code>~/.apple-hk-stock-profile</code> 保存你手動建立的登入狀態。請勿分享或提交該資料夾。</p>
</section></main>
<script>
const $=s=>document.querySelector(s); const form=$('#configForm');
async function call(path, options={}){const r=await fetch(path,{headers:{'Content-Type':'application/json'},...options});const j=await r.json();if(!r.ok)throw Error(j.error||'請求失敗');return j}
function render(s){const b=$('#badge'); b.textContent=s.running?'監控中':(s.available?'疑似有貨':'已停止');b.className='badge '+(s.running?'live':(s.available?'alert':''));$('#checks').textContent=s.checks||0;$('#last').textContent=s.last_check||'—';$('#message').textContent=s.message||'';if(s.config){$('#target').textContent=[s.config.model,s.config.storage,s.config.color].join(' / ')}}
async function refresh(){try{render(await (await fetch('/api/status')).json())}catch(e){$('#message').textContent=e.message}}
form.addEventListener('submit',async e=>{e.preventDefault();const data=Object.fromEntries(new FormData(form));try{await call('/api/start',{method:'POST',body:JSON.stringify(data)});await refresh()}catch(err){alert(err.message)}});
$('#stop').addEventListener('click',async()=>{try{await call('/api/stop',{method:'POST'});await refresh()}catch(err){alert(err.message)}});refresh();setInterval(refresh,2000);
</script></body></html>"""


if __name__ == "__main__":
    host = os.getenv("HOST", "127.0.0.1")
    port = int(os.getenv("PORT", "5050"))
    print(f"開啟 http://{host}:{port}")
    import webbrowser
    webbrowser.open(f"http://{host}:{port}")
    print("安全限制：不會自動付款、提交訂單、處理 CAPTCHA 或繞過反機器人機制。")
    app.run(host=host, port=port, debug=False, threaded=True)
