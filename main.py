import requests
from bs4 import BeautifulSoup

# 0. 从cookie.txt中提取完整的Cookie（示例数据）
cookies = {
    "s_gxxx_xxxf_auth": "",
    "s_gxxx_xxxf_saltkey": "",
    "s_gxxx_xxxf_checkpm": "1",
    "s_gxxx_xxxf_connect_is_bind": "1",
    "s_gxxx_xxxf_ulastactivity": "",
    # 其他cookie可根据需要添加...
}

# 1. 创建持久会话
session = requests.Session()
session.headers.update({
    'accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'connection': 'Keep-Alive',
    'Referer': 'https://tsdm39.com/plugin.php?id=dsu_paulsign:sign',
    'Content-Type': 'application/x-www-form-urlencoded'
})

# 2. 获取动态formhash（需携带完整Cookie）
sign_page_url = "https://tsdm39.com/plugin.php?id=dsu_paulsign:sign"
response = session.get(sign_page_url,cookies=cookies)
soup = BeautifulSoup(response.text, 'html.parser')
formhash = soup.find('input', {'name': 'formhash'}).get('value')  # 提取动态令牌

# 3. 构造带AJAX参数的签到接口（关键修改）
sign_api_url = "https://tsdm39.com/plugin.php?id=dsu_paulsign:sign&operation=qiandao&infloat=1&sign_as=1&inajax=1"

# 4. 完善POST参数（根据论坛要求）
post_data = {
    'formhash': formhash,
    'signsubmit': 'yes',
    'qdxq': 'kx',       # 心情类型：开心
    'qdmode': '2',      # 模式：普通签到
    'todaysay': '自动签到成功！',
    'fastreply': '0'
}

# 5. 发送签到请求（需携带完整Cookie）
sign_response = session.post(
    sign_api_url,
    data=post_data,
    cookies=cookies,
    headers={'Referer': sign_page_url}
)

# 可选：积分提取函数
def extract_points(text):
    try:
        return text.split("获得奖励")[1].split("<")[0].strip()
    except:
        return "未知"

# 6. 验证结果（根据AJAX响应）
if "succeed" in sign_response.text:
    print("✅ 签到成功！获得积分：", extract_points(sign_response.text))
    print(sign_response.text)
elif "已经签到" in sign_response.text:
    print("⏰ 今日已完成签到")
else:
    print("❌ 签到失败 | 响应内容：", sign_response.text[:200])

