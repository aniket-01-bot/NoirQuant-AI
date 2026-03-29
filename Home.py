import streamlit as st

def main():
    st.set_page_config(
        page_title="NoirQuant AI",
        # page_icon="🖤",
        layout="wide"
    )

    # Strong Black Theme CSS
    st.markdown("""
        <style>
        /* Full black background */
        .stApp {
            background-color: #000000;
            color: white;
        }

        .title {
            text-align: center;
            font-size: 52px;
            font-weight: bold;
            color: #00ffd5;
            letter-spacing: 2px;
        }

        .subtitle {
            text-align: center;
            font-size: 20px;
            color: #bbbbbb;
            margin-bottom: 40px;
        }

        .card {
            background: linear-gradient(145deg, #0f0f0f, #1a1a1a);
            padding: 25px;
            border-radius: 18px;
            box-shadow: 0px 0px 20px rgba(0,255,213,0.1);
            margin: 15px;
            color: white;
            transition: 0.3s;
        }

        .card:hover {
            transform: translateY(-5px);
            box-shadow: 0px 0px 25px rgba(0,255,213,0.3);
        }

        .card h3 {
            color: #00ffd5;
        }

        .button-container {
            display: flex;
            justify-content: center;
            gap: 60px;
            margin-top: 50px;
        }

        .project-button {
            padding: 15px 45px;
            font-size: 18px;
            background: linear-gradient(135deg, #00ffd5, #0066ff);
            color: black;
            border: none;
            border-radius: 40px;
            cursor: pointer;
            transition: 0.3s;
            font-weight: bold;
        }

        .project-button:hover {
            transform: scale(1.1);
            background: linear-gradient(135deg, #0066ff, #00ffd5);
        }
        </style>
    """, unsafe_allow_html=True)

    # Title
    st.markdown('<div class="title">NoirQuant AI</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Next-Gen Financial Intelligence Engine</div>', unsafe_allow_html=True)

    # Cards
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
            <div class="card">
                <h3> News Analyzer</h3>
                <p>
                Decode financial news with precision using AI-driven insights.
                Identify trends, sentiment, and market impact instantly.
                </p>
            </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
            <div class="card">
                <h3> PDF Chat Bot</h3>
                <p>
                Interact with financial documents effortlessly.
                Extract deep insights and accelerate your research workflow.
                </p>
            </div>
        """, unsafe_allow_html=True)

    # Buttons
    st.markdown(f'''
        <div class="button-container">
            <a target="_self" href="http://localhost:8501/URL">
                <button class="project-button"> Launch News Analyzer</button>
            </a>
            <a target="_self" href="http://localhost:8501/PDF">
                <button class="project-button"> Open PDF Chat Bot</button>
            </a>
        </div>
    ''', unsafe_allow_html=True)


if __name__ == "__main__":
    main()