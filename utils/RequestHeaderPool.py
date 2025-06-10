import random
import time
from typing import Dict, List
import requests
from fake_useragent import UserAgent


class RequestHeaderPool:
    """请求头池类，用于管理和生成随机请求头"""

    def __init__(self, use_fake_useragent: bool = True, refresh_interval: int = 86400):
        """
        初始化请求头池

        参数:
            use_fake_useragent: 是否使用fake-useragent生成随机UA，默认为True
            refresh_interval: 刷新User-Agent的间隔时间(秒)，默认为24小时
        """
        self.use_fake_useragent = use_fake_useragent
        self.refresh_interval = refresh_interval
        self.last_refresh_time = 0
        self.user_agents = self._initialize_user_agents()
        self.common_headers = self._get_common_headers()

    def _initialize_user_agents(self) -> List[str]:
        """初始化User-Agent列表"""
        if self.use_fake_useragent:
            try:
                ua = UserAgent()
                # 生成不同浏览器的User-Agent
                return [
                    ua.chrome,
                    ua.firefox,
                    ua.safari,
                    ua.ie,
                    ua.opera,
                    ua.android,
                    ua.ios
                ]
            except Exception as e:
                print(f"fake-useragent初始化失败: {e}，将使用内置User-Agent")
                self.use_fake_useragent = False

        # 内置的User-Agent列表
        return [
            # Chrome浏览器
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36",

            # Firefox浏览器
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:90.0) Gecko/20100101 Firefox/90.0",
            "Mozilla/5.0 (X11; Linux i686; rv:89.0) Gecko/20100101 Firefox/89.0",

            # Safari浏览器
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15",
            "Mozilla/5.0 (iPhone; CPU iPhone OS 14_7_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Mobile/15E148 Safari/604.1",
            "Mozilla/5.0 (iPad; CPU OS 14_7_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Mobile/15E148 Safari/604.1",

            # Edge浏览器
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 Edg/91.0.864.59",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36 Edg/92.0.902.55",

            # 移动设备
            "Mozilla/5.0 (Linux; Android 10; SM-G981B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Mobile Safari/537.36",
            "Mozilla/5.0 (iPhone; CPU iPhone OS 14_7_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Mobile/15E148 Safari/604.1",
            "Mozilla/5.0 (iPad; CPU OS 14_7_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Mobile/15E148 Safari/604.1"
        ]

    def _get_common_headers(self) -> Dict[str, str]:
        """获取常用的请求头字段"""
        return {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
            "Accept-Encoding": "gzip, deflate, br",
            "DNT": "1",  # 不跟踪
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
            "Cache-Control": "max-age=0"
        }

    def refresh_user_agents(self) -> None:
        """刷新User-Agent列表"""
        if self.use_fake_useragent and (time.time() - self.last_refresh_time > self.refresh_interval):
            self.user_agents = self._initialize_user_agents()
            self.last_refresh_time = time.time()

    def get_random_headers(self, additional_headers: Dict[str, str] = None) -> Dict[str, str]:
        """
        获取随机请求头

        参数:
            additional_headers: 额外的请求头字段，将合并到返回的请求头中

        返回:
            包含随机User-Agent和常用请求头的字典
        """
        self.refresh_user_agents()

        # 复制常用请求头
        headers = self.common_headers.copy()

        # 添加随机User-Agent
        headers["User-Agent"] = random.choice(self.user_agents)

        # 添加额外的请求头
        if additional_headers:
            headers.update(additional_headers)

        return headers

    def get_specific_headers(self, browser: str = None) -> Dict[str, str]:
        """
        获取特定浏览器的请求头

        参数:
            browser: 浏览器类型，可选值: chrome, firefox, safari, edge, android, ios

        返回:
            特定浏览器的请求头
        """
        # 过滤出包含指定浏览器关键词的User-Agent
        if browser:
            browser_keywords = {
                "chrome": "Chrome",
                "firefox": "Firefox",
                "safari": "Safari",
                "edge": "Edg",
                "android": "Android",
                "ios": "iPhone|iPad|iPod"
            }

            keyword = browser_keywords.get(browser.lower())
            if keyword:
                filtered_uas = [ua for ua in self.user_agents if keyword in ua]
                if filtered_uas:
                    specific_ua = random.choice(filtered_uas)
                    headers = self.common_headers.copy()
                    headers["User-Agent"] = specific_ua
                    return headers

        # 如果指定的浏览器不存在或出错，返回随机请求头
        return self.get_random_headers()


# 使用示例
if __name__ == "__main__":
    # 创建请求头池实例
    header_pool = RequestHeaderPool()

    # 获取随机请求头
    random_headers = header_pool.get_random_headers()
    print("随机请求头:")
    for key, value in random_headers.items():
        print(f"{key}: {value}")

    print("\n---\n")

    # 获取Chrome浏览器的请求头
    chrome_headers = header_pool.get_specific_headers("chrome")
    print("Chrome请求头:")
    for key, value in chrome_headers.items():
        print(f"{key}: {value}")

    print("\n---\n")

    # 带额外请求头的示例
    additional = {"Referer": "https://www.example.com", "X-Requested-With": "XMLHttpRequest"}
    custom_headers = header_pool.get_random_headers(additional)
    print("带额外字段的请求头:")
    for key, value in custom_headers.items():
        print(f"{key}: {value}")

    # 使用请求头进行HTTP请求示例
    try:
        response = requests.get("https://httpbin.org/headers", headers=random_headers)
        print("\n请求结果:")
        print(response.text)
    except Exception as e:
        print(f"请求出错: {e}")