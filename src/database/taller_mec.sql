-- --------------------------------------------------------
-- Host:                         127.0.0.1
-- Versión del servidor:         8.0.30 - MySQL Community Server - GPL
-- SO del servidor:              Win64
-- HeidiSQL Versión:             12.1.0.6537
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


-- Volcando estructura de base de datos para ganadera
CREATE DATABASE IF NOT EXISTS `ganadera` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `ganadera`;

-- Volcando estructura para tabla ganadera.actions_users
CREATE TABLE IF NOT EXISTS `actions_users` (
  `fech` datetime NOT NULL COMMENT 'En minutos 00 y segundos 00',
  `ses_id` int NOT NULL DEFAULT '0' COMMENT 'ID de la session sobre la que se esta realizando esta acción',
  `action` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT 'Qué acción hizo',
  PRIMARY KEY (`fech`),
  UNIQUE KEY `ses_id` (`ses_id`),
  CONSTRAINT `FK_actions_users_session` FOREIGN KEY (`ses_id`) REFERENCES `session` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- La exportación de datos fue deseleccionada.

-- Volcando estructura para tabla ganadera.actividades
CREATE TABLE IF NOT EXISTS `actividades` (
  `id` int NOT NULL AUTO_INCREMENT,
  `rfc_cap` varchar(13) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT 'RFC de la persona que asigno la tarea',
  `rfc_jor` varchar(13) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT 'RFC del empleado al que se le asigno la tarea',
  `titulo` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT 'Nombre de la actividad. Ejemplo: Limpieza de zona, rellenar biberes',
  `desc` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT 'Descripción de la tarea por si se necesitan más indicaciones',
  `fech_in` datetime NOT NULL COMMENT 'Fecha de inicio de la tarea en Dia y hora',
  `fech_fi` datetime NOT NULL COMMENT 'Fecha maximo de finalización',
  `estado` int NOT NULL DEFAULT '0' COMMENT '0 = Pendiente, 1 = Completada, 2 = Verificada, 3 = Inconcluso',
  `observ` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci COMMENT 'Si hubo algun problema aqui se describe',
  PRIMARY KEY (`id`),
  KEY `FK_actividades_personas` (`rfc_cap`),
  KEY `FK_actividades_personas_2` (`rfc_jor`),
  CONSTRAINT `FK_actividades_personas` FOREIGN KEY (`rfc_cap`) REFERENCES `personas` (`rfc`),
  CONSTRAINT `FK_actividades_personas_2` FOREIGN KEY (`rfc_jor`) REFERENCES `personas` (`rfc`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- La exportación de datos fue deseleccionada.

-- Volcando estructura para tabla ganadera.alertas
CREATE TABLE IF NOT EXISTS `alertas` (
  `id` int NOT NULL AUTO_INCREMENT,
  `titulo` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `descrip` varchar(150) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `estatus` tinyint NOT NULL DEFAULT '1',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- La exportación de datos fue deseleccionada.

-- Volcando estructura para tabla ganadera.alimentos
CREATE TABLE IF NOT EXISTS `alimentos` (
  `id` int NOT NULL,
  `nombre` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT 'Nombre del alimento (heno, grano, etc.)',
  `tipo` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT 'Tipo de alimento (forraje, concentrado, suplemento)',
  `calorias` double NOT NULL COMMENT 'Nivel de energía (kcal/kg)',
  `costo_kg_lt` double NOT NULL COMMENT 'Costo por kilogramo',
  PRIMARY KEY (`id`),
  KEY `idx_alimentos_nombre` (`nombre`),
  KEY `idx_alimentos_tipo` (`tipo`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- La exportación de datos fue deseleccionada.

-- Volcando estructura para tabla ganadera.animales
CREATE TABLE IF NOT EXISTS `animales` (
  `id` int NOT NULL,
  `nombre` double NOT NULL,
  `especie` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `raza_id` int NOT NULL,
  `sexo` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT 'M, H',
  `finca_id` int DEFAULT NULL COMMENT 'Relación con la finca donde está el ganado',
  `fech` date NOT NULL COMMENT 'Fecha de nacimiento del animal',
  `estado` int NOT NULL COMMENT '1 = Sano, 2 = Vendido, 3 = Muerto',
  `externo` tinyint(1) NOT NULL COMMENT 'FALSE = Interno, TRUE = Externo',
  `corral_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `FK_animales_razas` (`raza_id`),
  KEY `FK_animales_fincas` (`finca_id`),
  KEY `FK_animales_corrales` (`corral_id`),
  CONSTRAINT `FK_animales_corrales` FOREIGN KEY (`corral_id`) REFERENCES `corrales` (`id`),
  CONSTRAINT `FK_animales_fincas` FOREIGN KEY (`finca_id`) REFERENCES `fincas` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- La exportación de datos fue deseleccionada.

-- Volcando estructura para tabla ganadera.asistencias
CREATE TABLE IF NOT EXISTS `asistencias` (
  `id` int NOT NULL AUTO_INCREMENT,
  `rfc_emp` varchar(13) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT 'Relación con el empleado',
  `hora_entrada` time DEFAULT NULL COMMENT 'Hora de entrada registrada',
  `hora_salida` time DEFAULT NULL COMMENT 'Hora de salida registrada',
  `fechentra` date DEFAULT NULL,
  `fecsalida` date DEFAULT NULL,
  `estado` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `FK_asistencias_empleados` (`rfc_emp`),
  CONSTRAINT `FK_asistencias_empleados` FOREIGN KEY (`rfc_emp`) REFERENCES `empleados` (`rfc`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- La exportación de datos fue deseleccionada.

-- Volcando estructura para tabla ganadera.beneficios
CREATE TABLE IF NOT EXISTS `beneficios` (
  `id` int NOT NULL,
  `nombre` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT 'Nombre del beneficio (seguro médico, bonos, etc.)',
  `desc` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci COMMENT 'Descripción del beneficio',
  PRIMARY KEY (`id`),
  KEY `idx_beneficios_nombre` (`nombre`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- La exportación de datos fue deseleccionada.

-- Volcando estructura para tabla ganadera.colonias
CREATE TABLE IF NOT EXISTS `colonias` (
  `id` int NOT NULL AUTO_INCREMENT,
  `mun_id` int DEFAULT NULL,
  `nom` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `ciud` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `asen` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `cp` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `FK_colonias_municipios` (`mun_id`),
  CONSTRAINT `FK_colonias_municipios` FOREIGN KEY (`mun_id`) REFERENCES `municipios` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1607710190 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- La exportación de datos fue deseleccionada.

-- Volcando estructura para tabla ganadera.companies
CREATE TABLE IF NOT EXISTS `companies` (
  `rfc_comp` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '',
  `logo_path` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '/companies/default-logo.jpg',
  `nom` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `tel` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '',
  `des` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `sm_face` varchar(150) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `sm_x` varchar(150) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `sm_sw` varchar(150) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `id_colonia` int DEFAULT NULL,
  PRIMARY KEY (`rfc_comp`),
  KEY `FK_companies_colonias` (`id_colonia`),
  CONSTRAINT `FK_companies_colonias` FOREIGN KEY (`id_colonia`) REFERENCES `colonias` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- La exportación de datos fue deseleccionada.

-- Volcando estructura para tabla ganadera.compras_ganados
CREATE TABLE IF NOT EXISTS `compras_ganados` (
  `id` int NOT NULL,
  `rfc_prov` varchar(13) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT 'Relación con la tabla Proveedores, indica el proveedor',
  `no_arete` int DEFAULT NULL,
  `comp_pago` blob NOT NULL COMMENT 'Comprobante de pago, almacenado como un objeto binario (blob)',
  `fech` date DEFAULT NULL COMMENT 'Fecha en la que se realizo la compra',
  `precio_kg` double NOT NULL COMMENT 'Precio por kilogramo del ganado',
  `peso` double NOT NULL COMMENT 'Peso del ganado al momento de la compra',
  `estatus` int NOT NULL DEFAULT '1' COMMENT 'Estatus de la compra: 1 = Pendiente, 2 = Pagada, 3 = Cancelada',
  `observ` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci COMMENT 'Comentarios adicionales sobre la compra',
  PRIMARY KEY (`id`),
  KEY `FK_compras_ganados_personas` (`rfc_prov`),
  KEY `FK_compras_ganados_ganados` (`no_arete`),
  CONSTRAINT `FK_compras_ganados_ganados` FOREIGN KEY (`no_arete`) REFERENCES `ganados` (`animal_id`),
  CONSTRAINT `FK_compras_ganados_personas` FOREIGN KEY (`rfc_prov`) REFERENCES `personas` (`rfc`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- La exportación de datos fue deseleccionada.

-- Volcando estructura para tabla ganadera.compras_insumos
CREATE TABLE IF NOT EXISTS `compras_insumos` (
  `id` int NOT NULL COMMENT 'Identificador único de la compra de insumos',
  `tipo` int NOT NULL COMMENT '0 = Medicamentos, 1 = Alimentos',
  `rfc_prov` varchar(13) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT 'Relación con la tabla Proveedores, indica el proveedor',
  `fech` date NOT NULL COMMENT 'Fecha en la que se realizó la compra',
  `cantidad` int NOT NULL COMMENT 'Cantidad de insumos comprados',
  `precio_u` double NOT NULL COMMENT 'Precio por unidad del insumo',
  `estatus` int NOT NULL DEFAULT '1' COMMENT 'Estatus de la compra: 1 = Pendiente, 2 = Pagada, 3 = Cancelada',
  `observ` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci COMMENT 'Comentarios adicionales sobre la compra',
  PRIMARY KEY (`id`),
  KEY `FK_compras_insumos_personas` (`rfc_prov`),
  CONSTRAINT `FK_compras_insumos_personas` FOREIGN KEY (`rfc_prov`) REFERENCES `personas` (`rfc`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- La exportación de datos fue deseleccionada.

-- Volcando estructura para tabla ganadera.config_puestos
CREATE TABLE IF NOT EXISTS `config_puestos` (
  `id` int NOT NULL AUTO_INCREMENT,
  `id_puesto` int DEFAULT NULL,
  `salario_base` double NOT NULL,
  `dias_lab` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `h_ent` time NOT NULL,
  `h_sal` time NOT NULL,
  `rfc_comp` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `FK_config_puestos_companies` (`rfc_comp`),
  KEY `FK_config_puestos_puestos` (`id_puesto`),
  CONSTRAINT `FK_config_puestos_companies` FOREIGN KEY (`rfc_comp`) REFERENCES `companies` (`rfc_comp`),
  CONSTRAINT `FK_config_puestos_puestos` FOREIGN KEY (`id_puesto`) REFERENCES `puestos` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- La exportación de datos fue deseleccionada.

-- Volcando estructura para tabla ganadera.consumo
CREATE TABLE IF NOT EXISTS `consumo` (
  `raza_id` int NOT NULL COMMENT 'Relación con la tabla Razas',
  `alimento_id` int NOT NULL COMMENT 'Relación con la tabla Alimentos, indica el alimento consumido',
  `fecha` date NOT NULL COMMENT 'Fecha en que se registró el consumo',
  `cantidad_kg` double NOT NULL COMMENT 'Cantidad de alimento consumido, en kilogramos (kg)',
  PRIMARY KEY (`raza_id`),
  KEY `FK_consumo_alimentos` (`alimento_id`),
  CONSTRAINT `FK_consumo_alimentos` FOREIGN KEY (`alimento_id`) REFERENCES `alimentos` (`id`),
  CONSTRAINT `FK_consumo_razas` FOREIGN KEY (`raza_id`) REFERENCES `razas` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- La exportación de datos fue deseleccionada.

-- Volcando estructura para tabla ganadera.corrales
CREATE TABLE IF NOT EXISTS `corrales` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nom` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `id_finca` int NOT NULL,
  `rfc_comp` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  PRIMARY KEY (`id`),
  KEY `FK__fincas` (`id_finca`),
  KEY `FK__companies` (`rfc_comp`),
  CONSTRAINT `FK__companies` FOREIGN KEY (`rfc_comp`) REFERENCES `companies` (`rfc_comp`),
  CONSTRAINT `FK__fincas` FOREIGN KEY (`id_finca`) REFERENCES `fincas` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- La exportación de datos fue deseleccionada.

-- Volcando estructura para tabla ganadera.empleados
CREATE TABLE IF NOT EXISTS `empleados` (
  `rfc` varchar(13) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT 'Relación con la tabla Personas',
  `puesto_id` int NOT NULL COMMENT 'Relación con el puesto del empleado',
  `finca_id` int NOT NULL COMMENT 'Relación con la finca donde trabaja',
  `fecha_con` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'Fecha en la que fue contratado',
  `estatus` int NOT NULL DEFAULT '1' COMMENT '1 = Activo, 2 = Vacaciones, 3 = Despedido, 4 = Renunciado',
  `turno` int DEFAULT '0' COMMENT '0 = Mañana 1 = Tarde 2 = Noche',
  `rfc_comp` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  PRIMARY KEY (`rfc`),
  KEY `FK_empleados_puestos` (`puesto_id`),
  KEY `FK_empleados_fincas` (`finca_id`),
  KEY `FK_empleados_companies` (`rfc_comp`),
  CONSTRAINT `FK_empleados_companies` FOREIGN KEY (`rfc_comp`) REFERENCES `companies` (`rfc_comp`),
  CONSTRAINT `FK_empleados_fincas` FOREIGN KEY (`finca_id`) REFERENCES `fincas` (`id`),
  CONSTRAINT `FK_empleados_personas` FOREIGN KEY (`rfc`) REFERENCES `personas` (`rfc`),
  CONSTRAINT `FK_empleados_puestos` FOREIGN KEY (`puesto_id`) REFERENCES `puestos` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- La exportación de datos fue deseleccionada.

-- Volcando estructura para tabla ganadera.empleado_beneficios
CREATE TABLE IF NOT EXISTS `empleado_beneficios` (
  `id` int NOT NULL,
  `rfc_emp` varchar(13) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT 'Relación con el empleado',
  `benef_id` int NOT NULL COMMENT 'Relación con el beneficio',
  `fecha_inicio` date NOT NULL COMMENT 'Fecha de inicio del beneficio',
  `fecha_fin` date NOT NULL COMMENT 'Fecha de finalización del beneficio (opcional)',
  PRIMARY KEY (`id`),
  KEY `FK_empleado_beneficios_empleados` (`rfc_emp`),
  KEY `FK_empleado_beneficios_beneficios` (`benef_id`),
  CONSTRAINT `FK_empleado_beneficios_beneficios` FOREIGN KEY (`benef_id`) REFERENCES `beneficios` (`id`),
  CONSTRAINT `FK_empleado_beneficios_empleados` FOREIGN KEY (`rfc_emp`) REFERENCES `empleados` (`rfc`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- La exportación de datos fue deseleccionada.

-- Volcando estructura para tabla ganadera.enfermedades
CREATE TABLE IF NOT EXISTS `enfermedades` (
  `id` int NOT NULL,
  `nombre` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT 'Nombre de la enfermedad',
  `tratam_id` int DEFAULT NULL,
  `mod_transm` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT 'Contacto, alimento, aire, etc.',
  `prev` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT 'Medidas para evitar la enfermedad',
  `gravedad` int NOT NULL COMMENT 'TRUE = Reversible con tratamiento, FALSE = Permanente',
  `sintoma` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT 'Nombre del síntoma (Ejemplo: Fiebre, Pérdida de apetito)',
  PRIMARY KEY (`id`),
  KEY `FK_enfermedades_tratamientos` (`tratam_id`),
  CONSTRAINT `FK_enfermedades_tratamientos` FOREIGN KEY (`tratam_id`) REFERENCES `tratamientos` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- La exportación de datos fue deseleccionada.

-- Volcando estructura para tabla ganadera.estados
CREATE TABLE IF NOT EXISTS `estados` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nom` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `pais_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `FK_estados_paises` (`pais_id`),
  CONSTRAINT `FK_estados_paises` FOREIGN KEY (`pais_id`) REFERENCES `paises` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=33 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- La exportación de datos fue deseleccionada.

-- Volcando estructura para tabla ganadera.fincas
CREATE TABLE IF NOT EXISTS `fincas` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT 'Nombre de la finca',
  `capacidad` int NOT NULL COMMENT 'Número de ganados en la camada',
  `descrip` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci COMMENT 'Descripción adicional',
  `id_colonia` int NOT NULL COMMENT 'Dirección o coordenadas',
  `rfc_comp` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  PRIMARY KEY (`id`),
  KEY `FK_fincas_colonias` (`id_colonia`),
  KEY `FK_fincas_companies` (`rfc_comp`),
  CONSTRAINT `FK_fincas_colonias` FOREIGN KEY (`id_colonia`) REFERENCES `colonias` (`id`),
  CONSTRAINT `FK_fincas_companies` FOREIGN KEY (`rfc_comp`) REFERENCES `companies` (`rfc_comp`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- La exportación de datos fue deseleccionada.

-- Volcando estructura para tabla ganadera.ganados
CREATE TABLE IF NOT EXISTS `ganados` (
  `animal_id` int NOT NULL COMMENT 'ID del animal -> Número de arete',
  `tipo` int DEFAULT NULL COMMENT '0=Leche, 1=Carne, 2=Trabajo, 3=Reproducción',
  PRIMARY KEY (`animal_id`),
  CONSTRAINT `FK_ganados_animales` FOREIGN KEY (`animal_id`) REFERENCES `animales` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- La exportación de datos fue deseleccionada.

-- Volcando estructura para tabla ganadera.incidentes
CREATE TABLE IF NOT EXISTS `incidentes` (
  `id` int NOT NULL,
  `animal_id` int NOT NULL COMMENT 'Relación con el ganado',
  `fech` date NOT NULL COMMENT 'Fecha en la que ocurrió el incidente',
  `tipo` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT 'Tipo de incidente (enfermedad, fractura, fallecimiento, etc.)',
  `enferm_id` int DEFAULT NULL COMMENT 'Relación con la enfermedad (si aplica)',
  `observ` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci COMMENT 'Comentarios adicionales',
  PRIMARY KEY (`id`),
  KEY `FK_incidentes_enfermedades` (`enferm_id`),
  CONSTRAINT `FK_incidentes_enfermedades` FOREIGN KEY (`enferm_id`) REFERENCES `enfermedades` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- La exportación de datos fue deseleccionada.

-- Volcando estructura para tabla ganadera.medicamentos
CREATE TABLE IF NOT EXISTS `medicamentos` (
  `id` int NOT NULL COMMENT 'Identificador único de la vacuna o desparasitación',
  `rfc_prov` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT 'Nombre del laboratorio que produce la vacuna o desparasitación',
  `nom` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT 'Nombre del medicamento',
  `enf_id` int NOT NULL COMMENT 'Relación con la tabla Enfermedades, indica la enfermedad que previene',
  `marca` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT 'Nombre de la marca que produce el medicamento',
  `dur` int NOT NULL COMMENT 'Duración de la inmunidad en meses',
  `unid` int NOT NULL COMMENT 'Unidades disponibles',
  `cont` double NOT NULL,
  `via_adm` int NOT NULL COMMENT 'Vía de administración: 0=Intramuscular, 1=Subcutánea, 2=Oral',
  `desc` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci COMMENT 'Descripción adicional de la vacuna o desparasitación',
  PRIMARY KEY (`id`),
  KEY `FK_medicamentos_personas` (`rfc_prov`),
  KEY `FK_medicamentos_enfermedades` (`enf_id`),
  CONSTRAINT `FK_medicamentos_enfermedades` FOREIGN KEY (`enf_id`) REFERENCES `enfermedades` (`id`),
  CONSTRAINT `FK_medicamentos_personas` FOREIGN KEY (`rfc_prov`) REFERENCES `personas` (`rfc`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- La exportación de datos fue deseleccionada.

-- Volcando estructura para tabla ganadera.municipios
CREATE TABLE IF NOT EXISTS `municipios` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nom` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `est_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `idx_municipios_estado_id` (`est_id`) USING BTREE,
  CONSTRAINT `FK_municipios_estados` FOREIGN KEY (`est_id`) REFERENCES `estados` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=32059 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- La exportación de datos fue deseleccionada.

-- Volcando estructura para tabla ganadera.pagos
CREATE TABLE IF NOT EXISTS `pagos` (
  `no_ref` int NOT NULL,
  `rfc_emp` varchar(13) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT 'Relación con el empleado',
  `fecha_pago` date NOT NULL COMMENT 'Fecha del pago',
  `monto` double NOT NULL COMMENT 'Monto pagado',
  `metodo_pago` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT 'Método de pago (efectivo, transferencia, etc.)',
  `observ` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci COMMENT 'Comentarios adicionales',
  PRIMARY KEY (`no_ref`),
  KEY `FK_pagos_personas` (`rfc_emp`),
  CONSTRAINT `FK_pagos_personas` FOREIGN KEY (`rfc_emp`) REFERENCES `personas` (`rfc`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- La exportación de datos fue deseleccionada.

-- Volcando estructura para tabla ganadera.paises
CREATE TABLE IF NOT EXISTS `paises` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nom` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- La exportación de datos fue deseleccionada.

-- Volcando estructura para tabla ganadera.personas
CREATE TABLE IF NOT EXISTS `personas` (
  `rfc` varchar(13) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `nombre` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `correo` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `app` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `apm` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `fech_nac` date NOT NULL,
  `sex` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `tel` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `id_colonia` int NOT NULL,
  PRIMARY KEY (`rfc`),
  UNIQUE KEY `correo` (`correo`),
  KEY `FK_personas_colonias` (`id_colonia`),
  CONSTRAINT `FK_personas_colonias` FOREIGN KEY (`id_colonia`) REFERENCES `colonias` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- La exportación de datos fue deseleccionada.

-- Volcando estructura para tabla ganadera.puestos
CREATE TABLE IF NOT EXISTS `puestos` (
  `id` int NOT NULL,
  `nombre` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT 'Nombre del puesto (Ejemplo: Veterinario, Cuidador, Administrador)',
  `descripcion` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci COMMENT 'Descripción del puesto',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- La exportación de datos fue deseleccionada.

-- Volcando estructura para tabla ganadera.razas
CREATE TABLE IF NOT EXISTS `razas` (
  `id` int NOT NULL,
  `nom` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT 'Nombre de la raza',
  `img` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '' COMMENT 'Imagen representativa de la raza',
  `desc` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT 'Descripción de la raza del animal',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- La exportación de datos fue deseleccionada.

-- Volcando estructura para tabla ganadera.revisiones
CREATE TABLE IF NOT EXISTS `revisiones` (
  `id` int NOT NULL,
  `rfc_vet` varchar(13) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `no_arete` int NOT NULL,
  `peso` double NOT NULL,
  `frec_card` int NOT NULL,
  `temp_corp` float NOT NULL,
  `fech` datetime NOT NULL,
  `observ` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  PRIMARY KEY (`id`),
  KEY `FK_revisiones_personas` (`rfc_vet`),
  KEY `FK_revisiones_ganados` (`no_arete`),
  CONSTRAINT `FK_revisiones_ganados` FOREIGN KEY (`no_arete`) REFERENCES `ganados` (`animal_id`),
  CONSTRAINT `FK_revisiones_personas` FOREIGN KEY (`rfc_vet`) REFERENCES `personas` (`rfc`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- La exportación de datos fue deseleccionada.

-- Volcando estructura para tabla ganadera.session
CREATE TABLE IF NOT EXISTS `session` (
  `id` int NOT NULL COMMENT 'rfc + fecha DD-MM-YY_HH-MM-SS',
  `rfc` varchar(13) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT 'RFC del usuario que accedio al sistema',
  `fech_in` datetime NOT NULL COMMENT 'Fecha y hora que incio la session',
  `fech_fin` datetime DEFAULT NULL COMMENT 'Fecha y hora que vencio la session',
  PRIMARY KEY (`id`),
  UNIQUE KEY `rfc` (`rfc`),
  CONSTRAINT `FK_session_personas` FOREIGN KEY (`rfc`) REFERENCES `personas` (`rfc`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- La exportación de datos fue deseleccionada.

-- Volcando estructura para tabla ganadera.tratamientos
CREATE TABLE IF NOT EXISTS `tratamientos` (
  `id` int NOT NULL,
  `nombre` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT 'Nombre del tratamiento',
  `instrucciones` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci COMMENT 'Cómo aplicar el tratamiento',
  `duracion` int NOT NULL COMMENT 'Duración en días',
  `observaciones` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci COMMENT 'Información adicional',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- La exportación de datos fue deseleccionada.

-- Volcando estructura para tabla ganadera.usuarios
CREATE TABLE IF NOT EXISTS `usuarios` (
  `rfc` varchar(13) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `pass` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `rol` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '-1 SUPERUSER, 0 = DUEÑO, 1 = CONTABILIDAD, 2 = Capataz, 3 = Jornalero, 4 = Veterinario',
  `created` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'Fecha y hora en que se creo el usuario',
  `last_session` datetime DEFAULT NULL COMMENT 'Último inicio de sesión',
  `rfc_comp` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '',
  PRIMARY KEY (`rfc`),
  KEY `FK_usuarios_companies` (`rfc_comp`) USING BTREE,
  CONSTRAINT `FK_usuarios_companies` FOREIGN KEY (`rfc_comp`) REFERENCES `companies` (`rfc_comp`),
  CONSTRAINT `FK_usuarios_personas` FOREIGN KEY (`rfc`) REFERENCES `personas` (`rfc`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- La exportación de datos fue deseleccionada.

-- Volcando estructura para tabla ganadera.vacunaciones
CREATE TABLE IF NOT EXISTS `vacunaciones` (
  `id` int NOT NULL,
  `fech` date NOT NULL COMMENT 'Fecha de aplicación de la vacuna',
  `rfc_vet` varchar(13) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT 'Nombre del veterinario o encargado',
  `no_arete` int NOT NULL COMMENT 'Relación con la tabla Ganados',
  `med_id` int NOT NULL COMMENT 'Relación con la tabla Vacunas',
  `prox_dosis` date NOT NULL COMMENT 'Fecha programada para la siguiente dosis',
  `obs` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci COMMENT 'Observaciones o notas adicionales',
  PRIMARY KEY (`id`),
  KEY `idx_vacunaciones_rfc_vet` (`rfc_vet`),
  KEY `idx_vacunaciones_no_arete` (`no_arete`),
  KEY `idx_vacunaciones_med_id` (`med_id`),
  KEY `idx_vacunaciones_prox_dosis` (`prox_dosis`),
  CONSTRAINT `FK_vacunaciones_ganados` FOREIGN KEY (`no_arete`) REFERENCES `ganados` (`animal_id`),
  CONSTRAINT `FK_vacunaciones_medicamentos` FOREIGN KEY (`med_id`) REFERENCES `medicamentos` (`id`),
  CONSTRAINT `FK_vacunaciones_personas` FOREIGN KEY (`rfc_vet`) REFERENCES `personas` (`rfc`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- La exportación de datos fue deseleccionada.

-- Volcando estructura para tabla ganadera.ventas
CREATE TABLE IF NOT EXISTS `ventas` (
  `no_venta` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT 'Clave combinada formada por [rfc_comprador]+[no_arete]',
  `no_arete` int NOT NULL COMMENT 'Relación con la tabla Ganados, indica el ganado vendido',
  `rfc_comp` varchar(13) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT 'RFC del comprador',
  `rfc_ven` varchar(13) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT 'RFC del vendedor',
  `fech` date NOT NULL COMMENT 'Fecha en la que se realizó la venta',
  `prec_kg` double NOT NULL COMMENT 'Precio por kg de peso del ganado',
  `peso` double NOT NULL COMMENT 'Peso del ganado al momento de la venta',
  `met_pago` int NOT NULL COMMENT 'Método de pago: 0 = Efectivo, 1 = Transferencia, 2 = Tarjeta',
  `observ` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci COMMENT 'Comentarios adicionales sobre la venta',
  PRIMARY KEY (`no_venta`),
  UNIQUE KEY `no_arete` (`no_arete`),
  KEY `FK_ventas_personas` (`rfc_comp`),
  KEY `FK_ventas_personas_2` (`rfc_ven`),
  CONSTRAINT `FK_ventas_personas` FOREIGN KEY (`rfc_comp`) REFERENCES `personas` (`rfc`),
  CONSTRAINT `FK_ventas_personas_2` FOREIGN KEY (`rfc_ven`) REFERENCES `personas` (`rfc`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- La exportación de datos fue deseleccionada.

/*!40103 SET TIME_ZONE=IFNULL(@OLD_TIME_ZONE, 'system') */;
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;
