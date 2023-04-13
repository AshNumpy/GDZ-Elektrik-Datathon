## Dış Veri Kullanımı Hk.

Her türlü halka açık verinin kullanılabileceği yönünde, yarışma sayfasında yapılan bildiriyi gözeterek hava durumu verilerinin tahminleme aşamasında bana yardımcı olacağını düşündüm.

GDZ-Elektrik şirketinin elektrik dağıtımlarına ilişkin %85'lik verinin İzmir %15'lik verinin Manisa'ya ait olduğunu öğrendim.  
Buradan hareketle Hangi tarihlerdeki verilerin Manisa'daki dağıtıma ait olduğunu bilmediğim için verilerin çoğu olan İzmir'e ait hava durumu bilgilerini günlük bazda çektim.  


## Veri Kazıma Süreci Hk.

Veri kazıma sürecinde internet siteleri:  
* [World Weather Online](https://www.worldweatheronline.com/izmir-weather-history/izmir/tr.aspx)
* [Playwright](https://playwright.dev/)

Verileri kazımak için `playwright` kütüphanesini kullandım. Veri kazıma sürecinde kullandığım kodlara `../Web Scraping/weather-scraping.py` kısmından ulaşılabilir.
