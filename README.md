# Sistema-de-Gesti-n-de-Mantenimiento-y-Servicios-para-Motocicletas-Veh-culos-MotoCare-

## MotoCare API - Backend REST con Spring Boot y MySQL (Fase 2)

Servicio backend desarrollado en Java con Spring Boot para la gestion de mantenimiento preventivo y correctivo de motocicletas y vehiculos. Expone una interfaz RESTful que permite la autenticacion de usuarios y la administracion integral de los registros de servicio (CRUD), persistiendo la informacion en una base de datos relacional MySQL mediante Spring Data JPA.

---

## 1. Librerias del Backend y Justificacion Tecnica

| Dependencia | Identificador Maven | Proposito Tecnico | Donde se Aplica |
| :--- | :--- | :--- | :--- |
| **Spring Web (MVC)** | `spring-boot-starter-webmvc` | Expone endpoints REST, gestiona el servidor embebido Tomcat, procesa peticiones HTTP y serializa/deserializa objetos Java a JSON mediante Jackson. | Clases en el paquete `controllers/` (`@RestController`, `@RequestMapping`, `@CrossOrigin`). |
| **Spring Data JPA** | `spring-boot-starter-data-jpa` | Mapea clases Java a tablas SQL mediante Hibernate ORM y provee metodos CRUD automaticos y consultas derivadas por firma de metodo sin requerir SQL manual. | Entidades en `models/` (`@Entity`, `@Table`, `@Id`) e interfaces en `repositories/` (`JpaRepository`). |
| **MySQL Connector/J** | `mysql-connector-j` | Driver JDBC oficial de MySQL que establece y administra el canal de comunicacion TCP/IP y protocolos de conexion entre Java y el motor MySQL 8.x. | Configuracion de conexion de datasource en `src/main/resources/application.properties`. |
| **Spring Boot Validation** | `spring-boot-starter-validation` | Implementa Jakarta Bean Validation (Hibernate Validator) para validar campos obligatorios, restricciones de longitud y tipos numericos antes de la persistencia. | Atributos de modelos y parametros validados en controladores. |

---

## 2. Arquitectura y Flujo de Comunicacion

La aplicacion implementa un patron de arquitectura por capas con desacoplamiento entre presentacion, logica de persistencia y almacenamiento:

```
[Cliente: Postman / Flutter Mobile]
             |
             | (HTTP JSON / REST)
             v
[Controllers: AuthController / ServicioController]
             |
             | (Inyeccion de Dependencias / DTOs / Entidades)
             v
[Repositories: UsuarioRepository / RegistroServicioRepository (Spring Data JPA)]
             |
             | (Hibernate ORM / Dialecto MySQL / Pool HikariCP)
             v
[Driver JDBC: MySQL Connector/J]
             |
             | (TCP/IP Port 3306)
             v
[Base de Datos: MySQL 8.0 - motocare_db]
```

### Por que se eligio Spring Data JPA
1. **Abstraccion de alto nivel**: Elimina el codigo repetitivo (boilerplate) de aperturas de conexion JDBC, preparacion de sentencias (`PreparedStatement`) y mapeo manual de `ResultSet`.
2. **Generacion de consultas por convencion**: Metodos como `findByIdUsuarioOrderByFechaServicioDesc(Integer idUsuario)` son traducidos a consultas SQL optimizadas de manera automatica por Spring Data.
3. **Mantenibilidad y tipado fuerte**: Cualquier cambio en la estructura de una entidad se refleja de inmediato en tiempo de compilacion, reduciendo errores de sintaxis SQL en tiempo de ejecucion.
4. **Pool de conexiones HikariCP integrado**: Optimiza el rendimiento gestionando un pool eficiente de conexiones reutilizables hacia el motor MySQL.

---

## 3. Configuracion de Base de Datos (`application.properties`)

Ubicacion del archivo: `src/main/resources/application.properties`

```properties
server.port=8080

spring.datasource.url=jdbc:mysql://localhost:3306/motocare_db?useSSL=false&serverTimezone=America/Mexico_City&allowPublicKeyRetrieval=true
spring.datasource.username=root
spring.datasource.password=TU_CONTRASEÑA_MYSQL
spring.datasource.driver-class-name=com.mysql.cj.jdbc.Driver

spring.jpa.hibernate.ddl-auto=update
spring.jpa.show-sql=true
spring.jpa.properties.hibernate.format_sql=true
```

---

## 4. Esquema Relacional de Base de Datos (`schema.sql`)

El esquema consta de dos tablas con integridad referencial garantizada por una clave foranea con eliminacion en cascada (`ON DELETE CASCADE`):

```sql
CREATE DATABASE IF NOT EXISTS motocare_db;
USE motocare_db;

CREATE TABLE IF NOT EXISTS usuarios (
    id_usuario INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS registros_servicio (
    id_servicio INT AUTO_INCREMENT PRIMARY KEY,
    id_usuario INT NOT NULL,
    tipo_servicio VARCHAR(80) NOT NULL,
    kilometraje INT NOT NULL,
    costo DECIMAL(10,2) NOT NULL,
    fecha_servicio DATE NOT NULL,
    proximo_kilometraje INT NOT NULL,
    estado VARCHAR(20) DEFAULT 'Pendiente',
    observaciones TEXT,
    CONSTRAINT fk_usuario FOREIGN KEY (id_usuario)
        REFERENCES usuarios(id_usuario) ON DELETE CASCADE
);

-- Datos semilla para pruebas de lectura iniciales
INSERT INTO usuarios (nombre, email, password_hash)
VALUES ('Usuario Prueba', 'demo@motocare.com', '123456');

INSERT INTO registros_servicio
(id_usuario, tipo_servicio, kilometraje, costo, fecha_servicio, proximo_kilometraje, estado, observaciones)
VALUES
(1, 'Cambio de aceite', 12000, 450.00, '2026-11-20', 15000, 'Completado', 'Aceite sintetico 10W-40'),
(1, 'Ajuste de frenos', 12500, 280.00, '2026-11-26', 17500, 'Pendiente', 'Revision de balatas delanteras');
```

