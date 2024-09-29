##Yazılım Testi Django Web Projesi
Bu proje, bir Django web uygulaması ile GitHub üzerinden klonlanan bir depo içindeki `.java` uzantılı dosyaların analiz edilmesini ve PostgreSQL veritabanına kaydedilmesini içerir. Ayrıca projede 30 birim testi ve 5 entegrasyon testi uygulanmıştır.

## Proje Özeti

- **GitHub Depo Analizi**: Kullanıcıdan bir GitHub repo bağlantısı alınır, bu depo klonlanır ve `.java` uzantılı dosyalar taranır.
- **Sınıf Ayıklama**: Sadece sınıf içeren `.java` dosyaları ayıklanır.
- **Analiz ve Kayıt**: Ayıklanan sınıflar analiz edilir ve analiz sonuçları PostgreSQL veritabanına kaydedilir.
- **Testler**: Proje 30 birim testi ve 5 entegrasyon testi içerecek şekilde tasarlanmıştır.

## Kullanım

1. Projeyi çalıştırmak için:
   ```
   cd b201210100_yazılım_testi\b201210100
   python .\manage.py runserver 127.0.0.1:3000
   ```
2. Tarayıcınızda `http://127.0.0.1:3000` adresine gidin.
3. GitHub depo URL'sini girin ve analizi başlatın.

## Testler

Testleri çalıştırmak için:
   ```
   cd b201210100_yazılım_testi\b201210100
   python test.py
   ```
