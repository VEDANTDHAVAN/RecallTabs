class TextChunker:
    def chunk(self, text: str, size=500, overlap=50):
        words = text.split()
        chunks = []
        start = 0

        while start < len(words):
            end = start + size

            chunk = " ".join(words[start:end])
            chunks.append(chunk)

            start += size - overlap

        return chunks