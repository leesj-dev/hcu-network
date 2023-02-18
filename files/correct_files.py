import requests
import re
import base64
import logging
import os
import html
import magic
import mimetypes
import Cp949ToUniTable as ct
from multiprocessing import Pool

chk_list = [229345, 229425, 229448, 229452, 232348, 233978, 233983, 233986, 233992, 233996, 233999, 234004, 234006, 234015, 234018, 234020, 234023, 234048, 234049, 234050, 234051, 234052, 234053, 234054, 234326, 234367, 234386, 234632, 235020, 235026, 235088, 235089, 235170, 235172, 236440, 236441, 238469, 238475, 238479, 238564, 238570, 240330, 240481, 241760, 241761, 241763, 241764, 241765, 241767, 241768, 241962, 241978, 241979, 241987, 242088, 243088, 243089, 246058, 249541, 249544, 249548, 249550, 249554, 249641, 249643, 249644, 249646, 249652, 249653, 249654, 251514, 252016, 253046, 253429, 254008, 254442, 254799, 254802, 254806, 254807, 254811, 254812, 254813, 254817, 254818, 254819, 254821, 254826, 254829, 254839, 255367, 255371, 255372, 255506, 257092, 257109, 257175, 257281, 257347, 257539, 257793, 257811, 257838, 257851, 258500, 258517]

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
        fname = html.unescape(euc2utf(re.findall("filename=(.+)", response.headers["content-disposition"])[0]))
        # 확장자가 없을 경우
        if not os.path.splitext(fname)[1]:
            try:
                suffix = mimetypes.guess_extension(magic.from_file(content, mime=True))
                fname = ".".join(fname, suffix)

            except:
                fname = fname + ".png"

        with open(os.path.join(".", "files", "result2", f"[{str(i)}] {fname}"), "wb") as f:
            f.write(content)
        logging.info(f"[{str(i)}] O")
    else:
        logging.info(f"[{str(i)}] X")


if __name__ == "__main__":
    pool = Pool(os.cpu_count())
    pool.map(download, chk_list)
