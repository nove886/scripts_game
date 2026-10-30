# -*- coding: utf-8 -*-
"""
只登录 + 读 GET /api/me 状态，**不发签到请求**。
用来确认账号能登录、余额字段是哪个、今天到底签没签。

    set CCBOT_USERNAME=账号 & set CCBOT_PASSWORD=密码 & python check_state.py
"""
import json
import sys

import checkin as ck


def main() -> int:
    print(f"🎯 目标站点：{ck.BASE_URL}")
    if not ck.login():
        print("❌ 登录失败（看上面那一行服务端返回的原因）")
        return 1

    me = ck.who_am_i()
    if not me:
        print("❌ /api/me 没拿到数据")
        return 1

    print("\n——— /api/me 原始返回 ———")
    print(json.dumps(me, ensure_ascii=False, indent=2)[:2500])

    print("\n——— 关键字段 ———")
    print(f"账号      : {me.get('name')}")
    print(f"余额(iv)  : {ck.parse_balance(me)} {me.get('money') or ''}")
    print(f"今日可签  : {me.get('canCheckin')}")
    print(f"奖励区间  : {me.get('checkinReward')}")
    print(f"到期时间  : {me.get('ex')}")
    print(f"兑换成本  : {me.get('exchangeCost')}")
    print(f"管理员    : {me.get('isAdmin')}")

    can = me.get("canCheckin")
    if can is True:
        print("\n👉 canCheckin=True：今天还没签，跑 `python checkin.py` 就会真正签到")
    elif can is False:
        print("\n👉 canCheckin=False：今天已经签过了（脚本再跑只会回「今日已签到」）")
    else:
        print("\n👉 返回里没有 canCheckin 字段，脚本会直接 POST 一次尝试")
    return 0


if __name__ == "__main__":
    sys.exit(main())
