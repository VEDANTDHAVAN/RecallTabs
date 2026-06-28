import { useState } from "react";
import { search } from "../shared/api/search";

export default function SearchPanel() {
    const [query, setQuery] = useState("");
    const [results, setResults] = useState<any[]>([]);

    async function handleSearch() {
        if (!query.trim()) return;

        const data = await search(query);

        setResults(data);
    }

    return (
        <div style={{padding: 16}}>
         <h3>Semantic Search</h3>
         <input value={query} onChange={(e) => setQuery(e.target.value)}
          placeholder="Search your Memory...." style={{
            width: "100%", padding: 8,
          }}
         />

         <button onClick={handleSearch} style={{ marginTop: 10 }}>Search</button>

         <div style={{ marginTop: 20 }}>
          {results.map((item) => (
            <div key={item.tab_id} style={{
                border: "1px solid #ddd", padding: 10,
                marginBottom: 12, borderRadius: 6,
            }}>
             <div><strong>{item.title}</strong></div>
             <div style={{
                color: "#666", fontSize: 13,
             }}>
              Score: {(item.score * 100).toFixed(1)}%
             </div>
             <a href={item.url}
              target="_blank" rel="noreferrer">{item.url}</a>
            </div>
          ))}
         </div>
        </div>
    );
}