# Paper Idea Vault

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

## Tech Stack

- **Frontend**: Streamlit
- **Backend**: FastAPI
- **Database**: Redis
- **MISC**: Docker, Langchain

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

1. Open the application in your browser.

2. Enter your username and password to log in.

3. Go to Navigation > Idea to create a new idea.

4. Fill in the details for your idea, such as the title, description, and Tags.

5. Click on the "Save" button to save your idea.

6. Go to Navigation > Meeting to get further research topics or formulating research questions, hypotheses, and objectives or designing experimental goals and methods.

## Demo

![Demo](./demo_data/demo_gif/demo_video_large.gif)

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for more information.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.