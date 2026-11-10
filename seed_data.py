"""
PURE & OLIVE - Seed Data
Clean, Minimalist E-Commerce Platform
Curated products, reviews, and test data
"""
import sqlite3
from database import get_db_connection, init_db

PRODUCTS = [
    # --- SKINCARE & CREAMS ---
    {
        "name": "เจลล้างหน้าสูตรอ่อนโยน ใบบัวบกและชาเขียว",
        "name_en": "Centella & Green Tea Calming Cleanser",
        "brand": "PURE & OLIVE",
        "category": "skincare",
        "subcategory": "cleanser",
        "price": 390.0,
        "original_price": 490.0,
        "image_url": "https://images.unsplash.com/photo-1556228720-195a672e8a03?auto=format&fit=crop&w=800&q=80",
        "rating": 4.9,
        "reviews_count": 128,
        "stock": 35,
        "skin_types": "all,sensitive,oily,combination",
        "skin_concerns": "acne,soothing,barrier",
        "routine_step": "cleanser",
        "routine_time": "both",
        "key_ingredients": "Centella Asiatica, Green Tea Extract, Panthenol (B5)",
        "volume": "150 ml",
        "description": "เจลล้างหน้าสูตร pH สมดุล 5.5 ฟองโฟมนุ่มละมุน ล้างทำความสะอาดสิ่งสกปรกและมลภาวะได้อย่างล้ำลึกโดยไม่ทำลายเกราะป้องกันผิว ไม่แห้งตึง อุดมด้วยสารสกัดใบบัวบกออร์แกนิกและใบชาเขียวช่วยปลอบประโลมผิวเป็นสิวและผิวแพ้ง่าย",
        "how_to_use": "ปั๊มเจล 1-2 ปั๊มลงบนฝ่ามือที่เปียก ถูให้เกิดฟองนุ่ม นวดเบาๆ ทั่วใบหน้าเป็นวงกลม แล้วล้างออกด้วยน้ำสะอาด เช้า-เย็น",
        "is_bestseller": 1,
        "is_featured": 1
    },
    {
        "name": "โทนเนอร์ปรับสมดุลผิว สารสกัดใบมะกอกและฮาร์ทลีฟ",
        "name_en": "Olive Leaf & Heartleaf Balancing Toner",
        "brand": "PURE & OLIVE",
        "category": "skincare",
        "subcategory": "toner",
        "price": 450.0,
        "original_price": 550.0,
        "image_url": "https://images.unsplash.com/photo-1608248597359-58d56b060f64?auto=format&fit=crop&w=800&q=80",
        "rating": 4.8,
        "reviews_count": 94,
        "stock": 28,
        "skin_types": "all,oily,combination,sensitive",
        "skin_concerns": "acne,soothing,hydration",
        "routine_step": "toner",
        "routine_time": "both",
        "key_ingredients": "Olive Leaf Extract, Heartleaf 77%, Centella, Allantoin",
        "volume": "200 ml",
        "description": "โทนเนอร์เนื้อน้ำบางเบา ซึมซาบไว อุดมด้วยสารต้านอนุมูลอิสระจากใบมะกอกและ Heartleaf ช่วยลดรอยแดง ปลอบประโลมการระคายเคือง รูขุมขนแลดูกระชับ พร้อมปรับสมดุลน้ำและน้ำมันบนผิวให้พร้อมรับการบำรุง",
        "how_to_use": "หลังล้างหน้า เทโทนเนอร์ลงบนแผ่นสำลีหรือฝ่ามือ ตบเบาๆ ทั่วใบหน้าและลำคอ สามารถใช้เป็นมาสก์ชีทโดยชุบสำลีแปะทิ้งไว้ 5 นาที",
        "is_bestseller": 0,
        "is_featured": 1
    },
    {
        "name": "เซรั่มสควาเลนจากมะกอก & เซราไมด์ ฟื้นฟูเกราะป้องกันผิว",
        "name_en": "Pure Squalane & Ceramide Barrier Serum",
        "brand": "PURE & OLIVE",
        "category": "skincare",
        "subcategory": "serum",
        "price": 690.0,
        "original_price": 850.0,
        "image_url": "https://images.unsplash.com/photo-1620916566398-39f1143ab7be?auto=format&fit=crop&w=800&q=80",
        "rating": 5.0,
        "reviews_count": 210,
        "stock": 40,
        "skin_types": "all,dry,sensitive,combination",
        "skin_concerns": "barrier,hydration,soothing",
        "routine_step": "serum",
        "routine_time": "both",
        "key_ingredients": "100% Olive-derived Squalane, 5 Essential Ceramides, Cholesterol",
        "volume": "30 ml",
        "description": "เซรั่มไอเท็มดาวเด่น อัดแน่นด้วยสควาเลนบริสุทธิ์ 100% สกัดจากผลมะกอกออร์แกนิก ผสานเซราไมด์จำเป็น 5 ชนิด เสริมความแข็งแรงให้ผิวชั้นนอก ลดการสูญเสียน้ำ ฟื้นฟูผิวแพ้ง่าย ผิวแห้งลอกให้กลับมาเนียนนุ่ม สุขภาพดี ดูอิ่มฟู",
        "how_to_use": "ดรอปเซรั่ม 2-3 หยดลงบนฝ่ามือ วอร์มเบาๆ แล้วกดประคบทั่วใบหน้า เช้าและก่อนนอน เป็นประจำทุกวัน",
        "is_bestseller": 1,
        "is_featured": 1
    },
    {
        "name": "เซรั่มไนอะซินาไมด์ 10% + ซิงค์ พีซีเอ ลดรอยสิว คุมมัน",
        "name_en": "Botanical Niacinamide 10% + Zinc Glow Drops",
        "brand": "PURE & OLIVE",
        "category": "skincare",
        "subcategory": "serum",
        "price": 520.0,
        "original_price": 650.0,
        "image_url": "https://images.unsplash.com/photo-1601049541289-9b1b7bbbfe19?auto=format&fit=crop&w=800&q=80",
        "rating": 4.8,
        "reviews_count": 156,
        "stock": 25,
        "skin_types": "oily,combination,acne-prone",
        "skin_concerns": "acne,brightening,oil-control",
        "routine_step": "serum",
        "routine_time": "both",
        "key_ingredients": "Niacinamide 10%, Zinc PCA 1%, Willow Bark Extract",
        "volume": "30 ml",
        "description": "เซรั่มลดรอยดำ รอยแดงจากสิวอย่างอ่อนโยน ปรับโทนสีผิวให้เรียบเนียนสม่ำเสมอ ผสาน Zinc PCA ช่วยควบคุมความมันส่วนเกินโดยไม่ทำให้ผิวแห้งขาดน้ำ รูขุมขนแลดูกระชับ เนื้อเซรั่มสัมผัสบางเบา ไม่เหนียวเหนอะหนะ",
        "how_to_use": "ทาให้ทั่วใบหน้า 2-3 หยด เช้าและเย็น ก่อนลงมอยส์เจอไรเซอร์ หลีกเลี่ยงบริเวณรอบดวงตา",
        "is_bestseller": 1,
        "is_featured": 0
    },
    {
        "name": "มอยส์เจอไรเซอร์ครีมน้ำมันมะกอกสกัดเย็น กักเก็บความชุ่มชื้น",
        "name_en": "Olive Nourishing Barrier Recovery Cream",
        "brand": "PURE & OLIVE",
        "category": "skincare",
        "subcategory": "cream",
        "price": 590.0,
        "original_price": 720.0,
        "image_url": "https://images.unsplash.com/photo-1598440947619-2c35fc9aa908?auto=format&fit=crop&w=800&q=80",
        "rating": 4.9,
        "reviews_count": 182,
        "stock": 30,
        "skin_types": "dry,normal,sensitive",
        "skin_concerns": "hydration,barrier,aging",
        "routine_step": "moisturizer",
        "routine_time": "both",
        "key_ingredients": "Extra Virgin Olive Oil, Shea Butter, Oat Extract, Vitamin E",
        "volume": "50 ml",
        "description": "ครีมบำรุงเข้มข้นเนื้อละมุน ซึมลึกเคลือบผิวอย่างอ่อนโยน ด้วยคุณค่าจากน้ำมันมะกอกสกัดเย็นเกรดพรีเมียมและข้าวโอ๊ต ช่วยปลอบประโลมผิวแห้งกร้าน ล็อคความชุ่มชื้นยาวนาน 48 ชั่วโมง ผิวแลดูเปล่งปลั่ง นุ่มเด้ง ไม่มันเยิ้ม",
        "how_to_use": "แต้มเนื้อครีม 5 จุดทั่วใบหน้า ลูบไล้และนวดเบาๆ ให้เนื้อครีมซึมสู่ผิว ใช้เป็นขั้นตอนสุดท้ายก่อนนอน หรือก่อนทากันแดดในตอนเช้า",
        "is_bestseller": 1,
        "is_featured": 1
    },
    {
        "name": "เจลครีมซิก้า ปลอบประโลมผิวเป็นสิวและลดรอยแดง",
        "name_en": "Cica Soothing Moisture Gel Cream",
        "brand": "PURE & OLIVE",
        "category": "skincare",
        "subcategory": "cream",
        "price": 490.0,
        "original_price": 590.0,
        "image_url": "https://images.unsplash.com/photo-1570194065650-d99fb4bedf0a?auto=format&fit=crop&w=800&q=80",
        "rating": 4.7,
        "reviews_count": 88,
        "stock": 22,
        "skin_types": "oily,combination,sensitive",
        "skin_concerns": "acne,soothing,oil-control",
        "routine_step": "moisturizer",
        "routine_time": "both",
        "key_ingredients": "Centella Asiatica 73%, Tea Tree Water, Madecassoside",
        "volume": "60 ml",
        "description": "เจลครีมสูตรเย็นสบายผิว ปราศจากน้ำมัน (Oil-Free) ซึมเร็วเป็นพิเศษ ไม่ทิ้งความมัน ลดอาการแสบแดงจากการเผชิญแดดและลดสิวอักเสบ อุดมด้วย Madecassoside เข้มข้น ช่วยสมานผิวและลดโอกาสเกิดรอยสิวใหม่",
        "how_to_use": "ทาทั่วใบหน้าและลำคอหลังลงเซรั่ม ใช้ได้ทั้งเช้าและเย็น เหมาะสำหรับคนผิวมันและผิวเป็นสิวง่าย",
        "is_bestseller": 0,
        "is_featured": 0
    },
    {
        "name": "กันแดดมิเนอรัลบางเบาพิเศษ ป้องกันแสงสีฟ้า SPF50+ PA++++",
        "name_en": "Ultra-Light Invisible Mineral Sunscreen SPF50+ PA++++",
        "brand": "PURE & OLIVE",
        "category": "skincare",
        "subcategory": "sunscreen",
        "price": 620.0,
        "original_price": 750.0,
        "image_url": "https://images.unsplash.com/photo-1567928815104-b6973dbab38c?auto=format&fit=crop&w=800&q=80",
        "rating": 4.9,
        "reviews_count": 245,
        "stock": 45,
        "skin_types": "all,sensitive,acne-prone",
        "skin_concerns": "sun-protection,aging,brightening",
        "routine_step": "sunscreen",
        "routine_time": "morning",
        "key_ingredients": "Non-nano Zinc Oxide, Olive Leaf Extract, Niacinamide 2%",
        "volume": "50 ml",
        "description": "ครีมกันแดดเนื้อฟลูอิดมิเนอรัล 100% สัมผัสบางเบาดุจน้ำ ไม่เหนียว ไม่ทิ้งคราบขาว (Zero White Cast) ปลอดภัยต่อปะการังและสิ่งแวดล้อม ปกป้องผิวครบทั้ง UVA/UVB แสงสีฟ้า (Blue Light) และมลภาวะ PM 2.5 อ่อนโยนแม้ผิวทารกหรือผิวหลังทำเลเซอร์",
        "how_to_use": "เขย่าขวดก่อนใช้ ทาทั่วใบหน้าและลำคอเป็นขั้นตอนสุดท้ายของการบำรุงผิวก่อนออกแดด 15 นาที",
        "is_bestseller": 1,
        "is_featured": 1
    },
    {
        "name": "ออยล์บำรุงผิวยามค่ำคืน บาคูชิออล 1% ทางเลือกเรตินอล",
        "name_en": "Bakuchiol Youth Restoring Night Oil",
        "brand": "PURE & OLIVE",
        "category": "skincare",
        "subcategory": "serum",
        "price": 750.0,
        "original_price": 920.0,
        "image_url": "https://images.unsplash.com/photo-1608248543803-ba4f8c70ae0b?auto=format&fit=crop&w=800&q=80",
        "rating": 4.9,
        "reviews_count": 76,
        "stock": 18,
        "skin_types": "all,dry,sensitive",
        "skin_concerns": "aging,firming,hydration",
        "routine_step": "serum",
        "routine_time": "night",
        "key_ingredients": "Natural Bakuchiol 1%, Cold-pressed Olive Oil, Rosehip Seed Oil",
        "volume": "30 ml",
        "description": "ออยล์บำรุงผิวสูตรเรตินอลจากพืชธรรมชาติ (Natural Retinol Alternative) ที่อ่อนโยน ไม่ก่อให้เกิดการระคายเคืองหรือผิวลอก ช่วยลดเลือนริ้วรอยแรกเริ่ม เสริมคอลลาเจนใต้ผิว และเพิ่มความยืดหยุ่นให้ผิวดูกระชับเรียบเนียน ตื่นมาพร้อมผิวเปล่งประกายอ่อนเยาว์",
        "how_to_use": "หยด 2-3 หยดลงบนฝ่ามือ ลูบไล้ทั่วใบหน้าและลำคอในขั้นตอนสุดท้ายก่อนนอนเป็นประจำ",
        "is_bestseller": 0,
        "is_featured": 1
    },

    # --- CLEAN COSMETICS & MAKEUP ---
    {
        "name": "คุชชั่นเซรั่มงานผิวธรรมชาติ ดิวอี้โกลว์ SPF35 PA+++",
        "name_en": "Dewy Olive Glow Serum Cushion SPF35 PA+++",
        "brand": "PURE & OLIVE",
        "category": "cosmetics",
        "subcategory": "cushion",
        "price": 690.0,
        "original_price": 820.0,
        "image_url": "https://images.unsplash.com/photo-1522337360788-8b13dee7a37e?auto=format&fit=crop&w=800&q=80",
        "rating": 4.8,
        "reviews_count": 134,
        "stock": 25,
        "skin_types": "all,dry,combination",
        "skin_concerns": "makeup,hydration,glow",
        "routine_step": "makeup",
        "routine_time": "morning",
        "key_ingredients": "Olive Squalane, Hyaluronic Acid, Centella, Mineral Pigments",
        "volume": "15 g (แถมรีฟิล 1 ชิ้น)",
        "description": "คุชชั่นเซรั่มที่ผสานการบำรุงผิวในขั้นตอนเดียว ให้งานผิวธรรมชาติสไตล์ 'Clean Girl' เรียบเนียน ฉ่ำโกลว์อย่างเป็นธรรมชาติ ไม่หนักหน้า เบลอรูขุมขนและรอยสิวได้อย่างแนบเนียน ติดทนยาวนาน 12 ชม. ไม่อุดตันรูขุมขน",
        "how_to_use": "ใช้พัฟฟ์แตะเนื้อคุชชั่นเบาๆ แล้วกดซับให้ทั่วใบหน้า สามารถแตะซ้ำในบริเวณที่ต้องการปกปิดเพิ่ม",
        "is_bestseller": 1,
        "is_featured": 1
    },
    {
        "name": "ลิปแอนด์ชีคบัตเตอร์ออร์แกนิก สี 01 Terracotta Nude",
        "name_en": "Clean Tinted Lip & Cheek Butter - 01 Terracotta Nude",
        "brand": "PURE & OLIVE",
        "category": "cosmetics",
        "subcategory": "lip",
        "price": 350.0,
        "original_price": 420.0,
        "image_url": "https://images.unsplash.com/photo-1586495777744-4413f21062fa?auto=format&fit=crop&w=800&q=80",
        "rating": 4.9,
        "reviews_count": 198,
        "stock": 40,
        "skin_types": "all",
        "skin_concerns": "makeup,hydration",
        "routine_step": "makeup",
        "routine_time": "both",
        "key_ingredients": "Organic Olive Butter, Jojoba Oil, Vitamin E, Plant Wax",
        "volume": "4.5 g",
        "description": "ลิปบาล์มมีสีเนื้อบัตเตอร์ละมุน ใช้ได้ทั้งริมฝีปากและพวงแก้ม สี 01 ส้มอิฐนู้ดละมุน ให้ลุคอบอุ่น สุขภาพดี ชุ่มชื้นยาวนานด้วยเนยน้ำมันมะกอกออร์แกนิก ปราศจากน้ำหอมสังเคราะห์และพาราเบน ไม่ทำให้ปากคล้ำเสีย",
        "how_to_use": "ทาบำรุงริมฝีปากได้บ่อยตามต้องการ หรือแต้มบางๆ บริเวณโหนกแก้มแล้วใช้นิ้วเกลี่ยให้ระเรื่อ",
        "is_bestseller": 1,
        "is_featured": 1
    },
    {
        "name": "ลิปแอนด์ชีคบัตเตอร์ออร์แกนิก สี 02 Rosewood Glow",
        "name_en": "Clean Tinted Lip & Cheek Butter - 02 Rosewood Glow",
        "brand": "PURE & OLIVE",
        "category": "cosmetics",
        "subcategory": "lip",
        "price": 350.0,
        "original_price": 420.0,
        "image_url": "https://images.unsplash.com/photo-1625093742435-6fa192b6fb10?auto=format&fit=crop&w=800&q=80",
        "rating": 4.9,
        "reviews_count": 165,
        "stock": 35,
        "skin_types": "all",
        "skin_concerns": "makeup,hydration",
        "routine_step": "makeup",
        "routine_time": "both",
        "key_ingredients": "Organic Olive Butter, Rosehip Oil, Natural Mica",
        "volume": "4.5 g",
        "description": "ลิปบาล์มมีสีสูตรคลีน สี 02 ชมพูกุหลาบตุ่นธรรมชาติ เกลี่ยง่าย กลมกลืนกับทุกสีผิว ให้ริมฝีปากดูอวบอิ่มชุ่มชื้นสุขภาพดี ดุจดื่มน้ำวันละ 8 แก้ว",
        "how_to_use": "ทาริมฝีปากและแต้มบริเวณพวงแก้มเพื่อเพิ่มสีสันสดใสอย่างเป็นธรรมชาติ",
        "is_bestseller": 0,
        "is_featured": 0
    },
    {
        "name": "บลัชออนเนื้อครีมละมุนแก้มใส สารสกัดจากผลมะกอก",
        "name_en": "Dewy Olive Cream Blush - Peachy Coral",
        "brand": "PURE & OLIVE",
        "category": "cosmetics",
        "subcategory": "blush",
        "price": 390.0,
        "original_price": 490.0,
        "image_url": "https://images.unsplash.com/photo-1596462502278-27bfdc403348?auto=format&fit=crop&w=800&q=80",
        "rating": 4.7,
        "reviews_count": 92,
        "stock": 20,
        "skin_types": "all",
        "skin_concerns": "makeup,glow",
        "routine_step": "makeup",
        "routine_time": "morning",
        "key_ingredients": "Olive Oil Ester, Candelilla Wax, Camellia Oil",
        "volume": "6 g",
        "description": "บลัชออนเนื้อครีมเนียนนุ่ม สัมผัสบางเบา เกลี่ยง่ายไม่เป็นคราบแม้ทาทับแป้ง สีพีชคอรัลระเรื่อดูเป็นธรรมชาติเหมือนมีเลือดฝาด ติดทนนานตลอดวัน ไม่อุดตันผิว",
        "how_to_use": "ใช้นิ้วหรือฟองน้ำแตะเนื้อบลัชเล็กน้อย แล้วเกลี่ยเบาๆ บนพวงแก้ม",
        "is_bestseller": 0,
        "is_featured": 0
    },
    {
        "name": "แป้งฝุ่นโปร่งแสงสารสกัดจากข้าวออร์แกนิก ล็อกเมคอัพคุมมัน",
        "name_en": "Silk Veil Translucent Rice Setting Powder",
        "brand": "PURE & OLIVE",
        "category": "cosmetics",
        "subcategory": "powder",
        "price": 450.0,
        "original_price": 550.0,
        "image_url": "https://images.unsplash.com/photo-1599305090598-fe179d501227?auto=format&fit=crop&w=800&q=80",
        "rating": 4.8,
        "reviews_count": 140,
        "stock": 30,
        "skin_types": "all,oily,combination",
        "skin_concerns": "makeup,oil-control",
        "routine_step": "makeup",
        "routine_time": "morning",
        "key_ingredients": "Organic Rice Starch, Silica, Olive Leaf Powder, Talc-Free",
        "volume": "10 g",
        "description": "แป้งฝุ่นสูตรปราศจากแร่ทัลก์ (100% Talc-Free) ผลิตจากแป้งข้าวออร์แกนิกเนื้อเนียนละเอียดดุจแพรไหม ช่วยดูดซับความมันส่วนเกิน เบลอรูขุมขน เซ็ตเครื่องสำอางให้ติดทน ไม่ทำให้หน้าลอยขาววอก ไม่อุดตันสิว",
        "how_to_use": "ใช้พัฟฟ์หรือแปรงแตะแป้งเบาๆ เคาะส่วนเกินออก แล้วกดซับบริเวณทีโซนหรือทั่วใบหน้า",
        "is_bestseller": 0,
        "is_featured": 1
    },

    # --- BEAUTY TOOLS & GADGETS ---
    {
        "name": "เซตกัวซาหินหยกแท้และลูกกลิ้งนวดหน้า กระชับกรอบหน้า",
        "name_en": "Natural Green Jade Gua Sha & Facial Roller Set",
        "brand": "PURE & OLIVE",
        "category": "tools",
        "subcategory": "tool",
        "price": 590.0,
        "original_price": 790.0,
        "image_url": "https://images.unsplash.com/photo-1617897903246-719242758050?auto=format&fit=crop&w=800&q=80",
        "rating": 4.9,
        "reviews_count": 230,
        "stock": 25,
        "skin_types": "all",
        "skin_concerns": "firming,circulation,puffiness",
        "routine_step": "tool",
        "routine_time": "night",
        "key_ingredients": "100% Natural Xiuyan Jade Stone, Zinc Alloy Frame",
        "volume": "1 เซต (ลูกกลิ้ง + กัวซา + กล่องผ้าซาติน)",
        "description": "อุปกรณ์นวดหน้าหินหยกแท้ธรรมชาติ 100% กักเก็บความเย็นได้ยาวนาน ช่วยกระตุ้นการไหลเวียนโลหิต ลดอาการบวมน้ำยามเช้า ยกกระชับกรอบหน้า ลดเลือนริ้วรอย และช่วยผลักเซรั่มหรือออยล์ให้ซึมลึกสู่ผิวได้อย่างมีประสิทธิภาพ",
        "how_to_use": "หลังทาเซรั่มหรือออยล์บำรุงผิว ใช้กัวซาขูดปาดขึ้นตามแนวกราม แก้ม และหน้าผาก จากล่างขึ้นบน วันละ 5-10 นาที",
        "is_bestseller": 1,
        "is_featured": 1
    },
    {
        "name": "เซตแปรงแต่งหน้าใยมังสวิรัติขนนุ่มพิเศษ 8 ชิ้น ด้ามไม้มินิมอล",
        "name_en": "Ultra-Soft Vegan Essential Makeup Brush Set (8 Pcs)",
        "brand": "PURE & OLIVE",
        "category": "tools",
        "subcategory": "tool",
        "price": 690.0,
        "original_price": 890.0,
        "image_url": "https://images.unsplash.com/photo-1527799820374-dcf8d9d4a388?auto=format&fit=crop&w=800&q=80",
        "rating": 4.8,
        "reviews_count": 115,
        "stock": 20,
        "skin_types": "all",
        "skin_concerns": "makeup,tools",
        "routine_step": "tool",
        "routine_time": "both",
        "key_ingredients": "High-Density Vegan Synthetic Bristles, FSC Beech Wood Handle",
        "volume": "8 ชิ้น พร้อมกระเป๋าผ้าลินินรักษ์โลก",
        "description": "เซตแปรงแต่งหน้าขนนุ่มพิเศษไม่บาดผิว ผลิตจากเส้นใยสังเคราะห์ Vegan เกรดนาโน ดักจับเนื้อแป้งและครีมได้ดีเยี่ยม ด้ามจับทำจากไม้บีชแท้ขัดเนียนสไตล์มินิมอล ครอบคลุมทั้งแปรงลงรองพื้น แปรงแป้ง แปรงปัดแก้ม และแปรงตา",
        "how_to_use": "ใช้สำหรับเกลี่ยแป้ง ครีม หรือเมคอัพตามจุดที่ต้องการ ทำความสะอาดสัปดาห์ละ 1 ครั้งด้วยสบู่สูตรอ่อนโยน",
        "is_bestseller": 0,
        "is_featured": 1
    },
    {
        "name": "เครื่องล้างหน้าคลื่นโซนิคซิลิโคนอ่อนโยน กันน้ำ IPX7",
        "name_en": "Sonic Silicone Gentle Cleansing Brush",
        "brand": "PURE & OLIVE",
        "category": "tools",
        "subcategory": "tool",
        "price": 890.0,
        "original_price": 1290.0,
        "image_url": "https://images.unsplash.com/photo-1512496015851-a90fb38ba796?auto=format&fit=crop&w=800&q=80",
        "rating": 4.9,
        "reviews_count": 87,
        "stock": 15,
        "skin_types": "all,oily,combination,acne-prone",
        "skin_concerns": "cleansing,pores,blackheads",
        "routine_step": "tool",
        "routine_time": "both",
        "key_ingredients": "Food-grade Medical Silicone, Ultrasonic Motor 8000 RPM",
        "volume": "1 เครื่อง พร้อมสายชาร์จแม่เหล็ก USB",
        "description": "เครื่องล้างหน้าคลื่นสั่นโซนิค 8,000 ครั้ง/นาที ขนแปรงซิลิโคนเกรดการแพทย์สัมผัสนุ่มพิเศษ ไม่สะสมแบคทีเรีย ทำความสะอาดลึกถึงรูขุมขน ขจัดสิ่งสกปรกและเซลล์ผิวเสื่อมสภาพได้หมดจดกว่าการใช้มือถึง 6 เท่า",
        "how_to_use": "ชโลมเจลล้างหน้าบนผิวหน้า เปิดเครื่องเลือกระดับความสั่นที่ต้องการ เคลื่อนหัวแปรงวนเป็นวงกลมทั่วใบหน้า 1-2 นาที แล้วล้างออก",
        "is_bestseller": 1,
        "is_featured": 0
    },
    {
        "name": "เครื่องนวดหน้าผลักวิตามินประจุไอออนิก พร้อมแสง LED บำบัดผิว",
        "name_en": "Ionic Nutrient Face Booster & Photon LED Massager",
        "brand": "PURE & OLIVE",
        "category": "tools",
        "subcategory": "tool",
        "price": 1290.0,
        "original_price": 1890.0,
        "image_url": "https://images.unsplash.com/photo-1540555700478-4be289fbecef?auto=format&fit=crop&w=800&q=80",
        "rating": 5.0,
        "reviews_count": 64,
        "stock": 12,
        "skin_types": "all",
        "skin_concerns": "firming,absorption,brightening,aging",
        "routine_step": "tool",
        "routine_time": "night",
        "key_ingredients": "Titanium Probe, Red & Blue LED Lights, Microcurrent EMS",
        "volume": "1 เครื่อง พร้อมฐานชาร์จไร้สาย",
        "description": "นวัตกรรมปรนนิบัติผิวระดับโฮมสปา ผสาน 3 เทคโนโลยี: ประจุไอออนิกช่วยผลักสารบำรุงเซรั่มลึกกว่าทามือ 4 เท่า, คลื่น EMS Microcurrent ยกกระชับกล้ามเนื้อใบหน้า และแสงบำบัด LED (แสงแดงฟื้นฟูคอลลาเจน / แสงน้ำเงินฆ่าเชื้อสิว)",
        "how_to_use": "ทาเซรั่มหรือเจลครีม เปิดโหมดที่ต้องการ แล้วค่อยๆ แนบหัวนวดแนบผิวเลื่อนจากล่างขึ้นบน 5-10 นาทียามค่ำคืน",
        "is_bestseller": 0,
        "is_featured": 1
    }
]

