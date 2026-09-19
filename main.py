import requests
from bs4 import BeautifulSoup

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Referer': 'https://live.semttv.xyz/'
}

# Eğer 'zirve' seçeneği için özel bir URL kullanmıyorsanız varsayılan bir yedek link yazabilirsiniz
WORKING_BS1_URL = "https://pasadasin71.cfd/zirve.m3u8"

def fetch_netspor():
    results = []
    try:
        url = "https://live.semttv.xyz/"
        res = requests.get(url, headers=HEADERS, timeout=15)
        res.encoding = 'utf-8'
        
        if res.status_code != 200:
            print(f"Siteye erişilemedi, HTTP Kod: {res.status_code}")
            return results

        soup = BeautifulSoup(res.text, 'html.parser')
        
        for div in soup.find_all('div', class_='mac', option=True):
            sid = div.get('option')
            if not sid:
                continue
                
            t_div = div.find('div', class_='match-takimlar')
            if not t_div:
                continue
                
            title = t_div.get_text(strip=True)
            if not title:
                continue

            group = "NETSPOR MACLAR" if not div.find_parent('div', id='kontrolPanelKanallar') else "NETSPOR CANLI"
            f_url = WORKING_BS1_URL if sid == "zirve" else f"https://pasadasin71.cfd/{sid}.m3u8"
            
            results.append({
                "name": title, 
                "url": f_url, 
                "group": group, 
                "ref": "https://live.semttv.xyz/"
            })
            
    except Exception as e:
        print(f"Veri çekilirken hata oluştu: {e}")
        
    return results

def save_m3u():
    items = fetch_netspor()
    if not items:
        print("Hiçbir yayın bulunamadı veya site yapısı değişti.")
        return

    m3u_content = "#EXTM3U\n"
    for item in items:
        m3u_content += f'#EXTINF:-1 group-title="{item["group"]}",{item["name"]}\n'
        m3u_content += f'#EXTVLCOPT:http-referrer={item["ref"]}\n'
        m3u_content += f'{item["url"]}\n'

    with open("netspor.m3u", "w", encoding="utf-8") as f:
        f.write(m3u_content)
        
    print(f"Başarıyla {len(items)} yayın 'netspor.m3u' dosyasına kaydedildi.")

if __name__ == "__main__":
    save_m3u()
