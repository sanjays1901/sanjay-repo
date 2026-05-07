from services.retrieval_service import retrieve_chunks
from services.prompt_service import build_prompt
from services.llm_service import generate_answer


def ask_question(query, tenant_id="default", history=None):

    if history is None:
        history = []

    # Retrieve chunks
    rows = retrieve_chunks( query, tenant_id)
    if not rows:
        return {
            "answer": "I could not find this in knowledge base.",
            "sources": []
        }

    # Build context
    context = "\n\n".join([f"SOURCE: {row.meta.get('source')}\nCONTENT: {row.content}" for row in rows])

    # Build prompt
    prompt = build_prompt(context, query)

    # Build messages
    messages = history + [{"role": "user", "content": prompt}]

    # Generate answer
    answer = generate_answer(messages)

    return {
        "answer": answer,
        "sources": [{"source": row.meta, "distance": row.distance} for row in rows]
    }