# -*- coding: utf-8 -*-

"""
伶伦转换器 版本检查组件
Linglun Converter Version Checking Component

版权所有 © 2024 金羿 & 睿穆开发组
Copyright © 2024 EillesWan & TriM Org.

开源相关声明请见 ./License.md
Terms & Conditions: ./Lisense.md
"""

from .io import TrimLog, urllib, Sequence, Iterable, Callable, Optional


def is_ver_char(text: str) -> bool:
    return text.isnumeric() or text == "."


def cut_ver_str(text: str) -> str:
    text += " "
    len_of_text = len(text) - 1
    i = 0
    while i <= len_of_text:
        if is_ver_char(text[i]) and (text[i + 1] if i < len_of_text else False):
            j = i
            while is_ver_char(text[j]) and j < len_of_text:
                j += 1
            temp_str = text[i:j].strip()
            if ("." in temp_str) and (temp_str[0] != ".") and (temp_str[-1] != "."):
                return temp_str
            i = j
        i += 1
    return ""


def get_ver_str(text: str) -> Iterable[str]:
    text += " "
    all_ver_str = []
    len_of_text = len(text) - 1
    i = 0
    while i <= len_of_text:
        if is_ver_char(text[i]) and (text[i + 1] if i < len_of_text else False):
            j = i
            while is_ver_char(text[j]) and j < len_of_text:
                j += 1
            temp_str = text[i:j].strip()
            if ("." in temp_str) and (temp_str[0] != ".") and (temp_str[-1] != "."):
                all_ver_str.append(temp_str)
            i = j
        i += 1
    return all_ver_str


def is_ver_bigger(ver_1: Sequence[int], ver_2: Sequence[int]) -> bool:
    len_v1 = len(ver_1)
    len_v2 = len(ver_2)
    for i in range(min(len_v1, len_v2)):
        if ver_1[i] == ver_2[i]:
            continue
        else:
            return ver_1[i] > ver_2[i]
    return len_v1 > len_v2


def check_update(
    appname: str,
    get_text_url: str,
    version_now: str,
    message_show_fun: Callable,
    logger: TrimLog.Logger,
    version_disp: Optional[str] = None,
):
    if not version_disp:
        version_disp = version_now

    logger.info("当前版本信息：{}".format(version_now))
    try:
        code_content: str = urllib.request.urlopen(get_text_url).read().decode("utf-8")
    except Exception as E:  # noinspection PyBroadException
        logger.warning("无法获取更新版本信息：{}".format(E))
        return

    code_content = code_content[code_content.find("__version__") :]
    code_content = code_content[code_content.find('"') + 1 :]
    version_content = code_content[: code_content.find('"')]

    logger.info("已获取更新版本信息：{}".format(version_content))

    if is_ver_bigger(
        [int(v) for v in cut_ver_str(version_content).split(".")],
        [int(v) for v in cut_ver_str(version_now).split(".")],
    ):
        if "__zhver__" in code_content:
            code_content = code_content[code_content.find("__zhver__") :]
            code_content = code_content[code_content.find('"') + 1 :]
            version_content = code_content[: code_content.find('"')]

        message_show_fun(
            "！有新版本！\n最新的 {app} 已经是 {latest} 版本，当前您正在使用的仍是 {current} 版本，您可以前往下载地址更新。".format(
                app=appname, latest=version_content, current=version_disp
            )
        )

    # code_content = code_content[code_content.find('"')+1:]

    # version_content = code_content[:code_content.find('"')]

    # version_content_len = len(version_content)

    # for i in range(version_content_len):
    #     if is_ver_char(version_content[i]) and (version_content[i+1] if i < version_content.__len__() else False):
    #         j = i
    #         while is_ver_char(version_content[j]):j+=1
    #         return version_content[i:j]

    # "".join([version_content[i] for i in range(version_content.__len__()) if is_ver_char(version_content[i]) and ((version_content[i-1] if i > 0 else False) or (version_content[i+1] if i < version_content.__len__() else False))]).split('.')
