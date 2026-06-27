import { useState } from "react";

interface Props {
  onSend: (message: string) => void;
}

export default function ChatInput({
  onSend,
}: Props) {
  const [text, setText] = useState("");

  return (
    <div
      style={{
        display: "flex",
        gap: 8,
        padding: 10,
        borderTop: "1px solid #ddd",
      }}
    >
      <input
        value={text}
        onChange={(e) =>
          setText(e.target.value)
        }
        placeholder="Ask RecallTabs..."
        style={{
          flex: 1,
        }}
      />

      <button
        onClick={() => {
          if (!text.trim()) return;

          onSend(text);

          setText("");
        }}
      >
        Send
      </button>
    </div>
  );
}