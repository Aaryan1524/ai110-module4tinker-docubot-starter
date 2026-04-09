# DocuBot Model Card

This model card is a short reflection on your DocuBot system. Fill it out after you have implemented retrieval and experimented with all three modes:

1. Naive LLM over full docs  
2. Retrieval only  
3. RAG (retrieval plus LLM)

Use clear, honest descriptions. It is fine if your system is imperfect.

---

## 1. System Overview

**What is DocuBot trying to do?**  
To experience the 3 ways of using LLMs to answer questions about the codebase: Naive, Retrieval only, and RAG.

**What inputs does DocuBot take?**  
User question, docs in folder, and environment variables. It can also take in a custom query.

**What outputs does DocuBot produce?**
It produces answers to the user's query based on the selected mode.

---

## 2. Retrieval Design

**How does your retrieval system work?**  
Describe your choices for indexing and scoring.

- How do you turn documents into an index?
I used a dictionary to store the index.
- How do you score relevance for a query?
I used a scoring system to score the relevance of each document to the query.
- How do you choose top snippets?
I chose the top 3 snippets to return.

**What tradeoffs did you make?**  
RAG & LLM are slower but more accurate. Retrieval only is faster but less accurate.

---

## 3. Use of the LLM (Gemini)

**When does DocuBot call the LLM and when does it not?**  
Briefly describe how each mode behaves.

- Naive LLM mode: Vague & fast 
- Retrieval only mode: Fast but not specific
- RAG mode: Slow but specific & perfect

**What instructions do you give the LLM to keep it grounded?**  
I told the LLM to only use the snippets provided and to say "I do not know" if it did not know the answer based on provided context.

---

## 4. Experiments and Comparisons

Run the **same set of queries** in all three modes. Fill in the table with short notes.

| Query | Naive LLM: helpful or harmful? | Retrieval only: helpful or harmful? | RAG: helpful or harmful? | Notes |
|------|---------------------------------|--------------------------------------|---------------------------|-------|
| Example: Where is the auth token generated? | Harmful | Helpful | Helpful | |
| Example: How do I connect to the database? | Harmful | Helpful | Helpful | |
| Example: Which endpoint lists all users? | Harmful | Helpful | Helpful | |
| Example: How does a client refresh an access token? | Harmful | Helpful | Helpful | |

**What patterns did you notice?**  

- When does naive LLM look impressive but untrustworthy?  
It answers with the context it has, but it doesn't have the full context of the codebase.
- When is retrieval only clearly better?  
When the question is very specific and the answer is in the docs.
- When is RAG clearly better than both?
It's a custom answer that is specific to the docs that it has a context of.

---

## 5. Failure Cases and Guardrails

**Describe at least two concrete failure cases you observed.**  

1. No retrieval in docubot initially because it was missing logic.
2. `score_document` didn't calculate correctly before implementation.

**When should DocuBot say “I do not know based on the docs I have”?**  
When the question is not related to the documentation provided.

**What guardrails did you implement?**  
Specific prompt instructions to prevent hallucination by forcing the model to stick to the provided snippets.

---

## 6. Limitations and Future Improvements

**Current limitations**  
1. Keyword matching is basic and might miss synonyms.
2. Large documents are loaded entirely into memory.
3. No semantic understanding in the retrieval step.

**Future improvements**  
1. Implement vector embeddings for better search.
2. Add support for more file types (PDF, etc).
3. Improve snippet chunking for localized answers.

---

## 7. Responsible Use

**Where could this system cause real world harm if used carelessly?**  
If used on critical security or infrastructure code where a hallucinated answer could lead to vulnerabilities.

**What instructions would you give real developers who want to use DocuBot safely?**  
- Always verify the citations and files mentioned.
- Do not use for high-stakes deployment without human review.
- Keep documentation up to date to ensure the bot has the correct context.

---
