# Scalable Cloud-Based Wallpaper API

This repository contains the **Wallpaper API**, a FastAPI-based application that allows users to upload, update, delete, and retrieve wallpapers. The API integrates with cloud services such as **AWS Elastic Beanstalk** for deployment, **AWS RDS** for database management, and additional web services for file storage and URL shortening.

## Table of Contents
- [Project Overview](#project-overview)
- [Key Features](#key-features)
- [Architecture](#architecture)
- [Technology Stack](#technology-stack)
- [AWS Services Used](#aws-services-used)
- [API Endpoints](#api-endpoints)
- [Installation](#installation)
- [Environment Variables](#environment-variables)
- [Running the App](#running-the-app)
- [Deployment](#deployment)
- [Continuous Integration/Continuous Delivery (CI/CD)](#continuous-integrationcontinuous-delivery-cicd)
- [License](#license)
- [Acknowledgments](#acknowledgments)

## Project Overview

The **Wallpaper API** is designed to be a scalable and highly available web service that enables users to manage wallpapers via a RESTful API. The application uses **FastAPI** for API development and leverages **AWS Elastic Beanstalk** for hosting in a multi-availability zone setup, ensuring scalability and resilience.

The API integrates two additional web services:
- **File Store Service** for uploading and retrieving wallpaper images.
- **URL Shortener Service** to shorten the URLs of the stored wallpapers.

This project also utilizes **AWS CodePipeline** for CI/CD, ensuring continuous delivery and automatic scaling based on the load.

## Key Features

- **CRUD Functionality**: The API allows users to create, retrieve, update, and delete wallpapers.
- **File Upload Integration**: Wallpapers are uploaded using a third-party file store service.
- **URL Shortening**: The URLs returned by the file storage service are shortened before being stored in the database.
- **Public API**: Exposes endpoints for public use by third-party developers.
- **Pagination**: Supports pagination for wallpaper retrieval to optimize performance.

## Architecture

![image](https://github.com/user-attachments/assets/ffc0d21c-0bcb-49fe-ab03-6fc444abe700)

The application follows a **microservice-oriented architecture**, integrating external services for file storage and URL shortening. The backend is built using **FastAPI** and deployed on **AWS Elastic Beanstalk**, with the database hosted on **Amazon RDS**.

Key architectural components:
1. **Wallpaper API**: Handles CRUD operations for wallpapers.
2. **File Store Service**: Stores uploaded images and returns a URL.
3. **URL Shortener Service**: Shortens long URLs for easy access.
4. **Database**: AWS RDS with MySQL is used to store metadata about wallpapers, such as shortened URLs and other details.

## Technology Stack

- **Framework**: FastAPI (Python)
- **Cloud Provider**: AWS
  - AWS Elastic Beanstalk (PaaS)
  - AWS RDS (MySQL)
  - AWS CloudWatch for monitoring
  - AWS CodePipeline for CI/CD
- **Database**: MySQL with SQLAlchemy ORM
- **Frontend**: Jinja2 templates and Bootstrap for a responsive user interface
- **Version Control**: Git with AWS CodeCommit

## AWS Services Used

- **AWS Elastic Beanstalk**: For deploying and managing the application, including load balancing and auto-scaling.
- **Amazon RDS (MySQL)**: For storing wallpaper metadata and URLs.
- **AWS CodePipeline**: For CI/CD, automating the build, test, and deployment process.
- **Amazon CloudWatch**: For logging and monitoring the application.
- **AWS CodeCommit**: For version control of the source code.

## API Endpoints

The following endpoints are exposed by the Wallpaper API:

1. **GET /wallpapers**: Retrieves a paginated list of wallpapers (maximum 12 per page).
2. **GET /wallpapers/{id}**: Retrieves details of a specific wallpaper by its ID.
3. **POST /wallpapers**: Uploads a new wallpaper.
   - The file is uploaded to the file storage service, and a shortened URL is stored in the database.
4. **PUT /wallpapers/{id}**: Updates the details of an existing wallpaper (restricted to API use).
5. **DELETE /wallpapers/{id}**: Deletes a wallpaper by its ID (restricted to API use).

## Installation

### Prerequisites

- **Python 3.8+**
- **FastAPI 0.78+**
- **AWS CLI**
- **Heroku CLI** or **Elastic Beanstalk CLI**
- **MySQL** or a similar database system

### Clone the Repository

```bash
git clone https://github.com/your-repo/wallpaper-api.git
cd wallpaper-api
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Configure the Database

Ensure you have a MySQL instance running (preferably on AWS RDS). Set up the database and run migrations using SQLAlchemy.

## Environment Variables

You will need to set up the following environment variables to run the application:

```bash
# AWS and Database Credentials
AWS_ACCESS_KEY_ID=your_aws_access_key
AWS_SECRET_ACCESS_KEY=your_aws_secret_key
DATABASE_URL=mysql://your_user:your_password@your_host/your_db_name

# External Web Services
FILE_STORE_API_URL=https://filestore.example.com/api/upload
URL_SHORTENER_API_URL=https://shorturl.example.com/api/shorten
```

## Running the App

1. **Run the FastAPI Development Server**:

```bash
uvicorn app.main:app --reload
```

2. **Access the API Documentation**:
   FastAPI provides interactive API documentation that can be accessed at `http://127.0.0.1:8000/docs`.

3. **Use the API**:
   You can now interact with the API using the provided endpoints.

## Deployment

### AWS Elastic Beanstalk Deployment

To deploy the application on **AWS Elastic Beanstalk**, follow these steps:

1. **Install the Elastic Beanstalk CLI**:

```bash
pip install awsebcli
```

2. **Initialize the Elastic Beanstalk environment**:

```bash
eb init
```

3. **Create the environment and deploy**:

```bash
eb create
eb deploy
```

4. **Access the Deployed Application**:
   Once deployed, the application can be accessed via the Elastic Beanstalk URL provided by AWS.

## Continuous Integration/Continuous Delivery (CI/CD)

The project is integrated with **AWS CodePipeline** for continuous deployment. When code is pushed to the **AWS CodeCommit** repository, the pipeline automatically builds and deploys the changes.

### Steps for CI/CD:
1. Push changes to the CodeCommit repository.
2. The pipeline is triggered to build and test the application.
3. Upon successful tests, the application is deployed to AWS Elastic Beanstalk.

Monitoring and logging are handled via **AWS CloudWatch**, where you can track application performance and view logs.

## License

This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for details.

## Acknowledgments

This project was developed as part of the **Master's in Cloud Computing** program at the **National College of Ireland**, under the supervision of **Vikas Sahni**. Special thanks to the instructors and peers who contributed to this project.
