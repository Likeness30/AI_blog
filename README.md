# AI Blog Generator
## Overview
* The AI Blog Generator is a web application that automatically converts YouTube videos into blog posts. By utilizing cutting-edge AI models for transcription and content generation, the app enables users to input YouTube video links and receive well-structured blog posts in return.

## Features
* AI-Powered Transcription: Converts YouTube video audio into text.
* Blog Post Generation: Automatically creates a blog post from the transcribed text.
* User Authentication: Secure login and signup system for users.
* Responsive UI: Frontend built with HTML, CSS, and Tailwind for a clean and user-friendly experience.

## Technologies Used
## Frontend:
* HTML & CSS: For structuring and styling web pages.
* Tailwind CSS: For responsive and modern UI components.
* JavaScript: Enhances interactivity on the frontend.

Backend:
Django: A robust web framework for handling user requests, authentication, and API integration.
PostgreSQL: Database management for storing user data and blog posts.
Assembly AI API: For converting video audio to text.
OpenAI API: For generating well-structured blog content from the transcription.

## Deployment:
* AWS (Qovery): Cloud infrastructure for managing and deploying the application.

## Getting Started
* Prerequisites
* Python 3.x
* Django
* PostgreSQL
* Assembly AI API Key
* OpenAI API Key
* Node.js and npm (for frontend assets)

## Installation
* Clone the repository:
```git clone https://github.com/your-username/ai-blog-generator.git
```
```
cd ai-blog-generator
```
Set up a virtual environment:
```
python3 -m venv venv
```
```
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

Install dependencies:

```pip install -r requirements.txt
```
## Set up your environment variables: Create a .env file and configure the following:

SECRET_KEY (Django secret key)
DATABASE_URL (PostgreSQL database connection)
ASSEMBLYAI_API_KEY (API key for transcription)
OPENAI_API_KEY (API key for blog generation)


Run migrations:
````python manage.py migrate
```
Start the development server:
```
python manage.py runserver
```
## Frontend
* The frontend is built using Tailwind CSS and provides a responsive user interface for user login, signup, and generating blog posts.

## Usage
* Sign up or log in.
* Enter a YouTube video link.
* Click Generate Blog Post and let the AI-powered tools handle the rest.
* Review the generated post in the "All Blog Posts" section.

Testing
To run tests:
```
python manage.py test
```

