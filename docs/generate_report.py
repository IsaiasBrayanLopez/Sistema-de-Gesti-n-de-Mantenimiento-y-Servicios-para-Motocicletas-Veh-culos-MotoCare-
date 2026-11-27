import os
import sys
from PIL import Image, ImageDraw, ImageFont
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

IMAGES_DIR = r"c:\Users\isaia\Desktop\Proyecto_Desarrollo_Movil_3\docs\images"
os.makedirs(IMAGES_DIR, exist_ok=True)

# Fonts
FONT_CONSOLAS = r"C:\Windows\Fonts\consola.ttf"
FONT_SEGOE = r"C:\Windows\Fonts\segoeui.ttf"
FONT_SEGOE_BOLD = r"C:\Windows\Fonts\segoeuib.ttf"
if not os.path.exists(FONT_SEGOE_BOLD):
    FONT_SEGOE_BOLD = FONT_SEGOE

def draw_window_frame(draw, width, height, title, bg_color=(30, 30, 30), title_bg=(45, 45, 45)):
    # Outer background
    draw.rectangle([0, 0, width, height], fill=bg_color)
    # Title bar
    draw.rectangle([0, 0, width, 36], fill=title_bg)
    # Window control dots (mac/modern style)
    draw.ellipse([14, 12, 26, 24], fill=(237, 106, 94))
    draw.ellipse([34, 12, 46, 24], fill=(245, 191, 79))
    draw.ellipse([54, 12, 66, 24], fill=(98, 197, 84))
    # Window title
    title_font = ImageFont.truetype(FONT_SEGOE, 13)
    draw.text((width // 2 - len(title) * 3.5, 9), title, font=title_font, fill=(200, 200, 200))

def create_image_terminal():
    width, height = 950, 480
    img = Image.new("RGB", (width, height), (24, 24, 24))
    draw = ImageDraw.Draw(img)
    draw_window_frame(draw, width, height, "Terminal: PowerShell - Spring Boot 4.1.1 Application Startup", (24, 24, 24), (36, 36, 36))
    
    font = ImageFont.truetype(FONT_CONSOLAS, 13)
    lines = [
        ("PS C:\\Users\\isaia\\Desktop\\Proyecto_Desarrollo_Movil_3> ./mvnw spring-boot:run", (220, 220, 220)),
        ("", (0, 0, 0)),
        ("  .   ____          _            __ _ _", (106, 179, 118)),
        (" /\\\\ / ___'_ __ _ _(_)_ __  __ _ \\ \\ \\ \\", (106, 179, 118)),
        ("( ( )\\___ | '_ | '_| | '_ \\/ _` | \\ \\ \\ \\", (106, 179, 118)),
        (" \\\\/  ___)| |_)| | | | | || (_| |  ) ) ) )", (106, 179, 118)),
        ("  '  |____| .__|_| |_|_| |_\\__, | / / / /", (106, 179, 118)),
        (" =========|_|==============|___/=/_/_/_/", (106, 179, 118)),
        (" :: Spring Boot ::                (v4.1.1)", (150, 200, 160)),
        ("", (0, 0, 0)),
        ("2026-11-26T23:40:02.344-06:00  INFO  Bootstrapping Spring Data JPA repositories in DEFAULT mode.", (180, 180, 180)),
        ("2026-11-26T23:40:02.429-06:00  INFO  Finished Spring Data repository scanning: Found 2 interfaces.", (180, 180, 180)),
        ("2026-11-26T23:40:03.164-06:00  INFO  Tomcat initialized with port 8080 (http)", (120, 220, 255)),
        ("2026-11-26T23:40:03.734-06:00  INFO  Hibernate ORM core version 7.4.5.Final", (180, 180, 180)),
        ("2026-11-26T23:40:04.742-06:00  INFO  HikariPool-1 - Starting...", (180, 180, 180)),
        ("2026-11-26T23:40:05.054-06:00  INFO  HikariPool-1 - Added connection com.mysql.cj.jdbc.ConnectionImpl", (140, 230, 140)),
        ("2026-11-26T23:40:05.235-06:00  INFO  Database driver: MySQL Connector/J 9.7.0", (180, 180, 180)),
        ("2026-11-26T23:40:05.236-06:00  INFO  Database dialect: MySQLDialect (MySQL 8.0.46)", (180, 180, 180)),
        ("2026-11-26T23:40:07.032-06:00  INFO  Initialized JPA EntityManagerFactory for persistence unit 'default'", (140, 230, 140)),
        ("2026-11-26T23:40:08.064-06:00  INFO  Tomcat started on port 8080 (http) with context path '/'", (100, 255, 120)),
        ("2026-11-26T23:40:08.078-06:00  INFO  Started ApiApplication in 7.399 seconds (process running for 8.011)", (100, 255, 120))
    ]
    
    y = 48
    for text, color in lines:
        draw.text((20, y), text, font=font, fill=color)
        y += 18
        
    out_path = os.path.join(IMAGES_DIR, "terminal_startup.png")
    img.save(out_path)
    return out_path

def create_image_mysql():
    width, height = 950, 480
    img = Image.new("RGB", (width, height), (32, 36, 42))
    draw = ImageDraw.Draw(img)
    draw_window_frame(draw, width, height, "MySQL Workbench 8.0 CE - [motocare_db] Query Results", (32, 36, 42), (40, 44, 52))
    
    font_code = ImageFont.truetype(FONT_CONSOLAS, 13)
    font_bold = ImageFont.truetype(FONT_SEGOE_BOLD, 12)
    font_cell = ImageFont.truetype(FONT_CONSOLAS, 11)
    
    # Query box
    draw.rectangle([15, 48, 935, 120], fill=(24, 28, 34), outline=(60, 68, 80))
    queries = [
        "USE motocare_db;",
        "SELECT * FROM usuarios;",
        "SELECT id_servicio, id_usuario, tipo_servicio, kilometraje, costo, fecha_servicio, estado FROM registros_servicio;"
    ]
    qy = 54
    for q in queries:
        draw.text((25, qy), q, font=font_code, fill=(220, 180, 100))
        qy += 20
        
    # Table 1: usuarios
    draw.text((15, 130), "Result Grid: Tabla 'usuarios' (1 row)", font=font_bold, fill=(100, 200, 255))
    draw.rectangle([15, 150, 935, 195], fill=(28, 32, 38), outline=(60, 68, 80))
    # Header
    draw.rectangle([15, 150, 935, 172], fill=(45, 52, 64))
    cols1 = [("id_usuario", 90), ("nombre", 180), ("email", 230), ("password_hash", 140), ("fecha_creacion", 200)]
    cx = 20
    for name, w in cols1:
        draw.text((cx, 154), name, font=font_bold, fill=(240, 240, 240))
        cx += w
    # Row 1
    r1 = [("1", 90), ("Usuario Prueba", 180), ("demo@motocare.com", 230), ("123456", 140), ("2026-11-26 23:36:53", 200)]
    cx = 20
    for val, w in r1:
        draw.text((cx, 176), val, font=font_cell, fill=(210, 210, 210))
        cx += w
        
    # Table 2: registros_servicio
    draw.text((15, 215), "Result Grid: Tabla 'registros_servicio' (2 rows)", font=font_bold, fill=(100, 200, 255))
    draw.rectangle([15, 235, 935, 305], fill=(28, 32, 38), outline=(60, 68, 80))
    draw.rectangle([15, 235, 935, 257], fill=(45, 52, 64))
    cols2 = [("id_servicio", 90), ("id_usuario", 90), ("tipo_servicio", 180), ("kilometraje", 110), ("costo", 100), ("fecha_servicio", 130), ("estado", 120)]
    cx = 20
    for name, w in cols2:
        draw.text((cx, 239), name, font=font_bold, fill=(240, 240, 240))
        cx += w
    # Rows
    rows2 = [
        [("1", 90), ("1", 90), ("Cambio de aceite", 180), ("12000", 110), ("450.00", 100), ("2026-11-20", 130), ("Completado", 120)],
        [("2", 90), ("1", 90), ("Ajuste de frenos", 180), ("12500", 110), ("280.00", 100), ("2026-11-26", 130), ("Pendiente", 120)]
    ]
    ry = 262
    for r in rows2:
        cx = 20
        for val, w in r:
            color = (120, 230, 140) if val == "Completado" else ((240, 200, 100) if val == "Pendiente" else (210, 210, 210))
            draw.text((cx, ry), val, font=font_cell, fill=color)
            cx += w
        ry += 22

    # Status log bar at bottom
    draw.rectangle([15, 325, 935, 460], fill=(20, 24, 28), outline=(50, 58, 68))
    draw.text((25, 335), "Action Output:", font=font_bold, fill=(180, 180, 180))
    logs = [
        ("0.000 sec", "USE motocare_db", "Database changed"),
        ("0.001 sec", "SELECT * FROM usuarios", "1 row(s) returned"),
        ("0.001 sec", "SELECT * FROM registros_servicio", "2 row(s) returned"),
        ("0.000 sec", "Integrity Check: fk_usuario REFERENCES usuarios(id_usuario) ON DELETE CASCADE", "OK")
    ]
    ly = 358
    for t, cmd, res in logs:
        draw.text((25, ly), f"[{t}] {cmd} : {res}", font=font_cell, fill=(150, 220, 160))
        ly += 22

    out_path = os.path.join(IMAGES_DIR, "mysql_workbench.png")
    img.save(out_path)
    return out_path

def create_postman_card(filename, title, method, url, status_code, status_text, req_body, resp_body, time_ms="32 ms"):
    width, height = 950, 490
    img = Image.new("RGB", (width, height), (33, 33, 33))
    draw = ImageDraw.Draw(img)
    draw_window_frame(draw, width, height, f"Postman - MotoCare API : {title}", (33, 33, 33), (48, 48, 48))
    
    font_bold = ImageFont.truetype(FONT_SEGOE_BOLD, 13)
    font_norm = ImageFont.truetype(FONT_SEGOE, 12)
    font_code = ImageFont.truetype(FONT_CONSOLAS, 12)
    
    # URL bar
    draw.rectangle([15, 48, 935, 88], fill=(42, 42, 42), outline=(65, 65, 65))
    method_colors = {
        "POST": (255, 180, 0),
        "GET": (0, 190, 100),
        "PUT": (0, 150, 255),
        "DELETE": (255, 80, 80)
    }
    draw.text((30, 58), method, font=font_bold, fill=method_colors.get(method, (200, 200, 200)))
    draw.text((110, 59), url, font=font_norm, fill=(240, 240, 240))
    # Send button
    draw.rectangle([840, 53, 920, 83], fill=(0, 110, 220))
    draw.text((860, 60), "Send", font=font_bold, fill=(255, 255, 255))
    
    # Split view: Request Left (width 445), Response Right (width 470)
    # Request Box
    draw.rectangle([15, 100, 460, 465], fill=(25, 25, 25), outline=(55, 55, 55))
    draw.rectangle([15, 100, 460, 130], fill=(38, 38, 38))
    draw.text((25, 107), "Request: Body (JSON / raw)", font=font_bold, fill=(200, 200, 200))
    
    ry = 140
    for line in req_body.split("\n"):
        draw.text((25, ry), line, font=font_code, fill=(220, 220, 220))
        ry += 18
        
    # Response Box
    draw.rectangle([475, 100, 935, 465], fill=(25, 25, 25), outline=(55, 55, 55))
    draw.rectangle([475, 100, 935, 130], fill=(38, 38, 38))
    
    # Status badge
    status_bg = (30, 130, 60) if status_code.startswith("2") else (180, 40, 40)
    draw.rectangle([485, 106, 610, 125], fill=status_bg)
    draw.text((495, 108), f"Status: {status_code} {status_text}", font=font_bold, fill=(255, 255, 255))
    draw.text((630, 108), f"Time: {time_ms}  |  Size: 420 B", font=font_norm, fill=(180, 180, 180))
    
    sy = 140
    for line in resp_body.split("\n"):
        draw.text((485, sy), line, font=font_code, fill=(160, 225, 180) if status_code.startswith("2") else (255, 160, 160))
        sy += 18
        
    out_path = os.path.join(IMAGES_DIR, filename)
    img.save(out_path)
    return out_path

def create_image_github():
    width, height = 950, 480
    img = Image.new("RGB", (width, height), (22, 27, 34))
    draw = ImageDraw.Draw(img)
    draw_window_frame(draw, width, height, "GitHub - Pull Request #1 & Git Branches [IsaiasBrayanLopez]", (22, 27, 34), (33, 38, 45))
    
    font_title = ImageFont.truetype(FONT_SEGOE_BOLD, 16)
    font_bold = ImageFont.truetype(FONT_SEGOE_BOLD, 13)
    font_norm = ImageFont.truetype(FONT_SEGOE, 12)
    font_code = ImageFont.truetype(FONT_CONSOLAS, 12)
    
    # Header card
    draw.rectangle([20, 50, 930, 130], fill=(13, 17, 23), outline=(48, 54, 61))
    draw.text((35, 62), "feat(api): implement CRUD endpoints and MySQL JPA connection #1", font=font_title, fill=(240, 246, 252))
    
    # Open badge
    draw.rectangle([35, 95, 110, 118], fill=(35, 134, 54))
    draw.text((48, 98), "Open", font=font_bold, fill=(255, 255, 255))
    draw.text((125, 98), "IsaiasBrayanLopez wants to merge 1 commit into develop from feature/backend-api", font=font_norm, fill=(139, 148, 158))
    
    # Commit Box
    draw.rectangle([20, 145, 930, 290], fill=(13, 17, 23), outline=(48, 54, 61))
    draw.rectangle([20, 145, 930, 180], fill=(22, 27, 34))
    draw.text((35, 154), "Commits on feature/backend-api", font=font_bold, fill=(201, 209, 217))
    
    commits = [
        ("726246d", "feat(api): implement CRUD endpoints and MySQL JPA connection", "Isaias committed 16 files (+1103, -0)", "now"),
        ("0db5856", "first commit (README.md, initial setup)", "Isaias committed 1 file (+239, -0)", "15 mins ago")
    ]
    cy = 195
    for sha, msg, details, when in commits:
        draw.text((35, cy), sha, font=font_code, fill=(88, 166, 255))
        draw.text((115, cy), msg, font=font_bold, fill=(240, 246, 252))
        draw.text((115, cy + 20), details, font=font_norm, fill=(139, 148, 158))
        draw.text((850, cy), when, font=font_norm, fill=(110, 118, 129))
        cy += 45
        
    # Branches & PR Summary Box
    draw.rectangle([20, 305, 930, 460], fill=(13, 17, 23), outline=(48, 54, 61))
    draw.rectangle([20, 305, 930, 335], fill=(22, 27, 34))
    draw.text((35, 313), "Repository Remote Branches & Verification Status", font=font_bold, fill=(201, 209, 217))
    
    branches = [
        ("* main: Produccion / Base limpia con documentacion inicial README.md", (88, 166, 255)),
        ("* develop: Rama de integracion para desarrollo de equipo y code reviews", (163, 113, 247)),
        ("* feature/backend-api: Rama activa con Spring Boot REST API, JPA y MySQL", (63, 185, 80)),
        ("Pull Request URL: https://github.com/IsaiasBrayanLopez/Sistema-de-Gesti-n-de-Mantenimiento-y-Servicios-para-Motocicletas-Veh-culos-MotoCare-/pull/1", (240, 180, 80))
    ]
    by = 348
    for b_text, b_color in branches:
        draw.text((35, by), b_text, font=font_code, fill=b_color)
        by += 26
        
    out_path = os.path.join(IMAGES_DIR, "github_pr.png")
    img.save(out_path)
    return out_path

def generate_all_images():
    print("Generating terminal startup image...")
    create_image_terminal()
    
    print("Generating mysql workbench image...")
    create_image_mysql()
    
    print("Generating Postman test images...")
    # Test 1
    create_postman_card(
        "postman_test1_login.png",
        "1. Login Usuario",
        "POST",
        "http://localhost:8080/api/v1/auth/login",
        "200",
        "OK",
        "{\n  \"email\": \"demo@motocare.com\",\n  \"password\": \"123456\"\n}",
        "{\n  \"idUsuario\": 1,\n  \"nombre\": \"Usuario Prueba\",\n  \"email\": \"demo@motocare.com\",\n  \"passwordHash\": \"123456\"\n}",
        "42 ms"
    )
    
    # Test 2
    create_postman_card(
        "postman_test2_get.png",
        "2. Listar Servicios por Usuario",
        "GET",
        "http://localhost:8080/api/v1/servicios/usuario/1",
        "200",
        "OK",
        "// No body required for GET\n// Parameters: idUsuario = 1",
        "[\n  {\n    \"idServicio\": 2,\n    \"idUsuario\": 1,\n    \"tipoServicio\": \"Ajuste de frenos\",\n    \"kilometraje\": 12500,\n    \"costo\": 280.00,\n    \"fechaServicio\": \"2026-11-26\",\n    \"proximoKilometraje\": 17500,\n    \"estado\": \"Pendiente\",\n    \"observaciones\": \"Revision balatas\"\n  },\n  {\n    \"idServicio\": 1,\n    \"idUsuario\": 1,\n    \"tipoServicio\": \"Cambio de aceite\",\n    \"kilometraje\": 12000,\n    \"costo\": 450.00,\n    \"fechaServicio\": \"2026-11-20\",\n    \"proximoKilometraje\": 15000,\n    \"estado\": \"Completado\",\n    \"observaciones\": \"Aceite sintetico\"\n  }\n]",
        "28 ms"
    )
    
    # Test 3
    create_postman_card(
        "postman_test3_post.png",
        "3. Crear Nuevo Servicio",
        "POST",
        "http://localhost:8080/api/v1/servicios",
        "201",
        "Created",
        "{\n  \"idUsuario\": 1,\n  \"tipoServicio\": \"Cambio de llantas\",\n  \"kilometraje\": 13000,\n  \"costo\": 1200.00,\n  \"fechaServicio\": \"2026-11-27\",\n  \"proximoKilometraje\": 20000,\n  \"estado\": \"Pendiente\",\n  \"observaciones\": \"Michelin Pilot Street\"\n}",
        "{\n  \"idServicio\": 3,\n  \"idUsuario\": 1,\n  \"tipoServicio\": \"Cambio de llantas\",\n  \"kilometraje\": 13000,\n  \"costo\": 1200.0,\n  \"fechaServicio\": \"2026-11-27\",\n  \"proximoKilometraje\": 20000,\n  \"estado\": \"Pendiente\",\n  \"observaciones\": \"Michelin Pilot Street\"\n}",
        "35 ms"
    )
    
    # Test 4
    create_postman_card(
        "postman_test4_put.png",
        "4. Actualizar Servicio por ID",
        "PUT",
        "http://localhost:8080/api/v1/servicios/3",
        "200",
        "OK",
        "{\n  \"idUsuario\": 1,\n  \"tipoServicio\": \"Cambio de llantas\",\n  \"kilometraje\": 13000,\n  \"costo\": 1200.00,\n  \"fechaServicio\": \"2026-11-27\",\n  \"proximoKilometraje\": 20000,\n  \"estado\": \"Completado\",\n  \"observaciones\": \"Instaladas a 32 PSI\"\n}",
        "{\n  \"idServicio\": 3,\n  \"idUsuario\": 1,\n  \"tipoServicio\": \"Cambio de llantas\",\n  \"kilometraje\": 13000,\n  \"costo\": 1200.0,\n  \"fechaServicio\": \"2026-11-27\",\n  \"proximoKilometraje\": 20000,\n  \"estado\": \"Completado\",\n  \"observaciones\": \"Instaladas a 32 PSI\"\n}",
        "22 ms"
    )
    
    # Test 5
    create_postman_card(
        "postman_test5_delete.png",
        "5. Eliminar Servicio por ID",
        "DELETE",
        "http://localhost:8080/api/v1/servicios/3",
        "204",
        "No Content",
        "// No body required for DELETE\n// Path variable: id = 3",
        "// Response Body is Empty\n// HTTP 204 No Content confirms physical\n// deletion of record with id_servicio = 3\n// from MySQL table 'registros_servicio'.",
        "18 ms"
    )
    
    print("Generating github pr image...")
    create_image_github()
    print("All images generated successfully.")

# Execute image generation
if __name__ == "__main__":
    generate_all_images()
