import os,re
import javalang

def count_code_lines(file_content):
    lines = file_content.split('\n')  # Dosya içeriğini satırlara böl
    code_lines = 0
    
    for line in lines:
        line = line.strip()  # Satırın başındaki ve sonundaki boşlukları temizle
        
        # Boş satırları veya yorum satırlarını kontrol et
        if line == '' or line.startswith('//') or line.startswith('/*') or line.startswith('*') or line.startswith('*/'):
            continue  # Boş satır veya yorum satırı ise atla
        
        code_lines += 1 
        
    return code_lines

def count_functions(file_content):
    # Java kodunu parçala
    tree = javalang.parse.parse(file_content)
    method_count = 0

    # Her bir sınıf tanımını kontrol et
    for _, node in tree:
        if isinstance(node, javalang.tree.ConstructorDeclaration) or isinstance(node, javalang.tree.MethodDeclaration):
            method_count += 1

    return method_count

def code_loc_count(file_content):  #LOC 
    lines = file_content.split('\n')
    
    # Eğer dosyanın son satırı boşsa, onu hesaplamadan önce çıkar
    if lines[-1] == '':
        lines.pop()
        
    return len(lines)

def count_comment_lines(java_code):
    in_multi_line_comment = False
    comments = 0

    lines = java_code.split("\n")
    for line in lines:
        line = line.strip()
        if line.startswith("//") or '//' in line:  # Tek satırlık yorum satırı
            comments+=1
        elif line.startswith("/*") and not line.startswith('/**'):  # Çok satırlık yorumun başlangıcı
            in_multi_line_comment = True
        elif line.endswith("*/"):  # Çok satırlık yorumun sonu
            in_multi_line_comment = False
        elif in_multi_line_comment:  # Çok satırlık yorum içerisindeki satırlar
            comments+=1
    return comments

def count_javadoc_comment_lines(file_content):
    lines = file_content.split('\n')
    in_comment_block = False
    javadoc_comments = []

    for line in lines:
        line = line.strip()

        if '*/' in line and in_comment_block:
            in_comment_block = False
            continue
        elif line.startswith('/**'):
            in_comment_block = True
            if '*/' in line:
                in_comment_block = False
            continue
        elif in_comment_block:
            javadoc_comments.append(line)

    javadoc_lines = [comment for comment in javadoc_comments if comment.strip() != '']

    return len(javadoc_lines)