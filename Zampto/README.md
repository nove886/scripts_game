# 🎮 Zampto-Renew
自动续期 Zampto 免费游戏服务器，每隔两天定时运行。

## 🔐 Secrets 配置
**Settings → Secrets and variables → Actions → New repository secret** 添加以下变量：

| Secret 名 | 说明 | 示例 |
|---|---|---|
| `ZAMPTO_ACCOUNT` | 🧾 Zampto 登录账号和密码，用英文逗号分隔 | `myaccount@example.com,mypassword` |
| `GOST_PROXY` | 🌐 Gost 代理地址 | `socks5://user:pass@1.2.3.4:1080` |
| `TG_BOT` | 📨 Telegram 推送，Chat ID 和 Bot Token 用英文逗号分隔（可选） | `987654321,123456:AAFxxx` |
| `PRIVATE_REPO_TOKEN` | 🔑 有私库读取权限的 GitHub PAT | `github_pat_xxxxxx` |

## ⚙️ 服务器配置
私库脚本 `zampto_renew.py` 中的 `TARGET_SERVERS` 需根据实际情况修改：

```python
TARGET_SERVERS = [
    {"id": "4490", "name": "🇩🇪 Zampto DE"},
    {"id": "4489", "name": "🇮🇹 Zampto IT"},
]
```

`id` 为服务器 ID（可在 Dashboard URL 中找到），`name` 为自定义显示名称（用于 TG 推送）。

## 📝 PRIVATE_REPO_TOKEN 生成方式
GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic) → Generate new token (classic) → 勾选 `repo` + `workflow` → Generate token → 填入 Secret。
