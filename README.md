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

## Demo

## Contributing

Thank you for your interest in contributing to the Paper Idea Vault! We welcome contributions from everyone, whether it's code, documentation, bug reports, or feature requests. Here's how you can contribute:

### Reporting Bugs

1. **Check Existing Issues**: Before submitting a bug report, please check if it's already reported. If you find an existing issue that matches yours, you can contribute by providing additional information in the comments.
2. **Submit a New Issue**: If no existing issue addresses the problem, create a new issue. Please provide a clear title and description, as much relevant information as possible, and a code sample or an executable test case demonstrating the expected behavior that is not occurring.

### Feature Requests

1. **Discuss in Issues**: Before working on a new feature, please open an issue to discuss its relevance and implementation. This way, you can gather feedback from other community members and the maintainers before investing time.
2. **Provide Context**: In your issue, explain why the feature is beneficial, and if possible, how it could be implemented.

### Submitting Pull Requests

1. **Fork the Repository**: Start by forking the repository and then cloning it locally.
2. **Create a Branch**: Create a new branch in your fork for each feature or bug fix.
3. **Develop**: Make your changes in your branch. Ensure that your code adheres to the existing style to maintain the project's consistency.
4. **Test Your Changes**: Add tests if possible and ensure all tests pass locally. It's important to maintain and improve the test coverage.
5. **Write Documentation**: Update the documentation to reflect any changes or additions you have made.
6. **Submit a Pull Request**: Once you've completed your changes, submit a pull request to the main repository. Provide a clear description of the problem and solution. Include the relevant issue number if applicable.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.