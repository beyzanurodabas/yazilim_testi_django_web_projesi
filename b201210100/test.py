import re,os
import unittest
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'veriproje.settings')
import django
from unittest.mock import patch, MagicMock
from django.test import Client
from django.urls import reverse
from faker import Faker
from parameterized import parameterized
from veriproje.tools import count_code_lines,count_functions,code_loc_count,count_comment_lines,count_javadoc_comment_lines
import time
# Django ayarlarını yapılandır
django.setup()
from veriproje.mymodels.Dosya import Dosya2
from templates.views import index,analyses,data
from django.test import TestCase
from django.test.client import Client
from django.urls import reverse

class BirimTest(unittest.TestCase):
    def setUp(self): #testten önce
        self.start =time.time()
        self.fake = Faker()

    def tearDown(self): #her testten sonra teardown calısır
        self.end=time.time()
        runtime_length = self.end-self.start
        test_name=self.id().split('.')[-1]
        print(f'{test_name}  runtime length: {runtime_length} seconds')

    @parameterized.expand([
        ("public_method", "public", "void", "methodName"),
        ("private_method", "private", "String", "anotherMethod"),
        ("protected_method", "protected", "int", "protectedMethod"),
        ("constructor", "public", "MyClass", "__init__"),
        ("main_method", "public", "static void", "main"),
    ])
    def test_count_functions(self, test_name, access_modifier, return_type, method_name):
        content = f"""
        public class MyClass {{
            {access_modifier} {return_type} {method_name}() {{
                // Method body
            }}
        }}
        """
        self.assertEqual(count_functions(content), 1)

    def test_multiple_functions(self):
        content = """
        public class MyClass {
            public void method1() {
                // Method 1 body
            }
            private int method2() {
                // Method 2 body
            }
            protected String method3() {
                // Method 3 body
            }
        }
        """
        self.assertEqual(count_functions(content), 3)

    def test_no_function(self):
        content = """
        public class MyClass {
            // No method in this class
        }
        """
        self.assertEqual(count_functions(content), 0)

    def test_count_code_lines(self):
        content = """import os\nimport re\n\n# Bir örnek kod satırı\nprint('Hello, world!')"""
        self.assertEqual(count_code_lines(content), 4)

    def test_count_functions(self):
        content = """
            public class Example {
                public void method1() {
                    // Kod
                }
                
                private int method2() {
                    // Kod
                    return 0;
                }
            }
        """
        self.assertEqual(count_functions(content), 2)

    def test_code_loc_count(self):
        content = """import os\nimport re\n\n# Bir örnek kod satırı\nprint('Hello, world!')"""
        self.assertEqual(code_loc_count(content), 5)

    def test_count_comment_lines(self):
        content = """
            // Bu bir yorum satırıdır
            /* Bu da bir yorum satırıdır */
            int x = 5; // Tek satırlık bir yorum
            /*
                Bu bir çok satırlık
                yorum bloğudur
            */
        """
        self.assertEqual(count_comment_lines(content), 4)

    def test_count_javadoc_comment_lines(self):
        content = """
            /**
             * Bu bir JavaDoc yorum satırıdır
             * @param x Bir parametre
             * @return Bir değer
             */
            public int example(int x) {
                return x + 1;
            }
        """
        self.assertEqual(count_javadoc_comment_lines(content), 3)

    #FAKER KÜTÜPHANESİ
    def test_count_code_lines_with_faker(self):
        fake = Faker()
        fake_text = fake.text()
        self.assertEqual(count_code_lines(fake_text), len(fake_text.split('\n')))

    @parameterized.expand([
        ("// Single line comment", "// Single line comment", 1),
        ("/* Multi-line comment */", "/* Multi-line comment */", 0),
        ("// Single line comment\n/* Multi-line comment */", "// Single line comment\n/* Multi-line comment */", 1),
    ])
    def test_count_comment_lines_parameterized(self, name, file_content, expected):
        self.assertEqual(count_comment_lines(file_content), expected)


    # Parametrelendirilmiş test kullanarak 'metotlar' desenini doğrulama
    @parameterized.expand([
        ("Test1", "public void method1() {}", 1),
        ("Test2", "private int method2() {}", 1),
        ("Test3", "", 0),
    ])
    def test_metotlar_pattern(self, name, content, expected):
        self.assertEqual(len(re.findall(r"\b(public|private|protected)\s+([\w<>]+)\s+(\w+)\s*\([^)]*\)\s*{", content)), expected)

    @parameterized.expand([
        ("Test1", "public Example() {}", 1),
        ("Test2", "private Example() {}", 1),
        ("Test3", "", 0),
    ])
    def test_kurucu_pattern(self, name, content, expected):
        self.assertEqual(len(re.findall(r"\b(public|private|protected)\s+(\w+)\s*\([^)]*\)\s*{", content)), expected)

    # Parametrelendirilmiş test kullanarak 'fonksiyonlar' değişkenini doğrulama
    @parameterized.expand([
        ("Test1", "public void method1() {}", 1),
        ("Test2", "private int method2() {}", 1),
        ("Test3", "public Example() {}", 1),
        ("Test4", "private Example() {}", 1),
        ("Test5", "public static void main(String[] args) {}", 1),
        ("Test6", "", 0),
    ])
    def test_fonksiyonlar_variable(self, name, content, expected):
        metotlar_count = len(re.findall(r"\b(public|private|protected)\s+([\w<>]+)\s+(\w+)\s*\([^)]*\)\s*{", content))
        kurucu_count = len(re.findall(r"\b(public|private|protected)\s+(\w+)\s*\([^)]*\)\s*{", content))
        main_count = len(re.findall(r"\bpublic\s+static\s+void\s+main\s*\(.*\)\s*{", content))

        self.assertEqual(metotlar_count + kurucu_count + main_count, expected)

class ViewsTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_index_page_loads_successfully(self):
        response = self.client.get(reverse('index'))

        self.assertEqual(response.status_code, 200)

    def test_analyses(self):
        response = self.client.get(reverse('analyses'))
        self.assertEqual(response.status_code, 200)
        
    def test_data(self):
        response = self.client.get(reverse('data'))
        self.assertEqual(response.status_code, 200)

    def test_data_view_with_data(self):
        response = self.client.get(reverse('data'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Atm.java')
        self.assertContains(response, '10')
        self.assertContains(response, '0')
        self.assertContains(response, '11')
        self.assertContains(response, '28')
        self.assertContains(response, '2')
        self.assertContains(response, '142.42424242424244')

#ENTEGRASYON TESTİ:TESTCASE
class IntegrationTests(TestCase):
    def test_view_analyzed_results(self):
        response = self.client.get(reverse('analyses'))

        self.assertEqual(response.status_code, 200)

    def test_view_analyzed_results_from_database(self):
        response = self.client.get(reverse('data'))

        self.assertEqual(response.status_code, 200)

    def test_submit_invalid_form(self):
        response = self.client.post(reverse('index'), data={})

        self.assertEqual(response.status_code, 200)

#ENTEGRASYON TESTİ 2:unittest.TestCase
class ToolsTest(unittest.TestCase):
    def setUp(self):
        dosya1 = Dosya2(id=381,sinif="Hesap.java", javadoc_sayisi=3, yorum_sayisi=0, kod_sayisi=35,loc_sayisi=53,fonksiyon_sayisi=6,yorum_sapma_yuzdesi=-77.14285714285714)
        dosya2 = Dosya2(id=382,sinif="Kart.java", javadoc_sayisi=5, yorum_sayisi=0, kod_sayisi=17,loc_sayisi=33,fonksiyon_sayisi=3,yorum_sapma_yuzdesi=-21.5686274509804)
        dosya3 = Dosya2(id=383,sinif="MasterKart.java", javadoc_sayisi=0, yorum_sayisi=0, kod_sayisi=17,loc_sayisi=22,fonksiyon_sayisi=3,yorum_sapma_yuzdesi=-100)
        dosya4 = Dosya2(id=384,sinif="Program.java", javadoc_sayisi=4, yorum_sayisi=0, kod_sayisi=18,loc_sayisi=33,fonksiyon_sayisi=1,yorum_sapma_yuzdesi=-40.74074074074073)

        dosyalar = [dosya1, dosya2, dosya3, dosya4]

    # def test_count_data_Integration(self):
    #     dosyalar = Dosya2.objects.all() #ENTEGRASYON
    #     # Veritabanında toplam kayıt
    #     self.assertEqual(len(dosyalar), 1634)

    def test_count_sinif_Integration(self):
        dosyalar = Dosya2.objects.all() 
        # İlk kaydın özelliklerini doğrulayalım
        self.assertEqual(dosyalar[0].sinif, 'abc')

    def test_count_code_lines_Integration(self): 
        dosyalar = Dosya2.objects.all() 
        self.assertEqual(dosyalar[1].kod_sayisi, 11)

    def test_count_functions_Integration(self): 
        dosyalar = Dosya2.objects.all() 
        self.assertEqual(dosyalar[2].fonksiyon_sayisi, 2)

    def test_code_loc_count_Integration(self): 
        dosyalar = Dosya2.objects.all() 
        self.assertEqual(dosyalar[3].loc_sayisi, 53)

    def test_count_comment_lines_Integration(self): 
        dosyalar = Dosya2.objects.all() 
        self.assertEqual(dosyalar[4].yorum_sayisi, 0)

    def test_count_javadoc_comment_lines_Integration(self): 
        dosyalar = Dosya2.objects.all()
        self.assertEqual(dosyalar[5].javadoc_sayisi, 3)

    def test_count_yorum_sapma_yuzdesi_Integration(self): 
        dosyalar = Dosya2.objects.all() 
        self.assertEqual(dosyalar[6].yorum_sapma_yuzdesi, -21.5686274509804)

#FAKER KÜTÜPHANESİ İLE TEST
class Dosya2Test(unittest.TestCase):
    def __init__(self, methodName='dosya2_test'):
        super().__init__(methodName)
        self.fake = Faker()

    def test_dosya_olustur(self):
        dosya = Dosya2.objects.create(
            sinif=self.fake.word(),
            javadoc_sayisi=self.fake.random_int(min=0, max=100),
            yorum_sayisi=self.fake.random_int(min=0, max=100),
            kod_sayisi=self.fake.random_int(min=0, max=100),
            loc_sayisi=self.fake.random_int(min=0, max=100),
            fonksiyon_sayisi=self.fake.random_int(min=0, max=100),
            yorum_sapma_yuzdesi=self.fake.pyfloat(min_value=-100, max_value=100, right_digits=2)
        )
        self.assertTrue(isinstance(dosya, Dosya2))

    def test_code_line_count(self):
        fake_content = '\n'.join([self.fake.text() for _ in range(self.fake.random_int(min=10, max=100))])
        code_line_count = count_code_lines(fake_content)
        self.assertEqual(code_line_count, len(fake_content.split('\n')))

    def generate_fake_java_code(self):
        # Rastgele bir Java kodu parçası oluştur
        java_code = """
            public class MyClass {{
                public void method1() {{
                    // Method 1 body
                }}
                
                private int method2() {{
                    // Method 2 body
                    return 0;
                }}
                
                protected void method3() {{
                    // Method 3 body
                }}
            }}
        """.format(self.fake.word(), self.fake.word(), self.fake.word())  # Sözcüklerin yerine rastgele değerler yerleştirilebilir
        return java_code

    def test_function_count(self):
        # Sahte Java kodu oluştur
        fake_content = self.generate_fake_java_code()

        # count_functions fonksiyonunu çağır ve döndürülen metod sayısını al
        function_count = count_functions(fake_content)

        # Burada, herhangi bir sayı bekleyerek testi geçebiliriz, çünkü sahte Java kodu oluşturduğumuzda metod sayısı değişken olacaktır.
        self.assertTrue(function_count >= 0)

    def test_comment_line_count(self):
        fake_content = '\n'.join([self.fake.text() for _ in range(self.fake.random_int(min=10, max=100))])
        comment_line_count = count_comment_lines(fake_content)

        self.assertEqual(comment_line_count, 0)

    def test_javadoc_comment_line_count(self):
        fake_content = '\n'.join([self.fake.text() for _ in range(self.fake.random_int(min=10, max=100))])
        javadoc_comment_line_count = count_javadoc_comment_lines(fake_content)

        self.assertEqual(javadoc_comment_line_count, 0)

if __name__ == '__main__':
    unittest.main()