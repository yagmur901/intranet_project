# Corporate Intranet Management System

A modern corporate intranet portal developed using Django and Tailwind CSS, designed to digitalize internal communications, document management, and operational workflows. The system is containerized with **Docker** and utilizes **PostgreSQL** as its primary database.

The platform is built on a strictly modular architecture. Administrators can seamlessly toggle departmental modules on or off via the admin panel. The user interface, notification center, and global search engine dynamically adapt to these changes in real-time.

## Key Features

*   **Dynamic Module Management:** Toggle core modules (IT Tickets, Documents, Calendar, Employee Directory, Workspaces) globally via the admin dashboard (`DashboardSettings`).
*   **Smart Middleware Protection:** Custom middleware automatically intercepts requests to disabled modules, gracefully blocks access, and redirects users to the home page with a localized warning.
*   **Context-Aware Notifications:** The notification system filters alerts based on currently active modules. If a module is disabled, its historical notifications are temporarily hidden from the user interface.
*   **Global Live Search (AJAX):** A centralized, real-time search engine that queries across all *active* modules simultaneously without page reloads, providing instant, clickable results.
*   **Corporate & Personal Calendar:** A dual-layer calendar system. Administrators can publish company-wide "Corporate Events," while standard users can create and manage their own private "Personal Events."
*   **Adaptive Grid UI:** The dashboard layout utilizes Tailwind's Flexbox and Grid utilities to automatically adjust component dimensions (e.g., announcements, weather, events) depending on the number of active modules, ensuring a seamless UX with no empty spaces.
*   **Role-Based Security:** Leverages Django's built-in authentication for secure password management, while restricting core profile data updates (Name, Surname, Email) to system administrators to maintain corporate data integrity.

## Tech Stack

*   **Backend:** Python, Django
*   **Database:** PostgreSQL
*   **Infrastructure:** Docker
*   **Frontend:** HTML5, Tailwind CSS, JavaScript (AJAX)
*   **External APIs:** Open-Meteo (Live Weather & Air Quality Index)

## Administration & Configuration

The entire platform can be managed via the built-in Django Admin interface (`/admin`), which has been fully customized and localized for enterprise use.
*   **Module Toggling:** Visibility of modules and features can be controlled centrally from the `Dashboard Settings` section.
*   **Data Management:** Full CRUD operations for Announcements, Documents, Employees, and IT Support Tickets are restricted to authorized personnel.



