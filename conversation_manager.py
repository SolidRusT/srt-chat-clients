import redis
import uuid


class AdvancedConversationManager:
    def __init__(self, redis_host="localhost", redis_port=6379):
        self.redis = redis.Redis(
            host=redis_host, port=redis_port, decode_responses=True
        )

    def start_session(self, user_id):
        """Start a new conversation session for a user."""
        session_id = str(uuid.uuid4())
        self.redis.json().set(
            f"session:{session_id}",
            "$",
            {"user_id": user_id, "messages": [], "context": {}},
        )
        return session_id

    def store_user_profile(self, user_id, profile_data):
        """Store or update a user's profile data."""
        self.redis.json().set(f"user_profile:{user_id}", "$", profile_data)

    def get_user_profile(self, user_id):
        """Retrieve a user's profile data."""
        return self.redis.json().get(f"user_profile:{user_id}")

    def append_message(self, session_id, message):
        """Append a message to the conversation history."""
        self.redis.json().arrappend(f"session:{session_id}", "$.messages", message)

    def update_context(self, session_id, context):
        """Update the conversation context."""
        self.redis.json().set(f"session:{session_id}", "$.context", context)

    def get_conversation_history(self, session_id):
        """Retrieve the conversation history for a session."""
        return self.redis.json().get(f"session:{session_id}", "$.messages")

    def get_context(self, session_id):
        """Get the current conversation context."""
        return self.redis.json().get(f"session:{session_id}", "$.context")


# Example usage
if __name__ == "__main__":
    manager = AdvancedConversationManager()
    user_id = ""
    session_id = manager.start_session(user_id)
    manager.store_user_profile(
        user_id, {"name": "John Doe", "interests": ["technology", "music"]}
    )
    manager.append_message(session_id, {"sender": "user", "text": "Hello, world!"})
    manager.append_message(
        session_id, {"sender": "bot", "text": "Hi there! How can I assist you today?"}
    )
    print(manager.get_conversation_history(session_id))
    manager.update_context(session_id, {"last_topic": "greetings"})
    print(manager.get_context(session_id))
