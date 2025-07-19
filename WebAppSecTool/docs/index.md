# Web Application Vulnerability Scanner

**Web Application Vulnerability Scanner** is a comprehensive tool designed to identify and report security vulnerabilities in web applications. It aims to assist developers, security professionals, and organizations in securing their web applications by detecting common vulnerabilities such as SQL Injection, Cross-Site Scripting (XSS), and more.

## Features

- **Comprehensive Scanning**: Detects a wide range of vulnerabilities, including but not limited to:
  - SQL Injection
  - Cross-Site Scripting (XSS)
  - Command Injection
  - File Upload Vulnerabilities
  - Path Traversal
  - XML External Entity (XXE) Injection
  - Server-Side Request Forgery (SSRF)
  - Open Redirects

- **User-Friendly Interface**: Provides an intuitive web-based interface for easy interaction and configuration.

- **Extensibility**: Modular architecture allows for easy addition of new vulnerability checks and features.

## Technologies Used

- **Backend**: Python, Flask
- **Frontend**: ReactJS, JavaScript/TypeScript
- **Database**: SQLite/MySQL (depending on configuration)
- **Others**: Docker for containerization, GitHub Actions for CI/CD

## Installation

To set up the Web Application Vulnerability Scanner locally, follow these steps:

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/Roh00t/PersonalProjects/web-vulnerability-scanner.git
   cd web-vulnerability-scanner