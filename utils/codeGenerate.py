import pprint
import random
from collections import deque


def codeGenerate(num, model):
    """
    双色球号码生成器主函数

    参数:
        num (int): 需要生成的号码组数
        model (int): 生成模式 (1=普通模式, 2=预测模式，当前版本两种模式逻辑相同)

    返回:
        list: 包含双色球号码的列表，每个元素为字典格式 {'redCodes': {红球集合}, 'blueCodes': {蓝球集合}}

    异常:
        ValueError: 当模式参数不为1或2时抛出
    """
    if model == 1:
        return codeBaseGenerateDeduplicate(num)
    elif model == 2:
        return codeBaseGenerateDeduplicate(num)
    else:
        raise ValueError("模式参数必须为1或2")


def codeBaseGenerate():
    """生成一组不重复的双色球号码

    返回:
        dict: 包含红、蓝球号码的字典
            - redCodes (set): 6个不重复的红球号码 (1-33)
            - blueCodes (set): 1个蓝球号码 (1-16)
    """
    # 定义号码范围（含上限）
    red_range = range(1, 34)  # 红球范围1-33
    blue_range = range(1, 17)  # 蓝球范围1-16

    # 使用random.sample一次性生成6个不重复的红球
    # 相比循环生成，这种方式效率更高且保证不重复
    red_code = set(random.sample(red_range, 6))

    # 蓝球只需一个随机数，使用集合结构保持与红球一致的数据类型
    blue_code = {random.randint(1, 16)}

    return {"redCodes": red_code, "blueCodes": blue_code}


def codeBaseGenerateDeduplicate(num):
    """批量生成去重的双色球号码

    参数:
        num (int): 需要生成的号码组数

    返回:
        list: 去重后的双色球号码列表

    去重规则:
        1. 完整组合（红球+蓝球）不能重复
        2. 蓝球号码在最近16期内不能重复
    """
    # 存储最终生成的号码组合
    code_list = []

    # 使用双端队列维护最近16个蓝球号码
    # maxlen=16确保队列满时自动移除最旧元素，实现滑动窗口机制
    recent_blue_codes = deque(maxlen=16)

    # 使用集合存储已生成的完整号码组合
    # 键为(red_tuple, blue_num)元组，利用哈希表实现O(1)时间复杂度的查重
    existing_codes = set()

    # 循环生成号码直到达到指定数量
    while len(code_list) < num:
        # 生成一组新号码
        cur_code = codeBaseGenerate()

        # 将红球集合转为有序元组（集合是无序的，不能直接哈希）
        # sorted确保相同数字的不同顺序被视为同一组合
        red_tuple = tuple(sorted(cur_code["redCodes"]))

        # 提取蓝球数字（集合中唯一元素）
        blue_num = next(iter(cur_code["blueCodes"]))

        # 构建完整组合的哈希键
        code_tuple = (red_tuple, blue_num)

        # 检查是否存在完全相同的组合（红球和蓝球都相同）
        if code_tuple in existing_codes:
            continue  # 重复则跳过本次循环

        # 检查蓝球是否在最近16次内出现过
        # deque的成员检查时间复杂度为O(n)，但n=16时可视为常数时间
        if blue_num in recent_blue_codes:
            continue  # 蓝球重复则跳过

        # 通过所有查重检查，添加到结果集
        code_list.append(cur_code)

        # 记录已生成的组合，用于后续查重
        existing_codes.add(code_tuple)

        # 更新蓝球历史记录（自动维护长度为16）
        recent_blue_codes.append(blue_num)

    return code_list


if __name__ == '__main__':
    # 程序入口，测试功能
    print(f"{'测试结果':↓^20}")  # 打印居中的标题
    # pprint.pprint(codeGenerate(10, 1))  # 生成10组普通模式号码并美观打印