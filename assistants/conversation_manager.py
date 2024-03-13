import redis
import uuid
import logging

# Initialize the logger for this module
logger = logging.getLogger(__name__)

class AdvancedConversationManager:
    def __init__(self, redis_host="localhost", redis_port=6379, redis_password=None):
        self.redis_host = redis_host
        self.redis_port = redis_port
        self.redis_password = redis_password
        self.redis = redis.Redis(
            host=self.redis_host,
            port=self.redis_port,
            password=self.redis_password,
            decode_responses=True,
        )
        logger.debug("AdvancedConversationManager initialized")

    def verify_rejson(self):
        """Verify that the ReJSON module is loaded."""
        try:
            modules = self.redis.execute_command("MODULE LIST")
            if any("ReJSON" in module.values() for module in modules):
                logger.info("ReJSON module found in Redis.")
                return True
            else:
                logger.warning("ReJSON module not found in Redis.")
                return False
        except redis.RedisError as e:
            logger.error(f"Redis error: {e}")
            return False

    def start_session(self, user_id):
        session_id = str(uuid.uuid4())
        self.redis.json().set(
            f"session:{session_id}",
            "$",
            {"user_id": user_id, "messages": [], "context": {}},
        )
        logger.info(f"Session {session_id} started for user {user_id}")
        return session_id

    def store_user_profile(self, user_id, profile_data):
        self.redis.json().set(f"user_profile:{user_id}", "$", profile_data)
        logger.debug(f"Stored profile for user {user_id}")

    def append_message(self, session_id, message):
        self.redis.json().arrappend(f"session:{session_id}", "$.messages", message)
        logger.debug(f"Appended message to session {session_id}: {message}")

    def update_context(self, session_id, context):
        self.redis.json().set(f"session:{session_id}", "$.context", context)
        logger.debug(f"Updated context for session {session_id}")

    def get_conversation_history(self, session_id):
        history = self.redis.json().get(f"session:{session_id}", "$.messages")
        logger.debug(f"Retrieved conversation history for session {session_id}")
        return history

    def get_context(self, session_id):
        context = self.redis.json().get(f"session:{session_id}", "$.context")
        logger.debug(f"Retrieved context for session {session_id}")
        return context

    def trim_conversation_history(self, session_id, max_tokens=1024):
        logger.debug(f"Trimming conversation history for session {session_id} with max tokens {max_tokens}")
        nested_history = self.get_conversation_history(session_id)

        # Flatten the list if it's nested
        history = (
            [msg for sublist in nested_history for msg in sublist]
            if nested_history and isinstance(nested_history[0], list)
            else nested_history
        )

        total_tokens = sum(len(message["text"].split()) for message in history)

        while total_tokens > max_tokens and history:
            history.sort(key=lambda msg: msg.get("importance", 0))
            removed_message = history.pop(
                0
            )  # Remove the least important/oldest message
            total_tokens -= len(removed_message["text"].split())

        # Update the trimmed history back into Redis correctly
        self.redis.json().set(f"session:{session_id}", "$.messages", history)
        logger.info(f"Trimmed conversation history for session {session_id}")

    def flush_db(self):
        """Flush the Redis database to clear all data."""
        self.redis.flushdb()
        logger.info("Redis database flushed.")


# Example use of the AdvancedConversationManager
if __name__ == "__main__":
    manager = AdvancedConversationManager(redis_host="127.0.0.1", redis_port=6379)
    if manager.verify_rejson():
        user_id = "user123"
        session_id = manager.start_session(user_id)
        print(f"Session started with ID: {session_id}")

        # Simulate appending messages to the conversation
        messages = [
            {"text": "Hello, how can I assist you today?", "importance": 1},
            {"text": "I'm looking for information on topic XYZ.", "importance": 2},
            # Add more messages as needed to simulate a conversation
        ]

        for message in messages:
            manager.append_message(session_id, message)

        # Debugging: Fetch and print the raw conversation history from Redis
        history = manager.get_conversation_history(session_id)
        print("Raw Conversation History from Redis:")
        print(history)  # This should print the list of message dictionaries

        # Now, let's attempt to trim the conversation history
        try:
            manager.trim_conversation_history(session_id, max_tokens=1024)
            # Fetch and print the adjusted conversation history to see the effect of trimming
            history = manager.get_conversation_history(session_id)
            print("Adjusted Conversation History after Trimming:")
            for message in history:
                print(message)
        except TypeError as e:
            print(f"Error during trimming: {e}")
