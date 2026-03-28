GitHub Actions Secrets（需在仓库中配置）
Secret 名称必填说明PRIVATE_REPO_TOKEN✅ 必填用于检出私有仓库的 GitHub PAT TokenHACHIMI_BATCH✅ 必填账号批量配置（见下方格式说明）HY2_PROXY_URL⬜ 可选Hysteria2 代理 URL，不填则直连SOCKS_PORT⬜ 可选SOCKS5 代理端口，默认 51080

HACHIMI_BATCH 格式
每行一个账号，支持两种格式：
# 不需要 Telegram 通知（2列）
username,password

# 需要 Telegram 通知（4列）
username,password,tg_bot_token,tg_chat_id
支持 # 开头的注释行，多账号换行叠加即可。