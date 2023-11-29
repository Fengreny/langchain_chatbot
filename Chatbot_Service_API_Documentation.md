
# Chatbot Service API Documentation

## Overview

This API documentation details the endpoints available in the Chatbot Service, which includes sending messages and retrieving conversation history.

## API Endpoints

### Send Message

- **Endpoint**: `/message`
- **Method**: `POST`
- **Body**:
  ```json
  {
    "user_id": "string",
    "message": "string"
  }
  ```
- **Response**:
  - **Code**: 200 OK
  - **Content**:
    ```json
    {
      "response": "string"
    }
    ```
- **Error Response**:
  - **Code**: 500 Internal Server Error
  - **Content**: Error details

### Get Conversation History

- **Endpoint**: `/history/{user_id}`
- **Method**: `GET`
- **URL Parameters**:
  - `user_id`: Unique identifier for the user.
- **Response**:
  - **Code**: 200 OK
  - **Content**:
    ```json
    {
      "history": "string"
    }
    ```
- **Error Response**:
  - **Code**: 404 Not Found
  - **Content**: User not found
