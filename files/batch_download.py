import requests
import re
import base64
import logging
import sys
import os
import Cp949ToUniTable as ct
from multiprocessing import Pool

logging.basicConfig(
    handlers=[logging.StreamHandler(sys.stdout), logging.FileHandler(os.path.join(os.path.dirname(__file__), "run.log"))],
    format="%(asctime)s.%(msecs)03d %(levelname)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    level=logging.INFO,
)


def euc2utf(original: str) -> str:
    try:
        new = ""
        i = 0
        while True:
            if i == len(original):
                break
            if ct.uni_conv_table[ord(original[i])] == "LEAD":
                new += chr(ct.uni_conv_table[ord(original[i]) * 0x100 + ord(original[i + 1])])
                i += 1
            else:
                new += chr(ct.uni_conv_table[ord(original[i])])
            i += 1
        return new
    except:
        return original


def download(i):
    uid = base64.b64encode(str(i).encode("utf-8")).decode("utf-8")
    url = "https://hcuhs.kr/portfolio/read.php?UID=" + uid
    response = requests.get(url)
    content = response.content

    if content != "해당 파일이나 경로가 존재하지 않습니다.".encode(encoding="euc-kr"):
        fname = euc2utf(re.findall("filename=(.+)", response.headers["content-disposition"])[0])
        with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), "result1", f"[{str(i)}] {fname}"), "wb") as f:
            f.write(content)
        logging.info(f"[{str(i)}] O")
    else:
        logging.info(f"[{str(i)}] X")


if __name__ == "__main__":
    pool = Pool(os.cpu_count())
    pool.map(download, range(220000, 260000))