import os
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

DOCX_OUTPUT_PATH = r"C:\Users\isaia\OneDrive\Desktop\Reporte_Proyecto_MotoCare_Fase2.docx"
DOCX_BACKUP_PATH = r"c:\Users\isaia\Desktop\Proyecto_Desarrollo_Movil_3\docs\Reporte_Proyecto_MotoCare_Fase2.docx"
IMAGES_DIR = r"c:\Users\isaia\Desktop\Proyecto_Desarrollo_Movil_3\docs\images"

def set_cell_background(cell, fill_hex):
    shading_elm = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    cell._tc.get_or_add_tcPr().append(shading_elm)

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        node = OxmlElement(f'w:{m}')
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def add_callout(doc, text, title="NOTA TECNICA"):
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell = tbl.cell(0, 0)
    set_cell_background(cell, "F0F4F8")
    set_cell_margins(cell, top=140, bottom=140, left=200, right=180)
    
    # Left border only (thick blue)
    tcPr = cell._tc.get_or_add_tcPr()
    tcBorders = parse_xml(
        f'<w:tcBorders {nsdecls("w")}>'
        f'<w:top w:val="none"/>'
        f'<w:left w:val="single" w:sz="24" w:space="0" w:color="1E3A8A"/>'
        f'<w:bottom w:val="none"/>'
        f'<w:right w:val="none"/>'
        f'</w:tcBorders>'
    )
    tcPr.append(tcBorders)
    
    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(2)
    run_t = p.add_run(f"[{title}] ")
    run_t.bold = True
    run_t.font.name = "Segoe UI"
    run_t.font.size = Pt(10)
    run_t.font.color.rgb = RGBColor(30, 58, 138)
    
    run_b = p.add_run(text)
    run_b.font.name = "Segoe UI"
    run_b.font.size = Pt(9.5)
    run_b.font.color.rgb = RGBColor(40, 50, 70)
    
    doc.add_paragraph().paragraph_format.space_after = Pt(4)

def add_code_block(doc, code_str):
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell = tbl.cell(0, 0)
    set_cell_background(cell, "1E222A")
    set_cell_margins(cell, top=100, bottom=100, left=150, right=150)
    
    tcPr = cell._tc.get_or_add_tcPr()
    tcBorders = parse_xml(
        f'<w:tcBorders {nsdecls("w")}>'
        f'<w:top w:val="single" w:sz="4" w:space="0" w:color="3E4451"/>'
        f'<w:left w:val="single" w:sz="4" w:space="0" w:color="3E4451"/>'
        f'<w:bottom w:val="single" w:sz="4" w:space="0" w:color="3E4451"/>'
        f'<w:right w:val="single" w:sz="4" w:space="0" w:color="3E4451"/>'
        f'</w:tcBorders>'
    )
    tcPr.append(tcBorders)
    
    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(2)
    run = p.add_run(code_str)
    run.font.name = "Consolas"
    run.font.size = Pt(9)
    run.font.color.rgb = RGBColor(220, 224, 230)
    
    doc.add_paragraph().paragraph_format.space_after = Pt(4)

def add_image_figure(doc, img_filename, caption_text, width_inches=6.2):
    img_path = os.path.join(IMAGES_DIR, img_filename)
    if os.path.exists(img_path):
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.paragraph_format.space_before = Pt(8)
        p_img.paragraph_format.space_after = Pt(2)
        run = p_img.add_run()
        run.add_picture(img_path, width=Inches(width_inches))
        
        p_cap = doc.add_paragraph()
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_cap.paragraph_format.space_before = Pt(2)
        p_cap.paragraph_format.space_after = Pt(10)
        run_cap = p_cap.add_run(caption_text)
        run_cap.font.name = "Segoe UI"
        run_cap.font.size = Pt(9)
        run_cap.font.italic = True
        run_cap.font.color.rgb = RGBColor(100, 110, 120)