REVIEWS = [
    {
        "product_id": 3,
        "reviewer_name": "คุณนภัสสร พ.",
        "skin_type": "ผิวผสม แพ้ง่ายมาก",
        "rating": 5,
        "comment": "เป็นเซรั่มสควาเลนที่เนื้อดีที่สุดที่เคยใช้มาเลยค่ะ ไม่เหนียวเหนอะหนะ ใช้ติดต่อกัน 2 สัปดาห์ผิวที่เคยแห้งลอกแสบข้างจมูกหายสนิท ผิวดูฟูแน่นขึ้นมาก กลิ่นธรรมชาติผ่อนคลาย แนะนำเลยค่ะ!",
        "created_at": "2026-10-25 14:20:00"
    },
    {
        "product_id": 3,
        "reviewer_name": "คุณธนภรณ์ ล.",
        "skin_type": "ผิวแห้ง ขาดน้ำ",
        "rating": 5,
        "comment": "ประทับใจมากค่ะ ผิวฉ่ำแบบสุขภาพดี ทาก่อนนอนตื่นมารู้สึกหน้าเนียนนุ่มมาก แต่งหน้าง่ายขึ้นเยอะเลยค่ะ",
        "created_at": "2026-11-01 19:45:00"
    },
    {
        "product_id": 1,
        "reviewer_name": "คุณมินตรา ช.",
        "skin_type": "ผิวมัน เป็นสิวง่าย",
        "rating": 5,
        "comment": "เจลล้างหน้าตัวนี้อ่อนโยนจริงๆ สิวผดลดลงอย่างเห็นได้ชัด ล้างแล้วหน้าไม่แห้งเอี๊ยด ใช้คู่กับแปรงล้างหน้าของทางร้านยิ่งฟินสุดๆ ค่ะ",
        "created_at": "2026-11-03 09:12:00"
    },
    {
        "product_id": 7,
        "reviewer_name": "คุณชลธิชา ร.",
        "skin_type": "ผิวบอบบาง แพ้ครีมกันแดดง่าย",
        "rating": 5,
        "comment": "ปกติใช้กันแดดตัวไหนก็อุดตัน แต่ตัวนี้รอดสนิท! เนื้อบางเบาเหมือนน้ำ ซึมไว ไม่ขาวลอย ไม่เยิ้มระหว่างวัน เลิฟมากกก",
        "created_at": "2026-11-05 16:30:00"
    },
    {
        "product_id": 9,
        "reviewer_name": "คุณกัญญารัตน์ ม.",
        "skin_type": "ผิวธรรมดา-แห้ง",
        "rating": 5,
        "comment": "คุชชั่นให้งานผิวสวยคลีนมากกก ได้ลุค Glass Skin แบบเกาหลีแต่ไม่เหนอะ สบายผิวทั้งวัน ไม่ตกร่องเลยค่ะ สีละมุนเป็นธรรมชาติมาก",
        "created_at": "2026-11-06 11:05:00"
    },
    {
        "product_id": 14,
        "reviewer_name": "คุณวริศรา ด.",
        "skin_type": "ทุกสภาพผิว",
        "rating": 5,
        "comment": "เซตกัวซาหินหยกแท้เย็นสบายผิวมาก ด้ามจับถนัดมือ ใช้กัวซานวดหน้าทุกคืนก่อนนอน กรอบหน้าชัดขึ้น ตื่นมาหน้าไม่บวมเลยค่ะ คุณภาพคุ้มราคามาก",
        "created_at": "2026-11-08 21:10:00"
    }
]

