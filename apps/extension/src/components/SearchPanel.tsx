import { useState } from "react";
import { search } from "../shared/api/search";

type SearchResult = {
    tab_id: string;
    title: string;
    url: string;
    score: number;
    summary?: string | null;
    topic?: string | null;
};

type SearchResponse = {
    semantic: SearchResult[];
    keyword: SearchResult[];
};

export default function SearchPanel() {
    const [query, setQuery] = useState("");
    const [results, setResults] = useState<SearchResult[]>([]);

    async function handleSearch() {
        if (!query.trim()) return;

        const data = await search(query);

        if (Array.isArray(data)) {
            setResults(data);
            return;
        }

        setResults([
            ...(data.semantic ?? []),
            ...(data.keyword ?? []),
        ]);
    }

    function formatScore(score: number) {
        if (score > 1) {
            return `${score.toFixed(1)}%`;
        }

        return score.toFixed(3);
    }

    function renderResults(title: string, items: SearchResult[]) {
        if (!items.length) return null;

        return (
            <section style={{ marginTop: 18 }}>
             <h4 style={{ marginBottom: 10 }}>{title}</h4>
             {items.map((item) => (
                <div key={`${title}-${item.tab_id}`} style={{
                    border: "1px solid #ddd", padding: 10,
                    marginBottom: 12, borderRadius: 6,
                }}>
                 <div><strong>{item.title}</strong></div>
                 {item.topic && (
                    <div style={{ color: "#444", fontSize: 13 }}>
                     {item.topic}
                    </div>
                 )}
                 <div style={{
                    color: "#666", fontSize: 13,
                 }}>
                  Score: {formatScore(item.score)}
                 </div>
                 <a href={item.url}
                  target="_blank" rel="noreferrer">{item.url}</a>
                </div>
              ))}
            </section>
        );
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

         {renderResults("Results", results)}
        </div>
    );
}
