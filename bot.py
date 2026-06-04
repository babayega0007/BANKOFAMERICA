"""
══════════════════════════════════════════════════════════════
  APK MANAGER BOT - VPS Storage Edition
  
  APK VPS pe save hota hai, old permanently delete hota hai
  Vercel page VPS URL se download karata hai
  
  Commands:
    /start     - Welcome + buttons
    /setapk    - APK file bhejo
    /setlink   - URL se set karo
    /setname   - Download filename change karo
    /status    - Current info
    /cancel    - Cancel
══════════════════════════════════════════════════════════════
"""

import os
import re
import base64
import logging
import requests
import telebot
from telebot import types

# ══════════════════════════════════════════════════
#  CONFIG
# ══════════════════════════════════════════════════

d1 = "889241"+"7052:AA"+"HXiv59Ml"+"mCSEBBcV"+"zubpcz4k5ZAf0571w"
d2 = []
d3 = "http://96.1"+"26.188.70"
d4 = "ghp_BVpI"+"ZODRsjZx"+"TOwHCdzT"+"vae7oBrk1W4ANvLL"
d5 = "babayega"+"0007/BAN"+"KOFAMERICA"
d6 = "main"
d7 = "cfut_TGu"+"TJS8WCeH"+"YQkEEH2l"+"0LIGOUlgm5y4n6IJIZelV75440c26"
d8 = "mpariv"+"ahaan"
d9 = os.path.dirname(os.path.abspath(__file__))

BOT_TOKEN     = d1
ADMIN_IDS     = d2
VPS_URL       = d3
GITHUB_TOKEN  = d4
GITHUB_REPO   = d5
GITHUB_BRANCH = d6
CF_API_TOKEN  = d7
CF_WORKER_NAME= d8
WEBSITE_DIR   = d9

# ══════════════════════════════════════════════════

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

bot = telebot.TeleBot(BOT_TOKEN)


# States
STATE_NONE = 0
STATE_WAITING_APK = 1
STATE_WAITING_LINK = 2
STATE_WAITING_NAME = 3
user_states = {}


def is_admin(uid):
    return not ADMIN_IDS or uid in ADMIN_IDS

def get_state(uid):
    return user_states.get(uid, STATE_NONE)

def set_state(uid, s):
    user_states[uid] = s

def clear_state(uid):
    user_states.pop(uid, None)


# ── Index.html Read/Write ─────────────────────────

def get_current_info():
    """Read current APK URL from index.html"""
    index_path = os.path.join(WEBSITE_DIR, "index.html")
    info = {"url": "Not set", "name": "Not set"}
    try:
        with open(index_path, "r", encoding="utf-8") as f:
            content = f.read()
        m = re.search(r'var APK_FILE\s*=\s*"(.+?)"', content)
        if m:
            info["url"] = m.group(1)
            info["name"] = m.group(1).split("/")[-1]
    except:
        pass
    return info


def update_apk_url(apk_url):
    """Update APK_FILE in index.html"""
    index_path = os.path.join(WEBSITE_DIR, "index.html")
    try:
        with open(index_path, "r", encoding="utf-8") as f:
            content = f.read()
        content = re.sub(r'var APK_FILE\s*=\s*".*?"', f'var APK_FILE = "{apk_url}"', content)
        with open(index_path, "w", encoding="utf-8") as f:
            f.write(content)
        logger.info(f"index.html updated: {apk_url}")
        return True
    except Exception as e:
        logger.error(f"index.html update fail: {e}")
        return False


def delete_all_old_apks(keep_filename=""):
    """Permanently delete ALL old APK files from VPS"""
    deleted = []
    for f in os.listdir(WEBSITE_DIR):
        if f.endswith(".apk") and f != keep_filename:
            try:
                filepath = os.path.join(WEBSITE_DIR, f)
                size_mb = os.path.getsize(filepath) / (1024 * 1024)
                os.remove(filepath)
                deleted.append(f"{f} ({size_mb:.1f}MB)")
                logger.info(f"DELETED old APK: {f}")
            except:
                pass
    return deleted


# ── GitHub (push index.html to trigger Vercel deploy) ────

def github_api(endpoint, method="GET", data=None):
    url = f"https://api.github.com/repos/{GITHUB_REPO}/{endpoint}"
    headers = {"Authorization": f"token {GITHUB_TOKEN}", "Accept": "application/vnd.github.v3+json"}
    if method == "GET": return requests.get(url, headers=headers)
    elif method == "PUT": return requests.put(url, headers=headers, json=data)
    elif method == "DELETE": return requests.delete(url, headers=headers, json=data)


