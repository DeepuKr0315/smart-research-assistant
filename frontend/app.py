import gradio as gr
from backend.parser import read_document
from backend.summarizer import generate_summary
from backend.qa_engine import answer_question
from backend.challenge_engine import generate_questions, evaluate_answer
from gradio.themes.base import Soft

theme = Soft()

def handle_upload(file):
    try:
        if file.name.endswith('.pdf'):
            text = read_document(file.name)
        elif file.name.endswith('.txt'):
            with open(file.name, 'r', encoding='utf-8') as f:
                text = f.read()
        else:
            return "❌ Unsupported file format. Please upload PDF or TXT.", "", []

        summary_data = generate_summary(text)
        summary = summary_data.get("summary", "⚠️ Summary generation failed.")
        return summary, text, []

    except Exception as e:
        return f"❌ Error: {str(e)}", "", []

def ask_anything(history, question, context):
    if not context or context.startswith("❌") or not question.strip():
        return history + [["Please upload a valid document and enter a question.", None]]

    result = answer_question(question, context)
    answer = result.get("answer", "⚠️ No answer returned.")
    justification = result.get("justification", "")
    history.append([question, f"{answer}\n\n📌 {justification}"])
    return history

def get_challenge_questions(context):
    if not context or context.startswith("❌") or context.strip() == "":
        return "Please upload a valid document first."
    result = generate_questions(context)
    return result.get("questions", "⚠️ No questions generated.")

def check_challenge_answer(question, answer, context):
    if not context or context.startswith("❌") or context.strip() == "":
        return "Please upload a valid document first."
    result = evaluate_answer(question, answer, context)
    return result.get("feedback", "⚠️ No feedback generated.")

# Final UI
with gr.Blocks(title="📚 Smart Research Assistant", theme=theme) as interface:
    gr.Markdown("""
    # 📚 Smart Research Assistant
    Upload your research paper and explore intelligent AI interaction.
    """)
    
    full_text_state = gr.State("")
    history_state = gr.State([])

    # Upload
    with gr.Row():
        file_input = gr.File(label="📄 Upload Document (.pdf or .txt)", type="filepath")
    
    summary_output = gr.Textbox(label="📝 Auto Summary", lines=5, interactive=False)

    with gr.Tabs():
        with gr.TabItem("❓ Ask Anything"):
            with gr.Row():
                with gr.Column(scale=2):
                    chat = gr.Chatbot(label="💬 Conversation History")
                with gr.Column(scale=1):
                    question_input = gr.Textbox(placeholder="e.g. What is the main finding?")
                    ask_btn = gr.Button("📨 Ask")

        with gr.TabItem("🧠 Challenge Me"):
            with gr.Column():
                gen_btn = gr.Button("🧠 Generate Questions")
                question_box = gr.Textbox(label="🧪 AI-Generated Question", lines=6)
                user_answer = gr.Textbox(label="🧍 Your Answer", lines=2)
                eval_btn = gr.Button("✅ Evaluate Answer")
                feedback_box = gr.Textbox(label="💡 Feedback", lines=3)

    # Upload event
    file_input.upload(
        fn=handle_upload,
        inputs=file_input,
        outputs=[summary_output, full_text_state, history_state]
    )

    # Ask Anything event
    ask_btn.click(
        fn=ask_anything,
        inputs=[history_state, question_input, full_text_state],
        outputs=[history_state]
    ).then(lambda x: x, inputs=history_state, outputs=chat)

    # Challenge event
    gen_btn.click(fn=get_challenge_questions, inputs=full_text_state, outputs=question_box)
    eval_btn.click(fn=check_challenge_answer, inputs=[question_box, user_answer, full_text_state], outputs=feedback_box)

    gr.Markdown("---\n🔗 Built with ❤️ by Deepanshu Kumar")

if __name__ == "__main__":
    interface.launch()