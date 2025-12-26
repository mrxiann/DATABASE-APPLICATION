-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1:3306
-- Generation Time: Dec 26, 2025 at 03:16 PM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `sk_youth_portal`
--

-- --------------------------------------------------------

--
-- Table structure for table `awards`
--

CREATE TABLE `awards` (
  `id` int(11) NOT NULL,
  `user_id` int(11) DEFAULT NULL,
  `award_name` varchar(100) DEFAULT NULL,
  `description` text DEFAULT NULL,
  `award_date` date DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `awards`
--

INSERT INTO `awards` (`id`, `user_id`, `award_name`, `description`, `award_date`, `created_at`) VALUES
(1, 27, 'Outstanding Youth Leader', 'Recognized for exceptional leadership in community projects', '2024-12-28', '2025-12-25 07:32:32'),
(2, 7, 'Community Service Award', 'Dedicated service in barangay clean-up drives', '2025-04-26', '2025-12-25 07:32:32'),
(7, 12, 'Public Speaking Champion', 'Winner in youth debate competition', '2025-01-04', '2025-12-25 07:32:32'),
(8, 13, 'Technology Innovator', 'Best project in youth tech expo', '2024-12-15', '2025-12-25 07:32:32'),
(9, 14, 'Cultural Preservation', 'Excellence in traditional dance performance', '2025-02-15', '2025-12-25 07:32:32'),
(10, 15, 'Entrepreneurial Spirit', 'Outstanding business proposal in youth forum', '2024-12-25', '2025-12-25 07:32:32'),
(11, 6, 'Volunteer of the Month', 'Most dedicated volunteer for March 2024', '2024-12-31', '2025-12-25 07:32:32'),
(12, 7, 'Leadership Excellence', 'Outstanding performance in leadership training', '2024-12-20', '2025-12-25 07:32:32'),
(17, 12, 'Disaster Response Hero', 'Bravery and quick response during disaster drill', '2024-12-22', '2025-12-25 07:32:32'),
(18, 27, 'Health Advocate', 'Active participation in health awareness campaigns', '2025-12-08', '2025-12-25 07:32:32'),
(19, 27, 'Digital Literacy Champion', 'Top performer in computer training', '2024-12-14', '2025-12-25 07:32:32'),
(20, 15, 'Youth Ambassador', 'Represented SK in regional youth conference', '2025-02-27', '2025-12-25 07:32:32');

-- --------------------------------------------------------

--
-- Table structure for table `events`
--

CREATE TABLE `events` (
  `id` int(11) NOT NULL,
  `title` varchar(200) NOT NULL,
  `description` text DEFAULT NULL,
  `event_date` date NOT NULL,
  `event_time` time NOT NULL,
  `location` varchar(200) DEFAULT NULL,
  `event_type` varchar(50) DEFAULT NULL,
  `max_participants` int(11) DEFAULT NULL,
  `registered_participants` int(11) DEFAULT 0,
  `status` varchar(20) DEFAULT 'upcoming',
  `created_by` int(11) DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `events`
--

INSERT INTO `events` (`id`, `title`, `description`, `event_date`, `event_time`, `location`, `event_type`, `max_participants`, `registered_participants`, `status`, `created_by`, `created_at`) VALUES
(1, 'Coastal Clean-Up Drive', 'Environmental clean-up activity', '2024-12-20', '09:00:00', 'Boulevard', 'Volunteer', 100, 0, 'upcoming', 1, '2025-12-25 06:07:33'),
(2, 'Youth Leadership Summit', 'Leadership training workshop', '2024-12-25', '10:00:00', 'Barangay Hall', 'Seminar', 150, 0, 'upcoming', 1, '2025-12-25 06:07:33'),
(3, 'Christmas Party', 'Annual youth Christmas celebration', '2024-12-23', '18:00:00', 'Community Center', 'Social', 200, 0, 'upcoming', 1, '2025-12-25 06:07:33'),
(4, 'Basketball Tournament', 'Inter-purok basketball competition', '2024-12-28', '14:00:00', 'Sports Complex', 'Sports', 50, 0, 'upcoming', 1, '2025-12-25 06:07:33'),
(5, 'First Aid Training', 'Basic first aid certification', '2025-01-05', '08:00:00', 'Health Center', 'Training', 30, 0, 'upcoming', 1, '2025-12-25 06:07:33'),
(6, 'Youth Leadership Summit', 'Annual leadership training for SK youth leaders', '2024-03-15', '09:00:00', 'Quezon City Convention Center', 'Seminar', 200, 150, 'completed', 1, '2025-12-25 07:32:32'),
(7, 'Community Clean-up Drive', 'Barangay-wide clean-up activity', '2024-03-20', '07:00:00', 'Barangay 1 Covered Court', 'Volunteer', 100, 85, 'completed', 2, '2025-12-25 07:32:32'),
(8, 'Basketball Tournament', 'Inter-barangay basketball competition', '2024-04-05', '14:00:00', 'City Sports Complex', 'Sports', 16, 16, 'completed', 3, '2025-12-25 07:32:32'),
(9, 'Digital Literacy Workshop', 'Basic computer skills training for youth', '2024-04-12', '10:00:00', 'Public Library Computer Lab', 'Training', 30, 28, 'completed', 4, '2025-12-25 07:32:32'),
(10, 'Youth Entrepreneurship Forum', 'Business ideas and startup discussions', '2024-04-25', '13:00:00', 'Business Center Auditorium', 'Seminar', 80, 72, 'completed', 5, '2025-12-25 07:32:32'),
(11, 'Environmental Awareness Campaign', 'Tree planting and eco-education', '2024-05-10', '08:00:00', 'City Eco-Park', 'Volunteer', 150, 120, 'cancelled', 1, '2025-12-25 07:32:32'),
(12, 'Cultural Dance Festival', 'Traditional dance performances and competition', '2024-05-18', '16:00:00', 'City Cultural Center', 'Social', 300, 210, 'upcoming', 2, '2025-12-25 07:32:32'),
(13, 'First Aid Training', 'Basic life support and emergency response', '2024-05-22', '09:00:00', 'Red Cross Training Center', 'Training', 40, 35, 'upcoming', 3, '2025-12-25 07:32:32'),
(14, 'Youth Job Fair', 'Employment opportunities for young people', '2024-06-05', '10:00:00', 'SM Mega Trade Hall', 'Seminar', 500, 320, 'upcoming', 4, '2025-12-25 07:32:32'),
(15, 'Anti-Drug Awareness Seminar', 'Prevention and education program', '2024-06-12', '14:00:00', 'Barangay Hall', 'Seminar', 80, 65, 'upcoming', 5, '2025-12-25 07:32:32'),
(16, 'Swimming Competition', 'Inter-school swimming tournament', '2024-06-20', '08:00:00', 'City Olympic Pool', 'Sports', 50, 42, 'upcoming', 1, '2025-12-25 07:32:32'),
(17, 'Art Workshop', 'Painting and creative arts training', '2024-06-25', '13:00:00', 'City Art Gallery', 'Training', 25, 22, 'upcoming', 2, '2025-12-25 07:32:32'),
(18, 'Youth Year-End Party', 'Annual holiday celebration for SK members', '2024-12-15', '18:00:00', 'Barangay Covered Court', 'Social', 200, 180, 'upcoming', 3, '2025-12-25 07:32:32'),
(19, 'Disaster Preparedness Drill', 'Earthquake and fire safety演习', '2024-07-10', '07:00:00', 'Evacuation Center', 'Training', 100, 85, 'completed', 4, '2025-12-25 07:32:32'),
(20, 'Music Festival', 'Local band performances and competitions', '2024-07-20', '17:00:00', 'City Plaza', 'Social', 400, 310, 'ongoing', 5, '2025-12-25 07:32:32'),
(21, 'Public Speaking Workshop', 'Communication skills development', '2024-08-05', '10:00:00', 'University Auditorium', 'Training', 60, 52, 'ongoing', 1, '2025-12-25 07:32:32'),
(22, 'Blood Donation Drive', 'Community blood donation activity', '2024-08-12', '09:00:00', 'City Health Center', 'Volunteer', 100, 78, 'ongoing', 2, '2025-12-25 07:32:32'),
(24, 'Cooking Competition', 'Traditional Filipino cooking contest', '2024-09-05', '10:00:00', 'Barangay Food Court', 'Social', 20, 18, 'cancelled', 4, '2025-12-25 07:32:32'),
(25, 'Tech Innovation Expo', 'Youth technology projects showcase', '2024-09-15', '11:00:00', 'Tech Hub Convention', 'Seminar', 150, 125, 'cancelled', 5, '2025-12-25 07:32:32');

-- --------------------------------------------------------

--
-- Table structure for table `event_registrations`
--

CREATE TABLE `event_registrations` (
  `id` int(11) NOT NULL,
  `event_id` int(11) DEFAULT NULL,
  `user_id` int(11) DEFAULT NULL,
  `registration_date` timestamp NOT NULL DEFAULT current_timestamp(),
  `attendance_status` varchar(20) DEFAULT 'registered',
  `check_in_time` datetime DEFAULT NULL,
  `check_out_time` datetime DEFAULT NULL,
  `hours_credited` decimal(5,2) DEFAULT 0.00
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `event_registrations`
--

INSERT INTO `event_registrations` (`id`, `event_id`, `user_id`, `registration_date`, `attendance_status`, `check_in_time`, `check_out_time`, `hours_credited`) VALUES
(1, 1, 2, '2025-12-25 06:07:33', 'registered', NULL, NULL, 0.00),
(2, 2, 2, '2025-12-25 06:07:33', 'registered', NULL, NULL, 0.00),
(3, 1, 3, '2025-12-25 06:07:33', 'registered', NULL, NULL, 0.00),
(4, 2, 3, '2025-12-25 06:07:33', 'registered', NULL, NULL, 0.00),
(5, 1, 6, '2024-03-10 02:30:00', 'attended', '2025-03-07 08:45:00', '2025-03-07 17:30:00', 8.50),
(6, 1, 27, '2024-03-11 06:20:00', 'attended', '2024-03-15 08:30:00', '2024-03-15 17:00:00', 8.00),
(11, 3, 12, '2024-04-02 02:45:00', 'attended', '2024-04-05 13:45:00', '2024-04-05 17:45:00', 4.00),
(12, 4, 13, '2024-04-10 08:00:00', 'attended', '2024-04-12 09:30:00', '2024-04-12 16:00:00', 6.50),
(13, 4, 14, '2024-04-11 03:15:00', 'attended', '2024-04-12 09:45:00', '2024-04-12 15:30:00', 5.75),
(14, 5, 15, '2024-04-22 06:50:00', 'attended', '2024-04-25 12:30:00', '2024-04-25 18:00:00', 5.50),
(15, 5, 26, '2024-04-23 01:40:00', 'attended', '2024-04-25 12:45:00', '2024-04-25 17:30:00', 4.75),
(16, 6, 27, '2024-05-05 02:20:00', 'registered', NULL, NULL, 0.00),
(21, 9, 12, '2024-06-01 05:20:00', 'registered', NULL, NULL, 0.00),
(22, 10, 13, '2024-06-10 02:15:00', 'registered', NULL, NULL, 0.00),
(23, 11, 14, '2024-06-18 06:40:00', 'registered', NULL, NULL, 0.00),
(24, 13, 15, '2025-12-25 07:42:57', 'checked_in', '2025-12-25 15:42:57', NULL, 0.00),
(25, 13, 2, '2025-12-25 08:53:22', 'attended', NULL, NULL, 0.00),
(26, 18, 2, '2025-12-25 08:55:38', 'registered', NULL, NULL, 0.00),
(27, 11, 27, '2025-12-25 08:59:38', 'attended', '2025-12-25 16:59:38', NULL, 6.00),
(28, 11, 28, '2025-12-25 08:59:45', 'checked_in', '2025-12-25 16:59:45', NULL, 0.00),
(29, 20, 26, '2025-12-25 09:00:02', 'checked_in', '2025-12-25 17:00:02', NULL, 0.00),
(30, 12, 27, '2025-12-25 09:00:11', 'registered', '2025-12-25 17:00:11', NULL, 6.00),
(31, 12, 22, '2025-12-25 09:00:17', 'checked_in', '2025-12-25 17:00:17', NULL, 0.00),
(32, 12, 21, '2025-12-25 09:00:24', 'checked_in', '2025-12-25 17:00:24', NULL, 0.00),
(33, 5, 27, '2025-12-26 07:12:21', 'registered', '2025-12-25 17:00:30', NULL, 0.00),
(34, 4, 27, '2025-12-26 07:12:29', 'registered', '2025-12-20 17:00:50', '2025-12-20 18:00:50', 1.00),
(35, 22, 14, '2025-12-26 09:32:13', 'checked_in', '2025-12-26 17:32:13', NULL, 0.00),
(36, 22, 12, '2025-12-26 09:32:18', 'checked_in', '2025-12-26 17:32:18', NULL, 0.00),
(37, 22, 13, '2025-12-26 09:32:26', 'checked_in', '2025-12-26 17:32:26', NULL, 0.00),
(38, 22, 15, '2025-12-26 09:32:35', 'checked_in', '2025-12-26 17:32:35', NULL, 0.00),
(39, 22, 16, '2025-12-26 09:32:40', 'checked_in', '2025-12-26 17:32:40', NULL, 0.00),
(40, 22, 17, '2025-12-26 09:32:45', 'checked_in', '2025-12-26 17:32:45', NULL, 0.00),
(41, 22, 18, '2025-12-26 09:32:50', 'checked_in', '2025-12-26 17:32:50', NULL, 0.00),
(42, 22, 19, '2025-12-26 09:32:53', 'checked_in', '2025-12-26 17:32:53', NULL, 0.00),
(43, 22, 20, '2025-12-26 09:32:57', 'checked_in', '2025-12-26 17:32:57', NULL, 0.00),
(44, 22, 21, '2025-12-26 09:33:14', 'checked_in', '2025-12-26 17:33:14', NULL, 0.00),
(45, 22, 23, '2025-12-26 09:35:28', 'checked_in', '2025-12-26 17:35:28', NULL, 0.00),
(46, 22, 24, '2025-12-26 09:35:38', 'checked_in', '2025-12-26 17:35:38', NULL, 0.00),
(47, 22, 25, '2025-12-26 09:35:47', 'checked_in', '2025-12-26 17:35:47', NULL, 0.00),
(48, 4, 12, '2025-12-26 09:39:54', 'registered', NULL, NULL, 0.00),
(49, 15, 12, '2025-12-26 10:26:43', 'checked_in', '2025-12-26 18:26:43', NULL, 0.00),
(50, 15, 13, '2025-12-26 10:26:51', 'checked_in', '2025-12-26 18:26:51', NULL, 0.00),
(51, 15, 14, '2025-12-26 10:26:56', 'checked_in', '2025-12-26 18:26:56', NULL, 0.00),
(52, 15, 15, '2025-12-26 10:27:01', 'checked_in', '2025-12-26 18:27:01', NULL, 0.00),
(53, 15, 16, '2025-12-26 10:31:47', 'checked_in', '2025-12-26 18:31:47', NULL, 0.00),
(54, 15, 17, '2025-12-26 10:31:53', 'checked_in', '2025-12-26 18:31:53', NULL, 0.00),
(55, 15, 18, '2025-12-26 10:31:58', 'checked_in', '2025-12-26 18:31:58', NULL, 0.00),
(56, 15, 27, '2025-12-26 10:32:03', 'checked_in', '2025-12-26 18:32:03', NULL, 4.30),
(57, 15, 26, '2025-12-26 10:32:07', 'checked_in', '2025-12-26 18:32:07', NULL, 0.00),
(58, 15, 24, '2025-12-26 10:32:13', 'checked_in', '2025-12-26 18:32:13', NULL, 0.00),
(59, 15, 21, '2025-12-26 10:32:31', 'checked_in', '2025-12-26 18:32:31', NULL, 0.00),
(60, 15, 22, '2025-12-26 10:32:39', 'checked_in', '2025-12-26 18:32:39', NULL, 0.00),
(61, 15, 23, '2025-12-26 10:32:55', 'checked_in', '2025-12-26 18:32:55', NULL, 0.00),
(62, 22, 27, '2025-12-26 11:06:38', 'registered', NULL, NULL, 0.00),
(63, 2, 27, '2025-12-26 11:06:50', 'registered', NULL, NULL, 0.00),
(64, 12, 12, '2025-12-26 11:29:11', 'checked_in', '2025-12-26 19:29:11', NULL, 0.00),
(65, 12, 13, '2025-12-26 11:29:15', 'checked_in', '2025-12-26 19:29:15', NULL, 0.00),
(66, 12, 14, '2025-12-26 11:29:20', 'checked_in', '2025-12-26 19:29:20', NULL, 0.00),
(67, 12, 26, '2025-12-26 11:29:33', 'checked_in', '2025-12-26 19:29:33', NULL, 0.00),
(68, 12, 20, '2025-12-26 11:29:41', 'checked_in', '2025-12-26 19:29:41', NULL, 0.00),
(69, 3, 27, '2025-12-26 12:22:52', 'registered', NULL, NULL, 0.00),
(70, 13, 27, '2025-12-26 12:22:59', 'attended', NULL, NULL, 0.00),
(71, 19, 27, '2025-12-26 12:27:08', 'registered', NULL, NULL, 0.00),
(72, 12, 15, '2025-12-26 13:34:15', 'checked_in', '2025-12-26 21:34:15', NULL, 0.00);

-- --------------------------------------------------------

--
-- Table structure for table `feedback`
--

CREATE TABLE `feedback` (
  `id` int(11) NOT NULL,
  `user_id` int(11) DEFAULT NULL,
  `subject` varchar(200) DEFAULT NULL,
  `message` text DEFAULT NULL,
  `feedback_type` varchar(50) DEFAULT 'general',
  `status` varchar(20) DEFAULT 'pending',
  `admin_reply` text DEFAULT NULL,
  `linked_item_type` varchar(50) DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `feedback`
--

INSERT INTO `feedback` (`id`, `user_id`, `subject`, `message`, `feedback_type`, `status`, `admin_reply`, `linked_item_type`, `created_at`, `updated_at`) VALUES
(1, 2, 'Great event!', 'The clean-up drive was fantastic!', 'appreciation', 'resolved', NULL, 'event', '2025-12-25 06:07:33', '2025-12-26 07:37:31'),
(2, 3, 'Technical issue', 'Website loading slowly', 'technical', 'resolved', NULL, NULL, '2025-12-25 06:07:33', '2025-12-26 07:37:37'),
(3, 4, 'Suggestion', 'More sports events please', 'suggestion', 'pending', NULL, 'event', '2025-12-25 06:07:33', '2025-12-26 08:29:58'),
(4, 6, 'Great Leadership Summit', 'The youth leadership summit was very informative and well-organized. Learned a lot!', 'appreciation', 'resolved', 'Thank you for your feedback! We are glad you enjoyed the event.', 'event', '2025-12-25 07:32:32', '2025-12-25 07:32:32'),
(11, 13, 'Need More Sports Events', 'We need more sports competitions for different age groups.', 'suggestion', 'resolved', NULL, NULL, '2025-12-25 07:32:32', '2025-12-26 13:38:59'),
(12, 14, 'Excellent Training', 'The digital literacy workshop was very helpful. The instructor was great!', 'appreciation', 'resolved', 'Thank you! We will share your feedback with the instructor.', 'event', '2025-12-25 07:32:32', '2025-12-25 07:32:32'),
(14, 6, 'Application Status', 'How long does it take to hear back about opportunity applications?', 'general', 'resolved', 'Applications are reviewed within 5-7 business days.', 'opportunity', '2025-12-25 07:32:32', '2025-12-25 07:32:32'),
(20, 12, 'Feedback on Awards System', 'The awards nomination process should be more transparent.', 'general', 'resolved', 'We are reviewing the awards process for improvements.', NULL, '2025-12-25 07:32:32', '2025-12-26 08:29:49'),
(21, 13, 'Volunteer Hours Tracking', 'Can we have a better system to track volunteer hours?', 'suggestion', 'resolved', 'A new volunteer tracking system will be implemented next month.', NULL, '2025-12-25 07:32:32', '2025-12-25 07:32:32'),
(22, 14, 'Excellent Support', 'The admin team was very helpful with my application.', 'appreciation', 'resolved', 'Thank you! We are here to help.', 'opportunity', '2025-12-25 07:32:32', '2025-12-25 07:32:32'),
(23, 15, 'Event Photos', 'When will the event photos be available online?', 'general', 'in progress', NULL, 'event', '2025-12-25 07:32:32', '2025-12-26 13:40:42'),
(24, 2, 'Appreciation Feedback', 'appreciate da food', 'appreciation', 'pending', NULL, 'event', '2025-12-25 08:54:31', '2025-12-26 13:49:15'),
(25, 27, 'Suggestion ra ni', 'nindot if daghan chairs para ma accomodate tanan attendees', 'suggestion', 'resolved', 'dont worry madame. mag daghan namig chairs sa sunod dam.\n', 'event', '2025-12-26 07:16:55', '2025-12-26 13:49:00'),
(26, 27, 'Appreciation for the Recently Held Activity', 'Thank you to the SK officials for the successful and well-coordinated event.', 'appreciation', 'pending', NULL, NULL, '2025-12-26 12:58:13', '2025-12-26 12:58:13');

-- --------------------------------------------------------

--
-- Table structure for table `opportunities`
--

CREATE TABLE `opportunities` (
  `id` int(11) NOT NULL,
  `title` varchar(200) NOT NULL,
  `type` varchar(50) NOT NULL,
  `description` text DEFAULT NULL,
  `compensation` varchar(100) DEFAULT NULL,
  `location` varchar(200) DEFAULT NULL,
  `commitment` varchar(100) DEFAULT NULL,
  `deadline` date DEFAULT NULL,
  `max_applicants` int(11) DEFAULT NULL,
  `current_applicants` int(11) DEFAULT 0,
  `status` varchar(20) DEFAULT 'open',
  `created_by` int(11) DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `opportunities`
--

INSERT INTO `opportunities` (`id`, `title`, `type`, `description`, `compensation`, `location`, `commitment`, `deadline`, `max_applicants`, `current_applicants`, `status`, `created_by`, `created_at`) VALUES
(1, 'SK Admin Assistant (Part-Time)', 'Job', 'Support SK council', 'P50/hr', 'SK Office', '20 hours/week', '2025-12-13', 2, 0, 'closed', 1, '2025-12-25 06:07:33'),
(2, 'Barangay Health Volunteer', 'Volunteer', 'Assist health center', 'None', 'Health Center', 'Flexible', NULL, 5, 0, 'open', 1, '2025-12-25 06:07:33'),
(3, 'Youth IT Intern', 'Internship', 'Website maintenance', 'Allowance', 'SK Office', '3 months', '2025-12-11', 3, 0, 'open', 1, '2025-12-25 06:07:33'),
(4, 'Youth Coordinator Assistant', 'Job', 'Assist in planning and implementing youth programs', '₱15,000/month', 'City Hall', 'Full-time', '2025-11-20', 2, 1, 'filled', 1, '2025-12-25 07:32:32'),
(5, 'Community Volunteer', 'Volunteer', 'Help in various community outreach programs', 'Volunteer Certificate', 'Purok Saging', 'Flexible hours', '2025-12-05', 50, 15, 'open', 2, '2025-12-25 07:32:32'),
(6, 'Marketing Intern', 'Internship', 'Digital marketing for youth programs', '₱8,000/month', 'Barangay Hall', '20 hours/week', '2025-12-16', 5, 3, 'open', 3, '2025-12-25 07:32:32'),
(7, 'First Aid Training Program', 'Training', 'Certified first aid and emergency response training', 'Free training', 'Red Cross Center', '3 days', '2025-12-09', 40, 28, 'open', 4, '2025-12-25 07:32:32'),
(8, 'Website Developer', 'Job', 'Develop and maintain SK website and portal', '₱20,000/month', 'Remote', 'Full-time', '2025-12-19', 1, 0, 'closed', 5, '2025-12-25 07:32:32'),
(9, 'Event Photographer', 'Job', 'Photograph SK events and activities', '₱12,000/month', 'Various locations', 'Part-time', '2025-11-22', 2, 1, 'open', 1, '2025-12-25 07:32:32'),
(10, 'Social Media Manager', 'Internship', 'Manage SK social media accounts', '₱6,000/month', 'Remote', '15 hours/week', '2025-11-22', 3, 2, 'open', 2, '2025-12-25 07:32:32'),
(11, 'Environmental Research Assistant', 'Volunteer', 'Assist in environmental research projects', 'Research experience', 'Rotonda Park', '10 hours/week', '2025-12-02', 10, 4, 'open', 3, '2025-12-25 07:32:32'),
(12, 'Graphic Design Workshop', 'Training', 'Professional graphic design skills training', '₱2,500 fee', 'Mega Gym, Dao', '5 sessions', '2025-12-17', 20, 12, 'open', 4, '2025-12-25 07:32:32'),
(13, 'Data Entry Clerk', 'Job', 'Input and manage youth program data', '₱10,000/month', 'SK Office', 'Full-time', '2025-12-17', 3, 2, 'filled', 5, '2025-12-25 07:32:32'),
(14, 'Basketball Coach', 'Job', 'Coach youth basketball teams', '₱8,000/month', 'Dao Sports Complex', 'Weekends only', '2025-11-26', 4, 3, 'open', 1, '2025-12-25 07:32:32'),
(15, 'Public Speaking Workshop', 'Training', 'Improve communication and presentation skills', '₱1,500 fee', 'University Campus', '2 days', '2025-12-09', 30, 18, 'open', 2, '2025-12-25 07:32:32'),
(16, 'Research Intern', 'Internship', 'Assist in youth development research', '₱5,000/month', 'Youth Research Center', '20 hours/week', '2025-12-04', 6, 4, 'open', 3, '2025-12-25 07:32:32'),
(17, 'Clean-up Drive Volunteer', 'Volunteer', 'Weekly community clean-up activities', 'Volunteer hours', 'Various barangays', 'Saturdays', '2025-12-12', 100, 45, 'open', 4, '2025-12-25 07:32:32'),
(18, 'Coding Bootcamp', 'Training', 'Learn web development and programming', '₱5,000 fee', 'DICT', '1 month', '2025-12-07', 25, 15, 'open', 5, '2025-12-25 07:32:32'),
(19, 'Administrative Assistant', 'Job', 'Office administration and support', '₱12,000/month', 'Barangay Hall', 'Full-time', '2025-11-26', 2, 1, 'closed', 1, '2025-12-25 07:32:32'),
(20, 'Art Workshop Facilitator', 'Volunteer', 'Lead art workshops for children', 'Art materials provided', 'Community Center', 'Weekends', '2025-11-07', 15, 8, 'open', 2, '2025-12-25 07:32:32'),
(21, 'Digital Marketing Course', 'Training', 'Comprehensive digital marketing training', '₱3,000 fee', 'Business Center', '4 weeks', '2025-12-08', 35, 22, 'open', 3, '2025-12-25 07:32:32'),
(22, 'Survey Enumerator', 'Job', 'Conduct youth surveys and interviews', '₱9,000/month', 'Field work', 'Part-time', '2025-12-04', 8, 6, 'open', 4, '2025-12-25 07:32:32'),
(23, 'Music Teacher', 'Volunteer', 'Teach basic music to underprivileged youth', 'Instrument provided', 'Plaza Luz Covered Court', 'Sundays', '2025-12-15', 10, 5, 'open', 5, '2025-12-25 07:32:32');

-- --------------------------------------------------------

--
-- Table structure for table `opportunity_applications`
--

CREATE TABLE `opportunity_applications` (
  `id` int(11) NOT NULL,
  `opportunity_id` int(11) DEFAULT NULL,
  `user_id` int(11) DEFAULT NULL,
  `application_date` timestamp NOT NULL DEFAULT current_timestamp(),
  `status` varchar(20) DEFAULT 'pending',
  `notes` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `opportunity_applications`
--

INSERT INTO `opportunity_applications` (`id`, `opportunity_id`, `user_id`, `application_date`, `status`, `notes`) VALUES
(1, 1, 27, '2025-04-13 02:30:00', 'accepted', 'Experience in youth leadership'),
(7, 4, 12, '2024-04-14 02:10:00', 'accepted', 'Completed basic first aid'),
(8, 4, 27, '2025-07-08 08:40:00', 'accepted', 'Healthcare background'),
(9, 5, 27, '2025-07-16 03:25:00', 'pending', 'Web development portfolio attached'),
(10, 6, 27, '2024-04-17 06:15:00', 'accepted', 'Professional photographer'),
(11, 7, 6, '2024-04-18 01:50:00', 'accepted', 'Social media management experience'),
(17, 13, 12, '2024-04-24 03:30:00', 'accepted', 'Research assistant experience'),
(18, 14, 13, '2024-04-25 05:45:00', 'accepted', 'Regular volunteer'),
(19, 15, 14, '2024-04-26 07:20:00', 'pending', 'Self-taught programmer'),
(20, 16, 15, '2024-04-27 02:15:00', 'rejected', 'Application submitted late'),
(21, 1, 2, '2025-12-25 08:55:12', 'accepted', NULL),
(22, 2, 27, '2025-12-26 07:12:39', 'accepted', NULL),
(23, 3, 27, '2025-12-26 07:13:49', 'pending', NULL),
(24, 12, 12, '2025-12-26 09:39:34', 'pending', NULL),
(25, 18, 12, '2025-12-26 09:39:44', 'pending', NULL);

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `name` varchar(100) NOT NULL,
  `email` varchar(100) NOT NULL,
  `password` varchar(255) NOT NULL,
  `role` varchar(20) DEFAULT 'youth',
  `status` varchar(20) DEFAULT 'active',
  `phone` varchar(20) DEFAULT NULL,
  `address` text DEFAULT NULL,
  `barangay` varchar(50) DEFAULT NULL,
  `birthdate` date DEFAULT NULL,
  `gender` varchar(20) DEFAULT NULL,
  `youth_id` varchar(50) DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`id`, `name`, `email`, `password`, `role`, `status`, `phone`, `address`, `barangay`, `birthdate`, `gender`, `youth_id`, `created_at`) VALUES
(1, 'SK Chairman', 'admin@sk.ph', '240be518fabd2724ddb6f04eeb1da5967448d7e831c08c8fa822809f74c720a9', 'admin', 'active', '09888782465', 'Purok Bingka', 'Kahayagan', '2000-05-30', 'Female', 'SK-ADMIN-001', '2025-12-25 06:07:33'),
(2, 'Carlowe Deala', 'youth1@sk.ph', '8a630de72b9c76f0978978cf1be92917fd8240f4975d53befcceaf938fe29901', 'youth', 'active', '09897889878', 'Purok Saging', 'Kahayagan', '2000-05-08', 'Male', 'SK-YOUTH-001', '2025-12-25 06:07:33'),
(3, 'Dave Labadan', 'youth2@sk.ph', '8a630de72b9c76f0978978cf1be92917fd8240f4975d53befcceaf938fe29901', 'youth', 'active', '09888789245', 'Purok Pinya', 'Kahayagan', '2000-05-08', 'Male', 'SK-YOUTH-002', '2025-12-25 06:07:33'),
(4, 'Danryl Usa', 'youth3@sk.ph', '8a630de72b9c76f0978978cf1be92917fd8240f4975d53befcceaf938fe29901', 'youth', 'active', '09888789012', 'Purok Bayabas', 'Kahayagan', '2005-05-20', 'Male', 'SK-YOUTH-003', '2025-12-25 06:07:33'),
(5, 'Christy Antone', 'youth4@sk.ph', '8a630de72b9c76f0978978cf1be92917fd8240f4975d53befcceaf938fe29901', 'youth', 'active', '09888789897', 'Purok Bingka', 'Kahayagan', '2002-05-08', 'Female', 'SK-YOUTH-004', '2025-12-25 06:07:33'),
(6, 'Josie Oliveros', 'youth5@sk.ph', '8a630de72b9c76f0978978cf1be92917fd8240f4975d53befcceaf938fe29901', 'youth', 'active', '09888789878', 'Purok Nangka', 'Kahayagan', '2000-05-08', 'Female', 'SK-YOUTH-005', '2025-12-25 06:07:33'),
(7, 'SK Secretary', 'admin1@sk.ph', '240be518fabd2724ddb6f04eeb1da5967448d7e831c08c8fa822809f74c720a9', 'admin', 'active', '09171234567', 'Purok Mangga', 'Kahayagan', '1985-05-15', 'Male', 'SK-ADMIN-002', '2025-12-25 07:32:32'),
(12, 'Marian Marchan', 'youth8@sk.ph', '8a630de72b9c76f0978978cf1be92917fd8240f4975d53befcceaf938fe29901', 'youth', 'active', '09171234501', 'Purok Pinya', 'Kahayagan', '2000-01-15', 'Male', 'SK-2024-001', '2025-12-25 07:32:32'),
(13, 'Regin Angala', 'maria.santos@sk.ph', '8a630de72b9c76f0978978cf1be92917fd8240f4975d53befcceaf938fe29901', 'youth', 'active', '09171234502', 'Purok Nangka', 'Kahayagan', '2001-03-22', 'Female', 'SK-2024-002', '2025-12-25 07:32:32'),
(14, 'Ace Estoya', 'pedro.reyes@sk.ph', '8a630de72b9c76f0978978cf1be92917fd8240f4975d53befcceaf938fe29901', 'youth', 'active', '09171234503', 'Purok Bayabas', 'Kahayagan', '1999-12-10', 'Male', 'SK-2024-003', '2025-12-25 07:32:32'),
(15, 'Vice Ganda', 'ana.lim@sk.ph', '8a630de72b9c76f0978978cf1be92917fd8240f4975d53befcceaf938fe29901', 'youth', 'active', '09171234504', 'Purok Mangga', 'Kahayagan', '2002-06-30', 'Female', 'SK-2024-004', '2025-12-25 07:32:32'),
(16, 'John Mira', 'miguel.torres@sk.ph', '8a630de72b9c76f0978978cf1be92917fd8240f4975d53befcceaf938fe29901', 'youth', 'active', '09171234505', 'Purok Kalamansi', 'Kahayagan', '2000-08-18', 'Male', 'SK-2024-005', '2025-12-25 07:32:32'),
(17, 'Sofia Garcia', 'sofia.garcia@sk.ph', 'e802505de82f2e3304757e928748c5e89c2de915a85231bfb62dd6953e6e6e0d', 'youth', 'active', '09171234506', 'Purok Mangga', 'Kahayagan', '2001-11-25', 'Female', 'SK-2024-006', '2025-12-25 07:32:32'),
(18, 'Anjo Fernandez', 'luis.fernandez@sk.ph', '8a630de72b9c76f0978978cf1be92917fd8240f4975d53befcceaf938fe29901', 'youth', 'active', '09171234507', 'Purok Kalamansi', 'Kahayagan', '2003-02-14', 'Male', 'SK-2024-007', '2025-12-25 07:32:32'),
(19, 'Kwen Bsnar', 'youth9@sk.ph', '8a630de72b9c76f0978978cf1be92917fd8240f4975d53befcceaf938fe29901', 'youth', 'active', '09171234508', 'Purok Bayabas', 'Kahayagan', '2000-09-05', 'Female', 'SK-2024-008', '2025-12-25 07:32:32'),
(20, 'Antonio Cruz', 'antonio.cruz@sk.ph', '8a630de72b9c76f0978978cf1be92917fd8240f4975d53befcceaf938fe29901', 'youth', 'active', '09171234509', 'Purok Pinya', 'Kahayagan', '2002-04-20', 'Male', 'SK-2024-009', '2025-12-25 07:32:32'),
(21, 'Isabel Mendoza', 'isabel.mendoza@sk.ph', '8a630de72b9c76f0978978cf1be92917fd8240f4975d53befcceaf938fe29901', 'youth', 'active', '09171234510', 'Purok Saging', 'Kahayagan', '2001-07-12', 'Female', 'SK-2024-010', '2025-12-25 07:32:32'),
(22, 'Carlos Lopez', 'carlos.lopez@sk.ph', '8a630de72b9c76f0978978cf1be92917fd8240f4975d53befcceaf938fe29901', 'youth', 'inactive', '09171234511', 'Purok Pinya', 'Kahayagan', '2003-10-08', 'Male', 'SK-2024-011', '2025-12-25 07:32:32'),
(23, 'Elena Castro', 'elena.castro@sk.ph', '8a630de72b9c76f0978978cf1be92917fd8240f4975d53befcceaf938fe29901', 'youth', 'inactive', '09171234512', 'Purok Mangga', 'Kahayagan', '2000-12-01', 'Female', 'SK-2024-012', '2025-12-25 07:32:32'),
(24, 'Jose Navarro', 'jose.navarro@sk.ph', '8a630de72b9c76f0978978cf1be92917fd8240f4975d53befcceaf938fe29901', 'youth', 'active', '09171234513', 'Purok Saging', 'Kahayagan', '2002-05-19', 'Male', 'SK-2024-013', '2025-12-25 07:32:32'),
(25, 'Rosa Chavez', 'rosa.chavez@sk.ph', '8a630de72b9c76f0978978cf1be92917fd8240f4975d53befcceaf938fe29901', 'youth', 'active', '09171234514', 'Purok Nangka', 'Kahayagan', '2001-08-27', 'Female', 'SK-2024-014', '2025-12-25 07:32:32'),
(26, 'Fernando Morales', 'fernando.morales@sk.ph', '8a630de72b9c76f0978978cf1be92917fd8240f4975d53befcceaf938fe29901', 'youth', 'inactive', '09171234515', 'Purok Mangga', 'Kahayagan', '2003-03-03', 'Male', 'SK-2024-015', '2025-12-25 07:32:32'),
(27, 'Quien Bisnar', 'youth6@sk.ph', '8a630de72b9c76f0978978cf1be92917fd8240f4975d53befcceaf938fe29901', 'youth', 'active', '09099989878', 'Purok Guyabano', 'Kahayagan', '1999-01-14', 'Female', 'SK-2024-016', '2024-12-11 07:34:01'),
(28, 'Drexzel Escoreal', 'youth7@sk.ph', '8a630de72b9c76f0978978cf1be92917fd8240f4975d53befcceaf938fe29901', 'youth', 'active', '09112541254', 'Purok Kalamansi', 'Kahayagan', NULL, 'Male', 'SK-2024-017', '2025-12-25 08:58:33');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `awards`
--
ALTER TABLE `awards`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`);

--
-- Indexes for table `events`
--
ALTER TABLE `events`
  ADD PRIMARY KEY (`id`),
  ADD KEY `created_by` (`created_by`);

--
-- Indexes for table `event_registrations`
--
ALTER TABLE `event_registrations`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `unique_event_user` (`event_id`,`user_id`),
  ADD KEY `user_id` (`user_id`);

--
-- Indexes for table `feedback`
--
ALTER TABLE `feedback`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`);

--
-- Indexes for table `opportunities`
--
ALTER TABLE `opportunities`
  ADD PRIMARY KEY (`id`),
  ADD KEY `created_by` (`created_by`);

--
-- Indexes for table `opportunity_applications`
--
ALTER TABLE `opportunity_applications`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `unique_opp_user` (`opportunity_id`,`user_id`),
  ADD KEY `user_id` (`user_id`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `email` (`email`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `awards`
--
ALTER TABLE `awards`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=21;

--
-- AUTO_INCREMENT for table `events`
--
ALTER TABLE `events`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=26;

--
-- AUTO_INCREMENT for table `event_registrations`
--
ALTER TABLE `event_registrations`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=73;

--
-- AUTO_INCREMENT for table `feedback`
--
ALTER TABLE `feedback`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=27;

--
-- AUTO_INCREMENT for table `opportunities`
--
ALTER TABLE `opportunities`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=24;

--
-- AUTO_INCREMENT for table `opportunity_applications`
--
ALTER TABLE `opportunity_applications`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=26;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=30;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `awards`
--
ALTER TABLE `awards`
  ADD CONSTRAINT `awards_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `events`
--
ALTER TABLE `events`
  ADD CONSTRAINT `events_ibfk_1` FOREIGN KEY (`created_by`) REFERENCES `users` (`id`);

--
-- Constraints for table `event_registrations`
--
ALTER TABLE `event_registrations`
  ADD CONSTRAINT `event_registrations_ibfk_1` FOREIGN KEY (`event_id`) REFERENCES `events` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `event_registrations_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `feedback`
--
ALTER TABLE `feedback`
  ADD CONSTRAINT `feedback_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `opportunities`
--
ALTER TABLE `opportunities`
  ADD CONSTRAINT `opportunities_ibfk_1` FOREIGN KEY (`created_by`) REFERENCES `users` (`id`);

--
-- Constraints for table `opportunity_applications`
--
ALTER TABLE `opportunity_applications`
  ADD CONSTRAINT `opportunity_applications_ibfk_1` FOREIGN KEY (`opportunity_id`) REFERENCES `opportunities` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `opportunity_applications_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
