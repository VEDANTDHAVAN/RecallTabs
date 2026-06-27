interface Props {
  role: "user" | "assistant";
  content: string;
}

export default function MessageBubble({
  role, content,
}: Props) {
  const isUser = role === "user";

  return (
    <div
      style={{
        display: "flex",
        justifyContent: isUser
          ? "flex-end"
          : "flex-start",
        marginBottom: 12,
      }}
    >
      <div
        style={{
          maxWidth: "80%",
          padding: 10,
          borderRadius: 8,
          background: isUser
            ? "#DCF8C6"
            : "#F1F1F1",
          whiteSpace: "pre-wrap",
        }}
      >
        {content}
      </div>
    </div>
  );
}