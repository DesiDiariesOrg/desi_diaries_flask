<a href="https://warriorwhocodes.com"><img src="repo_images/header.jpg"></a>

<p align="center">
  <a href="https://ankushsinghgandhi.github.io">
    <img src="https://img.shields.io/badge/Website-3b5998?style=flat-square&logo=google-chrome&logoColor=white" />
  </a>
  <a href="http://twitter.com/ankushsgandhi">
    <img src="https://img.shields.io/badge/-Twitter-blue?style=flat-square&logo=twitter&logoColor=white" />
  </a>
   <a href="https://www.linkedin.com/in/ankush-singh-gandhi-2487771aa/">
    <img src="https://img.shields.io/badge/-LinkedIn-0e76a8?style=flat-square&logo=Linkedin&logoColor=white" />
  </a>
  <a href="https://dev.to/@ankushsinghgandhi">
    <img src="https://img.shields.io/badge/-Dev.to-grey?style=flat-square&logo=dev.to&logoColor=white"/>
  </a>
  <a href="https://stackoverflow.com/users/13790266/ankush-singh">
    <img src="https://img.shields.io/badge/-Stackoverflow-orange?style=flat-square&logo=stackoverflow&logoColor=white"/>
  </a>
  <a href="https://leetcode.com/ankushsinghgandhi/">
    <img src="https://img.shields.io/badge/-Leetcode-yellow?style=flat-square&logo=Leetcode&logoColor=white"/>
  </a>
    <a href="https://www.hackerrank.com/ankushsgandhi">
    <img src="https://img.shields.io/badge/-HackerRank-green?style=flat-square&logo=Hackerrank&logoColor=white"/>
  </a>
    <a href="https://www.hackerearth.com/@bhanusinghank">
    <img src="https://img.shields.io/badge/-Hackerearth-purple?style=flat-square&logo=Hackerearth&logoColor=white"/>
  </a>
</p>


# ShareX Social Media Flask

## Overview
This project is a comprehensive web application built with Flask, designed to provide users with a rich multimedia sharing and social networking experience. It combines features such as video reel sharing, real-time chat, live streaming, event booking, and social networking functionalities like following other users. The application aims to create a dynamic and interactive platform where users can connect, share content, communicate, and engage with each other in various ways.

## Key Features

### User Authentication
- **Firebase Authentication**: Secure user authentication is implemented using Firebase Authentication. Users can sign up, log in, and manage their accounts securely.

### Reel Management
- **Upload and Share**: Users can upload short video reels, add descriptions, and share them with others.
- **Interactions**: Users can like, comment on, and bookmark reels, fostering engagement and interaction within the community.

### Real-time Chat
- **Instant Messaging**: Real-time chat functionality allows users to communicate with each other instantly.
- **Group Chat**: Users can create and participate in group chats, facilitating group discussions and collaboration.

### Live Streaming
- **Live Video Streams**: Users can stream live video content and interact with viewers in real-time.
- **Scheduled Events**: Scheduled live streams and events are featured on the platform, providing users with exciting live entertainment.

### Event Booking
- **Discover and Book Events**: Users can discover upcoming events, book tickets, and attend events hosted on the platform.
- **Event Management**: Event organizers can manage event details, ticket sales, and attendee information.

### Social Networking
- **Follow Users**: Users can follow other users to stay updated with their activities and content.
- **Feed and Notifications**: Personalized feeds and notifications keep users informed about new content, interactions, and updates from followed users.

## Technologies Used

### Backend
- **Flask**: The backend of the application is built with Flask, a lightweight and flexible web framework for Python.
- **Firebase**: Firebase services are utilized for user authentication, real-time chat, and data storage.
- **MongoDB**: MongoDB is used as the database for storing user data, media content, chat messages, and event information.

### Frontend
- **HTML/CSS/JavaScript**: The frontend interface is built using HTML, CSS, and JavaScript, providing a responsive and interactive user experience.
- **Vue.js/React/Angular**: Modern frontend frameworks like Vue.js, React, or Angular can be used to enhance the user interface and interactivity of the application.

### Deployment
- **Docker**: Docker containers are used to package the application and its dependencies for easy deployment and scaling.
- **NGINX**: NGINX serves as a high-performance web server and reverse proxy, handling incoming requests and routing them to the appropriate backend services.
- **Amazon EC2**: The application is deployed on Amazon EC2 instances, providing scalable and reliable cloud infrastructure.

## Getting Started

### Prerequisites
- Install Docker on your local machine or set up an Amazon EC2 instance for deployment.
- Configure environment variables for Firebase Authentication credentials, MongoDB connection URI, and other configuration settings.

### Installation
1. Clone the repository: `git clone <repository-url>`
2. Navigate to the project directory: `cd <project-directory>`
3. Set up environment variables: Configure environment variables as per the provided template or instructions.
4. Build Docker image: `docker build -t <image-name> .`
5. Run Docker container: `docker run -d -p <host-port>:<container-port> <image-name>`

### Deployment
1. Set up NGINX: Configure NGINX to act as a reverse proxy for routing requests to the Flask application.
2. Set up Firebase: Set up Firebase Authentication and Realtime Database for managing user authentication and real-time chat functionality.
3. Launch Application: Launch the application and verify its functionality.

## Contributing
Contributions are welcome! Feel free to open issues, submit pull requests, or suggest new features and improvements.

## License
This project is licensed under the [MIT License](LICENSE).