def build_report():
    doc = docx.Document()
    
    # Configure 1-inch margins
    sections = doc.sections
    for section in sections:
        section.top_margin = Inches(1)
        section.bottom_margin = Inches(1)
        section.left_margin = Inches(1)
        section.right_margin = Inches(1)
        
        # Header / Footer
        header = section.header
        hp = header.paragraphs[0]
        hp.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        hrun = hp.add_run("MotoCare API - Reporte Tecnico de Implementacion (Fase 2)")
        hrun.font.name = "Segoe UI"
        hrun.font.size = Pt(8.5)
        hrun.font.color.rgb = RGBColor(140, 150, 160)
        
        footer = section.footer
        fp = footer.paragraphs[0]
        fp.alignment = WD_ALIGN_PARAGRAPH.CENTER
        frun = fp.add_run("Proyecto de Desarrollo Movil | Spring Boot & MySQL | Noviembre 2026")
        frun.font.name = "Segoe UI"
        frun.font.size = Pt(8.5)
        frun.font.color.rgb = RGBColor(140, 150, 160)

    # ==================== PORTADA ====================
    title_p = doc.add_paragraph()
    title_p.paragraph_format.space_before = Pt(36)
    title_p.paragraph_format.space_after = Pt(6)
    title_run = title_p.add_run("REPORTE TECNICO DE IMPLEMENTACION")
    title_run.font.name = "Segoe UI"
    title_run.font.size = Pt(24)
    title_run.bold = True
    title_run.font.color.rgb = RGBColor(26, 54, 93) # Navy blue
    
    sub_p = doc.add_paragraph()
    sub_p.paragraph_format.space_before = Pt(0)
    sub_p.paragraph_format.space_after = Pt(18)
    sub_run = sub_p.add_run("Fase 2: Backend REST con Spring Boot, Persistencia en MySQL y Verificacion CRUD con Postman")
    sub_run.font.name = "Segoe UI"
    sub_run.font.size = Pt(14)
    sub_run.font.color.rgb = RGBColor(43, 108, 176)
    
    # Divider line
    div_p = doc.add_paragraph()
    div_p.paragraph_format.space_after = Pt(18)
    drun = div_p.add_run("―" * 45)
    drun.font.color.rgb = RGBColor(200, 210, 220)
    
    # Metadata Table
    meta_tbl = doc.add_table(rows=6, cols=2)
    meta_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    meta_data = [
        ("Proyecto:", "Sistema de Gestion de Mantenimiento y Servicios para Motocicletas y Vehiculos (MotoCare)"),
        ("Modulo:", "Backend REST API (Spring Boot 4.1 / Java 25 / MySQL 8.0)"),
        ("Autor / Desarrollador:", "Isaias Brayan Lopez"),
        ("Repositorio GitHub:", "https://github.com/IsaiasBrayanLopez/Sistema-de-Gesti-n-de-Mantenimiento-y-Servicios-para-Motocicletas-Veh-culos-MotoCare-"),
        ("Rama de Entrega / PR:", "feature/backend-api -> develop (Pull Request #1)"),
        ("Fecha de Entrega:", "26 de Noviembre de 2026")
    ]
    for i, (k, v) in enumerate(meta_data):
        cell_k = meta_tbl.cell(i, 0)
        cell_v = meta_tbl.cell(i, 1)
        cell_k.width = Inches(2.2)
        cell_v.width = Inches(4.3)
        set_cell_margins(cell_k, top=60, bottom=60, left=80, right=80)
        set_cell_margins(cell_v, top=60, bottom=60, left=80, right=80)
        
        pk = cell_k.paragraphs[0]
        pk.paragraph_format.space_before = Pt(1)
        pk.paragraph_format.space_after = Pt(1)
        rk = pk.add_run(k)
        rk.font.name = "Segoe UI"
        rk.font.size = Pt(10)
        rk.bold = True
        rk.font.color.rgb = RGBColor(30, 41, 59)
        
        pv = cell_v.paragraphs[0]
        pv.paragraph_format.space_before = Pt(1)
        pv.paragraph_format.space_after = Pt(1)
        rv = pv.add_run(v)
        rv.font.name = "Segoe UI"
        rv.font.size = Pt(10)
        rv.font.color.rgb = RGBColor(51, 65, 85)

    doc.add_page_break()

    # Helper for Section Titles
    def add_h1(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(16)
        p.paragraph_format.space_after = Pt(6)
        run = p.add_run(text)
        run.font.name = "Segoe UI"
        run.font.size = Pt(15)
        run.bold = True
        run.font.color.rgb = RGBColor(30, 58, 138)
        return p

    def add_h2(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(12)
        p.paragraph_format.space_after = Pt(4)
        run = p.add_run(text)
        run.font.name = "Segoe UI"
        run.font.size = Pt(12.5)
        run.bold = True
        run.font.color.rgb = RGBColor(43, 108, 176)
        return p

    def add_p(text, bold_prefix=None):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(2)
        p.paragraph_format.space_after = Pt(5)
        p.paragraph_format.line_spacing = 1.15
        if bold_prefix:
            rb = p.add_run(bold_prefix)
            rb.font.name = "Segoe UI"
            rb.font.size = Pt(10)
            rb.bold = True
            rb.font.color.rgb = RGBColor(30, 41, 59)
        run = p.add_run(text)
        run.font.name = "Segoe UI"
        run.font.size = Pt(10)
        run.font.color.rgb = RGBColor(51, 65, 85)
        return p

    # ==================== RESUMEN EJECUTIVO ====================
    add_h1("Resumen Ejecutivo")
    add_p(
        "El presente informe documenta de forma exhaustiva el desarrollo, arquitectura, ejecucion y validacion de la Fase 2 "
        "del proyecto MotoCare (Sistema de Gestion de Mantenimiento y Servicios para Motocicletas y Vehiculos). "
        "En esta etapa se implemento un servidor RESTful con Spring Boot y Java, configurando la comunicacion con una base de "
        "datos relacional MySQL 8.0 a traves de Spring Data JPA y Hibernate. "
        "Se expusieron y verificaron al 100% las operaciones CRUD requeridas para la autenticacion de usuarios y administracion de servicios, "
        "garantizando el soporte de solicitudes de origen cruzado (CORS) para su posterior integracion sin restricciones con la aplicacion movil en Flutter."
    )
    
    add_callout(
        doc,
        "Todos los endpoints fueron sometidos a pruebas funcionales en Postman y automatizadas via script, obteniendo los codigos de respuesta "
        "HTTP 200 OK, 201 Created y 204 No Content. La coleccion de pruebas fue exportada y versionada en la carpeta /docs del repositorio.",
        "EXITO EN PRUEBAS Y VALIDACION"
    )

    # ==================== SECCION 1 ====================
    add_h1("1. Introduccion y Objetivos de la Fase 2")
    add_p(
        "En el desarrollo de software moderno enfocado a plataformas moviles, desacoplar la interfaz de usuario de la logica de persistencia "
        "es una practica fundamental. La arquitectura cliente-servidor mediante API REST permite que multiples clientes (aplicaciones Flutter en Android/iOS, "
        "portales web administrativos) consuman un unico punto de verdad centralizado y seguro."
    )
    add_p("Los objetivos tecnicos definidos y alcanzados en esta fase fueron:", bold_prefix="Objetivos especificos: ")
    bullets_obj = [
        "Disenar e instanciar el esquema relacional 'motocare_db' en MySQL con integridad referencial y eliminacion en cascada.",
        "Generar y estructurar el proyecto backend en Spring Boot separando responsabilidades en controladores, modelos y repositorios.",
        "Configurar el DataSource JDBC y propiedades de Hibernate ORM en 'application.properties' respetando la seguridad de credenciales.",
        "Implementar las entidades JPA 'Usuario' y 'RegistroServicio' junto con sus correspondientes interfaces 'JpaRepository'.",
        "Construir los controladores REST 'AuthController' y 'ServicioController' con CORS habilitado y documentacion Javadoc completa.",
        "Verificar cada una de las 5 operaciones CRUD desde Postman y asegurar la persistencia inmediata en MySQL.",
        "Versionar el codigo siguiendo el flujo colaborativo en Git, creando ramas 'main', 'develop' y 'feature/backend-api', y abriendo el Pull Request correspondiente."
    ]
    for b in bullets_obj:
        bp = doc.add_paragraph(style='List Bullet')
        bp.paragraph_format.space_before = Pt(1)
        bp.paragraph_format.space_after = Pt(2)
        brun = bp.add_run(b)
        brun.font.name = "Segoe UI"
        brun.font.size = Pt(9.5)
        brun.font.color.rgb = RGBColor(51, 65, 85)

    # ==================== SECCION 2 ====================
    add_h1("2. Librerias del Backend y Justificacion Tecnica")
    add_p(
        "La seleccion de dependencias responde estrictamente a criterios de estabilidad, desacoplamiento, facilidad de mantenimiento y optimizacion "
        "en la transmision de datos JSON hacia clientes moviles. La siguiente tabla detalla cada componente:"
    )

    tbl_deps = doc.add_table(rows=5, cols=4)
    tbl_deps.alignment = WD_TABLE_ALIGNMENT.CENTER
    deps_headers = ["Dependencia", "Identificador Maven", "Proposito Tecnico", "Donde se Aplica"]
    for col_idx, h_text in enumerate(deps_headers):
        cell = tbl_deps.cell(0, col_idx)
        set_cell_background(cell, "1E3A8A")
        set_cell_margins(cell, top=100, bottom=100, left=100, right=100)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = p.add_run(h_text)
        run.bold = True
        run.font.name = "Segoe UI"
        run.font.size = Pt(9.5)
        run.font.color.rgb = RGBColor(255, 255, 255)

    deps_rows = [
        ("Spring Web (MVC)", "spring-boot-starter-webmvc", "Expone endpoints REST, maneja el servidor embebido Tomcat y serializa objetos Java a JSON con Jackson.", "Clases en controllers/ (@RestController, @RequestMapping, @CrossOrigin)."),
        ("Spring Data JPA", "spring-boot-starter-data-jpa", "Mapea clases Java a tablas SQL mediante Hibernate y genera consultas CRUD automaticas sin escribir SQL manual.", "Clases en models/ (@Entity) e interfaces en repositories/ (JpaRepository)."),
        ("MySQL Connector/J", "mysql-connector-j", "Driver JDBC oficial que establece el canal de comunicacion entre la aplicacion Java y el motor MySQL.", "Configuracion de conexion en src/main/resources/application.properties."),
        ("Spring Boot Validation", "spring-boot-starter-validation", "Valida campos obligatorios, formatos de correo y valores numericos antes de guardar en base de datos.", "Atributos de modelos y parametros @Valid en controladores.")
    ]

    for row_idx, r_data in enumerate(deps_rows, start=1):
        bg_color = "F8FAFC" if row_idx % 2 == 1 else "FFFFFF"
        for col_idx, text in enumerate(r_data):
            cell = tbl_deps.cell(row_idx, col_idx)
            set_cell_background(cell, bg_color)
            set_cell_margins(cell, top=80, bottom=80, left=90, right=90)
            p = cell.paragraphs[0]
            run = p.add_run(text)
            run.font.name = "Segoe UI"
            run.font.size = Pt(9)
            if col_idx == 0:
                run.bold = True
            run.font.color.rgb = RGBColor(30, 41, 59)

    add_h2("Justificacion de Arquitectura: Por que Spring Data JPA y no JDBC Tradicional")
    add_p(
        "Durante la defensa tecnica del proyecto, es crucial fundamentar la decision de emplear Spring Data JPA sobre sentencias JDBC nativas. "
        "Las principales ventajas tecnicas comprobadas son:"
    )
    reasons_jpa = [
        "Productividad y reduccion de codigo repetitivo: Evita tener que codificar manualmente objetos Connection, PreparedStatement y ResultSet, reduciendo hasta un 70% del codigo de persistencia.",
        "Consultas derivadas automaticas: La interfaz RegistroServicioRepository permite definir el metodo 'findByIdUsuarioOrderByFechaServicioDesc' y Spring genera internamente la consulta SQL exacta optimizada.",
        "Pool de conexiones de alto rendimiento (HikariCP): Spring Boot gestiona de forma transparente un pool reutilizable de conexiones TCP activas hacia MySQL, eliminando el costo de crear una conexion por cada peticion HTTP de la aplicacion movil.",
        "Seguridad contra inyeccion SQL: Hibernate parametriza de manera estricta todos los valores antes de ejecutarlos contra el motor relacional."
    ]
    for r in reasons_jpa:
        bp = doc.add_paragraph(style='List Bullet')
        bp.paragraph_format.space_before = Pt(1)
        bp.paragraph_format.space_after = Pt(2)
        brun = bp.add_run(r)
        brun.font.name = "Segoe UI"
        brun.font.size = Pt(9.5)
        brun.font.color.rgb = RGBColor(51, 65, 85)

    # Flujo de datos
    add_h2("Flujo de Peticion y Desacoplamiento por Capas")
    add_p("La arquitectura implementa un flujo unidireccional y desacoplado:")
    add_code_block(
        doc,
        "1. Cliente (Postman / Flutter Mobile)\n"
        "   └── Envia peticion HTTP (JSON) con verbo REST (GET, POST, PUT, DELETE)\n"
        "2. Controlador (@RestController en com.motocare.api.controllers)\n"
        "   └── Recibe peticion, deserializa JSON a Entidad mediante Jackson, valida datos y delega.\n"
        "3. Repositorio (JpaRepository en com.motocare.api.repositories)\n"
        "   └── Ejecuta logica de acceso a datos utilizando Hibernate ORM y cache de primer nivel.\n"
        "4. Driver JDBC (MySQL Connector/J 9.7)\n"
        "   └── Transmite sentencias SQL optimizadas al socket TCP port 3306 usando HikariCP.\n"
        "5. Motor MySQL 8.0 (motocare_db)\n"
        "   └── Ejecuta consulta, garantiza atomicidad (ACID) y retorna filas modificadas/leidas."
    )

    # ==================== SECCION 3 ====================
    add_h1("3. Diseno y Persistencia en Base de Datos MySQL")
    add_p(
        "Se creo la base de datos 'motocare_db' con soporte UTF-8. El esquema cuenta con dos entidades relacionales conectadas "
        "mediante la clave foranea 'fk_usuario' con integridad referencial 'ON DELETE CASCADE' para prevenir registros huerfanos "
        "en caso de eliminacion de cuentas de usuario."
    )
    
    add_h2("Script SQL Ejecutado y Semilla de Datos Inicial")
    add_code_block(
        doc,
        "CREATE DATABASE IF NOT EXISTS motocare_db;\n"
        "USE motocare_db;\n\n"
        "CREATE TABLE usuarios (\n"
        "    id_usuario INT AUTO_INCREMENT PRIMARY KEY,\n"
        "    nombre VARCHAR(100) NOT NULL,\n"
        "    email VARCHAR(100) NOT NULL UNIQUE,\n"
        "    password_hash VARCHAR(255) NOT NULL,\n"
        "    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP\n"
        ");\n\n"
        "CREATE TABLE registros_servicio (\n"
        "    id_servicio INT AUTO_INCREMENT PRIMARY KEY,\n"
        "    id_usuario INT NOT NULL,\n"
        "    tipo_servicio VARCHAR(80) NOT NULL,\n"
        "    kilometraje INT NOT NULL,\n"
        "    costo DECIMAL(10,2) NOT NULL,\n"
        "    fecha_servicio DATE NOT NULL,\n"
        "    proximo_kilometraje INT NOT NULL,\n"
        "    estado VARCHAR(20) DEFAULT 'Pendiente',\n"
        "    observaciones TEXT,\n"
        "    CONSTRAINT fk_usuario FOREIGN KEY (id_usuario)\n"
        "        REFERENCES usuarios(id_usuario) ON DELETE CASCADE\n"
        ");\n\n"
        "INSERT INTO usuarios (nombre, email, password_hash)\n"
        "VALUES ('Usuario Prueba', 'demo@motocare.com', '123456');\n\n"
        "INSERT INTO registros_servicio\n"
        "(id_usuario, tipo_servicio, kilometraje, costo, fecha_servicio, proximo_kilometraje, estado, observaciones)\n"
        "VALUES\n"
        "(1, 'Cambio de aceite', 12000, 450.00, '2026-11-20', 15000, 'Completado', 'Aceite sintetico 10W-40'),\n"
        "(1, 'Ajuste de frenos', 12500, 280.00, '2026-11-26', 17500, 'Pendiente', 'Revision de balatas delanteras');"
    )

    add_image_figure(doc, "mysql_workbench.png", "Figura 1: Verificacion en MySQL Workbench de las tablas creadas y los registros semilla.")

    # ==================== SECCION 4 ====================
    add_h1("4. Estructura y Organizacion del Proyecto en Spring Boot")
    add_p(
        "El proyecto fue estructurado bajo las directrices oficiales de Spring Boot, ubicando el codigo fuente en el paquete "
        "'com.motocare.api' con clara segregacion de responsabilidades:"
    )
    
    add_code_block(
        doc,
        "src/main/java/com/motocare/api/\n"
        "├── controllers/\n"
        "│   ├── AuthController.java        # Endpoints /api/v1/auth (login, register)\n"
        "│   └── ServicioController.java    # Endpoints /api/v1/servicios (CRUD completo)\n"
        "├── models/\n"
        "│   ├── Usuario.java               # Entidad mapeada a tabla 'usuarios'\n"
        "│   └── RegistroServicio.java      # Entidad mapeada a tabla 'registros_servicio'\n"
        "├── repositories/\n"
        "│   ├── UsuarioRepository.java     # Interfaz Spring Data con findByEmail\n"
        "│   └── RegistroServicioRepository.java # Consultas ordenadas por fecha desc\n"
        "└── ApiApplication.java           # Punto de entrada de la aplicacion Spring Boot"
    )

    add_h2("Configuracion del DataSource en application.properties")
    add_p(
        "El archivo 'src/main/resources/application.properties' establece los parametros de conexion con MySQL 8.0. "
        "Se configuro el dialecto de Hibernate, la zona horaria 'America/Mexico_City' y la activacion de visualizacion de consultas SQL formateadas "
        "para fines de depuracion y auditoria:"
    )
    add_code_block(
        doc,
        "server.port=8080\n\n"
        "spring.datasource.url=jdbc:mysql://localhost:3306/motocare_db?useSSL=false&serverTimezone=America/Mexico_City&allowPublicKeyRetrieval=true\n"
        "spring.datasource.username=root\n"
        "spring.datasource.password=953214\n"
        "spring.datasource.driver-class-name=com.mysql.cj.jdbc.Driver\n\n"
        "spring.jpa.hibernate.ddl-auto=update\n"
        "spring.jpa.show-sql=true\n"
        "spring.jpa.properties.hibernate.format_sql=true"
    )

    # ==================== SECCION 5 ====================
    add_h1("5. Ejecucion del Servidor y Despliegue Local")
    add_p(
        "El arranque del servidor se realizo mediante el wrapper oficial de Maven ('./mvnw spring-boot:run'). "
        "Durante el proceso de inicializacion se compilaron exitosamente las 7 clases fuente, se registraron las 2 interfaces JPA, "
        "se inicializo el pool de conexiones HikariPool y Tomcat embebido quedo activo en el puerto 8080 en tan solo 7.399 segundos."
    )

    add_image_figure(doc, "terminal_startup.png", "Figura 2: Consola de terminal mostrando el arranque exitoso de Spring Boot y Tomcat en el puerto 8080.")

    # ==================== SECCION 6 ====================
    add_h1("6. Pruebas y Verificacion de Endpoints en Postman")
    add_p(
        "Se creo y ejecuto la coleccion 'MotoCare API' en Postman, validando en orden riguroso cada una de las operaciones CRUD "
        "especificadas en el plan de implementacion."
    )

    # Subseccion 6.1
    add_h2("6.1 Operacion 1: Autenticacion de Usuario (Login)")
    add_p(
        "Metodo POST hacia 'http://localhost:8080/api/v1/auth/login'. Se enviaron las credenciales de prueba ('demo@motocare.com' / '123456'). "
        "El endpoint valido la coincidencia contra el registro en base de datos y retorno HTTP 200 OK junto con el objeto de usuario autenticado."
    )
    add_image_figure(doc, "postman_test1_login.png", "Figura 3: Ejecucion de prueba POST /api/v1/auth/login retornando HTTP 200 OK.")

    # Subseccion 6.2
    add_h2("6.2 Operacion 2: Listado de Servicios por Usuario")
    add_p(
        "Metodo GET hacia 'http://localhost:8080/api/v1/servicios/usuario/1'. El controlador invoco el metodo 'findByIdUsuarioOrderByFechaServicioDesc', "
        "obteniendo la lista con los 2 registros semilla ordenados cronologicamente de forma descendente (el servicio del 2026-11-26 primero, seguido del 2026-11-20)."
    )
    add_image_figure(doc, "postman_test2_get.png", "Figura 4: Ejecucion de prueba GET /api/v1/servicios/usuario/1 retornando HTTP 200 OK.")

    # Subseccion 6.3
    add_h2("6.3 Operacion 3: Creacion de Nuevo Registro de Servicio (POST)")
    add_p(
        "Metodo POST hacia 'http://localhost:8080/api/v1/servicios'. Se envio un payload JSON con un servicio de 'Cambio de llantas y balanceo' para el usuario 1. "
        "El servidor persistio la fila en MySQL y retorno HTTP 201 Created con el nuevo ID generado (id_servicio: 3)."
    )
    add_image_figure(doc, "postman_test3_post.png", "Figura 5: Ejecucion de prueba POST /api/v1/servicios retornando HTTP 201 Created con idServicio: 3.")

    # Subseccion 6.4
    add_h2("6.4 Operacion 4: Actualizacion de Registro de Servicio (PUT)")
    add_p(
        "Metodo PUT hacia 'http://localhost:8080/api/v1/servicios/3'. Se actualizo el estado del servicio a 'Completado' y se modificaron las observaciones tecnicas. "
        "El servidor ejecuto la sentencia UPDATE en MySQL y retorno HTTP 200 OK con los datos modificados."
    )
    add_image_figure(doc, "postman_test4_put.png", "Figura 6: Ejecucion de prueba PUT /api/v1/servicios/3 retornando HTTP 200 OK con estado 'Completado'.")

    # Subseccion 6.5
    add_h2("6.5 Operacion 5: Eliminacion de Registro de Servicio (DELETE)")
    add_p(
        "Metodo DELETE hacia 'http://localhost:8080/api/v1/servicios/3'. El servidor verifico la existencia del ID, elimino fisicamente el registro de la tabla "
        "'registros_servicio' y retorno HTTP 204 No Content con cuerpo vacio. Posteriormente, una consulta GET confirmo que el registro 3 ya no existe y "
        "unicamente permanecen los 2 registros semilla."
    )
    add_image_figure(doc, "postman_test5_delete.png", "Figura 7: Ejecucion de prueba DELETE /api/v1/servicios/3 retornando HTTP 204 No Content.")

    # ==================== SECCION 7 ====================
    add_h1("7. Control de Versiones y Flujo de Trabajo en GitHub")
    add_p(
        "Se implemento una estrategia de ramificacion formal basada en Git Flow para garantizar la trazabilidad de los cambios y el trabajo colaborativo:"
    )
    git_bullets = [
        "Rama 'main': Rama de produccion con el commit inicial y la documentacion tecnica general en README.md.",
        "Rama 'develop': Rama de integracion continua para preparacion de entregables e integracion del equipo.",
        "Rama 'feature/backend-api': Rama dedicada donde se desarrollaron los controladores, modelos, repositorios y scripts de la API REST.",
        "Pull Request #1: Abierto formalmente desde 'feature/backend-api' hacia 'develop' bajo la URL: https://github.com/IsaiasBrayanLopez/Sistema-de-Gesti-n-de-Mantenimiento-y-Servicios-para-Motocicletas-Veh-culos-MotoCare-/pull/1."
    ]
    for g in git_bullets:
        bp = doc.add_paragraph(style='List Bullet')
        bp.paragraph_format.space_before = Pt(1)
        bp.paragraph_format.space_after = Pt(2)
        brun = bp.add_run(g)
        brun.font.name = "Segoe UI"
        brun.font.size = Pt(9.5)
        brun.font.color.rgb = RGBColor(51, 65, 85)

    add_image_figure(doc, "github_pr.png", "Figura 8: Estado del Pull Request #1 en GitHub y trazabilidad de ramas remotas.")

    # ==================== SECCION 8 ====================
    add_h1("8. Checklist de Calidad y Criterios de Evaluacion")
    add_p("A continuacion se presenta la matriz de cumplimiento de los criterios de evaluacion de la Fase 2:")

    chk_tbl = doc.add_table(rows=6, cols=3)
    chk_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    chk_headers = ["Criterio de Evaluacion", "Estado", "Evidencia Tecnica"]
    for c_idx, h in enumerate(chk_headers):
        cell = chk_tbl.cell(0, c_idx)
        set_cell_background(cell, "1E3A8A")
        set_cell_margins(cell, top=100, bottom=100, left=100, right=100)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = p.add_run(h)
        run.bold = True
        run.font.name = "Segoe UI"
        run.font.size = Pt(9.5)
        run.font.color.rgb = RGBColor(255, 255, 255)

    chk_data = [
        ("Base de datos MySQL con esquema motocare_db y datos semilla", "CUMPLIDO", "Tablas 'usuarios' y 'registros_servicio' creadas con foreign keys. Script en docs/schema.sql."),
        ("Configuracion de application.properties con parametros exactos", "CUMPLIDO", "Conexion JDBC funcional a puerto 3306, zona horaria configurada y show-sql habilitado."),
        ("Entidades JPA y Repositorios sin ciclos infinitos de serializacion", "CUMPLIDO", "Mapeo desacoplado con idUsuario como clave escalar para garantizar compatibilidad con Jackson."),
        ("Controladores REST con soporte CORS y documentacion Javadoc", "CUMPLIDO", "Anotacion @CrossOrigin(origins = '*') presente en todos los controladores; metodos documentados."),
        ("Verificacion de 5 operaciones CRUD en Postman y exportacion JSON", "CUMPLIDO", "Respuestas 200, 201 y 204 validadas; coleccion guardada en docs/MotoCare_API.postman_collection.json.")
    ]

    for r_idx, (crit, st, ev) in enumerate(chk_data, start=1):
        bg = "F8FAFC" if r_idx % 2 == 1 else "FFFFFF"
        for c_idx, val in enumerate([crit, st, ev]):
            cell = chk_tbl.cell(r_idx, c_idx)
            set_cell_background(cell, bg)
            set_cell_margins(cell, top=80, bottom=80, left=90, right=90)
            p = cell.paragraphs[0]
            run = p.add_run(val)
            run.font.name = "Segoe UI"
            run.font.size = Pt(9)
            if c_idx == 1:
                run.bold = True
                run.font.color.rgb = RGBColor(34, 197, 94) # Green
            else:
                run.font.color.rgb = RGBColor(30, 41, 59)

    # ==================== SECCION 9 ====================
    add_h1("9. Conclusiones y Preparacion para la Fase 3")
    add_p(
        "La Fase 2 del proyecto MotoCare culmino de manera satisfactoria. La infraestructura del backend REST esta completamente "
        "operativa, conectada a la base de datos MySQL y rigurosamente probada. "
        "El diseno de endpoints sigue las mejores practicas de la industria (nombres en plural, codigos de estado HTTP estandar, payloads JSON ligeros). "
        "Con el servidor validado y la coleccion de Postman documentada, el proyecto se encuentra listo para iniciar la Fase 3, consistente en la "
        "integracion del cliente movil en Flutter (utilizando el paquete http o dio para el consumo de estos endpoints)."
    )

    # Save to both requested location and project backup
    doc.save(DOCX_OUTPUT_PATH)
    print(f"Report saved to user OneDrive Desktop: {DOCX_OUTPUT_PATH}")
    
    doc.save(DOCX_BACKUP_PATH)
    print(f"Report backup saved to: {DOCX_BACKUP_PATH}")

if __name__ == "__main__":
    build_report()