def seed_database():
    init_db()
    conn = get_db_connection()
    cursor = conn.cursor()

    # Clear old products and reviews if seeding afresh
    cursor.execute("DELETE FROM products")
    cursor.execute("DELETE FROM reviews")

    # Insert products
    for p in PRODUCTS:
        cursor.execute('''
            INSERT INTO products (
                name, name_en, brand, category, subcategory, price, original_price,
                image_url, rating, reviews_count, stock, skin_types, skin_concerns,
                routine_step, routine_time, key_ingredients, volume, description,
                how_to_use, is_bestseller, is_featured
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            p["name"], p["name_en"], p["brand"], p["category"], p["subcategory"],
            p["price"], p["original_price"], p["image_url"], p["rating"],
            p["reviews_count"], p["stock"], p["skin_types"], p["skin_concerns"],
            p["routine_step"], p["routine_time"], p["key_ingredients"], p["volume"],
            p["description"], p["how_to_use"], p["is_bestseller"], p["is_featured"]
        ))

    # Insert reviews
    for r in REVIEWS:
        cursor.execute('''
            INSERT INTO reviews (product_id, reviewer_name, skin_type, rating, comment, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (r["product_id"], r["reviewer_name"], r["skin_type"], r["rating"], r["comment"], r["created_at"]))

    conn.commit()
    conn.close()
    print(f"Database seeded successfully with {len(PRODUCTS)} products and {len(REVIEWS)} reviews.")

if __name__ == '__main__':
    seed_database()