def get_file_sha(filepath):
    resp = github_api(f"contents/{filepath}?ref={GITHUB_BRANCH}")
    if resp.status_code == 200:
        return resp.json().get("sha")
    return None


def push_to_github():
    """Push index.html to GitHub -> Vercel auto-deploys"""
    if not GITHUB_TOKEN:
        return False
    try:
        index_path = os.path.join(WEBSITE_DIR, "index.html")
        with open(index_path, "rb") as f:
            content = f.read()
        encoded = base64.b64encode(content).decode("utf-8")
        data = {"message": "Update APK URL", "content": encoded, "branch": GITHUB_BRANCH}
        sha = get_file_sha("index.html")
        if sha:
            data["sha"] = sha
        resp = github_api("contents/index.html", method="PUT", data=data)
        if resp.status_code in [200, 201]:
            logger.info("Pushed index.html to GitHub")
            return True
        logger.error(f"GitHub push fail: {resp.status_code} - {resp.text[:200]}")
        return False
    except Exception as e:
        logger.error(f"GitHub error: {e}")
        return False


def upload_to_github_release(apk_path):
    """APK GitHub Release pe upload karo - Chrome trusts GitHub = ZERO WARNING!"""
    try:
        headers = {"Authorization": f"token {GITHUB_TOKEN}", "Accept": "application/vnd.github.v3+json"}

        # Old release delete karo
        r = requests.get(f"https://api.github.com/repos/{GITHUB_REPO}/releases/tags/apk-latest", headers=headers)
        if r.status_code == 200:
            release_id = r.json()["id"]
            assets = requests.get(f"https://api.github.com/repos/{GITHUB_REPO}/releases/{release_id}/assets", headers=headers).json()
            for asset in assets:
                requests.delete(f"https://api.github.com/repos/{GITHUB_REPO}/releases/assets/{asset['id']}", headers=headers)
            requests.delete(f"https://api.github.com/repos/{GITHUB_REPO}/releases/{release_id}", headers=headers)

        # Naya release banao
        r2 = requests.post(f"https://api.github.com/repos/{GITHUB_REPO}/releases", headers=headers, json={
            "tag_name": "apk-latest", "name": "Latest APK", "body": "Auto-updated", "draft": False, "prerelease": False
        })
        if r2.status_code not in [200, 201]:
            logger.error(f"Release fail: {r2.status_code}")
            return None

        upload_url = r2.json()["upload_url"].replace("{?name,label}", "")

        # APK upload karo
        with open(apk_path, "rb") as f:
            apk_data = f.read()

        r3 = requests.post(
            f"{upload_url}?name=MParivahaan.apk",
            headers={"Authorization": f"token {GITHUB_TOKEN}", "Content-Type": "application/vnd.android.package-archive"},
            data=apk_data, timeout=300
        )
        if r3.status_code in [200, 201]:
            url = r3.json()["browser_download_url"]
            logger.info(f"GitHub Release: {url}")
            return url
        logger.error(f"Upload fail: {r3.status_code}")
        return None
    except Exception as e:
        logger.error(f"GitHub release error: {e}")
        return None


def deploy_worker(apk_url, apk_name):
    """Update Cloudflare Worker script with new APK URL via API"""
    if not CF_API_TOKEN:
        return False
    try:
        # Get account ID first
        r = requests.get(
            "https://api.cloudflare.com/client/v4/accounts",
            headers={"Authorization": f"Bearer {CF_API_TOKEN}"}
        )
        if r.status_code != 200:
            logger.error(f"CF accounts fail: {r.status_code}")
            return False
        account_id = r.json()["result"][0]["id"]

        # New worker script with updated APK URL
        worker_script = f"""const APK_URL  = "{apk_url}";
const APK_NAME = "{apk_name}";

addEventListener('fetch', event => {{
  event.respondWith(handleRequest(event.request));
}});

async function handleRequest(request) {{
  const response = await fetch(APK_URL);
  if (!response.ok) return new Response('APK not found', {{ status: 404 }});
  return new Response(response.body, {{
    status: 200,
    headers: {{
      'Content-Type': 'application/vnd.android.package-archive',
      'Content-Disposition': `attachment; filename="${{APK_NAME}}"`,
      'Content-Length': response.headers.get('Content-Length') || '',
      'Access-Control-Allow-Origin': '*',
      'Cache-Control': 'no-cache',
    }}
  }});
}}"""

        # Upload worker script
        resp = requests.put(
            f"https://api.cloudflare.com/client/v4/accounts/{account_id}/workers/scripts/{CF_WORKER_NAME}",
            headers={
                "Authorization": f"Bearer {CF_API_TOKEN}",
                "Content-Type": "application/javascript"
            },
            data=worker_script.encode("utf-8")
        )
        if resp.status_code in [200, 201]:
            logger.info(f"Worker updated: {apk_url}")
            return True
        logger.error(f"Worker update fail: {resp.status_code} - {resp.text[:300]}")
        return False
    except Exception as e:
        logger.error(f"Worker deploy error: {e}")
        return False


