<h1 align="center">Proje Raporu</h1>

<h2>GDZ Elektrik</h2>

<img src='./Images/gdz-logo.jpg' style="float: left;margin:5px 20px 5px 1px" height='180'> 

Gdz Elektrik, günlük yaşamın vazgeçilmezi, tarımın, ticaretin ve sanayinin itici gücü olan elektriği; güvenli, verimli, çevre ve insan odaklı hizmet anlayışı ve çağın gerekliliklerine uygun teknolojik sistemleri ile tüketicilere ulaştırmaktadır.

Gdz Elektrik, 2013 yılında attığı başlayan yolculuğunda bugün; İzmir ve Manisa illerinde 47 ilçe ve 2.383 mahalleden oluşan toplam 13.123 kilometrekarelik yüzölçümü üzerinde, 3.6 milyon tüketiciye ve 5.9  milyon nüfusa  24 saat kesintisiz olarak elektrik dağıtım hizmeti vermektedir.

## Akış Şeması
1. [Giriş](#giriş)
1. [Veri Seti Hk.](#veri-seti-hk)
1. [Kullanılan Modeller](#kullanılan-modeller)
1. [Modellerin Değerlendirilmesi](#modellerin-değerlendirmesi)
1. [Sonuç](#sonuç)

<hr>

## Giriş

Bu projede saatlik olarak dağıtılan enerji (MWh) değerinin zaman serisi olarak ele alınıp,  gelecek tahminlerinin yapılması amaçlanmıştır.

Bu amaca istinaden modele katkı sağlayacağı düşünülen her türlü halka açık veri veri kazıma ile elde edilip veri setine eklenmiştir.

Tahminlerin yapıldığı modelleri karşılaştırmak ve en iyi performans gösteren modeli seçmek için, XGBoost, AdaBoost, RandomForest, Huber Regressor, RANSAC Regressor, TheilSenRegressor, Vanilla LSTM modelleri uygulandı. Model performansı MAPE ve RMSE değerleri ile ölçüldü. Ayrıca, test verisi ile grafiksel uyumuna da bakıldı. Sonuç olarak, Vanilla LSTM modeli en iyi performans gösteren model olarak seçildi.

Bu raporda, veri seti ve kullanılan modellerin detayları, model performansı ve sonuçlarının analizi sunulacaktır.

<hr>

## Veri Seti Hk.
Veri seti, saatlik olarak kaydedilen tarih sütununa sahip bir zaman serisidir. Toplam 40152 satır ve 2 sütundan oluşur. Veri setindeki tarihler sıralıdır ve örneklemeler her 60 dakikada bir alınmıştır.

Veri setindeki özellik çıkarımı aşağıdaki değişkenler oluşturuldu:
* Saat
* Gün
* Hafta
* Ay
* Yıl
* Haftanın Günü
* Ayın Günü
* Yılın Günü
* Resmi Bayramlar
* Dini Bayramlar
* Mevsimler

Ayrıca verilerin %85'inin İzmir'e %15'inin ise Manisa'ya ait olduğu bilindiğinden, ilgili tarihlerin İzmir'deki hava durumu değerleri **[World Weather Online](https://www.worldweatheronline.com/izmir-weather-history/izmir/tr.aspx)** sitesinden `playwright` kütüphanesi ile kazındı.

> İlgili kodlara `../Web Scraping/weather-scraping.py` kısmından erişilebilir.

## Kullanılan Modeller
Bu raporda, Vanilla LSTM modeli ile birlikte XGBoost, AdaBoost, RandomForest ve Robust Regresyon modelleri de uygulandı. Modellerin detayları şu şekildedir:

### XGBoost
XGBoost, gradient boosting algoritması kullanarak yapay sinir ağı oluşturur. Bu modelde hipoer parametre ayarlaması sonucu en iyi model;
```py
XGBRegressor(
    early_stopping_rounds=30,
    learning_rate = 0.05,
    max_depth=5,
    n_estimators=500)
```
şeklinde kullanıldı.


### AdaBoost
AdaBoost'un zaman serilerinde kullanımı, zaman serisi verilerinin doğası gereği yüksek varyasyonlu olması nedeniyle avantajlıdır. Zaman serisi verileri, örneğin hava durumu tahminleri gibi, değişkenlik gösteren bir yapıya sahip olabilirler. Bu nedenle, zayıf öğrenicilerin birleştirilmesi ile oluşturulan güçlü öğrenici, veri setindeki yüksek varyasyonlu örneklerin sınıflandırılması için daha iyi bir performans gösterir.  
Hiper parametre ayarından sonra model aşağıdaki gibi kullanılmıştır:
```py
AdaBoostRegressor(
    learning_rate=1.0,
    loss='square',
    n_estimators=1000)
```

### RandomForest
Zaman serileri verilerinde Random Forest kullanmanın avantajları arasında, bu modelin yüksek doğruluk ve stabilite sunması yer almaktadır. Ayrıca, zaman serilerindeki gürültü ve dalgalanmaları daha iyi ele alabilen bir modeldir. Bu model, özellikle diğer modellerde görülen aşırı öğrenme (overfitting) sorununa karşı daha dirençlidir. Bunun nedeni, ağaçların farklı özellikler üzerinde eğitilmiş olmalarıdır ve bu nedenle bir ağacın hata yapma eğilimi diğer ağaçlardan farklı olabilir. Sonuç olarak, birleştirilmiş model daha az varyansa sahip olur ve daha az aşırı öğrenme yapar.
```py
RandomForestRegressor(
    max_depth=7,
    min_samples_leaf=1,
    min_samples_split=2,
    n_estimators=1000)
```

### Robust Regressor Modelleri
Robust regresyon yöntemleri, veri setindeki aykırı (outlier) değerlerin model performansını olumsuz etkilemesini azaltmak amacıyla kullanılır. Bu yöntemler, veri setindeki aykırı değerleri baskılayarak veya ağırlıklarını azaltarak modele katkıda bulunmayacakları şekilde ele alırlar.  
Bu hususta Huber Regressor, RANSAC Regressor ve TheilSen Regressor modelleri denendi. Ancak daha önce denenen ensemble modellerine yaklaşamadıkları için hiper parametre ayarı uygulanmadı default ayarlarda kaldı.

### Vanilla LSTM
Vanilla LSTM (Long Short-Term Memory) modeli, zaman serisi verilerinde kullanımı oldukça yaygın olan bir modeldir. Bu model, zaman serisi verilerindeki yapısal özellikleri öğrenerek gelecekteki değerleri tahmin etmeye çalışır. Vanilla LSTM modelinin birçok avantajı vardır.

Birincisi, Vanilla LSTM modeli zaman serilerindeki girdi verilerindeki yapılara duyarlıdır. Bu, modelin verilerdeki örüntüleri daha iyi anlamasına ve doğru tahminler yapmasına yardımcı olur. Ayrıca, Vanilla LSTM modeli doğal olarak uzun vadeli bağımlılıkları öğrenebilir, bu da zaman serisi verilerinde gelecekteki değerlerin tahmin edilmesi için önemlidir.

İkincisi, Vanilla LSTM modeli, modelin performansını artırmak için kullanılabilecek birçok hiperparametreye sahiptir. Bu hiperparametreler, modelin farklı özelliklerini ayarlayarak daha iyi sonuçlar elde edilmesine olanak tanır. Örneğin, Vanilla LSTM modelinde hücre sayısı, katman sayısı, dropout oranı, aktivasyon fonksiyonları gibi hiperparametreler kullanılabilir.

Üçüncüsü, Vanilla LSTM modeli, zaman serilerindeki trendleri ve mevsimsellikleri öğrenerek bu yapıları tahmin edebilir. Bu özellik, modelin gelecekteki değerlerin tahmininde daha doğru sonuçlar vermesine yardımcı olur.

Son olarak Vanilla LSTM modeli olarak kurulan sinir ağlarına ilişkin mimari aşağdaki gibidir:
```py
model = Sequential()
model.add(LSTM(50, input_shape=(train_X.shape[1], train_X.shape[2])))
model.add(Dense(1))
model.compile(loss='mae', optimizer='adam')

model.fit(train_X, y_train, epochs=20, batch_size=72, validation_data=(test_X, y_test), 
                    callbacks=[EarlyStopping(monitor='val_loss', patience=10)], verbose=0, shuffle=False)
```

## Modellerin Değerlendirmesi

|Model|MAPE|RMSE|
|:---|---:|--:|
|Vanilla LSTM|0.04|0.02|
|XGBoost|0.05|125.57|
|AdaBoost|0.07|187.43|
|Random Forest|0.07|188.38|
|Huber Regressor|0.15|402.94|

## Sonuç
Yaptığımız model değerlendirmesi sonucunda, beş farklı modeli MAPE ve RMSE metrikleriyle değerlendirdik. Vanilla LSTM modelimiz en başarılı sonucu elde etti. MAPE değeri 0.04 ve RMSE değeri 0.02 olarak belirlendi. Diğer modeller ise XGBoost, AdaBoost, Random Forest ve Huber Regressor şeklinde sıralandı. Bu modellerin MAPE ve RMSE değerleri Vanilla LSTM modelinden daha yüksek çıktı. XGBoost modelimiz Vanilla LSTM'den hafif bir şekilde daha kötü performans sergiledi, ancak AdaBoost, Random Forest ve Huber Regressor modelleri önemli ölçüde daha kötü sonuçlar gösterdi. Sonuç olarak, bu model değerlendirmesi Vanilla LSTM modelinin zaman serileri için başarılı bir seçenek olduğunu gösterdi ve bu modelin diğer modellere göre daha iyi performans sergilediği görüldü.