---

## 5. Endpoints REST Verificados

Todos los endpoints han sido validados exitosamente en Postman con soporte CORS habilitado mediante `@CrossOrigin(origins = "*")`:

| Operacion | Metodo | Endpoint | Codigo HTTP | Descripcion / Payload |
| :--- | :--- | :--- | :--- | :--- |
| **Login** | `POST` | `/api/v1/auth/login` | `200 OK` | Valida credenciales (`email`, `password`) y retorna los datos del usuario autenticado. |
| **Registro** | `POST` | `/api/v1/auth/register` | `201 Created` | Registra un nuevo usuario verificando que el email sea unico (`409 Conflict` si ya existe). |
| **Listar Servicios** | `GET` | `/api/v1/servicios/usuario/{idUsuario}` | `200 OK` | Lista todos los servicios del usuario ordenados descendentemente por fecha. |
| **Crear Servicio** | `POST` | `/api/v1/servicios` | `201 Created` | Inserta un nuevo registro de servicio en la base de datos y retorna el objeto con su ID generado. |
| **Actualizar Servicio** | `PUT` | `/api/v1/servicios/{id}` | `200 OK` | Actualiza los datos de un registro de servicio existente (`404 Not Found` si no existe). |
| **Eliminar Servicio** | `DELETE` | `/api/v1/servicios/{id}` | `204 No Content` | Elimina fisicamente el registro de servicio indicado (`404 Not Found` si no existe). |

### Ejemplos de Cargas Utiles (Payloads)

#### 1. POST `/api/v1/auth/login`
```json
{
    "email": "demo@motocare.com",
    "password": "123456"
}
```
Respuesta `200 OK`:
```json
{
    "idUsuario": 1,
    "nombre": "Usuario Prueba",
    "email": "demo@motocare.com",
    "passwordHash": "123456"
}
```

#### 2. POST `/api/v1/servicios`
```json
{
    "idUsuario": 1,
    "tipoServicio": "Cambio de llantas y balanceo",
    "kilometraje": 13000,
    "costo": 1200.00,
    "fechaServicio": "2026-11-27",
    "proximoKilometraje": 20000,
    "estado": "Pendiente",
    "observaciones": "Llantas Michelin Pilot Street"
}
```
Respuesta `201 Created`:
```json
{
    "idServicio": 3,
    "idUsuario": 1,
    "tipoServicio": "Cambio de llantas y balanceo",
    "kilometraje": 13000,
    "costo": 1200.00,
    "fechaServicio": "2026-11-27",
    "proximoKilometraje": 20000,
    "estado": "Pendiente",
    "observaciones": "Llantas Michelin Pilot Street"
}
```

---

## 6. Estructura del Proyecto

```
c:/Users/isaia/Desktop/Proyecto_Desarrollo_Movil_3/
├── .mvn/
│   └── wrapper/
│       ├── maven-wrapper.jar
│       └── maven-wrapper.properties
├── docs/
│   ├── MotoCare_API.postman_collection.json
│   └── schema.sql
├── src/
│   ├── main/
│   │   ├── java/
│   │   │   └── com/
│   │   │       └── motocare/
│   │   │           └── api/
│   │   │               ├── ApiApplication.java
│   │   │               ├── controllers/
│   │   │               │   ├── AuthController.java
│   │   │               │   └── ServicioController.java
│   │   │               ├── models/
│   │   │               │   ├── RegistroServicio.java
│   │   │               │   └── Usuario.java
│   │   │               └── repositories/
│   │   │                   ├── RegistroServicioRepository.java
│   │   │                   └── UsuarioRepository.java
│   │   └── resources/
│   │       └── application.properties
│   └── test/
│       └── java/
│           └── com/
│               └── motocare/
│                   └── api/
│                       └── ApiApplicationTests.java
├── mvnw
├── mvnw.cmd
├── pom.xml
└── README.md
```

---

## 7. Instrucciones de Ejecucion Local

1. **Requisitos Previos**:
   - Java Development Kit (JDK 17, 21 o 25).
   - Servicio de MySQL activo en el puerto 3306.

2. **Crear la Base de Datos**:
   Ejecutar el script `docs/schema.sql` en MySQL Workbench o desde linea de comandos:
   ```bash
   mysql -u root -p < docs/schema.sql
   ```

3. **Iniciar el Servidor**:
   ```powershell
   ./mvnw spring-boot:run
   ```

4. **Importar y Probar en Postman**:
   - Abrir Postman -> Click en `Import`.
   - Seleccionar el archivo `docs/MotoCare_API.postman_collection.json`.
   - Ejecutar las 5 peticiones configuradas.
