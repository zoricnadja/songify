# Songify

_Project for the course Računarstvo u oblaku (Cloud Computing), part of the Software Engineering and Information Technologies program at the Faculty of Technical Sciences, University of Novi Sad, Serbia, 2025._

Songify is a web application for uploading, sharing, and listening to music content, developed using AWS cloud services and following a cloud-native architecture.

---

## Specification

### User Types

- **Unauthenticated User**
  - Can register on the system.
  - Can log in if already possesses an account.

- **Administrator**
  - Authenticated user with administrator role.
  - Can add and edit music content and artists.

- **Regular User**
  - Authenticated user, has access to explore and rate content, create playlists, subscribe and manage subscriptions, and gets notifications and personalized recommendations.
  - Can locally download uploaded content.

### System Components

- **Client Application:** Provides a graphical interface for users to access system functionalities.
- **Server Application:** Cloud-native backend, containing business logic. Designed to satisfy all functional and non-functional requirements using AWS services.

### Functional Requirements

- User registration (unique username and email, password, full name, birth date)
- User login
- Artist creation and editing (admin)
- Uploading music content with metadata (admin)
- Content viewing for users and admins
- Content editing/deletion (admin)
- Content filtering/discover via genres 
- “Offline” playback
- Content download
- Content rating 
- Subscribing to content 
- Managing subscriptions
- Personalized feed (based on ratings, subscriptions, activity)
- Automatic lyrics transcription via audio processing, presented alongside songs

### Non-functional Requirements

- Cloud-native architecture
- Separate storage for content and metadata
- High performance filtering, proper data modeling
- Infrastructure as Code (IaC) using AWS CDK
- Adequate communication style between components (event-driven, synchronous/async as needed)
- API Gateway as system entry point (REST API for frontend-backend communication)
- Frontend deployment on AWS (publicly accessible)
- Notification system: user receives notification (email/SMS or WebSocket) when new subscribed content is posted

## Setup

- Crate a new file or rename `.env.example` to `.env` and update the variables

### Terraform

- Update variables in `config.s3.tfbackend`
- Run `terraform init -backend-config='./config.s3.tfbackend'`
- Run `terraform apply` and check if the changes are acceptable
