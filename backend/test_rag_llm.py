from app.services.rag_service import answer_question


def main():
    print("\n========== SYNTRIX RAG TEST ==========\n")

    question = input("Ask a question: ")

    print("\nGenerating answer...\n")

    answer = answer_question(question)

    print("=" * 60)
    print(answer)
    print("=" * 60)


if __name__ == "__main__":
    main()