import { useEffect, useState } from "react";

import ConversationSidebar from "../components/ConversationSidebar";
import ChatWindow from "../components/ChatWindow";

import { 
  createConversation, listConversations,
} from "../shared/api/conversation";

export default function App() {
  const [conversations, setConversations] = useState<any[]>([]);
  const [currentConversation, setCurrentConversation] = useState<string | null>(null);

  async function loadConversations() {
    const data = await listConversations();

    setConversations(data);

    if (data.length && !currentConversation) {
      setCurrentConversation(data[0].id);
    }
  }

  async function handleNewConversation() {
    const conversation = await createConversation();

    await loadConversations();

    setCurrentConversation(conversation.id);
  }

  useEffect(() => {
    loadConversations();
  }, []);

  return (
    <div style={{display: "flex", width: 800, height: 600,}}>
      <ConversationSidebar 
       conversations={conversations} currentId={currentConversation}
       onSelect={setCurrentConversation} onNew={handleNewConversation}
      />

      <ChatWindow conversationId={currentConversation} />
    </div>
  );
}