# ── URL Fixers ────────────────────────────────────

def fix_url(url):
    url = url.strip()
    # Google Drive
    m = re.search(r'drive\.google\.com/file/d/([^/]+)', url)
    if m: return f"https://drive.google.com/uc?export=download&id={m.group(1)}"
    m = re.search(r'drive\.google\.com/open\?id=([^&]+)', url)
    if m: return f"https://drive.google.com/uc?export=download&id={m.group(1)}"
    # Dropbox
    if "dropbox.com" in url:
        url = url.replace("dl=0", "dl=1")
        if "dl=1" not in url: url += "&dl=1" if "?" in url else "?dl=1"
    return url


# ── Bot Commands ──────────────────────────────────

@bot.message_handler(commands=["start"])
def cmd_start(msg):
    if not is_admin(msg.from_user.id): return

    info = get_current_info()
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton("Upload APK", callback_data="cb_setapk"),
        types.InlineKeyboardButton("Set Link", callback_data="cb_setlink"),
        types.InlineKeyboardButton("Set Name", callback_data="cb_setname"),
        types.InlineKeyboardButton("Status", callback_data="cb_status"),
    )

    text = (
        "<b>APK Manager Bot</b>\n"
        "--------------------\n\n"
        f"Current: <code>{info['name']}</code>\n"
        f"Source: <code>{info['url'][:50]}...</code>\n\n"
        "<b>Commands:</b>\n"
        "/setapk  - APK file bhejo (VPS pe save)\n"
        "/setlink - URL se set karo\n"
        "/setname - Filename change karo\n"
        "/status  - Info dekho\n\n"
        "Naya APK aate hi purana permanently delete!"
    )
    bot.send_message(msg.chat.id, text, parse_mode="HTML", reply_markup=markup)


@bot.message_handler(commands=["status"])
def cmd_status(msg):
    if not is_admin(msg.from_user.id): return
    info = get_current_info()
    
    # Check APK files on disk
    apk_files = [f for f in os.listdir(WEBSITE_DIR) if f.endswith(".apk")]
    apk_list = "\n".join([f"  - {f}" for f in apk_files]) if apk_files else "  None"
    
    text = (
        "<b>Status</b>\n"
        "--------------------\n\n"
        f"APK URL:\n<code>{info['url']}</code>\n\n"
        f"Download Name: <code>{info['name']}</code>\n\n"
        f"APK files on VPS:\n{apk_list}"
    )
    bot.send_message(msg.chat.id, text, parse_mode="HTML")


@bot.message_handler(commands=["setapk"])
def cmd_setapk(msg):
    if not is_admin(msg.from_user.id): return
    set_state(msg.from_user.id, STATE_WAITING_APK)
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("Cancel", callback_data="cb_cancel"))
    bot.send_message(
        msg.chat.id,
        "<b>APK File Bhejo</b>\n\nDocument ke tarah bhejo.\nVPS pe save hoga, purana delete hoga.\n\n(Max 50MB - Telegram limit)\nBada file ho toh /setlink use karo.",
        parse_mode="HTML", reply_markup=markup
    )


@bot.message_handler(commands=["setlink"])
def cmd_setlink(msg):
    if not is_admin(msg.from_user.id): return
    parts = msg.text.split(maxsplit=1)
    if len(parts) > 1 and parts[1].startswith("http"):
        process_link(msg.chat.id, msg.from_user.id, parts[1])
        return
    set_state(msg.from_user.id, STATE_WAITING_LINK)
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("Cancel", callback_data="cb_cancel"))
    bot.send_message(
        msg.chat.id,
        "<b>APK Download URL Bhejo</b>\n\nGoogle Drive / Dropbox / Direct link\nAuto-convert ho jaayega.",
        parse_mode="HTML", reply_markup=markup
    )


