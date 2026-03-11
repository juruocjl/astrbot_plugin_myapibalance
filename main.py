import json
import urllib.error
import urllib.parse
import urllib.request

from astrbot.api import logger
from astrbot.api.event import filter, AstrMessageEvent
from astrbot.api.star import Context, Star, register


@register("myapibalance", "cjlqwq", "查询 API 余额与用量", "1.0.3")
class MyApiBalancePlugin(Star):
    def __init__(self, context: Context, config: dict = None):
        super().__init__(context)
        self.config = config or {}

    def _get_base_url(self) -> str:
        host = str(self.config.get("host", "127.0.0.1")).strip() or "127.0.0.1"
        port = str(self.config.get("port", 3000)).strip() or "3000"
        scheme = str(self.config.get("scheme", "http")).strip() or "http"
        return f"{scheme}://{host}:{port}"

    def _request_json(self, path: str, query: dict = None) -> str:
        query = query or {}
        base_url = self._get_base_url()
        encoded_query = urllib.parse.urlencode(query)
        url = f"{base_url}{path}"
        if encoded_query:
            url = f"{url}?{encoded_query}"

        try:
            with urllib.request.urlopen(url, timeout=10) as response:
                body = response.read().decode("utf-8", errors="replace")
                try:
                    payload = json.loads(body)
                    return json.dumps(payload, ensure_ascii=False, indent=2)
                except json.JSONDecodeError:
                    return body
        except urllib.error.HTTPError as exc:
            error_body = exc.read().decode("utf-8", errors="replace")
            logger.error("myapibalance HTTPError: %s %s", exc.code, error_body)
            return f"请求失败，HTTP {exc.code}: {error_body or exc.reason}"
        except urllib.error.URLError as exc:
            logger.error("myapibalance URLError: %s", exc.reason)
            return f"请求失败，无法连接到 {base_url}，错误: {exc.reason}"
        except Exception as exc:  # noqa: BLE001
            logger.exception("myapibalance unknown error")
            return f"请求失败，未知错误: {exc}"

    @filter.llm_tool(name="query_total_cost_by_date")
    async def query_total_cost_by_date(self, event: AstrMessageEvent, start_date: str, end_date: str) -> str:
        """查询区间总花费。

        Args:
            start_date(string): 开始日期，格式 YYYY-MM-DD。
            end_date(string): 结束日期，格式 YYYY-MM-DD。
        """
        return self._request_json(
            "/admin/stats/total-cost",
            {"start_date": start_date, "end_date": end_date},
        )

    @filter.llm_tool(name="query_total_cost_by_time")
    async def query_total_cost_by_time(self, event: AstrMessageEvent, start_time: str, end_time: str) -> str:
        """按细粒度时间范围查询总花费（精确到秒）。

        Args:
            start_time(string): 开始时间，格式 YYYY-MM-DDTHH:MM:SS。
            end_time(string): 结束时间，格式 YYYY-MM-DDTHH:MM:SS。
        """
        return self._request_json(
            "/admin/stats/total-cost",
            {"start_time": start_time, "end_time": end_time},
        )

    @filter.llm_tool(name="query_remaining_quota")
    async def query_remaining_quota(self, event: AstrMessageEvent) -> str:
        """查询全局剩余额度汇总。"""
        return self._request_json("/admin/stats/remaining-quota")
