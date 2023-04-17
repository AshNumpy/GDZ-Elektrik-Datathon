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