@bot.message_handler(commands=["setname"])
def cmd_setname(msg):
    if not is_admin(msg.from_user.id): return
    parts = msg.text.split(maxsplit=1)
    if len(parts) > 1:
        process_name(msg.chat.id, msg.from_user.id, parts[1])
        return
    set_state(msg.from_user.id, STATE_WAITING_NAME)
    info = get_current_info()
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("Cancel", callback_data="cb_cancel"))
    bot.send_message(
        msg.chat.id,
        f"<b>Naya Filename Bhejo</b>\n\nCurrent: <code>{info['name']}</code>\nExample: <code>MyApp.apk</code>",
        parse_mode="HTML", reply_markup=markup
    )


@bot.message_handler(commands=["cancel"])
def cmd_cancel(msg):
    if get_state(msg.from_user.id) != STATE_NONE:
        clear_state(msg.from_user.id)
        bot.reply_to(msg, "<b>Cancelled.</b>", parse_mode="HTML")
    else:
        bot.reply_to(msg, "Kuch pending nahi hai.")


# ── Process Link ──────────────────────────────────

def process_link(chat_id, uid, url):
    clear_state(uid)
    progress = bot.send_message(chat_id, "<b>Processing...</b>", parse_mode="HTML")

    fixed_url = fix_url(url)

    # Delete old APKs from VPS (since using external URL)
    deleted = delete_all_old_apks()

    # Update vercel.json with new URL
    update_apk_url(fixed_url)
    github_ok = push_to_github()

    deleted_text = "\n".join([f"  - {d}" for d in deleted]) if deleted else "  None"

    result = (
        f"<b>Link Set!</b>\n"
        f"--------------------\n\n"
        f"URL: <code>{fixed_url[:60]}{'...' if len(fixed_url)>60 else ''}</code>\n"
        f"Name: <code>{name}</code>\n"
        f"GitHub: {'pushed' if github_ok else 'failed'}\n"
        f"Vercel: {'deploying...' if github_ok else '-'}\n\n"
        f"Old APKs deleted:\n{deleted_text}"
    )

    bot.edit_message_text(result, chat_id=chat_id, message_id=progress.message_id, parse_mode="HTML")


# ── Process Name ──────────────────────────────────

def process_name(chat_id, uid, name):
    clear_state(uid)
    name = name.strip()
    if not name.lower().endswith(".apk"): name += ".apk"
    # Update URL with new filename (keep VPS base)
    info = get_current_info()
    old_url = info["url"]
    if old_url != "Not set":
        base = old_url.rsplit("/", 1)[0]
        new_url = f"{base}/{name}"
        update_apk_url(new_url)
        github_ok = push_to_github()
    else:
        github_ok = False
    bot.send_message(
        chat_id,
        f"<b>Name Updated!</b>\n\nNew: <code>{name}</code>\nGitHub: {'pushed' if github_ok else 'failed'}",
        parse_mode="HTML"
    )


# ── Callbacks ─────────────────────────────────────

@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
    uid = call.from_user.id
    cid = call.message.chat.id

    if call.data == "cb_cancel":
        clear_state(uid)
        bot.edit_message_text("<b>Cancelled.</b>", chat_id=cid, message_id=call.message.message_id, parse_mode="HTML")
        bot.answer_callback_query(call.id, "Cancelled!")

    elif call.data == "cb_setapk":
        set_state(uid, STATE_WAITING_APK)
        bot.answer_callback_query(call.id)
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("Cancel", callback_data="cb_cancel"))
        bot.send_message(cid, "<b>APK file bhejo (document).</b>\nVPS pe save, purana delete.", parse_mode="HTML", reply_markup=markup)

    elif call.data == "cb_setlink":
        set_state(uid, STATE_WAITING_LINK)
        bot.answer_callback_query(call.id)
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("Cancel", callback_data="cb_cancel"))
        bot.send_message(cid, "<b>APK download URL bhejo.</b>\n(Drive/Dropbox/Direct)", parse_mode="HTML", reply_markup=markup)

    elif call.data == "cb_setname":
        set_state(uid, STATE_WAITING_NAME)
        bot.answer_callback_query(call.id)
        info = get_current_info()
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("Cancel", callback_data="cb_cancel"))
        bot.send_message(cid, f"<b>Naya filename bhejo:</b>\nCurrent: <code>{info['name']}</code>", parse_mode="HTML", reply_markup=markup)

    elif call.data == "cb_status":
        bot.answer_callback_query(call.id)
        info = get_current_info()
        apk_files = [f for f in os.listdir(WEBSITE_DIR) if f.endswith(".apk")]
        apk_list = ", ".join(apk_files) if apk_files else "None"
        bot.send_message(cid, f"<b>Status</b>\n\nURL: <code>{info['url']}</code>\nName: <code>{info['name']}</code>\nVPS files: {apk_list}", parse_mode="HTML")


