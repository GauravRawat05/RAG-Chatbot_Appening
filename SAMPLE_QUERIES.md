# Sample Queries

Four tested queries against the `/chat` endpoint, showing grounded answers, retrieved context, and confidence scores across different question types.

---

### 1. Direct factual question

**Request:**
```json
{ "question": "What is Agentic AI?" }
```

**Response:**
```json
{
  "answer": "Agentic AI refers to systems capable of autonomous decision-making and action in pursuit of specific objectives.",
  "confidence": 0.6
}
```

High confidence — the question closely matches a direct definition sentence in the source document.

---

### 2. Comparative question

**Request:**
```json
{ "question": "How is Agentic AI different from traditional AI?" }
```

**Response:**
```json
{
  "answer": "Agentic AI differs from traditional AI in that it is designed to act autonomously and make decisions toward specific objectives, rather than simply responding to inputs. It moves beyond the simpler, reactive generative-AI architectures... In short, Agentic AI offers proactive problem-solving and autonomous action, whereas traditional AI is generally more reactive and less self-directed.",
  "confidence": 0.49
}
```

Lower confidence than a direct definitional match, but still correctly grounded — the model synthesized the comparison from context spread across a couple of chunks rather than one clean match.

---

### 3. Specific detail question

**Request:**
```json
{ "question": "What are the challenges in orchestrating multi-agent systems?" }
```

**Response:**
```json
{
  "answer": "The document highlights several challenges when orchestrating multi-agent systems:\n\n- Lack of coordination: Uncoordinated systems struggle to achieve objectives, leading to high failure rates (estimated 70-80% for digital transformations).\n- Redundancy and conflict: Without orchestration, agents may duplicate effort or perform conflicting actions.\n- Synchronization difficulties: Aligning the activities of many autonomous agents requires careful management.\n- Complexity of coordination: Orchestrating MAS demands a balance of technical strategies and collaborative efforts to maintain efficient, fault-tolerant operation.",
  "confidence": 0.49
}
```

Retrieved the correct section (Orchestrating Agentic AI Systems) and produced a well-structured, multi-point answer directly from the source.

---

### 4. Out-of-scope question (grounding check)

**Request:**
```json
{ "question": "What is the capital of France?" }
```

**Response:**
```json
{
  "answer": "I don't know based on the provided document.",
  "confidence": 0
}
```

Confirms the strict grounding constraint works as intended: the model refuses to answer from outside knowledge, and the confidence score correctly drops to 0 since the retrieved chunks (about planning layers and orchestration) have no relevance to the question.

---

## Observations

- Confidence scores meaningfully track retrieval relevance — a completely unrelated question scores 0, a direct definitional match scores highest (0.6), and reasoning/synthesis questions land in between (~0.49).
- The system correctly refuses rather than hallucinates when the source document doesn't cover the topic.
- `context_chunks` are included in every response for transparency — the caller can always verify what the answer is grounded in.
