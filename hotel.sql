-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 25-08-2026 a las 01:20:11
-- Versión del servidor: 10.4.32-MariaDB
-- Versión de PHP: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `hotel`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `auth_group`
--

CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL,
  `name` varchar(150) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `auth_group`
--

INSERT INTO `auth_group` (`id`, `name`) VALUES
(2, 'Administradores'),
(1, 'Clientes');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `auth_group_permissions`
--

CREATE TABLE `auth_group_permissions` (
  `id` bigint(20) NOT NULL,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `auth_group_permissions`
--

INSERT INTO `auth_group_permissions` (`id`, `group_id`, `permission_id`) VALUES
(25, 1, 28),
(21, 1, 32),
(22, 1, 36),
(23, 1, 40),
(24, 1, 44),
(1, 2, 25),
(2, 2, 26),
(3, 2, 27),
(4, 2, 28),
(5, 2, 29),
(6, 2, 30),
(7, 2, 31),
(8, 2, 32),
(9, 2, 33),
(10, 2, 34),
(11, 2, 35),
(12, 2, 36),
(13, 2, 37),
(14, 2, 38),
(15, 2, 39),
(16, 2, 40),
(17, 2, 41),
(18, 2, 42),
(19, 2, 43),
(20, 2, 44);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `auth_permission`
--

CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `auth_permission`
--

INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES
(1, 'Can add log entry', 1, 'add_logentry'),
(2, 'Can change log entry', 1, 'change_logentry'),
(3, 'Can delete log entry', 1, 'delete_logentry'),
(4, 'Can view log entry', 1, 'view_logentry'),
(5, 'Can add permission', 3, 'add_permission'),
(6, 'Can change permission', 3, 'change_permission'),
(7, 'Can delete permission', 3, 'delete_permission'),
(8, 'Can view permission', 3, 'view_permission'),
(9, 'Can add group', 2, 'add_group'),
(10, 'Can change group', 2, 'change_group'),
(11, 'Can delete group', 2, 'delete_group'),
(12, 'Can view group', 2, 'view_group'),
(13, 'Can add user', 4, 'add_user'),
(14, 'Can change user', 4, 'change_user'),
(15, 'Can delete user', 4, 'delete_user'),
(16, 'Can view user', 4, 'view_user'),
(17, 'Can add content type', 5, 'add_contenttype'),
(18, 'Can change content type', 5, 'change_contenttype'),
(19, 'Can delete content type', 5, 'delete_contenttype'),
(20, 'Can view content type', 5, 'view_contenttype'),
(21, 'Can add session', 6, 'add_session'),
(22, 'Can change session', 6, 'change_session'),
(23, 'Can delete session', 6, 'delete_session'),
(24, 'Can view session', 6, 'view_session'),
(25, 'Can add cliente', 7, 'add_cliente'),
(26, 'Can change cliente', 7, 'change_cliente'),
(27, 'Can delete cliente', 7, 'delete_cliente'),
(28, 'Can view cliente', 7, 'view_cliente'),
(29, 'Can add tipo habitacion', 11, 'add_tipohabitacion'),
(30, 'Can change tipo habitacion', 11, 'change_tipohabitacion'),
(31, 'Can delete tipo habitacion', 11, 'delete_tipohabitacion'),
(32, 'Can view tipo habitacion', 11, 'view_tipohabitacion'),
(33, 'Can add habitacion', 8, 'add_habitacion'),
(34, 'Can change habitacion', 8, 'change_habitacion'),
(35, 'Can delete habitacion', 8, 'delete_habitacion'),
(36, 'Can view habitacion', 8, 'view_habitacion'),
(37, 'Can add reserva', 9, 'add_reserva'),
(38, 'Can change reserva', 9, 'change_reserva'),
(39, 'Can delete reserva', 9, 'delete_reserva'),
(40, 'Can view reserva', 9, 'view_reserva'),
(41, 'Can add servicio', 10, 'add_servicio'),
(42, 'Can change servicio', 10, 'change_servicio'),
(43, 'Can delete servicio', 10, 'delete_servicio'),
(44, 'Can view servicio', 10, 'view_servicio');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `auth_user`
--

CREATE TABLE `auth_user` (
  `id` int(11) NOT NULL,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(150) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `auth_user`
--

INSERT INTO `auth_user` (`id`, `password`, `last_login`, `is_superuser`, `username`, `first_name`, `last_name`, `email`, `is_staff`, `is_active`, `date_joined`) VALUES
(1, 'pbkdf2_sha256$1000000$RRzTMi0HKohYx1ht1vGbKB$qchdzlI1qZGt027a0RPCn9nVcp4e1M+zc9QYON3n1Yc=', '2026-06-13 01:08:44.000000', 1, 'Andres', 'Hector Andres', 'Hueman Ovalle', 'hector.hueman@virginiogomez.cl', 1, 1, '2026-06-03 00:11:00.000000'),
(3, 'pbkdf2_sha256$1000000$sIFTNyimOrQ86t4UaUclJn$T26AeeVrQM2zMLaPY5V2BTgO296jnOwm2VxUdIS+5Pg=', '2026-06-13 01:02:21.000000', 1, 'admin', 'Administrador', 'Hotel', 'adminhotel@demo.local', 1, 1, '2026-06-03 00:24:31.000000'),
(4, 'pbkdf2_sha256$1000000$oxhpw0e7TLhi1UkSjzI27C$/M0GmLP7c8RiInBtfaIhUVDe+LVB2kq9doDvqm3P9iU=', '2026-06-13 00:26:23.000000', 0, 'cliente', 'Cliente', 'Demo', 'clientehotel@demo.local', 0, 1, '2026-06-03 00:24:32.000000'),
(5, 'pbkdf2_sha256$1000000$7Z3v9qZq87kMhWNuMQFiMH$MM2tVKsgLocLRGQesDH+vsuUEgutmLZodg77NdWE61Q=', '2026-06-12 23:57:45.000000', 0, 'Hector', 'Hector', 'Hueman', 'hector@gmail.com', 0, 1, '2026-06-10 02:48:15.000000'),
(6, 'pbkdf2_sha256$1000000$nvOGxbZkvWU8vt7VF6MIJK$B9v8KcGh5ExZ0j3pjaJB/YCvyaxTj9zf9Q+lFZPWDNk=', '2026-06-13 00:54:20.000000', 0, 'andrea', 'andrea', 'Hueman', 'andrea@gmail.com', 0, 1, '2026-06-13 00:32:55.000000');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `auth_user_groups`
--

CREATE TABLE `auth_user_groups` (
  `id` bigint(20) NOT NULL,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `auth_user_groups`
--

INSERT INTO `auth_user_groups` (`id`, `user_id`, `group_id`) VALUES
(4, 1, 2),
(2, 3, 2),
(3, 4, 1),
(5, 5, 1),
(6, 6, 1);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `auth_user_user_permissions`
--

CREATE TABLE `auth_user_user_permissions` (
  `id` bigint(20) NOT NULL,
  `user_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `cliente`
--

CREATE TABLE `cliente` (
  `id` bigint(20) NOT NULL,
  `nombre` varchar(120) NOT NULL,
  `rut` varchar(12) NOT NULL,
  `email` varchar(254) NOT NULL,
  `telefono` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `cliente`
--

INSERT INTO `cliente` (`id`, `nombre`, `rut`, `email`, `telefono`) VALUES
(1, 'Andres Hueman', '16850587-6', 'hector.hueman@virginiogomez.com', '935315783'),
(2, 'Fer', '21555555-5', 'fer@gmail.com', '934345432'),
(3, 'Michel', '12543456-9', 'michi@gmail.com', '345345676'),
(4, 'Belen', '12432543-6', 'belen@gmail.com', '456456765'),
(5, 'Alexis', '6173221-7', 'alexis@gmail.com', '+56965876578'),
(6, 'Gerardo', '8425050-3', 'gerardo@gmail.com', '+56965765687'),
(7, 'Marce', '11111111-1', 'marce@gmail.com', '+56935315783'),
(8, 'Alicia', '22222222-2', 'ali@gmail.com', '+56943654678'),
(9, 'Claudia', '33333333-3', 'clau@gmail.com', '+35316587');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `django_admin_log`
--

CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext DEFAULT NULL,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) UNSIGNED NOT NULL,
  `change_message` longtext NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `user_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `django_admin_log`
--

INSERT INTO `django_admin_log` (`id`, `action_time`, `object_id`, `object_repr`, `action_flag`, `change_message`, `content_type_id`, `user_id`) VALUES
(1, '2026-06-05 22:43:47.000000', '1', 'Andres', 2, '[{\"changed\": {\"fields\": [\"password\"]}}]', 4, 3),
(2, '2026-06-05 22:47:37.000000', '1', 'Andres', 2, '[{\"changed\": {\"fields\": [\"Groups\"]}}]', 4, 3),
(3, '2026-06-05 22:48:53.000000', '1', 'Andres', 2, '[{\"changed\": {\"fields\": [\"Staff status\", \"Superuser status\"]}}]', 4, 3),
(4, '2026-06-05 23:08:14.000000', '3', 'adminhotel', 2, '[{\"changed\": {\"fields\": [\"password\"]}}]', 4, 3),
(5, '2026-06-05 23:08:33.000000', '3', 'admin', 2, '[{\"changed\": {\"fields\": [\"Username\"]}}]', 4, 3),
(6, '2026-06-05 23:09:31.000000', '4', 'clientehotel', 2, '[{\"changed\": {\"fields\": [\"password\"]}}]', 4, 3),
(7, '2026-06-05 23:09:42.000000', '4', 'cliente', 2, '[{\"changed\": {\"fields\": [\"Username\"]}}]', 4, 3),
(8, '2026-06-09 22:48:02.000000', '3', 'admin', 2, '[{\"changed\": {\"fields\": [\"password\"]}}]', 4, 1),
(9, '2026-06-09 22:49:24.000000', '1', 'Andres', 2, '[{\"changed\": {\"fields\": [\"password\"]}}]', 4, 3),
(10, '2026-06-09 22:50:08.000000', '4', 'cliente', 2, '[{\"changed\": {\"fields\": [\"password\"]}}]', 4, 3);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `django_content_type`
--

CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `django_content_type`
--

INSERT INTO `django_content_type` (`id`, `app_label`, `model`) VALUES
(1, 'admin', 'logentry'),
(2, 'auth', 'group'),
(3, 'auth', 'permission'),
(4, 'auth', 'user'),
(5, 'contenttypes', 'contenttype'),
(6, 'sessions', 'session'),
(7, 'TipoHabitacion', 'cliente'),
(8, 'TipoHabitacion', 'habitacion'),
(9, 'TipoHabitacion', 'reserva'),
(10, 'TipoHabitacion', 'servicio'),
(11, 'TipoHabitacion', 'tipohabitacion');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `django_migrations`
--

CREATE TABLE `django_migrations` (
  `id` bigint(20) NOT NULL,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `django_migrations`
--

INSERT INTO `django_migrations` (`id`, `app`, `name`, `applied`) VALUES
(1, 'TipoHabitacion', '0001_initial', '2026-05-13 01:12:09.000000'),
(2, 'TipoHabitacion', '0002_alter_habitacion_options_alter_cliente_table_and_more', '2026-05-13 01:12:09.000000'),
(3, 'contenttypes', '0001_initial', '2026-05-13 01:12:09.000000'),
(4, 'auth', '0001_initial', '2026-05-13 01:12:10.000000'),
(5, 'admin', '0001_initial', '2026-05-13 01:12:10.000000'),
(6, 'admin', '0002_logentry_remove_auto_add', '2026-05-13 01:12:10.000000'),
(7, 'admin', '0003_logentry_add_action_flag_choices', '2026-05-13 01:12:10.000000'),
(8, 'contenttypes', '0002_remove_content_type_name', '2026-05-13 01:12:10.000000'),
(9, 'auth', '0002_alter_permission_name_max_length', '2026-05-13 01:12:10.000000'),
(10, 'auth', '0003_alter_user_email_max_length', '2026-05-13 01:12:10.000000'),
(11, 'auth', '0004_alter_user_username_opts', '2026-05-13 01:12:10.000000'),
(12, 'auth', '0005_alter_user_last_login_null', '2026-05-13 01:12:10.000000'),
(13, 'auth', '0006_require_contenttypes_0002', '2026-05-13 01:12:10.000000'),
(14, 'auth', '0007_alter_validators_add_error_messages', '2026-05-13 01:12:10.000000'),
(15, 'auth', '0008_alter_user_username_max_length', '2026-05-13 01:12:10.000000'),
(16, 'auth', '0009_alter_user_last_name_max_length', '2026-05-13 01:12:10.000000'),
(17, 'auth', '0010_alter_group_name_max_length', '2026-05-13 01:12:10.000000'),
(18, 'auth', '0011_update_proxy_permissions', '2026-05-13 01:12:10.000000'),
(19, 'auth', '0012_alter_user_first_name_max_length', '2026-05-13 01:12:10.000000'),
(20, 'sessions', '0001_initial', '2026-05-13 01:12:10.000000'),
(21, 'TipoHabitacion', '0003_create_default_groups', '2026-06-03 00:18:29.000000'),
(22, 'TipoHabitacion', '0004_clientes_and_demo_users', '2026-06-03 00:24:32.000000'),
(23, 'TipoHabitacion', '0005_seed_dashboard_demo_data', '2026-06-03 01:23:53.000000'),
(24, 'TipoHabitacion', '0006_sync_room_states', '2026-06-05 22:27:07.000000'),
(25, 'TipoHabitacion', '0007_recalculate_reservation_totals', '2026-06-06 00:54:04.000000');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `django_session`
--

CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `django_session`
--

INSERT INTO `django_session` (`session_key`, `session_data`, `expire_date`) VALUES
('34dm16qtre2fe80lxvrd1wdb55lqh38v', '.eJxVjDkOwjAQAP-yNbJ8HynpeYPltdc4gBwpTirE31GkFNDOjOYNMe1bi_ugNc4FJlBw-WWY8pP6Icoj9fvC8tK3dUZ2JOy0g92WQq_r2f4NWhoNJpAoUuW5GIHkXTXOo9WUVdCoMdtkuQ7CG-VJVysr92SMy6hE0EJIaeDzBeo1N0Y:1wVdvK:yenMG7KSvx07JvnkER2_rvkUQjv0qNkGVYRo5ycTIa4', '2026-06-19 23:25:58.000000'),
('38maxk9rxdmqylxc4psb4y4uy9kb7nwp', '.eJxVjEsKwjAUAO_y1hKaJk2aLt33DOH9NFVpoJ-VeHcpdKHbmWHekHHfSt5XXfIkMICDyy8j5KfOh5AHzvdquM7bMpE5EnPa1YxV9HU9279BwbXAANr5PvYhRWma2FoKHQu70DLdvLgoll1orIokjZwUkSS0jKTekySH8PkC42o4wg:1wUaEG:PRFECOjMYDqbwYqjyd1KTwHX1egWaWEoAGR-A0GW3WI', '2026-06-17 01:17:08.000000'),
('5a9dn5gs8rvii4cs1cf190j8jl9losrp', '.eJxVjEEOwiAQAP-yZ0MEFkp79N43NCy72KqBpLQn499Nkx70OjOZN0xx3-Zpb7JOC8MAGi6_jGJ6SjkEP2K5V5Vq2daF1JGo0zY1VpbX7Wz_BnNsMwzQWWYjznBOKZtApnPO6th7IYc-2CAs3hOi7q3P2OdMwVF31Sia0DF8vuw0N-c:1wX7kT:o89rEwgx-M2T59mbpwwAm1UpBsIxU05JABEoJ6og9zU', '2026-06-24 01:28:53.000000'),
('5z3e6ifhqh8iuvflkaliz9v5c2owwl49', '.eJxVjEEOwiAQAP-yZ0MEFkp79N43NCy72KqBpLQn499Nkx70OjOZN0xx3-Zpb7JOC8MAGi6_jGJ6SjkEP2K5V5Vq2daF1JGo0zY1VpbX7Wz_BnNsMwzQWWYjznBOKZtApnPO6th7IYc-2CAs3hOi7q3P2OdMwVF31Sia0DF8vuw0N-c:1wX9CQ:FYRdNOU_e6tFj1h0hKigm6t6iasXd5O0ErwqhfRnay0', '2026-06-24 03:01:50.000000'),
('6kkq4cdoj47zgwph499sx2h8hft4c42i', '.eJxVjEEOwiAQAP-yZ0MEFkp79N43NCy72KqBpLQn499Nkx70OjOZN0xx3-Zpb7JOC8MAGi6_jGJ6SjkEP2K5V5Vq2daF1JGo0zY1VpbX7Wz_BnNsMwzQWWYjznBOKZtApnPO6th7IYc-2CAs3hOi7q3P2OdMwVF31Sia0DF8vuw0N-c:1wX9b3:HrUsgSp9VyaUKa4iPrxYwsQUERk6vCBKEVhHwS_ptqQ', '2026-06-24 03:27:17.000000'),
('9gmthwrz9vig2xhxqrpfvrt0v8z50exn', '.eJxVjEEOwiAQAP-yZ0MEFkp79N43NCy72KqBpLQn499Nkx70OjOZN0xx3-Zpb7JOC8MAGi6_jGJ6SjkEP2K5V5Vq2daF1JGo0zY1VpbX7Wz_BnNsMwzQWWYjznBOKZtApnPO6th7IYc-2CAs3hOi7q3P2OdMwVF31Sia0DF8vuw0N-c:1wX8gR:6qTZysw4DcRDMCdHdNQHDhhtt1xUsGSz2GpunO7AkpQ', '2026-06-24 02:28:47.000000'),
('bd72howp1csnarbdwbpvpmxyb8ysi7b0', '.eJxVjEsKwjAUAO_y1hKaJk2aLt33DOH9NFVpoJ-VeHcpdKHbmWHekHHfSt5XXfIkMICDyy8j5KfOh5AHzvdquM7bMpE5EnPa1YxV9HU9279BwbXAANr5PvYhRWma2FoKHQu70DLdvLgoll1orIokjZwUkSS0jKTekySH8PkC42o4wg:1wUa8I:1HBppi_bfDQou-A2ibTWcvPoDRaWRHDp6iF7IuzrL8E', '2026-06-17 01:10:58.000000'),
('bwoqqiisf8zj4g6tg0mjhxmf99rmf4dj', '.eJxVjEEOwiAQAP-yZ0MEFkp79N43NCy72KqBpLQn499Nkx70OjOZN0xx3-Zpb7JOC8MAGi6_jGJ6SjkEP2K5V5Vq2daF1JGo0zY1VpbX7Wz_BnNsMwzQWWYjznBOKZtApnPO6th7IYc-2CAs3hOi7q3P2OdMwVF31Sia0DF8vuw0N-c:1wX8Z6:5dFvG_emaXZmGCLg6cwXP3aeQ0QUR0RHFJX0se1ub-U', '2026-06-24 02:21:12.000000'),
('d6zcayuevkqbrk6s8dymtnhjdtux6pk2', '.eJxVjEEOwiAQAP-yZ0MEFkp79N43NCy72KqBpLQn499Nkx70OjOZN0xx3-Zpb7JOC8MAGi6_jGJ6SjkEP2K5V5Vq2daF1JGo0zY1VpbX7Wz_BnNsMwzQWWYjznBOKZtApnPO6th7IYc-2CAs3hOi7q3P2OdMwVF31Sia0DF8vuw0N-c:1wX7gH:MB4aDklHAkOTAn2PA1_WSe_4UwV3FUgdmF2z3V0DnZ8', '2026-06-24 01:24:33.000000'),
('eszi34veicy52hq4lhjwflcmonew474s', '.eJxVjDEOgzAMAP_iuYpI4jgpY3fegOw4FNoKJAJT1b9XSAztene6N_S8b2O_17L2k0ILCJdfJpyfZT6EPni-LyYv87ZOYo7EnLaabtHyup3t32DkOkILEVMkSyWLUCF2aKnxKKyDExd08BkxXJUl2RQ8eVLNWV0TUXwU28DnC-CYN8Q:1wX75Y:bsPGOV1Xx3I8LPSTchOMNsXpcJGdlz1PBpw0JzV5a-I', '2026-06-24 00:46:36.000000'),
('f04gahi81ilaj8hh4it25aqfgbkaehma', '.eJxVjDkOwjAQAP-yNbJ8HynpeYPltdc4gBwpTirE31GkFNDOjOYNMe1bi_ugNc4FJlBw-WWY8pP6Icoj9fvC8tK3dUZ2JOy0g92WQq_r2f4NWhoNJpAoUuW5GIHkXTXOo9WUVdCoMdtkuQ7CG-VJVysr92SMy6hE0EJIaeDzBeo1N0Y:1wVdy3:fY1rJGg6ygJwuxj169HO1bn1UbHl0UKFQpDTF4Wk5Pc', '2026-06-19 23:28:47.000000'),
('icuiuw2sdo50eygem3ap6w750yj5svet', '.eJxVjEsKwjAUAO_y1hKaJk2aLt33DOH9NFVpoJ-VeHcpdKHbmWHekHHfSt5XXfIkMICDyy8j5KfOh5AHzvdquM7bMpE5EnPa1YxV9HU9279BwbXAANr5PvYhRWma2FoKHQu70DLdvLgoll1orIokjZwUkSS0jKTekySH8PkC42o4wg:1wVd0b:fjNwrUdrHs47S2eaxV_ro7yd7OMR43NR2FuXvJKH29c', '2026-06-19 22:27:21.000000'),
('ital7vgpazcioxun7mzgmqcqryb0ke57', '.eJxVjEEOwiAQAP-yZ0MK222hR---gSwsSNXQpLQn499Nkx70OjOZN3jet-L3llY_C0yAcPllgeMz1UPIg-t9UXGp2zoHdSTqtE3dFkmv69n-DQq3AhPofsxEZAbTcbTkxp5dR8nJIOg0otZZLLoUSazOHDHn7AIlQjIB2cDnC7_hN4I:1wYBkB:IYyfka6iqRsH8S2Lo7hYtVe7l4_i9EM2Qg_grCshKxw', '2026-06-26 23:56:59.000000'),
('j2jgitu8ydepjj3jvy6fgzo3j7p19mo1', '.eJxVjEEOwiAQAP-yZ0MEFkp79N43NCy72KqBpLQn499Nkx70OjOZN0xx3-Zpb7JOC8MAGi6_jGJ6SjkEP2K5V5Vq2daF1JGo0zY1VpbX7Wz_BnNsMwzQWWYjznBOKZtApnPO6th7IYc-2CAs3hOi7q3P2OdMwVF31Sia0DF8vuw0N-c:1wX7Yd:4JUDlD9bKNDEL_2g5x0gmBEg8Nr6Gm3qFnGzWrY3W2s', '2026-06-24 01:16:39.000000'),
('j6whhovycowiyosivi8yyputut37m4xk', '.eJxVjEEOwiAQAP-yZ0MK222hR---gSwsSNXQpLQn499Nkx70OjOZN3jet-L3llY_C0yAcPllgeMz1UPIg-t9UXGp2zoHdSTqtE3dFkmv69n-DQq3AhPofsxEZAbTcbTkxp5dR8nJIOg0otZZLLoUSazOHDHn7AIlQjIB2cDnC7_hN4I:1wX75Z:Y4vFLeKQ4vnTZFLFJLsxy-1BEcTYI2ArqdqjFTVFhyw', '2026-06-24 00:46:37.000000'),
('mdi1w7u2c86s6c3oldrgqaqdvm9uz3e7', '.eJxVjDEOgzAMAP_iuYpI4jgpY3fegOw4FNoKJAJT1b9XSAztene6N_S8b2O_17L2k0ILCJdfJpyfZT6EPni-LyYv87ZOYo7EnLaabtHyup3t32DkOkILEVMkSyWLUCF2aKnxKKyDExd08BkxXJUl2RQ8eVLNWV0TUXwU28DnC-CYN8Q:1wX9CP:5HuOPOH_qIxjUQQdwfeCmgz5jmGvlETyypGlUDZOX90', '2026-06-24 03:01:49.000000'),
('qsjnrnwm4v3z2z3jv953mun3k442b92f', '.eJxVjEsKwjAUAO_y1hKaJk2aLt33DOH9NFVpoJ-VeHcpdKHbmWHekHHfSt5XXfIkMICDyy8j5KfOh5AHzvdquM7bMpE5EnPa1YxV9HU9279BwbXAANr5PvYhRWma2FoKHQu70DLdvLgoll1orIokjZwUkSS0jKTekySH8PkC42o4wg:1wUaEu:NhD8_97wt7Il8yXsMhzN_HW-VXeUxF7tTr2Xt6KgkXk', '2026-06-17 01:17:48.000000'),
('r9yza0rh41dxri1tk5ul158y5aftdhml', '.eJxVjDkOwjAQAP-yNbJ8HynpeYPltdc4gBwpTirE31GkFNDOjOYNMe1bi_ugNc4FJlBw-WWY8pP6Icoj9fvC8tK3dUZ2JOy0g92WQq_r2f4NWhoNJpAoUuW5GIHkXTXOo9WUVdCoMdtkuQ7CG-VJVysr92SMy6hE0EJIaeDzBeo1N0Y:1wVfJQ:h14khg8WJJe3Gr5TkC2T0bLV_-QTDKI_DPHejNcQUkk', '2026-06-20 00:54:56.000000'),
('ud34tz4gmfdqmngi80qdxdtpcsor4p3l', '.eJxVjEEOwiAQAP-yZ0MEFkp79N43NCy72KqBpLQn499Nkx70OjOZN0xx3-Zpb7JOC8MAGi6_jGJ6SjkEP2K5V5Vq2daF1JGo0zY1VpbX7Wz_BnNsMwzQWWYjznBOKZtApnPO6th7IYc-2CAs3hOi7q3P2OdMwVF31Sia0DF8vuw0N-c:1wX7za:khWr-6ROlu7WiDjo_b3xL2qClLEVGZytx-WyYhFZYMY', '2026-06-24 01:44:30.000000'),
('uup0g4kidjp0u1np0oy37fe2mwvtlupn', '.eJxVjEsKwjAUAO_y1hKaJk2aLt33DOH9NFVpoJ-VeHcpdKHbmWHekHHfSt5XXfIkMICDyy8j5KfOh5AHzvdquM7bMpE5EnPa1YxV9HU9279BwbXAANr5PvYhRWma2FoKHQu70DLdvLgoll1orIokjZwUkSS0jKTekySH8PkC42o4wg:1wUaKt:oo_YQYbhJkyefr5vfJvvKmNkVFlZX6SIr2b_AMFFugI', '2026-06-17 01:23:59.000000'),
('xc31l042bzy8iai0d35tjh5yrtpc5sj6', '.eJxVjLsOwjAMAP_FM4qaOHHSjux8Q2U7KS2gVOpjQvw7qtQB1rvTvaHnfRv7fS1LP2XowMLllwnrs9RD5AfX-2x0rtsyiTkSc9rV3OZcXtez_RuMvI7QgRt8FGkSKiXEwdkYNGBTWIgDJxZG5yI5jN4zkVivQxup5RyTVUL4fAHPVTc8:1wVfZV:Da_dr84jr4svSrKGi7F6BlymrNmfZfEJzKny3dDdmts', '2026-06-20 01:11:33.000000');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `habitación`
--

CREATE TABLE `habitación` (
  `id` bigint(20) NOT NULL,
  `numero` varchar(10) NOT NULL,
  `piso` int(11) NOT NULL,
  `estado` varchar(20) NOT NULL,
  `tipo_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `habitación`
--

INSERT INTO `habitación` (`id`, `numero`, `piso`, `estado`, `tipo_id`) VALUES
(2, '34', 30, 'Disponible', 2),
(3, '40', 20, 'Disponible', 3),
(6, '5', 5, 'Disponible', 5),
(7, '7733', 22, 'Ocupada', 5),
(8, '66', 45, 'Mantenimiento', 9),
(9, '55', 44, 'Ocupada', 6),
(10, '43', 56, 'Disponible', 2),
(11, '300', 9, 'Ocupada', 9),
(12, '11', 11, 'Disponible', 9);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `reserva`
--

CREATE TABLE `reserva` (
  `id` bigint(20) NOT NULL,
  `check_in` date NOT NULL,
  `check_out` date NOT NULL,
  `estado` varchar(20) NOT NULL,
  `total` decimal(10,2) NOT NULL,
  `cliente_id` bigint(20) NOT NULL,
  `habitacion_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `reserva`
--

INSERT INTO `reserva` (`id`, `check_in`, `check_out`, `estado`, `total`, `cliente_id`, `habitacion_id`) VALUES
(3, '2026-04-10', '2026-04-14', 'Finalizada', 300000.00, 1, 3),
(6, '2026-06-09', '2026-06-11', 'Cancelada', 150000.00, 3, 3),
(8, '2026-06-14', '2026-06-20', 'Pendiente', 180000.00, 6, 7),
(10, '2026-06-24', '2026-06-30', 'Confirmada', 1200000.00, 8, 11),
(11, '2026-06-24', '2026-07-01', 'Pendiente', 210000.00, 7, 6),
(12, '2026-07-10', '2026-08-09', 'Pendiente', 1500000.00, 6, 2),
(13, '2026-07-08', '2026-07-11', 'Cancelada', 600000.00, 4, 12),
(14, '2026-07-05', '2026-07-12', 'Confirmada', 210000.00, 9, 7);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `servicio`
--

CREATE TABLE `servicio` (
  `id` bigint(20) NOT NULL,
  `nombre` varchar(100) NOT NULL,
  `precio` decimal(10,2) NOT NULL,
  `descripcion` longtext NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `servicio`
--

INSERT INTO `servicio` (`id`, `nombre`, `precio`, `descripcion`) VALUES
(1, 'Estandar', 25000.00, 'Alojamiento y Confort: Cama individual, armario, escritorio y silla.\r\n\r\nBaño Privado: Equipado con productos de higiene personal (amenities), toallas limpias y agua caliente.Conectividad y \r\n\r\nEntretenimiento: Wi-Fi de alta velocidad, televisor y tomas de corriente \r\n\r\naccesibles.Comodidades: Aire acondicionado/calefacción, servicio de minibar, caja fuerte y teléfono'),
(2, 'Servicios Básicos e Indispensables', 15000.00, 'Recepción 24 horas: \r\n\r\nAtención constante para check-in/check-out.\r\n\r\nLimpieza diaria: Mantenimiento y aseo de la habitación.\r\n\r\nConexión WiFi: Acceso a internet en habitaciones y áreas comunes.\r\n\r\nClimatización: Aire acondicionado y/o calefacción.\r\n\r\nArtículos de aseo (Amenities): Champú, jabón, secador de pelo.\r\n\r\nServicios de seguridad: Cajas fuertes y vigilancia'),
(3, 'Servicios de Restauración y Alimentos', 20000.00, 'Desayuno: Buffet o a la carta, a menudo incluido.Servicio a la habitación (Room Service): Comida y bebida servida en la habitación.Restaurante y Bar: Áreas de comida dentro del hotel.Cafetera en la habitación (Coffee Kit): Cafetera con insumos'),
(4, 'Servicios de Confort y Amenidades (4-5 Estrellas)', 25000.00, 'Spa y Bienestar: Jacuzzi, masajes, sauna y tratamientos.Gimnasio: Equipamiento para ejercicio.Alberca/Piscina: Áreas de baño.Centro de Negocios y Coworking: Espacios para trabajar.Servicio de Conserjería (Concierge): Asistencia personalizada para reservas y actividades');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `servicio_reservas`
--

CREATE TABLE `servicio_reservas` (
  `id` bigint(20) NOT NULL,
  `servicio_id` bigint(20) NOT NULL,
  `reserva_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `tipo de habitación`
--

CREATE TABLE `tipo de habitación` (
  `id` bigint(20) NOT NULL,
  `nombre` varchar(100) NOT NULL,
  `descripcion` longtext NOT NULL,
  `precio_noche` decimal(10,2) NOT NULL,
  `capacidad` int(11) NOT NULL,
  `foto` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `tipo de habitación`
--

INSERT INTO `tipo de habitación` (`id`, `nombre`, `descripcion`, `precio_noche`, `capacidad`, `foto`) VALUES
(1, 'Individual', 'Pensada para un huésped, cuenta con una cama individual o simple.', 25000.00, 1, 'habitaciones/individual.jpg'),
(2, 'Doble', 'Diseñada para 2 personas. Puede tener una cama matrimonial (King o Queen) o dos camas separadas.', 50000.00, 2, 'habitaciones/doble.jpg'),
(3, 'Triple', 'Equipada para 3 personas. Suele incluir tres camas individuales o una cama matrimonial más una individual', 75000.00, 3, 'habitaciones/triple.jpg'),
(5, 'Estándar', 'Es la habitación básica del hotel. Incluye una cama, baño y equipamiento esencial.', 30000.00, 2, 'habitaciones/estandar.jpg'),
(6, 'Superior', 'Un poco más amplia que la estándar, a menudo ofrece mejores vistas, un diseño más moderno o comodidades adicionales.', 45000.00, 2, 'habitaciones/superior.jpg'),
(8, 'Junior Suite', 'Una habitación más grande que la estándar que integra una pequeña zona de estar (sofá y mesa) en el mismo ambiente, sin paredes divisorias', 100000.00, 4, 'habitaciones/JuniorSuite.jpg'),
(9, 'Suite Presidencial', 'La categoría más lujosa, grande y costosa del hotel. Ofrece servicios VIP, varias habitaciones, vistas excepcionales y comodidades exclusivas.', 200000.00, 6, 'habitaciones/sclsi-suite-living-9191-hor-feat.webp');

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `auth_group`
--
ALTER TABLE `auth_group`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `name` (`name`);

--
-- Indices de la tabla `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  ADD KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`);

--
-- Indices de la tabla `auth_permission`
--
ALTER TABLE `auth_permission`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`);

--
-- Indices de la tabla `auth_user`
--
ALTER TABLE `auth_user`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`);

--
-- Indices de la tabla `auth_user_groups`
--
ALTER TABLE `auth_user_groups`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_user_groups_user_id_group_id_94350c0c_uniq` (`user_id`,`group_id`),
  ADD KEY `auth_user_groups_group_id_97559544_fk_auth_group_id` (`group_id`);

--
-- Indices de la tabla `auth_user_user_permissions`
--
ALTER TABLE `auth_user_user_permissions`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq` (`user_id`,`permission_id`),
  ADD KEY `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` (`permission_id`);

--
-- Indices de la tabla `cliente`
--
ALTER TABLE `cliente`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `rut` (`rut`),
  ADD UNIQUE KEY `email` (`email`);

--
-- Indices de la tabla `django_admin_log`
--
ALTER TABLE `django_admin_log`
  ADD PRIMARY KEY (`id`),
  ADD KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  ADD KEY `django_admin_log_user_id_c564eba6_fk_auth_user_id` (`user_id`);

--
-- Indices de la tabla `django_content_type`
--
ALTER TABLE `django_content_type`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`);

--
-- Indices de la tabla `django_migrations`
--
ALTER TABLE `django_migrations`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `django_session`
--
ALTER TABLE `django_session`
  ADD PRIMARY KEY (`session_key`),
  ADD KEY `django_session_expire_date_a5c62663` (`expire_date`);

--
-- Indices de la tabla `habitación`
--
ALTER TABLE `habitación`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `numero` (`numero`),
  ADD KEY `TipoHabitacion_habit_tipo_id_ee98862c_fk_TipoHabit` (`tipo_id`);

--
-- Indices de la tabla `reserva`
--
ALTER TABLE `reserva`
  ADD PRIMARY KEY (`id`),
  ADD KEY `TipoHabitacion_reser_cliente_id_3014c617_fk_TipoHabit` (`cliente_id`),
  ADD KEY `TipoHabitacion_reser_habitacion_id_061c18af_fk_TipoHabit` (`habitacion_id`);

--
-- Indices de la tabla `servicio`
--
ALTER TABLE `servicio`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `servicio_reservas`
--
ALTER TABLE `servicio_reservas`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `TipoHabitacion_servicio__servicio_id_reserva_id_08becef6_uniq` (`servicio_id`,`reserva_id`),
  ADD KEY `TipoHabitacion_servi_reserva_id_c04b709f_fk_TipoHabit` (`reserva_id`);

--
-- Indices de la tabla `tipo de habitación`
--
ALTER TABLE `tipo de habitación`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `auth_group`
--
ALTER TABLE `auth_group`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT de la tabla `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=26;

--
-- AUTO_INCREMENT de la tabla `auth_permission`
--
ALTER TABLE `auth_permission`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=45;

--
-- AUTO_INCREMENT de la tabla `auth_user`
--
ALTER TABLE `auth_user`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT de la tabla `auth_user_groups`
--
ALTER TABLE `auth_user_groups`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT de la tabla `auth_user_user_permissions`
--
ALTER TABLE `auth_user_user_permissions`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `cliente`
--
ALTER TABLE `cliente`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;

--
-- AUTO_INCREMENT de la tabla `django_admin_log`
--
ALTER TABLE `django_admin_log`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT de la tabla `django_content_type`
--
ALTER TABLE `django_content_type`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=12;

--
-- AUTO_INCREMENT de la tabla `django_migrations`
--
ALTER TABLE `django_migrations`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=26;

--
-- AUTO_INCREMENT de la tabla `habitación`
--
ALTER TABLE `habitación`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=13;

--
-- AUTO_INCREMENT de la tabla `reserva`
--
ALTER TABLE `reserva`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=15;

--
-- AUTO_INCREMENT de la tabla `servicio`
--
ALTER TABLE `servicio`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT de la tabla `servicio_reservas`
--
ALTER TABLE `servicio_reservas`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT de la tabla `tipo de habitación`
--
ALTER TABLE `tipo de habitación`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  ADD CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  ADD CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`);

--
-- Filtros para la tabla `auth_permission`
--
ALTER TABLE `auth_permission`
  ADD CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`);

--
-- Filtros para la tabla `auth_user_groups`
--
ALTER TABLE `auth_user_groups`
  ADD CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  ADD CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Filtros para la tabla `auth_user_user_permissions`
--
ALTER TABLE `auth_user_user_permissions`
  ADD CONSTRAINT `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  ADD CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Filtros para la tabla `django_admin_log`
--
ALTER TABLE `django_admin_log`
  ADD CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  ADD CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Filtros para la tabla `habitación`
--
ALTER TABLE `habitación`
  ADD CONSTRAINT `TipoHabitacion_habit_tipo_id_ee98862c_fk_TipoHabit` FOREIGN KEY (`tipo_id`) REFERENCES `tipo de habitación` (`id`);

--
-- Filtros para la tabla `reserva`
--
ALTER TABLE `reserva`
  ADD CONSTRAINT `TipoHabitacion_reser_cliente_id_3014c617_fk_TipoHabit` FOREIGN KEY (`cliente_id`) REFERENCES `cliente` (`id`),
  ADD CONSTRAINT `TipoHabitacion_reser_habitacion_id_061c18af_fk_TipoHabit` FOREIGN KEY (`habitacion_id`) REFERENCES `habitación` (`id`);

--
-- Filtros para la tabla `servicio_reservas`
--
ALTER TABLE `servicio_reservas`
  ADD CONSTRAINT `TipoHabitacion_servi_reserva_id_c04b709f_fk_TipoHabit` FOREIGN KEY (`reserva_id`) REFERENCES `reserva` (`id`),
  ADD CONSTRAINT `TipoHabitacion_servi_servicio_id_1b48d942_fk_TipoHabit` FOREIGN KEY (`servicio_id`) REFERENCES `servicio` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
