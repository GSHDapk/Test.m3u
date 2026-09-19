import requests
from bs4 import BeautifulSoup

# Tarayıcı gibi görünmek için detaylı header bilgileri
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
    'Accept-Language': 'tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.9',
    'Referer': 'https://live.semttv.xyz/'
}

def test_fetch():
    url = "https://live.semttv.xyz/"
    print(f"Bağlanmaya çalışılıyor: {url}")
    
    try:
        response = requests.get(url, headers=HEADERS, timeout=15)
        print(f"HTTP Durum Kodu: {response.status_code}")
        
        if response.status_code != 200:
            print(f"HATA: Site olumlu yanıt vermedi. Kod: {response.status_code}")
            return

        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Sitedeki maç elementlerini arayalım
        maclar = soup.find_all('div', class_='mac')
        print(f"Bulunan '.mac' sınıfına sahip element sayısı: {len(maclar)}")
        
        if len(maclar) == 0:
            print("UYARI: Sitede '.mac' sınıfı bulunamadı. Site tasarımı değişmiş veya bot koruması sayfayı gizliyor olabilir.")
            print("Gelen sayfanın ilk 500 karakteri:")
            print(response.text[:500])
        else:
            for i, div in enumerate(maclar[:3]): # İlk 3 maçı test için yazdır
                print(f"Örnek Maç {i+1}: {div.get_text(strip=True)}")

    except Exception as e:
        print(f"Bağlantı sırasındakritik hata oluştu: {e}")

if __name__ == "__main__":
    test_fetch()
