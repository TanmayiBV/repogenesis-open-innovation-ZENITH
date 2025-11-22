import gradio as gr

def create_header():
    '''Create application header'''
    return gr.Markdown('### 🌾 KRISHI SAHAYA 2.0 | Intelligent Farming OS')

def create_footer():
    '''Create application footer'''
    return gr.HTML('''
        <div style='text-align: center; padding: 20px; margin-top: 30px; 
                    border-top: 2px solid rgba(46, 125, 50, 0.3); color: #81c784;'>
            <p>🌾 <strong>Krishi Sahaya 2.0</strong> | Built with ❤️ for Karnataka Farmers</p>
        </div>
    ''')
