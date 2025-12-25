-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1:3306
-- Generation Time: Dec 25, 2025 at 10:15 AM
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
(1, 6, 'Outstanding Youth Leader', 'Recognized for exceptional leadership in community projects', '2024-01-15', '2025-12-25 07:32:32'),
(2, 7, 'Community Service Award', 'Dedicated service in barangay clean-up drives', '2024-01-20', '2025-12-25 07:32:32'),
(3, 8, 'Academic Excellence', 'Top performer in youth development program', '2024-01-25', '2025-12-25 07:32:32'),
(4, 9, 'Sports Achievement', 'Champion in inter-barangay basketball tournament', '2024-02-05', '2025-12-25 07:32:32'),
(5, 10, 'Artistic Talent Award', 'First prize in youth painting competition', '2024-02-10', '2025-12-25 07:32:32'),
(6, 11, 'Environmental Advocate', 'Outstanding contribution to tree planting activities', '2024-02-15', '2025-12-25 07:32:32'),
(7, 12, 'Public Speaking Champion', 'Winner in youth debate competition', '2024-02-20', '2025-12-25 07:32:32'),
(8, 13, 'Technology Innovator', 'Best project in youth tech expo', '2024-02-25', '2025-12-25 07:32:32'),
(9, 14, 'Cultural Preservation', 'Excellence in traditional dance performance', '2024-03-01', '2025-12-25 07:32:32'),
(10, 15, 'Entrepreneurial Spirit', 'Outstanding business proposal in youth forum', '2024-03-05', '2025-12-25 07:32:32'),
(11, 6, 'Volunteer of the Month', 'Most dedicated volunteer for March 2024', '2024-03-10', '2025-12-25 07:32:32'),
(12, 7, 'Leadership Excellence', 'Outstanding performance in leadership training', '2024-03-15', '2025-12-25 07:32:32'),
(13, 8, 'Team Player Award', 'Exceptional teamwork in community projects', '2024-03-20', '2025-12-25 07:32:32'),
(14, 9, 'Creative Writing Award', 'First prize in youth essay writing contest', '2024-03-25', '2025-12-25 07:32:32'),
(15, 10, 'Scientific Achievement', 'Best project in youth science fair', '2024-03-30', '2025-12-25 07:32:32'),
(16, 11, 'Musical Talent', 'Outstanding performance in music festival', '2024-04-05', '2025-12-25 07:32:32'),
(17, 12, 'Disaster Response Hero', 'Bravery and quick response during disaster drill', '2024-04-10', '2025-12-25 07:32:32'),
(18, 13, 'Health Advocate', 'Active participation in health awareness campaigns', '2024-04-15', '2025-12-25 07:32:32'),
(19, 14, 'Digital Literacy Champion', 'Top performer in computer training', '2024-04-20', '2025-12-25 07:32:32'),
(20, 15, 'Youth Ambassador', 'Represented SK in regional youth conference', '2024-04-25', '2025-12-25 07:32:32');

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
(1, 'Coastal Clean-Up Drive', 'Environmental clean-up activity', '2024-12-20', '09:00:00', 'Beachfront', 'Volunteer', 100, 0, 'upcoming', 1, '2025-12-25 06:07:33'),
(2, 'Youth Leadership Summit', 'Leadership training workshop', '2024-12-25', '10:00:00', 'Barangay Hall', 'Seminar', 150, 0, 'upcoming', 1, '2025-12-25 06:07:33'),
(3, 'Christmas Party', 'Annual youth Christmas celebration', '2024-12-23', '18:00:00', 'Community Center', 'Social', 200, 0, 'upcoming', 1, '2025-12-25 06:07:33'),
(4, 'Basketball Tournament', 'Inter-purok basketball competition', '2024-12-28', '14:00:00', 'Sports Complex', 'Sports', 50, 0, 'upcoming', 1, '2025-12-25 06:07:33'),
(5, 'First Aid Training', 'Basic first aid certification', '2025-01-05', '08:00:00', 'Health Center', 'Training', 30, 0, 'upcoming', 1, '2025-12-25 06:07:33'),
(6, 'Youth Leadership Summit', 'Annual leadership training for SK youth leaders', '2024-03-15', '09:00:00', 'Quezon City Convention Center', 'Seminar', 200, 150, 'completed', 1, '2025-12-25 07:32:32'),
(7, 'Community Clean-up Drive', 'Barangay-wide clean-up activity', '2024-03-20', '07:00:00', 'Barangay 1 Covered Court', 'Volunteer', 100, 85, 'completed', 2, '2025-12-25 07:32:32'),
(8, 'Basketball Tournament', 'Inter-barangay basketball competition', '2024-04-05', '14:00:00', 'City Sports Complex', 'Sports', 16, 16, 'completed', 3, '2025-12-25 07:32:32'),
(9, 'Digital Literacy Workshop', 'Basic computer skills training for youth', '2024-04-12', '10:00:00', 'Public Library Computer Lab', 'Training', 30, 28, 'completed', 4, '2025-12-25 07:32:32'),
(10, 'Youth Entrepreneurship Forum', 'Business ideas and startup discussions', '2024-04-25', '13:00:00', 'Business Center Auditorium', 'Seminar', 80, 72, 'completed', 5, '2025-12-25 07:32:32'),
(11, 'Environmental Awareness Campaign', 'Tree planting and eco-education', '2024-05-10', '08:00:00', 'City Eco-Park', 'Volunteer', 150, 120, 'upcoming', 1, '2025-12-25 07:32:32'),
(12, 'Cultural Dance Festival', 'Traditional dance performances and competition', '2024-05-18', '16:00:00', 'City Cultural Center', 'Social', 300, 210, 'upcoming', 2, '2025-12-25 07:32:32'),
(13, 'First Aid Training', 'Basic life support and emergency response', '2024-05-22', '09:00:00', 'Red Cross Training Center', 'Training', 40, 35, 'upcoming', 3, '2025-12-25 07:32:32'),
(14, 'Youth Job Fair', 'Employment opportunities for young people', '2024-06-05', '10:00:00', 'SM Mega Trade Hall', 'Seminar', 500, 320, 'upcoming', 4, '2025-12-25 07:32:32'),
(15, 'Anti-Drug Awareness Seminar', 'Prevention and education program', '2024-06-12', '14:00:00', 'Barangay Hall', 'Seminar', 80, 65, 'upcoming', 5, '2025-12-25 07:32:32'),
(16, 'Swimming Competition', 'Inter-school swimming tournament', '2024-06-20', '08:00:00', 'City Olympic Pool', 'Sports', 50, 42, 'upcoming', 1, '2025-12-25 07:32:32'),
(17, 'Art Workshop', 'Painting and creative arts training', '2024-06-25', '13:00:00', 'City Art Gallery', 'Training', 25, 22, 'upcoming', 2, '2025-12-25 07:32:32'),
(18, 'Youth Christmas Party', 'Annual holiday celebration for SK members', '2024-12-15', '18:00:00', 'Barangay Covered Court', 'Social', 200, 180, 'upcoming', 3, '2025-12-25 07:32:32'),
(19, 'Disaster Preparedness Drill', 'Earthquake and fire safety演习', '2024-07-10', '07:00:00', 'Evacuation Center', 'Training', 100, 85, 'ongoing', 4, '2025-12-25 07:32:32'),
(20, 'Music Festival', 'Local band performances and competitions', '2024-07-20', '17:00:00', 'City Plaza', 'Social', 400, 310, 'ongoing', 5, '2025-12-25 07:32:32'),
(21, 'Public Speaking Workshop', 'Communication skills development', '2024-08-05', '10:00:00', 'University Auditorium', 'Training', 60, 52, 'ongoing', 1, '2025-12-25 07:32:32'),
(22, 'Blood Donation Drive', 'Community blood donation activity', '2024-08-12', '09:00:00', 'City Health Center', 'Volunteer', 100, 78, 'ongoing', 2, '2025-12-25 07:32:32'),
(23, 'Debate Tournament', 'Inter-school debate competition', '2024-08-20', '14:00:00', 'City University', 'Seminar', 32, 30, 'ongoing', 3, '2025-12-25 07:32:32'),
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
(5, 1, 6, '2024-03-10 02:30:00', 'attended', '2024-03-15 08:45:00', '2024-03-15 17:30:00', 8.50),
(6, 1, 7, '2024-03-11 06:20:00', 'attended', '2024-03-15 08:30:00', '2024-03-15 17:00:00', 8.00),
(7, 1, 8, '2024-03-12 01:15:00', 'absent', NULL, NULL, 0.00),
(8, 2, 9, '2024-03-18 03:00:00', 'attended', '2024-03-20 06:45:00', '2024-03-20 12:00:00', 5.25),
(9, 2, 10, '2024-03-19 07:30:00', 'attended', '2024-03-20 07:00:00', '2024-03-20 11:30:00', 4.50),
(10, 3, 11, '2024-04-01 05:20:00', 'attended', '2024-04-05 13:30:00', '2024-04-05 18:00:00', 4.50),
(11, 3, 12, '2024-04-02 02:45:00', 'attended', '2024-04-05 13:45:00', '2024-04-05 17:45:00', 4.00),
(12, 4, 13, '2024-04-10 08:00:00', 'attended', '2024-04-12 09:30:00', '2024-04-12 16:00:00', 6.50),
(13, 4, 14, '2024-04-11 03:15:00', 'attended', '2024-04-12 09:45:00', '2024-04-12 15:30:00', 5.75),
(14, 5, 15, '2024-04-22 06:50:00', 'attended', '2024-04-25 12:30:00', '2024-04-25 18:00:00', 5.50),
(15, 5, 6, '2024-04-23 01:40:00', 'attended', '2024-04-25 12:45:00', '2024-04-25 17:30:00', 4.75),
(16, 6, 7, '2024-05-05 02:20:00', 'registered', NULL, NULL, 0.00),
(17, 6, 8, '2024-05-06 06:35:00', 'registered', NULL, NULL, 0.00),
(18, 7, 9, '2024-05-15 03:10:00', 'registered', NULL, NULL, 0.00),
(19, 7, 10, '2024-05-16 08:25:00', 'registered', NULL, NULL, 0.00),
(20, 8, 11, '2024-05-20 01:45:00', 'checked_in', '2024-05-22 08:30:00', NULL, 0.00),
(21, 9, 12, '2024-06-01 05:20:00', 'registered', NULL, NULL, 0.00),
(22, 10, 13, '2024-06-10 02:15:00', 'registered', NULL, NULL, 0.00),
(23, 11, 14, '2024-06-18 06:40:00', 'registered', NULL, NULL, 0.00),
(24, 13, 15, '2025-12-25 07:42:57', 'checked_in', '2025-12-25 15:42:57', NULL, 0.00),
(25, 13, 2, '2025-12-25 08:53:22', 'registered', NULL, NULL, 0.00),
(26, 18, 2, '2025-12-25 08:55:38', 'registered', NULL, NULL, 0.00),
(27, 11, 27, '2025-12-25 08:59:38', 'checked_in', '2025-12-25 16:59:38', NULL, 0.00),
(28, 11, 28, '2025-12-25 08:59:45', 'checked_in', '2025-12-25 16:59:45', NULL, 0.00),
(29, 20, 26, '2025-12-25 09:00:02', 'checked_in', '2025-12-25 17:00:02', NULL, 0.00),
(30, 12, 27, '2025-12-25 09:00:11', 'checked_in', '2025-12-25 17:00:11', NULL, 0.00),
(31, 12, 22, '2025-12-25 09:00:17', 'checked_in', '2025-12-25 17:00:17', NULL, 0.00),
(32, 12, 21, '2025-12-25 09:00:24', 'checked_in', '2025-12-25 17:00:24', NULL, 0.00);

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
  `linked_item_id` int(11) DEFAULT NULL,
  `linked_item_type` varchar(50) DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `feedback`
