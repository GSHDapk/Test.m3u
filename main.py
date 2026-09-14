from bs4 import BeautifulSoup
import requests

# İsteklerin engellenmemesi için tarayıcı taklidi yapan başlıklar
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/122.0.0.0 Safari/537.36"
    ),
    "Accept": (
        "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*|q=0.8"
    ),
    "Accept-Language": "tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7",
    "Referer": "https://live.semttv.xyz/",
}

# Eğer sid "zirve" gelirse kullanılacak özel URL (ihtiyacınıza göre değiştirebilirsiniz)
WORKING_BS1_URL = "https://pasadasin71.cfd/zirve.m3u8"


def fetch_netspor():
  results = []
  target_url = "https://live.semttv.xyz/"

  try:
    print(f"Bağlanılıyor: {target_url}")
    res = requests.get(target_url, headers=HEADERS, timeout=15)
    res.encoding = "utf-8"

    if res.status_code != 200:
      print(f"Siteye erişilemedi, HTTP Kod: {res.status_code}")
      return results

    soup = BeautifulSoup(res.text, "html.parser")

    # live.semttv.xyz sitesindeki mac divlerini tarama
    for div in soup.find_all("div", class_="mac", option=True):
      sid = div["option"]
      t_div = div.find("div", class_="match-takimlar")
      if not t_div:
        continue

      title = t_div.get_text(strip=True)

      # Kanal veya maç gruplandırması
      group = (
          "NETSPOR MACLAR"
          if not div.find_parent("div", id="kontrolPanelKanallar")
          else "NETSPOR CANLI"
      )

      # İstediğiniz siteye göre URL yapısı
      if sid == "zirve":
        f_url = WORKING_BS1_URL
      else:
        f_url = f"https://pasadasin71.cfd/{sid}.m3u8"

      results.append(
          {"name": title, "url": f_url, "group": group, "ref": target_url}
      )

    print(f"Toplam {len(results)} maç/kanal bulundu.")

  except Exception as e:
    print(f"Çekme sırasında hata oluştu: {e}")

  return results


def generate_m3u():
  items = fetch_netspor()

  if not items:
    print("Hiç maç bulunamadı.")

  m3u_content = "#EXTM3U\n"

  for item in items:
    m3u_content += (
        f'#EXTINF:-1 tvg-name="{item["name"]}"'
        f' group-title="{item["group"]}",{item["name"]}\n'
    )
    if item.get("ref"):
      m3u_content += f'#EXTVLCOPT:http-referrer={item["ref"]}\n'
    m3u_content += f"{item['url']}\n"

  with open("kanallar.m3u", "w", encoding="utf-8") as f:
    f.write(m3u_content)
  print("M3U dosyası başarıyla oluşturuldu ve kaydedildi.")


if __name__ == "__main__":
  generate_m3u()
