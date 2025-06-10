import json

from utils.EncodeJsonTOSQL import insert_data_to_database, process_json_file


def getNetworkCodes():
    """获取网络上双色球号码"""

    # 导入爬虫库
    import requests

    # 定义数据url
    codeUrl = "https://www.cwl.gov.cn/cwl_admin/front/cwlkj/search/kjxx/findDrawNotice?name=ssq&pageNo=1&pageSize=100000000&systemType=PC"

    # 调用随机请求头
    from utils.RequestHeaderPool import RequestHeaderPool   # 调入请求头获取类
    header_pool = RequestHeaderPool()   # 实例化请求头工具池

    randomHeaders = header_pool.get_random_headers()    # 获取随机请求头

    # 请求网页获取响应
    response = requests.get(codeUrl, headers=randomHeaders)

    # 将获取到的双色球信息加载的嵌入式数据库中
    if response.status_code == 200:
        data = response.json() # 将获取的文件转换为JSON对象
        with open("temp.json", "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

        # 将网上获取的数据从temp.json文件中导出
        process_json_file("temp.json")

        # 执行操作删除这个临时的temp文件
        import os
        try:
            os.remove("temp.json")
            print("temp.json is Delete")
        except FileNotFoundError:
            print(f"文件不存在")
        except Exception as e:
            print(f"删除文件出错：{e}")



if __name__ == '__main__':
    getNetworkCodes()