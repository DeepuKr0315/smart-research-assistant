import gradio as gr
from backend.parser import read_document
from backend.summarizer import generate_summary
from backend.qa_engine import answer_question
from backend.challenge_engine import generate_questions, evaluate_answer
from gradio.themes import Soft

theme = Soft()

# --- Core Logic Functions ---

def handle_upload(file):
    try:
        if file.name.endswith('.pdf'):
            text = read_document(file.name)
        elif file.name.endswith('.txt'):
            with open(file.name, 'r', encoding='utf-8') as f:
                text = f.read()
        else:
            return "❌ Unsupported file format. Please upload a PDF or TXT.", ""

        summary_data = generate_summary(text)
        summary = summary_data.get("summary", "⚠️ Summary generation failed.")
        return summary, text

    except Exception as e:
        return f"❌ Error processing file: {str(e)}", ""

def ask_anything(history, question, context):
    if not context or context.startswith("❌") or context.strip() == "":
        return history + [["Please upload a valid document first.", None]]
    
    result = answer_question(question, context)
    answer = result["answer"]
    justification = result.get("justification", "")
    history.append([question, f"{answer}\n\n{justification}"])
    return history

def get_challenge_questions(context):
    if not context or context.startswith("❌") or context.strip() == "":
        return "Please upload a valid document first."
    
    result = generate_questions(context)
    return result["questions"]

def check_challenge_answer(question, answer, context):
    if not context or context.startswith("❌") or context.strip() == "":
        return "Please upload a valid document first."
    
    result = evaluate_answer(question, answer, context)
    return result["feedback"]

# --- Gradio UI ---
with gr.Blocks(title="📚 Smart Assistant for Research", theme=theme) as interface:
    gr.Markdown("""
    <div style="text-align:center;">
        <h1>📚 Smart Assistant for Research</h1>
        <p><strong>Upload a research paper and ask questions, generate summaries, or test your understanding!</strong></p>
    </div>
    """)

    # States
    full_text_state = gr.State("")
    history_state = gr.State([])

    with gr.Row():
        doc_upload = gr.File(label="📄 Upload PDF or TXT", type="filepath")
    
    summary_box = gr.Textbox(label="📝 Auto Summary (≤150 words)", lines=6)

    with gr.Tabs():
        with gr.TabItem("❓ Ask Anything"):
            with gr.Row():
                with gr.Column(scale=2):
                    chat_history = gr.Chatbot(label="Conversation History")
                with gr.Column(scale=1):
                    question_input = gr.Textbox(placeholder="e.g., What is the methodology?", show_label=False)
                    send_btn = gr.Button("📨 Send")
        
        with gr.TabItem("🧪 Challenge Me"):
            question_box = gr.Textbox(label="🧠 Logic-Based Questions", lines=8)
            user_answer = gr.Textbox(label="Your Answer")
            eval_btn = gr.Button("✅ Evaluate Answer")
            feedback_box = gr.Textbox(label="🗣 Feedback", lines=4)
            generate_btn = gr.Button("🔁 Generate Questions")

    # Events
    doc_upload.upload(
        fn=handle_upload,
        inputs=doc_upload,
        outputs=[summary_box, full_text_state]
    )

    send_btn.click(
        fn=ask_anything,
        inputs=[history_state, question_input, full_text_state],
        outputs=[history_state]
    ).then(
        lambda x: x, inputs=history_state, outputs=chat_history
    )

    generate_btn.click(
        fn=get_challenge_questions,
        inputs=full_text_state,
        outputs=question_box
    )

    eval_btn.click(
        fn=check_challenge_answer,
        inputs=[question_box, user_answer, full_text_state],
        outputs=feedback_box
    )

    gr.Markdown("---\nMade with ❤️ by Deepanshu Kumar")

if __name__ == "__main__":
    interface.launch()