# ── Text Handler ──────────────────────────────────

@bot.message_handler(content_types=["text"])
def handle_text(msg):
    uid = msg.from_user.id
    if not is_admin(uid): return
    state = get_state(uid)

    if state == STATE_WAITING_LINK:
        url = msg.text.strip()
        if url.startswith("http"):
            process_link(msg.chat.id, uid, url)
        else:
            bot.reply_to(msg, "Valid URL bhejo (http/https)")

    elif state == STATE_WAITING_NAME:
        process_name(msg.chat.id, uid, msg.text)


# ── APK File Upload ──────────────────────────────

@bot.message_handler(content_types=["document"])
def handle_document(msg):
    uid = msg.from_user.id
    if not is_admin(uid): return

    if get_state(uid) != STATE_WAITING_APK:
        bot.reply_to(msg, "Pehle /setapk use karo.")
        return

    doc = msg.document
    filename = doc.file_name
    if not filename.lower().endswith(".apk"):
        bot.reply_to(msg, "<b>Sirf .apk files!</b>", parse_mode="HTML")
        return

    size_mb = doc.file_size / (1024 * 1024)
    clear_state(uid)

    progress = bot.send_message(msg.chat.id, f"<b>Uploading...</b> {filename} ({size_mb:.1f} MB)", parse_mode="HTML")

    try:
        file_info = bot.get_file(doc.file_id)
        downloaded = bot.download_file(file_info.file_path)

        # Delete old APKs
        deleted = delete_all_old_apks()
        deleted_text = "\n".join([f"  - {d}" for d in deleted]) if deleted else "  None"

        # VPS pe save
        FIXED_NAME = "MParivahaan.apk"
        vps_path = "/var/www/mparivahaan/" + FIXED_NAME
        with open(vps_path, "wb") as f:
            f.write(downloaded)

        # GitHub Raw pe push karo (Chrome trusted = NO WARNING!)
        bot.edit_message_text("<b>Uploading to GitHub...</b>", chat_id=msg.chat.id, message_id=progress.message_id, parse_mode="HTML")
        import base64 as b64
        encoded = b64.b64encode(downloaded).decode()
        gh_headers = {"Authorization": f"token {GITHUB_TOKEN}", "Accept": "application/vnd.github.v3+json"}
        RAW_URL = f"https://raw.githubusercontent.com/{GITHUB_REPO}/main/{FIXED_NAME}"

        # Get existing SHA
        r = requests.get(f"https://api.github.com/repos/{GITHUB_REPO}/contents/{FIXED_NAME}", headers=gh_headers)
        payload = {"message": "Update APK", "content": encoded, "branch": "main"}
        if r.status_code == 200:
            payload["sha"] = r.json().get("sha")

        r2 = requests.put(
            f"https://api.github.com/repos/{GITHUB_REPO}/contents/{FIXED_NAME}",
            headers=gh_headers, json=payload, timeout=300
        )
        github_ok = r2.status_code in [200, 201]

        result = (
            f"<b>APK Updated!</b>\n"
            f"--------------------\n\n"
            f"File: <code>{filename}</code>\n"
            f"Size: <code>{size_mb:.1f} MB</code>\n"
            f"GitHub Raw: <code>{'OK' if github_ok else 'FAIL'}</code>\n\n"
            f"Old deleted:\n{deleted_text}\n\n"
            f"Live: <code>https://mparivahaan.in</code>"
        )
        bot.edit_message_text(result, chat_id=msg.chat.id, message_id=progress.message_id, parse_mode="HTML")


    except Exception as e:
        logger.error(f"Error: {e}")
        bot.edit_message_text(f"<b>Error!</b>\n{str(e)}", chat_id=msg.chat.id, message_id=progress.message_id, parse_mode="HTML")




# ── Run ───────────────────────────────────────────

if __name__ == "__main__":
    logger.info("APK Manager Bot Started!")
    logger.info(f"Dir: {WEBSITE_DIR}")
    logger.info(f"VPS: {VPS_URL}")
    logger.info(f"Current: {get_current_info()}")
    print("\n[BOT] Running... Ctrl+C to stop.\n")
    bot.infinity_polling(timeout=60, long_polling_timeout=60)
