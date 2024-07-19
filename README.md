# paper idea vault

<p align="center">
  <img src="https://img.shields.io/github/license/hibana2077/paper-idea-vault" alt="License">
  <img src="https://img.shields.io/github/issues/hibana2077/paper-idea-vault" alt="Issues">
  <img src="https://img.shields.io/github/forks/hibana2077/paper-idea-vault" alt="Forks">
  <img src="https://img.shields.io/github/stars/hibana2077/paper-idea-vault" alt="Stars">
  <img src="https://img.shields.io/github/issues-pr/hibana2077/paper-idea-vault" alt="Pull Requests">
  <img src="https://img.shields.io/github/contributors/hibana2077/paper-idea-vault" alt="Contributors">
</p>

A small tool that can help computer scientists, researchers, and students to brainstorm and further develop research ideas.

## Features

- A lightweight application based on Redis and FastAPI.
- Automatic literature search for relevant references.
- Assistance in formulating research questions, hypotheses, and objectives.
- Help with designing experimental goals and methods.
- Brainstorming further research topics.

## Installation

### Prerequisites

- Docker and Docker Compose
- Groq API key
- OpenAI API key (optional)

### Steps

1. Clone the repository.

    ```bash
    git clone https://github.com/hibana2077/paper-idea-vault.git
    cd paper-idea-vault/src
    ```

2. Edit the `docker-compose.yml` file and replace the placeholder values with your API keys and username and password for the application authentication.

    ```yaml
    environment:
        USER: "admin"
        PASSWORD: "admin"
        BACKEND_SERVER: "backend:8081"
        LLM_PROVIDER: groq
        LLM_MODEL: gemma2-9b-it
        LLM_API_TOKEN: "your-api-token-here"
        OPENAI_API_TOKEN: "your-api-token-here"
    ```

3. Build and run the application.

    ```bash
    docker-compose up -d
    ```

4. Access the application at `http://localhost:80`.

## Usage

## Demo

## Contributing

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.