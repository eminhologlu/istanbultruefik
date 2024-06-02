# İstanbul Truefik

Bu proje, Leaflet ve Google Maps kullanarak rota planlama ve trafik yoğunluğu haritalarını gösteren bir web uygulamasıdır. 
Uygulama, başlangıç ve bitiş noktaları arasındaki ana rotayı çizdikten sonra benzin istasyonları, restoranlar, 
hastaneler ve diğer yerler gibi ilgi noktalarına olan alternatif rotaları da göstermektedir.

![Nokta Seçme Ekran Görüntüsü](https://i.imgur.com/AMndnTS.png)

## Özellikler

- Başlangıç ve bitiş noktaları arasındaki ana rotayı çizme.
- Benzin istasyonları, restoranlar, hastaneler ve diğer yerlere alternatif rotaları çizme.
- Leaflet haritasını ve Google Maps trafik yoğunluğu haritasını arasında geçiş yapma.
- Trafik bilgilerini periyodik olarak güncelleme (API entegrasyonu gereklidir).

## Gereksinimler

- Python 3.x
- Flask
- Leaflet.js
- Leaflet Routing Machine
- PapaParse

## Kurulum

1. Bu projeyi yerel makinenize klonlayın:
    ```bash
    git clone https://github.com/eminhologlu/istanbultruefik.git
    cd istanbultruefik
    ```

2. Gerekli Python paketlerini yükleyin:
    ```bash
    pip install Flask
    ```

3. Flask uygulamasını başlatın:
    ```bash
    flask run
    ```

4. Web tarayıcınızda `http://127.0.0.1:5000` adresine gidin.

## Kullanım

- Başlangıç ve bitiş noktaları haritada işaretlenecektir.
- Ana rota mavi renkle gösterilecektir.
- Alternatif rotalar yeşil renkle gösterilecektir.
- "Rota Haritasına Geç" butonuna tıklayarak Leaflet haritasına geçebilirsiniz.
- "Trafik Yoğunluk Haritasına Geç" butonuna tıklayarak Google Maps trafik yoğunluğu haritasına geçebilirsiniz.

## Yapı

- `main.py`: Flask uygulamasının ana dosyası.
- `templates/index.html`: İki Nokta Seçme HTML dosyası.
- `templates/map.html`: Harita HTML dosyası.
- `static/gas_stations.csv`, `static/restoran.csv`, `static/hastane.csv`, `static/yerler.csv`: İlgili yerlerin konum verilerini içeren CSV dosyaları.

## Örnek HTML Kodu

```html
<!DOCTYPE html>
<html lang="tr">
<head>
    <!-- Meta ve stil dosyaları buraya gelecek -->
</head>
<body>
    <div id="map-container">
        <!-- Harita ve butonlar buraya gelecek -->
    </div>
    <script>
        // JavaScript kodu buraya gelecek
    </script>
</body>
</html>
