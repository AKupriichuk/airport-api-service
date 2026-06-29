# Airport API Service

API service for managing airport flights, routes, ticket bookings, and crews. Built with Django REST Framework.


## Features

- JWT Authentication: Secure user registration, login, and profile management using JSON Web Tokens.
- Flight Management: Complete system for managing airports, routes, airplanes, and crews.
- Advanced Flight Search: Filtering flights by source, destination, and departure date.
- Smart Seat Booking: Interactive seat validation that strictly checks if the selected row/seat exists in the airplane and prevents double-booking (overbooking).
- Database Safety: Atomic database transactions to ensure that orders and tickets are saved correctly or rolled back in case of an error.
- API Documentation: Interactive and auto-generated Swagger documentation.

## Installation & How to Run Locally

You can easily run this project using Docker, which automatically sets up the Python environment and the PostgreSQL database.

### Prerequisites
Make sure you have Docker and Docker Compose installed on your system.

### Steps to run:

1. Clone the repository:
git clone https://github.com/YOUR_GITHUB_USERNAME/airport-api-service.git
cd airport-api-service

2. Run the project using Docker Compose:
This command builds the container, applies database migrations, and starts the development server.
docker-compose up --build

3. Access the API:
Once the terminal shows that the server is running, you can access the service:
- Interactive API Documentation (Swagger): http://127.0.0.1:8000/api/doc/swagger/
- Browsable API: http://127.0.0.1:8000/api/airport/

## Authentication & Getting Access

To use endpoints that require authentication (like creating an order):
1. Register a new user at POST /api/user/register/.
2. Get your JWT tokens at POST /api/user/token/ using your credentials.
3. In Swagger or Postman, add the access token to the request header as:
Authorization: Bearer <your_access_token>