--

INSERT INTO `feedback` (`id`, `user_id`, `subject`, `message`, `feedback_type`, `status`, `admin_reply`, `linked_item_id`, `linked_item_type`, `created_at`, `updated_at`) VALUES
(1, 2, 'Great event!', 'The clean-up drive was fantastic!', 'appreciation', 'pending', NULL, NULL, NULL, '2025-12-25 06:07:33', '2025-12-25 06:07:33'),
(2, 3, 'Technical issue', 'Website loading slowly', 'technical', 'pending', NULL, NULL, NULL, '2025-12-25 06:07:33', '2025-12-25 06:07:33'),
(3, 4, 'Suggestion', 'More sports events please', 'suggestion', 'pending', NULL, NULL, NULL, '2025-12-25 06:07:33', '2025-12-25 06:07:33'),
(4, 6, 'Great Leadership Summit', 'The youth leadership summit was very informative and well-organized. Learned a lot!', 'appreciation', 'resolved', 'Thank you for your feedback! We are glad you enjoyed the event.', 1, 'event', '2025-12-25 07:32:32', '2025-12-25 07:32:32'),
(5, 7, 'Venue Issue', 'The sound system at the basketball tournament was not working properly.', 'complaint', 'resolved', 'We apologize for the inconvenience. The sound system has been repaired for future events.', 3, 'event', '2025-12-25 07:32:32', '2025-12-25 07:32:32'),
(6, 8, 'Suggestion for More Workshops', 'Can we have more hands-on workshops instead of just seminars?', 'suggestion', 'in progress', 'Thank you for the suggestion! We are planning more workshop-based events.', NULL, NULL, '2025-12-25 07:32:32', '2025-12-25 07:32:32'),
(7, 9, 'Registration Process', 'The online registration for events is confusing. Can it be simplified?', 'technical', 'resolved', 'We are working on improving the registration interface. Thank you for pointing this out.', NULL, NULL, '2025-12-25 07:32:32', '2025-12-25 07:32:32'),
(8, 10, 'Clean-up Drive Appreciation', 'The community clean-up was very successful. Thank you for organizing!', 'appreciation', 'resolved', 'We appreciate your participation! Together we can keep our community clean.', 2, 'event', '2025-12-25 07:32:32', '2025-12-25 07:32:32'),
(9, 11, 'Event Timing', 'Some events start too early in the morning. Can we have later options?', 'suggestion', 'pending', NULL, NULL, NULL, '2025-12-25 07:32:32', '2025-12-25 07:32:32'),
(10, 12, 'Website Bug', 'Cannot upload documents in the opportunity application form.', 'technical', 'resolved', 'The bug has been fixed. Please try again.', 5, 'opportunity', '2025-12-25 07:32:32', '2025-12-25 07:32:32'),
(11, 13, 'Need More Sports Events', 'We need more sports competitions for different age groups.', 'suggestion', 'pending', NULL, NULL, NULL, '2025-12-25 07:32:32', '2025-12-25 07:32:32'),
(12, 14, 'Excellent Training', 'The digital literacy workshop was very helpful. The instructor was great!', 'appreciation', 'resolved', 'Thank you! We will share your feedback with the instructor.', 4, 'event', '2025-12-25 07:32:32', '2025-12-25 07:32:32'),
(13, 15, 'Poor Communication', 'Event details were not communicated clearly via email.', 'complaint', 'resolved', 'We apologize and have improved our communication system.', 1, 'event', '2025-12-25 07:32:32', '2025-12-25 07:32:32'),
(14, 6, 'Application Status', 'How long does it take to hear back about opportunity applications?', 'general', 'resolved', 'Applications are reviewed within 5-7 business days.', 1, 'opportunity', '2025-12-25 07:32:32', '2025-12-25 07:32:32'),
(15, 7, 'Certificate Issue', 'Did not receive certificate for completed training.', 'technical', 'in progress', 'We are checking our records and will issue the certificate.', 4, 'event', '2025-12-25 07:32:32', '2025-12-25 07:32:32'),
(16, 8, 'Suggestion: Youth Forum', 'Can we have a monthly youth forum to discuss concerns?', 'suggestion', 'pending', NULL, NULL, NULL, '2025-12-25 07:32:32', '2025-12-25 07:32:32'),
(17, 9, 'Great Job Fair', 'The youth job fair helped me find employment. Thank you!', 'appreciation', 'resolved', 'Congratulations! We are happy to hear about your success.', 9, 'event', '2025-12-25 07:32:32', '2025-12-25 07:32:32'),
(18, 10, 'Website Slow', 'The SK portal website loads very slowly.', 'technical', 'resolved', 'We have optimized the website for better performance.', NULL, NULL, '2025-12-25 07:32:32', '2025-12-25 07:32:32'),
(19, 11, 'Need More Cultural Events', 'We should have more events showcasing local culture.', 'suggestion', 'pending', NULL, NULL, NULL, '2025-12-25 07:32:32', '2025-12-25 07:32:32'),
(20, 12, 'Feedback on Awards System', 'The awards nomination process should be more transparent.', 'general', 'in progress', 'We are reviewing the awards process for improvements.', NULL, NULL, '2025-12-25 07:32:32', '2025-12-25 07:32:32'),
(21, 13, 'Volunteer Hours Tracking', 'Can we have a better system to track volunteer hours?', 'suggestion', 'resolved', 'A new volunteer tracking system will be implemented next month.', NULL, NULL, '2025-12-25 07:32:32', '2025-12-25 07:32:32'),
(22, 14, 'Excellent Support', 'The admin team was very helpful with my application.', 'appreciation', 'resolved', 'Thank you! We are here to help.', 3, 'opportunity', '2025-12-25 07:32:32', '2025-12-25 07:32:32'),
(23, 15, 'Event Photos', 'When will the event photos be available online?', 'general', 'pending', NULL, 2, 'event', '2025-12-25 07:32:32', '2025-12-25 07:32:32'),
(24, 2, 'Appreciation Feedback', 'appreciate da food', 'appreciation', 'pending', NULL, NULL, NULL, '2025-12-25 08:54:31', '2025-12-25 08:54:31');

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
(1, 'SK Admin Assistant (Part-Time)', 'Job', 'Support SK council', 'P50/hr', 'SK Office', '20 hours/week', '2024-12-31', 2, 0, 'open', 1, '2025-12-25 06:07:33'),
(2, 'Barangay Health Volunteer', 'Volunteer', 'Assist health center', 'None', 'Health Center', 'Flexible', NULL, 5, 0, 'open', 1, '2025-12-25 06:07:33'),
(3, 'Youth IT Intern', 'Internship', 'Website maintenance', 'Allowance', 'SK Office', '3 months', '2025-01-15', 3, 0, 'open', 1, '2025-12-25 06:07:33'),
(4, 'Youth Coordinator Assistant', 'Job', 'Assist in planning and implementing youth programs', '₱15,000/month', 'Quezon City Hall', 'Full-time', '2024-04-30', 2, 1, 'filled', 1, '2025-12-25 07:32:32'),
(5, 'Community Volunteer', 'Volunteer', 'Help in various community outreach programs', 'Volunteer Certificate', 'Barangay 1-15', 'Flexible hours', '2024-12-31', 50, 15, 'open', 2, '2025-12-25 07:32:32'),
(6, 'Marketing Intern', 'Internship', 'Digital marketing for youth programs', '₱8,000/month', 'SK Office, Makati', '20 hours/week', '2024-05-15', 5, 3, 'open', 3, '2025-12-25 07:32:32'),
(7, 'First Aid Training Program', 'Training', 'Certified first aid and emergency response training', 'Free training', 'Red Cross Center', '3 days', '2024-06-30', 40, 28, 'open', 4, '2025-12-25 07:32:32'),
(8, 'Website Developer', 'Job', 'Develop and maintain SK website and portal', '₱20,000/month', 'Remote', 'Full-time', '2024-05-10', 1, 0, 'closed', 5, '2025-12-25 07:32:32'),
(9, 'Event Photographer', 'Job', 'Photograph SK events and activities', '₱12,000/month', 'Various locations', 'Part-time', '2024-05-20', 2, 1, 'open', 1, '2025-12-25 07:32:32'),
(10, 'Social Media Manager', 'Internship', 'Manage SK social media accounts', '₱6,000/month', 'Remote', '15 hours/week', '2024-06-15', 3, 2, 'open', 2, '2025-12-25 07:32:32'),
(11, 'Environmental Research Assistant', 'Volunteer', 'Assist in environmental research projects', 'Research experience', 'City Eco-Park', '10 hours/week', '2024-07-31', 10, 4, 'open', 3, '2025-12-25 07:32:32'),
(12, 'Graphic Design Workshop', 'Training', 'Professional graphic design skills training', '₱2,500 fee', 'Design Studio, BGC', '5 sessions', '2024-05-31', 20, 12, 'open', 4, '2025-12-25 07:32:32'),
(13, 'Data Entry Clerk', 'Job', 'Input and manage youth program data', '₱10,000/month', 'SK Office, Pasig', 'Full-time', '2024-05-05', 3, 2, 'filled', 5, '2025-12-25 07:32:32'),
(14, 'Basketball Coach', 'Job', 'Coach youth basketball teams', '₱8,000/month', 'City Sports Complex', 'Weekends only', '2024-05-25', 4, 3, 'open', 1, '2025-12-25 07:32:32'),
(15, 'Public Speaking Workshop', 'Training', 'Improve communication and presentation skills', '₱1,500 fee', 'University Campus', '2 days', '2024-06-10', 30, 18, 'open', 2, '2025-12-25 07:32:32'),
(16, 'Research Intern', 'Internship', 'Assist in youth development research', '₱5,000/month', 'Youth Research Center', '20 hours/week', '2024-07-15', 6, 4, 'open', 3, '2025-12-25 07:32:32'),
(17, 'Clean-up Drive Volunteer', 'Volunteer', 'Weekly community clean-up activities', 'Volunteer hours', 'Various barangays', 'Saturdays', '2024-12-31', 100, 45, 'open', 4, '2025-12-25 07:32:32'),
(18, 'Coding Bootcamp', 'Training', 'Learn web development and programming', '₱5,000 fee', 'Tech Hub, Makati', '1 month', '2024-06-30', 25, 15, 'open', 5, '2025-12-25 07:32:32'),
(19, 'Administrative Assistant', 'Job', 'Office administration and support', '₱12,000/month', 'SK Main Office', 'Full-time', '2024-05-08', 2, 1, 'closed', 1, '2025-12-25 07:32:32'),
(20, 'Art Workshop Facilitator', 'Volunteer', 'Lead art workshops for children', 'Art materials provided', 'Community Center', 'Weekends', '2024-08-31', 15, 8, 'open', 2, '2025-12-25 07:32:32'),
(21, 'Digital Marketing Course', 'Training', 'Comprehensive digital marketing training', '₱3,000 fee', 'Business Center', '4 weeks', '2024-06-20', 35, 22, 'open', 3, '2025-12-25 07:32:32'),
(22, 'Survey Enumerator', 'Job', 'Conduct youth surveys and interviews', '₱9,000/month', 'Field work', 'Part-time', '2024-05-30', 8, 6, 'open', 4, '2025-12-25 07:32:32'),
(23, 'Music Teacher', 'Volunteer', 'Teach basic music to underprivileged youth', 'Instrument provided', 'Music School', 'Sundays', '2024-09-30', 10, 5, 'open', 5, '2025-12-25 07:32:32');

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
(1, 1, 6, '2024-04-15 02:30:00', 'accepted', 'Experience in youth leadership'),
(2, 1, 7, '2024-04-16 06:20:00', 'rejected', 'Lacking relevant experience'),
(3, 2, 8, '2024-04-10 01:15:00', 'pending', 'Available on weekends'),
(4, 2, 9, '2024-04-11 03:45:00', 'accepted', 'Previous volunteer experience'),
(5, 3, 10, '2024-04-12 05:30:00', 'accepted', 'Marketing student'),
(6, 3, 11, '2024-04-13 07:20:00', 'pending', 'Interested in digital marketing'),
(7, 4, 12, '2024-04-14 02:10:00', 'accepted', 'Completed basic first aid'),
(8, 4, 13, '2024-04-15 08:40:00', 'accepted', 'Healthcare background'),
(9, 5, 14, '2024-04-16 03:25:00', 'pending', 'Web development portfolio attached'),
(10, 6, 15, '2024-04-17 06:15:00', 'accepted', 'Professional photographer'),
(11, 7, 6, '2024-04-18 01:50:00', 'accepted', 'Social media management experience'),
(12, 8, 7, '2024-04-19 05:20:00', 'pending', 'Environmental science student'),
(13, 9, 8, '2024-04-20 07:30:00', 'accepted', 'Graphic design student'),
(14, 10, 9, '2024-04-21 02:45:00', 'rejected', 'Position already filled'),
(15, 11, 10, '2024-04-22 06:10:00', 'accepted', 'Basketball varsity player'),
(16, 12, 11, '2024-04-23 08:25:00', 'pending', 'Wants to improve public speaking'),
(17, 13, 12, '2024-04-24 03:30:00', 'accepted', 'Research assistant experience'),
(18, 14, 13, '2024-04-25 05:45:00', 'accepted', 'Regular volunteer'),
(19, 15, 14, '2024-04-26 07:20:00', 'pending', 'Self-taught programmer'),
(20, 16, 15, '2024-04-27 02:15:00', 'rejected', 'Application submitted late'),
(21, 1, 2, '2025-12-25 08:55:12', 'pending', NULL);

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
(1, 'SK Officer', 'admin@sk.ph', '240be518fabd2724ddb6f04eeb1da5967448d7e831c08c8fa822809f74c720a9', 'admin', 'active', NULL, 'Purok Bayabas', 'Kahayagan', NULL, 'Female', 'SK-ADMIN-001', '2025-12-25 06:07:33'),
(2, 'Carlowe Deala', 'youth1@example.com', '8a630de72b9c76f0978978cf1be92917fd8240f4975d53befcceaf938fe29901', 'youth', 'active', '09897889878', 'Purok Mangga', 'Kahayagan', NULL, 'Male', 'SK-YOUTH-001', '2025-12-25 06:07:33'),
(3, 'Dave Labadan', 'youth2@example.com', '8a630de72b9c76f0978978cf1be92917fd8240f4975d53befcceaf938fe29901', 'youth', 'active', NULL, 'Purok Pinya', 'Kahayagan', NULL, 'Male', 'SK-YOUTH-002', '2025-12-25 06:07:33'),
(4, 'Danryl Usa', 'youth3@example.com', '8a630de72b9c76f0978978cf1be92917fd8240f4975d53befcceaf938fe29901', 'youth', 'active', NULL, 'Purok Bayabas', 'Kahayagan', NULL, 'Male', 'SK-YOUTH-003', '2025-12-25 06:07:33'),
(5, 'Christy Antone', 'youth4@example.com', '8a630de72b9c76f0978978cf1be92917fd8240f4975d53befcceaf938fe29901', 'youth', 'active', NULL, 'Purok Bayabas', 'Kahayagan', NULL, 'Female', 'SK-YOUTH-004', '2025-12-25 06:07:33'),
(6, 'Josie Oliveros', 'youth5@example.com', '8a630de72b9c76f0978978cf1be92917fd8240f4975d53befcceaf938fe29901', 'youth', 'active', NULL, 'Purok Nangka', 'Kahayagan', NULL, 'Female', 'SK-YOUTH-005', '2025-12-25 06:07:33'),
(7, 'SK Secretary', 'admin1@sk.ph', '240be518fabd2724ddb6f04eeb1da5967448d7e831c08c8fa822809f74c720a9', 'admin', 'active', '09171234567', 'Purok Mangga', 'Kahayagan', '1985-05-15', 'Male', 'SK-ADMIN-002', '2025-12-25 07:32:32'),
(8, 'SK Chairman', 'admin2@sk.ph', '240be518fabd2724ddb6f04eeb1da5967448d7e831c08c8fa822809f74c720a9', 'admin', 'active', '09171234568', 'Purok Pinya', 'Kahayagan', '1990-08-22', 'Female', 'SK-ADMIN-003', '2025-12-25 07:32:32'),
(9, 'SK Officer', 'admin3@sk.ph', '240be518fabd2724ddb6f04eeb1da5967448d7e831c08c8fa822809f74c720a9', 'admin', 'active', '09171234569', 'Purok Pinya', 'Kahayagan', '1988-03-10', 'Male', 'SK-ADMIN-004', '2025-12-25 07:32:32'),
(10, 'SK Officer', 'admin4@sk.ph', '240be518fabd2724ddb6f04eeb1da5967448d7e831c08c8fa822809f74c720a9', 'admin', 'active', '09171234570', 'Purok Saging', 'Kahayagan', '1992-11-30', 'Female', 'SK-ADMIN-005', '2025-12-25 07:32:32'),
(11, 'SK Officer', 'admin5@sk.ph', '240be518fabd2724ddb6f04eeb1da5967448d7e831c08c8fa822809f74c720a9', 'admin', 'active', '09171234571', 'Purok Bayabas', 'Kahayagan', '1995-07-18', 'Male', 'SK-ADMIN-006', '2025-12-25 07:32:32'),
(12, 'Marian Marchan', 'youth8@example.com', '8a630de72b9c76f0978978cf1be92917fd8240f4975d53befcceaf938fe29901', 'youth', 'active', '09171234501', 'Purok Pinya', 'Kahayagan', '2000-01-15', 'Male', 'SK-2024-001', '2025-12-25 07:32:32'),
(13, 'Maria Santos', 'maria.santos@sk.ph', '8a630de72b9c76f0978978cf1be92917fd8240f4975d53befcceaf938fe29901', 'youth', 'active', '09171234502', 'Purok Nangka', 'Kahayagan', '2001-03-22', 'Female', 'SK-2024-002', '2025-12-25 07:32:32'),
(14, 'Pedro Reyes', 'pedro.reyes@sk.ph', '8a630de72b9c76f0978978cf1be92917fd8240f4975d53befcceaf938fe29901', 'youth', 'active', '09171234503', 'Purok Bayabas', 'Kahayagan', '1999-12-10', 'Male', 'SK-2024-003', '2025-12-25 07:32:32'),
(15, 'Ana Lim', 'ana.lim@sk.ph', '8a630de72b9c76f0978978cf1be92917fd8240f4975d53befcceaf938fe29901', 'youth', 'active', '09171234504', 'Purok Mangga', 'Kahayagan', '2002-06-30', 'Female', 'SK-2024-004', '2025-12-25 07:32:32'),
(16, 'Miguel Torres', 'miguel.torres@sk.ph', '8a630de72b9c76f0978978cf1be92917fd8240f4975d53befcceaf938fe29901', 'youth', 'active', '09171234505', 'Purok Kalamansi', 'Kahayagan', '2000-08-18', 'Male', 'SK-2024-005', '2025-12-25 07:32:32'),
(17, 'Sofia Garcia', 'sofia.garcia@sk.ph', '8a630de72b9c76f0978978cf1be92917fd8240f4975d53befcceaf938fe29901', 'youth', 'active', '09171234506', 'Purok Mangga', 'Kahayagan', '2001-11-25', 'Female', 'SK-2024-006', '2025-12-25 07:32:32'),
(18, 'Luis Fernandez', 'luis.fernandez@sk.ph', '8a630de72b9c76f0978978cf1be92917fd8240f4975d53befcceaf938fe29901', 'youth', 'active', '09171234507', 'Purok Kalamansi', 'Kahayagan', '2003-02-14', 'Male', 'SK-2024-007', '2025-12-25 07:32:32'),
(19, 'Carmen Ramos', 'carmen.ramos@sk.ph', '8a630de72b9c76f0978978cf1be92917fd8240f4975d53befcceaf938fe29901', 'youth', 'pending', '09171234508', 'Purok Bayabas', 'Kahayagan', '2000-09-05', 'Female', 'SK-2024-008', '2025-12-25 07:32:32'),
(20, 'Antonio Cruz', 'antonio.cruz@sk.ph', '8a630de72b9c76f0978978cf1be92917fd8240f4975d53befcceaf938fe29901', 'youth', 'active', '09171234509', 'Purok Pinya', 'Kahayagan', '2002-04-20', 'Male', 'SK-2024-009', '2025-12-25 07:32:32'),
(21, 'Isabel Mendoza', 'isabel.mendoza@sk.ph', '8a630de72b9c76f0978978cf1be92917fd8240f4975d53befcceaf938fe29901', 'youth', 'active', '09171234510', 'Purok Saging', 'Kahayagan', '2001-07-12', 'Female', 'SK-2024-010', '2025-12-25 07:32:32'),
(22, 'Carlos Lopez', 'carlos.lopez@sk.ph', '8a630de72b9c76f0978978cf1be92917fd8240f4975d53befcceaf938fe29901', 'youth', 'pending', '09171234511', 'Purok Pinya', 'Kahayagan', '2003-10-08', 'Male', 'SK-2024-011', '2025-12-25 07:32:32'),
(23, 'Elena Castro', 'elena.castro@sk.ph', '8a630de72b9c76f0978978cf1be92917fd8240f4975d53befcceaf938fe29901', 'youth', 'active', '09171234512', 'Purok Mangga', 'Kahayagan', '2000-12-01', 'Female', 'SK-2024-012', '2025-12-25 07:32:32'),
(24, 'Jose Navarro', 'jose.navarro@sk.ph', '8a630de72b9c76f0978978cf1be92917fd8240f4975d53befcceaf938fe29901', 'youth', 'active', '09171234513', 'Purok Saging', 'Kahayagan', '2002-05-19', 'Male', 'SK-2024-013', '2025-12-25 07:32:32'),
(25, 'Rosa Chavez', 'rosa.chavez@sk.ph', '8a630de72b9c76f0978978cf1be92917fd8240f4975d53befcceaf938fe29901', 'youth', 'active', '09171234514', 'Purok Nangka', 'Kahayagan', '2001-08-27', 'Female', 'SK-2024-014', '2025-12-25 07:32:32'),
(26, 'Fernando Morales', 'fernando.morales@sk.ph', '8a630de72b9c76f0978978cf1be92917fd8240f4975d53befcceaf938fe29901', 'youth', 'pending', '09171234515', 'Purok Mangga', 'Kahayagan', '2003-03-03', 'Male', 'SK-2024-015', '2025-12-25 07:32:32'),
(27, 'Quien Bisnar', 'youth6@sk.ph', '8a630de72b9c76f0978978cf1be92917fd8240f4975d53befcceaf938fe29901', 'youth', 'active', '09099989878', 'Purok Guyabano', 'Kahayagan', NULL, 'Female', 'SK-2024-016', '2025-12-25 07:34:01'),
(28, 'Drexzel Escoreal', 'youth7@example.com', '8a630de72b9c76f0978978cf1be92917fd8240f4975d53befcceaf938fe29901', 'youth', 'active', '09112541254', NULL, 'Kahayagan', NULL, NULL, 'SK-2024-017', '2025-12-25 08:58:33');

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
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=33;

--
-- AUTO_INCREMENT for table `feedback`
--
ALTER TABLE `feedback`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=25;

--
-- AUTO_INCREMENT for table `opportunities`
--
ALTER TABLE `opportunities`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=24;

--
-- AUTO_INCREMENT for table `opportunity_applications`
--
ALTER TABLE `opportunity_applications`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=22;

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
