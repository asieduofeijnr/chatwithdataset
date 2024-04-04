# Chat with your Dataset

This project demonstrates a web-based application to query a dataset through natural language.

![Screenshot 2024-03-18 at 12 51 23 PM](https://github.com/asieduofeijnr/chatwithdataset/assets/114332208/d6def335-e682-4841-b06a-91a071cf7617)

<img width="829" alt="Screenshot 2024-04-04 at 12 24 15 AM" src="https://github.com/asieduofeijnr/chatwithdataset/assets/114332208/7d30f142-3467-4f03-a968-71ff2cba111f">


For this purpose, it uses:

- [Streamlit](https://streamlit.io/): Streamlit is used to create the user interface for the web app. It provides an easy-to-use framework for building interactive web applications with Python.
- [PandasAI](https://pandas-ai.com/): PandasAI is integrated into the web app to generate Pandas code from user queries. It utilizes [OpenAI GPT-3.5](https://platform.openai.com/docs/api-reference) for natural language processing and code generation.
- [Hugging Face](https://huggingface.co/): Hugging Face's models are incorporated for various NLP tasks within the web app. This includes tasks such as text classification, sentiment analysis, etc.
- [LLama index](https://github.com/LLNL/LLAMA): LLama index is used for semantic search and similarity matching in the web app. It provides tools for building semantic search engines and performing similarity search on large-scale text data.

## Download dataset

Jobsy produces data when result is queried
VISEM application requires you to use VISEM app from www.visemgh.org. [Contact for more details]
LLM Proeject requires you to upload pdf or txt file.

## Run the project

If you don't have a Python environment available, you can use the [conda package manager](https://docs.conda.io/projects/conda/en/latest/index.html) which comes with the [Anaconda distribution](https://www.anaconda.com/download) to manage a clean Python environment.

Create a new environment and activate it:

```sh
conda create -n streamlit-pandasai python=3.9
conda activate streamlit-pandasai
```

Install Python dependencies in the activate Python environment:

```sh
pip install -r requirements.txt
```

Create a [new API key](https://platform.openai.com/account/api-keys) and set it to the `OPENAI_API_KEY` environment variable beforehand.

![Screenshot 2024-03-18 at 12 49 46 PM](https://github.com/asieduofeijnr/chatwithdataset/assets/114332208/92695a29-4f85-4481-9c26-0bce45863bc2)



On Windows:

```bash
set OPENAI_API_KEY="sk-..."
```

On Unix:

```sh
export OPENAI_API_KEY="sk-..."
```

Run the Streamlit project:

```sh
streamlit run streamlit_app.py
```
