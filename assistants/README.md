# SRT AI Assistant

## Description

An AI Assistant designed for sophisticated conversation management, leveraging advanced conversational memory capabilities. This assistant is built to handle extensive dialogues by dynamically managing conversation histories, ensuring meaningful interactions without the constraints of traditional context window limitations.

## Requirements

- Python 3.x
- Redis server with the ReJSON module installed
- Python `redis` package (version that includes ReJSON support)

## Setup Instructions

### Installing Python Dependencies

Install the necessary Python packages by running:

```bash
pip install -r requirements.txt
```

Note: This project utilizes Gradio for creating a web-based interface for interactions with the AI Assistant.

### Setting Up Redis

This project requires a [Redis server](https://redis.com/download-center/modules/) running with the [ReJSON module](https://redis.io/docs/data-types/json/) for advanced conversation history management. Follow these steps to set up your environment:

1. **Start Redis Server**: Ensure your Redis server is running. You can start Redis by using:

    ```bash
    sudo systemctl start redis
    ```

    or

    ```bash
    redis-server
    ```

2. **ReJSON Module**: Confirm that the ReJSON module is installed and loaded in your Redis instance. The module is usually downloadable from You can check this with the Redis CLI:

    ```bash
    redis-cli MODULE LIST
    ```

    Look for a module named `ReJSON` in the output.

### Configuring the Application

Update the Redis connection parameters in `conversation_manager.py` to match your setup:

```python
conversation_manager = AdvancedConversationManager(redis_host='localhost', redis_port=6379, redis_password=None)
```

Adjust `redis_host`, `redis_port`, and `redis_password` as necessary to align with your Redis server's configuration.

## Running the Application

To start the SRT AI Assistant, run the following command:

```bash
python main.py
```

This will launch a Gradio interface accessible via a local web browser, facilitating interactions with the AI Assistant.

## Additional Notes

- Consider implementing additional security measures for production environments, such as enabling Redis authentication and utilizing TLS for encrypted connections.
- Regular backups of Redis data are recommended, particularly for applications relying heavily on conversation history for functionality.

## Testing

Detailed instructions for manual testing of the `AdvancedConversationManager` are provided to verify its correct operation before full integration. Follow the steps outlined in the **Testing** section to ensure the conversation manager handles session management, message appending, history trimming, and edge cases as expected.

---

## Recent Updates

- **Integration of AdvancedConversationManager**: Enhanced conversation management capabilities to dynamically manage conversation histories, ensuring the AI Assistant can maintain context effectively over extended interactions.
- **Gradio Interface**: Instructions added for utilizing Gradio to interact with the AI Assistant, providing a user-friendly interface for testing and demonstrations.
- **Debugging and Testing**: Added insights into debugging strategies and test cases to validate the functionality of conversation management and inference processing.

For further details on project updates, refer to the commit history and release notes.
