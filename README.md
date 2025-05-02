# 🏦 Bank Statement API (Flask + MongoDB)

A RESTful API built with **Flask** and **MongoDB**, simulating basic banking operations such as user registration, fund transfers, and loan handling. This project uses `flask_restful` for clean API design and `bcrypt` for secure password hashing.

---

## 🚀 Features

- **User Registration**: `/register`
- **Add Funds**: `/add`
- **Transfer Funds**: `/transfer`
- **Check Balance**: `/checkbalance`
- **Take a Loan**: `/loan`
- **Pay Loan**: `/payloan`

---

## 🛠 Tech Stack

- Python 3.10
- Flask & Flask-RESTful
- MongoDB
- Docker & Docker Compose
- bcrypt for password hashing

---

## 📦 Setup Instructions (Linux)

### 1. 🔽 Clone the Repository

```bash
git clone https://github.com/walidfoysol/API_Bank_Transactions.git
cd bank-statement-api
```

### 🐳 Install Docker & Docker Compose
### 2. Install Docker:
```bash
sudo apt update
sudo apt install docker.io -y
sudo apt install docker-compose -y
```

### 3. Enable Docker service:
```bash
sudo systemctl enable docker
sudo systemctl start docker
```

### 4. 📦 Build and Run the Project
```bash
# Build the Docker images
sudo docker compose build

# Start the containers
sudo docker compose up
```
### Your Flask API will be accessible at: http://localhost:5000/
