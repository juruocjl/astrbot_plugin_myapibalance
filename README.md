# astrbot_plugin_myapibalance

用于给 AstrBot 提供 AI 工具，查询 API 的总花费与剩余额度。

## 功能

- 查询区间总花费（按日期）
- 查询细粒度时间范围总花费（精确到秒）
- 查询全局剩余额度汇总
- 支持在插件配置中修改请求端口

## 对应接口

- `/admin/stats/total-cost?start_date=YYYY-MM-DD&end_date=YYYY-MM-DD`
- `/admin/stats/total-cost?start_time=YYYY-MM-DDTHH:MM:SS&end_time=YYYY-MM-DDTHH:MM:SS`
- `/admin/stats/remaining-quota`

## 配置项

可在 AstrBot WebUI 插件配置中设置：

- `scheme`：默认 `http`
- `host`：默认 `127.0.0.1`
- `port`：默认 `3000`

默认情况下，请求地址为 `http://127.0.0.1:3000`。

## 暴露的 LLM 工具

- `query_total_cost_by_date(start_date, end_date)`
- `query_total_cost_by_time(start_time, end_time)`
- `query_remaining_quota()`

## 示例（接口层）

```powershell
# 仅查询区间总花费
Invoke-RestMethod "http://127.0.0.1:3000/admin/stats/total-cost?start_date=2026-03-11&end_date=2026-03-11"

# 细粒度时间范围查询总花费（精确到秒，基于请求明细）
Invoke-RestMethod "http://127.0.0.1:3000/admin/stats/total-cost?start_time=2026-03-11T10:00:00&end_time=2026-03-11T10:30:00"

# 查询全局剩余额度汇总
Invoke-RestMethod "http://127.0.0.1:3000/admin/stats/remaining-quota"
```
