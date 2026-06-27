interface Conversation {
    id: string;
    title: string | null;
}

interface Props {
    conversations: Conversation[];
    currentId: string | null;
    onSelect: (id: string) => void;
    onNew: () => void;
}

export default function ConversationSidebar({
    conversations, currentId, onSelect, onNew,
}: Props) {
    return (
    <div
      style={{
        width: 220,
        borderRight: "1px solid #ddd",
        display: "flex",
        flexDirection: "column",
      }}
    >
      <button
        onClick={onNew}
        style={{
          margin: 10,
          padding: 8,
        }}
      >
        + New Chat
      </button>

      <div
        style={{
          overflowY: "auto",
          flex: 1,
        }}
      >
        {conversations.map((conversation) => (
          <div
            key={conversation.id}
            onClick={() => onSelect(conversation.id)}
            style={{
              padding: 10,
              cursor: "pointer",
              background:
                currentId === conversation.id
                  ? "#f3f3f3"
                  : "white",
              borderBottom: "1px solid #eee",
            }}
          >
            {conversation.title ?? "Untitled Chat"}
          </div>
        ))}
      </div>
    </div>
  );
}