class ContextCompressionService:
    def compress(
        self, chunks, max_chunks=6,
    ):
        seen = set()

        result = []

        for chunk in chunks:
            title = chunk["title"]

            if title in seen:
                continue

            seen.add(title)
            result.append(chunk)

            if len(result) >= max_chunks:
                break
        
        return result