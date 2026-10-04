import os, shutil, zipfile, re
from xml.sax.saxutils import escape

SRC = "/home/iger/Документы/node-lab-website"
DOC_NAME = "task1_lab.docx"
OUT = os.path.join(SRC, DOC_NAME)

# Remove existing output
if os.path.exists(OUT):
    os.remove(OUT)

# Template DOCX minimal content
DOC_XML = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
<w:body>
'''

# Read original text from .doc
import subprocess
txt = subprocess.check_output(["catdoc", os.path.join(SRC, "completed_lab1.doc")], text=True)

# Parse tasks and insert screenshots
lines = txt.split('\n')
body = []
body.append('<w:p><w:r><w:t>Web Application Development Tools Laboratory Work N1</w:t></w:r></w:p>')

screenshots = {
    "Task 1.": "task1_node_versions.png",
    "Task 2.": "task2_project_tree.png",
    "Task 3.": "task3_index_html.png",
    "Task 4.": "task4_website_running.png",
    "Task 5.": "task5_css_styled.png",
    "Task 6.": "task6_js_effects.png",
}

# Build a simplified report from scratch with proper content
report_sections = [
    ("Task 1. Install NPM at your local environment.", "Установка Node.js и NPM", "task1_node_versions.png", 
     "Node.js v24.21.0, npm v11.19.0. Команды node -v и npm -v выполнены успешно."),
    ("Task 2. Create New Web App Project.", "Создание проекта Node.js с Express.js", "task2_project_tree.png",
     "Создана структура: package.json, server.js, express/index.html. Зависимости установлены (npm install)."),
    ("Task 3. Add design template to your Web App.", "Добавление дизайна", "task3_index_html.png",
     "Создан index.html с CSS-стилями для параграфа, div, ul, li, img. Добавлены анимации."),
    ("Task 4. Run Project.", "Запуск проекта", "task4_website_running.png",
     "Сервер запущен на порту 3000. HTTP 200. Сайт доступен по адресу localhost:3000."),
    ("Task 5. Add your unique CSS style to the project.", "CSS-стили", "task5_css_styled.png",
     "Добавлены стили: .paragraph-style, div.card, ul.list-style, img.rounded. Hover-эффекты и анимации."),
    ("Task 6. Add Javascript effects and animation", "JavaScript эффекты", "task6_js_effects.png",
     "Добавлены 3 JS-эффекта: клик по кнопке (счётчик), скролл-анимация, паралакс при движении мыши. CSS-анимации: fade-in, slide-in, pulse."),
    ("Task 7. Debug the code", "Отладка", None,
     "Ошибки и решения: 1) Express версия 4.17.1 заменена на 4.18.2. 2) Сервер иногда не запускался - добавлен sleep 2. 3) Firefox headless скриншоты."),
    ("Task 8. Commit final code to GitHub.", "GitHub", None,
     "Не выполняется по просьбе пользователя."),
]

for title, subtitle, screenshot, result in report_sections:
    body.append(f'<w:p><w:pPr><w:b/></w:pPr><w:r><w:t>{escape(title)}</w:t></w:r></w:p>')
    body.append(f'<w:p><w:i><w:r><w:t>{escape(subtitle)}</w:t></w:r></i></w:p>')
    body.append(f'<w:p><w:r><w:t>{escape(result)}</w:t></w:r></w:p>')
    if screenshot:
        body.append(f'<w:p><w:r><w:drawing><wp:inline distT="0" distB="0" distL="0" distR="0"><wp:extent cx="5943600" cy="4191600"/><wp:effectExtent l="0" t="0" r="0" b="0"/><wp:docPr id="0" name="{screenshot}"/><wp:cNvGraphicFramePr><a:graphicFrameLocks xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" noChangeAspect="1"/></wp:cNvGraphicFramePr><a:graphic xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"><a:graphicData uri="http://schemas.openxmlformats.org/drawingml/2006/picture"><pic:pic xmlns:pic="http://schemas.openxmlformats.org/drawingml/2006/picture" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"><pic:nvPicPr><pic:cNvPr id="0" name="{screenshot}"/><pic:cNvPicPr/></pic:nvPicPr><pic:blipFill><a:blip r:embed="rId{screenshots[screenshot]}"/><a:stretch><a:fillRect/></a:stretch></pic:blipFill><pic:spPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="5943600" cy="4191600"/></a:xfrm><a:prstGeom prst="rect"><a:avLst/></a:prstGeom></pic:spPr></pic:pic></a:graphicData></a:graphic></wp:inline></w:drawing></w:r></w:p>')

body.append('</w:body></w:document>')

# Create DOCX zip
with zipfile.ZipFile(OUT, 'w', zipfile.ZIP_DEFLATED) as docx:
    # [Content_Types].xml
    content_types = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="xml" ContentType="application/xml"/><Default Extension="png" ContentType="image/png"/><Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/></Types>'
    docx.writestr('[Content_Types].xml', content_types)
    
    # _rels/.rels
    rels = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/></Relationships>'
    docx.writestr('_rels/.rels', rels)
    
    # word/document.xml
    doc_xml = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n' + '\n'.join(body)
    docx.writestr('word/document.xml', doc_xml)
    
    # word/_rels/document.xml.rels - relationships to images
    img_rels = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
    for i, (_, _, screenshot, _) in enumerate(report_sections):
        if screenshot:
            rid = f'rId{i+1}'
            img_rels += f'<Relationship Id="{rid}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="../media/{screenshot}"/>'
    img_rels += '</Relationships>'
    docx.writestr('word/_rels/document.xml.rels', img_rels)
    
    # Media files
    for _, _, screenshot, _ in report_sections:
        if screenshot:
            img_path = os.path.join(SRC, "screenshots", screenshot)
            docx.write(img_path, f"word/media/{screenshot}")

print(f"DOCX created: {OUT} ({os.path.getsize(OUT)} bytes)")
print("Files included:")
with zipfile.ZipFile(OUT) as z:
    for name in z.namelist():
        print(f"  {name}")
