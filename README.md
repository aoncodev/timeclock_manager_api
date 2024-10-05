# Time Clock Manager

## Overview

The Time Clock Manager is a web application designed specifically for restaurants to efficiently manage employee clock-ins and clock-outs, as well as to calculate their daily wages. This project utilizes Django REST Framework for the backend API, enabling seamless interactions between users and the server.

## Features

- **User Management**: Create and manage users with a unique PIN and hourly wage.
- **Clock In/Out Tracking**: Employees can clock in and out, with the system automatically recording their clock-in times and calculating late minutes.
- **Wage Calculation**: Calculate total wages based on hours worked and the user's hourly wage.
- **Weekly Schedule**: Define work schedules for users based on the day of the week.
- **Data Retrieval**: Fetch user clock data for specific dates to monitor attendance and calculate wages.

## Technologies Used

- **Backend**: Django, Django REST Framework
- **Database**: SQLite3
- **Programming Languages**: Python

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/time-clock-manager.git
   ```

2. Navigate to the project directory:

   ```bash
   cd employee_attendance
   ```

3. Install the required packages:

   ```bash
   pip install -r requirements.txt
   ```

4. Run migrations to set up the database:

   ```bash
   python manage.py migrate
   ```

5. Start the development server:
   ```bash
   python manage.py runserver
   ```

## API Endpoints

### User Management:

- GET /api/users/ - List all users
- POST /api/users/ - Create a new user
- GET /api/users/{user_id}/ - Retrieve user details
- PUT /api/users/{user_id}/ - Update user details
- DELETE /api/users/{user_id}/ - Delete a user

### Clock Entry Management:

- GET /api/clock-entries/ - List all clock entries
- POST /api/clock-entries/ - Clock in or out for a user

### Week Schedule Management:

- GET /api/week-schedules/ - List all week schedules
- POST /api/week-schedules/ - Create a new week schedule

### User Clock Data:

- GET /api/users/{user_id}/clock-data/ - Retrieve clock data for a user on a specific date

## Usage

1. **Clocking In/Out**:

   - Users can clock in and out using their unique PIN.
   - The system will calculate any late minutes based on their scheduled start time.

2. **View User Data**:

   - Admins can view all user data and clock entries via the API or Django admin interface.

3. **Access Reports**:
   - Generate reports on employee attendance and wages for specified dates.

## Contributing

Contributions are welcome! If you have suggestions for improvements or features, please follow these steps:

1. Fork the repository
2. Create a new branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## Contact

Akhidjon - aoncodev@gmail.com

Project Link: [https://github.com/yourusername/time-clock-manager](https://github.com/yourusername/time-clock-manager)
