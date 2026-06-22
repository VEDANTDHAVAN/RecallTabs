import { useState } from "react";

import {
  searchTabs,
  askRecall,
} from "../shared/api/recall";

export default function App() {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState<any[]>([]);
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");

  async function handleSearch() {
    try {
      const data = await searchTabs(query);

      setResults(data);
    }

    catch (err) {
      console.error(err);
    }
  }

  async function handleAsk() {
    try {
      const data = await askRecall(question);

      setAnswer(data.answer);
    }

    catch (err) {
      console.error(err);
    }
  }

  return (
    <div
      style={{
        width: 400, padding: 16,
        fontFamily: "Arial"
      }}
    >
      <h1>RecallTabs</h1>
      <p>AI Browser Memory</p>
      {/* SEARCH */}
      <h3>🔍 Search Tabs</h3>
      <input
        style={{
          width: "100%", padding: 8,
          marginBottom: 8
        }}
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        placeholder="Search your tabs"
      />
      <button onClick={handleSearch}>Search</button>

      <div style={{ marginTop: 12 }}>
        {
          results.map((tab) => (
            <div
              key={tab.tab_id}
              style={{
                border: "1px solid #ddd",
                padding: 8, marginBottom: 8,
              }}
            >
              <strong>{tab.title}</strong>
              <br />
              Score:{" "}{tab.score.toFixed(2)}
            </div>
          ))
        }
      </div>

      <hr style={{ margin: "20px 0" }} />
      {/* ASK RECALL */}
      <h3>🤖 Ask Recall</h3>
      <input
        style={{
          width: "100%", padding: 8,
          marginBottom: 8
        }}
        value={question}
        onChange={(e) => setQuestion(e.target.value)}
        placeholder="Ask anything"
      />
      <button onClick={handleAsk}>Ask</button>
      {
        answer && (<div style={{
              marginTop: 16, padding: 10,
              border: "1px solid #ddd",
            }}>
            {answer}
          </div>)
      }
    </div>
  );
}