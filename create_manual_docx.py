"""
Script to generate the User Manual & Project Report in DOCX format
PURE & OLIVE - Clean Beauty E-Commerce Platform
"""
import os
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml, OxmlElement
from docx.oxml.ns import nsdecls, qn

def set_cell_background(cell, fill_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    tcPr.append(parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>'))

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        node = OxmlElement(f'w:{m}')
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def generate_report():
    doc = Document()

    # Page Margins
    for section in doc.sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)

    # Styles
    style_normal = doc.styles['Normal']
    font = style_normal.font
    font.name = 'Cordia New'
    font.size = Pt(14)
    font.color.rgb = RGBColor(40, 48, 40)

    # ------------------ COVER PAGE ------------------ #
    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_title.paragraph_format.space_before = Pt(80)
    p_title.paragraph_format.space_after = Pt(10)
    run_title = p_title.add_run("รายงานโครงการพัฒนาระบบพาณิชย์อิเล็กทรอนิกส์\n(E-Commerce Web Application Project)")
    run_title.font.size = Pt(24)
    run_title.font.bold = True
    run_title.font.color.rgb = RGBColor(47, 62, 49)

    p_sub = doc.add_paragraph()
    p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_sub.paragraph_format.space_after = Pt(40)
    run_sub = p_sub.add_run("ระบบร้านค้าออนไลน์สกินแคร์ เครื่องสำอางคลีนบิวตี้ และอุปกรณ์เสริมความงาม\n« PURE & OLIVE — Minimal & Clean Beauty »")
    run_sub.font.size = Pt(18)
    run_sub.font.bold = True
    run_sub.font.color.rgb = RGBColor(74, 93, 76)

    p_meta = doc.add_paragraph()
    p_meta.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_meta.paragraph_format.space_before = Pt(120)
    p_meta.paragraph_format.line_spacing = 1.3
    run_meta = p_meta.add_run("จัดทำโดย\nนักศึกษา รหัสประจำตัว 075\n\nเสนอ\nอาจารย์ประจำรายวิชาการพัฒนาเว็บแอปพลิเคชันและพาณิชย์อิเล็กทรอนิกส์\nภาคการศึกษาที่ 2 ประจำปีการศึกษา 2569")
    run_meta.font.size = Pt(15)

    doc.add_page_break()

    # ------------------ CHAPTER 1 ------------------ #
    h1 = doc.add_heading("1. บทนำและแนวคิดโครงการ (Project Overview)", level=1)
    h1.paragraph_format.space_after = Pt(12)
    for r in h1.runs:
        r.font.size = Pt(18)
        r.font.color.rgb = RGBColor(47, 62, 49)

    p = doc.add_paragraph(
        "โครงการ PURE & OLIVE (เพียว แอนด์ โอลีฟ) มีวัตถุประสงค์เพื่อพัฒนาระบบร้านค้าออนไลน์จำหน่ายผลิตภัณฑ์สกินแคร์ "
        "ครีมบำรุงผิว เครื่องสำอางคลีนบิวตี้ และอุปกรณ์เสริมความงาม โดยเน้นการออกแบบสไตล์ มินิมอล คลีน (Minimalist & Clean Beauty) "
        "ที่ให้ความรู้สึกเรียบง่าย อบอุ่น และน่าเชื่อถือ ใช้ชุดโทนสีขาวและเขียวโอลีฟธรรมชาติ (Olive Green) ผสานกับเขียวเซจ (Sage Green) "
        "ซึ่งสะท้อนถึงผลิตภัณฑ์ออร์แกนิกที่อ่อนโยนต่อผิวบอบบางแพ้ง่าย ปราศจากสารระคายเคือง (100% Vegan & Cruelty-Free)"
    )
    p.paragraph_format.space_after = Pt(14)
    p.paragraph_format.line_spacing = 1.25

    # Objectives Bullet
    doc.add_heading("1.1 วัตถุประสงค์ของโครงการ", level=2)
    bullets = [
        "เพื่อสร้างเว็บไซต์ร้านค้าออนไลน์แบบ Full-Stack ด้วย Python (Flask) และฐานข้อมูล SQLite ที่ทำงานได้ครบวงจร",
        "เพื่อพัฒนาระบบแบบทดสอบวิเคราะห์สภาพผิวอัจฉริยะ (Skin Quiz & Routine Builder) ที่สามารถจัดเซตผลิตภัณฑ์เช้า-เย็นเฉพาะบุคคลได้อัตโนมัติ",
        "เพื่อสร้างระบบแคตตาล็อกสินค้าที่รองรับการกรองตาม 'ปัญหาผิว' (Skin Concern) และค้นหาตามส่วนผสมสำคัญ (Key Ingredients)",
        "เพื่อสร้างระบบตะกร้าสินค้า คูปองส่วนลด การจำลองการชำระเงินด้วย PromptPay QR Code และการออกใบเสร็จรับเงิน",
        "เพื่อพัฒนาระบบจัดการหลังบ้าน (Admin Dashboard) สำหรับตรวจสอบยอดขาย รายการออเดอร์ และควบคุมสต็อกสินค้า"
    ]
    for b in bullets:
        bp = doc.add_paragraph(f"• {b}")
        bp.paragraph_format.space_after = Pt(6)
        bp.paragraph_format.left_indent = Inches(0.25)

    doc.add_paragraph().paragraph_format.space_after = Pt(10)

    # ------------------ CHAPTER 2 ------------------ #
    h2 = doc.add_heading("2. โครงสร้างระบบและเทคโนโลยีที่ใช้ (System Architecture)", level=1)
    h2.paragraph_format.space_after = Pt(12)
    for r in h2.runs:
        r.font.size = Pt(18)
        r.font.color.rgb = RGBColor(47, 62, 49)

    tech_table = doc.add_table(rows=6, cols=3)
    tech_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    headers = ["ส่วนงาน (Layer)", "เทคโนโลยีที่ใช้", "รายละเอียดการทำงาน"]
    tech_data = [
        ["Backend Server", "Python 3.14 + Flask 3.1", "ประมวลผลคำสั่ง ควบคุมการทำงานของ Routing และ REST API"],
        ["Database", "SQLite 3", "จัดเก็บข้อมูลสินค้า (Products) คำสั่งซื้อ (Orders) และรีวิว (Reviews)"],
        ["Frontend UI", "HTML5 + Modern CSS3", "ออกแบบด้วยแนวคิด Responsive Web Design โทนสีเขียวโอลีฟ"],
        ["Client Interaction", "Vanilla JavaScript (ES6+)", "ระบบตะกร้าสินค้า LocalStorage, Cart Drawer, Animation, Toast"],
        ["Diagnostic Engine", "JSON REST API", "ระบบจับคู่สกินแคร์รูทีนจากเงื่อนไขสภาพผิวของผู้ใช้"]
    ]

    for col_idx, text in enumerate(headers):
        cell = tech_table.cell(0, col_idx)
        cell.paragraphs[0].text = text
        cell.paragraphs[0].runs[0].font.bold = True
        cell.paragraphs[0].runs[0].font.size = Pt(13)
        cell.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
        set_cell_background(cell, "EBF0E9")
        set_cell_margins(cell, 120, 120, 140, 140)

    for row_idx, row in enumerate(tech_data, start=1):
        for col_idx, text in enumerate(row):
            cell = tech_table.cell(row_idx, col_idx)
            cell.paragraphs[0].text = text
            cell.paragraphs[0].runs[0].font.size = Pt(12)
            set_cell_margins(cell, 80, 80, 120, 120)

    doc.add_paragraph().paragraph_format.space_after = Pt(16)

    # ------------------ CHAPTER 3 ------------------ #
    h3 = doc.add_heading("3. ฟังก์ชันการทำงานหลักของเว็บไซต์ (Core Features)", level=1)
    h3.paragraph_format.space_after = Pt(12)
    for r in h3.runs:
        r.font.size = Pt(18)
        r.font.color.rgb = RGBColor(47, 62, 49)

    features = [
        ("3.1 หน้าแรกและเอกลักษณ์แบรนด์ (Homepage & Philosophy)",
         "นำเสนอแบนเนอร์หลักพร้อมสโลแกน จุดเด่นด้านความปลอดภัย (Dermatologist Tested), ค่านิยม 100% Clean, Vegan & Cruelty-Free, "
         "หมวดหมู่สินค้าหลัก 3 หมวด (สกินแคร์, เครื่องสำอาง, อุปกรณ์บิวตี้), สินค้าขายดีประจำร้าน, ปรัชญาส่วนผสมสำคัญจากผลมะกอก "
         "และรีวิวจากผู้ใช้จริงที่ระบุสภาพผิวชัดเจน"),

        ("3.2 แคตตาล็อกและการกรองสินค้าอัจฉริยะ (Catalog & Skin Concern Filters)",
         "แสดงรายการสินค้าทั้งหมด 17 รายการ รองรับการค้นหาแบบข้อความ (Search) ทั้งชื่อและส่วนผสม, ตัวกรองแยกตามประเภทสินค้า, "
         "ตัวกรองด่วนตามปัญหาผิว เช่น 'สิวและคุมมัน', 'ผิวแห้งขาดน้ำ', 'ฟื้นฟูเกราะป้องกันผิว', 'ชะลอวัย' และระบบเรียงลำดับราคา/คะแนนรีวิว"),

        ("3.3 ระบบแบบทดสอบวิเคราะห์สภาพผิว (Skin Quiz & Routine Builder)",
         "ฟีเจอร์เด่นระดับพรีเมียม ให้ผู้ใช้ตอบคำถาม 3 ขั้นตอน (สภาพผิว -> ปัญหาผิว -> สไตล์การดูแล) "
         "ระบบจะส่งข้อมูลไปยัง REST API เพื่อวิเคราะห์และจัดชุด 'Morning Routine' และ 'Night Routine' พร้อมคำอธิบายเชิงวิชาการ "
         "และมีปุ่มกด 'สั่งซื้อทั้งเซตแนะนำลงตะกร้าทันที' พร้อมรับส่วนลดเซต 15%"),

        ("3.4 หน้ารายละเอียดสินค้าและระบบรีวิว (Product Details & Reviews)",
         "แสดงข้อมูลส่วนผสมเด่น (Key Ingredients), วิธีการใช้งาน (How to Use), จำนวนสต็อก, ปริมาณ, ปุ่มปรับจำนวนสินค้า, "
         "ระบบรีวิวจากลูกค้าจริง พร้อมฟอร์มให้ผู้ใช้สามารถส่งรีวิว ให้คะแนนดาว และระบุสภาพผิวของตนเองได้จริง"),

        ("3.5 ระบบตะกร้าสินค้า คูปอง และชำระเงิน (Cart Drawer & Checkout Simulation)",
         "มี Cart Drawer ด้านข้างที่กดเปิด-ปิดได้จากทุกหน้า, แถบคำนวณส่งฟรีเมื่อช้อปครบ 990 บาท, "
         "ระบบกรอกโค้ดส่วนลด (เช่น CLEAN10 ลด 10%, OLIVE50 ลด 50 บาท), ฟอร์มกรอกที่อยู่จัดส่ง และระบบจำลองการชำระเงินด้วย PromptPay QR"),

        ("3.6 หน้าใบเสร็จรับเงินและการพิมพ์ (Official Order Receipt & Print View)",
         "แสดงรหัสคำสั่งซื้อ (Order Number), หมายเลขพัสดุ (Tracking Number), รายการสินค้า, QR Code ชำระเงินจำลอง, "
         "พร้อมปุ่มกดพิมพ์ใบเสร็จรับเงินที่จัดรูปแบบหน้ากระดาษแบบ Print-Friendly เหมาะสำหรับการพิมพ์หรือบันทึกเป็น PDF"),

        ("3.7 ระบบหลังบ้านสำหรับผู้ดูแลระบบ (Admin Dashboard)",
         "เข้าถึงได้ทาง URL: /admin แสดงสถิติยอดขายรวม, จำนวนคำสั่งซื้อ, สินค้าทั้งหมด และแจ้งเตือนสต็อกต่ำ, "
         "ตารางจัดการออเดอร์พร้อมฟังก์ชันอัปเดตสถานะจัดส่ง, ตารางตรวจสอบสต็อกสินค้า และฟอร์มเพิ่มสินค้าใหม่เข้าร้าน")
    ]

    for title, desc in features:
        sub_h = doc.add_heading(title, level=2)
        sub_h.paragraph_format.space_after = Pt(4)
        for r in sub_h.runs:
            r.font.size = Pt(14)
            r.font.color.rgb = RGBColor(74, 93, 76)
        p = doc.add_paragraph(desc)
        p.paragraph_format.space_after = Pt(10)
        p.paragraph_format.line_spacing = 1.25

    doc.add_page_break()

    # ------------------ CHAPTER 4 ------------------ #
    h4 = doc.add_heading("4. โครงสร้างฐานข้อมูล (Database Schema)", level=1)
    h4.paragraph_format.space_after = Pt(12)
    for r in h4.runs:
        r.font.size = Pt(18)
        r.font.color.rgb = RGBColor(47, 62, 49)

    doc.add_paragraph("ระบบใช้งานฐานข้อมูล SQLite (pure_olive.db) ประกอบด้วย 3 ตารางหลัก ดังนี้:")

    db_tables = [
        ("ตาราง products (จัดเก็บข้อมูลสินค้า)", [
            ("id", "INTEGER PRIMARY KEY", "รหัสประจำตัวสินค้า (Auto Increment)"),
            ("name / name_en", "TEXT", "ชื่อสินค้าภาษาไทย และ ภาษาอังกฤษ"),
            ("category / subcategory", "TEXT", "หมวดหมู่หลัก (skincare, cosmetics, tools) และหมวดหมู่ย่อย"),
            ("price / original_price", "REAL", "ราคาขายปัจจุบัน และราคาเดิมก่อนลด"),
            ("stock", "INTEGER", "จำนวนสินค้าคงเหลือในคลัง"),
            ("skin_types / skin_concerns", "TEXT", "สภาพผิวและปัญหาผิวที่เหมาะสม"),
            ("key_ingredients", "TEXT", "ส่วนผสมสำคัญ"),
            ("is_bestseller / is_featured", "INTEGER", "แฟล็กระบุสินค้าขายดี และสินค้าแนะนำหน้าแรก")
        ]),
        ("ตาราง orders (จัดเก็บข้อมูลคำสั่งซื้อ)", [
            ("id", "INTEGER PRIMARY KEY", "รหัสคำสั่งซื้อ"),
            ("order_number", "TEXT UNIQUE", "หมายเลขคำสั่งซื้อรูปแบบ PO-YYYYMMDD-XXXX"),
            ("customer_name / phone / address", "TEXT", "ข้อมูลชื่อ เบอร์โทร และที่อยู่จัดส่งของผู้รับ"),
            ("items_json", "TEXT", "รายการสินค้าและจำนวนที่สั่งซื้อในรูปแบบ JSON"),
            ("subtotal / discount / total_price", "REAL", "ยอดรวม ส่วนลด และยอดชำระสุทธิ"),
            ("payment_method / status", "TEXT", "วิธีชำระเงิน (promptpay, cod) และสถานะ (paid, shipping, completed)"),
            ("tracking_number", "TEXT", "หมายเลขติดตามพัสดุจำลอง")
        ]),
        ("ตาราง reviews (จัดเก็บรีวิวจากลูกค้า)", [
            ("id", "INTEGER PRIMARY KEY", "รหัสรีวิว"),
            ("product_id", "INTEGER", "รหัสสินค้าที่อ้างอิง"),
            ("reviewer_name / skin_type", "TEXT", "ชื่อผู้รีวิว และสภาพผิวของผู้รีวิว"),
            ("rating", "INTEGER", "คะแนนดาว (1 - 5 ดาว)"),
            ("comment", "TEXT", "ความคิดเห็นและผลลัพธ์หลังใช้งาน")
        ])
    ]

    for tbl_title, fields in db_tables:
        sub = doc.add_heading(tbl_title, level=2)
        sub.paragraph_format.space_after = Pt(4)
        t = doc.add_table(rows=len(fields)+1, cols=3)
        t.alignment = WD_TABLE_ALIGNMENT.CENTER
        
        # Header
        for c_idx, h_text in enumerate(["ชื่อฟิลด์ (Column)", "ประเภทข้อมูล (Data Type)", "คำอธิบาย"]):
            c = t.cell(0, c_idx)
            c.paragraphs[0].text = h_text
            c.paragraphs[0].runs[0].font.bold = True
            c.paragraphs[0].runs[0].font.size = Pt(12)
            set_cell_background(c, "EBF0E9")
            set_cell_margins(c, 80, 80, 100, 100)

        for r_idx, f in enumerate(fields, start=1):
            for c_idx, val in enumerate(f):
                c = t.cell(r_idx, c_idx)
                c.paragraphs[0].text = val
                c.paragraphs[0].runs[0].font.size = Pt(11)
                set_cell_margins(c, 60, 60, 100, 100)

        doc.add_paragraph().paragraph_format.space_after = Pt(10)

    # ------------------ CHAPTER 5 ------------------ #
    h5 = doc.add_heading("5. วิธีการติดตั้งและรันโปรเจกต์ (Installation Guide)", level=1)
    h5.paragraph_format.space_after = Pt(12)
    for r in h5.runs:
        r.font.size = Pt(18)
        r.font.color.rgb = RGBColor(47, 62, 49)

    steps = [
        "1. เปิดโปรแกรม Command Prompt, PowerShell หรือ Terminal",
        "2. ไปยังโฟลเดอร์โปรเจกต์: cd C:\\075",
        "3. ติดตั้งไลบรารีที่จำเป็น: python -m pip install flask python-docx",
        "4. เริ่มต้นเซิร์ฟเวอร์ด้วยคำสั่ง: python app.py",
        "5. เปิดเว็บเบราว์เซอร์ (Chrome, Edge หรือ Firefox) แล้วเข้าไปที่: http://127.0.0.1:5000",
        "6. หากต้องการเข้าสู่ระบบแอดมินหลังบ้าน ให้เข้าไปที่: http://127.0.0.1:5000/admin"
    ]
    for s in steps:
        p = doc.add_paragraph(s)
        p.paragraph_format.space_after = Pt(4)

    # Save
    out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "User_Manual_PURE_AND_OLIVE.docx")
    doc.save(out_path)
    print("User Manual DOCX created successfully at:", out_path)

if __name__ == '__main__':
    generate_report()
