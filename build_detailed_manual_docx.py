"""
Script to generate a comprehensive, beautifully styled User Manual (DOCX)
for the PURE & OLIVE E-Commerce Platform.
Includes Cover Page, System Overview, Customer Guide, Admin Guide,
Database Dictionary, Installation Steps, and Test Cases.
"""
import os
import sys
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import parse_xml, OxmlElement
from docx.oxml.ns import nsdecls, qn

def set_cell_background(cell, fill_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    tcPr.append(parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>'))

def set_cell_margins(cell, top=120, bottom=120, left=180, right=180):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        node = OxmlElement(f'w:{m}')
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def add_callout_box(doc, title, text, bg_hex="F4F6F3", border_hex="4A5D4C"):
    table = doc.add_table(rows=1, cols=1)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell = table.cell(0, 0)
    set_cell_background(cell, bg_hex)
    set_cell_margins(cell, 140, 140, 200, 200)

    tcPr = cell._tc.get_or_add_tcPr()
    tcBorders = parse_xml(
        f'<w:tcBorders {nsdecls("w")}>\n'
        f'  <w:top w:val="none"/>\n'
        f'  <w:left w:val="single" w:sz="24" w:space="0" w:color="{border_hex}"/>\n'
        f'  <w:bottom w:val="none"/>\n'
        f'  <w:right w:val="none"/>\n'
        f'</w:tcBorders>'
    )
    tcPr.append(tcBorders)

    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(4)
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.line_spacing = 1.25

    run_t = p.add_run(f"📌 {title}\n")
    run_t.font.name = 'Cordia New'
    run_t.font.size = Pt(14)
    run_t.font.bold = True
    run_t.font.color.rgb = RGBColor(47, 62, 49)

    run_body = p.add_run(text)
    run_body.font.name = 'Cordia New'
    run_body.font.size = Pt(13)
    run_body.font.color.rgb = RGBColor(50, 50, 50)

    p_spacer = doc.add_paragraph()
    p_spacer.paragraph_format.space_after = Pt(6)

def create_manual():
    doc = Document()

    # Page Margins
    for section in doc.sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)

    # Base Normal Style
    style_normal = doc.styles['Normal']
    font = style_normal.font
    font.name = 'Cordia New'
    font.size = Pt(14)
    font.color.rgb = RGBColor(40, 48, 40)

    # ========================================================
    # COVER PAGE
    # ========================================================
    p_badge = doc.add_paragraph()
    p_badge.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_badge.paragraph_format.space_before = Pt(60)
    p_badge.paragraph_format.space_after = Pt(10)
    r_badge = p_badge.add_run("🌿 โครงการพัฒนาระบบพาณิชย์อิเล็กทรอนิกส์ (E-Commerce Web Application)")
    r_badge.font.name = 'Cordia New'
    r_badge.font.size = Pt(15)
    r_badge.font.bold = True
    r_badge.font.color.rgb = RGBColor(126, 147, 124)

    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_title.paragraph_format.space_after = Pt(14)
    r_title = p_title.add_run("คู่มือการใช้งานเว็บไซต์และเอกสารประกอบโครงงาน\n(Official System Manual & User Guide)")
    r_title.font.name = 'Cordia New'
    r_title.font.size = Pt(26)
    r_title.font.bold = True
    r_title.font.color.rgb = RGBColor(47, 62, 49)

    p_sub = doc.add_paragraph()
    p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_sub.paragraph_format.space_after = Pt(30)
    r_sub = p_sub.add_run(
        "ร้านสกินแคร์ เครื่องสำอางคลีนบิวตี้ และอุปกรณ์เสริมความงาม\n"
        "« PURE & OLIVE — Minimal & Clean Beauty »\n"
        "พร้อมระบบแบบทดสอบวิเคราะห์สภาพผิวอัจฉริยะ (Skin Quiz & Routine Builder)"
    )
    r_sub.font.name = 'Cordia New'
    r_sub.font.size = Pt(17)
    r_sub.font.bold = True
    r_sub.font.color.rgb = RGBColor(74, 93, 76)

    # Project Info Box
    p_meta = doc.add_paragraph()
    p_meta.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_meta.paragraph_format.space_before = Pt(100)
    p_meta.paragraph_format.line_spacing = 1.3
    r_meta = p_meta.add_run(
        "จัดทำโดย\n"
        "นักศึกษา รหัสประจำตัว 075\n\n"
        "เสนอ\n"
        "อาจารย์ประจำรายวิชาการพัฒนาเว็บแอปพลิเคชันและเทคโนโลยีพาณิชย์อิเล็กทรอนิกส์\n"
        "ภาคการศึกษาที่ 2 ประจำปีการศึกษา 2569\n"
        "สถานะระบบ: ผ่านการทดสอบระดับ Full-Stack พร้อมใช้งาน 100%"
    )
    r_meta.font.name = 'Cordia New'
    r_meta.font.size = Pt(14)

    doc.add_page_break()

    # ========================================================
    # TABLE OF CONTENTS
    # ========================================================
    h_toc = doc.add_heading("สารบัญเนื้อหา (Table of Contents)", level=1)
    h_toc.paragraph_format.space_after = Pt(12)
    for r in h_toc.runs:
        r.font.name = 'Cordia New'
        r.font.size = Pt(20)
        r.font.bold = True
        r.font.color.rgb = RGBColor(47, 62, 49)

    toc_items = [
        ("บทที่ 1: บทนำและแนวคิดการออกแบบเว็บไซต์ (Project Concept)", "หน้า 3"),
        ("บทที่ 2: สถาปัตยกรรมและโครงสร้างไฟล์ของระบบ (System Architecture)", "หน้า 4"),
        ("บทที่ 3: คู่มือการใช้งานสำหรับลูกค้า / ผู้ใช้งานทั่วไป (Customer Guide)", "หน้า 5"),
        ("   3.1 การเข้าชมหน้าแรกและเมนูหลัก (Homepage Overview)", "หน้า 5"),
        ("   3.2 การค้นหาและตัวกรองตามปัญหาผิว (Catalog & Skin Concern Filters)", "หน้า 6"),
        ("   3.3 การทำแบบทดสอบวิเคราะห์สภาพผิว (Skin Quiz & Routine Builder)", "หน้า 7"),
        ("   3.4 หน้ารายละเอียดสินค้า สารสกัดเด่น และการรีวิว (Product & Reviews)", "หน้า 8"),
        ("   3.5 ระบบตะกร้าสินค้า คูปองส่วนลด และการส่งฟรี (Cart & Drawer)", "หน้า 9"),
        ("   3.6 ขั้นตอนการสั่งซื้อและการชำระเงินจำลอง (Checkout & PromptPay QR)", "หน้า 10"),
        ("บทที่ 4: คู่มือการใช้งานสำหรับผู้ดูแลระบบ (Admin Dashboard Guide)", "หน้า 11"),
        ("   4.1 การเข้าใช้งานระบบหลังบ้าน (/admin)", "หน้า 11"),
        ("   4.2 การตรวจสอบสรุปสถิติ (KPIs Dashboard)", "หน้า 11"),
        ("   4.3 การจัดการคำสั่งซื้อและเปลี่ยนสถานะจัดส่ง (Order Management)", "หน้า 12"),
        ("   4.4 การตรวจเช็คสต็อกสินค้าและเพิ่มสินค้าใหม่ (Product Inventory)", "หน้า 12"),
        ("บทที่ 5: พจนานุกรมข้อมูลและโครงสร้างฐานข้อมูล (Data Dictionary)", "หน้า 13"),
        ("บทที่ 6: ขั้นตอนการติดตั้งและรันโปรแกรม (Setup & Execution Guide)", "หน้า 15"),
        ("ภาคผนวก: ข้อมูลทดสอบระบบ (Test Cases & Demo Data)", "หน้า 16")
    ]

    for title, page in toc_items:
        p_toc = doc.add_paragraph()
        p_toc.paragraph_format.space_after = Pt(4)
        p_toc.paragraph_format.line_spacing = 1.15
        r_t = p_toc.add_run(title)
        r_t.font.name = 'Cordia New'
        r_t.font.size = Pt(13)
        if not title.startswith("   "):
            r_t.font.bold = True

    doc.add_page_break()

    # ========================================================
    # CHAPTER 1: CONCEPT
    # ========================================================
    h1 = doc.add_heading("บทที่ 1: บทนำและแนวคิดการออกแบบเว็บไซต์ (Project Concept)", level=1)
    h1.paragraph_format.space_after = Pt(10)
    for r in h1.runs:
        r.font.name = 'Cordia New'
        r.font.size = Pt(18)
        r.font.bold = True
        r.font.color.rgb = RGBColor(47, 62, 49)

    doc.add_paragraph(
        "เว็บไซต์ PURE & OLIVE (เพียว แอนด์ โอลีฟ) ได้รับการพัฒนาขึ้นตามโจทย์โครงงานพาณิชย์อิเล็กทรอนิกส์ "
        "โดยเน้นกลุ่มสินค้า 'อุปกรณ์เสริมความงาม เครื่องสำอาง และครีมสกินแคร์' ซึ่งเป็นหมวดหมู่ธุรกิจที่มีการเติบโตสูง "
        "และต้องการความน่าเชื่อถือในด้านความปลอดภัยของส่วนผสมเป็นอันดับแรก"
    )

    doc.add_heading("1.1 เอกลักษณ์และธีมการออกแบบ (Mood & Tone)", level=2)
    doc.add_paragraph(
        "ระบบใช้แนวคิด Minimalist & Clean Beauty ที่ได้รับแรงบันดาลใจจากธรรมชาติและสวนมะกอกออร์แกนิกในแถบเมดิเตอร์เรเนียน "
        "โดยมีองค์ประกอบหลักดังนี้:"
    )

    theme_points = [
        ("โทนสีหลัก (Primary Color):", "สีเขียวโอลีฟธรรมชาติ (#4A5D4C) สื่อถึงความบริสุทธิ์ สมุนไพรพฤกษศาสตร์ และความผ่อนคลาย"),
        ("โทนสีรอง (Secondary Color):", "สีเขียวเซจละมุน (#8FA382) และสีขาวอุ่นละมุนตา (#FAF8F5 / #FFF) สร้างบรรยากาศคลีน โปร่งสบาย"),
        ("สีเน้นจุดสัมผัส (Accent Color):", "สีส้มอิฐนู้ด (Terracotta #C7826F) สื่อถึงความอบอุ่น มีชีวิตชีวา และสีทองอ่อนสำหรับคะแนนดาวรีวิว"),
        ("ตัวอักษร (Typography):", "ใช้แบบอักษร 'Prompt' ผสานกับ 'Playfair Display' ให้ภาพลักษณ์ที่ร่วมสมัย หรูหรา สะอาด และอ่านง่ายบนทุกอุปกรณ์")
    ]
    for label, val in theme_points:
        p = doc.add_paragraph()
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.left_indent = Inches(0.2)
        r1 = p.add_run(f"• {label} ")
        r1.font.bold = True
        p.add_run(val)

    add_callout_box(
        doc,
        "จุดเด่นด้านมาตรฐานผลิตภัณฑ์ (Clean Beauty Standards)",
        "ผลิตภัณฑ์ทุกชิ้นในร้านยึดหลัก 100% Vegan (ปราศจากสารสกัดจากสัตว์), Cruelty-Free (ไม่ทดลองกับสัตว์), "
        "Dermatologist Tested (ผ่านการทดสอบโดยแพทย์ผิวหนัง) และไม่มีส่วนผสมของพาราเบน แอลกอฮอล์เข้มข้น และน้ำหอมสังเคราะห์"
    )

    doc.add_page_break()

    # ========================================================
    # CHAPTER 2: ARCHITECTURE
    # ========================================================
    h2 = doc.add_heading("บทที่ 2: สถาปัตยกรรมและโครงสร้างไฟล์ของระบบ (System Architecture)", level=1)
    h2.paragraph_format.space_after = Pt(10)
    for r in h2.runs:
        r.font.name = 'Cordia New'
        r.font.size = Pt(18)
        r.font.bold = True
        r.font.color.rgb = RGBColor(47, 62, 49)

    doc.add_paragraph(
        "ระบบพัฒนาด้วยสถาปัตยกรรม Model-View-Controller (MVC) แบบ Monolithic ที่มีความกระชับ ติดตั้งง่าย และมีประสิทธิภาพสูง "
        "ประกอบด้วย 3 องค์ประกอบหลัก:"
    )

    arch_table = doc.add_table(rows=5, cols=3)
    arch_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    headers = ["องค์ประกอบ", "เครื่องมือ / ภาษา", "หน้าที่รับผิดชอบ"]
    rows = [
        ["Backend (Controller)", "Python Flask 3.1", "ประมวลผลคำสั่ง ควบคุมระบบ Routing, Session, REST APIs และการคำนวณส่วนลด"],
        ["Database (Model)", "SQLite 3", "จัดเก็บข้อมูลสินค้า ตะกร้า ออเดอร์ รีวิว พร้อมระบบ Foreign Key และ Transaction"],
        ["Frontend (View)", "HTML5 + Jinja2 Templates", "เรนเดอร์โครงสร้างหน้าเว็บ แบ่งเป็น base layout และเพจย่อย 8 หน้า"],
        ["Client Interaction", "Modern CSS3 + JavaScript ES6", "ระบบตะกร้าสินค้า LocalStorage, Cart Drawer, Animation, Toast, Skin Quiz Wizard"]
    ]
    for c_idx, h_text in enumerate(headers):
        cell = arch_table.cell(0, c_idx)
        cell.paragraphs[0].text = h_text
        cell.paragraphs[0].runs[0].font.bold = True
        cell.paragraphs[0].runs[0].font.size = Pt(13)
        set_cell_background(cell, "EBF0E9")
        set_cell_margins(cell, 100, 100, 120, 120)

    for r_idx, row_data in enumerate(rows, start=1):
        for c_idx, val in enumerate(row_data):
            cell = arch_table.cell(r_idx, c_idx)
            cell.paragraphs[0].text = val
            cell.paragraphs[0].runs[0].font.size = Pt(12)
            set_cell_margins(cell, 70, 70, 100, 100)

    doc.add_paragraph().paragraph_format.space_after = Pt(12)
    doc.add_heading("2.1 โครงสร้างไฟล์ในระบบ (Project Directory Structure)", level=2)

    dir_structure = (
        "C:\\075\\\n"
        "├── app.py                      # เซิร์ฟเวอร์หลัก Flask และ REST APIs\n"
        "├── database.py                 # ตัวจัดการเชื่อมต่อ SQLite และการสร้างตาราง\n"
        "├── seed_data.py                # ข้อมูลสินค้าตั้งต้น 17 รายการ และรีวิวตัวอย่าง\n"
        "├── pure_olive.db               # ฐานข้อมูล SQLite\n"
        "├── verify_app.py               # สคริปต์ Automated Test ตรวจสอบทุก Route และ API\n"
        "├── create_manual_docx.py       # สคริปต์สร้างเอกสารคู่มือ Word เล่มนี้\n"
        "├── README.md                   # เอกสารสรุปโครงการ\n"
        "├── static/\n"
        "│   ├── css/style.css           # สไตล์ชีตโทนมินิมอลขาว-เขียวโอลีฟ\n"
        "│   └── js/\n"
        "│       ├── main.js             # ตัวจัดการตะกร้า LocalStorage, Drawer, Toast\n"
        "│       └── quiz.js             # เอนจินวิเคราะห์สภาพผิวและจัด Routine Bundle\n"
        "└── templates/\n"
        "    ├── base.html               # โครงสร้างหลัก Header, Nav, Drawer, Footer\n"
        "    ├── index.html              # หน้าแรก สรุปโปรโมชั่น และสินค้าขายดี\n"
        "    ├── products.html           # หน้ารวมสินค้า ตัวกรองปัญหาผิว และค้นหา\n"
        "    ├── product_detail.html     # หน้ารายละเอียดสินค้า สเปก และรีวิว\n"
        "    ├── routine_quiz.html       # หน้าแบบทดสอบวิเคราะห์สภาพผิว 3 ขั้นตอน\n"
        "    ├── cart.html               # หน้าตะกร้าสินค้า คูปอง และชำระเงิน\n"
        "    ├── order_success.html      # หน้าใบเสร็จรับเงิน และ QR Code พร้อมเพย์\n"
        "    ├── tips.html               # บทความปรัชญา Clean Beauty และคู่มือนวดหน้า\n"
        "    └── admin.html              # ระบบหลังบ้านสำหรับแอดมิน\n"
    )

    p_code = doc.add_paragraph()
    p_code.paragraph_format.left_indent = Inches(0.2)
    p_code.paragraph_format.space_after = Pt(14)
    r_code = p_code.add_run(dir_structure)
    r_code.font.name = 'Consolas'
    r_code.font.size = Pt(10.5)
    r_code.font.color.rgb = RGBColor(40, 60, 45)

    doc.add_page_break()

    # ========================================================
    # CHAPTER 3: CUSTOMER GUIDE
    # ========================================================
    h3 = doc.add_heading("บทที่ 3: คู่มือการใช้งานสำหรับลูกค้า / ผู้ใช้งานทั่วไป (Customer Guide)", level=1)
    h3.paragraph_format.space_after = Pt(10)
    for r in h3.runs:
        r.font.name = 'Cordia New'
        r.font.size = Pt(18)
        r.font.bold = True
        r.font.color.rgb = RGBColor(47, 62, 49)

    doc.add_paragraph(
        "ส่วนนี้อธิบายขั้นตอนการเข้าใช้งานและการสั่งซื้อสินค้าสำหรับลูกค้าทั่วไป "
        "โดยออกแบบให้ใช้งานง่าย (User-Friendly) ทั้งบนคอมพิวเตอร์ แท็บเล็ต และสมาร์ตโฟน"
    )

    sections = [
        ("3.1 หน้าแรกของเว็บไซต์ (Homepage Overview)", [
            "แถบประกาศด้านบน (Announcement Bar): แจ้งสิทธิ์ส่งฟรีเมื่อครบ 990 บาท และโค้ดส่วนลดแนะนำ CLEAN10",
            "ส่วนหัวของเว็บ (Navbar): มีโลโก้แบรนด์ PURE & OLIVE เมนูหมวดหมู่ ปุ่มแบบทดสอบวิเคราะห์สภาพผิว (Skin Quiz) และไอคอนตะกร้าพร้อมตัวเลขนับจำนวนสินค้าแบบเรียลไทม์",
            "แบนเนอร์หลัก (Hero Banner): นำเสนอภาพลักษณ์คลีน พร้อมปุ่ม 'ช้อปสินค้าทั้งหมด' และ 'วิเคราะห์สภาพผิว'",
            "สัญลักษณ์ความน่าเชื่อถือ (Trust Badges): 100% Clean & Vegan, Cruelty-Free, จัดส่งฟรี, บรรจุภัณฑ์รักษ์โลก Eco-Friendly",
            "หมวดหมู่แนะนำ 3 ด้าน: สกินแคร์ & ครีม, เครื่องสำอางคลีนบิวตี้ และอุปกรณ์เสริมความงาม",
            "สินค้าขายดียอดนิยม (Bestsellers): การ์ดสินค้าแสดงภาพ ราคา คะแนนรีวิว และปุ่ม Quick Add to Cart",
            "ปรัชญาสารสกัดพฤกษศาสตร์: อธิบายคุณค่าของ Olive Squalane, Centella, Ceramide 5 ชนิด และ Bakuchiol",
            "รีวิวจากผู้ใช้จริง: การ์ดรีวิวแสดงความคิดเห็น ดาว และแท็กระบุสภาพผิวของผู้รีวิว"
        ]),

        ("3.2 การค้นหาและตัวกรองตามปัญหาผิว (Catalog & Filters)", [
            "การเข้าถึง: คลิกเมนู 'สินค้าทั้งหมด' หรือเลือกหมวดที่ต้องการจากเมนูบาร์",
            "ช่องค้นหา (Search Box): พิมพ์คำค้นหา เช่น 'serum', 'ครีม', 'บาคูชิออล' ระบบจะค้นหาจากชื่อและส่วนผสมทันที",
            "แถบตัวกรองปัญหาผิว (Skin Concern Pills): คลิกเพื่อกรองเฉพาะสินค้าที่ตอบโจทย์ เช่น 'สิวและคุมมัน', 'ผิวแห้งขาดน้ำ', 'ฟื้นฟูเกราะป้องกันผิว', 'ชะลอวัย' หรือ 'ผิวกระจ่างใส'",
            "การจัดเรียง (Sorting): เลือกเรียงตาม 'ความนิยม', 'คะแนนรีวิวสูงสุด', 'ราคา: ต่ำไปสูง', 'ราคา: สูงไปต่ำ' หรือ 'สินค้ามาใหม่'"
        ]),

        ("3.3 การทำแบบทดสอบวิเคราะห์สภาพผิว (Skin Quiz & Routine Builder)", [
            "การเข้าถึง: คลิกปุ่ม 'วิเคราะห์สภาพผิว' บนแถบเมนู หรือลิงก์บนหน้าแรก",
            "ขั้นตอนที่ 1 (สภาพผิว): เลือกระหว่าง 'ผิวผสม', 'ผิวมัน', 'ผิวแห้ง' หรือ 'ผิวบอบบางแพ้ง่าย'",
            "ขั้นตอนที่ 2 (ปัญหาผิวหลัก): เลือกระหว่าง 'สิวอุดตัน/รอยสิว', 'ฟื้นฟูเกราะป้องกันผิว', 'ผิวขาดน้ำ' หรือ 'ริ้วรอย/ยกกระชับ'",
            "ขั้นตอนที่ 3 (สไตล์การดูแล): เลือกระหว่าง 'Complete Ritual + บิวตี้ทูลส์' หรือ 'Minimalist Daily 5 นาทีจบ'",
            "ผลลัพธ์การวินิจฉัย (Results): ระบบจะแสดงคำแนะนำเฉพาะบุคคล รูทีนตอนเช้า (Morning Routine Step 1-5) และรูทีนก่อนนอน (Night Routine Step 1-5)",
            "การสั่งซื้อเซตแนะนำ: มีการ์ดข้อเสนอพิเศษรวมสินค้าทุกชิ้นในรูทีน พร้อมคำนวณส่วนลดเซต 15% และปุ่ม 'สั่งซื้อเซตแนะนำนี้ลงตะกร้าทันที' ใน 1 คลิก"
        ]),

        ("3.4 หน้ารายละเอียดสินค้าและการส่งรีวิว (Product Details & Reviews)", [
            "ข้อมูลสินค้าครบถ้วน: แสดงชื่อไทย-อังกฤษ ราคาเดิม ราคาลด ปริมาณ และสถานะสต็อกพร้อมส่ง",
            "สารสกัดเด่นและวิธีใช้: ระบุ Key Ingredients และ How to Use อย่างละเอียด",
            "ปุ่มปรับจำนวนสินค้า: ปรับเพิ่ม/ลดจำนวนที่ต้องการสั่งซื้อ และกดปุ่ม 'เพิ่มลงตะกร้าสินค้า'",
            "การส่งรีวิว (Write a Review): ลูกค้าสามารถกรอกชื่อ เลือกสภาพผิวของตนเอง (เช่น ผิวผสม แพ้ง่าย) ให้คะแนน 1-5 ดาว และพิมพ์ความคิดเห็น เมื่อกดส่ง ข้อมูลจะถูกบันทึกและคำนวณคะแนนเฉลี่ยใหม่ทันที"
        ]),

        ("3.5 ระบบตะกร้าสินค้า คูปอง และการชำระเงิน (Cart & Checkout)", [
            "Cart Drawer (ตะกร้าสไลด์ข้าง): กดไอคอน 🛒 เพื่อเปิดดูรายการสินค้า ปรับจำนวน หรือลบสินค้าได้ทันที",
            "หน้าตะกร้าเต็มรูปแบบ (/cart): แสดงแถบคำนวณสิทธิ์ส่งฟรี (เป้าหมาย 990 บาท)",
            "การใช้โค้ดส่วนลด: กรอกโค้ด เช่น CLEAN10 (ลด 10%) หรือ OLIVE50 (ลด 50 บาท) แล้วกด 'ใช้โค้ด'",
            "ฟอร์มที่อยู่จัดส่ง: กรอกชื่อ-นามสกุล เบอร์โทรศัพท์ อีเมล และที่อยู่จัดส่งโดยละเอียด",
            "ช่องทางชำระเงิน: เลือกได้ 3 วิธี (PromptPay QR, บัตรเครดิต/เดบิต, เก็บเงินปลายทาง COD)",
            "ยืนยันคำสั่งซื้อ: กดปุ่ม 'ยืนยันการสั่งซื้อและชำระเงิน' ระบบจะสร้างเลขออเดอร์ หักสต็อก และเปลี่ยนไปหน้าใบเสร็จ"
        ]),

        ("3.6 หน้าใบเสร็จรับเงินและการพิมพ์ (Receipt & Print View)", [
            "แสดงรหัสคำสั่งซื้อ เช่น PO-20261110-XXXX และหมายเลขพัสดุสำหรับติดตาม (Tracking Number)",
            "กรณีเลือกพร้อมเพย์: ระบบจะแสดงภาพ QR Code จำลองพร้อมยอดเงินสุทธิให้ลูกค้าเห็น",
            "ตารางสรุปรายการ: แสดงสินค้า จำนวน ราคา ส่วนลด และยอดชำระสุทธิ",
            "ปุ่มพิมพ์ใบเสร็จ: กดปุ่ม 'พิมพ์ใบเสร็จรับเงิน' เพื่อเปิดมุมมอง Print View จัดหน้ากระดาษอย่างเป็นระเบียบ"
        ])
    ]

    for title, points in sections:
        sub = doc.add_heading(title, level=2)
        sub.paragraph_format.space_after = Pt(4)
        for r in sub.runs:
            r.font.name = 'Cordia New'
            r.font.size = Pt(14)
            r.font.bold = True
            r.font.color.rgb = RGBColor(74, 93, 76)

        for pt in points:
            p = doc.add_paragraph()
            p.paragraph_format.space_after = Pt(3)
            p.paragraph_format.left_indent = Inches(0.2)
            parts = pt.split(":", 1)
            if len(parts) == 2:
                r1 = p.add_run(f"• {parts[0]}: ")
                r1.font.bold = True
                p.add_run(parts[1])
            else:
                p.add_run(f"• {pt}")

    doc.add_page_break()

    # ========================================================
    # CHAPTER 4: ADMIN GUIDE
    # ========================================================
    h4 = doc.add_heading("บทที่ 4: คู่มือการใช้งานสำหรับผู้ดูแลระบบ (Admin Dashboard Guide)", level=1)
    h4.paragraph_format.space_after = Pt(10)
    for r in h4.runs:
        r.font.name = 'Cordia New'
        r.font.size = Pt(18)
        r.font.bold = True
        r.font.color.rgb = RGBColor(47, 62, 49)

    doc.add_paragraph(
        "ระบบหลังบ้าน (Admin Dashboard) ถูกออกแบบมาเพื่ออำนวยความสะดวกให้เจ้าของร้านสามารถตรวจสอบภาพรวมธุรกิจ "
        "อัปเดตสถานะการจัดส่ง และจัดการสต็อกสินค้าได้อย่างสะดวกรวดเร็วโดยไม่ต้องเปิดดูฐานข้อมูลโดยตรง"
    )

    doc.add_heading("4.1 การเข้าใช้งานระบบหลังบ้าน", level=2)
    doc.add_paragraph("ผู้ดูแลระบบสามารถเข้าใช้งานได้โดยเปิดเว็บเบราว์เซอร์ไปที่:")
    p_url = doc.add_paragraph()
    p_url.paragraph_format.left_indent = Inches(0.2)
    r_u = p_url.add_run("URL: http://127.0.0.1:5000/admin หรือคลิกที่ไอคอนรูปฟันเฟือง ⚙️ บริเวณมุมขวาบนของเมนูบาร์")
    r_u.font.bold = True
    r_u.font.color.rgb = RGBColor(74, 93, 76)

    doc.add_heading("4.2 แผงสรุปสถิติสำคัญ (KPIs Dashboard)", level=2)
    doc.add_paragraph("ด้านบนสุดของหน้าแอดมินแสดงการ์ดสรุปผล 4 หมวด ได้แก่:")
    kpi_list = [
        ("ยอดขายรวมทั้งหมด (Total Revenue):", "คำนวณจากผลรวมของออเดอร์ทั้งหมดในระบบแบบเรียลไทม์"),
        ("จำนวนคำสั่งซื้อทั้งหมด (Total Orders):", "นับจำนวนรายการออเดอร์ที่สั่งซื้อสำเร็จ"),
        ("รายการสินค้าในร้าน (Total Products):", "นับจำนวนสินค้าทั้งหมดที่วางจำหน่ายใน 3 หมวดหมู่"),
        ("สินค้าสต็อกน้อย (Low Stock Alert):", "แจ้งเตือนจำนวนสินค้าที่มีสต็อกคงเหลือ 15 ชิ้นลงไป เพื่อให้แอดมินเตรียมเติมของ")
    ]
    for k, v in kpi_list:
        p = doc.add_paragraph()
        p.paragraph_format.space_after = Pt(3)
        p.paragraph_format.left_indent = Inches(0.2)
        r = p.add_run(f"• {k} ")
        r.font.bold = True
        p.add_run(v)

    doc.add_heading("4.3 การจัดการคำสั่งซื้อ (Orders Management)", level=2)
    doc.add_paragraph(
        "ตารางแสดงรายการคำสั่งซื้อล่าสุด เรียงลำดับจากใหม่ไปเก่า แสดงเลขที่ออเดอร์, ชื่อลูกค้า, เบอร์โทร, "
        "ยอดเงินสุทธิ, วิธีชำระเงิน, สถานะ และวันที่สั่งซื้อ\n"
        "• ผู้ดูแลระบบสามารถเปลี่ยนสถานะออเดอร์ได้จากเมนูดรอปดาวน์: 'ชำระแล้ว' ➔ 'กำลังจัดส่ง' ➔ 'เสร็จสมบูรณ์' แล้วกดปุ่ม 'บันทึก'\n"
        "• สามารถคลิกที่เลขที่ออเดอร์เพื่อเปิดดูใบเสร็จรับเงินฉบับเต็มได้ทันที"
    )

    doc.add_heading("4.4 การจัดการสินค้าในคลังและการเพิ่มสินค้าใหม่ (Product Inventory)", level=2)
    doc.add_paragraph(
        "• ตรวจสอบสต็อก: ตารางแสดงรูปภาพสินค้า ชื่อ หมวดหมู่ ราคาขาย และจำนวนสต็อกคงเหลือ โดยสินค้าสต็อกต่ำจะมีป้ายเตือนสีแดง\n"
        "• การลบสินค้า: มีปุ่ม 'ลบ' สีแดงพร้อมระบบแจ้งเตือนยืนยัน (Confirmation Alert) ก่อนลบออกจากฐานข้อมูลจริง\n"
        "• การเพิ่มสินค้าใหม่: กดปุ่ม '+ เพิ่มสินค้าใหม่เข้าร้าน' ที่มุมขวาบน จะมีหน้าต่างโมดอลป๊อปอัปขึ้นมาให้กรอกข้อมูล:"
    )

    add_fields = [
        "ชื่อสินค้าภาษาไทย และ ชื่อภาษาอังกฤษ",
        "หมวดหมู่หลัก (สกินแคร์ / เครื่องสำอาง / อุปกรณ์บิวตี้) และหมวดหมู่ย่อย",
        "ราคาขาย (บาท) และราคาเดิมก่อนลด",
        "จำนวนสต็อกตั้งต้น และขนาด/ปริมาณ",
        "URL รูปภาพสินค้า (รองรับภาพความละเอียดสูงจาก Unsplash หรือไฟล์ในเครื่อง)",
        "ส่วนผสมสำคัญ (Key Ingredients), คำอธิบายสรรพคุณ และวิธีใช้งาน",
        "ตัวเลือกติ๊กถูก: สินค้าขายดี (Best Seller) และ แสดงในหน้าแรก (Featured)"
    ]
    for f in add_fields:
        p = doc.add_paragraph(f"   - {f}")
        p.paragraph_format.space_after = Pt(2)

    doc.add_page_break()

    # ========================================================
    # CHAPTER 5: DATABASE DICTIONARY
    # ========================================================
    h5 = doc.add_heading("บทที่ 5: พจนานุกรมข้อมูลและโครงสร้างฐานข้อมูล (Data Dictionary)", level=1)
    h5.paragraph_format.space_after = Pt(10)
    for r in h5.runs:
        r.font.name = 'Cordia New'
        r.font.size = Pt(18)
        r.font.bold = True
        r.font.color.rgb = RGBColor(47, 62, 49)

    doc.add_paragraph(
        "ฐานข้อมูลของระบบจัดเก็บในไฟล์ SQLite ชื่อ 'pure_olive.db' ประกอบด้วย 3 ตารางหลัก "
        "ซึ่งมีความสัมพันธ์และการจัดเก็บข้อมูลดังตารางต่อไปนี้:"
    )

    # Products Table
    doc.add_heading("5.1 ตาราง products (ตารางสินค้า)", level=2)
    p_tbl = doc.add_table(rows=10, cols=4)
    p_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    p_headers = ["ชื่อฟิลด์ (Field)", "ประเภท (Type)", "คีย์ (Key)", "คำอธิบาย"]
    p_rows = [
        ["id", "INTEGER", "PRIMARY KEY", "รหัสประจำตัวสินค้า (Auto Increment)"],
        ["name / name_en", "TEXT", "-", "ชื่อสินค้าภาษาไทย และภาษาอังกฤษ"],
        ["category", "TEXT", "-", "หมวดหมู่หลัก ('skincare', 'cosmetics', 'tools')"],
        ["subcategory", "TEXT", "-", "หมวดหมู่ย่อย (เช่น 'serum', 'cream', 'lip', 'tool')"],
        ["price / original_price", "REAL", "-", "ราคาขายปัจจุบัน และราคาตั้งต้นก่อนลด"],
        ["stock", "INTEGER", "-", "จำนวนสินค้าคงเหลือในคลัง"],
        ["skin_types / concerns", "TEXT", "-", "เงื่อนไขประเภทผิวและปัญหาผิวที่เหมาะสม (คั่นด้วยจุลภาค)"],
        ["key_ingredients", "TEXT", "-", "ส่วนผสมพฤกษศาสตร์สำคัญ"],
        ["is_bestseller / featured", "INTEGER", "-", "แฟล็กระบุสินค้าขายดี (1) และสินค้าแนะนำหน้าแรก (1)"]
    ]
    for c_idx, h_text in enumerate(p_headers):
        cell = p_tbl.cell(0, c_idx)
        cell.paragraphs[0].text = h_text
        cell.paragraphs[0].runs[0].font.bold = True
        set_cell_background(cell, "EBF0E9")
        set_cell_margins(cell, 80, 80, 100, 100)

    for r_idx, row_data in enumerate(p_rows, start=1):
        for c_idx, val in enumerate(row_data):
            cell = p_tbl.cell(r_idx, c_idx)
            cell.paragraphs[0].text = val
            set_cell_margins(cell, 50, 50, 100, 100)

    doc.add_paragraph().paragraph_format.space_after = Pt(12)

    # Orders Table
    doc.add_heading("5.2 ตาราง orders (ตารางคำสั่งซื้อ)", level=2)
    o_tbl = doc.add_table(rows=8, cols=4)
    o_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    o_rows = [
        ["id", "INTEGER", "PRIMARY KEY", "รหัสคำสั่งซื้อ (Auto Increment)"],
        ["order_number", "TEXT", "UNIQUE", "เลขที่คำสั่งซื้อทางการ (เช่น 'PO-20261110-XXXX')"],
        ["customer_name / phone", "TEXT", "-", "ชื่อผู้รับ และหมายเลขโทรศัพท์ติดต่อ"],
        ["customer_address", "TEXT", "-", "ที่อยู่จัดส่งพัสดุโดยละเอียด"],
        ["items_json", "TEXT", "-", "รายการสินค้า จำนวน และราคาในรูปแบบ JSON Array"],
        ["subtotal / discount / total", "REAL", "-", "ยอดรวม ส่วนลดจากคูปอง และยอดสุทธิที่ต้องชำระ"],
        ["payment_method / status", "TEXT", "-", "วิธีชำระ ('promptpay', 'cod') และสถานะ ('paid', 'shipping')"]
    ]
    for c_idx, h_text in enumerate(p_headers):
        cell = o_tbl.cell(0, c_idx)
        cell.paragraphs[0].text = h_text
        cell.paragraphs[0].runs[0].font.bold = True
        set_cell_background(cell, "EBF0E9")
        set_cell_margins(cell, 80, 80, 100, 100)

    for r_idx, row_data in enumerate(o_rows, start=1):
        for c_idx, val in enumerate(row_data):
            cell = o_tbl.cell(r_idx, c_idx)
            cell.paragraphs[0].text = val
            set_cell_margins(cell, 50, 50, 100, 100)

    doc.add_paragraph().paragraph_format.space_after = Pt(12)

    # Reviews Table
    doc.add_heading("5.3 ตาราง reviews (ตารางรีวิวสินค้า)", level=2)
    r_tbl = doc.add_table(rows=6, cols=4)
    r_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    r_rows = [
        ["id", "INTEGER", "PRIMARY KEY", "รหัสรีวิว"],
        ["product_id", "INTEGER", "FOREIGN KEY", "รหัสสินค้าที่อ้างอิงถึง products(id)"],
        ["reviewer_name", "TEXT", "-", "ชื่อลูกค้าผู้รีวิว"],
        ["skin_type", "TEXT", "-", "สภาพผิวของผู้รีวิว (เช่น 'ผิวผสม แพ้ง่าย')"],
        ["rating / comment", "INTEGER / TEXT", "-", "คะแนนดาว (1-5) และข้อความรีวิวผลลัพธ์"]
    ]
    for c_idx, h_text in enumerate(p_headers):
        cell = r_tbl.cell(0, c_idx)
        cell.paragraphs[0].text = h_text
        cell.paragraphs[0].runs[0].font.bold = True
        set_cell_background(cell, "EBF0E9")
        set_cell_margins(cell, 80, 80, 100, 100)

    for r_idx, row_data in enumerate(r_rows, start=1):
        for c_idx, val in enumerate(row_data):
            cell = r_tbl.cell(r_idx, c_idx)
            cell.paragraphs[0].text = val
            set_cell_margins(cell, 50, 50, 100, 100)

    doc.add_page_break()

    # ========================================================
    # CHAPTER 6: SETUP & EXECUTION
    # ========================================================
    h6 = doc.add_heading("บทที่ 6: ขั้นตอนการติดตั้งและรันโปรแกรม (Setup & Execution Guide)", level=1)
    h6.paragraph_format.space_after = Pt(10)
    for r in h6.runs:
        r.font.name = 'Cordia New'
        r.font.size = Pt(18)
        r.font.bold = True
        r.font.color.rgb = RGBColor(47, 62, 49)

    doc.add_paragraph("เพื่อให้การนำเสนอผลงานราบรื่น สามารถทำตามขั้นตอนการรันโปรเจกต์ได้ดังนี้:")

    steps_detail = [
        ("ขั้นตอนที่ 1: เตรียมสภาพแวดล้อม Python",
         "ตรวจสอบว่าเครื่องคอมพิวเตอร์ติดตั้ง Python 3.8 ขึ้นไป (แนะนำ Python 3.10 - 3.14)\n"
         "เปิดโปรแกรม PowerShell หรือ Command Prompt"),

        ("ขั้นตอนที่ 2: ติดตั้งโมดูลเสริมที่จำเป็น",
         "พิมพ์คำสั่งเพื่อติดตั้งแพ็กเกจ Flask และ python-docx:\n"
         "pip install flask python-docx"),

        ("ขั้นตอนที่ 3: ไปยังโฟลเดอร์โปรเจกต์",
         "cd C:\\075"),

        ("ขั้นตอนที่ 4: สั่งเริ่มต้นเซิร์ฟเวอร์",
         "python app.py\n"
         "ระบบจะแสดงข้อความ: [SERVER] PURE & OLIVE Server starting on http://127.0.0.1:5000"),

        ("ขั้นตอนที่ 5: เปิดเข้าชมในเว็บเบราว์เซอร์",
         "เปิด Google Chrome หรือ Microsoft Edge แล้วไปที่ URL:\n"
         "• หน้าร้านค้าสำหรับลูกค้า: http://127.0.0.1:5000\n"
         "• หน้าวิเคราะห์สภาพผิว: http://127.0.0.1:5000/routine-quiz\n"
         "• หน้าแอดมินจัดการหลังบ้าน: http://127.0.0.1:5000/admin"),

        ("ขั้นตอนที่ 6: การทดสอบความถูกต้องของระบบอัตโนมัติ (Automated Testing)",
         "ในโฟลเดอร์มีไฟล์ verify_app.py สำหรับรันเทสต์ทุก Route และ API แบบอัตโนมัติ สั่งรันด้วย:\n"
         "python verify_app.py")
    ]

    for title, desc in steps_detail:
        sub = doc.add_heading(title, level=2)
        sub.paragraph_format.space_after = Pt(2)
        p = doc.add_paragraph(desc)
        p.paragraph_format.space_after = Pt(8)
        p.paragraph_format.left_indent = Inches(0.2)

    doc.add_page_break()

    # ========================================================
    # APPENDIX: TEST CASES & DEMO DATA
    # ========================================================
    h_app = doc.add_heading("ภาคผนวก: ข้อมูลทดสอบระบบ (Test Cases & Demo Data)", level=1)
    h_app.paragraph_format.space_after = Pt(10)
    for r in h_app.runs:
        r.font.name = 'Cordia New'
        r.font.size = Pt(18)
        r.font.bold = True
        r.font.color.rgb = RGBColor(47, 62, 49)

    doc.add_paragraph("ข้อมูลสำหรับนำไปใช้สาธิต (Demonstration) ต่อหน้าอาจารย์หรือคณะกรรมการ:")

    doc.add_heading("1. โค้ดส่วนลดที่ใช้งานได้จริงในระบบ", level=2)
    coupon_table = doc.add_table(rows=4, cols=3)
    coupon_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    c_headers = ["รหัสโค้ด (Code)", "สิทธิประโยชน์", "เงื่อนไขการใช้งาน"]
    c_rows = [
        ["CLEAN10", "ส่วนลด 10% ทันที", "ใช้ได้กับสินค้าทุกชิ้นในตะกร้า ไม่มีขั้นต่ำ"],
        ["OLIVE50", "ส่วนลด 50 บาท", "ยอดสั่งซื้อขั้นต่ำ 300 บาทขึ้นไป"],
        ["ROUTINE15", "ส่วนลดพิเศษ 15%", "สำหรับสั่งซื้อเซตสกินแคร์จากการทำ Skin Quiz"]
    ]
    for c_idx, h_text in enumerate(c_headers):
        cell = coupon_table.cell(0, c_idx)
        cell.paragraphs[0].text = h_text
        cell.paragraphs[0].runs[0].font.bold = True
        set_cell_background(cell, "EBF0E9")
        set_cell_margins(cell, 80, 80, 100, 100)

    for r_idx, row_data in enumerate(c_rows, start=1):
        for c_idx, val in enumerate(row_data):
            cell = coupon_table.cell(r_idx, c_idx)
            cell.paragraphs[0].text = val
            set_cell_margins(cell, 60, 60, 100, 100)

    doc.add_paragraph().paragraph_format.space_after = Pt(12)

    doc.add_heading("2. ตัวอย่างข้อมูลทดสอบสั่งซื้อ (Test Scenario)", level=2)
    doc.add_paragraph(
        "• ชื่อผู้รับ: คุณณัฐวุฒิ สิทธิสมบูรณ์\n"
        "• เบอร์โทรศัพท์: 089-123-4567\n"
        "• อีเมล: natthawut@example.com\n"
        "• ที่อยู่จัดส่ง: 75/12 ถนนสุขุมวิท ซอย 21 แขวงคลองเตยเหนือ เขตวัฒนา กรุงเทพฯ 10110\n"
        "• วิธีชำระเงิน: PromptPay QR (ระบบจะสร้างหมายเลขออเดอร์ PO-20261110-XXXX และ QR Code จำลองทันที)"
    )

    add_callout_box(
        doc,
        "สรุปภาพรวมความพร้อมของโครงการ",
        "โครงการ PURE & OLIVE พัฒนาเสร็จสมบูรณ์ 100% มีไฟล์ฐานข้อมูล ข้อมูลสินค้า โค้ดโปรแกรม "
        "และเอกสารคู่มือการใช้งานเล่มนี้ครบถ้วน พร้อมส่งตรวจและประเมินผลการเรียนรู้ในระดับดีเยี่ยม"
    )

    # Save to both file names
    path1 = os.path.join(os.path.dirname(os.path.abspath(__file__)), "User_Manual_PURE_AND_OLIVE.docx")
    path2 = os.path.join(os.path.dirname(os.path.abspath(__file__)), "คู่มือการใช้งาน_PURE_AND_OLIVE.docx")
    doc.save(path1)
    doc.save(path2)
    print(f"Manual created successfully:\n  -> {path1}\n  -> {path2}")

if __name__ == '__main__':
    create_manual()
