# Inventory Management System

The Inventory Management System is a Python-based application developed using Tkinter and customtkinter for the graphical interface, and MySQL for database management. This system is designed to help clinics efficiently manage their disposable inventory items such as syringes, test tubes, scissors, and bandages. It features secure login, member management, stock threshold alerts, and automatic email notifications for inventory replenishment. The project is scalable to handle large volumes of data, making it suitable for clinics of various sizes.

## Features

- Secure user authentication with admin and basic user roles.
- Add new staff members with customizable permission levels.
- Manage inventory items with specified minimum and maximum quantities.
- Automatic email notifications to suppliers when stock falls below the minimum threshold.
- Input validation for email addresses to ensure proper email format.
- Support for multiple supplier email addresses per item.
- Real-time calculation of current stock based on initial stock and consumption.
- Scalable to handle growing data as the clinic expands.

## Success Criteria

- The client can securely log in to the system.
- New members can be added by the client with admin or user-level permissions.
- The system manages inventory items with set maximum and minimum values.
- Automatic email notifications are sent to suppliers when stock is low.
- The system validates email addresses to ensure proper format.
- Initial stock values can be set by the client or user.
- Stock consumption can be tracked, and current stock is calculated automatically.
- The system is designed to handle large volumes of data as the clinic grows.

## Future Enhancements

I look forward to enhancing the Inventory Management System in the coming days by adding more features and improving its functionality based on feedback and evolving requirements.

## Acknowledgments

I would like to express my gratitude to my friend who helped me successfully complete this project.

## Technologies Used

- Python
- Tkinter
- customtkinter
- SQLite3

## Getting Started

### Prerequisites

- Python 3.x
- SQLite3

### Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/snehasharma18/inventory-management-system.git
    ```

2. Install required Python packages:
    ```bash
    pip install -r requirements.txt
    ```

3. Set up SQLite3 database and update connection details in the code.

4. Run the application:
    ```bash
    python main.py
    ```

## License

This project is licensed under the MIT License.
