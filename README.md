# Lewa GaGaLe 自动签到部署说明

自动登录 [Lewa GaGaLe](https://ue2.taotu.ink) 完成每日签到，并支持**积分余额查询**、**自动兑换月卡**、**Telegram 通知推送**与 **Hysteria2 代理**，由 GitHub Actions 定时运行。

## 仓库结构

签到涉及两个仓库分工：

| 仓库 | 可见性 | 存放内容 |
|---|---|---|
| 公库（如 `scripts_game`） | 公开 | `.github/workflows/lewa_checkin.yml`（workflow）、`lewa/time.txt`（防休眠时间戳）、全部 Secrets/Variables |
| 私库 `lewa_gagale_checkin` | 私有 | `checkin.py`（签到脚本本体，不含任何账号密码） |

之所以拆成两个仓库：workflow 定时任务必须放在有效仓库里跑，而签到脚本单独放私库，改脚本时不用动公库；workflow 通过 PAT 拉取私库代码执行。

> **Secrets 配置位置**：GitHub 的 Secrets 只从**运行 workflow 的仓库**解析，所以本项目的所有 Secrets 都配置在公库；私库不需要配置任何 Secret。

```
公库/
├── .github/workflows/lewa_checkin.yml   ← 签到 workflow
└── lewa/time.txt                        ← 每次运行自动更新，防止 Actions 60 天无活动被禁用

私库 lewa_gagale_checkin/（私有）
└── checkin.py                           ← 实际签到脚本
```

## 部署步骤

### 1. 生成 PAT（用于公库拉取私库代码）

1. GitHub 头像 → Settings → Developer settings → Personal access tokens → **Fine-grained tokens** → Generate new token
2. Repository access 选 "Only select repositories" → 勾选 `lewa_gagale_checkin`
3. Permissions 里给 **Contents: Read-only**
4. 生成后复制 token（仅显示一次）

### 2. 配置 Secrets（公库）

在 **公库** Settings → Secrets and variables → Actions → Secrets 页签添加：

| Secret | 必填 | 说明 |
|---|---|---|
| `PRIVATE_REPO_TOKEN` | ✅ | 上一步生成的 PAT，用于拉取私库代码 |
| `EMBY_USERNAME` | ✅ | Emby 登录账号 |
| `EMBY_PASSWORD` | 账号无密码可不填 | Emby 登录密码 |
| `TG_BOT_TOKEN` | 可选 | Telegram Bot Token，用于推送签到结果 |
| `TG_CHAT_ID` | 可选 | Telegram Chat ID |
| `HY2_PROXY_URL` | 可选 | Hysteria2 代理节点链接，格式 `hysteria2://密码@host:port?insecure=1`；配置后 workflow 会自动安装 Hysteria2 并走 SOCKS5 代理 |
| `SOCKS_PORT` | 可选 | 本地 SOCKS5 监听端口，不填默认 `51080` |

### 3. 配置月卡自动兑换开关（可选，公库 Variables）

在 **公库** Settings → Secrets and variables → Actions → **Variables** 页签添加：

| Variable | 必填 | 说明 |
|---|---|---|
| `AUTO_REDEEM_MONTHLY` | 可选 | 自动兑换月卡总开关，**不配置 = 默认开启**。`0`/`false`/`no`/`off` 关闭，`1`/`true`/`yes`/`on` 开启 |

不建变量、保持默认开启即可；想彻底关闭自动兑换时把它设为 `0`。

### 4. 放置文件

- `checkin.py` → 私库 `lewa_gagale_checkin` **根目录**
- `lewa_checkin.yml` → 公库 `.github/workflows/lewa_checkin.yml`
- `lewa/time.txt` → 公库 `lewa/time.txt`（首次放一个占位文件即可，之后由 Actions 自动更新）

### 5. 测试运行

进入公库 **Actions** → 选择 "🔄 Lewa GaGaLe Auto Checkin" → **Run workflow**：

- 手动触发时会出现下拉框 **"🎫 自动兑换月卡"**：`跟随仓库变量`（默认）/ `开启` / `关闭`，可临时覆盖本次运行的行为
- 检查运行结果：
  - ✅ 能成功拉取私库 `checkin.py`
  - ✅ 登录成功、签到成功（或提示"今日已签到"）
  - ✅ 打印 `💰 查询到真实余额` 与 `🛒 商城商品` 列表
  - ✅ 按开关状态出现兑换记录，或 `积分不足，跳过月卡兑换` / `自动兑换月卡已关闭`
  - ✅ 配置了 Telegram 的话能收到推送
  - ✅ `lewa/time.txt` 被自动提交更新

## 月卡自动兑换说明

签到完成后脚本会自动尝试兑换月卡，流程：

1. 调用积分接口拿到**真实余额**与**商城商品列表**（`store_items`，日志中 `🛒 商城商品` 一行会完整打印，可随时核对真实商品 id 与价格）
2. 自动挑选月卡商品：名称**精确为"月卡"** 的优先，否则选 30 天固定续期卡（不会误买"半月卡"等其他商品）
3. 余额 ≥ 商品价格时发起兑换请求（带随机 `request_id`，与服务端幂等校验兼容）；余额不足则打印 `积分不足，跳过月卡兑换`
4. 兑换结果会追加在 TG 推送的 `🎫 月卡兑换:` 一行；兑换成功后推送中的余额为**兑换后余额**

开关优先级（高 → 低）：

| 优先级 | 控制方式 | 生效范围 |
|---|---|---|
| 1 | 手动触发时的下拉框（开启/关闭） | 仅当次运行 |
| 2 | 公库仓库变量 `AUTO_REDEEM_MONTHLY` | 所有定时任务 |
| 3 | 默认值（开启） | 兜底 |

进阶：私库脚本顶部的 `MONTHLY_CARD_ITEM_ID` 可手动指定商品 id（如 `item_1792885258138`），**默认留空即自动选品**，无需维护；只有当商城被站长重建、自动选品拿不到预期商品时才需要改。

## 运行机制

- **定时触发**：每天 UTC `00:10` 与 `12:10`（北京时间 8:10 / 20:10）各跑一次，避免漏签
- **随机延迟**：每次运行随机等待 0~120 秒再执行，降低被目标站点识别为自动化脚本的概率
- **防休眠**：无论签到成功与否，最后一步都会更新并提交 `lewa/time.txt`，保持公库有持续的 commit 活动，避免 GitHub 因 60 天无活动自动暂停 Actions
- **代理可选**：配置 `HY2_PROXY_URL` 后，workflow 会自动安装 Hysteria2 客户端，脚本拉起本地 SOCKS5 代理后再发请求；不配置则直连
- **失败隔离**：月卡兑换失败（余额不足、商品下架、网络异常等）只在 TG 报告中标注 ⚠️，不影响运行结果；只有签到本身失败才会以非零码退出

## 常见问题

**Q: Cookie/账号密码会不会泄露在公库的 Actions 日志里？**
A: 不会。账号在日志中会做脱敏处理（如 `abc***xyz`），密码类 Secret 本身在 Actions 日志中会被自动打码为 `***`；脚本文件里也不含任何凭据（全部走环境变量）。

**Q: 如何修改签到时间？**
A: 编辑公库 `.github/workflows/lewa_checkin.yml` 中 `schedule` 下的 `cron` 表达式（UTC 时间）。

**Q: 如何关闭自动兑换月卡？**
A: 见上方"开关优先级"：临时关一次用手动触发下拉框选"关闭"；长期关闭把公库 Variables 里 `AUTO_REDEEM_MONTHLY` 设为 `0`。

**Q: 兑换提示"商品不存在或已下架"？**
A: 站长重建商城后商品 id 会变化。脚本默认自动从商城列表选品（每次运行实时获取），一般无需处理；如果你在私库脚本里手动指定过 `MONTHLY_CARD_ITEM_ID`，请清空它或从日志 `🛒 商城商品` 一行里找到新 id 更新。

**Q: Actions 页面报了一个跟 Gradle/Java 相关的错误？**
A: 与本签到 workflow 无关，是仓库里其他遗留的 workflow 文件报错，可以在 `.github/workflows/` 目录下找到并删除或禁用。
