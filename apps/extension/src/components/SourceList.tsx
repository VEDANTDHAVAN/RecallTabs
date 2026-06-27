interface Source {
  title: string;
  url: string;
}

interface Props {
  sources: Source[];
}

export default function SourceList({
  sources,
}: Props) {
  if (!sources.length) return null;

  return (
    <div
      style={{
        marginTop: 10,
      }}
    >
      <strong>Sources</strong>

      {sources.map((source) => (
        <div key={source.url}>
          <a
            href={source.url}
            target="_blank"
            rel="noreferrer"
          >
            {source.title}
          </a>
        </div>
      ))}
    </div>
  );
}