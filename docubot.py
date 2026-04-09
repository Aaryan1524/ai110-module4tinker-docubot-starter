"""
Core DocuBot class responsible for:
- Loading documents from the docs/ folder
- Building a simple retrieval index (Phase 1)
- Retrieving relevant snippets (Phase 1)
- Supporting retrieval only answers
- Supporting RAG answers when paired with Gemini (Phase 2)
"""

import os
import glob

class DocuBot:
    def __init__(self, docs_folder="docs", llm_client=None):
        """
        docs_folder: directory containing project documentation files
        llm_client: optional Gemini client for LLM based answers
        """
        self.docs_folder = docs_folder
        self.llm_client = llm_client

        # Load documents into memory
        self.documents = self.load_documents()  # List of (filename, text)
        print(f"--- Debug: Loaded {len(self.documents)} documents from '{self.docs_folder}' folder ---")

        # Build a retrieval index (implemented in Phase 1)
        self.index = self.build_index(self.documents)

    # -----------------------------------------------------------
    # Document Loading
    # -----------------------------------------------------------

    def load_documents(self):
        """
        Loads all .md and .txt files inside docs_folder.
        Returns a list of tuples: (filename, text)
        """
        docs = []
        pattern = os.path.join(self.docs_folder, "*.*")
        for path in glob.glob(pattern):
            if path.endswith(".md") or path.endswith(".txt"):
                with open(path, "r", encoding="utf8") as f:
                    text = f.read()
                filename = os.path.basename(path)
                docs.append((filename, text))
        return docs

    # -----------------------------------------------------------
    # Index Construction (Phase 1)
    # -----------------------------------------------------------

    def build_index(self, documents):
        """
        Builds a tiny inverted index mapping lowercase words to the documents
        they appear in.
        """
        index = {}
        for filename, text in documents:
            words = text.lower().split()
            for word in words:
                clean_word = word.strip('.,!?;:()[]"\'')
                if not clean_word:
                    continue
                if clean_word not in index:
                    index[clean_word] = set()
                index[clean_word].add(filename)
        return index

    # -----------------------------------------------------------
    # Scoring and Retrieval (Phase 1)
    # -----------------------------------------------------------

    def score_document(self, query, text):
        """
        Returns a simple relevance score (keyword overlap count).
        """
        query_words = set(query.lower().split())
        query_words = {w.strip('.,!?;:()[]"\'') for w in query_words if w.strip('.,!?;:()[]"\'')}
        
        doc_words = set(text.lower().split())
        doc_words = {w.strip('.,!?;:()[]"\'') for w in doc_words if w.strip('.,!?;:()[]"\'')}
        
        score = 0
        for word in query_words:
            if word in doc_words:
                score += 1
        return score

    def retrieve(self, query, top_k=3):
        """
        Scores all documents and returns the top_k relevant snippets.
        """
        scored_docs = []
        for filename, text in self.documents:
            score = self.score_document(query, text)
            if score > 0:
                scored_docs.append((score, filename, text))
        
        scored_docs.sort(key=lambda x: x[0], reverse=True)
        return [(filename, text) for score, filename, text in scored_docs[:top_k]]

    # -----------------------------------------------------------
    # Answering Modes
    # -----------------------------------------------------------

    def answer_retrieval_only(self, query, top_k=3):
        """
        Phase 1 retrieval only mode.
        Returns raw snippets and filenames with no LLM involved.
        """
        snippets = self.retrieve(query, top_k=top_k)

        if not snippets:
            return "I do not know based on these docs."

        formatted = []
        for filename, text in snippets:
            formatted.append(f"[{filename}]\n{text}\n")

        return "\n---\n".join(formatted)

    def answer_rag(self, query, top_k=3):
        """
        Phase 2 RAG mode.
        Uses student retrieval to select snippets, then asks Gemini
        to generate an answer using only those snippets.
        """
        if self.llm_client is None:
            raise RuntimeError(
                "RAG mode requires an LLM client. Provide a GeminiClient instance."
            )

        snippets = self.retrieve(query, top_k=top_k)

        if not snippets:
            return "I do not know based on these docs."

        return self.llm_client.answer_from_snippets(query, snippets)

    # -----------------------------------------------------------
    # Bonus Helper: concatenated docs for naive generation mode
    # -----------------------------------------------------------

    def full_corpus_text(self):
        """
        Returns all documents concatenated into a single string.
        This is used in Phase 0 for naive 'generation only' baselines.
        """
        return "\n\n".join(text for _, text in self.documents)
