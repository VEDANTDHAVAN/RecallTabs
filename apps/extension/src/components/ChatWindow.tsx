import { useEffect, useRef, useState } from "react";

import ChatInput from "./ChatInput";
import MessageBubble from "./MessageBubble";
import SourceList from "./SourceList";

import { getMessages } from "../shared/api/conversation";
import { sendMessage } from "../shared/api/chat";

interface Props {
  conversationId: string | null;
}

export default function ChatWindow({
  conversationId,
}: Props) {
  const [messages, setMessages] = useState<any[]>([]);
  const [loading, setLoading] = useState(false);

  const bottomRef = useRef<HTMLDivElement>(null);

  async function loadMessages() {
    if (!conversationId) {
      setMessages([]);
      return;
    }

    try {
      const data = await getMessages(conversationId);
      setMessages(data);
    } catch (err) {
      console.error("Failed to load messages:", err);
    }
  }

  useEffect(() => {
    loadMessages();
  }, [conversationId]);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({
      behavior: "smooth",
    });
  }, [messages]);

  async function handleSend(question: string) {
    if (!conversationId) return;

    try {
      setLoading(true);

      await sendMessage(conversationId, question);

      await loadMessages();
    } catch (err) {
      console.error("Failed to send message:", err);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div
      style={{
        display: "flex",
        flexDirection: "column",
        flex: 1,
      }}
    >
      <div
        style={{
          flex: 1,
          overflowY: "auto",
          padding: 12,
        }}
      >
        {messages.length === 0 && (
          <div
            style={{
              color: "#666",
              textAlign: "center",
              marginTop: 40,
            }}
          >
            Start a conversation with RecallTabs 🚀
          </div>
        )}

        {messages.map((message) => (
          <div key={message.id}>
            <MessageBubble
              role={message.role}
              content={message.content}
            />

            {message.role === "assistant" &&
              message.sources &&
              message.sources.length > 0 && (
                <SourceList
                  sources={message.sources}
                />
              )}
          </div>
        ))}

        <div ref={bottomRef} />
      </div>

      {loading && (
        <div
          style={{
            padding: 10,
            fontStyle: "italic",
          }}
        >
          RecallTabs is thinking...
        </div>
      )}

      <ChatInput onSend={handleSend} />
    </div>
  );
}