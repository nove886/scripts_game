# Aclclouds-Renew

一个可手动触发/定时运行的 GitHub Actions 工作流，通过注入会话 Cookie 登录
ACLClouds 控制面板，对即将到期的服务器卡片自动触发续期操作，并在每次
操作后通过 Telegram 推送结果通知。

## 依赖要求

- 在仓库设置中配置好 Secrets（`Settings → Secrets and variables → Actions`）
- Python 3.10（工作流会自动安装）
- `seleniumbase`、`requests`

## 仓库 Secrets

| Secret          | 是否必需 | 说明                                              |
|------------------|----------|------------------------------------------------------|
| `GH_TOKEN`       | 是      | 用于检出 `renew_tasks` 仓库的 token             |
| `ACL_COOKIE`     | 是      | ACLClouds 的 `remember_web_...` 会话 Cookie 值    |
| `KATA_LINK`      | 否      | 用于构建本地代理隧道的节点链接（VLESS/VMess 等）  |
| `TG_TOKEN`       | 否      | 用于通知的 Telegram Bot Token                        |
| `TG_USERID`      | 否      | 接收通知的 Telegram Chat ID                          |

如果未配置 `TG_TOKEN` / `TG_USERID`，通知步骤会被静默跳过。
如果未配置 `KATA_LINK`，代理步骤会被跳过，浏览器将直接连接目标站点。

## 环境变量（脚本层面）

| 变量          | 默认值                          | 说明                          |
|----------------|-----------------------------------|----------------------------------------|
| `PROXY`        | `socks5://127.0.0.1:1080`        | 浏览器使用的代理地址     |
| `COOKIE`       | —                                 | 会话 Cookie 的值                  |
| `COOKIE_NAME`  | `remember_web_...`               | 要注入的 Cookie 名称                 |
| `BASE_URL`     | `https://dash.aclclouds.com`     | 控制面板的基础 URL                    |
| `MAX_RETRY`    | `20`                              | 验证步骤的最大重试次数  |
| `TG_TOKEN`     | —                                 | Telegram Bot Token                    |
| `TG_CHAT_ID`   | —                                 | Telegram Chat ID                      |

## 使用方法

1. Fork/克隆本仓库以及 workflow 中引用的 `renew_tasks` 配套仓库。
2. 按上表添加各项 Secrets。
3. 在 **Actions** 标签页中手动触发工作流（`workflow_dispatch`）。
4. 在 `artifacts/` 目录（或你的 Telegram 聊天）中查看每台服务器的截图和状态。

## 注意事项 / 风险提示

- 本工作流会使用你手动获取并需妥善保密的会话 Cookie，对第三方服务
  （ACLClouds）执行真实的自动化操作。
- 脚本中包含反复尝试点击、绕过"我不是机器人"验证的逻辑。自动化绕过
  某个网站的反机器人/反自动化检测，很可能违反该服务的用户条款
  （Terms of Service），这与 GitHub 自身对爬虫/自动化行为的政策是
  相互独立的两回事。在 CI 中运行此脚本前，请先查阅 ACLClouds 的服务
  条款，并考虑手动续期是否是更稳妥的选择。
- Cookie 值属于长期有效的凭证——请像对待密码一样谨慎处理 `ACL_COOKIE`，
  如有泄露风险应及时轮换。
