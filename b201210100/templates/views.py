from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
import os, re
from django.conf import settings
from git import Repo
from veriproje.mymodels.Dosya import Dosya2
from veriproje.forms import GitHubRepoForm
from veriproje.tools import count_code_lines
from veriproje.tools import count_comment_lines
from veriproje.tools import count_functions
from veriproje.tools import count_javadoc_comment_lines
from veriproje.tools import code_loc_count

# Analiz sonuçları için
analysis_results = {}

def is_class_file(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        content = file.read()
        if "class" in content:
            return True
        else:
            return False

def index(request):
    global analysis_results

    if request.method == 'POST':
        form = GitHubRepoForm(request.POST)
        if form.is_valid():
            repo_url = form.cleaned_data['repo_url']

            # Klonlanacak dizin ve yol
            current_dir = os.getcwd()  # Mevcut çalışma dizinini alıyoruz
            clone_path = os.path.join(current_dir, "cloned_repo")  # Klonlanacak dizin yolu

            # GitHub deposunu klonla
            if not os.path.exists(clone_path):
                os.makedirs(clone_path)

            try:
                Repo.clone_from(repo_url, clone_path)
                print("Clone işlemi başarılı")
            except Exception as e:
                print(f"Clone işlemi sırasında hata oluştu: {str(e)}")

            # *.java dosyalarını içeren sınıfları al
            java_files = []
            for root, dirs, files in os.walk(clone_path):
                for file in files:
                    if file.endswith(".java"):
                        file_path = os.path.join(root, file)
                        if is_class_file(file_path):
                            java_files.append(file_path)

            # Sınıfları analiz et
            class_files = []
            for java_file in java_files:
                with open(java_file, "r", encoding="utf-8") as f:
                    content = f.read()
                    if re.search(r"\bclass\b", content):
                        class_files.append(java_file)
            

            # Sınıfların analizi
            for class_file in class_files:
                with open(class_file, "r", encoding="utf-8") as f:
                    content = f.read()
                    comments_count = count_comment_lines(content)
                    javadoc_count =count_javadoc_comment_lines(content)
                    code_lines_count = count_code_lines(content)
                    function_count = count_functions(content)
                    loc_count = code_loc_count(content)

                    # Yorum Sapma Yüzdesi'nin Hesabı
                    if function_count != 0:
                        YG = ((javadoc_count + comments_count) * 0.8) / function_count
                    else:
                        YG = 0  # Fonksiyon sayısı sıfırsa yorum sapma yüzdesini sıfır yap
                    if function_count != 0:
                        YH = (code_lines_count / function_count) * 0.3
                    else:
                        YH = 0  # Fonksiyon sayısı sıfırsa yorum sapma yüzdesini sıfır yap
                    
                    if YH != 0:
                        yorum_sapma_yuzdesi = ((100 * YG) / YH) - 100
                    else:
                        yorum_sapma_yuzdesi = 0  # YH sıfırsa yorum sapma yüzdesini sıfır yap

                    file_name = os.path.basename(class_file)

                    analysis_results[class_file] = {
                        "Sınıf":file_name,
                        "Javadoc_Satır_Sayısı": javadoc_count,
                        "Yorum_Satır_Sayısı": comments_count,
                        "Kod_Satır_Sayısı": code_lines_count,
                        "LOC": loc_count,
                        "Fonksiyon_Sayısı": function_count,
                        "Yorum_Sapma_Yüzdesi": yorum_sapma_yuzdesi
                    }
                    
                    # Analiz sonuçlarını veritabanına kaydet
                    for class_file, result in analysis_results.items():
                        Dosya2.objects.create(
                            sinif=result["Sınıf"],
                            javadoc_sayisi=result["Javadoc_Satır_Sayısı"],
                            yorum_sayisi=result["Yorum_Satır_Sayısı"],
                            kod_sayisi=result["Kod_Satır_Sayısı"],
                            loc_sayisi=result["LOC"],
                            fonksiyon_sayisi=result["Fonksiyon_Sayısı"],
                            yorum_sapma_yuzdesi=result["Yorum_Sapma_Yüzdesi"]
                        )
            return HttpResponseRedirect('/analyses/')
    else:
        form = GitHubRepoForm()
    
    return render(request, 'index.html', {'form': form})


def analyses(request):
    global analysis_results
    return render(request, 'analyses.html', {'analysis_results': analysis_results})

def data(request):
    # Tüm analiz verilerini veritabanından al
    dosyalar = Dosya2.objects.all()
    return render(request, 'data.html', {'dosyalar': dosyalar})